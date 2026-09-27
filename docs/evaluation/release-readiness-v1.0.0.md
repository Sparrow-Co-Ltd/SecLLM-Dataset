# Release readiness: SecLLM-Dataset 1.0.0

This record uses the 7-area scoring of the release-readiness template, as set out in
[POLICY.md](POLICY.md). Release 1.0.0 was published on 2026-09-20 ([CHANGELOG.md](../../CHANGELOG.md));
this assessment was made afterwards, on 2026-09-28, and decides what must happen before the release
is tagged.

## Release information

- **Project / release:** SecLLM-Dataset 1.0.0, `data/java/input.jsonl`, SHA-256
  `9a03c0a04b39814be14876ae9683f6f450c497a9712f11d9f3b8be593880af37`.
- **Tag:** **the `v1.0.0` tag does not exist yet** (no tag locally or on the remote, no GitHub release
  on 2026-09-28), although CHANGELOG links to `releases/tag/v1.0.0`.
- **Purpose:** a public benchmark and training set for detecting, explaining, and repairing
  vulnerabilities ([DATASHEET.md](../../DATASHEET.md#motivation)).
- **Published assets:** the core Java data, the validator, and the documentation in this repository.
- **Not published:** the Sparrow SAST analyzer and its configuration (a commercial product).
- **License:** CC BY 4.0 for the compilation and annotations; upstream licenses for `entireCode`
  ([NOTICE.md](../../NOTICE.md)).
- **Maintainers:** see [MAINTAINERS.md](../../MAINTAINERS.md).

## Stop conditions

| # | Condition | Result | Evidence |
|---|---|---|---|
| 1 | The company holds or is licensed for everything published | Met with condition | Compilation and annotations are Sparrow's work; `entireCode` stays under upstream licenses; about 80 files with GPL-family headers are disclosed and scheduled for removal ([NOTICE.md](../../NOTICE.md), [GDR-0002](../decisions/0002-gpl-header-records.md), [intake-starcoderdata.md](intake-starcoderdata.md)) |
| 2 | No secrets, personal data, customer data, or trade secrets | **Not met** | Upstream PII redaction leaves placeholders only ([DATASHEET.md](../../DATASHEET.md#personal-and-sensitive-information)), but GitHub secret scanning (enabled, with push protection) reports open alerts with unknown validity in `data/java/input.jsonl` on 2026-09-28. They must be triaged, and confirmed secrets removed or documented, before the tag. Details stay in the private Security tab. |
| 3 | LICENSE and the required NOTICE exist | Met | [LICENSE](../../LICENSE), [NOTICE.md](../../NOTICE.md), [CITATION.cff](../../CITATION.cff) |
| 4 | No critical unresolved vulnerability or dangerous default in the tooling | Met | Stdlib-only validator with self-test in CI ([validate.yml](../../.github/workflows/validate.yml)); SHA-pinned actions with read-only defaults; 0 open Dependabot alerts on 2026-09-28. Vulnerable code in `entireCode` is intended ([SECURITY.md](../../SECURITY.md)). |
| 5 | Management, program, and contract approval to publish | Not recorded | No approval record exists in the repository; the approver is named below |

## Readiness scores

| Area | Max | Score | Evidence | Open actions |
|---|---:|---:|---|---|
| Rights and license | 20 | 14 | NOTICE, GDR-0002, starcoderdata intake (70/100) | Remove GPL-header records |
| Security and privacy | 20 | 11 | SECURITY.md with private reporting; secret scanning and push protection on | Triage open secret-scanning alerts |
| Build, test, and quality | 15 | 13 | `scripts/validate.py` with `--self-test`, run on every push and pull request; DCO check | Document the sampling method |
| Documentation and usability | 15 | 14 | README (English and Korean), DATASHEET, CONTRIBUTING, CHANGELOG, CITATION.cff | – |
| Governance and operations | 15 | 8 | GOVERNANCE.md and MAINTAINERS.md exist; one active Maintainer; governance not yet approved | Fill the open roles; approve governance |
| Supply chain and release | 10 | 5 | Pinned actions, Dependabot, Scorecard; SHA-256 in CHANGELOG | Create the tag and release; attach the SBOM ([POLICY.md](POLICY.md#5-sbom)) |
| Business alignment | 5 | 5 | Funded under the NIPA 2026 program ([NOTICE.md](../../NOTICE.md#funding-acknowledgment)) | – |
| **Total** | 100 | **70** | | |

## Decision

- **Decision:** conditional release. The data stays public; the `v1.0.0` tag and GitHub release are
  created only after stop conditions 2 and 5 are met.
- **Conditions:**
  1. Triage the open secret-scanning alerts on `data/java/input.jsonl`; remove or document confirmed
     secrets (Maintainers, before the tag).
  2. Record the publication approval below (Sparrow Co., Ltd., before the tag).
  3. Create the `v1.0.0` tag and GitHub release on the commit that matches the SHA-256 above, and
     attach the SPDX SBOM (owner account `@Sparrow-Co-Ltd`, after 1 and 2).
  4. Remove the GPL-header records in the next release ([GDR-0002](../decisions/0002-gpl-header-records.md)).
- **Release date:** data published 2026-09-20; tag pending.
- **First operations review:** 2026-10-28.
- **Approver:**
  [TBD: release approver]
