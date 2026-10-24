# Hugging Face Community Rules

Rules for the Community tabs of the SecLLM Hugging Face repositories listed in
[COMMUNITY.md](../../COMMUNITY.md#hugging-face).

## Scope

- **Dataset repository:** loading, schema, samples, license, and card questions about a specific revision.
- **Model repository:** loading, inference, evaluation, and card questions about a specific revision.

Everything else has another home:

- Data errors and all decisions: GitHub ([data error form](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=data-error.yml), [GOVERNANCE.md](../../GOVERNANCE.md)).
- General ML questions: a general forum such as the Hugging Face Forum.
- Vulnerabilities: [SECURITY.md](../../SECURITY.md). Personal data, removal, and rights issues: the [removal request form](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=removal-request.yml) or the private contact in [CODE_OF_CONDUCT.md](../../CODE_OF_CONDUCT.md#how-to-report). Never post these in a public Discussion.

## What to include in a question

- Repository ID, repo type (dataset or model), and the exact commit or revision
- Library, runtime, and hardware versions
- Expected and actual result
- A minimal, shareable reproduction and the error message
- The card limitation you checked, if any

## Closing a thread

- Leave the resolving revision, document, or GitHub issue URL, and the reason for closing.
- Close out-of-scope questions explicitly, with a pointer to the right channel.
- Deleting a pull request ref cannot be undone; confirm nothing needs to be kept first.

## Repeat questions

When the same question comes up **3 times**, do not keep pasting the answer. Fix the card (intended
use, limitations, loading instructions) with a pull request on GitHub, then link it from the thread.

## Weekly check

Once a week the on-call moderator ([MODERATOR_RUNBOOK.md](MODERATOR_RUNBOOK.md#on-call)) lists open
discussions in both repositories (web UI or Hub API) and answers or routes any item unanswered for
7 days. Bots get no permission to hide, close, or merge.

## Revision sync table

Every release notice and both cards carry this table, one row per release:

| Release | GitHub commit | HF dataset revision | HF model revision | Known issues | Support channels |
|---|---|---|---|---|---|
| `x.y.z` | 40-character SHA | Hub commit | Hub commit | Link or "none" | [COMMUNITY.md](../../COMMUNITY.md) |
