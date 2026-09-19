# Community data track

This directory holds vulnerability records produced with **third-party tools** (for example Semgrep or CodeQL)
and contributed by the community. Core data in `data/java/` is produced by Sparrow SAST and re-verified by the maintainers;
community data is not.

> **Verification tier.** Community records are attested by their contributors. CI checks the schema and
> provenance only. The maintainers do not re-run the contributor's tool, so detection and patch correctness are
> the contributor's claim. Filter on the directory if you need only core data.

How to submit: see [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Layout

```
data/community/<lang>/<tool>-<yyyymmdd>.jsonl
```

Example: `data/community/java/semgrep-20261001.jsonl`. One line is one record.

Supported `<lang>` directories and the values their records must use:

| Directory | `fileExtension` | `programmingLanguage` |
| --- | --- | --- |
| `java` | `.java` | `Java` |

Adding a language requires a maintainer change to `scripts/validate.py` and this table.

## Record format

Community records use the same `input` and `output` schema as core records (see the [README](../../README.md#schema)),
plus a required top-level `meta` object. The envelope therefore has **three keys**: `{input, output, meta}`.
Core records keep exactly `{input, output}`.

Relaxations compared with core records:

- `contexts` may be `[]` when the tool reports no data-flow trace.
- `issueNameKo`, `issueDescriptionKo`, `dangerousExampleEn`, `dangerousExampleKo`, `safeExampleEn`, and `safeExampleKo` may be `""`.

All other rules are the same: every field present, `issueRisk` from the five allowed values, line numbers within
`entireCode`, and valid `delete`/`add` operations. Map the tool's severity to `issueRisk` as described in
[CONTRIBUTING.md](../../CONTRIBUTING.md).

### `meta` fields

| Field | Type | Rule |
| --- | --- | --- |
| `tool` | string | Tool name, e.g. `semgrep` |
| `toolVersion` | string | Tool version used for detection and re-analysis |
| `ruleId` | string | Rule or query identifier that reported the finding |
| `sourceRepo` | string | `https://` URL of the upstream repository |
| `sourceCommit` | string | Upstream commit, 7 to 40 hexadecimal characters |
| `sourcePath` | string | File path within the upstream repository |
| `sourceLicense` | string | SPDX identifier of the upstream file's license. Must be one of: `MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `ISC`, `0BSD`, `Unlicense`, `CC0-1.0`, `Zlib`, `BSL-1.0` |
| `patchVerified` | boolean | Must be `true`: the contributor re-ran the same tool and version on the patched file and the finding is gone |

To propose another license for the allowlist, open a
[community data issue](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=community-data.yml).

### Example

Shown pretty-printed; in the file each record is a single line.

```json
{
  "input": {
    "fileExtension": ".java",
    "programmingLanguage": "Java",
    "issueRisk": "높음",
    "issueNameEn": "Weak hash algorithm (MD5)",
    "issueNameKo": "",
    "issueDescriptionEn": "MD5 is a broken hash algorithm and must not be used for security purposes.",
    "issueDescriptionKo": "",
    "issueLineNumber": 5,
    "entireCode": "import java.security.MessageDigest;\n\npublic class Hasher {\n  byte[] hash(byte[] data) throws Exception {\n    MessageDigest md = MessageDigest.getInstance(\"MD5\");\n    return md.digest(data);\n  }\n}\n",
    "dangerousExampleEn": "",
    "dangerousExampleKo": "",
    "safeExampleEn": "",
    "safeExampleKo": "",
    "contexts": []
  },
  "output": [
    { "type": "delete", "startLine": 5, "endLine": 5, "content": null },
    { "type": "add", "startLine": 5, "endLine": null, "content": "    MessageDigest md = MessageDigest.getInstance(\"SHA-256\");" }
  ],
  "meta": {
    "tool": "semgrep",
    "toolVersion": "1.90.0",
    "ruleId": "java.lang.security.audit.crypto.use-of-md5.use-of-md5",
    "sourceRepo": "https://github.com/example-org/example-project",
    "sourceCommit": "0123456789abcdef0123456789abcdef01234567",
    "sourcePath": "src/main/java/Hasher.java",
    "sourceLicense": "MIT",
    "patchVerified": true
  }
}
```

Run `python scripts/validate.py` before opening a pull request.
