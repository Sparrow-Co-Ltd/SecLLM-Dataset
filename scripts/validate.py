#!/usr/bin/env python3
"""Validate SecLLM-Dataset JSONL files (Python 3.9+, standard library only).

Usage:
  python scripts/validate.py [FILE ...]   validate files (default: every data/**/*.jsonl)
  python scripts/validate.py --stats FILE print dataset statistics
  python scripts/validate.py --self-test  check that the validator rejects broken records

Tiers are derived from the path:
  data/<lang>/*.jsonl            core records      {input, output}
  data/community/<lang>/*.jsonl  community records {input, output, meta}
"""
import argparse
import copy
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# Language directory -> (fileExtension, programmingLanguage). Add one line per new language.
LANGS = {
    "java": (".java", "Java"),
    "javascript": (".js", "JavaScript"),
    "typescript": (".ts", "TypeScript"),
    "go": (".go", "Go"),
    "python": (".py", "Python"),
    "c": (".c", "C"),
    "cpp": (".cpp", "C++"),
}
RISKS = {"매우 높음", "높음", "보통", "낮음", "매우 낮음"}
EVENTS = {"source", "branch", "sink"}
LICENSES = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "0BSD",
            "Unlicense", "CC0-1.0", "Zlib", "BSL-1.0"}

INPUT_FIELDS = {"fileExtension", "programmingLanguage", "issueRisk", "issueNameEn", "issueNameKo",
                "issueDescriptionEn", "issueDescriptionKo", "issueLineNumber", "entireCode",
                "dangerousExampleEn", "dangerousExampleKo", "safeExampleEn", "safeExampleKo", "contexts"}
TEXT_FIELDS = ["issueNameEn", "issueNameKo", "issueDescriptionEn", "issueDescriptionKo",
               "dangerousExampleEn", "dangerousExampleKo", "safeExampleEn", "safeExampleKo"]
# Community contributors may leave these empty; everything else must be non-empty.
COMMUNITY_OPTIONAL = {"issueNameKo", "issueDescriptionKo", "dangerousExampleEn",
                      "dangerousExampleKo", "safeExampleEn", "safeExampleKo"}
CONTEXT_FIELDS = {"lineNo", "eventType", "messageKey", "message", "params"}
OUTPUT_FIELDS = {"type", "startLine", "endLine", "content"}
META_FIELDS = {"tool", "toolVersion", "ruleId", "sourceRepo", "sourceCommit", "sourcePath",
               "sourceLicense", "patchVerified"}


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def keys_error(obj, expected, where):
    if not isinstance(obj, dict):
        return [f"{where}: expected object"]
    missing, extra = expected - obj.keys(), obj.keys() - expected
    errs = [f"{where}: missing field {k!r}" for k in sorted(missing)]
    return errs + [f"{where}: unexpected field {k!r}" for k in sorted(extra)]


def check_record(rec, community, lang):
    """Return a list of error strings for one record (empty list = valid)."""
    envelope = {"input", "output", "meta"} if community else {"input", "output"}
    errs = keys_error(rec, envelope, "record")
    if errs:
        return errs
    inp = rec["input"]
    errs = keys_error(inp, INPUT_FIELDS, "input")
    if errs:
        return errs

    ext, language = LANGS[lang]
    if (inp["fileExtension"], inp["programmingLanguage"]) != (ext, language):
        errs.append(f"input: fileExtension/programmingLanguage must be {ext!r}/{language!r} in {lang}/")
    if inp["issueRisk"] not in RISKS:
        errs.append(f"input.issueRisk: {inp['issueRisk']!r} not in {sorted(RISKS)}")
    for k in TEXT_FIELDS:
        v = inp[k]
        if not isinstance(v, str):
            errs.append(f"input.{k}: expected string")
        elif not v and not (community and k in COMMUNITY_OPTIONAL):
            errs.append(f"input.{k}: must not be empty")
    code = inp["entireCode"]
    if not isinstance(code, str) or not code:
        return errs + ["input.entireCode: expected non-empty string"]
    n = len(code.split("\n"))
    if not is_int(inp["issueLineNumber"]) or not 1 <= inp["issueLineNumber"] <= n:
        errs.append(f"input.issueLineNumber: expected int in 1..{n}")

    ctxs = inp["contexts"]
    if not isinstance(ctxs, list) or (not ctxs and not community):
        errs.append("input.contexts: expected list" if community else "input.contexts: expected non-empty list")
        ctxs = []
    for i, c in enumerate(ctxs):
        where = f"input.contexts[{i}]"
        ke = keys_error(c, CONTEXT_FIELDS, where)
        if ke:
            errs += ke
            continue
        if not is_int(c["lineNo"]) or not 1 <= c["lineNo"] <= n:
            errs.append(f"{where}.lineNo: expected int in 1..{n}")
        if c["eventType"] not in EVENTS:
            errs.append(f"{where}.eventType: {c['eventType']!r} not in {sorted(EVENTS)}")
        if not isinstance(c["messageKey"], str) or not isinstance(c["message"], str):
            errs.append(f"{where}: messageKey/message must be strings")
        if not isinstance(c["params"], dict):
            errs.append(f"{where}.params: expected object")

    out = rec["output"]
    if not isinstance(out, list) or not out:
        errs.append("output: expected non-empty list")
        out = []
    for i, o in enumerate(out):
        where = f"output[{i}]"
        ke = keys_error(o, OUTPUT_FIELDS, where)
        if ke:
            errs += ke
            continue
        start, end = o["startLine"], o["endLine"]
        if o["type"] == "delete":
            if not (is_int(start) and is_int(end) and 1 <= start <= end <= n):
                errs.append(f"{where}: delete needs int startLine <= endLine within 1..{n}")
            if o["content"] is not None:
                errs.append(f"{where}: delete must have content null")
        elif o["type"] == "add":
            if not is_int(start) or not 1 <= start <= n + 1:
                errs.append(f"{where}: add needs int startLine in 1..{n + 1}")
            if end is not None:
                errs.append(f"{where}: add must have endLine null")
            if not isinstance(o["content"], str) or not o["content"]:
                errs.append(f"{where}: add needs non-empty string content")
        else:
            errs.append(f"{where}.type: {o['type']!r} not in ['add', 'delete']")

    if community:
        meta = rec["meta"]
        ke = keys_error(meta, META_FIELDS, "meta")
        if ke:
            return errs + ke
        for k in ("tool", "toolVersion", "ruleId", "sourcePath"):
            if not isinstance(meta[k], str) or not meta[k]:
                errs.append(f"meta.{k}: expected non-empty string")
        if not isinstance(meta["sourceRepo"], str) or not re.fullmatch(
                r"https://[A-Za-z0-9.-]+\.[A-Za-z]{2,}(/[A-Za-z0-9._~/-]*)?", meta["sourceRepo"]):
            errs.append("meta.sourceRepo: expected https:// URL")
        if not isinstance(meta["sourceCommit"], str) or not re.fullmatch(r"[0-9a-f]{7,40}", meta["sourceCommit"]):
            errs.append("meta.sourceCommit: expected 7-40 lowercase hex chars")
        if meta["sourceLicense"] not in LICENSES:
            errs.append(f"meta.sourceLicense: {meta['sourceLicense']!r} not in allowlist {sorted(LICENSES)}")
        if meta["patchVerified"] is not True:
            errs.append("meta.patchVerified: must be true")
    return errs


def tier_of(path):
    """Return (community, lang) for a data file path, or raise ValueError."""
    try:
        parts = path.resolve().relative_to(DATA).parts
    except ValueError:
        raise ValueError("file must be under data/")
    community = parts[0] == "community"
    if community:
        parts = parts[1:]
    if len(parts) != 2:
        raise ValueError("expected data/<lang>/FILE.jsonl or data/community/<lang>/FILE.jsonl")
    if parts[0] not in LANGS:
        raise ValueError(f"unknown language directory {parts[0]!r}; add it to LANGS in scripts/validate.py")
    return community, parts[0]


def validate_file(path):
    try:
        community, lang = tier_of(path)
    except ValueError as e:
        return 0, [f"{path}: {e}"]
    count, errs = 0, []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            count += 1
            try:
                rec = json.loads(line)
            except json.JSONDecodeError as e:
                errs.append(f"{path}:{lineno}: invalid JSON ({e.msg})")
                continue
            errs += [f"{path}:{lineno}: {m}" for m in check_record(rec, community, lang)]
    if count == 0:
        errs.append(f"{path}: file contains no records")
    return count, errs


def print_stats(path):
    risks, ops, names, lines = Counter(), Counter(), set(), []
    with open(path, encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            inp = rec["input"]
            names.add(inp["issueNameEn"])
            risks[inp["issueRisk"]] += 1
            lines.append(len(inp["entireCode"].split("\n")))
            ops.update(o["type"] for o in rec["output"])
    print(f"records: {len(lines)}")
    print(f"unique issue types (issueNameEn): {len(names)}")
    print(f"code lines min/median/max: {min(lines)} / {statistics.median(lines):g} / {max(lines)}")
    print("issueRisk: " + ", ".join(f"{k} {v}" for k, v in risks.most_common()))
    print("output ops: " + ", ".join(f"{k} {v}" for k, v in ops.most_common()))


def self_test():
    code = "class A {\n  void f() {\n    new Thread().start();\n  }\n}\n"
    core = {
        "input": {
            "fileExtension": ".java", "programmingLanguage": "Java", "issueRisk": "높음",
            "issueNameEn": "Direct Use of Threads", "issueNameKo": "스레드의 직접 사용",
            "issueDescriptionEn": "desc", "issueDescriptionKo": "설명", "issueLineNumber": 3,
            "entireCode": code, "dangerousExampleEn": "1. bad", "dangerousExampleKo": "1. bad",
            "safeExampleEn": "1. good", "safeExampleKo": "1. good",
            "contexts": [{"lineNo": 3, "eventType": "sink", "messageKey": "k", "message": "m", "params": {}}],
        },
        "output": [{"type": "delete", "startLine": 3, "endLine": 3, "content": None},
                   {"type": "add", "startLine": 3, "endLine": None, "content": "    run();"}],
    }
    comm = copy.deepcopy(core)
    comm["input"].update(issueNameKo="", issueDescriptionKo="", safeExampleKo="", contexts=[])
    comm["meta"] = {"tool": "semgrep", "toolVersion": "1.0.0", "ruleId": "java.thread",
                    "sourceRepo": "https://github.com/example/repo", "sourceCommit": "0123abc",
                    "sourcePath": "src/A.java", "sourceLicense": "MIT", "patchVerified": True}

    def set_(path, value):
        def f(r):
            *keys, last = path
            for k in keys:
                r = r[k]
            r[last] = value
        return f

    def del_(path):
        def f(r):
            *keys, last = path
            for k in keys:
                r = r[k]
            del r[last]
        return f

    cases = [  # (name, community, mutation) -- every one must be rejected
        ("missing field", False, del_(["input", "issueRisk"])),
        ("extra field", False, set_(["input", "extra"], 1)),
        ("bad issueRisk", False, set_(["input", "issueRisk"], "high")),
        ("bad eventType", False, set_(["input", "contexts", 0, "eventType"], "sanitizer")),
        ("issueLineNumber out of range", False, set_(["input", "issueLineNumber"], 99)),
        ("issueLineNumber bool", False, set_(["input", "issueLineNumber"], True)),
        ("context lineNo out of range", False, set_(["input", "contexts", 0, "lineNo"], 0)),
        ("delete with content", False, set_(["output", 0, "content"], "x")),
        ("delete endLine < startLine", False, set_(["output", 0, "endLine"], 2)),
        ("add with endLine", False, set_(["output", 1, "endLine"], 3)),
        ("add empty content", False, set_(["output", 1, "content"], "")),
        ("empty entireCode", False, set_(["input", "entireCode"], "")),
        ("community contexts not a list", True, set_(["input", "contexts"], None)),
        ("unknown op type", False, set_(["output", 1, "type"], "replace")),
        ("empty output", False, set_(["output"], [])),
        ("core empty contexts", False, set_(["input", "contexts"], [])),
        ("core empty issueNameKo", False, set_(["input", "issueNameKo"], "")),
        ("core with meta", False, set_(["meta"], {})),
        ("language mismatch", False, set_(["input", "programmingLanguage"], "Kotlin")),
        ("community missing meta", True, del_(["meta"])),
        ("community empty issueNameEn", True, set_(["input", "issueNameEn"], "")),
        ("community non-permissive license", True, set_(["meta", "sourceLicense"], "GPL-3.0-only")),
        ("community patchVerified false", True, set_(["meta", "patchVerified"], False)),
        ("community bad sourceCommit", True, set_(["meta", "sourceCommit"], "xyz")),
        ("community http sourceRepo", True, set_(["meta", "sourceRepo"], "http://example.com/r")),
        ("community non-URL sourceRepo", True, set_(["meta", "sourceRepo"], "https://<script>")),
        ("community extension mismatch", True, set_(["input", "fileExtension"], ".py")),
    ]
    failures = []
    for name, community, rec in (("valid core", False, core), ("valid community", True, comm)):
        errs = check_record(rec, community, "java")
        if errs:
            failures.append(f"{name} rejected: {errs}")
    for name, community, mutate in cases:
        rec = copy.deepcopy(comm if community else core)
        mutate(rec)
        if not check_record(rec, community, "java"):
            failures.append(f"not rejected: {name}")
    for bad in ("community/cobol/x.jsonl", "x.jsonl", "java/sub/x.jsonl"):
        try:
            tier_of(DATA / bad)
            failures.append(f"path not rejected: data/{bad}")
        except ValueError:
            pass
    if tier_of(DATA / "community/java/x.jsonl") != (True, "java") or tier_of(DATA / "java/x.jsonl") != (False, "java"):
        failures.append("valid paths misclassified")
    if failures:
        print("self-test FAILED:\n  " + "\n  ".join(failures))
        return 1
    print(f"self-test OK: 2 valid records accepted, {len(cases)} broken records and 3 bad paths rejected")
    return 0


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--stats", type=Path, metavar="FILE")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if args.stats:
        print_stats(args.stats)
        return 0
    files = args.files or sorted(DATA.glob("**/*.jsonl"))
    if not files:
        print("no .jsonl files found under data/")
        return 1
    failed = False
    for path in files:
        count, errs = validate_file(path)
        for e in errs:
            print(e)
        print(f"{path}: {count} records, {len(errs)} errors")
        failed |= bool(errs)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
