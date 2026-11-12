# Intake evaluation: pydantic

This record uses the 7-area scoring of the intake template, as set out in [POLICY.md](POLICY.md).
It was written on 2026-11-10 for a component already in use (retroactive intake): `train/` was added
in [#21](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/pull/21) and this intake was requested in
[#20](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/20). Facts were checked on 2026-11-10
against PyPI, the GitHub API, and api.scorecard.dev.

## Basic information

- **Candidate / version / commit:** [pydantic/pydantic](https://github.com/pydantic/pydantic)
  `2.12.5`; tag `v2.12.5` resolves to commit `bd2d0dd0137dfa1a8fdff2529b9dfb1547980150`; released
  2025-11-26; pinned with hashes in `train/judge/uv.lock`. Latest release on 2026-11-10: 2.14.3.
- **Use:** typed contracts of the judge modules (`schemas.py`, `corpus.py`, `judge_client.py`):
  judge requests, verdicts, and decision records are validated on read and write.
- **Transitive licenses outside the Allowed class:** none (`typing-extensions` is PSF-2.0, allowed).
- **Distribution:** installed by the user with `uv sync` from PyPI; nothing is copied into this
  repository or a release.
- **Prepared by:** the Maintainers (see [MAINTAINERS.md](../../MAINTAINERS.md)).

## Candidates compared

| Candidate | Summary | Outcome |
|---|---|---|
| **pydantic** | Validation and JSON serialization from type annotations | Selected |
| `dataclasses` with hand-written validation | No dependency | Not selected: validation of LLM output by hand for every field |
| msgspec | BSD-3-Clause; faster | Not selected: no need for the speed; smaller ecosystem |

## Fatal conditions

- [x] Official source and version identified (tag, SHA, and lock hashes above).
- [x] License identified: MIT (allowed).
- [x] No condition forbids commercial use.
- [x] No unresolvable critical security risk: PyPI lists no advisory for 2.12.5.
- [x] Meets the functional need (rejects malformed judge output).
- [x] No code of unknown origin: published by the Pydantic project.

## Scores

| Area | Max | Score | Facts and evidence | Judgment |
|---|---:|---:|---|---|
| License and rights | 20 | 20 | MIT | Allowed list |
| Security and supply chain | 20 | 15 | Lock hashes; no advisory for 2.12.5 on PyPI; OpenSSF Scorecard 6.6 (2026-10-26) | Acceptable |
| Function and performance | 15 | 14 | Validates every judge response | Fits |
| Maintainability | 15 | 14 | Pushed 2026-11-09; two minor versions behind 2.14.3 | Active |
| Architecture and operations | 10 | 9 | 4 transitive packages; compiled core | Simple |
| Community and governance | 10 | 9 | 29,417 stars | Good |
| Sustainability and replaceability | 10 | 8 | Schemas would need rewriting | Replaceable with effort |
| **Total** | 100 | **89** | | |

## Decision

- **Decision:** approve.
- **Approved version and scope:** `2.12.5`, in the `train/judge/` environment (`train/uv.lock` pins
  2.13.4 as a transitive dependency of wandb).
- **Conditions:** keep the lock hashes.
- **Fallback:** `dataclasses` with explicit validation.
- **Re-evaluation:** 2027-03-28, or earlier on any trigger in
  [POLICY.md](POLICY.md#3-re-evaluation), in particular a new major version or a security advisory.

## Evaluation history

| Date | Result |
|---|---|
| 2026-11-10 | First intake record: approve, 89/100 |
