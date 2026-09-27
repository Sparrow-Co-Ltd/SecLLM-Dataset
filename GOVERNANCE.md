# SecLLM-Dataset Governance

> Status: Draft pending approval / Version: 1.0 / Effective date: the approval date below / Next review date: 2027-03-28
>
> Approval:
> [TBD: approver and approval date]

## 1. Purpose and Scope

This document defines how decisions are made in SecLLM-Dataset, who holds which role, and what each
role is responsible for. It applies to this repository, its issues, pull requests and Discussions,
and to the official community channels listed in [COMMUNITY.md](COMMUNITY.md).

SecLLM-Dataset is a company-led open source project maintained by Sparrow Co., Ltd.

## 2. Principles

- **Openness.** Discussions and decisions happen in public channels, except for security, personal
  data, and personnel matters.
- **Respect.** Everyone follows the [Code of Conduct](CODE_OF_CONDUCT.md).
- **Technical merit.** Evidence, reproducible results, and the project's goals count for more than
  affiliation.
- **Accountability.** People who hold a role answer for their decisions and hand the role over when
  they become inactive.
- **Disclosure of interests.** People with a direct interest in a decision disclose it and, where
  needed, step aside.

## 3. Roles and Responsibilities

Current role holders and their repository permissions are listed in [MAINTAINERS.md](MAINTAINERS.md).

### Contributor

- Contributes through issues, pull requests, reviews, documentation, translations, community data,
  or user support, following [CONTRIBUTING.md](CONTRIBUTING.md).
- Needs no write access to the repository.

### Reviewer

- Reviews pull requests in an assigned area and asks for tests, fixes, or documentation.
- Does not merge or release alone.

### Maintainer

- Triages issues, reviews pull requests, re-verifies core data, and prepares releases.
- **Approving reviews is a Maintainer duty.** Maintainers review the areas assigned to them in
  [CODEOWNERS](.github/CODEOWNERS) and keep the decision records in [docs/decisions/](docs/decisions/).
- **Merging to `main` is done by the owner account `@Sparrow-Co-Ltd`.** The repository is owned by a
  personal account, not an organization, so collaborators hold the `write` role only and there is no
  Maintain role. The branch ruleset on `main` requires a pull request, one approval, and the
  `validate` check, and only the owner account can complete the merge.

### Project Lead

- Owns the project scope and external commitments, and is accountable for releases.
- Decides deadlocks under section 5 and records the rationale.
- Does not use emergency decisions as a standing power.

### Community Moderator

- Runs the community channels described in [COMMUNITY.md](COMMUNITY.md) and triages new questions.
- Applies the [Code of Conduct](CODE_OF_CONDUCT.md) enforcement ladder in the community channels and
  escalates cases to the Maintainers.
- Has no merge or release duties.

## 4. Decision Levels

| Level | Examples | Default process |
|---|---|---|
| Routine | Documentation fixes, validator bug fixes, community data that passes CI | Pull request, CODEOWNERS approval, passing checks |
| Significant | New languages or tracks, changes to the license allowlist, new dependencies or GitHub Actions, repository settings | Proposal issue, 3 business days of review |
| Major | Schema changes that break loaders, license changes, removal of core records, changes to this document | Written proposal, 7-day review, decision record |
| Emergency | Leaked secrets or personal data, a vulnerability in scripts or workflows, a credible rights claim | Immediate containment through a private channel, public record within 5 business days |

## 5. Consensus and Voting

1. Consensus means no unresolved serious objection remains and the proposer has addressed reasonable
   concerns. Consensus is always tried first.
2. Major decisions stay open for review for at least 7 days.
3. If consensus fails after the review period, active Maintainers vote and a simple majority decides.
   A vote needs a quorum of 2/3 of the active Maintainers.
4. A tie is decided by the Project Lead, who writes down the rationale in the decision record.
5. While the project has a single active Maintainer, Major decisions also need the Project Lead's
   written agreement.
6. Sparrow Co., Ltd. may veto a decision only on legal grounds, on security grounds, or on the
   release of core data (`data/java/`). A veto is recorded with its reason in a decision record.
7. The result, dissenting opinions, and follow-up actions are recorded.

## 6. Proposals and Decision Records

- Significant and Major proposals start as a GitHub issue or Discussion with the `governance` label.
- Major decisions are recorded in [docs/decisions/](docs/decisions/) using the
  [template](docs/decisions/0000-template.md). Decisions made before this document are recorded
  retroactively.
- Each decision links to the pull requests and releases that carry it out.

## 7. Granting Roles

- Reviewer candidates show sustained contributions and reliable reviews over the last 6 months.
- Maintainer candidates are nominated with the
  [maintainer nomination form](https://github.com/Sparrow-Co-Ltd/SecLLM-Dataset/issues/new?template=maintainer_nomination.yml),
  need endorsements from 2 people who hold the Maintainer or Project Lead role, and go through a
  7-day objection window.
- Documentation, reviews, user support, security, and community work count as contributions, not
  only data or code.
- The Project Lead or a Maintainer records the outcome and its rationale in the nomination issue and
  updates [MAINTAINERS.md](MAINTAINERS.md) by pull request.
- **A new Maintainer receives the `write` repository role.** Merges stay with the owner account
  `@Sparrow-Co-Ltd` unless the repository moves to an organization.

## 8. Inactivity, Resignation, and Removal

- A Reviewer or Maintainer with no activity for 6 months is contacted and may then be moved to
  Emeritus status; the owner account removes the repository role.
- Anyone may resign by opening an issue or telling a Maintainer; the role is moved to Emeritus.
- Access can be revoked temporarily to protect the project after a security incident, misuse of
  permissions, or a serious Code of Conduct violation.
- Final removal needs approval from 2/3 of the Maintainers, excluding anyone with a conflict of
  interest, and is recorded.

## 9. Conflicts of Interest

People taking part in a decision disclose employment, investment, contracts, or personal
relationships that bear on it. Anyone with a direct conflict abstains from the vote and the final
approval. When people employed by one company hold more than 2/3 of the Maintainer seats, the
project works on recruiting Maintainers from outside that company. Today all Maintainers are
Sparrow Co., Ltd. staff.

## 10. Disputes and Escalation

- **Technical disagreements:** Reviewer → Maintainer → Project Lead.
- **Code of Conduct incidents:** the private reporting path in
  [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md#how-to-report).
- **Security issues:** the private reporting path in [SECURITY.md](SECURITY.md).
- **Stalled pull requests:** a pull request with no review for 14 days may be raised with the
  Project Lead.
- Nobody decides alone on a report about themselves.

## 11. Meetings and Transparency

- The project has no standing meeting. Decisions are made in issues, pull requests, and
  Discussions.
- The Maintainers review the project metrics once a month; the minutes are added to the repository
  by pull request.
- Decisions are public except for security, personal data, and personnel matters.

## 12. Releases

1. Changes to core data (`data/java/`) are re-verified by the team with Sparrow SAST before release.
2. Every release gets an entry in [CHANGELOG.md](CHANGELOG.md) and a version number:
   - **MAJOR**: schema changes that break existing loaders
   - **MINOR**: records added or removed
   - **PATCH**: corrections to existing records or documentation
3. The `version` and `date-released` fields in [CITATION.cff](CITATION.cff) are updated to match.

Tags and merges to `main` are performed by the owner account `@Sparrow-Co-Ltd` after maintainer
approval.

## 13. Amendments and Periodic Review

- Changes to this document are Major decisions: a pull request with the `governance` label, at least
  7 days of comment, and approval by 2 people who hold the Maintainer or Project Lead role.
- Every 6 months, the Maintainers check that the roles, repository permissions, rulesets, and
  CODEOWNERS match this document, and record the result.
- When the project has 3 active Maintainers from outside Sparrow Co., Ltd., it considers moving to
  a steering committee or delegated governance.

## 14. Contact

- General questions: see [COMMUNITY.md](COMMUNITY.md).
- Governance questions: open an issue or Discussion with the `governance` label.
- Security reports: see [SECURITY.md](SECURITY.md).
- Code of Conduct reports: see [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md#how-to-report).
