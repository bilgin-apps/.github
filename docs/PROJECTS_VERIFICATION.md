# Projects verification record — 25 October 2026

The three Projects V2 boards are live and private:

| Project | URL | Current source policy |
| --- | --- | --- |
| Bilgin Exam TR | https://github.com/orgs/bilgin-apps/projects/1 | Relevant open Admin/Web issues; Backend/Mobile issues excluded |
| Bilgin ABC | https://github.com/orgs/bilgin-apps/projects/2 | No repository intake; do not restore removed draft plans |
| Bilgin Apps Roadmap | https://github.com/orgs/bilgin-apps/projects/3 | Organization governance issues in `.github` |

## Views and fields

All three have Board, Table and Roadmap views, the six documented Status options, P0–P3 priorities and the agreed custom fields. `Work Type` replaces the reserved API field name `Type`.

Board columns use Status and all views sort Priority ascending. Roadmap views were explicitly mapped to **Start Date** and **Target Date**, saved as shared view defaults, then reloaded and checked in the browser. No item dates, release commitments or sprint assignments were fabricated. Sprint cadence is 14 days, starting on Monday, with iterations awaiting capacity planning.

## Native automation configuration

| Project | New item rule | Auto-add rule |
| --- | --- | --- |
| Bilgin Exam TR | Issue/PR added → Status Backlog | Repository `bilgin-exam-tr-admin`; `is:issue is:open` |
| Bilgin ABC | Issue/PR added → Status Backlog | Disabled; no dedicated product repository exists |
| Bilgin Apps Roadmap | Issue/PR added → Status Backlog | Repository `.github`; `is:issue is:open` |

The native new-item workflow exposes issue and pull-request types; draft items must be explicitly assigned Backlog during approved planning. No drafts were created as part of verification.

The current plan allows one native auto-add workflow per project. Web intake remains manual rather than purchasing an upgrade or introducing an unreviewed token-backed repository workflow. Source repository links do not authorize issue intake.

Automatic sub-issue intake, automatic issue closure and automatic completion transitions remain disabled. Auto-add filters exclude closed issues and pull requests, and no intake rule targets a protected repository. Saved workflow screens were read back to confirm enabled state, repository and filter. No test issues were created to exercise these rules.

## Access review

The existing base role is Write for organization members; organization owners are project administrators. No additional direct project collaborators are listed. This review made no changes to membership, grants, base roles or visibility.

## Source and release governance

The bootstrap fix and documentation are proposed in draft PR https://github.com/bilgin-apps/.github/pull/4. Local tests and the GitHub Actions check must pass on the PR's current commit before review. The PR is not merged automatically.

See [RELEASE_SAFETY_PLAN.md](RELEASE_SAFETY_PLAN.md) for the entitlement check, exact-check inventory, branch-rule pilot, environment separation and approval gates. Preparing that plan does not authorize production deployment, access changes or a paid subscription.

## Verification boundaries

Initial project provisioning was verified with the GitHub CLI and GraphQL API. The additional native workflow targets/filters and Roadmap date mapping were verified in the browser after saving; these settings are not all exposed by the public API. Record any fresh API readback separately rather than treating earlier snapshots as proof of later changes.

An enabled and saved workflow is a verified configuration, not evidence that an untested future event has already executed successfully. Existing issue states and protected-repository issue metadata were checked independently without creating or reopening work.
