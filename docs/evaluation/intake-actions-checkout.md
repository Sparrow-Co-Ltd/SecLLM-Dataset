# Intake evaluation: actions/checkout

This record uses the 7-area scoring of the intake template, as set out in [POLICY.md](POLICY.md).
It was written on 2026-09-28 for a component already in use (retroactive intake).

## Basic information

- **Candidate / version / commit:** [actions/checkout](https://github.com/actions/checkout) `v7.0.1`,
  commit `3d3c42e5aac5ba805825da76410c181273ba90b1` (the tag points at this commit; latest release on
  2026-09-28).
- **Use:** checks out the repository in every workflow (`validate.yml`, `scorecard.yml`,
  `policy-check.yml`), always with `persist-credentials: false`.
- **Distribution:** runs in CI only; nothing is redistributed.
- **Prepared by:** the Maintainers (see [MAINTAINERS.md](../../MAINTAINERS.md)).

## Candidates compared

| Candidate | Summary | Outcome |
|---|---|---|
| **actions/checkout** | Official GitHub action; handles fetch depth, auth, and cleanup | Selected |
| `git clone` in a `run:` step | No third-party action | Not selected: token handling and fetch-depth logic would be hand-written in each workflow |
| No checkout | Nothing to pin | Not possible: every job reads repository files |

## Fatal conditions

- [x] Official source and version identified (tag and 40-character SHA above).
- [x] License identified: MIT (allowed).
- [x] No condition forbids commercial use.
- [x] No unresolvable critical security risk: pinned by SHA; credentials are not persisted, so later
      steps cannot reuse the token.
- [x] Meets the functional need.
- [x] No code of unknown origin: published by GitHub.

## Scores

| Area | Max | Score | Facts and evidence | Judgment |
|---|---:|---:|---|---|
| License and rights | 20 | 20 | MIT | Allowed list |
| Security and supply chain | 20 | 16 | SHA-pinned, `persist-credentials: false`; OpenSSF Scorecard of the action itself 6.6 (2026-09-21, api.scorecard.dev) | Acceptable with pinning |
| Function and performance | 15 | 15 | Full, shallow, and history checkouts | Fits |
| Maintainability | 15 | 14 | Pushed 2026-09-21; Dependabot tracks it (`.github/dependabot.yml`) | Active |
| Architecture and operations | 10 | 10 | One step per job | Simple |
| Community and governance | 10 | 9 | Maintained by GitHub; 8,912 stars | Good |
| Sustainability and replaceability | 10 | 10 | `git clone` is always a fallback | Replaceable |
| **Total** | 100 | **94** | | |

## Decision

- **Decision:** approve.
- **Approved version and scope:** `v7.0.1` at the SHA above, in all workflows.
- **Conditions:** always pin the SHA and set `persist-credentials: false`; Dependabot proposes updates.
- **Fallback:** `git clone` in a `run:` step.
- **Re-evaluation:** 2027-03-28, or earlier on any trigger in [POLICY.md](POLICY.md#3-re-evaluation),
  in particular a new major version or a Scorecard drop of 2 points or more.

## Evaluation history

| Date | Result |
|---|---|
| 2026-09-28 | First intake record: approve, 94/100 |
