# GitHub Projects — Bilgin Apps

This document defines the shared operating model for Bilgin Apps' **private GitHub Projects V2** boards. It complements the [Development Standards](DEVELOPMENT_STANDARDS.md), [Release Process](RELEASE_PROCESS.md), and the repository-level Issue forms.

> **Important:** This is the intended configuration. Committing this document does not itself create GitHub Projects, enable workflows, invite members, or deploy software. Use [PROJECTS_SETUP.md](PROJECTS_SETUP.md) to provision and verify the actual boards.

## The three boards

| Project | Ownership | Scope | Source of work |
| --- | --- | --- | --- |
| **Bilgin Exam TR** | Exam product maintainers | Backend, Admin, Mobile, Web, educational content, beta and release readiness | Issues in four private Exam TR repositories |
| **Bilgin ABC** | ABC product maintainers | Turkish early literacy, characters, curriculum, pedagogy, mobile development and parent experience | Private Project drafts until dedicated ABC repositories exist |
| **Bilgin Apps Roadmap** | Organization and product owners | Milestones, product strategy, shared architecture, security, operational readiness, launch dependencies | Roadmap-level issues and project drafts; link to implementation issues without duplicating them |

All three boards should have **private visibility**. Private issue contents should never be copied into public organization profile documentation.

## Shared lifecycle

| Status | Meaning | Entry criteria | Exit criteria |
| --- | --- | --- | --- |
| **Backlog** | Candidate work not committed to a sprint | Problem or opportunity recorded | Scope and relative priority assessed |
| **Todo** | Defined and ready for implementation | Clear owner, acceptance criteria, dependencies, and verification plan | Work begins |
| **In Progress** | Implementation underway | Work assigned, code/design/content activity started | Proposed solution submitted for review |
| **In Review** | Awaiting review | Pull request or editorial/design review requested | Changes approved or sent back |
| **Testing** | QA, content validation or beta verification | Approved work available in suitable test environment | Acceptance criteria verified and release implications understood |
| **Done** | Accepted and validated | Definition of done completed, required release references recorded | Item may be archived later |

**Status is not deployment status.** A Done item may be shipped later as part of a separate production release.

### Priority semantics

- **P0 — Critical / release-blocking:** Severe safety, availability, security, data integrity or a release prerequisite. Escalate for prompt triage; a P0 label alone does not make an issue a confirmed vulnerability.
- **P1 — High:** Significant learner value, core functionality or imminent delivery dependency.
- **P2 — Normal:** Planned improvement that is not blocking current delivery.
- **P3 — Later:** Optional enhancement, exploration or long-term refinement.

P0 and P1 assignments should have an identified owner and a concrete next action.

## Shared fields

| Field | Type | Options / usage |
| --- | --- | --- |
| Status | Single select | Backlog, Todo, In Progress, In Review, Testing, Done |
| Priority | Single select | P0, P1, P2, P3 |
| Work Type | Single select | Feature, Bug, Technical Task, Content, Release, Security, Research |
| Area | Single select | Backend, Admin, Mobile, Web, Content, Infrastructure, Product, Shared |
| Product | Single select | Bilgin Exam TR, Bilgin ABC, Shared |
| Sprint | Iteration | Two-week planning cadence; only populate after capacity planning |
| Release | Text | e.g., v0.2.0-beta; use approved version identifiers |
| Start Date | Date | Agreed work start / roadmap window |
| Target Date | Date | Approved target, not a guessed release date |
| Effort | Number | Relative estimation; optional until team sizing is adopted |

Use built-in GitHub **Assignees**, **Labels**, and **Repository** metadata where available rather than duplicating them as custom text fields.

## Required views

Create and validate the following layouts in each board:

1. **Board** — Kanban grouped by Status. Show Priority, Area, Assignee and Release where useful. Sort P0 before P1–P3. Keep Testing distinct from Done.
2. **Table** — Planning view with Title, Status, Priority, Work Type, Area, Assignees, Sprint, Release and Target Date. Use for backlog grooming and sprint commitments.
3. **Roadmap** — Timeline view driven by Start Date and Target Date. Tasks without approved dates can remain unscheduled instead of assigning arbitrary deadlines.

Suggested additional saved filters (create manually as needed): **P0 Release Blockers**, **Current Sprint**, **Needs Review**, **Mobile Beta**, **Content Review** and **Ready for Production**.

## Project-specific guidance

### Bilgin Exam TR

- Maintain one Issue per actionable task in the correct private repository.
- Link cross-repository dependencies between Issues rather than duplicating them.
- Keep Admin login/security and API compatibility work high visibility.
- Mobile and store publishing work should be tracked separately from backend/site deployment.
- **Release track:** main → test-env → prod → explicit release/deployment approval.

### Bilgin ABC

- Use Project **drafts** during pre-repository planning.
- Do not create an unrelated product repository or copy Exam TR code as an implicit starting point.
- Organize work around Turkish literacy pedagogy, age-appropriate exercises, curriculum review, UX, privacy, child safety, accessibility, parent controls, and an **ad-free** child experience.
- Convert a draft to a repository Issue only after owning repository and implementation details are established.

### Bilgin Apps Roadmap

- Keep the portfolio board focused on outcomes and dependencies, not every development subtask.
- Reference product Issues or release records when a milestone relies on implementation work.
- Do not publish private incident details, customer information, secret values, or confidential planning to the public .github repository.
- Use Roadmap dates only when a release window is approved.

## Meeting and triage cadence

- **Weekly intake and triage:** review new Issues, duplicates, acceptance criteria, product impact and P0/P1 urgency.
- **Sprint planning:** select achievable work; identify owners, dependencies and verification responsibility.
- **Asynchronous PR review:** review code, content and UI changes according to repository policies.
- **Release readiness:** validate Testing outcomes, dependency compatibility and production readiness separately from issue closure.
- **Portfolio review:** reconcile the product boards with the organization Roadmap, update blocked items, risks and approved milestones.

## Protected issue repositories

Do not create, reopen, edit, import, or restore issues from `bilgin-exam-tr-mobile` or `bilgin-exam-tr-backend`. Repository links may remain, but issue intake and automatic sub-issue intake must exclude this work. Only relevant, currently open Admin and Web issues may enter the Exam board. Do not recreate removed draft tasks.

`Type` is reserved by the current GitHub Projects API. The custom classification field is named **Work Type**, retaining the options in the field table.

## Recommended automations

Enable these through GitHub Projects **Workflows** only after confirming they behave correctly with private repositories and account permissions:

- New open issues in explicitly approved Admin/Web repositories → add to the Exam Project. Never use repository linking alone as authorization for issue intake.
- New items → Backlog (not automatically In Progress).
- Closing an Issue → Done only if the acceptance and QA process for that work permits it; otherwise prefer manual approval.
- Automatic archiving → archive old completed items without deleting original Issues.
- Pull requests → rely on linked Issues and real review status; an opened PR is not proof of completion.

The current public API can read and delete native workflows, but cannot create or enable them. GitHub Free permits one auto-add rule per project. Keep automatic issue closure and completion disabled unless acceptance policy explicitly permits them. Broad automatic sub-issue intake is removed by the safe bootstrap.

Native Project workflows may not cover every custom condition; use secure, reviewed GitHub Actions only when necessary and with an appropriately scoped Projects token.

## Quality and privacy requirements

- Every item must have a concrete reason, scope and acceptance criteria before entering Todo.
- P0 release blockers must not be silently demoted or closed.
- Avoid placing private implementation details into the public organization repository.
- Share access intentionally: least privilege for external contributors, write access for maintainers.
- Keep product Issues, code, CI and store credentials private.
- Review actual Project visibility and team permissions after provisioning.

## Related files

- [Project setup and verification](PROJECTS_SETUP.md)
- [Developer standards](DEVELOPMENT_STANDARDS.md)
- [Release process](RELEASE_PROCESS.md)
- [Contribution guidance](../CONTRIBUTING.md)
- [Issue templates](../.github/ISSUE_TEMPLATE/)
