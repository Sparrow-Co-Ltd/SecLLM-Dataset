#!/usr/bin/env python3
"""Qwen3.5-9B LoRA SFT — 보안 취약점 수정 툴콜 에이전트.

입력: train/sft/select/export_sft.py 가 만든 {train,val}.jsonl
      (read_code / edit_code / submit_fix 3도구 궤적, function.arguments 는 dict,
       어시스턴트 턴마다 툴콜 1개, 마지막 메시지는 submit_fix 호출).
      경로는 --train-file / --val-file 로 지정한다. 기본값은 작업 디렉터리 기준 선별 출력 경로다.

Qwen3.5 템플릿 특성 때문에 TRL 의 assistant_only_loss 를 쓰지 않는다.
  - 템플릿에 {% generation %} 마커가 없어서 assistant_only_loss 가 동작하지 않는다.
  - 그래서 턴 경계를 직접 렌더링해 char offset -> token index 로 라벨을 마스킹한다.
  - 툴콜이 JSON 이 아니라 <function=...><parameter=...> XML 로 렌더된다.
    arguments 를 dict 로 넘겨야 한다 (템플릿이 `arguments|items` 로 순회함).
  - assistant 턴은 항상 `<think>\n\n</think>\n\n` 로 시작하도록 렌더된다.
    add_generation_prompt=True + enable_thinking=False 와 정확히 일치하므로
    추론 시에도 enable_thinking=False 로 서빙해야 한다.
"""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import JsonValue
from srft_masking import IGNORE, AnnotationError, evaluate_example
from srft_masking import build_example as build_example  # noqa: PLC0414 - public compatibility export

if TYPE_CHECKING:
    from datasets import Dataset
    from transformers import PreTrainedTokenizerBase

# 시퀀스 길이 편차가 커서 생기는 메모리 단편화를 줄인다. torch 의 첫 CUDA 할당 전에 설정해야 한다.
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

# .env 의 자격증명(WANDB_API_KEY, HF_TOKEN)을 프로세스 환경으로 로드.
# 파이썬은 .env 를 자동으로 읽지 않으므로 여기서 직접 주입한다. 이미 설정된 값은 유지.
# 스크립트 위치(train/sft/)부터 위로 올라가며 처음 만나는 .env 를 쓴다.
_env = next(
    (p / ".env" for p in Path(__file__).resolve().parents if (p / ".env").exists()),
    None,
)
if _env is not None:
    for _line in _env.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _, _v = _line.partition("=")
            os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))
os.environ.setdefault("WANDB_PROJECT", "qwen35-secfix-sft")

import torch
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from transformers.trainer_pt_utils import LengthGroupedSampler

# ---------------------------------------------------------------- data


def load_rows(path: str | Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def prepare_dataset(
    rows: list[dict[str, JsonValue]], tok: PreTrainedTokenizerBase,
    max_length: int, num_proc: int, split: str,
) -> Dataset:
    """Keep original JSON intact until hash validation and token masking finish."""
    import datasets

    def tokenize_serialized(row):
        result = evaluate_example(json.loads(row["row_json"]), tok, max_length)
        if result.training_status == "invalid_annotations":
            raise AnnotationError(result.reason)
        return {**(result.example or {"input_ids": None, "labels": None, "length": 0}),
                "training_status": result.training_status}

    ds = datasets.Dataset.from_dict({"row_json": [json.dumps(row) for row in rows]})
    ds = ds.map(
        tokenize_serialized, remove_columns=ds.column_names,
        num_proc=num_proc, desc=f"tokenize:{split}",
    )
    print(f"[{split}] dispositions: {dict(Counter(ds['training_status']))}")
    ds = ds.filter(lambda row: row["input_ids"] is not None, num_proc=num_proc)
    ds = ds.remove_columns("training_status")
    n_tgt = sum(sum(token != IGNORE for token in labels) for labels in ds["labels"])
    print(f"[{split}] {len(ds)}건, 총 토큰 {sum(ds['length']):,}, 학습 대상 토큰 {n_tgt:,}")
    return ds


class LengthGroupedTrainer(Trainer):
    """transformers 5.x 에서 TrainingArguments.group_by_length 가 사라져 직접 붙인다.

    시퀀스 길이 편차가 커서(약 2.6k~12k 토큰) 랜덤 샘플링하면 패딩으로 버리는 연산이 많다.
    """

    def _get_train_sampler(self, train_dataset=None):
        ds = train_dataset if train_dataset is not None else self.train_dataset
        if ds is None or "length" not in getattr(ds, "column_names", []):
            return super()._get_train_sampler(train_dataset)
        return LengthGroupedSampler(
            batch_size=self.args.train_batch_size * self.args.gradient_accumulation_steps,
            lengths=list(ds["length"]),
        )


@dataclass
class PadCollator:
    pad_token_id: int

    def __call__(self, features: list[dict]) -> dict:
        n = max(len(f["input_ids"]) for f in features)
        batch = {"input_ids": [], "labels": [], "attention_mask": []}
        for f in features:
            pad = n - len(f["input_ids"])
            batch["input_ids"].append(f["input_ids"] + [self.pad_token_id] * pad)
            batch["labels"].append(f["labels"] + [IGNORE] * pad)
            batch["attention_mask"].append([1] * len(f["input_ids"]) + [0] * pad)
        return {k: torch.tensor(v, dtype=torch.long) for k, v in batch.items()}


# ---------------------------------------------------------------- main


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--model", default="Qwen/Qwen3.5-9B")
    p.add_argument("--train-file", default="datas/sft/select/export/train.jsonl")
    p.add_argument("--val-file", default="datas/sft/select/export/val.jsonl")
    p.add_argument("--run-name", default=None, help="W&B run 이름. 미지정 시 설정값으로 자동 생성")
    p.add_argument(
        "--data-tag",
        default="merged",
        help="run_name/어댑터 폴더에 들어갈 데이터셋 식별자. "
        "선별 출력은 다시 만들면 덮어써지므로, 어떤 데이터로 학습했는지 이 태그로 남긴다.",
    )
    p.add_argument("--output-dir", default=None, help="체크포인트 경로. 기본 outputs/<run_name>")
    p.add_argument("--adapters-dir", default="adapters", help="확정 어댑터 보관 폴더")
    # select_candidates.py / export_sft.py 의 --max-length 와 같은 값이어야 한다
    # (선별 단계에서 이 길이를 넘는 궤적을 미리 제외한다).
    p.add_argument("--max-length", type=int, default=12288)
    p.add_argument("--epochs", type=float, default=3.0)
    p.add_argument("--max-steps", type=int, default=-1, help="스모크 테스트용 (-1 = 미사용)")
    p.add_argument("--lr", type=float, default=1e-4)
    # 기본 bs=4 / grad-accum 4 는 80GB GPU 기준값이다 (Liger 사용, max_length 12288,
    # 가장 긴 시퀀스끼리 묶인 배치에서도 60GiB 이하). 183GB급 GPU 에서는 bs=12 /
    # grad-accum 2 로 학습했다.
    p.add_argument("--batch-size", type=int, default=4)
    p.add_argument("--grad-accum", type=int, default=4)
    p.add_argument("--lora-r", type=int, default=32)
    p.add_argument("--lora-alpha", type=int, default=64)
    p.add_argument("--lora-dropout", type=float, default=0.05)
    p.add_argument("--warmup-ratio", type=float, default=0.05)  # ms-swift 의 Qwen3.5 권장값
    p.add_argument(
        "--no-liger",
        action="store_true",
        help="Liger fused linear CE 끄기. 어휘가 248k라 8k 시퀀스 로짓만 fp32 16GiB다. "
             "끄면 bs=1 에서도 42GiB 를 쓰고 bs=2 는 OOM 난다.",
    )
    p.add_argument("--num-proc", type=int, default=8)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    if args.run_name is None:
        from datetime import datetime

        args.run_name = (
            f"qwen35-9b-secfix-{args.data_tag}-r{args.lora_r}"
            f"-lr{args.lr:g}-{datetime.now():%m%d-%H%M}"
        )
    if args.output_dir is None:
        args.output_dir = f"outputs/{args.run_name}"

    # 학습 로그를 run 폴더에 자동 기록한다. fd 수준으로 tee 하므로 stdout/stderr
    # (tqdm, HF logging, CUDA 경고 포함) 전부가 터미널과 파일 양쪽에 남는다.
    # 종료 시 어댑터 폴더로도 복사되어 run 별 산출물과 함께 보존된다.
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    log_path = Path(args.output_dir) / "train.log"
    import subprocess
    import sys

    _tee = subprocess.Popen(["tee", "-a", str(log_path)], stdin=subprocess.PIPE)
    sys.stdout.flush(); sys.stderr.flush()
    os.dup2(_tee.stdin.fileno(), 1)
    os.dup2(_tee.stdin.fileno(), 2)
    print(f"run: {args.run_name}\nlog: {log_path}")

    tok = AutoTokenizer.from_pretrained(args.model)

    train_ds = prepare_dataset(
        load_rows(args.train_file), tok, args.max_length, args.num_proc, "train",
    )
    eval_ds = (
        prepare_dataset(load_rows(args.val_file), tok, args.max_length, args.num_proc, "val")
        if Path(args.val_file).exists() else None
    )

    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        dtype=torch.bfloat16,
        attn_implementation="sdpa",  # flash-attn 설치했다면 flash_attention_2
        device_map=None,
    )
    model.config.use_cache = False
    if hasattr(model.config, "text_config"):
        model.config.text_config.use_cache = False

    lora = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM",
        # 언어 모델 쪽 선형층만. vision tower 는 이 데이터에서 쓰지 않으므로 제외한다.
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
    )
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()
    model.enable_input_require_grads()  # gradient checkpointing + LoRA 조합에 필요

    # transformers 5.x 에는 warmup_ratio 가 없다. 총 스텝을 계산해 warmup_steps 로 준다.
    eff_batch = args.batch_size * args.grad_accum
    total_steps = (
        args.max_steps
        if args.max_steps > 0
        else max(1, int(len(train_ds) / eff_batch * args.epochs))
    )
    warmup_steps = max(1, int(total_steps * args.warmup_ratio))
    print(f"총 {total_steps} 스텝 (유효 배치 {eff_batch}), warmup {warmup_steps} 스텝")

    targs = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        max_steps=args.max_steps,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        gradient_checkpointing=True,
        gradient_checkpointing_kwargs={"use_reentrant": False},
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        warmup_steps=warmup_steps,
        weight_decay=0.0,
        max_grad_norm=1.0,
        bf16=True,
        use_liger_kernel=not args.no_liger,
        logging_steps=10,
        eval_strategy="steps" if eval_ds is not None else "no",
        eval_steps=50,
        save_strategy="steps",
        save_steps=50,
        save_total_limit=3,
        load_best_model_at_end=eval_ds is not None,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        remove_unused_columns=False,
        report_to=["wandb"],
        run_name=args.run_name,
        seed=args.seed,
    )

    trainer = LengthGroupedTrainer(
        model=model,
        args=targs,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        data_collator=PadCollator(tok.pad_token_id),
    )
    trainer.train()
    peak = torch.cuda.max_memory_allocated() / 1024**3
    print(f"peak GPU memory: {peak:.1f} GiB")

    # load_best_model_at_end 로 eval_loss 최저 체크포인트가 로드된 상태.
    # 체크포인트(outputs/)와 분리된 확정 어댑터 보관소에 저장한다.
    adapter_dir = Path(args.adapters_dir) / args.run_name
    adapter_dir.mkdir(parents=True, exist_ok=True)
    trainer.save_model(str(adapter_dir))
    tok.save_pretrained(str(adapter_dir))
    (adapter_dir / "training_args.json").write_text(
        json.dumps(vars(args), ensure_ascii=False, indent=2, default=str)
    )
    data_stats = Path(args.train_file).parent / "stats.json"
    if data_stats.exists():
        (adapter_dir / "data_stats.json").write_text(data_stats.read_text())

    try:
        import wandb

        if wandb.run is not None:
            wandb.run.summary["peak_gpu_gib"] = round(peak, 1)
            wandb.run.summary["adapter_dir"] = str(adapter_dir)
    except ImportError:
        pass
    print(f"어댑터 저장 완료: {adapter_dir}")

    # 학습 로그를 확정 보관소로 복사 (outputs/ 는 정리 대상이므로)
    import shutil

    sys.stdout.flush(); sys.stderr.flush()
    shutil.copy2(log_path, adapter_dir / "train.log")


if __name__ == "__main__":
    main()
