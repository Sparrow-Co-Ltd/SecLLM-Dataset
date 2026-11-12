# Intake evaluation: datasets

This record uses the 7-area scoring of the intake template, as set out in [POLICY.md](POLICY.md).
It was written on 2026-11-10 for a component already in use (retroactive intake): `train/` was added
in [#21](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/pull/21) and this intake was requested in
[#20](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/20). Facts were checked on 2026-11-10
against PyPI, the GitHub API, and api.scorecard.dev.

## Basic information

- **Candidate / version / commit:** [huggingface/datasets](https://github.com/huggingface/datasets)
  `5.0.1`; tag `5.0.1` points at commit `921c2a7c0c9494e86fd145e03f68d12fa4ef90a2`; released
  2026-07-28; pinned with hashes in `train/uv.lock`. Latest release on 2026-11-10: 5.2.0.
- **Use:** `datasets.Dataset` holds the tokenized train and validation rows passed to `Trainer` in
  `train_sft.py`. No dataset is downloaded from the Hub.
- **Transitive licenses outside the Allowed class:** `tqdm` (MPL-2.0 AND MIT) and `certifi`
  (MPL-2.0), both Allowed with stronger notice.
- **Distribution:** installed by the user with `uv sync` from PyPI; nothing is copied into this
  repository or a release.
- **Prepared by:** the Maintainers (see [MAINTAINERS.md](../../MAINTAINERS.md)).

## Candidates compared

| Candidate | Summary | Outcome |
|---|---|---|
| **datasets** | `Dataset` with column access for length-grouped sampling; what `Trainer` expects | Selected |
| `torch.utils.data.Dataset` over JSON Lines | No extra package | Not selected at the time; a workable fallback |
| pandas | Already a transitive dependency | Not selected: no `Trainer` integration |

## Fatal conditions

- [x] Official source and version identified (tag, SHA, and lock hashes above).
- [x] License identified: Apache-2.0 (allowed).
- [x] No condition forbids commercial use.
- [x] No unresolvable critical security risk: PyPI lists no advisory for 5.0.1; only local JSON
      Lines files are read.
- [x] Meets the functional need.
- [x] No code of unknown origin: published by Hugging Face.

## Scores

| Area | Max | Score | Facts and evidence | Judgment |
|---|---:|---:|---|---|
| License and rights | 20 | 20 | Apache-2.0 | Allowed list |
| Security and supply chain | 20 | 14 | Lock hashes; no advisory for 5.0.1 on PyPI; no Scorecard result published | Acceptable |
| Function and performance | 15 | 12 | Used for an in-memory table only | More than needed |
| Maintainability | 15 | 14 | Pushed 2026-11-09; two minor versions behind 5.2.0 | Active |
| Architecture and operations | 10 | 8 | 28 transitive packages (pyarrow, pandas, aiohttp) for one class | Heavy for the use |
| Community and governance | 10 | 9 | 22,123 stars; company-backed | Good |
| Sustainability and replaceability | 10 | 9 | A torch `Dataset` replaces it | Easy to replace |
| **Total** | 100 | **86** | | |

## Decision

- **Decision:** approve.
- **Approved version and scope:** `5.0.1`, in the `train/` environment only.
- **Conditions:** keep the lock hashes; do not load remote datasets with scripts.
- **Fallback:** `torch.utils.data.Dataset` over the exported JSON Lines.
- **Re-evaluation:** 2027-03-28, or earlier on any trigger in
  [POLICY.md](POLICY.md#3-re-evaluation), in particular a new major version or a security advisory.

## Evaluation history

| Date | Result |
|---|---|
| 2026-11-10 | First intake record: approve, 86/100 |
