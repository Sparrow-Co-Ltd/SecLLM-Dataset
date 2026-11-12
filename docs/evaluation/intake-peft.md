# Intake evaluation: peft

This record uses the 7-area scoring of the intake template, as set out in [POLICY.md](POLICY.md).
It was written on 2026-11-10 for a component already in use (retroactive intake): `train/` was added
in [#21](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/pull/21) and this intake was requested in
[#20](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/20). Facts were checked on 2026-11-10
against PyPI, the GitHub API, and api.scorecard.dev.

## Basic information

- **Candidate / version / commit:** [huggingface/peft](https://github.com/huggingface/peft)
  `0.20.0`; tag `v0.20.0` resolves to commit `a5526d27a9d47d1e8264d5e1b1f96c0fdc79464e`; released
  2026-07-28; pinned with hashes in `train/uv.lock`. Latest release on 2026-11-10: 0.21.2.
- **Use:** `LoraConfig` and `get_peft_model` in `train_sft.py` (r=32, alpha=64); `PeftModel` in
  `smoke_generate.py`.
- **Transitive licenses outside the Allowed class:** the ones named in
  [intake-torch.md](intake-torch.md) and [intake-transformers.md](intake-transformers.md); peft adds
  none.
- **Distribution:** installed by the user with `uv sync` from PyPI; nothing is copied into this
  repository or a release.
- **Prepared by:** the Maintainers (see [MAINTAINERS.md](../../MAINTAINERS.md)).

## Candidates compared

| Candidate | Summary | Outcome |
|---|---|---|
| **peft** | Standard LoRA implementation; adapter format the merge step and serving stacks read | Selected |
| Hand-written LoRA modules | No extra package | Not selected: custom adapter format, no merge tooling |
| Full fine-tuning | No adapter library | Not selected: memory and storage cost for a 9B model |

## Fatal conditions

- [x] Official source and version identified (tag, SHA, and lock hashes above).
- [x] License identified: Apache-2.0 (allowed).
- [x] No condition forbids commercial use.
- [x] No unresolvable critical security risk: PyPI lists no advisory for 0.20.0.
- [x] Meets the functional need (LoRA adapters for Qwen3.5-9B).
- [x] No code of unknown origin: published by Hugging Face.

## Scores

| Area | Max | Score | Facts and evidence | Judgment |
|---|---:|---:|---|---|
| License and rights | 20 | 20 | Apache-2.0 | Allowed list |
| Security and supply chain | 20 | 14 | Lock hashes; no advisory for 0.20.0 on PyPI; no Scorecard result published | Acceptable |
| Function and performance | 15 | 14 | Produced the SFT adapter of the published model | Fits |
| Maintainability | 15 | 14 | Pushed 2026-11-10; one minor version behind 0.21.2 | Active |
| Architecture and operations | 10 | 9 | Two calls in the training script | Simple |
| Community and governance | 10 | 9 | 21,880 stars; company-backed | Good |
| Sustainability and replaceability | 10 | 8 | LoRA can be reimplemented; adapter format is the lock-in | Replaceable with effort |
| **Total** | 100 | **88** | | |

## Decision

- **Decision:** approve.
- **Approved version and scope:** `0.20.0`, in the `train/` environment only.
- **Conditions:** keep the lock hashes; load only adapters you trained yourself.
- **Fallback:** hand-written LoRA modules.
- **Re-evaluation:** 2027-03-28, or earlier on any trigger in
  [POLICY.md](POLICY.md#3-re-evaluation), in particular a new major version or a security advisory.

## Evaluation history

| Date | Result |
|---|---|
| 2026-11-10 | First intake record: approve, 88/100 |
