# Governance

SecLLM-Dataset is a company-led open source project maintained by Sparrow Co., Ltd.

## Roles

- **Users** use the dataset and report problems through issues.
- **Contributors** open issues or pull requests (documentation, scripts, or community data),
  following [CONTRIBUTING.md](CONTRIBUTING.md).
- **Maintainers** are listed in [MAINTAINERS.md](MAINTAINERS.md). They triage issues, review and
  merge pull requests, re-verify data, publish releases, and enforce the
  [Code of Conduct](CODE_OF_CONDUCT.md).

## Decision Making

Maintainers decide by lazy consensus: a proposal in an issue or pull request is accepted when no
maintainer objects after a reasonable review period. When maintainers disagree, Sparrow Co., Ltd.
has the final say on dataset content and releases.

## Releases

1. Changes to core data (`data/java/`) are re-verified by the team with Sparrow SAST before release.
2. Every release gets an entry in [CHANGELOG.md](CHANGELOG.md) and a version number:
   - **MAJOR**: schema changes that break existing loaders
   - **MINOR**: records added or removed
   - **PATCH**: corrections to existing records or documentation
3. The `version` and `date-released` fields in [CITATION.cff](CITATION.cff) are updated to match.

## Becoming a Maintainer

Contributors with a sustained record of high-quality contributions may be invited by the existing
maintainers. The invitation is made through a pull request that adds the person to
[MAINTAINERS.md](MAINTAINERS.md).

## Changes to This Document

Changes to this governance document are made by pull request and require approval by the
maintainers.
