# Moderator Runbook

For the moderators listed in [MAINTAINERS.md](../../MAINTAINERS.md). Policy:
[CHANNEL_POLICY.md](CHANNEL_POLICY.md). Conduct rules: [CODE_OF_CONDUCT.md](../../CODE_OF_CONDUCT.md).

## On-call

The on-call moderator runs the weekly triage (label `triage`), checks the Hugging Face Community tabs
for items unanswered for 7 days, and handles reports.

[TBD: on-call rota]

## Intake

1. Check the reporter's safety and the urgency first.
2. Preserve the evidence (URL, time, channel, screenshots) in the restricted incident record.
3. A moderator with a conflict of interest steps aside.
4. Public replies never reveal personal data or details of the investigation.

## Severity and default action

| Level | Examples | Default action |
|---|---|---|
| S1 | A mistake, a mildly unproductive remark | Private notice, ask for a correction |
| S2 | Repeated spam, aggressive language | Formal warning, temporary restriction |
| S3 | Harassment, hate, deliberate disruption | Immediate restriction, review by the moderators |
| S4 | Doxxing, physical threats, leaked credentials | Emergency ban, report to the platform, escalate to security ([SECURITY.md](../../SECURITY.md)) or legal |

## Incident record

- Incident ID, time received, handling moderator
- Policy section applied; facts confirmed, with URLs
- Action taken, scope, and expiry; notice to the people involved
- Appeal and review outcome
- Steps to prevent a repeat

## Record handling

- Keep incident records outside this repository and apart from general moderation channels.
- Give access only to the moderators and maintainers who handle the case (least privilege).
- Delete records when they are no longer needed for appeals or repeat cases.
