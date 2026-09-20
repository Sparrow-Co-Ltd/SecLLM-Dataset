# Contributing to SecLLM-Dataset

Thank you for helping improve SecLLM-Dataset. By participating you agree to follow our
[Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to Contribute

| What you want to do | Channel |
|---|---|
| Report a wrong label, a static-analysis false positive, or an incorrect patch | [Data error issue](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=data-error.yml) |
| Ask for removal of source code you hold rights to | [Removal request issue](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=removal-request.yml) |
| Contribute records produced with another analysis tool | [Community data issue](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=community-data.yml) first, then a pull request into `data/community/<lang>/` |
| Improve documentation, examples, or scripts | Pull request |
| Report a security vulnerability in this repository | Private report, see [SECURITY.md](SECURITY.md) |

### Core data is changed by the team only

The core dataset (`data/java/`) is produced with Sparrow SAST, and every patch is re-verified by
running the analyzer again. Outside contributors cannot reproduce that verification, so pull
requests that modify core data are not accepted. Instead, open a data error issue. The team
re-verifies the report and ships the correction in the next release (see
[GOVERNANCE.md](GOVERNANCE.md#releases)).

## Community Data

Records detected and patched with other tools (for example Semgrep or CodeQL) are accepted in a
separate track under `data/community/`.

> **Verification tier.** Community data is attested by its contributor. The team checks the schema
> and provenance fields automatically but does not re-run the contributor's tool. Core data and
> community data are therefore kept in separate directories, and users can choose which tier to use.

### Files

- Path: `data/community/<lang>/<tool>-<yyyymmdd>.jsonl`, for example
  `data/community/java/semgrep-20260919.jsonl`
- Format: JSON Lines, UTF-8, one record per line

### Record format

A community record has three top-level keys: `input`, `output`, and `meta`.

`input` and `output` follow the same schema as the core data (see the schema section of
[README.md](README.md)), with these relaxations:

- `contexts` may be an empty array if the tool does not report a trace
- `issueNameKo`, `issueDescriptionKo`, `dangerousExampleEn`, `dangerousExampleKo`,
  `safeExampleEn`, and `safeExampleKo` may be empty strings

`meta` is required and must contain exactly these fields:

| Field | Type | Description |
|---|---|---|
| `tool` | string | Analysis tool name, for example `semgrep` |
| `toolVersion` | string | Tool version used for detection and re-analysis |
| `ruleId` | string | Rule or checker identifier that reported the issue |
| `sourceRepo` | string | `https://` URL of the upstream repository |
| `sourceCommit` | string | Upstream commit hash (7–40 hex characters) |
| `sourcePath` | string | Path of the file in the upstream repository |
| `sourceLicense` | string | SPDX identifier of the upstream license; must be in the allowlist below |
| `patchVerified` | boolean | Must be `true`: after applying `output`, the same tool and rule no longer report the issue |

**License allowlist:** `MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `ISC`, `0BSD`,
`Unlicense`, `CC0-1.0`, `Zlib`, `BSL-1.0`. To propose another permissive license, open a
community data issue; a maintainer will update the allowlist if accepted.

**Languages:** the directory name must match the record's language.

| Directory | `fileExtension` | `programmingLanguage` |
|---|---|---|
| `java` | `.java` | `Java` |

Adding a language means adding one entry to `LANGS` in `scripts/validate.py` and a row to this
table.

**Severity mapping:** map your tool's severity to `issueRisk` as follows.

| Tool severity | `issueRisk` |
|---|---|
| critical | `매우 높음` |
| high | `높음` |
| medium | `보통` |
| low | `낮음` |
| info | `매우 낮음` |

## Pull Requests

1. Fork the repository and create a branch.
2. Make your change. If you edit `README.md`, update `README.ko.md` as well.
3. Run the local checks below.
4. Sign off every commit (see below) and open a pull request using the template.

### Local checks

Requires Python 3.9 or later; no third-party packages are needed.

```bash
python scripts/validate.py --self-test
python scripts/validate.py
```

Changes to `scripts/validate.py` that add or change a rule must add a matching case to
`--self-test`.

### Developer Certificate of Origin (DCO)

All commits must be signed off to certify the
[Developer Certificate of Origin](https://developercertificate.org/):

```bash
git commit -s -m "Your message"
```

This adds a `Signed-off-by: Your Name <your-email>` line using your Git configuration. The CI job
`dco` checks every commit in a pull request (Dependabot pull requests are exempt). To sign off
commits you already made, run `git rebase --signoff main` and force-push your branch.
