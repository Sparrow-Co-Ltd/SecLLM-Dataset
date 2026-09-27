# Community Channel Matrix

Each inquiry has exactly one source of record (the primary channel). Other channels keep only a
link to it and a short context; do not copy the original text. Business days are Monday to Friday, KST.

| Inquiry | Primary channel | Secondary channel | Switch condition | Target response |
|---|---|---|---|---|
| Data error (wrong label, false positive, wrong trace, bad patch) | [Data error form](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=data-error.yml) | HF dataset Community tab, Discord | The file and record line are known: open the form and link the thread | First triage in 2 business days; fix ships in the next release |
| Model behavior on a specific revision | HF model Community tab | Discussions Q&A | The cause is a data record: open a data error issue | 3 business days |
| Removal of code or personal data | [Removal request form](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=removal-request.yml) or the private contact in [CODE_OF_CONDUCT.md](../../CODE_OF_CONDUCT.md#how-to-report) | None | Personal data or rights issues move to the private contact; never discuss them in public | Triaged on receipt |
| Idea or feature | [Discussions Ideas](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/discussions/categories/ideas) | Discord | Scope and owner are agreed: open a community-to-issue issue | Triaged weekly |
| Governance or long-term decision | GitHub Discussion, then a decision record under `docs/decisions/` | Meetings, Discord | A proposal is ready: follow [GOVERNANCE.md](../../GOVERNANCE.md) | The review period in GOVERNANCE.md |
| Usage question | [Discussions Q&A](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/discussions/categories/q-a) | Discord, HF Community tabs | The same question comes up 3 times: add it to the docs or card by pull request | 2 business days |
| Security vulnerability | Private Vulnerability Reporting ([SECURITY.md](../../SECURITY.md)) | None | Never public | Triaged on receipt; acknowledged per SECURITY.md |
