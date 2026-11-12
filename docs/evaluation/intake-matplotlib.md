# Intake evaluation: matplotlib

This record uses the 7-area scoring of the intake template, as set out in [POLICY.md](POLICY.md).
It was written on 2026-11-10 for a component already in use (retroactive intake): `train/` was added
in [#21](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/pull/21) and this intake was requested in
[#20](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/20). Facts were checked on 2026-11-10
against PyPI, the GitHub API, and api.scorecard.dev.

## Basic information

- **Candidate / version / commit:**
  [matplotlib/matplotlib](https://github.com/matplotlib/matplotlib) `3.11.1`; tag `v3.11.1` resolves
  to commit `3c1757a567c58e41e565313af2d3bcdc52076b43`; released 2026-07-18; pinned with hashes in
  `train/uv.lock`. Latest release on 2026-11-10: 3.11.2.
- **Use:** none in this repository. `train/pyproject.toml` lists it "for the report figure scripts",
  and those scripts were not published; no file under `train/` imports it.
- **Transitive packages:** 10, among them `pillow` (MIT-CMU), which had published advisories at
  12.3.0 and was moved to 13.0.0 in [#25](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/pull/25)
  on 2026-11-10.
- **Distribution:** installed by the user with `uv sync` from PyPI; nothing is copied into this
  repository or a release.
- **Prepared by:** the Maintainers (see [MAINTAINERS.md](../../MAINTAINERS.md)).

## Candidates compared

| Candidate | Summary | Outcome |
|---|---|---|
| matplotlib | Plotting library | Not selected: nothing in the repository plots |
| **Remove the dependency** | Drops matplotlib and the packages only it needs (pillow, fonttools, contourpy, kiwisolver, cycler, pyparsing) | Selected |
| Optional dependency group for figures | Keeps it out of the default environment | Only if figure scripts are published later |

## Fatal conditions

- [x] Official source and version identified (tag, SHA, and lock hashes above).
- [ ] License identified, but not in a class: matplotlib uses its own license (based on the PSF
      license), which [POLICY.md](POLICY.md#2-license-lists) treats as "Legal review first" until it
      is classified.
- [x] No condition forbids commercial use.
- [x] No unresolvable critical security risk: the pillow advisories were fixed by the upgrade in
      #25; removing matplotlib removes pillow altogether.
- [ ] Meets a functional need: the published code does not use it.
- [x] No code of unknown origin: published by the Matplotlib project (NumFOCUS); OpenSSF Scorecard
      9.1 (2026-11-09).

## Scores

Not scored. Two fatal conditions fail, which stops the evaluation
([POLICY.md](POLICY.md#1-how-an-evaluation-is-done)).

## Decision

- **Decision:** reject: remove the dependency.
- **Approved version and scope:** none.
- **Conditions:** remove `matplotlib==3.11.1` from `train/pyproject.toml` and regenerate
  `train/uv.lock` in a separate pull request. Until then it stays pinned in the lock and is not
  imported.
- **Fallback:** if figure scripts are published later, open a new intake request and classify the
  matplotlib license first.
- **Re-evaluation:** when the removal pull request is merged, or on a new intake request.

## Evaluation history

| Date | Result |
|---|---|
| 2026-11-10 | First intake record: reject (unused; license not classified) |
