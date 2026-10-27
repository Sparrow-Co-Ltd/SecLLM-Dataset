#!/usr/bin/env python3
"""학습된 어댑터 생성 스모크 테스트 (read_code / edit_code / submit_fix 3도구 형식).

Qwen3.5 계열 SFT 후 툴콜 생성이 `<tool_call><|im_end|>` 로 절단되는 보고가 있어
(ms-swift #9234), val 궤적의 세 지점에서 다음 턴을 생성해 검증한다.
  T1 첫 턴:   system+user 만 주고 → 완결된 read_code 또는 edit_code 툴콜이 나오는가
  T2 편집 턴: 마지막 edit_code 직전까지 주고 → old_string/new_string 이 채워진
              완결된 edit_code 툴콜이 나오는가
  T3 제출 턴: 마지막 assistant(submit_fix) 직전까지 주고 → 한국어 desc(≤300자)를
              담은 완결된 submit_fix 툴콜이 나오는가
모든 턴은 툴콜을 정확히 1개만 내야 한다(학습 데이터의 어시스턴트 턴은 전부 호출 1개).
T2 는 교사가 편집 전에 한 턴 이상 진행한 궤적에서만 검사한다(아니면 SKIP).

val 은 train/sft/select/export_sft.py 출력 형식(마지막 메시지가 submit_fix 호출)을
전제한다. 프롬프트는 학습 마스킹과 같이 enable_thinking=False 로 렌더링한다.
결과는 <adapter>/smoke_test.json 에 [{test, idx, dataset_id, language, result}] 로 남는다.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from itertools import zip_longest
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

TOOL_CALL_RE = re.compile(r"<tool_call>\s*<function=(\w+)>(.*?)</function>\s*</tool_call>", re.S)
PARAM_RE = re.compile(r"<parameter=(\w+)>\n(.*?)\n</parameter>", re.S)
HANGUL_RE = re.compile(r"[가-힣]")
DESC_MAX_CHARS = 300  # submit_fix desc 상한 (하네스 시스템 프롬프트)
DEFAULT_VAL = "datas/sft/select/export/val.jsonl"


def parse_single_call(text: str, allowed: set[str]) -> tuple[str, dict[str, str]] | str:
    """완결된 툴콜 1개를 (name, params) 로, 아니면 실패 사유 문자열을 돌려준다."""
    calls = TOOL_CALL_RE.findall(text)
    if not calls:
        return f"완결된 툴콜 블록 없음: {text[:120]!r}"
    if len(calls) > 1:
        return f"툴콜 {len(calls)}개 (1개여야 함)"
    name, body = calls[0]
    if name not in allowed:
        return f"예상 밖 도구 {name!r} (허용: {sorted(allowed)})"
    return name, dict(PARAM_RE.findall(body))


def check_read(params: dict[str, str]) -> str | None:
    for key in ("offset", "limit"):
        if key in params and not params[key].strip().isdigit():
            return f"read_code {key} 가 정수가 아님: {params[key][:20]!r}"
    return None


def check_edit(params: dict[str, str]) -> str | None:
    missing = {"old_string", "new_string"} - params.keys()
    if missing:
        return f"edit_code 파라미터 누락: {sorted(missing)}"
    if not params["old_string"].strip():
        return "old_string 이 비어 있음"
    if params["old_string"] == params["new_string"]:
        return "old_string 과 new_string 이 같음 (no-op)"
    if re.match(r"^\s*\d+: ", params["old_string"]):
        return "old_string 에 줄 번호 접두가 포함됨"
    return None


def check_submit(params: dict[str, str]) -> str | None:
    desc = params.get("desc", "").strip()
    if not desc:
        return "submit_fix desc 가 비어 있음"
    if len(desc) > DESC_MAX_CHARS:
        return f"desc 가 {len(desc)}자 (≤{DESC_MAX_CHARS})"
    if not HANGUL_RE.search(desc):
        return f"desc 가 한국어가 아님: {desc[:60]!r}"
    return None


def check(text: str, allowed: set[str]) -> str | None:
    parsed = parse_single_call(text, allowed)
    if isinstance(parsed, str):
        return parsed
    name, params = parsed
    return {"read_code": check_read, "edit_code": check_edit, "submit_fix": check_submit}[name](params)


def called(message: dict, name: str) -> bool:
    return any(tc["function"]["name"] == name for tc in message.get("tool_calls") or [])


def pick_rows(rows: list[dict], n: int) -> list[dict]:
    """언어별 라운드로빈으로 n 개 (val 은 dataset/idx 순 정렬이라 앞부분이 한 언어로 몰린다)."""
    by_lang: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        by_lang[row.get("language", "?")].append(row)
    ordered = [r for group in zip_longest(*by_lang.values()) for r in group if r is not None]
    return ordered[:n]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--adapter", required=True, help="adapters/<run_name>")
    p.add_argument("--val-file", default=DEFAULT_VAL)
    p.add_argument("--n", type=int, default=6, help="검사할 val 궤적 수 (언어별 라운드로빈)")
    p.add_argument("--max-new-tokens", type=int, default=2048)
    args = p.parse_args()

    tok = AutoTokenizer.from_pretrained(args.adapter)
    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen3.5-9B", dtype=torch.bfloat16, device_map="cuda:0"
    )
    model = PeftModel.from_pretrained(model, args.adapter)
    model.eval()

    rows = pick_rows([json.loads(l) for l in open(args.val_file, encoding="utf-8")], args.n)
    results: list[dict] = []
    # 턴은 <|im_end|> 에서 끝난다. 베이스 체크포인트에 generation_config.json 이 없으면
    # generate() 가 config 의 eos(<|endoftext|>)만 보고 멈추지 않아, 모델이 도구 결과와
    # 다음 턴까지 이어 쓴다. 두 토큰 모두에서 멈추도록 명시한다.
    stop_ids = [tok.convert_tokens_to_ids("<|im_end|>"), tok.convert_tokens_to_ids("<|endoftext|>")]

    def generate(messages, tools):
        prompt = tok.apply_chat_template(
            messages, tools=tools, tokenize=False,
            add_generation_prompt=True, enable_thinking=False,
        )
        ids = tok(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            out = model.generate(
                **ids, max_new_tokens=args.max_new_tokens,
                do_sample=False, pad_token_id=tok.pad_token_id, eos_token_id=stop_ids,
            )
        return tok.decode(out[0][ids.input_ids.shape[1]:], skip_special_tokens=True).strip()

    def record(test: str, row: dict, err: str | None, skipped: str | None = None) -> None:
        result = f"SKIP: {skipped}" if skipped else ("PASS" if err is None else f"FAIL: {err}")
        results.append({
            "test": test, "idx": row["idx"], "dataset_id": row.get("dataset_id"),
            "language": row.get("language"), "result": result,
        })
        print(f"{test} {row.get('dataset_id')}:{row['idx']} ({row.get('language')}): {results[-1]['result']}")

    for row in rows:
        ms, tools = row["messages"], row["tools"]
        if not (ms[-1]["role"] == "assistant" and called(ms[-1], "submit_fix")):
            record("T0-format", row, "마지막 메시지가 submit_fix 호출이 아님 (export_sft.py 출력인지 확인)")
            continue

        # T1: 첫 턴 (system + user 만)
        record("T1-first", row, check(generate(ms[:2], tools), {"read_code", "edit_code"}))

        # T2: 마지막 edit_code 턴 직전까지. 교사가 첫 턴에 바로 편집한 궤적은 이 프롬프트가
        # T1 과 같아서(system+user) read_code 로 시작하는 것도 정상 행동이므로 건너뛴다.
        edit_at = max(i for i, m in enumerate(ms) if m["role"] == "assistant" and called(m, "edit_code"))
        if edit_at > 2:
            record("T2-edit", row, check(generate(ms[:edit_at], tools), {"edit_code"}))
        else:
            record("T2-edit", row, None, skipped="교사의 첫 턴이 edit_code (T1 과 같은 프롬프트)")

        # T3: 마지막 submit_fix 턴 직전까지 (edit OK 응답을 본 뒤)
        record("T3-submit", row, check(generate(ms[:-1], tools), {"submit_fix"}))

    n_pass = sum(1 for r in results if r["result"] == "PASS")
    n_run = sum(1 for r in results if not r["result"].startswith("SKIP"))
    print(f"\n결과: {n_pass}/{n_run} PASS (건너뜀 {len(results) - n_run})")
    out = Path(args.adapter) / "smoke_test.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"기록: {out}")


if __name__ == "__main__":
    main()
