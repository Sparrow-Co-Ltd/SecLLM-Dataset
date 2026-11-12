# Intake evaluation: tree-sitter and the grammar packages

This record uses the 7-area scoring of the intake template, as set out in [POLICY.md](POLICY.md).
It was written on 2026-11-10 for a component already in use (retroactive intake): `train/` was added
in [#21](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/pull/21) and this intake was requested in
[#20](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/20). Facts were checked on 2026-11-10
against PyPI, the GitHub API, and api.scorecard.dev.

## Basic information

- **Candidate / version / commit:**
  [tree-sitter/py-tree-sitter](https://github.com/tree-sitter/py-tree-sitter) (PyPI `tree-sitter`)
  `0.25.2`; tag `v0.25.2` resolves to commit `e2a5b21449c30c6a4fb49a55567a4699c3271f10`; released
  2025-09-25; pinned with hashes in `train/judge/uv.lock`. Latest release on 2026-11-10: 0.26.1.
- **Companion components:** the 7 grammar packages published by the same organization, pinned in the
  same lock file and covered by this record, each with the commit its `v` tag resolves to:
  `tree-sitter-java` `0.23.5` (`94703d5a6bed02b98e438d7cad1136c01a60ba2c`); `tree-sitter-javascript`
  `0.25.0` (`44c892e0be055ac465d5eeddae6d3e194424e7de`); `tree-sitter-c` `0.24.2`
  (`b780e47fc780ddc8da13afa35a3f4ed5c157823d`); `tree-sitter-cpp` `0.23.4`
  (`f41e1a044c8a84ea9fa8577fdd2eab92ec96de02`); `tree-sitter-go` `0.25.0`
  (`1547678a9da59885853f5f5cc8a99cc203fa2e2c`); `tree-sitter-python` `0.25.0`
  (`293fdc02038ee2bf0e2e206711b69c90ac0d413f`); `tree-sitter-typescript` `0.23.2`
  (`f975a621f4e7f532fe322e13c4f79495e0a7b2e7`).
- **Use:** `secllm_judge/syntax_gate.py`: a patch whose patched file has more ERROR or MISSING nodes
  than the original fails before any judge call.
- **Transitive licenses outside the Allowed class:** none; these packages have no dependencies.
- **Distribution:** installed by the user with `uv sync` from PyPI; nothing is copied into this
  repository or a release.
- **Prepared by:** the Maintainers (see [MAINTAINERS.md](../../MAINTAINERS.md)).

## Candidates compared

| Candidate | Summary | Outcome |
|---|---|---|
| **tree-sitter with per-language grammars** | One parser API for the 7 dataset languages; error-tolerant | Selected |
| The compiler or parser of each language (javac, gcc, tsc, go vet, `ast`) | Exact syntax checks | Not selected: 7 toolchains to install, and single files rarely compile without their project |
| Bracket and quote balance heuristics | No dependency | Not selected: misses most syntax errors |

## Fatal conditions

- [x] Official source and version identified (tags, SHAs, and lock hashes above).
- [x] License identified: MIT for all 8 packages (allowed).
- [x] No condition forbids commercial use.
- [x] No unresolvable critical security risk: PyPI lists no advisory for `tree-sitter` 0.25.2. The
      parsers are C code that reads dataset source files and model-written patches, so they run only
      on the machine doing the selection.
- [x] Meets the functional need (syntax regression gate for 7 languages).
- [x] No code of unknown origin: all published by the tree-sitter organization.

## Scores

| Area | Max | Score | Facts and evidence | Judgment |
|---|---:|---:|---|---|
| License and rights | 20 | 20 | MIT (8 packages) | Allowed list |
| Security and supply chain | 20 | 12 | Lock hashes; no advisory on PyPI; OpenSSF Scorecard 4.8 for py-tree-sitter (2026-10-19) and 3.1 to 3.8 for six grammars (2026-10-19), none published for tree-sitter-c; compiled C parsers | Acceptable |
| Function and performance | 15 | 14 | Gate used in stage 2 of the selection | Fits |
| Maintainability | 15 | 12 | py-tree-sitter pushed 2026-11-09, one minor version behind 0.26.1; grammars last pushed 2026-09-13 to 2026-09-17 | Active, slower grammars |
| Architecture and operations | 10 | 8 | 8 packages whose versions must stay ABI-compatible | Version coupling |
| Community and governance | 10 | 8 | 1,520 stars for the binding; 278 to 573 per grammar; volunteer-run organization | Adequate |
| Sustainability and replaceability | 10 | 7 | No other single library covers the 7 languages | Hard to replace |
| **Total** | 100 | **81** | | |

## Decision

- **Decision:** approve.
- **Approved version and scope:** the 8 versions above, in the `train/judge/` environment only.
- **Conditions:** keep the lock hashes; upgrade the binding and the grammars together and run
  `test_sft_select.py` afterwards; 0.x minor versions are treated as major versions for
  re-evaluation.
- **Fallback:** skip the gate and let the judge decide (more judge calls), or per-language
  compilers.
- **Re-evaluation:** 2027-03-28, or earlier on any trigger in
  [POLICY.md](POLICY.md#3-re-evaluation), in particular a new major version or a security advisory.

## Evaluation history

| Date | Result |
|---|---|
| 2026-11-10 | First intake record: approve, 81/100 |
