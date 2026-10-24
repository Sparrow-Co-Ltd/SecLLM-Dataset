# Intake evaluation: bigcode/starcoderdata

This record uses the 7-area scoring of the intake template, as set out in [POLICY.md](POLICY.md).
It was written on 2026-09-28 for a component already in use since release 1.0.0 (retroactive intake).

## Basic information

- **Candidate / revision:** [bigcode/starcoderdata](https://huggingface.co/datasets/bigcode/starcoderdata),
  Hugging Face dataset revision `9fc30b578cedaec69e47302df72cf00feed7c8c4` (last modified
  2023-05-16, checked 2026-09-28 through the Hugging Face API). The revision used to build 1.0.0 was
  not recorded; this is the only revision published since 2023-05-16, before the dataset was built.
- **Use:** source of the Java files stored in `entireCode`. The files are redistributed as part of
  the dataset.
- **Distribution:** public dataset on GitHub, and on Hugging Face later.
- **Expected period of use:** for as long as the 1.x releases are published.
- **Prepared by:** the Maintainers (see [MAINTAINERS.md](../../MAINTAINERS.md)).

## Candidates compared

| Candidate | Summary | Outcome |
|---|---|---|
| **bigcode/starcoderdata** | Deduplicated, permissive-license subset of The Stack, with PII redaction and per-language folders | Selected |
| bigcode/the-stack (v1.2) | Larger superset; same licensing model; gated behind the same terms | Not selected: more data than needed, no PII redaction step of its own |
| bigcode/the-stack-v2 | Newer; file contents must be fetched separately from Software Heritage | Not selected: extra download pipeline and a second set of terms |
| Own crawl of GitHub | Full control over license selection per file | Not selected: new crawler, license detection, and PII redaction to build and maintain |

## Fatal conditions

- [x] Official source and version identified (revision above).
- [x] License identified and reviewable: the card lists `license: other`. Access is gated behind the
      BigCode terms of use, and each file keeps the license of its upstream repository.
- [x] No condition forbids commercial use or redistribution of the permissively licensed files.
- [x] No unresolvable critical security risk. The files contain intended vulnerabilities, which are
      the subject of the dataset; PII placeholders remain from the upstream redaction
      ([DATASHEET.md](../../DATASHEET.md#personal-and-sensitive-information)).
- [x] Meets the functional need (real-world Java files at scale).
- [x] No code of unknown origin: every file comes from a public repository.

All six are met, with the licensing condition below.

## Scores

| Area | Max | Score | Facts and evidence | Judgment |
|---|---:|---:|---|---|
| License and rights | 20 | 11 | `license: other`; repository-level license filter; about 80 of 4,617 files carry GPL-family headers ([NOTICE.md](../../NOTICE.md), [GDR-0002](../decisions/0002-gpl-header-records.md)) | Usable with per-file header check and removal |
| Security and supply chain | 20 | 13 | PII redaction upstream, placeholders remain; open secret-scanning alerts point at dataset records (see [release-readiness-v1.0.0.md](release-readiness-v1.0.0.md)) | Needs triage of detected secrets |
| Function and performance | 15 | 14 | Per-language folders; large enough to sample 4,617 files | Fits |
| Maintainability | 15 | 8 | Unchanged since 2023-05-16 | Frozen corpus; stable but no fixes |
| Architecture and operations | 10 | 8 | Parquet files on the Hugging Face Hub; plain download | Simple |
| Community and governance | 10 | 8 | BigCode project; widely used (545 likes, 41,314 downloads on 2026-09-28); opt-out process for rights holders | Good |
| Sustainability and replaceability | 10 | 8 | The Stack v1.2 / v2 are drop-in sources for later releases | Replaceable |
| **Total** | 100 | **70** | | |

## Decision

- **Decision:** approve with conditions (license and rights 11/20, total 70).
- **Approved version and scope:** the revision above, for `entireCode` in 1.x releases.
- **Conditions:** check each file's license header and remove the GPL-family records
  ([GDR-0002](../decisions/0002-gpl-header-records.md)); honor rights holders' removal requests
  ([NOTICE.md](../../NOTICE.md#removal-requests)); record the exact source revision and sampling
  method for the next release.
- **Fallback:** bigcode/the-stack v1.2.
- **Re-evaluation:** 2027-03-28, or earlier on any trigger in [POLICY.md](POLICY.md#3-re-evaluation),
  in particular a change to the BigCode terms or a new revision of the corpus.

## Evaluation history

| Date | Result |
|---|---|
| 2026-09-28 | First intake record: approve with conditions, 70/100 |
