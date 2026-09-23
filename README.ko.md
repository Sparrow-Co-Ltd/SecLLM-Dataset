# SecLLM-Dataset

[English](README.md) | 한국어

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/Sparrow-Co-Ltd/SecLLM-Dataset/badge)](https://scorecard.dev/viewer/?uri=github.com/Sparrow-Co-Ltd/SecLLM-Dataset)

> **보안 취약점 탐지·설명·패치 LLM 학습을 위한 정적분석 기반 데이터셋**

SecLLM-Dataset은 정적 분석 도구(SAST)가 실제 오픈소스 코드에서 탐지한 보안 취약점을,
LLM 학습·평가에 사용할 수 있는 JSON Lines 형식으로 정리한 데이터셋입니다.

각 레코드는 단순한 `(코드, 라벨)` 쌍이 아니라 다음을 함께 제공합니다.

- 취약점이 발생한 **전체 소스 파일**과 **취약점 발생 라인**
- 취약점 유형에 대한 **한/영 설명**
- 같은 유형의 **취약한 예시 코드**와 **안전한 예시 코드** (한/영)
- 정적 분석기가 판단에 이르기까지의 **추적 경로(taint flow)** — source → branch → sink
- 취약점을 실제로 해결하는 **코드 수정 패치** — 패치 적용 후 SAST 재분석으로 해결이 확인된 수정만 수록

취약점 탐지뿐 아니라, 취약점 **설명 생성**, **패치 생성**,
**추론 경로 학습** 등 다양한 태스크에 활용할 수 있습니다.

제작 동기, 수집 과정, 한계, 책임 있는 사용에 대해서는 [데이터시트(영문)](DATASHEET.md)를 참고하세요.

---

## 데이터셋 구성

```
SecLLM-Dataset/
└── data/
    ├── java/
    │   └── input.jsonl        # Java 취약점 + 해결 확인된 패치 4,617건 (약 54MB)
    ├── javascript/
    │   └── input.jsonl        # JavaScript 취약점 + 패치 1,137건 (약 11MB)
    ├── cpp/
    │   └── input.jsonl        # C++ 취약점 + 패치 3,887건 (약 38MB)
    └── community/             # 커뮤니티 트랙: 서드파티 도구로 만든 데이터 (아래 참조)
```

파일 형식은 **JSON Lines** 입니다. 한 줄이 하나의 취약점 인스턴스(JSON 객체)에 해당하며,
각 레코드는 취약점 정보(`input`)와 해당 취약점을 해결하는 패치(`output`)의 쌍으로 구성됩니다.

> 언어별로 디렉터리를 분리하며, Java, JavaScript, C++ 데이터를 제공합니다.

## 데이터 등급

| 등급 | 경로 | 생성 주체 | 검증 |
| --- | --- | --- | --- |
| 코어 | `data/java/`, `data/javascript/`, `data/cpp/` | Sparrow SAST 탐지·주석 | 메인테이너가 Sparrow SAST로 패치를 재검증 |
| 커뮤니티 | `data/community/<언어>/` | 커뮤니티가 서드파티 도구(Semgrep, CodeQL 등)로 생성해 기여 | 기여자가 보증. CI는 스키마와 출처 정보만 검사 |

커뮤니티 레코드는 같은 `input`/`output` 스키마에 출처(도구, 규칙, 원본 저장소, 라이선스)를 담은
`meta` 객체가 필수로 추가됩니다. 자세한 내용은 [data/community/README.md](data/community/README.md)를 참고하세요.

---

## 데이터 통계

### 파일별

| 파일 | 레코드 수 | 형식 | 크기 |
| --- | --- | --- | --- |
| `data/java/input.jsonl` | 4,617 | input + output | 약 54 MB |
| `data/javascript/input.jsonl` | 1,137 | input + output | 약 11 MB (11,520,239 bytes) |
| `data/cpp/input.jsonl` | 3,887 | input + output | 약 38 MB (40,096,971 bytes) |

### Java (`data/java/input.jsonl` 기준)

| 항목 | 값 |
| --- | --- |
| 레코드 수 | 4,617 |
| 언어 | Java (`.java`) |
| 고유 취약점 유형 | 101종 |
| 파일 크기 | 약 54 MB (56,475,076 bytes) |
| 코드 길이(라인) | 최소 9 / 중앙값 117 / 최대 2,998 |

`python scripts/validate.py --stats data/java/input.jsonl` 로 다시 계산할 수 있습니다.

### JavaScript (`data/javascript/input.jsonl` 기준)

| 항목 | 값 |
| --- | --- |
| 레코드 수 | 1,137 |
| 언어 | JavaScript (`.js`) |
| 고유 취약점 유형 | 37종 |
| 파일 크기 | 약 11 MB (11,520,239 bytes) |
| 코드 길이(라인) | 최소 9 / 중앙값 93 / 최대 2,772 |

`python scripts/validate.py --stats data/javascript/input.jsonl` 로 다시 계산할 수 있습니다.

---

### C++ (`data/cpp/input.jsonl` 기준)

| 항목 | 값 |
| --- | --- |
| 레코드 수 | 3,887 |
| 언어 | C++ (`.cpp`) |
| 고유 취약점 유형 | 108종 |
| 파일 크기 | 약 38 MB (40,096,971 bytes) |
| 코드 길이(라인) | 최소 9 / 중앙값 95 / 최대 2,992 |

`python scripts/validate.py --stats data/cpp/input.jsonl` 로 다시 계산할 수 있습니다.

---

## 데이터 스키마

각 레코드는 최상위에 `input`(취약점 정보)과 `output`(패치) 2개 필드를 가집니다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `input` | object | 취약점 정보. 아래 14개 필드 참조 |
| `output` | array | 취약점을 해결하는 코드 수정 목록. 아래 참조 |

### `input` 필드

`input` 객체는 아래 14개 필드를 가집니다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `fileExtension` | string | 원본 파일 확장자 (예: `.java`) |
| `programmingLanguage` | string | 프로그래밍 언어 (예: `Java`) |
| `issueRisk` | string | 위험도. `매우 높음` / `높음` / `보통` / `낮음` / `매우 낮음` |
| `issueNameEn` | string | 취약점 유형명 (영문) |
| `issueNameKo` | string | 취약점 유형명 (한글) |
| `issueDescriptionEn` | string | 취약점 유형 설명 (영문) |
| `issueDescriptionKo` | string | 취약점 유형 설명 (한글) |
| `issueLineNumber` | int | 취약점이 보고된 라인 번호 (1-based, `entireCode` 기준) |
| `entireCode` | string | 취약점이 포함된 **전체 소스 파일 원문** |
| `dangerousExampleEn` | string | 해당 유형의 취약한 예시 코드 (영문 주석, 라인 번호 포함) |
| `dangerousExampleKo` | string | 해당 유형의 취약한 예시 코드 (한글 주석, 라인 번호 포함) |
| `safeExampleEn` | string | 해당 유형의 안전한 예시 코드 (영문 주석, 라인 번호 포함) |
| `safeExampleKo` | string | 해당 유형의 안전한 예시 코드 (한글 주석, 라인 번호 포함) |
| `contexts` | array | 정적 분석기의 추적 경로. 아래 참조 |

`dangerousExample*` / `safeExample*` 는 **사전에 정의된 예시**이며, `entireCode`에서 발췌한 코드가 아닙니다.

#### `contexts[]` 필드

`contexts`는 취약점 판정에 이르기까지의 데이터 흐름을 순서대로 담은 배열입니다.

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `lineNo` | int | 해당 이벤트가 발생한 라인 번호 (`entireCode` 기준) |
| `eventType` | string | `source` / `branch` / `sink` |
| `messageKey` | string | 분석기 내부 메시지 식별자 (예: `jfsyn.DIRECT_USE_OF_THREADS.defect`) |
| `message` | string | 사람이 읽을 수 있는 설명 (한글) |
| `params` | object | `message`에 삽입된 변수 값. 없으면 `{}` |

### `output[]` 필드

| 필드 | 타입 | 설명 |
| --- | --- | --- |
| `type` | string | `delete` / `add` |
| `startLine` | int | 대상 라인 번호 (1-based, **수정 전 `entireCode` 기준**) |
| `endLine` | int \| null | `delete` 시 삭제 구간의 끝 라인(포함). `add`는 `null` |
| `content` | string \| null | `add` 시 `startLine` 앞에 삽입할 코드(여러 줄 가능). `delete`는 `null` |

모든 라인 번호는 수정 전 원본 코드 기준입니다. `delete`는 `startLine`~`endLine` 라인을 삭제하고,
`add`는 원본의 `startLine` 위치 앞에 `content`를 삽입합니다(파일 끝을 넘는 경우 맨 뒤에 추가).

---

## 데이터 예시

```json
{
  "input": {
    "fileExtension": ".java",
    "programmingLanguage": "Java",
    "issueRisk": "높음",
    "issueNameEn": "Direct Use of Threads",
    "issueNameKo": "스레드의 직접 사용",
    "issueDescriptionEn": "The Direct Use of Threads checker finds instances of a J2EE Web application directly using threads. ...",
    "issueDescriptionKo": "스레드의 직접 사용 체커는 J2EE 웹 애플리케이션에서 직접적으로 스레드를 사용하는 경우를 검출합니다. ...",
    "issueLineNumber": 23,
    "entireCode": "package io.opentracing.contrib.specialagent.test.servlet.jetty;\n\nimport java.io.PrintWriter;\n...",
    "dangerousExampleEn": "1. public class U383 extends HttpServlet {\n2.   protected void doGet(...)\n...",
    "dangerousExampleKo": "1. public class U383 extends HttpServlet {\n2.   protected void doGet(...)\n...",
    "safeExampleEn": "1. public class S383 extends HttpServlet {\n...",
    "safeExampleKo": "1. public class S383 extends HttpServlet {\n...",
    "contexts": [
      {
        "lineNo": 23,
        "eventType": "sink",
        "messageKey": "jfsyn.DIRECT_USE_OF_THREADS.defect",
        "message": "Thread 를 직접 생성하거나 사용하지 않도록 합니다.",
        "params": {}
      }
    ]
  },
  "output": [
    {
      "type": "delete",
      "startLine": 23,
      "endLine": 40,
      "content": null
    },
    {
      "type": "add",
      "startLine": 23,
      "endLine": null,
      "content": "    asyncContext.start(new Runnable() {\n      @Override\n      public void run() {\n..."
    }
  ]
}
```

---

## 사용 방법

### Python (표준 라이브러리)

```python
import json

records = []
with open("data/java/input.jsonl", encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))

print(len(records))                      # 4617
r = records[0]
inp = r["input"]
print(inp["issueNameKo"], inp["issueRisk"])  # 스레드의 직접 사용 높음

# 취약점이 발생한 라인 확인
lines = inp["entireCode"].split("\n")
print(lines[inp["issueLineNumber"] - 1])

# 패치(코드 수정 목록) 확인
for mod in r["output"]:
    print(mod["type"], mod["startLine"], mod["endLine"])
```

### pandas

```python
import pandas as pd

df = pd.read_json("data/java/input.jsonl", lines=True)
inputs = pd.json_normalize(df["input"])
print(inputs["issueNameEn"].value_counts())
```

> 파일이 약 54MB이므로 전체를 메모리에 올릴 수 있지만, 대용량 처리 시에는 스트리밍 방식을 권장합니다.

---

## 데이터 검증

`scripts/validate.py`는 스키마와 필드 간 규칙(라인 범위, `delete`/`add` 의미, 커뮤니티 출처 정보)을 검사합니다. Python 표준 라이브러리만 사용합니다.

```bash
python scripts/validate.py --self-test                     # 검증기 자체 점검
python scripts/validate.py                                 # data/**/*.jsonl 전체 검증
python scripts/validate.py --stats data/java/input.jsonl   # 통계 출력
```

## 인용

인용 정보는 [CITATION.cff](CITATION.cff)에 있습니다(GitHub의 "Cite this repository" 버튼으로도 확인할 수 있습니다).

```bibtex
@misc{secllm_dataset_2026,
  title        = {SecLLM-Dataset: A Static-Analysis-Based Dataset for Vulnerability Detection, Explanation, and Repair with LLMs},
  author       = {{Sparrow Co., Ltd.}},
  year         = {2026},
  howpublished = {\url{https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset}},
  note         = {Version 1.0.0}
}
```

## 기여하기

코어 데이터는 메인테이너가 Sparrow SAST로 재검증한 뒤에만 변경합니다. 데이터 오류 제보, 문서·스크립트 개선,
커뮤니티 트랙에 서드파티 도구 데이터 기여로 참여할 수 있습니다. 정책 문서는 영문으로 작성되어 있습니다.

- [CONTRIBUTING.md](CONTRIBUTING.md): 기여 방법 (커밋에 DCO 서명 필요)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): 행동 강령
- [SECURITY.md](SECURITY.md): 보안 문제 신고 방법
- [GOVERNANCE.md](GOVERNANCE.md): 의사결정 방식
- [CHANGELOG.md](CHANGELOG.md): 릴리스 이력

## 도움 받기

- 질문과 데이터 오류: [GitHub Issues](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues)
- 보안 문제: [SECURITY.md](SECURITY.md)의 절차를 따라 주세요 (공개 이슈로 올리지 마세요)
- 권리자의 삭제 요청: [삭제 요청 양식](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=removal-request.yml)

## 라이선스

SecLLM-Dataset의 편집물과 주석 데이터는
[크리에이티브 커먼즈 저작자표시 4.0 국제 라이선스(CC BY 4.0)](LICENSE)를 따릅니다.

`entireCode` 필드에는 공개 오픈소스 프로젝트의 소스 파일 원문이 들어 있습니다. 이 코드는 CC BY 4.0의
적용 대상이 **아니며** 각 원저작물의 라이선스를 따릅니다. 정확한 적용 범위는 [NOTICE.md](NOTICE.md)를 참고하세요.

## 지원 사업 표기

본 데이터셋은 과학기술정보통신부·정보통신산업진흥원(NIPA)
「2026년도 오픈소스 AI·SW 개발·활용 지원사업(활용트랙)」의 지원으로 제작되었습니다.
