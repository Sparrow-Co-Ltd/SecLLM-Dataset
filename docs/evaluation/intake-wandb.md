# Intake evaluation: wandb

This record uses the 7-area scoring of the intake template, as set out in [POLICY.md](POLICY.md).
It was written on 2026-11-10 for a component already in use (retroactive intake): `train/` was added
in [#21](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/pull/21) and this intake was requested in
[#20](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/20). Facts were checked on 2026-11-10
against PyPI, the GitHub API, and api.scorecard.dev.

## Basic information

- **Candidate / version / commit:** [wandb/wandb](https://github.com/wandb/wandb) `0.28.1`; tag
  `v0.28.1` resolves to commit `bc2cf24b1bd9fa3a1b6cbeb920087b832afc526f`; released 2026-07-16;
  pinned with hashes in `train/uv.lock`. Latest release on 2026-11-10: 0.31.0.
- **Use:** experiment tracking in `train_sft.py` (`report_to=["wandb"]`, run summary fields).
  Metrics, hyperparameters, and the run name go to the Weights & Biases service unless `WANDB_MODE`
  is `offline` or `disabled`.
- **Transitive licenses outside the Allowed class:** `certifi` (MPL-2.0), Allowed with stronger
  notice. The client also installs `sentry-sdk` (MIT).
- **Distribution:** installed by the user with `uv sync` from PyPI; nothing is copied into this
  repository or a release.
- **Prepared by:** the Maintainers (see [MAINTAINERS.md](../../MAINTAINERS.md)).

## Candidates compared

| Candidate | Summary | Outcome |
|---|---|---|
| **wandb** | Hosted run tracking; built-in `Trainer` reporter | Selected |
| TensorBoard | Apache-2.0; local files only | Not selected at the time; a workable fallback with no external service |
| MLflow | Apache-2.0; self-hosted server | Not selected: a server to run |

## Fatal conditions

- [x] Official source and version identified (tag, SHA, and lock hashes above).
- [x] License identified: MIT (allowed). The hosted service has its own terms and is not part of
      this record.
- [x] No condition forbids commercial use of the client.
- [x] No unresolvable critical security risk: PyPI lists no advisory for 0.28.1; the API key is read
      from the environment or the git-ignored `train/.env`.
- [x] Meets the functional need (loss curves and run comparison).
- [x] No code of unknown origin: published by Weights & Biases.

## Scores

| Area | Max | Score | Facts and evidence | Judgment |
|---|---:|---:|---|---|
| License and rights | 20 | 20 | MIT | Allowed list |
| Security and supply chain | 20 | 12 | Lock hashes; no advisory for 0.28.1 on PyPI; no Scorecard result published; sends run data to an external service by default | Acceptable with the conditions |
| Function and performance | 15 | 13 | Tracked the SFT runs | Fits |
| Maintainability | 15 | 14 | Pushed 2026-11-10; three minor versions behind 0.31.0 | Active |
| Architecture and operations | 10 | 7 | Needs an account and a key unless offline; `report_to` is fixed in the script | External service |
| Community and governance | 10 | 8 | 11,313 stars; single vendor | Good |
| Sustainability and replaceability | 10 | 9 | `Trainer` supports other reporters | Easy to replace |
| **Total** | 100 | **83** | | |

## Decision

- **Decision:** approve with conditions.
- **Approved version and scope:** `0.28.1`, in the `train/` environment only.
- **Conditions:** (1) Keep `WANDB_API_KEY` out of the repository (`.env` is git-ignored). (2) Do not
  log source code, trajectories, or credentials as run artifacts or config. (3) `train/README.md`
  keeps documenting `WANDB_MODE=offline` and `disabled`.
- **Fallback:** `WANDB_MODE=disabled`, or TensorBoard as the `Trainer` reporter.
- **Re-evaluation:** 2027-03-28, or earlier on any trigger in
  [POLICY.md](POLICY.md#3-re-evaluation), in particular a new major version or a security advisory.

## Evaluation history

| Date | Result |
|---|---|
| 2026-11-10 | First intake record: approve with conditions, 83/100 |
