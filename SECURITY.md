# Security Policy

SecLLM-Dataset is a dataset of **intentionally vulnerable source code** collected for research on
vulnerability detection, explanation, and repair. Please read the scope below before reporting.

## Scope

**In scope** — please report privately:

- Vulnerabilities in the tooling of this repository, such as `scripts/validate.py`
- Supply-chain issues in the GitHub Actions workflows under `.github/workflows/`
  (for example, script injection or excessive token permissions)
- Secrets (API keys, tokens, passwords, private keys) or personal data that were accidentally
  included in the dataset files

**Out of scope** — please do not report these as security vulnerabilities:

- Vulnerabilities inside the `entireCode` samples. They are the subject of the dataset and are
  included on purpose. If you believe a sample reveals an unfixed vulnerability in a live project,
  report it to that upstream project.
- Static-analysis false positives, wrong labels, or incorrect patches. Use the
  [data error issue form](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=data-error.yml).
- Requests to remove source code you hold rights to. Use the
  [removal request issue form](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=removal-request.yml).

## Reporting a Vulnerability

Report through GitHub Private Vulnerability Reporting:

**<https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/security/advisories/new>**

Do not open a public issue or pull request for an in-scope vulnerability.
GitHub documents the process in
[Privately reporting a security vulnerability](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability).

Please include:

- A description of the issue and its impact
- Steps to reproduce, or the affected file and line (for leaked secrets or personal data, the
  record's line number in the `.jsonl` file)
- The release or commit you looked at
- Any suggested mitigation, if known

## Response Targets

| Step | Target |
|---|---|
| Acknowledge the report | within 5 business days |
| Triage and share next steps | within 10 business days |

## Supported Versions

Only the latest release on the `main` branch is supported. Fixes are not backported to earlier
dataset versions.

## Disclosure Policy

We follow coordinated disclosure. We work with the reporter on a fix, ship it in a new release,
and then publish a GitHub Security Advisory crediting the reporter unless they prefer to remain
anonymous. Leaked secrets or personal data are removed from the dataset in the next release;
if the data must also be purged from Git history, we will say so in the advisory.
