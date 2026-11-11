# GDR-0003: License the training code under `train/` as Apache-2.0

- Status: Accepted
- Proposed: 2026-11-06 ([#20](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/20))
- Decided: 2026-11-11
- Owner: @moosunny
- Participants: @moosunny, @Sparrow-Co-Ltd
- Related issues and pull requests:
  [#20](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/20) (proposal),
  [#21](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/pull/21) (added `train/`)

## Context

[#21](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/pull/21) added `train/`: the LoRA SFT code for
`Qwen/Qwen3.5-9B` and the pipeline that selects the SFT trajectories. Until then the repository held
data, documentation, and stdlib-only scripts.

The repository [LICENSE](../../LICENSE) is CC BY 4.0, and [NOTICE.md](../../NOTICE.md) limits it to
the compilation and annotations of the dataset. `train/README.md` said the license of the code was
not decided. Code that is public without a license cannot be used, changed, or redistributed by
anyone outside Sparrow Co., Ltd., and a contributor cannot tell under which terms a pull request to
`train/` is accepted.

This record covers the license; the dependency intake and the other follow-up are tracked in #20.

## Options

1. **Apache-2.0.** The license of the published model and of `transformers`, `peft`, `datasets`, and
   `accelerate`, which the code builds on. It has an explicit patent grant and a contribution clause
   (section 5). It is on the allowed list in
   [POLICY.md](../evaluation/POLICY.md#2-license-lists). It requires keeping the license text and
   stating changes.
2. **MIT.** Shorter and equally permissive, but has no patent grant and no contribution clause, and
   it differs from the license of the model the code produces.
3. **CC BY 4.0, the repository license.** One license for the whole repository, but Creative Commons
   advises against using its licenses for software: there are no terms for source code or patents.
4. **Leave the code without a license.** No work now, but nobody outside the company may reuse the
   code, which defeats publishing it.

## Decision

Option 1. Everything under `train/` (source, tests, configuration, and its README) is
licensed under the Apache License 2.0, copyright Sparrow Co., Ltd. The license text is
[train/LICENSE](../../train/LICENSE).

- The repository `LICENSE` (CC BY 4.0) and its scope are unchanged.
- The license does not cover the third-party packages the code installs, the base model, the
  published model weights (see the model card), or the teacher trajectories, which are not in this
  repository.
- Contributions to `train/` are accepted under Apache-2.0 (inbound = outbound, Apache-2.0
  section 5), with the DCO sign-off that [CONTRIBUTING.md](../../CONTRIBUTING.md) already requires.

## Rationale and Consequences

- Users can run, change, and redistribute the training code, and the code and the model it produces
  carry the same license.
- Redistributors of `train/` keep `train/LICENSE` and the copyright notice in
  [NOTICE.md](../../NOTICE.md), and state their changes.
- The repository now has two licenses split by directory. NOTICE.md, both READMEs,
  `train/README.md`, and the `license` field of both `pyproject.toml` files state the split.
- Dataset users are not affected: no data file changes and CC BY 4.0 still covers the same parts.
- Source files get no per-file license header; `train/LICENSE` governs the directory.

## Dissent

None recorded.

## Follow-up

- Ask the author of [#27](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/pull/27), an outside
  contribution to `train/` merged on 2026-11-10 before this decision, to confirm it is made under
  Apache-2.0 / Maintainers / 2026-11-30.
- Decide the license of `scripts/`, which NOTICE.md does not name either, in a separate proposal /
  Maintainers / next governance review (2027-03-28).

## Review Triggers

- A dependency of `train/` whose license is incompatible with distributing the code under Apache-2.0.
- A change of the license of the published model.
- Third-party code copied into `train/` under another license.
- Moving `train/` to its own repository.
