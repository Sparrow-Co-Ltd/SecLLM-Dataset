---
license: cc-by-4.0
language:
  - en
  - ko
pretty_name: SecLLM-Dataset
task_categories:
  - text-generation
  - text-classification
tags:
  - security
  - vulnerability-detection
  - program-repair
  - static-analysis
  - sast
  - code
  - java
size_categories:
  - 1K<n<10K
configs:
  - config_name: java
    data_files:
      - split: train
        path: data/java/input.jsonl
---

# SecLLM-Dataset

A static-analysis-based dataset for training LLMs to detect, explain, and patch security
vulnerabilities. Release 1.0.0 has 4,617 records from real open-source Java files. Each record holds
the full source file, the reported line, bilingual (Korean/English) type descriptions and examples,
the analyzer's data-flow trace (source → branch → sink), and a patch whose fix was confirmed by
re-running Sparrow SAST.

The Hub shows the data as a single `train` split for loading convenience; the release has no official
train/validation/test split.

- Datasheet (motivation, composition, collection, limitations, responsible use): <https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/blob/main/DATASHEET.md>
- Schema and usage examples: <https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset#schema>
- Source of record, issues, and releases: <https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset>

## License

The compilation and annotations are licensed under CC BY 4.0. The source code in `entireCode` is
**not** covered by CC BY 4.0 and keeps its original licenses; where a file's own header states a
license, that header governs the file. See
<https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/blob/main/NOTICE.md>.

## Where to ask

> GitHub is the source of record for data, bugs, and decisions; the Hugging Face Community tab covers questions about a specific Hugging Face revision; Discord is for chat only and never makes decisions; vulnerabilities and personal data are never posted publicly on any of them.

- Questions about this Hub revision: the Community tab of this repository.
- Wrong labels, false positives, or bad patches: the [data error form](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=data-error.yml) on GitHub.
- All channels: <https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/blob/main/COMMUNITY.md>

When you ask in the Community tab, include:

- The revision (commit) of this repository you loaded
- Your `datasets` library, Python, and OS versions
- The expected and actual result, with a minimal reproduction
- The record file and 1-based line number, if a specific record is involved

## Private contact

Do not post vulnerabilities, credentials, or personal data here.

- Vulnerabilities in the repository tooling, leaked secrets or personal data: <https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/blob/main/SECURITY.md>
- Removal of your code or personal data, or a conduct report: <https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/blob/main/CODE_OF_CONDUCT.md#how-to-report>

## Revision sync

| Release | GitHub commit | HF dataset revision | HF model revision | Known issues | Support channels |
|---|---|---|---|---|---|
| 1.0.0 | Set at upload | Set at upload | — | GPL-family headers in about 80 files (see NOTICE) | <https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/blob/main/COMMUNITY.md> |

`data/java/input.jsonl` SHA-256 for 1.0.0: `9a03c0a04b39814be14876ae9683f6f450c497a9712f11d9f3b8be593880af37`.

## Citation

See <https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/blob/main/CITATION.cff>.

## Acknowledgments

Produced with support from the Ministry of Science and ICT (MSIT) and the National IT Industry
Promotion Agency (NIPA) of Korea under the "2026 Open Source AI/SW Development and Utilization
Support Program (Utilization Track)".
