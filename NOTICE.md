# NOTICE

English | [한국어](#notice-한국어)

## License scope

The `LICENSE` of this repository (Creative Commons Attribution 4.0 International, CC BY 4.0)
**applies to the compilation and annotation data of SecLLM-Dataset**.

CC BY 4.0 covers:

- The composition, selection, structure, and schema of the dataset
- Vulnerability type names and descriptions (`issueNameKo/En`, `issueDescriptionKo/En`)
- Vulnerable and safe example code (`dangerousExampleKo/En`, `safeExampleKo/En`)
- Static analysis results and trace annotations (`issueRisk`, `issueLineNumber`, `contexts`)

## License of the training code

The code under `train/` is **not** covered by CC BY 4.0. It is licensed under the
[Apache License 2.0](train/LICENSE), Copyright 2026 Sparrow Co., Ltd.
(see [GDR-0003](docs/decisions/0003-train-code-license.md)).

The third-party packages that `train/` installs are not part of this repository and keep their own
licenses. The intake records in [docs/evaluation/](docs/evaluation/POLICY.md) list them.

## License of the original source code

The `entireCode` field of each record contains **original source files from public open-source projects**.

**That source code is not covered by CC BY 4.0 and remains under the original license of each work.**
It was collected from code distributed under permissive licenses (MIT, Apache-2.0, BSD, etc.).
When you use or redistribute that code, you must comply with the copyright notices and conditions required by its original license.

The upstream corpus selected code by **repository-level** license, not by file. An individual file can still carry its
own license header that differs from its repository's license: a scan of release 1.0.0 found GPL-family license text
(GPL, LGPL, AGPL) in roughly 80 of the 4,617 files, under 2%
(see [DATASHEET.md](DATASHEET.md#bias-risks-and-limitations)).
**Where a file's own header states a license, that header governs the file.** Check the header before reusing or
redistributing any `entireCode`. Those records are scheduled for removal in a future release; until then, follow the
license stated in each file's header.

## Data sources

- Original source code: [bigcode/starcoderdata](https://huggingface.co/datasets/bigcode/starcoderdata)
  (a corpus filtered to open-source code distributed under permissive licenses)
- Vulnerability detection and annotations: Sparrow SAST static analysis results

## Removal requests

If you are a rights holder and want included source code removed, submit the
[removal request form](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=removal-request.yml).
We will remove the affected records after verification.

## Funding acknowledgment

This dataset was produced with support from the Ministry of Science and ICT (MSIT) and the
National IT Industry Promotion Agency (NIPA) of Korea under the
"2026 Open Source AI/SW Development and Utilization Support Program (Utilization Track)".

---

# NOTICE (한국어)

## 라이선스 적용 범위

본 저장소의 `LICENSE`(Creative Commons Attribution 4.0 International, CC BY 4.0)는
**SecLLM-Dataset의 편집물(compilation)과 주석 데이터에 적용**됩니다.

CC BY 4.0이 적용되는 부분은 다음과 같습니다.

- 데이터셋의 구성·선별·구조 및 스키마
- 취약점 유형명·유형 설명 (`issueNameKo/En`, `issueDescriptionKo/En`)
- 위험 예시 코드·안전 예시 코드 (`dangerousExampleKo/En`, `safeExampleKo/En`)
- 정적 분석 결과 및 추적 경로 주석 (`issueRisk`, `issueLineNumber`, `contexts`)

## 학습 코드의 라이선스

`train/` 아래의 코드는 CC BY 4.0의 적용 대상이 **아닙니다**. 이 코드는
[Apache License 2.0](train/LICENSE)을 따르며, 저작권자는 Sparrow Co., Ltd.입니다(Copyright 2026 Sparrow Co., Ltd.,
[GDR-0003](docs/decisions/0003-train-code-license.md) 참조).

`train/`이 설치하는 서드파티 패키지는 이 저장소에 포함되어 있지 않으며 각자의 라이선스를 따릅니다.
목록은 [docs/evaluation/](docs/evaluation/POLICY.md)의 intake 기록에 있습니다.

## 원본 소스코드의 라이선스

각 레코드의 `entireCode` 필드에는 **공개된 오픈소스 프로젝트의 소스 파일 원문**이 포함되어 있습니다.

**해당 소스코드는 CC BY 4.0의 적용 대상이 아니며, 각 원저작물의 원래 라이선스를 그대로 따릅니다.**
원본 소스는 허용적 라이선스(MIT, Apache-2.0, BSD 등)로 배포된 코드에서 수집되었으며,
이용자는 해당 코드를 사용·재배포할 때 원 라이선스가 요구하는 저작권 고지 및 조건을 준수해야 합니다.

원본 코퍼스는 파일이 아니라 **저장소 단위** 라이선스로 코드를 선별했습니다. 따라서 개별 파일에 저장소 라이선스와 다른
라이선스 머리글이 있을 수 있습니다. 1.0.0 릴리스를 검사한 결과 4,617개 파일 중 약 80개(2% 미만)에서 GPL 계열(GPL, LGPL, AGPL)
라이선스 문구가 확인되었습니다([DATASHEET.md](DATASHEET.md#bias-risks-and-limitations) 참조).
**파일 머리글에 라이선스가 명시된 경우 해당 머리글이 그 파일에 적용됩니다.** `entireCode`를 재사용·재배포하기 전에 머리글을
확인하시기 바랍니다. 해당 레코드는 다음 릴리스에서 제거할 예정이며, 그때까지는 각 파일 머리글의 라이선스를 따라 주시기 바랍니다.

## 데이터 출처

- 소스코드 원본: [bigcode/starcoderdata](https://huggingface.co/datasets/bigcode/starcoderdata)
  (허용적 라이선스로 배포된 오픈소스 코드로 필터링된 코퍼스)
- 취약점 탐지 및 주석: Sparrow SAST 정적 분석 결과

## 삭제 요청

포함된 소스코드에 대해 권리자로서 삭제를 요청하려면
[삭제 요청 양식](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=removal-request.yml)으로 알려 주시기 바랍니다.
확인 후 해당 레코드를 제거하겠습니다.

## 지원 사업 표기

본 데이터셋은 과학기술정보통신부·정보통신산업진흥원(NIPA)
「2026년도 오픈소스 AI·SW 개발·활용 지원사업(활용트랙)」의 지원으로 제작되었습니다.
