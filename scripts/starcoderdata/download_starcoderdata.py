# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "huggingface-hub>=0.23",
#     "pandas>=2.0",
#     "pyarrow>=14.0",
#     "python-dotenv>=1.0",
#     "tqdm>=4.66",
# ]
# ///
"""Download bigcode/starcoderdata parquet files and extract one source file per row.

Run with `uv run scripts/starcoderdata/download_starcoderdata.py --help`.
See scripts/starcoderdata/README.md for usage and output layout.
"""

from __future__ import annotations

import argparse
import difflib
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq
from dotenv import load_dotenv
from huggingface_hub import hf_hub_download, list_repo_files
from huggingface_hub.errors import HFValidationError, LocalTokenNotFoundError, OfflineModeIsEnabled
from huggingface_hub.utils import httpx
from pyarrow import ArrowException
from tqdm import tqdm


DEFAULT_REPO_ID = "bigcode/starcoderdata"
DEFAULT_OUTPUT_DIR = Path("starcoderdata")
DEFAULT_SRC_CHUNK = 1000

EXT_MAP = {
    "c": ".c",
    "cpp": ".cpp",
    "c-sharp": ".cs",
    "dart": ".dart",
    "go": ".go",
    "html": ".html",
    "java": ".java",
    "java-server-pages": ".jsp",
    "javascript": ".js",
    "kotlin": ".kt",
    "php": ".php",
    "python": ".py",
    "ruby": ".rb",
    "rust": ".rs",
    "sql": ".sql",
    "swift": ".swift",
    "typescript": ".ts",
    "visual-basic": ".vb",
    "xslt": ".xsl",
}

# StarCoderData prepends repository/file metadata as a leading line using these
# special tokens. Only such a line should be stripped from `content`; real source
# code that legitimately starts with "<" (HTML/JSX, EJS templates, `<!DOCTYPE>`,
# git conflict markers, ...) must be preserved.
STARCODER_HEADER_PREFIXES = (
    "<reponame>",
    "<gh_stars>",
    "<filename>",
    "<gh_path>",
    "<empty_output>",
    "<commit_before>",
    "<commit_msg>",
    "<commit_after>",
    "<issue_start>",
    "<issue_comment>",
    "<issue_closed>",
    "<jupyter_start>",
    "<jupyter_text>",
    "<jupyter_code>",
    "<jupyter_output>",
    "<fim_prefix>",
    "<fim_middle>",
    "<fim_suffix>",
    "<fim_pad>",
)

LANGUAGE_ALIASES = {
    "cs": "c-sharp",
    "csharp": "c-sharp",
    "c#": "c-sharp",
    "c++": "cpp",
    "js": "javascript",
    "jsp": "java-server-pages",
    "kt": "kotlin",
    "py": "python",
    "rb": "ruby",
    "rs": "rust",
    "ts": "typescript",
    "vb": "visual-basic",
    "vbs": "visual-basic",
    "xsl": "xslt",
}


@dataclass(frozen=True)
class Config:
    repo_id: str
    language: str
    max_parquet: int | None
    max_rows: int
    output_dir: Path
    src_chunk: int
    token: str
    dry_run: bool
    list_languages: bool

    @property
    def language_dir(self) -> Path:
        return self.output_dir / self.language

    @property
    def src_dir(self) -> Path:
        return self.language_dir / "src_code"

    @property
    def extension(self) -> str:
        return EXT_MAP.get(self.language, ".txt")

    @property
    def manifest_path(self) -> Path:
        return self.language_dir / "manifest.json"

    @property
    def src_manifest_path(self) -> Path:
        return self.src_dir / "manifest.json"


@dataclass(frozen=True)
class ParquetInfo:
    repo_file: str
    local_path: Path
    rows: int
    size_bytes: int
    global_start: int
    global_end: int


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download StarCoderData parquet files and extract source files."
    )
    parser.add_argument("--language", "-l", default="c", help="Language slug to download.")
    parser.add_argument(
        "--max-parquet",
        "-p",
        type=int,
        default=5,
        help="Maximum parquet files to download. Use 0 for all files.",
    )
    parser.add_argument(
        "--max-rows",
        "-r",
        type=int,
        default=5000,
        help="Maximum source rows to extract.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where starcoderdata output is written.",
    )
    parser.add_argument(
        "--repo-id",
        default=DEFAULT_REPO_ID,
        help="HuggingFace dataset repository id.",
    )
    parser.add_argument(
        "--src-chunk",
        type=int,
        default=DEFAULT_SRC_CHUNK,
        help="Number of source files per chunk directory.",
    )
    parser.add_argument(
        "--token-env",
        default="HF_TOKEN",
        help="Environment variable containing the HuggingFace token.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Verify repo access and language availability without downloading.",
    )
    parser.add_argument(
        "--list-languages",
        action="store_true",
        help="Print available language slugs and exit without downloading.",
    )
    return parser.parse_args()


def normalize_language(language: str) -> str:
    normalized = language.strip().lower().replace("_", "-")
    return LANGUAGE_ALIASES.get(normalized, normalized)


def build_config(args: argparse.Namespace) -> Config:
    load_dotenv(Path.cwd() / ".env")

    if args.max_parquet < 0:
        raise ValueError("--max-parquet must be 0 or greater.")
    if args.max_rows < 1:
        raise ValueError("--max-rows must be 1 or greater.")
    if args.src_chunk < 1:
        raise ValueError("--src-chunk must be 1 or greater.")

    token = os.environ.get(args.token_env)
    if not token:
        raise ValueError(
            f"{args.token_env} is not set. Export it or add {args.token_env}=hf_... to .env "
            "in the current directory."
        )

    return Config(
        repo_id=args.repo_id,
        language=normalize_language(args.language),
        max_parquet=None if args.max_parquet == 0 else args.max_parquet,
        max_rows=args.max_rows,
        output_dir=args.output_dir,
        src_chunk=args.src_chunk,
        token=token,
        dry_run=args.dry_run,
        list_languages=args.list_languages,
    )


def fetch_repo_files(config: Config) -> list[str]:
    try:
        return list_repo_files(
            config.repo_id,
            repo_type="dataset",
            token=config.token,
        )
    except (
        httpx.HTTPError,
        HFValidationError,
        LocalTokenNotFoundError,
        OfflineModeIsEnabled,
    ) as exc:
        raise RuntimeError(
            "Failed to list HuggingFace dataset files. Check HF_TOKEN, gated dataset "
            f"access, repo id, and network connectivity. Original error: {exc}"
        ) from exc


def available_languages(repo_files: list[str]) -> list[str]:
    return sorted(
        {
            repo_file.split("/", 1)[0]
            for repo_file in repo_files
            if "/" in repo_file and repo_file.endswith(".parquet")
        }
    )


def validate_language_exists(repo_files: list[str], language: str) -> list[str]:
    parquet_files = sorted(
        repo_file
        for repo_file in repo_files
        if repo_file.startswith(f"{language}/") and repo_file.endswith(".parquet")
    )
    if parquet_files:
        return parquet_files

    languages = available_languages(repo_files)
    suggestions = difflib.get_close_matches(language, languages, n=3)
    suggestion_text = f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
    raise ValueError(
        f"No parquet files found for language '{language}'.{suggestion_text}\n"
        f"Available languages: {', '.join(languages)}"
    )


def select_target_files(parquet_files: list[str], max_parquet: int | None) -> list[str]:
    return parquet_files if max_parquet is None else parquet_files[:max_parquet]


def local_path_for_repo_file(config: Config, repo_file: str) -> Path:
    return config.output_dir / repo_file


def row_count(parquet_file: Path) -> int:
    return pq.ParquetFile(parquet_file).metadata.num_rows


def build_parquet_inventory(config: Config, target_files: list[str]) -> list[ParquetInfo]:
    inventory: list[ParquetInfo] = []
    global_start = 0
    for repo_file in target_files:
        local_path = local_path_for_repo_file(config, repo_file)
        if not local_path.exists():
            continue
        rows = row_count(local_path)
        global_end = global_start + rows - 1 if rows else global_start - 1
        inventory.append(
            ParquetInfo(
                repo_file=repo_file,
                local_path=local_path,
                rows=rows,
                size_bytes=local_path.stat().st_size,
                global_start=global_start,
                global_end=global_end,
            )
        )
        global_start += rows
    return inventory


def inventory_total_rows(inventory: list[ParquetInfo]) -> int:
    return sum(item.rows for item in inventory)


def download_parquet_files(config: Config, target_files: list[str]) -> tuple[list[ParquetInfo], list[str]]:
    print(f"[1/2] Ensuring local parquet rows for '{config.language}'.")
    downloaded: list[str] = []
    inventory = build_parquet_inventory(config, target_files)

    if inventory_total_rows(inventory) >= config.max_rows:
        print(
            f"Local parquet rows are sufficient: {inventory_total_rows(inventory)}/"
            f"{config.max_rows}. Skipping downloads."
        )
        return inventory, downloaded

    for repo_file in tqdm(target_files, unit="file"):
        if inventory_total_rows(inventory) >= config.max_rows:
            break
        if local_path_for_repo_file(config, repo_file).exists():
            continue
        hf_hub_download(
            repo_id=config.repo_id,
            repo_type="dataset",
            filename=repo_file,
            local_dir=config.output_dir,
            token=config.token,
        )
        downloaded.append(repo_file)
        inventory = build_parquet_inventory(config, target_files)

    return inventory, downloaded


def existing_source_indices(src_dir: Path, extension: str) -> set[int]:
    indices: set[int] = set()
    if not src_dir.exists():
        return indices

    for source_file in src_dir.rglob(f"*{extension}"):
        try:
            indices.add(int(source_file.stem))
        except ValueError:
            continue
    return indices


def clean_content(content: object) -> str:
    lines = str(content).splitlines(keepends=True)
    if lines and lines[0].startswith(STARCODER_HEADER_PREFIXES):
        lines = lines[1:]
    return "".join(lines)


def first_missing_index(existing_indices: set[int], max_rows: int) -> int | None:
    for index in range(max_rows):
        if index not in existing_indices:
            return index
    return None


def write_source_file(config: Config, index: int, content: object) -> None:
    chunk_dir = config.src_dir / f"{(index // config.src_chunk) * config.src_chunk:07d}"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    output_file = chunk_dir / f"{index:07d}{config.extension}"
    output_file.write_text(clean_content(content), encoding="utf-8")


def extract_source_files(
    config: Config,
    inventory: list[ParquetInfo],
) -> tuple[int, int, int | None]:
    print(f"[2/2] Extracting up to {config.max_rows} source file(s).")
    config.src_dir.mkdir(parents=True, exist_ok=True)

    existing_indices = existing_source_indices(config.src_dir, config.extension)
    created = 0
    start_index = first_missing_index(existing_indices, config.max_rows)

    if not inventory:
        raise FileNotFoundError(f"No local parquet files found in {config.language_dir}")
    if start_index is None:
        return created, len(existing_indices), max(existing_indices) if existing_indices else None

    for item in tqdm(inventory, unit="parquet"):
        if item.global_end < start_index:
            continue
        if item.global_start >= config.max_rows:
            break

        df = pd.read_parquet(item.local_path, columns=["content"])
        local_start = max(0, start_index - item.global_start)
        for local_index, content in enumerate(
            tqdm(df["content"].iloc[local_start:], leave=False, unit="row"),
            start=local_start,
        ):
            global_index = item.global_start + local_index
            if global_index >= config.max_rows:
                break
            if global_index not in existing_indices:
                write_source_file(config, global_index, content)
                created += 1
                existing_indices.add(global_index)

    last_index = max(existing_indices) if existing_indices else None
    return created, len(existing_indices) - created, last_index


def chunk_ranges(source_indices: list[int], chunk_size: int) -> list[tuple[int, int, int]]:
    if not source_indices:
        return []
    ranges: list[tuple[int, int, int]] = []
    for chunk_start in range(0, max(source_indices) + 1, chunk_size):
        chunk_end = chunk_start + chunk_size - 1
        count = sum(1 for index in source_indices if chunk_start <= index <= chunk_end)
        if count:
            ranges.append((chunk_start, min(chunk_end, max(source_indices)), count))
    return ranges


def parquet_spans_for_range(
    inventory: list[ParquetInfo],
    start_index: int,
    end_index: int,
) -> list[dict[str, object]]:
    spans: list[dict[str, object]] = []
    for item in inventory:
        if item.global_end < start_index or item.global_start > end_index:
            continue
        row_start = max(start_index, item.global_start) - item.global_start
        row_end = min(end_index, item.global_end) - item.global_start
        spans.append(
            {
                "repo_file": item.repo_file,
                "local_path": str(item.local_path),
                "row_start": row_start,
                "row_end": row_end,
            }
        )
    return spans


def write_manifests(
    config: Config,
    target_files: list[str],
    inventory: list[ParquetInfo],
    downloaded_files: list[str],
) -> None:
    source_indices = sorted(existing_source_indices(config.src_dir, config.extension))
    chunks = []
    for start_index, end_index, count in chunk_ranges(source_indices, config.src_chunk):
        chunk_name = f"{start_index:07d}"
        chunk_path = config.src_dir / chunk_name
        chunks.append(
            {
                "name": chunk_name,
                "path": str(chunk_path),
                "start_index": start_index,
                "end_index": end_index,
                "file_count": count,
                "ready_for_sast": count > 0 and chunk_path.exists(),
                "created_from": parquet_spans_for_range(inventory, start_index, end_index),
            }
        )

    config.src_manifest_path.write_text(
        json.dumps(
            {
                "language": config.language,
                "extension": config.extension,
                "src_chunk_size": config.src_chunk,
                "source_file_count": len(source_indices),
                "last_extracted_global_index": max(source_indices) if source_indices else None,
                "chunks": chunks,
                "updated_at": now_iso(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    local_rows = inventory_total_rows(inventory)
    config.manifest_path.write_text(
        json.dumps(
            {
                "language": config.language,
                "repo_id": config.repo_id,
                "target_parquet_files": target_files,
                "downloaded_parquet_files": downloaded_files,
                "local_parquet_files": [
                    {
                        "repo_file": item.repo_file,
                        "local_path": str(item.local_path),
                        "rows": item.rows,
                        "size_bytes": item.size_bytes,
                        "global_start": item.global_start,
                        "global_end": item.global_end,
                    }
                    for item in inventory
                ],
                "local_parquet_total_rows": local_rows,
                "max_rows_requested": config.max_rows,
                "total_extracted": len(source_indices),
                "last_extracted_global_index": max(source_indices) if source_indices else None,
                "truncated_by_max_rows": len(source_indices) >= config.max_rows
                and local_rows > len(source_indices),
                "exhausted_local_parquets": len(source_indices) < config.max_rows
                and len(source_indices) >= local_rows,
                "src_chunk_size": config.src_chunk,
                "src_manifest_path": str(config.src_manifest_path),
                "updated_at": now_iso(),
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def main() -> int:
    try:
        config = build_config(parse_args())
        repo_files = fetch_repo_files(config)
        languages = available_languages(repo_files)

        if config.list_languages:
            print("\n".join(languages))
            return 0

        parquet_files = validate_language_exists(repo_files, config.language)
        target_files = select_target_files(parquet_files, config.max_parquet)

        print(
            f"Language: {config.language} | parquet: {len(target_files)}/{len(parquet_files)} | "
            f"max rows: {config.max_rows} | output: {config.output_dir}"
        )

        if config.dry_run:
            print("Dry run complete. Repo access and language availability are valid.")
            return 0

        inventory, downloaded_files = download_parquet_files(config, target_files)
        created, skipped, last_index = extract_source_files(config, inventory)
        write_manifests(config, target_files, inventory, downloaded_files)
        print(f"Done. Created {created} source file(s); skipped {skipped} existing file(s).")
        print(f"Local parquet rows: {inventory_total_rows(inventory)}")
        print(f"Last extracted global index: {last_index}")
        print(f"Dataset manifest: {config.manifest_path}")
        print(f"Source manifest: {config.src_manifest_path}")
        print(f"Source directory: {config.src_dir}")
        return 0
    except (OSError, RuntimeError, ValueError, httpx.HTTPError, ArrowException) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
