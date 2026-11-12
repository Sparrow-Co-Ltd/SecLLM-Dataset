# Intake evaluation: liger-kernel

This record uses the 7-area scoring of the intake template, as set out in [POLICY.md](POLICY.md).
It was written on 2026-11-10 for a component already in use (retroactive intake): `train/` was added
in [#21](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/pull/21) and this intake was requested in
[#20](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/20). Facts were checked on 2026-11-10
against PyPI, the GitHub API, and api.scorecard.dev.

## Basic information

- **Candidate / version / commit:**
  [linkedin/Liger-Kernel](https://github.com/linkedin/Liger-Kernel) `0.8.1`; tag `v0.8.1` resolves
  to commit `a5234dfc1d29db350a3a7d57a2671274a0a9d7da`; released 2026-07-23; pinned with hashes in
  `train/uv.lock`. Latest release on 2026-11-10: 0.8.5.
- **Use:** `use_liger_kernel=True` in `TrainingArguments` (`train_sft.py`): fused linear and
  cross-entropy loss. With a 248k vocabulary, turning it off (`--no-liger`) costs about 42 GiB at
  batch size 1 (`train/README.md`).
- **Transitive licenses outside the Allowed class:** the NVIDIA wheels named in
  [intake-torch.md](intake-torch.md), through torch; liger-kernel adds none.
- **Distribution:** installed by the user with `uv sync` from PyPI; nothing is copied into this
  repository or a release.
- **Prepared by:** the Maintainers (see [MAINTAINERS.md](../../MAINTAINERS.md)).

## Candidates compared

| Candidate | Summary | Outcome |
|---|---|---|
| **liger-kernel** | Fused loss kernels, enabled by one `Trainer` flag | Selected |
| Default transformers loss path (`--no-liger`) | No extra package | Not selected: about 42 GiB more memory at batch size 1 |
| Hand-written chunked loss | No extra package | Not selected: custom code in the loss path to maintain and test |

## Fatal conditions

- [x] Official source and version identified (tag, SHA, and lock hashes above).
- [x] License identified: BSD-2-Clause (allowed).
- [x] No condition forbids commercial use.
- [x] No unresolvable critical security risk: PyPI lists no advisory for 0.8.1; the package reads no
      external input.
- [x] Meets the functional need (training fits on one GPU).
- [x] No code of unknown origin: published by LinkedIn.

## Scores

| Area | Max | Score | Facts and evidence | Judgment |
|---|---:|---:|---|---|
| License and rights | 20 | 20 | BSD-2-Clause | Allowed list |
| Security and supply chain | 20 | 13 | Lock hashes; no advisory for 0.8.1 on PyPI; no Scorecard result published | Acceptable |
| Function and performance | 15 | 15 | Makes single-GPU training of the 248k-vocabulary model possible | Required |
| Maintainability | 15 | 12 | Pushed 2026-11-09; 0.x versioning, four patch versions behind 0.8.5 | Active, pre-1.0 |
| Architecture and operations | 10 | 8 | One flag; triton kernels compile at first use | Simple |
| Community and governance | 10 | 7 | 6,691 stars; single-company project | Adequate |
| Sustainability and replaceability | 10 | 7 | `--no-liger` works but needs far more memory | Costly to replace |
| **Total** | 100 | **82** | | |

## Decision

- **Decision:** approve.
- **Approved version and scope:** `0.8.1`, in the `train/` environment only.
- **Conditions:** keep the lock hashes; 0.x minor versions are treated as major versions for
  re-evaluation.
- **Fallback:** `--no-liger` on a GPU with enough memory.
- **Re-evaluation:** 2027-03-28, or earlier on any trigger in
  [POLICY.md](POLICY.md#3-re-evaluation), in particular a new major version or a security advisory.

## Evaluation history

| Date | Result |
|---|---|
| 2026-11-10 | First intake record: approve, 82/100 |
