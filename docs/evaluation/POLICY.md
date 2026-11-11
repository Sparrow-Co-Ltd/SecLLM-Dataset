# Open Source Evaluation Policy

This policy says how SecLLM-Dataset evaluates external components before using them (intake) and
how it checks itself before a release (release readiness). Records live in this directory:

| Record | Gate | Subject |
|---|---|---|
| [intake-starcoderdata.md](intake-starcoderdata.md) | Intake | Upstream source corpus |
| [intake-scorecard-action.md](intake-scorecard-action.md) | Intake | GitHub Action |
| [intake-actions-checkout.md](intake-actions-checkout.md) | Intake | GitHub Action |
| [intake-torch.md](intake-torch.md) | Intake | Python package, training (with the NVIDIA CUDA runtime wheels) |
| [intake-transformers.md](intake-transformers.md) | Intake | Python package, training |
| [intake-peft.md](intake-peft.md) | Intake | Python package, training |
| [intake-datasets.md](intake-datasets.md) | Intake | Python package, training |
| [intake-accelerate.md](intake-accelerate.md) | Intake | Python package, training |
| [intake-liger-kernel.md](intake-liger-kernel.md) | Intake | Python package, training |
| [intake-wandb.md](intake-wandb.md) | Intake | Python package, training |
| [intake-matplotlib.md](intake-matplotlib.md) | Intake | Python package, training (rejected: to be removed) |
| [intake-httpx.md](intake-httpx.md) | Intake | Python package, judge |
| [intake-pydantic.md](intake-pydantic.md) | Intake | Python package, judge |
| [intake-tree-sitter.md](intake-tree-sitter.md) | Intake | Python package, judge (with the 7 grammar packages) |
| [release-readiness-v1.0.0.md](release-readiness-v1.0.0.md) | Release | This dataset, 1.0.0 |

To request an evaluation, use the
[OSS evaluation form](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=oss_evaluation.yml).
Adding a new external component (a dataset, tool, GitHub Action, or Python package) is a Significant
decision under [GOVERNANCE.md](../../GOVERNANCE.md#4-decision-levels) and needs an intake record first.

**Python packages.** The training code under `train/` has two environments, `train/pyproject.toml`
and `train/judge/pyproject.toml`, each with a `uv.lock` that pins every package with hashes.

- Each **direct dependency** listed under `dependencies` needs an intake record. Packages that one
  upstream publishes for one purpose can share a record as companion components (for example the
  tree-sitter grammars).
- **Transitive dependencies** are covered by the record of the direct dependency that brings them
  in. Their licenses are checked against section 2 when the record is written and at each
  re-evaluation, and any license outside the Allowed class is named in the record.
- **Development-only tools** (the `dev` dependency group: test runner, linter) are pinned and
  license-checked the same way but need no record of their own.

## 1. How an evaluation is done

1. Fix the requirement and the exact version: a tag plus a 40-character commit SHA, a dataset
   revision, or a package version pinned with hashes in a lock file.
2. Compare at least two candidates.
3. Check the 6 fatal conditions (intake) or the 5 stop conditions (release). One failure stops the
   evaluation until it is resolved.
4. Score the 7 areas of the template with facts, evidence URLs, and the check date.
5. Record the decision, its scope, the conditions, and the re-evaluation triggers.

Scoring uses the **7-area scoring of the evaluation templates** (100 points). Intake: license and
rights 20, security and supply chain 20, function and performance 15, maintainability 15,
architecture and operations 10, community and governance 10, sustainability and replaceability 10.
Release: rights and license 20, security and privacy 20, build, test, and quality 15, documentation
and usability 15, governance and operations 15, supply chain and release 10, business alignment 5.

**Decision rule:** approve at 70 points or more **and** at least 10 of 20 points for license and
rights. Below that, reject or postpone. (The evaluation guide's 6-item table uses 70 points and 15
of 30 for license; this is the same rule scaled to the template's 20-point license area.)

## 2. License lists

### Software, Python packages, and GitHub Actions

| Class | Licenses | Rule |
|---|---|---|
| Allowed | MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, 0BSD, Zlib, PSF-2.0, CNRI-Python, MIT-CMU, CC0-1.0 | Use; keep the notice |
| Allowed with stronger notice | MPL-2.0, EPL-2.0 | Use; keep notices and file-level terms |
| Conditional | LGPL-2.1, LGPL-3.0 | Use only unmodified and dynamically combined; record the condition |
| Conditional | Proprietary runtime licenses (NVIDIA CUDA wheels) | Use only as an unmodified install-time dependency that the user downloads from the vendor's index; never copy it into this repository or a release; record the condition |
| Legal review first | GPL-2.0, GPL-3.0, AGPL-3.0 | Do not use until legal review is recorded |
| Forbidden | No license stated, CC-BY-NC for code, SSPL | Do not use |

A license that is in none of these classes (for example a project-specific license) is treated as
"Legal review first" until it is added to a class through a Significant decision.

### Code in this repository

- **Training code** (`train/`) is licensed under Apache-2.0
  ([GDR-0003](../decisions/0003-train-code-license.md)). Its dependencies must be compatible with
  distributing the code under that license. No dependency is copied into the repository.

### Data

- **Core data** (`data/java/`) is licensed CC BY 4.0 for the compilation and annotations. Code in
  `entireCode` keeps its upstream license (see [NOTICE.md](../../NOTICE.md)).
- **Community data** (`data/community/`) must use a license from the allowlist. The allowlist is
  `LICENSES` in [scripts/validate.py](../../scripts/validate.py), which CI enforces; the copy in
  [CONTRIBUTING.md](../../CONTRIBUTING.md#record-format) must match it. Today it is: `MIT`,
  `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `ISC`, `0BSD`, `Unlicense`, `CC0-1.0`, `Zlib`,
  `BSL-1.0`.
- **Upstream corpora** (such as starcoderdata) need an intake record. A corpus whose license is not a
  single SPDX identifier is at most "approve with conditions".
- A file whose own header states a different license than its repository is governed by that header
  ([GDR-0002](../decisions/0002-gpl-header-records.md)).

## 3. Re-evaluation

- **Cadence:** every intake record is re-checked every 6 months (next: 2027-03-28, together with the
  governance review), and before every release.
- **Triggers:** a new major version; a license change; an archived or transferred upstream; a
  security advisory or a CVSS 7.0+ vulnerability; a Scorecard score drop of 2 points or more; a
  rights holder's removal request.
- Dependabot pull requests that move an action's pinned SHA within the same major version are
  reviewed in the pull request itself; a new major version needs a re-evaluation.
- Pull requests that move a locked Python package are handled the same way for direct dependencies:
  the same major version is reviewed in the pull request, a new major version needs a
  re-evaluation. For a transitive dependency, the pull request review checks the changelog and that
  the license is still in the Allowed class, also for a new major version.
- A pull request that changes `train/uv.lock` or `train/judge/uv.lock` is checked with
  `uv lock --check --project <dir>` and by running the `train/` tests locally, because CI does not
  run them.
- Each re-check adds a dated line to the "Evaluation history" of the record.

## 4. Vulnerability response targets

For vulnerabilities in this repository's tooling and dependencies (scripts, workflows, and the
packages locked for `train/`), counted from triage. For a locked package, the fix is a lock update;
a mitigation is a recorded reason why the training code does not reach the affected function.
Vulnerabilities inside `entireCode` samples are the subject of the dataset and are out of scope
([SECURITY.md](../../SECURITY.md)).

| CVSS score | Severity | Fix or mitigate within |
|---|---|---|
| 9.0–10.0 | Critical | 24 hours |
| 7.0–8.9 | High | 1 week |
| 4.0–6.9 | Medium | 1 month |
| 0.1–3.9 | Low | 3 months |

Leaked secrets or personal data found in the dataset follow the same table as Critical for
containment and are removed in the next release ([SECURITY.md](../../SECURITY.md)).

## 5. SBOM

The repository's software dependencies are the GitHub Actions in `.github/workflows/` and the Python
packages locked in `train/uv.lock` and `train/judge/uv.lock`. The GitHub dependency graph reads all
three, so the export below covers them. At each release:

1. Export the SPDX 2.3 SBOM from the GitHub dependency graph:
   `gh api repos/Sparrow-Co-Ltd/SecLLM-Dataset/dependency-graph/sbom --jq .sbom > secllm-dataset-vX.Y.Z.spdx.json`
2. Attach it to the GitHub release: `gh release upload vX.Y.Z secllm-dataset-vX.Y.Z.spdx.json`
3. List the SHA-256 of every data file in [CHANGELOG.md](../../CHANGELOG.md), as for 1.0.0.

A release workflow that does this automatically is not in place yet; until then it is a manual
release step.

## 6. List change history

| Date | Change | Reference |
|---|---|---|
| 2026-09-21 | Community data license allowlist created (10 SPDX identifiers) | `fb835dd` |
| 2026-09-22 | Community data opened to JavaScript, TypeScript, Go, Python, C, and C++; allowlist unchanged | `c433c66` |
| 2026-09-28 | This policy: software license lists, decision rule, re-evaluation cadence, response targets, SBOM procedure | this document |
| 2026-11-10 | Python packages added as a component type (records for direct dependencies, lock files for transitive ones); Allowed class extended with 0BSD, Zlib, PSF-2.0, CNRI-Python, MIT-CMU, CC0-1.0; Conditional class for proprietary runtime licenses; SBOM and response targets cover the `train/` lock files | [#20](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/20) |
| 2026-11-10 | Code license for `train/`: Apache-2.0 | [GDR-0003](../decisions/0003-train-code-license.md) |
