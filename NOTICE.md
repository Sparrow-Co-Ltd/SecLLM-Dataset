# NOTICE

## 라이선스 적용 범위

본 저장소의 `LICENSE`(Creative Commons Attribution 4.0 International, CC BY 4.0)는
**SecLLM-Dataset의 편집물(compilation)과 주석 데이터에 적용**됩니다.

CC BY 4.0이 적용되는 부분은 다음과 같습니다.

- 데이터셋의 구성·선별·구조 및 스키마
- 취약점 유형명·유형 설명 (`issueNameKo/En`, `issueDescriptionKo/En`)
- 위험 예시 코드·안전 예시 코드 (`dangerousExampleKo/En`, `safeExampleKo/En`)
- 정적 분석 결과 및 추적 경로 주석 (`issueRisk`, `issueLineNumber`, `contexts`)

## 원본 소스코드의 라이선스

각 레코드의 `entireCode` 필드에는 **공개된 오픈소스 프로젝트의 소스 파일 원문**이 포함되어 있습니다.

**해당 소스코드는 CC BY 4.0의 적용 대상이 아니며, 각 원저작물의 원래 라이선스를 그대로 따릅니다.**
원본 소스는 허용적 라이선스(MIT, Apache-2.0, BSD 등)로 배포된 코드에서 수집되었으며,
이용자는 해당 코드를 사용·재배포할 때 원 라이선스가 요구하는 저작권 고지 및 조건을 준수해야 합니다.

## 데이터 출처

- 소스코드 원본: [bigcode/starcoderdata](https://huggingface.co/datasets/bigcode/starcoderdata)
  (허용적 라이선스로 배포된 오픈소스 코드로 필터링된 코퍼스)
- 취약점 탐지 및 주석: Sparrow SAST 정적 분석 결과

## 삭제 요청

포함된 소스코드에 대해 권리자로서 삭제를 요청하려면 저장소 이슈로 알려 주시기 바랍니다.
확인 후 해당 레코드를 제거하겠습니다.

## 지원 사업 표기

본 데이터셋은 과학기술정보통신부·정보통신산업진흥원(NIPA)
「2026년도 오픈소스 AI·SW 개발·활용 지원사업(활용트랙)」의 지원으로 제작되었습니다.