# Discord Launch Plan

Discord is optional and chat-only (see [CHANNEL_POLICY.md](CHANNEL_POLICY.md)). The server does not
exist yet. This plan says how to open it safely.

## Channels

| Channel | Covers | Does not cover |
|---|---|---|
| `#rules` | Code of Conduct, channel policy, reporting link (read-only) | Discussion |
| `#announcements` | Releases and notices, mirrored from GitHub Discussions Announcements (read-only) | Replies |
| `#introductions` | Say hello | Support questions |
| `#general` | Casual project talk | Bug reports, decisions |
| `#help` | Usage questions, one thread per question | Data errors, vulnerabilities, personal data |
| `#contributors` | Coordination on open issues and pull requests | Decisions (these go to GitHub) |
| `#showcase` | Projects built with the dataset | Promotion unrelated to the project |
| `#events` | Office hours and meetups (proposals use the community event form on GitHub) | Other events |
| `#moderators` | Moderator coordination (private) | Incident records (kept outside Discord) |

When a `#help` thread is resolved, summarize it in three sentences in a GitHub Discussion or issue and
link both ways.

## Roles and security

- **Admin:** the company account and one named backup. Can change server settings.
- **Moderator:** the moderators listed in [MAINTAINERS.md](../../MAINTAINERS.md). Can time out, ban, and manage messages.
- **Contributor:** people with a merged pull request. No extra permissions.
- **Member:** everyone else.
- Require two-factor authentication for moderation actions (server setting), and MFA on every Admin and Moderator account.
- Bots get only the permissions they need; no bot has Administrator, ban, or role-management rights.
- Post the invite link only in [COMMUNITY.md](../../COMMUNITY.md#discord) (the README links there).

## Drills

Before launch, the moderators run four drills and record the result:

1. A question posted in the wrong channel
2. A token or credential posted in a message
3. A spam wave
4. A threat reported on a weekend

## 30-day plan

| Week | Work |
|---|---|
| 1 | No server yet. Name the Admin, backup Admin, and two moderators in MAINTAINERS.md; confirm the channel map above. |
| 2 | Create the server privately. Set roles, MFA, and `#rules`. Run the four drills. |
| 3 | Prepare 10 FAQ entries and 3–5 good first issues. |
| 4 | Soft launch to a small group, then publish the invite in COMMUNITY.md. |

## Launch-hold conditions

Do not publish the invite while any of these is true:

- The private reporting contact does not actually receive reports.
- The Admin account cannot be recovered (no backup Admin, no recovery codes stored).
- There is no second moderator to cover absence.
- There is no on-call rota in [MODERATOR_RUNBOOK.md](MODERATOR_RUNBOOK.md#on-call).

## Channel review

- A channel with no conversation for 30 days is merged into another.
- The full channel list is reviewed every 60 days.
