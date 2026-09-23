# Changelog

All notable changes to this dataset are documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).
Dataset versions use `MAJOR.MINOR.PATCH`:

- **MAJOR**: breaking schema changes (fields renamed, removed, or retyped)
- **MINOR**: records added or removed, or new languages or tracks, without breaking the schema
- **PATCH**: corrections to existing records or documentation

Each release lists the SHA-256 of its data files. Verify with `sha256sum data/java/input.jsonl`.

## [Unreleased]

### Added

- C++ dataset (`data/cpp/input.jsonl`): 3,887 records across 108 vulnerability types
- JavaScript dataset (`data/javascript/input.jsonl`): 1,137 records across 37 vulnerability types
  Excludes 3 records flagged by GitHub push protection for credential patterns.
- Project policies: CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, GOVERNANCE, MAINTAINERS
- Datasheet (`DATASHEET.md`), English README with Korean translation (`README.ko.md`), `CITATION.cff`
- Validator (`scripts/validate.py`) and CI workflows
- Validator support for JavaScript, TypeScript, Go, Python, C, and C++ datasets,
  in addition to Java
- Community data track (`data/community/`) for data produced with third-party tools

### Changed

- NOTICE: English translation added; file-level license headers in `entireCode` take precedence
  (the upstream corpus filtered by repository-level license); removal requests go through an issue form

### Deprecated

- Records whose `entireCode` carries a GPL-family license header (roughly 80 files, under 2%) are scheduled for
  removal in a future release. Until then, the license in each file's header governs that file.

## [1.0.0] - 2026-09-20

### Added

- Initial Java release: `data/java/input.jsonl`, 4,617 records, 101 vulnerability types
- SHA-256 `9a03c0a04b39814be14876ae9683f6f450c497a9712f11d9f3b8be593880af37` (56,475,076 bytes)

[Unreleased]: https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/releases/tag/v1.0.0
