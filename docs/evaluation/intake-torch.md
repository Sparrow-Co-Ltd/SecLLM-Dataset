# Intake evaluation: torch (PyTorch) and the NVIDIA CUDA runtime wheels

This record uses the 7-area scoring of the intake template, as set out in [POLICY.md](POLICY.md).
It was written on 2026-11-10 for a component already in use (retroactive intake): `train/` was added
in [#21](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/pull/21) and this intake was requested in
[#20](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/20). Facts were checked on 2026-11-10
against PyPI, the GitHub API, and api.scorecard.dev.

## Basic information

- **Candidate / version / commit:** [pytorch/pytorch](https://github.com/pytorch/pytorch)
  `2.9.1+cu128`; tag `v2.9.1` resolves to commit `d38164a545b4a4e4e0cf73ce67173f70574890b6`;
  released 2025-11-12; pinned with hashes in `train/uv.lock`. Latest release on 2026-11-10: 2.15.0.
- **Use:** tensor library and CUDA backend for LoRA SFT (`train/sft/train_sft.py`), label masking
  (`srft_masking.py`), and the generation smoke test (`smoke_generate.py`).
- **Companion components:** the cu128 build depends on 15 `nvidia-*-cu12` wheels and `triton` (MIT).
  12 of the NVIDIA wheels (cublas, cuda-cupti, cuda-nvrtc, cuda-runtime, cudnn, cufft, cufile,
  curand, cusolver, cusparse, cusparselt, nvjitlink) are under NVIDIA's proprietary license;
  `nvidia-nccl-cu12` and `nvidia-nvshmem-cu12` are BSD-3-Clause and `nvidia-nvtx-cu12` is
  Apache-2.0. They are pinned in the same lock file and covered by this record.
- **Distribution:** installed by the user with `uv sync`: torch from
  `https://download.pytorch.org/whl/cu128` (set in `train/pyproject.toml`), the NVIDIA wheels from
  PyPI. Nothing is copied into this repository or a release.
- **Prepared by:** the Maintainers (see [MAINTAINERS.md](../../MAINTAINERS.md)).

## Candidates compared

| Candidate | Summary | Outcome |
|---|---|---|
| **torch (CUDA 12.8 build)** | Framework of the base model's reference implementation; required by `peft` and `liger-kernel` | Selected |
| JAX / Flax | Apache-2.0 | Not selected: no Liger kernels and no maintained Qwen3.5 LoRA path |
| torch CPU-only build | No NVIDIA wheels | Not possible for training: a 9B model needs a GPU |

## Fatal conditions

- [x] Official source and version identified (tag, SHA, and lock hashes above; official PyTorch
      wheel index).
- [x] License identified: torch is BSD-3-Clause (allowed). The 12 NVIDIA wheels are proprietary
      (Conditional class in [POLICY.md](POLICY.md#2-license-lists)).
- [x] No condition forbids commercial use of torch. The NVIDIA wheels are used unmodified under the
      vendor's runtime license and are not redistributed; the license text was not reviewed clause
      by clause for this record (see Conditions).
- [x] No unresolvable critical security risk: the open advisories below are fixed by an upgrade or
      are local-only, and the training code loads only the base model and adapters the user
      produced.
- [x] Meets the functional need (bf16 LoRA training of a 9B model on one GPU).
- [x] No code of unknown origin: published by the PyTorch project (Linux Foundation) and by NVIDIA.

## Scores

| Area | Max | Score | Facts and evidence | Judgment |
|---|---:|---:|---|---|
| License and rights | 20 | 14 | BSD-3-Clause; 12 proprietary NVIDIA runtime wheels, install-time only | Conditional |
| Security and supply chain | 20 | 11 | Lock hashes. PyPI lists 4 advisories for 2.9.1: GHSA-63cw-57p8-fm3p (CVE-2026-24747, High, CVSS 3.1 8.8, `weights_only` unpickler, fixed in 2.10.0), GHSA-qfhq-4f3w-5fph (Low, fixed in 2.10.0), GHSA-rrmf-rvhw-rf47 (Low, fixed in 2.13.0), PYSEC-2026-139 (CVE-2026-4538, CVSS 3.1 7.8, local attack on `pt2` loading, no fixed version listed). No current Scorecard result (the API returns one from 2022-10-26) | Needs the upgrade below |
| Function and performance | 15 | 15 | Trained the SFT adapter of the published model | Fits |
| Maintainability | 15 | 13 | Pushed 2026-11-10; 2.9.1 is 6 minor versions behind 2.15.0 | Active upstream, old pin |
| Architecture and operations | 10 | 8 | Needs a CUDA 12.8 GPU and a separate wheel index | Acceptable |
| Community and governance | 10 | 10 | PyTorch Foundation; 105,302 stars | Strong |
| Sustainability and replaceability | 10 | 8 | De facto standard; replacing it means replacing `peft` and `liger-kernel` too | Hard to replace, low risk |
| **Total** | 100 | **79** | | |

## Decision

- **Decision:** approve with conditions.
- **Approved version and scope:** `2.9.1+cu128` with the NVIDIA wheels in the lock, in the `train/`
  environment only.
- **Conditions:** (1) Upgrade to 2.10.0 or later, which fixes GHSA-63cw-57p8-fm3p; under
  [POLICY.md](POLICY.md#4-vulnerability-response-targets) the target for High is 1 week from triage.
  PYSEC-2026-139 has no fixed version, so condition 2 is its recorded mitigation. (2) Until then,
  load only the official base model and adapters you trained yourself. (3) Never commit or attach
  the NVIDIA wheels. (4) Read NVIDIA's license terms for the CUDA wheels and record the result at
  the next re-evaluation.
- **Fallback:** none for training; `--no-liger` and a newer torch are independent of each other.
- **Re-evaluation:** 2027-03-28, or earlier on any trigger in
  [POLICY.md](POLICY.md#3-re-evaluation), in particular a new major version or a security advisory.

## Evaluation history

| Date | Result |
|---|---|
| 2026-11-10 | First intake record: approve with conditions, 79/100 |
