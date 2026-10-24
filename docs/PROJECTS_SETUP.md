# Provisioning GitHub Projects — Bilgin Apps

The organization uses three **private** GitHub Projects V2 boards:

1. **Bilgin Exam TR** — four private Exam TR repositories and their engineering Issues.
2. **Bilgin ABC** — early literacy product, seeded with private draft planning items.
3. **Bilgin Apps Roadmap** — cross-product decisions, launch milestones and shared infrastructure.

See [PROJECT_MANAGEMENT.md](PROJECT_MANAGEMENT.md) for the operating model and exact fields.

## What is already prepared

- English Issue forms and contributor standards in this public .github configuration repository.
- 13 actionable Exam TR planning Issues across Backend, Admin, Mobile, and Web.
- 3 organization-level governance Issues for branch safety, project management, and environment separation.
- A repeatable Projects V2 bootstrap script at [scripts/bootstrap_projects.py](../scripts/bootstrap_projects.py).

**Important:** The GitHub connector that authored this configuration does not have the organization-level Projects write operations. The script below must be run from a trusted developer machine with your **own** approved GitHub authentication. Do not paste tokens into this repository or chat.

## 1. Prerequisites on your Mac

Install GitHub CLI if needed:

~~~bash
brew install gh
~~~

Authenticate with an organization member account authorized to create Projects:

~~~bash
gh auth login
gh auth refresh -s project -s repo
gh auth status
~~~

GitHub Projects V2 requires explicit Projects permissions; private repository Issues also require access to those repositories. If your organization enforces SSO or token restrictions, authorize the login as required by the organization.

## 2. Run the bootstrap

~~~bash
gh repo clone bilgin-apps/.github bilgin-apps-org
cd bilgin-apps-org
python3 scripts/bootstrap_projects.py
~~~

The script:

- Reuses a project when the **exact same title** already exists; otherwise creates it.
- Sets all three Project boards to **PRIVATE**.
- Writes consistent short descriptions and Project READMEs.
- Adds Status/Priority/Type/Area/Product/Release/Start Date/Target Date/Effort and a native two-week Sprint field where supported.
- Attempts to configure the six Status options and Board/Table/Roadmap views using the GitHub GraphQL API.
- Links Bilgin Exam TR to its four repositories and the Roadmap project to the organization configuration repository.
- Imports the 13 Exam TR Issues and 3 governance Issues.
- Creates 10 **private** Bilgin ABC draft items and 3 cross-product roadmap drafts.
- Skips items already present on reruns, rather than intentionally duplicating them.
- Prints the resulting project URLs and verifies field and item counts.

The script does **not** modify, merge, delete or deploy product code. It does not create Bilgin ABC repositories or silently assign release dates.

## 3. Verify in the GitHub UI

Visit [Bilgin Apps Projects](https://github.com/orgs/bilgin-apps/projects).

Check each project:

- [ ] All three projects exist, are **private**, and have the intended names.
- [ ] Board, Table and Roadmap views are visible.
- [ ] The Board view is **grouped by Status**, with Backlog, Todo, In Progress, In Review, Testing and Done.
- [ ] The Table view displays Priority, Type, Area, Sprint, Release, Assignees and Target Date as appropriate.
- [ ] The Roadmap view uses **Start Date** and **Target Date** fields; unscheduled items remain undated until approved.
- [ ] Bilgin Exam TR is linked to Backend, Admin, Mobile and Web and contains the seeded Issues.
- [ ] Bilgin ABC contains **draft items**, not issues attached to unrelated repositories.
- [ ] Bilgin Apps Roadmap contains only strategic/governance work and private draft milestones.
- [ ] Native Sprint field reflects a two-week cadence. If setup warned that it could not create the field, add an Iteration field in the GitHub UI.
- [ ] Item fields are assigned (especially Status and Priority).
- [ ] Collaborators have only the access they need.
- [ ] The **Workflows** tab is configured for new Issue auto-add, status transitions, and eventual archiving where appropriate.

> Some views may need final UI grouping, sorting and filtering depending on GitHub's API/view behavior. The script prints warnings rather than claiming success for any unsupported API operation. Do not ignore them.

## 4. Configure native workflows

For the Exam TR project, use **Project Settings → Workflows → Auto-add to project** and scope the workflow to the relevant Exam TR repositories. Do not automatically add sensitive issues to a public Project.

A reasonable starting policy:

- New issues → Backlog.
- A maintainer marks an issue Todo only when acceptance criteria and priority are agreed.
- Code review moves to In Review.
- QA moves to Testing.
- Acceptance moves to Done.
- Closed Issues can be auto-marked Done only if the team's Definition of Done is satisfied by that event.

For Bilgin ABC, do not add auto-add rules for repositories that do not yet exist.

## 5. Validate the import

Confirm the seeded source Issues exist:

- Backend: [#2](https://github.com/bilgin-apps/bilgin-exam-tr-backend/issues/2), [#3](https://github.com/bilgin-apps/bilgin-exam-tr-backend/issues/3), [#4](https://github.com/bilgin-apps/bilgin-exam-tr-backend/issues/4), [#5](https://github.com/bilgin-apps/bilgin-exam-tr-backend/issues/5)
- Admin: [#19](https://github.com/bilgin-apps/bilgin-exam-tr-admin/issues/19), [#20](https://github.com/bilgin-apps/bilgin-exam-tr-admin/issues/20), [#21](https://github.com/bilgin-apps/bilgin-exam-tr-admin/issues/21)
- Mobile: [#1](https://github.com/bilgin-apps/bilgin-exam-tr-mobile/issues/1), [#2](https://github.com/bilgin-apps/bilgin-exam-tr-mobile/issues/2), [#3](https://github.com/bilgin-apps/bilgin-exam-tr-mobile/issues/3), [#4](https://github.com/bilgin-apps/bilgin-exam-tr-mobile/issues/4)
- Web: [#9](https://github.com/bilgin-apps/bilgin-exam-tr-web/issues/9), [#10](https://github.com/bilgin-apps/bilgin-exam-tr-web/issues/10)
- Organization: [#1](https://github.com/bilgin-apps/.github/issues/1), [#2](https://github.com/bilgin-apps/.github/issues/2), [#3](https://github.com/bilgin-apps/.github/issues/3)

### CLI verification

~~~bash
gh project list --owner bilgin-apps
gh project field-list <PROJECT_NUMBER> --owner bilgin-apps
gh project item-list <PROJECT_NUMBER> --owner bilgin-apps --limit 100
gh project view <PROJECT_NUMBER> --owner bilgin-apps --web
~~~

Replace PROJECT_NUMBER with the number printed by the script. Keep all project and API tokens outside git; never upload secret screenshots, private Issue content or user records.

## Troubleshooting

**Permission denied / Projects authorization:** Confirm membership and Projects write access. Re-run gh auth refresh -s project -s repo and authorize SSO if applicable.

**GraphQL mutation unsupported:** GitHub CLI or your GitHub Enterprise API schema may not yet expose that mutation. Use the GitHub UI for the specific field or view; the script records a warning and keeps existing projects intact.

**Issue cannot be added:** Ensure your authenticated account has access to the private repository and that the issue URL resolves.

**Already linked repository:** GitHub may reject linking a project to an already-linked repo. Verify the link in the project and repository UI; no existing links are removed.

**Rerunning:** The script is additive and checks existing titles and items, but always review warnings. It does not reconcile renamed projects or independently modified field option names; those require human review.

## Security

This repository is public. Configuration documentation and setup code are public; do not include private backlog details or live credentials here. The actual product Projects should remain private.

For changes to release infrastructure and permissions, see [RELEASE_PROCESS.md](RELEASE_PROCESS.md) and [SECURITY.md](../SECURITY.md).
