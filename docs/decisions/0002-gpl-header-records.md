# GDR-0002: Disclose GPL-family file headers in `entireCode` and remove those records

- Status: Accepted
- Proposed: 2026-09-20 (author date of `b994513`)
- Decided: 2026-09-21 (commit date of `b994513`; the NOTICE wording was also part of `fb835dd` on 2026-09-21)
- Owner: @Sparrow-Co-Ltd
- Participants: none recorded
- Related commits: `fb835dd` (NOTICE: per-file license headers clarified), `b994513` (NOTICE, DATASHEET, CHANGELOG, CITATION)
- Recorded: 2026-09-28, retroactively

Sources: `git show fb835dd`, `git show b994513`.

## Context

The `entireCode` field holds original source files from
[bigcode/starcoderdata](https://huggingface.co/datasets/bigcode/starcoderdata), which selected code
by the license of the whole repository, not of each file. A license-header scan of release 1.0.0
found GPL, LGPL, or AGPL text in roughly 80 of the 4,617 files, under 2%. The repository's CC BY 4.0
license covers only the compilation and annotations, so users need to know which license governs
each file.

## Options

1. **Say nothing.** Keeps the release as is, but misleads users about the licensing of those files.
2. **Remove the records immediately.** Cleanest, but changes 1.0.0 right after release and needs a
   new version with a new SHA-256 in the same week.
3. **Disclose now and remove in a future release.** State the finding in NOTICE and DATASHEET, make
   the per-file header authoritative, and schedule removal.

## Decision

Option 3. [NOTICE.md](../../NOTICE.md) and [DATASHEET.md](../../DATASHEET.md#bias-risks-and-limitations)
state the finding. Where a file's own header states a license, that header governs the file. The
affected records are listed as Deprecated in [CHANGELOG.md](../../CHANGELOG.md) and are scheduled for
removal in a future release.

## Rationale and Consequences

- Users get an accurate license picture without waiting for a new release.
- Redistributors must check each file header until the removal release ships.
- Removal is a MINOR version change (records removed) under
  [GOVERNANCE.md](../../GOVERNANCE.md#12-releases) and changes the published SHA-256.
- Community data cannot reintroduce the issue: its license allowlist has no copyleft licenses
  (see [GDR-0001](0001-core-community-data-split.md)).

## Dissent

None recorded.

## Follow-up

- Remove the records with GPL-family headers and publish the new version / Maintainers / next release.
- Publish the scan method with the removal release / Maintainers / next release.

## Review Triggers

- A rights holder's removal request that covers these files.
- A new scan that finds a different number of affected files.
- Legal advice that changes the treatment of per-file headers.
