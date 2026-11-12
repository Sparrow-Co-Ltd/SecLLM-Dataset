# Intake evaluation: transformers

This record uses the 7-area scoring of the intake template, as set out in [POLICY.md](POLICY.md).
It was written on 2026-11-10 for a component already in use (retroactive intake): `train/` was added
in [#21](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/pull/21) and this intake was requested in
[#20](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/20). Facts were checked on 2026-11-10
against PyPI, the GitHub API, and api.scorecard.dev.

## Basic information

- **Candidate / version / commit:**
  [huggingface/transformers](https://github.com/huggingface/transformers) `5.15.0`; tag `v5.15.0`
  resolves to commit `5eddc12edfaf8cafde8c9bae4ccb12f8a139b4f9`; released 2026-08-10; pinned with
  hashes in `train/uv.lock`. Latest release on 2026-11-10: 5.22.2.
- **Use:** model and tokenizer loading, the Qwen3.5 chat template, `Trainer`, `TrainingArguments`,
  and `LengthGroupedSampler` in `train/sft/`; the tokenizer alone in `select_candidates.py` and
  `export_sft.py`.
- **Transitive licenses outside the Allowed class:** `tqdm` (MPL-2.0 AND MIT) and `certifi`
  (MPL-2.0), both Allowed with stronger notice.
- **Distribution:** installed by the user with `uv sync` from PyPI; nothing is copied into this
  repository or a release.
- **Prepared by:** the Maintainers (see [MAINTAINERS.md](../../MAINTAINERS.md)).

## Candidates compared

| Candidate | Summary | Outcome |
|---|---|---|
| **transformers** | Reference implementation of Qwen3.5 and its chat template; integrates `peft` and Liger | Selected |
| Unsloth | Apache-2.0 wrapper around transformers and peft | Not selected: one more dependency on top of the same two |
| Hand-written training loop on torch | No extra package | Not selected: the model code and the chat template would have to be reimplemented |

## Fatal conditions

- [x] Official source and version identified (tag, SHA, and lock hashes above).
- [x] License identified: Apache-2.0 (allowed).
- [x] No condition forbids commercial use.
- [x] No unresolvable critical security risk: PyPI lists no advisory for 5.15.0; `trust_remote_code`
      is not used.
- [x] Meets the functional need (Qwen3.5-9B support, `use_liger_kernel`, length-grouped sampling).
- [x] No code of unknown origin: published by Hugging Face.

## Scores

| Area | Max | Score | Facts and evidence | Judgment |
|---|---:|---:|---|---|
| License and rights | 20 | 20 | Apache-2.0 | Allowed list |
| Security and supply chain | 20 | 15 | Lock hashes; no advisory for 5.15.0 on PyPI; OpenSSF Scorecard 6.5 (2026-11-02) | Acceptable |
| Function and performance | 15 | 15 | Trained the SFT adapter of the published model | Fits |
| Maintainability | 15 | 14 | Pushed 2026-11-10; 5.15.0 is 7 minor versions behind 5.22.2 | Active |
| Architecture and operations | 10 | 8 | 27 transitive packages; private `trainer_pt_utils` import can break on upgrade | Acceptable |
| Community and governance | 10 | 10 | 168,719 stars; company-backed | Strong |
| Sustainability and replaceability | 10 | 8 | The masking code depends on the exact chat template rendering | Upgrade needs `verify_template.py` |
| **Total** | 100 | **90** | | |

## Decision

- **Decision:** approve.
- **Approved version and scope:** `5.15.0`, in the `train/` environment only.
- **Conditions:** keep the lock hashes; after any version change run `verify_template.py` and
  `test_srft_masking.py`, because label masking depends on the template rendering.
- **Fallback:** none short of a hand-written loop.
- **Re-evaluation:** 2027-03-28, or earlier on any trigger in
  [POLICY.md](POLICY.md#3-re-evaluation), in particular a new major version or a security advisory.

## Evaluation history

| Date | Result |
|---|---|
| 2026-11-10 | First intake record: approve, 90/100 |
