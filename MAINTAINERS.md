# Maintainers

Roles are defined in [GOVERNANCE.md](GOVERNANCE.md#3-roles-and-responsibilities). Changes to this
file follow [Granting Roles](GOVERNANCE.md#7-granting-roles) and
[Inactivity, Resignation, and Removal](GOVERNANCE.md#8-inactivity-resignation-and-removal), and
link the related issue or pull request.

| Name | GitHub | Role | Repo permission | Areas | Appointed | Status |
|---|---|---|---|---|---|---|
| MuSun Choi | [@moosunny](https://github.com/moosunny) | Maintainer | `write` | Dataset content, SAST re-verification, validator, releases | 2026-09-21 | Active |
| Sparrow Co., Ltd. (company owner account, not counted as a person) | [@Sparrow-Co-Ltd](https://github.com/Sparrow-Co-Ltd) | Repository owner | `admin` (repo owner) | Merges to `main`, tags, repository settings | 2026-09-21 | Active |
| [TBD: second maintainer name and GitHub ID] | | Maintainer | `write` | | | Open |
| [TBD: Project Lead] | | Project Lead | | Scope, releases, deadlocks | | Open |
| [TBD: Community Moderator] | | Community Moderator | | Community channels | | Open |

The repository is owned by a personal account, so a Maintainer holds the `write` role and approves
pull requests, and the owner account `@Sparrow-Co-Ltd` performs the merge. Maintainers are also the
community leaders who enforce the [Code of Conduct](CODE_OF_CONDUCT.md). To report a conduct
concern, follow [How to report](CODE_OF_CONDUCT.md#how-to-report).

## Status

- **Active:** currently holds the role.
- **Emeritus:** former role holder with no approval rights.
- **On leave:** absent for a set period.
- **Open:** role not yet filled.

## Responsibilities (RACI)

R = responsible, A = accountable, C = consulted, I = informed.

| Activity | Project Lead | Maintainer | Community Moderator | Owner account `@Sparrow-Co-Ltd` |
|---|---|---|---|---|
| Release (CHANGELOG, CITATION, tag) | A | R | I | R (tag) |
| Merge to `main` | A | C (approving review) | I | R |
| Core data re-verification with Sparrow SAST | I | R, A | I | – |
| Security triage ([SECURITY.md](SECURITY.md)) | A | R | I | C |
| Code of Conduct enforcement | A | R | R | I |
| Community triage ([COMMUNITY.md](COMMUNITY.md)) | I | A | R | – |
| Governance change ([GOVERNANCE.md](GOVERNANCE.md)) | A | R | C | C |
| Hugging Face sync | A | R | I | C |
