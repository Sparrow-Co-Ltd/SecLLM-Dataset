# Intake evaluation: accelerate

This record uses the 7-area scoring of the intake template, as set out in [POLICY.md](POLICY.md).
It was written on 2026-11-10 for a component already in use (retroactive intake): `train/` was added
in [#21](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/pull/21) and this intake was requested in
[#20](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/20). Facts were checked on 2026-11-10
against PyPI, the GitHub API, and api.scorecard.dev.

## Basic information

- **Candidate / version / commit:**
  [huggingface/accelerate](https://github.com/huggingface/accelerate) `1.14.0`; tag `v1.14.0`
  resolves to commit `beb0672aa8444ea7647aee056f624effe5996346`; released 2026-06-11; pinned with
  hashes in `train/uv.lock`. Latest release on 2026-11-10: 1.15.0.
- **Use:** not imported by the code under `train/`; `transformers.Trainer` requires it, and
  `from_pretrained(..., device_map=...)` in `smoke_generate.py` uses it for device placement.
- **Transitive licenses outside the Allowed class:** the ones named in
  [intake-torch.md](intake-torch.md) and [intake-transformers.md](intake-transformers.md);
  accelerate adds none.
- **Distribution:** installed by the user with `uv sync` from PyPI; nothing is copied into this
  repository or a release.
- **Prepared by:** the Maintainers (see [MAINTAINERS.md](../../MAINTAINERS.md)).

## Candidates compared

| Candidate | Summary | Outcome |
|---|---|---|
| **accelerate** | Required by `Trainer`; device placement and mixed precision | Selected |
| Hand-written training loop without `Trainer` | No accelerate | Not selected: loses `Trainer`, Liger integration, and checkpointing |
| PyTorch Lightning | Apache-2.0 | Not selected: second training framework next to transformers |

## Fatal conditions

- [x] Official source and version identified (tag, SHA, and lock hashes above).
- [x] License identified: Apache-2.0 (allowed).
- [x] No condition forbids commercial use.
- [x] No unresolvable critical security risk: the open advisory below needs a crafted sharded
      checkpoint index, and the code loads only the official base model and adapters the user
      trained.
- [x] Meets the functional need.
- [x] No code of unknown origin: published by Hugging Face.

## Scores

| Area | Max | Score | Facts and evidence | Judgment |
|---|---:|---:|---|---|
| License and rights | 20 | 20 | Apache-2.0 | Allowed list |
| Security and supply chain | 20 | 12 | Lock hashes. PyPI lists GHSA-4j2p-28q2-5m79 (CVE-2026-69112; GitHub severity Moderate, CVSS 3.1 base score 7.1 from the published vector) for 1.14.0: path traversal in `load_checkpoint_in_model` and `load_checkpoint_and_dispatch`; no fixed version was listed on 2026-11-10. OpenSSF Scorecard 6.6 (2026-11-09) | Open advisory |
| Function and performance | 15 | 13 | Used through `Trainer` | Fits |
| Maintainability | 15 | 14 | Pushed 2026-11-09; one minor version behind 1.15.0 | Active |
| Architecture and operations | 10 | 9 | No direct call in this repository | Simple |
| Community and governance | 10 | 9 | 9,937 stars; company-backed | Good |
| Sustainability and replaceability | 10 | 7 | Cannot be removed while `Trainer` is used | Tied to transformers |
| **Total** | 100 | **84** | | |

## Decision

- **Decision:** approve with conditions.
- **Approved version and scope:** `1.14.0`, in the `train/` environment only.
- **Conditions:** (1) Load only the official base model and checkpoints you produced. (2) Check
  whether 1.15.0 or later fixes GHSA-4j2p-28q2-5m79 and update the lock when a fixed version is
  published. A CVSS score of 7.1 is High in [POLICY.md](POLICY.md#4-vulnerability-response-targets)
  (1 week from triage); until a fix exists, condition 1 is the recorded mitigation.
- **Fallback:** none while `Trainer` is used.
- **Re-evaluation:** 2027-03-28, or earlier on any trigger in
  [POLICY.md](POLICY.md#3-re-evaluation), in particular a new major version or a security advisory.

## Evaluation history

| Date | Result |
|---|---|
| 2026-11-10 | First intake record: approve with conditions, 84/100 |
