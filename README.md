# SecLLM-Dataset

English | [한국어](README.ko.md)

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/Sparrow-Co-Ltd/SecLLM-Dataset/badge)](https://scorecard.dev/viewer/?uri=github.com/Sparrow-Co-Ltd/SecLLM-Dataset)

> **A static-analysis-based dataset for training LLMs to detect, explain, and patch security vulnerabilities**

SecLLM-Dataset collects security vulnerabilities that a static application security testing (SAST) tool
found in real open-source code, packaged as JSON Lines for LLM training and evaluation.

Each record is more than a `(code, label)` pair. It provides:

- The **entire source file** where the vulnerability occurs and the **vulnerable line**
- A **Korean/English description** of the vulnerability type
- A **vulnerable example** and a **safe example** of the same type (Korean/English)
- The **taint flow** the analyzer followed to reach its verdict: source → branch → sink
- A **code patch** that actually fixes the vulnerability. Only patches confirmed by re-running SAST after applying them are included

Besides detection, the data supports tasks such as **explanation generation**, **patch generation**,
and **reasoning-path learning**.

For motivation, collection process, limitations, and responsible use, see the [datasheet](DATASHEET.md).

---

## Dataset layout

```
SecLLM-Dataset/
└── data/
    ├── java/
    │   └── input.jsonl        # Java vulnerabilities + verified patches, 4,617 records (~54 MB)
    ├── javascript/
    │   └── input.jsonl        # JavaScript vulnerabilities + patches, 1,137 records (~11 MB)
    ├── cpp/
    │   └── input.jsonl        # C++ vulnerabilities + patches, 3,887 records (~38 MB)
    └── community/             # Community track: data from third-party tools (see below)
```

Files are **JSON Lines**: one line is one vulnerability instance (a JSON object).
Each record pairs vulnerability information (`input`) with a patch that fixes it (`output`).

> Data is split by language. Java, JavaScript and C++ datasets are available.

## Data tiers

| Tier | Path | Produced by | Verification |
| --- | --- | --- | --- |
| Core | `data/java/`, `data/javascript/`, `data/cpp/` | Sparrow SAST detection and annotation | Patches re-verified by the maintainers with Sparrow SAST |
| Community | `data/community/<lang>/` | Third-party tools (e.g. Semgrep, CodeQL), contributed by the community | Attested by the contributor; CI checks schema and provenance only |

Community records use the same `input`/`output` schema plus a required `meta` object with provenance
(tool, rule, source repository, license). See [data/community/README.md](data/community/README.md).

---

## Statistics

### By file

| File | Records | Format | Size |
| --- | --- | --- | --- |
| `data/java/input.jsonl` | 4,617 | input + output | ~54 MB |
| `data/javascript/input.jsonl` | 1,137 | input + output | ~11 MB (11,520,239 bytes) |
| `data/cpp/input.jsonl` | 3,887 | input + output | ~38 MB (40,096,971 bytes) |

### Java (`data/java/input.jsonl`)

| Item | Value |
| --- | --- |
| Records | 4,617 |
| Language | Java (`.java`) |
| Unique vulnerability types | 101 |
| File size | ~54 MB (56,475,076 bytes) |
| Code length (lines) | min 9 / median 117 / max 2,998 |

Recompute with `python scripts/validate.py --stats data/java/input.jsonl`.

### JavaScript (`data/javascript/input.jsonl`)

| Item | Value |
| --- | --- |
| Records | 1,137 |
| Language | JavaScript (`.js`) |
| Unique vulnerability types | 37 |
| File size | ~11 MB (11,520,239 bytes) |
| Code length (lines) | min 9 / median 93 / max 2,772 |

Recompute with `python scripts/validate.py --stats data/javascript/input.jsonl`.

---

### C++ (`data/cpp/input.jsonl`)

| Item | Value |
| --- | --- |
| Records | 3,887 |
| Language | C++ (`.cpp`) |
| Unique vulnerability types | 108 |
| File size | ~38 MB (40,096,971 bytes) |
| Code length (lines) | min 9 / median 95 / max 2,992 |

Recompute with `python scripts/validate.py --stats data/cpp/input.jsonl`.

---

## Schema

Each record has two top-level fields: `input` (vulnerability information) and `output` (patch).

| Field | Type | Description |
| --- | --- | --- |
| `input` | object | Vulnerability information. See the 14 fields below |
| `output` | array | Code modifications that fix the vulnerability. See below |

### `input` fields

| Field | Type | Description |
| --- | --- | --- |
| `fileExtension` | string | Source file extension (e.g. `.java`) |
| `programmingLanguage` | string | Programming language (e.g. `Java`) |
| `issueRisk` | string | Risk level: `매우 높음` (very high) / `높음` (high) / `보통` (medium) / `낮음` (low) / `매우 낮음` (very low) |
| `issueNameEn` | string | Vulnerability type name (English) |
| `issueNameKo` | string | Vulnerability type name (Korean) |
| `issueDescriptionEn` | string | Vulnerability type description (English) |
| `issueDescriptionKo` | string | Vulnerability type description (Korean) |
| `issueLineNumber` | int | Reported line number (1-based, relative to `entireCode`) |
| `entireCode` | string | **Full original source file** containing the vulnerability |
| `dangerousExampleEn` | string | Vulnerable example for this type (English comments, with line numbers) |
| `dangerousExampleKo` | string | Vulnerable example for this type (Korean comments, with line numbers) |
| `safeExampleEn` | string | Safe example for this type (English comments, with line numbers) |
| `safeExampleKo` | string | Safe example for this type (Korean comments, with line numbers) |
| `contexts` | array | Analyzer trace. See below |

`dangerousExample*` / `safeExample*` are **predefined examples** per vulnerability type, not excerpts from `entireCode`.

#### `contexts[]` fields

`contexts` lists, in order, the data-flow events that led to the finding.

| Field | Type | Description |
| --- | --- | --- |
| `lineNo` | int | Line where the event occurs (relative to `entireCode`) |
| `eventType` | string | `source` / `branch` / `sink` |
| `messageKey` | string | Analyzer message identifier (e.g. `jfsyn.DIRECT_USE_OF_THREADS.defect`) |
| `message` | string | Human-readable explanation (Korean) |
| `params` | object | Values substituted into `message`; `{}` if none |

### `output[]` fields

| Field | Type | Description |
| --- | --- | --- |
| `type` | string | `delete` / `add` |
| `startLine` | int | Target line (1-based, **relative to the original `entireCode`**) |
| `endLine` | int \| null | For `delete`, last deleted line (inclusive). `null` for `add` |
| `content` | string \| null | For `add`, code inserted before `startLine` (may span lines). `null` for `delete` |

All line numbers refer to the original code before modification. `delete` removes lines `startLine` through `endLine`;
`add` inserts `content` before line `startLine` of the original (appended at the end if past the last line).

---

## Example

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

## Usage

### Python (standard library)

```python
import json

records = []
with open("data/java/input.jsonl", encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))

print(len(records))                      # 4617
r = records[0]
inp = r["input"]
print(inp["issueNameEn"], inp["issueRisk"])  # Direct Use of Threads 높음

# Show the vulnerable line
lines = inp["entireCode"].split("\n")
print(lines[inp["issueLineNumber"] - 1])

# Show the patch (code modifications)
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

> The file is about 54 MB and fits in memory, but streaming is recommended for large-scale processing.

---

## Validation

`scripts/validate.py` checks the schema and cross-field rules (line ranges, `delete`/`add` semantics, community provenance). It needs only the Python standard library.

```bash
python scripts/validate.py --self-test                     # validator checks itself
python scripts/validate.py                                 # validate every data/**/*.jsonl
python scripts/validate.py --stats data/java/input.jsonl   # print statistics
```

## Citation

Citation metadata is in [CITATION.cff](CITATION.cff) (GitHub shows a "Cite this repository" button).

```bibtex
@misc{secllm_dataset_2026,
  title        = {SecLLM-Dataset: A Static-Analysis-Based Dataset for Vulnerability Detection, Explanation, and Repair with LLMs},
  author       = {{Sparrow Co., Ltd.}},
  year         = {2026},
  howpublished = {\url{https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset}},
  note         = {Version 1.0.0}
}
```

## Contributing

Core data is changed only by the maintainers after re-verification with Sparrow SAST. You can help by reporting
data errors, sending documentation or script improvements, or contributing third-party-tool data to the community track.

- [CONTRIBUTING.md](CONTRIBUTING.md): how to contribute (commits must be signed off under the DCO)
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): community standards
- [SECURITY.md](SECURITY.md): how to report security issues
- [GOVERNANCE.md](GOVERNANCE.md): how decisions are made
- [CHANGELOG.md](CHANGELOG.md): release history

## Getting help

- Questions and data errors: [GitHub Issues](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues)
- Security issues: follow [SECURITY.md](SECURITY.md) (do not open a public issue)
- Removal requests from rights holders: [removal request form](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=removal-request.yml)

## License

The compilation and annotations of SecLLM-Dataset are licensed under
[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).

The `entireCode` field contains original source files from public open-source projects. That code is **not**
covered by CC BY 4.0 and remains under its original licenses. See [NOTICE.md](NOTICE.md) for the exact scope.

## Acknowledgments

This dataset was produced with support from the Ministry of Science and ICT (MSIT) and the
National IT Industry Promotion Agency (NIPA) of Korea under the
"2026 Open Source AI/SW Development and Utilization Support Program (Utilization Track)".
