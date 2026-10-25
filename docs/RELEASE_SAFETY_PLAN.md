# Release safety implementation plan

This plan covers branch protection and QA/production separation. It does not enable protections, alter access, provision paid services, deploy software, or certify a product as release-ready. Production actions remain subject to an explicit release approval.

## Accountable coordination

The requesting organization administrator coordinates intake, evidence collection and approval routing. Each implementation change must name its actual engineering owner before entering a sprint. Repository administrators retain their existing permissions; this plan grants no access.

## Phase 1 — Confirm entitlement and check identities

1. Confirm ruleset and environment-reviewer support for the organization plan without purchasing an upgrade. The initial audit returned entitlement errors for rulesets on private repositories.
2. Inventory checks from successful GitHub Actions runs, including their source GitHub App. Do not configure a guessed check name or require a check that does not run on the intended pull-request target.
3. Treat `main`, `test-env` and `prod` as separate promotion boundaries. Confirm the actual hosting provider's branch mapping; branch names alone do not define deployment targets.
4. Inventory repository and environment **secret names and ownership only**. Never copy values into issues, logs, or documentation.

Candidate checks observed in repository workflow definitions (revalidate their emitted names and current applicability before enforcement):

| Surface | Exact emitted check name | Verification |
| --- | --- | --- |
| Backend | `test` | Successful GitHub check on the audited default-branch commit; workflow CI |
| Admin | `Lint, types, unit, integration, build` | Successful GitHub check on the audited default-branch commit; workflow Quality |
| Admin | `Auth smoke E2E` | Successful GitHub check on the audited default-branch commit; workflow Quality |
| Organization tooling | `Validate Projects bootstrap script` | Successful GitHub check on the Projects tooling PR |
| Mobile and Web | None currently emitted on the audited default-branch commits | Do not require nonexistent checks |

These are observed check names, not a permanent guarantee. Revalidate the current commit, originating GitHub App and PR-target triggers immediately before enforcement. Keep deployment-provider metadata and private environment inventories in maintainer-controlled records rather than public issue comments.

## Phase 2 — Prepare a pilot, then obtain enforcement approval

Prepare a proposed pilot on a repository with repeatable checks. Record the exact rule changes before applying them:

- Require pull requests with one approving review, dismiss stale approvals, and require resolved review conversations where the plan supports them.
- Require the verified checks appropriate to the repository and target branch. Verify that rules do not deadlock promotion pull requests.
- Block force pushes and branch deletion on the promotion branches.
- Document a narrowly scoped emergency bypass, its authorized approver and the required audit record. Do not grant a new bypass actor by default.
- Preserve existing development branches and deployment integrations.

If private-repository enforcement requires a plan upgrade, record the blocked capability and obtain a subscription decision. Written rules and status labels are not substitutes for technical enforcement.

Only after the pilot settings and approval are recorded should a maintainer test one permitted PR, one rejected bypass attempt, and one approved emergency recovery. Roll back the **pilot rule change** if it blocks the agreed development flow; never roll back production as part of a ruleset test. Extend rules to other repositories after evaluating the pilot evidence.

## Phase 3 — Separate QA and production

Prepare a provider-specific deployment map with repository, source branch, build system, environment, domain, service owner, data boundary and rollback owner.

- QA uses distinct service endpoints, test data, secret scopes and external-service accounts. It must not default to production learner records.
- Production credentials remain limited to approved production jobs and responsible release personnel.
- Confirm whether GitHub environment approvals are supported by the plan. When approval is enforced by a hosting provider, record the actual control and verify it there.
- Keep pull-request checks independent of live production credentials and services.
- Promote a recorded commit through QA verification before requesting production approval. Store releases and server/site deployments have separate approval and rollback paths.

Do not create empty environment names as a substitute for configuring real protections. Do not rotate secrets, change provider integrations, or redirect a deployment until its separate change is reviewed and approved.

## Evidence required before enforcement or release

| Decision | Required evidence |
| --- | --- |
| Branch protection pilot | Plan support, exact check contexts, target branches, rule diff, approved recovery path |
| Environment separation | Provider deployment map, owner, endpoint/data boundaries, secret-name inventory without values |
| Production promotion | Recorded source commit/build, passing checks, QA outcome, compatibility assessment, explicit release approval |
| Rollback readiness | Known-safe compatible candidate, migration implications, operator and verification steps |

## Protected issue repositories

Issues in `bilgin-exam-tr-mobile` and `bilgin-exam-tr-backend` must not be created, edited, reopened, recreated or imported. This plan may read repository configuration, but creates no issue work there. Coordinate cross-repository release dependencies through the existing eligible Admin/Web and governance work, without restoring removed tasks.

## Completion criteria

Planning is ready when the check inventory, entitlement decision, pilot proposal, deployment map, ownership and verification steps are recorded. Enforcement is complete only after the actual rules and environment controls have been applied with approval and verified directly. An item is not Done merely because this plan or a PR exists.
