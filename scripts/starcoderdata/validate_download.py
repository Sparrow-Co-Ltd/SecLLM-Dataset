# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Validate the output of download_starcoderdata.py (standard library only).

See scripts/starcoderdata/README.md for usage.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


DEFAULT_OUTPUT_DIR = Path("starcoderdata")

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


def normalize_language(language: str) -> str:
    normalized = language.strip().lower().replace("_", "-")
    return LANGUAGE_ALIASES.get(normalized, normalized)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate extracted StarCoderData output.")
    parser.add_argument("--language", "-l", required=True, help="Language slug to validate.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory containing starcoderdata output.",
    )
    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="Expected maximum extracted source files. Used as an upper-bound check.",
    )
    parser.add_argument(
        "--allow-empty",
        action="store_true",
        help="Allow source files with zero bytes.",
    )
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="Write validation.json under the language output directory.",
    )
    return parser.parse_args()


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def main() -> int:
    args = parse_args()
    language = normalize_language(args.language)
    extension = EXT_MAP.get(language, ".txt")
    language_dir = args.output_dir / language
    src_dir = language_dir / "src_code"

    errors: list[str] = []
    parquet_files = sorted(language_dir.glob("*.parquet"))
    source_files = sorted(src_dir.rglob(f"*{extension}")) if src_dir.exists() else []

    if not language_dir.exists():
        errors.append(f"Missing language directory: {language_dir}")
    if not parquet_files:
        errors.append(f"No parquet files found in: {language_dir}")
    if not src_dir.exists():
        errors.append(f"Missing source directory: {src_dir}")
    if not source_files:
        errors.append(f"No source files with extension {extension} found in: {src_dir}")
    if args.max_rows is not None and len(source_files) > args.max_rows:
        errors.append(
            f"Source file count {len(source_files)} exceeds --max-rows {args.max_rows}."
        )
    if not args.allow_empty:
        empty_files = [path for path in source_files if path.stat().st_size == 0]
        if empty_files:
            preview = ", ".join(str(path) for path in empty_files[:5])
            errors.append(f"Found {len(empty_files)} empty source file(s): {preview}")

    print(f"Language: {language}")
    print(f"Parquet files: {len(parquet_files)}")
    print(f"Source files: {len(source_files)}")
    print(f"Source extension: {extension}")

    report = {
        "language": language,
        "language_dir": str(language_dir),
        "src_dir": str(src_dir),
        "parquet_files": len(parquet_files),
        "source_files": len(source_files),
        "source_extension": extension,
        "max_rows": args.max_rows,
        "allow_empty": args.allow_empty,
        "status": "failed" if errors else "passed",
        "errors": errors,
        "validated_at": now_iso(),
    }

    if args.write_report:
        language_dir.mkdir(parents=True, exist_ok=True)
        report_path = language_dir / "validation.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Validation report: {report_path}")

    if errors:
        for error in errors:
            print(f"Error: {error}", file=sys.stderr)
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
