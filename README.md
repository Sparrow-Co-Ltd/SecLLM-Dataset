# SecLLM-Dataset

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

---

## 데이터셋 구성

```
SecLLM-Dataset/
└── data/
    └── java/
        └── input.jsonl                   # Java 취약점 + 해결 확인된 패치 4,617건 (약 54MB)
```

파일 형식은 **JSON Lines** 입니다. 한 줄이 하나의 취약점 인스턴스(JSON 객체)에 해당하며,
각 레코드는 취약점 정보(`input`)와 해당 취약점을 해결하는 패치(`output`)의 쌍으로 구성됩니다.

> 언어별로 디렉터리를 분리하며, 앞으로 Java 외 언어가 추가될 예정입니다.

---

## 데이터 통계

### 파일별


| 파일            | 레코드 수 | 형식             | 크기      |
| ------------- | ----- | -------------- | ------- |
| `input.jsonl` | 4,617 | input + output | 약 54 MB |


### 전체 (`input.jsonl` 기준)


| 항목        | 값                         |
| --------- | ------------------------- |
| 레코드 수     | 4,617                     |
| 언어        | Java (`.java`)            |
| 고유 취약점 유형 | 101종                      |
| 파일 크기     | 약 54 MB                   |
| 코드 길이(라인) | 최소 9 / 중앙값 117 / 최대 2,998 |


---

## 데이터 스키마

각 레코드는 최상위에 `input`(취약점 정보)과 `output`(패치) 2개 필드를 가집니다.


| 필드       | 타입     | 설명                                           |
| -------- | ------ | -------------------------------------------- |
| `input`  | object | 취약점 정보. 아래 14개 필드 참조                         |
| `output` | array  | 취약점을 해결하는 코드 수정 목록(codeModifications). 아래 참조 |


### `input` 필드

`input` 객체는 아래 14개 필드를 가집니다.


| 필드                    | 타입     | 설명                                          |
| --------------------- | ------ | ------------------------------------------- |
| `fileExtension`       | string | 원본 파일 확장자 (예: `.java`)                      |
| `programmingLanguage` | string | 프로그래밍 언어 (예: `Java`)                        |
| `issueRisk`           | string | 위험도. `매우 높음` / `높음` / `보통` / `낮음` / `매우 낮음` |
| `issueNameEn`         | string | 취약점 유형명 (영문)                                |
| `issueNameKo`         | string | 취약점 유형명 (한글)                                |
| `issueDescriptionEn`  | string | 취약점 유형 설명 (영문)                              |
| `issueDescriptionKo`  | string | 취약점 유형 설명 (한글)                              |
| `issueLineNumber`     | int    | 취약점이 보고된 라인 번호 (1-based, `entireCode` 기준)   |
| `entireCode`          | string | 취약점이 포함된 **전체 소스 파일 원문**                    |
| `dangerousExampleEn`  | string | 해당 유형의 취약한 예시 코드 (영문 주석, 라인 번호 포함)          |
| `dangerousExampleKo`  | string | 해당 유형의 취약한 예시 코드 (한글 주석, 라인 번호 포함)          |
| `safeExampleEn`       | string | 해당 유형의 안전한 예시 코드 (영문 주석, 라인 번호 포함)          |
| `safeExampleKo`       | string | 해당 유형의 안전한 예시 코드 (한글 주석, 라인 번호 포함)          |
| `contexts`            | array  | 정적 분석기의 추적 경로. 아래 참조                        |


`dangerousExample*` / `safeExample*` 는 **사전에 정의된 예시**이며, `entireCode`에서 발췌한 코드가 아닙니다.

#### `contexts[]` 필드

`contexts`는 취약점 판정에 이르기까지의 데이터 흐름을 순서대로 담은 배열입니다.


| 필드           | 타입     | 설명                                                       |
| ------------ | ------ | -------------------------------------------------------- |
| `lineNo`     | int    | 해당 이벤트가 발생한 라인 번호 (`entireCode` 기준)                      |
| `eventType`  | string | `source` / `branch` / `sink`                             |
| `messageKey` | string | 분석기 내부 메시지 식별자 (예: `jfsyn.DIRECT_USE_OF_THREADS.defect`) |
| `message`    | string | 사람이 읽을 수 있는 설명 (한글)                                      |
| `params`     | object | `message`에 삽입된 변수 값. 없으면 `{}`                            |


### `output[]` 필드


| 필드          | 타입            | 설명                                                       |
| ----------- | ------------- | -------------------------------------------------------- |
| `type`      | string        | `delete` / `add`                                         |
| `startLine` | int           | 대상 라인 번호 (1-based, **수정 전 `entireCode` 기준**)             |
| `endLine`   | int | null    | `delete` 시 삭제 구간의 끝 라인(포함). `add`는 `null`                |
| `content`   | string | null | `add` 시 `startLine` 앞에 삽입할 코드(여러 줄 가능). `delete`는 `null` |


모든 라인 번호는 수정 전 원본 코드 기준이며, `delete`는 `startLine`~`endLine`라인을 삭제하고`add`는 원본의` startLine`위치 앞에`content`를 삽입합니다(파일 끝을 넘는 경우 맨 뒤에 추가).

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
