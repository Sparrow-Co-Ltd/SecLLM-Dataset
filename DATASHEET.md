# Datasheet: SecLLM-Dataset

This datasheet follows the structure of *Datasheets for Datasets* (Gebru et al., 2021, arXiv:1803.09010)
and adds the risk, personal-information, and responsible-use sections of Hugging Face dataset cards.
Numbers refer to release 1.0.0 (`data/java/input.jsonl`) and can be recomputed with
`python scripts/validate.py --stats data/java/input.jsonl`.

## Motivation

- **Purpose.** To train and evaluate large language models on three connected security tasks:
  detecting a vulnerability in a real source file, explaining it, and producing a patch that removes it.
  Most public vulnerability datasets provide `(function, label)` pairs; this dataset keeps the whole file,
  the analyzer's data-flow trace, bilingual (Korean/English) explanations, and a verified patch per finding.
- **Creator.** Sparrow Co., Ltd. Maintainers are listed in [MAINTAINERS.md](MAINTAINERS.md).
- **Funding.** Ministry of Science and ICT (MSIT) and National IT Industry Promotion Agency (NIPA) of Korea,
  "2026 Open Source AI/SW Development and Utilization Support Program (Utilization Track)".

## Composition

- **Instances.** Each instance is one SAST finding in one Java source file, paired with a patch.
  Release 1.0.0 has **4,617 records**; every record has a distinct `entireCode` (4,617 distinct files).
- **Fields.** `input` (14 fields: file metadata, risk level, bilingual type name and description, reported line,
  full source file, bilingual predefined vulnerable/safe examples, analyzer trace) and `output`
  (line-based `delete`/`add` modifications). The full schema is in the [README](README.md#schema).
- **Vulnerability types.** 101 unique types (`issueNameEn`). The ten most frequent types have 97–100 records each;
  8 types have a single record.
- **Risk levels (`issueRisk`).** 보통 (medium) 2,144; 높음 (high) 1,901; 낮음 (low) 239; 매우 낮음 (very low) 197; 매우 높음 (very high) 136.
- **Trace events (`contexts`).** 9,736 events in total: 4,671 `sink`, 2,975 `branch`, 2,090 `source`.
  Every record has 1 to 47 events.
- **Patches (`output`).** Every record has exactly one `delete` operation; 4,524 records also have one `add`
  operation (93 records are deletion-only).
- **Code length.** 9 to 2,998 lines per file (median 117).
- **Labels.** All records are positive findings reported by the analyzer. There are no negative (non-vulnerable) samples;
  the post-patch file can be reconstructed from `entireCode` and `output` and was not reported by the analyzer for the same finding.
- **Splits.** No train/validation/test split is provided in this release.
- **Self-contained.** Yes. The source code is embedded; no external download is needed.

## Collection Process

- **Source code.** Java files from [bigcode/starcoderdata](https://huggingface.co/datasets/bigcode/starcoderdata),
  a corpus of source code from repositories distributed under permissive licenses.
- **Sampling.** The procedure for selecting files from starcoderdata is not documented in this release.
  No type has more than 100 records, which suggests a per-type cap.
- **Detection.** Files were analyzed with the Sparrow SAST static analyzer. Each finding provides the type,
  risk level, reported line, and the data-flow trace (`contexts`).
- **Patches.** Patches come from remediation suggestions produced in the Sparrow workflow. The generation method
  is not documented in this release. A patch is included only if re-running Sparrow SAST on the patched file
  confirmed that the finding was resolved.
- **Time frame.** Not documented in this release. The data was first committed to this repository in August 2026; release 1.0.0 is dated 2026-09-19.

## Preprocessing and Labeling

- `issueName*`, `issueDescription*`, `dangerousExample*`, and `safeExample*` are predefined per vulnerability type
  by the analyzer and are **not** excerpts from `entireCode`.
- `contexts[].message` is the analyzer's Korean message; `messageKey` and `params` allow regenerating it.
- Line numbers in `issueLineNumber`, `contexts[].lineNo`, and `output[]` are 1-based and refer to the original `entireCode`.
- `entireCode` keeps the upstream text, including the PII placeholders introduced by starcoderdata's redaction
  (see [Personal and Sensitive Information](#personal-and-sensitive-information)).
- Manual review of individual findings or patches is not documented in this release.

## Uses

- **Intended uses.** Vulnerability detection, localization of the vulnerable line, explanation generation
  (Korean and English), patch generation, and learning from analyzer traces. Also usable as an evaluation set
  for these tasks.
- **Out-of-scope uses.**
  - Claiming ground truth about exploitability: findings are static-analysis results, not confirmed exploits.
  - Evaluating on "vulnerable vs. safe" classification without adding negative samples.
  - Treating patches as behavior-preserving: they were verified by the analyzer; test-based verification is not documented.
  - Any use listed under [Responsible Use](#responsible-use) as prohibited.

## Distribution

- **Where.** This GitHub repository (`data/java/input.jsonl`, about 54 MB, JSON Lines).
- **License.** The compilation and annotations are licensed under [CC BY 4.0](LICENSE). The code in `entireCode`
  keeps its original licenses and is not covered by CC BY 4.0. See [NOTICE.md](NOTICE.md).
- **Integrity.** The SHA-256 of each released data file is recorded in [CHANGELOG.md](CHANGELOG.md).

## Maintenance

- **Maintainers.** See [MAINTAINERS.md](MAINTAINERS.md) and [GOVERNANCE.md](GOVERNANCE.md).
- **Errors.** Report wrong labels, false positives, or incorrect patches with the
  [data error form](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=data-error.yml).
  Maintainers re-verify reports with Sparrow SAST and ship fixes in the next release.
- **Removal.** Rights holders can request removal with the
  [removal request form](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=removal-request.yml).
- **Contributions.** Data produced with other tools goes to the community track (`data/community/`);
  see [CONTRIBUTING.md](CONTRIBUTING.md) and [data/community/README.md](data/community/README.md).
- **Releases.** Changes are recorded in [CHANGELOG.md](CHANGELOG.md); see [Versioning](#versioning).

## Bias, Risks, and Limitations

- **Analyzer bias.** All core labels come from a single static analyzer. The dataset inherits its false positives,
  false negatives, and its choice of vulnerability types. Many types are code-quality or reliability issues
  (for example, excessively broad exception objects) rather than exploitable vulnerabilities.
- **Patch verification.** "Resolved" means the same analyzer no longer reports the finding. Compilation or test
  verification of patches is not documented in this release, and a patch may change program behavior.
- **Type frequencies.** No type has more than 100 records, so type frequencies do not reflect real-world prevalence.
- **Language coverage.** Java only in this release.
- **Language of annotations.** `contexts[].message` and `issueRisk` values are in Korean; English is available for type names,
  descriptions, and examples.
- **Upstream licensing.** starcoderdata filtered code by repository-level license. Individual files can still carry their own
  license headers: a header scan of release 1.0.0 found GPL-family license text in 79 files, 69 of them without any
  permissive-license mention. Treat the per-file header as authoritative and see [NOTICE.md](NOTICE.md).
- **Redaction artifacts.** Upstream PII redaction replaced some identifiers in code and comments with placeholders
  (for example `<PASSWORD>` or `<KEY>`), which can make a file syntactically or semantically different from the original project.

## Personal and Sensitive Information

- No personal information was collected by the dataset creators beyond what is in the upstream source files.
- starcoderdata applied PII redaction before this dataset was built. Placeholders remain in `entireCode`:
  `<NAME>` in 804 records, `<EMAIL>` in 307, `<PASSWORD>` in 129, and `<KEY>` in 26.
- Redaction is not perfect. Author names, handles, or other identifiers in headers and comments may remain.
- If you find personal or sensitive information, use the
  [removal request form](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=removal-request.yml)
  or, for credentials, follow [SECURITY.md](SECURITY.md).

## Responsible Use

- The dataset contains real vulnerable code patterns from public projects. It is intended for **defensive** research
  and tooling: detection, explanation, and repair.
- Do not use this dataset to attack, scan, or exploit systems or projects without authorization.
- Findings in `entireCode` are intentional dataset content. They are not reports against this repository; if you believe
  an upstream project is still affected, report it to that project through its own security process.
- Models trained on this data can produce incorrect findings and patches. Keep a human review step before applying
  generated patches to production code.

## Versioning

- Releases follow `MAJOR.MINOR.PATCH`:
  - **MAJOR**: breaking schema changes (fields renamed, removed, or retyped).
  - **MINOR**: records added or removed, or new languages or tracks, without breaking the schema.
  - **PATCH**: corrections to existing records or documentation.
- Each release is listed in [CHANGELOG.md](CHANGELOG.md) with the SHA-256 of its data files, and the version in
  [CITATION.cff](CITATION.cff) is updated to match.
