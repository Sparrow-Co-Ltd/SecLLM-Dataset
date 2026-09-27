---
language:
  - en
  - ko
tags:
  - security
  - vulnerability-detection
  - program-repair
  - code
  - java
---

# SecLLM model

A model trained on SecLLM-Dataset to detect, explain, and patch security vulnerabilities in Java
source code. Dataset: see the Hugging Face repositories listed in
<https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/blob/main/COMMUNITY.md#hugging-face>.

## License

[TBD: model license]

## Model details

[TBD: model architecture, base model, training setup, evaluation results]

## Intended use

- Vulnerability detection and localization of the vulnerable line in Java files
- Explanation of the finding in Korean and English
- Patch suggestions for review by a developer
- Defensive research and tooling

## Out-of-scope use

- Treating output as ground truth about exploitability. The training labels are static-analysis findings, not confirmed exploits.
- Applying generated patches without human review. Patches in the training data were verified only by re-running the analyzer, not by compilation or tests, and may change program behavior.
- Languages other than Java.

## Dual use

The training data contains real vulnerable code patterns from public projects. Use the model for
defensive work: detection, explanation, and repair. Do not use it to attack, scan, or exploit systems or
projects without authorization. See the datasheet's responsible-use section:
<https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/blob/main/DATASHEET.md#responsible-use>.

## Limitations

The model inherits the training data's limits: labels from a single analyzer, no negative samples,
capped type frequencies, and Korean-only trace messages. See
<https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/blob/main/DATASHEET.md#bias-risks-and-limitations>.

## Where to ask

> GitHub is the source of record for data, bugs, and decisions; the Hugging Face Community tab covers questions about a specific Hugging Face revision; Discord is for chat only and never makes decisions; vulnerabilities and personal data are never posted publicly on any of them.

- Questions about this model revision: the Community tab of this repository. Include the revision, library versions, hardware, and a minimal reproduction.
- All channels: <https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/blob/main/COMMUNITY.md>
- Private contact (vulnerabilities, personal data, conduct): <https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/blob/main/SECURITY.md> and <https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/blob/main/CODE_OF_CONDUCT.md#how-to-report>

## Revision sync

| Release | GitHub commit | HF dataset revision | HF model revision | Known issues | Support channels |
|---|---|---|---|---|---|
| First model release | Set at upload | Set at upload | Set at upload | — | <https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/blob/main/COMMUNITY.md> |
