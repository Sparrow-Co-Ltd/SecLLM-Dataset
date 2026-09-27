# GDR-0001: Keep core data and community data in separate tracks

- Status: Accepted
- Proposed: 2026-09-21
- Decided: 2026-09-21
- Owner: @Sparrow-Co-Ltd
- Participants: none recorded
- Related commits: `fb835dd` (community data track, validator, CONTRIBUTING), `c433c66` (more languages, pull request #4)
- Recorded: 2026-09-28, retroactively

## Context

The core dataset (`data/java/`) is produced with Sparrow SAST, and every patch is re-verified by
running the analyzer again. Outside contributors cannot run that verification, yet people want to
contribute records found with other tools such as Semgrep or CodeQL. Mixing the two would make it
impossible for users to tell verified records from attested ones, and it would put upstream
licensing of contributed code on the team without a way to check it.

## Options

1. **Core data only.** Refuse outside records. Simple, but closes the main contribution path of a
   dataset project.
2. **Accept outside records into the core files.** Maximum reuse, but users can no longer tell which
   records were re-verified, and the core SHA-256 in CHANGELOG changes with every contribution.
3. **Two tracks.** Core data stays team-only; community records go under `data/community/<lang>/`
   with required provenance fields, checked automatically by CI.

## Decision

Option 3. Core data (`data/java/`) is changed by the team only; outside pull requests that modify it
are not accepted and data errors are reported through the data error form instead. Community
records live in `data/community/<lang>/<tool>-<yyyymmdd>.jsonl`, must carry a `meta` object with
tool, rule, upstream repository, commit, path, and SPDX license, and must use a license from the
allowlist (`LICENSES` in [scripts/validate.py](../../scripts/validate.py)). `patchVerified` must be
`true`. The validator derives the tier from the directory (`tier_of`).

## Rationale and Consequences

- Users choose their trust level by directory: core records are analyzer-verified, community
  records are contributor-attested ([CONTRIBUTING.md](../../CONTRIBUTING.md#community-data)).
- CI checks schema and provenance; it does not re-run the contributor's tool, so detection and patch
  correctness in the community track remain the contributor's claim.
- The license allowlist keeps copyleft code out of the community track by construction.
- On 2026-09-22 (`c433c66`) the validator gained JavaScript, TypeScript, Go, Python, C, and C++;
  the two-track split applies unchanged to every language.

## Dissent

None recorded.

## Follow-up

- Keep the allowlist history in [docs/evaluation/POLICY.md](../evaluation/POLICY.md) / Maintainers / at each allowlist change.

## Review Triggers

- A way for the team to re-verify third-party tool results automatically.
- Repeated community submissions that turn out to be wrong.
- A request to merge community records into a release artifact.
