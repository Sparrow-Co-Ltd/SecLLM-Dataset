# Intake evaluation: httpx

This record uses the 7-area scoring of the intake template, as set out in [POLICY.md](POLICY.md).
It was written on 2026-11-10 for a component already in use (retroactive intake): `train/` was added
in [#21](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/pull/21) and this intake was requested in
[#20](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/20). Facts were checked on 2026-11-10
against PyPI, the GitHub API, and api.scorecard.dev.

## Basic information

- **Candidate / version / commit:** [encode/httpx](https://github.com/encode/httpx) `0.28.1`; tag
  `0.28.1` points at commit `26d48e0634e6ee9cdc0533996db289ce4b430177`; released 2024-12-06; pinned
  with hashes in `train/judge/uv.lock`. It is still the latest release on 2026-11-10.
- **Use:** HTTP client of `secllm_judge/judge_client.py`, which calls the OpenAI-compatible judge
  server set by `JUDGE_API_URL` in stage 2 of the selection pipeline.
- **Transitive licenses outside the Allowed class:** `certifi` (MPL-2.0), Allowed with stronger
  notice.
- **Distribution:** installed by the user with `uv sync` from PyPI; nothing is copied into this
  repository or a release.
- **Prepared by:** the Maintainers (see [MAINTAINERS.md](../../MAINTAINERS.md)).

## Candidates compared

| Candidate | Summary | Outcome |
|---|---|---|
| **httpx** | Typed client with timeouts and connection pooling | Selected |
| `urllib.request` (standard library) | No dependency | Not selected: retries, timeouts, and pooling by hand |
| openai SDK | Apache-2.0; ready-made client | Not selected: larger dependency that itself depends on httpx |

## Fatal conditions

- [x] Official source and version identified (tag, SHA, and lock hashes above).
- [x] License identified: BSD-3-Clause (allowed).
- [x] No condition forbids commercial use.
- [x] No unresolvable critical security risk: PyPI lists no advisory for 0.28.1; the server address
      and key come from the user's environment.
- [x] Meets the functional need.
- [x] No code of unknown origin: published by Encode.

## Scores

| Area | Max | Score | Facts and evidence | Judgment |
|---|---:|---:|---|---|
| License and rights | 20 | 20 | BSD-3-Clause | Allowed list |
| Security and supply chain | 20 | 13 | Lock hashes; no advisory for 0.28.1 on PyPI; OpenSSF Scorecard 4.9 (2026-11-02) | Acceptable |
| Function and performance | 15 | 14 | Stage 2 ran against a judge server with it | Fits |
| Maintainability | 15 | 10 | Pushed 2026-10-02; no release since 2024-12-06 | Slow release cadence |
| Architecture and operations | 10 | 9 | One client object | Simple |
| Community and governance | 10 | 8 | 15,764 stars; small maintainer team | Adequate |
| Sustainability and replaceability | 10 | 9 | The standard library can replace it | Easy to replace |
| **Total** | 100 | **83** | | |

## Decision

- **Decision:** approve.
- **Approved version and scope:** `0.28.1`, in the `train/judge/` environment (it is also a
  transitive dependency in `train/uv.lock`).
- **Conditions:** keep the lock hashes; watch the release cadence at each re-evaluation.
- **Fallback:** `urllib.request`.
- **Re-evaluation:** 2027-03-28, or earlier on any trigger in
  [POLICY.md](POLICY.md#3-re-evaluation), in particular a new major version or a security advisory.

## Evaluation history

| Date | Result |
|---|---|
| 2026-11-10 | First intake record: approve, 83/100 |
