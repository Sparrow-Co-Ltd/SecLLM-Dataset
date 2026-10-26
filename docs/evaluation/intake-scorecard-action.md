# Intake evaluation: ossf/scorecard-action

This record uses the 7-area scoring of the intake template, as set out in [POLICY.md](POLICY.md).
It was written on 2026-09-28 for a component already in use (retroactive intake).

## Basic information

- **Candidate / version / commit:** [ossf/scorecard-action](https://github.com/ossf/scorecard-action)
  `v2.4.4`, commit `2d1146689b8cda280b9bc96326124645441f03bc` (the annotated tag resolves to this
  commit; latest release on 2026-09-28).
- **Use:** weekly and on-push OpenSSF Scorecard analysis in `.github/workflows/scorecard.yml`; results
  go to code scanning and the public Scorecard API (badge).
- **Companion action:** `github/codeql-action/upload-sarif` `v4.38.1`
  (`1c5b675653bb5c22dbe9b12b556ec555138e09fd`) uploads the SARIF file. It is pinned the same way and
  covered by the same re-evaluation triggers.
- **Distribution:** runs in CI only; nothing is redistributed.
- **Prepared by:** the Maintainers (see [MAINTAINERS.md](../../MAINTAINERS.md)).

## Candidates compared

| Candidate | Summary | Outcome |
|---|---|---|
| **ossf/scorecard-action** | Official action; SARIF to code scanning; publishes results for the badge | Selected |
| Scorecard CLI or Docker image, run by hand | Same checks, no workflow permissions needed | Not selected: no continuous record and no badge |
| OpenSSF Best Practices badge only | Self-attested questionnaire | Complementary, not a replacement: no automated checks |

## Fatal conditions

- [x] Official source and version identified (tag and 40-character SHA above).
- [x] License identified: Apache-2.0 (allowed).
- [x] No condition forbids commercial use.
- [x] No unresolvable critical security risk: the job asks only for `security-events: write` and
      `id-token: write`; top-level permissions are `read-all`; checkout uses
      `persist-credentials: false`.
- [x] Meets the functional need (supply-chain posture score for OpenSSF re-inspection).
- [x] No code of unknown origin: published by the OpenSSF.

## Scores

| Area | Max | Score | Facts and evidence | Judgment |
|---|---:|---:|---|---|
| License and rights | 20 | 20 | Apache-2.0 | Allowed list |
| Security and supply chain | 20 | 17 | SHA-pinned; OpenSSF Scorecard of the action itself 8.1 (2026-07-23, api.scorecard.dev); needs two write scopes on its job | Acceptable |
| Function and performance | 15 | 14 | SARIF, badge, weekly schedule | Fits |
| Maintainability | 15 | 13 | Pushed 2026-09-25; Dependabot tracks it (`.github/dependabot.yml`) | Active |
| Architecture and operations | 10 | 9 | One step; no secrets needed | Simple |
| Community and governance | 10 | 9 | OpenSSF project under the Linux Foundation; 420 stars | Good |
| Sustainability and replaceability | 10 | 9 | CLI and Docker image are fallbacks | Replaceable |
| **Total** | 100 | **91** | | |

## Decision

- **Decision:** approve.
- **Approved version and scope:** `v2.4.4` at the SHA above, in `scorecard.yml` only.
- **Conditions:** keep the SHA pin and job-scoped permissions; Dependabot proposes updates.
- **Fallback:** Scorecard Docker image (`gcr.io/openssf/scorecard`), run by hand.
- **Re-evaluation:** 2027-03-28, or earlier on any trigger in [POLICY.md](POLICY.md#3-re-evaluation),
  in particular a new major version or new permission requirements.

## Evaluation history

| Date | Result |
|---|---|
| 2026-09-28 | First intake record: approve, 91/100 |
