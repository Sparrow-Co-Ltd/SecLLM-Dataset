#!/usr/bin/env python3
"""학습 전 sanity check: chat template 렌더링 + assistant 라벨 마스킹 검증.

train_sft.py 와 같은 srft_masking.evaluate_example() 로 토큰화하므로, 여기서 모든 행이
ready 로 나오면 학습 입력이 의도대로 만들어진 것이다. 출력의 "학습 신호 비율"은
전체 토큰 중 손실이 걸리는 어시스턴트 토큰의 비율이다.
"""

from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter
from pathlib import Path

from srft_masking import evaluate_example
from transformers import AutoTokenizer


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--data", default="datas/sft/select/export/train.jsonl")
    p.add_argument("--model", default="Qwen/Qwen3.5-9B")
    p.add_argument("--max-length", type=int, default=12288)
    p.add_argument("--show", type=int, default=1, help="렌더링 결과를 출력할 샘플 수")
    p.add_argument("--report", type=Path, help="Write per-row token eligibility JSON")
    p.add_argument("--local-files-only", action="store_true")
    args = p.parse_args()

    tok = AutoTokenizer.from_pretrained(args.model, local_files_only=args.local_files_only)
    if "generation %}" in (tok.chat_template or ""):
        print("NOTE: 템플릿에 {% generation %} 마커가 있음 -> TRL assistant_only_loss 사용 가능")
    else:
        print("NOTE: {% generation %} 마커 없음 -> 수동 마스킹 경로가 맞음")

    with open(args.data, encoding="utf-8") as stream:
        rows = [json.loads(line) for line in stream]
    tot, tgt, results = [], [], []

    for n, row in enumerate(rows):
        result = evaluate_example(row, tok, args.max_length)
        results.append({"row_index": n, "training_status": result.training_status,
                        "reason": result.reason, "token_count": result.token_count,
                        "supervised_tokens": result.supervised_tokens})
        ex = result.example
        if ex is None:
            continue
        ids, labels = ex["input_ids"], ex["labels"]
        assert len(ids) == len(labels), "input_ids/labels 길이 불일치"
        n_tgt = sum(1 for x in labels if x != -100)
        assert n_tgt > 0, "학습 대상 토큰이 0개"
        tot.append(len(ids))
        tgt.append(n_tgt)

        if n < args.show:
            print("=" * 70)
            print(tok.decode(ids))
            print("-" * 30, "LOSS 대상 구간만 디코딩", "-" * 30)
            print(tok.decode([i for i, l in zip(ids, labels) if l != -100]))
            print("=" * 70)

    counts = dict(Counter(item["training_status"] for item in results))
    print(f"dispositions: {json.dumps(counts, sort_keys=True)}")
    if args.report:
        args.report.write_text(json.dumps({"counts": counts, "rows": results}, indent=2) + "\n")
    if counts.get("invalid_annotations"):
        raise SystemExit("invalid SRFT annotations; see dispositions/report")
    if not tot:
        print("No trainable rows")
        return
    def q(values: list[int], ratio: float) -> int:
        return sorted(values)[int(len(values) * ratio)]

    print(f"검증 통과: {len(tot)}건")
    print(f"TOTAL  p50={q(tot, .5)} p90={q(tot, .9)} p99={q(tot, .99)} max={max(tot)}")
    print(f"TARGET p50={q(tgt, .5)} p90={q(tgt, .9)} max={max(tgt)} mean={statistics.mean(tgt):.0f}")
    print(f"학습 신호 비율: {100 * sum(tgt) / sum(tot):.1f}%  (총 target 토큰 {sum(tgt):,})")


if __name__ == "__main__":
    main()
