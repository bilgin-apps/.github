# Bilgin Apps — Development Standards

**Status:** Organization-wide guidance  
**Scope:** Bilgin Exam TR, Bilgin ABC, and shared engineering assets  
**Source of truth:** A product repository's documented architecture, CI, and release requirements take precedence when they are more specific.

These standards describe the intended engineering workflow. They do **not** claim that branch protections, GitHub Actions, app-store pipelines, or environment integrations are already configured.

## 1. Repository organization

- Keep distinct products in separate repositories or clearly isolated modules.
- Use descriptive repository names and maintain a current technical README.
- Preserve a single documented source of truth for API contracts and architectural decisions.
- Maintain CONTRIBUTING and SECURITY guidance for each product when it needs more detailed rules.
- Treat the public organization configuration repository as documentation-only. Never store application secrets here.

## 2. Branches and promotion

| Branch | Role | Promotion policy |
| --- | --- | --- |
| main | Active development and integration | Changes arrive through reviewed pull requests. |
| test-env | QA and beta candidate | Promote selected, validated work from main. |
| prod | Approved release baseline | Promote only an explicitly approved test candidate. |
| feat/*, fix/*, docs/*, chore/* | Short-lived work branches | Merge after review and quality checks. |

**Suggested flow:** feature branch → main → test-env → prod.

Do not use a branch name alone as proof of deployment. Deployment environments, signing, approval gates, and release automation require separate configuration.

Avoid directly committing to prod or force-pushing protected branches. Before applying mandatory rulesets, check GitHub plan support, integration permissions, CI check names, and administrator exception policy.

## 3. Pull request quality

Each pull request should state:

1. **Purpose:** the user or engineering problem being solved.
2. **Scope:** what changed, and what was explicitly not changed.
3. **Verification:** automated tests, manual QA, and their outcomes.
4. **Compatibility:** API, schema, app version, client, and data implications.
5. **Risk and rollback:** potential impact, monitoring, and recovery strategy.
6. **Evidence:** screenshots or screen recordings for meaningful UI changes.
7. **Traceability:** linked issue, task, or project reference when available.

Request at least one meaningful review before merging changes to shared or release branches. Branch protection must be enabled separately to enforce this rule.

## 4. Validation requirements

Use the commands and workflows documented in each product repository.

- **Backend/API:** run unit, integration, architecture, and contract tests appropriate to the changed behavior. Review migrations, authorization, and user-data impact.
- **Admin/Web:** run lint, type checking, tests, build checks, and UI accessibility checks relevant to the repository.
- **Mobile:** run available static analysis, unit/widget/UI tests, platform build verification, and beta device checks once the app toolchain is established.
- **Learning content:** verify curriculum mappings, answer correctness, publication approval, and accessibility; require appropriate subject-matter review before shipping educational material.
- **Infrastructure:** validate environment configuration, secret access, deployment ordering, observability, and rollback.

Test or build commands must not require production secrets on a pull request from untrusted code.

## 5. Security, privacy, and learner safety

- Never commit credentials, private keys, signing assets, production environment files, or personal data.
- Prefer minimal permissions for GitHub Actions, service credentials, and deployment integrations.
- Never expose server-only credentials in apps, static websites, or browser bundles.
- Treat accounts, authentication, payments, progress data, and administrator access as high-risk changes.
- Design educational content and interactions with privacy and age-appropriate safety in mind, especially for early learners.
- Report suspected vulnerabilities privately through [SECURITY.md](../SECURITY.md).

## 6. API and data contract coordination

A change that affects another repository should include:

- The versioned interface or schema change.
- Backward-compatibility assessment and migration plan.
- Consumer impact across mobile, web, and admin.
- Tests or fixtures exercising the affected contract.
- Deployment ordering, feature gating, and rollback instructions when necessary.

Avoid breaking live clients by deploying incompatible backend changes without a compatibility strategy.

## 7. Changes and releases

- Use concise, descriptive commit subjects such as feat:, fix:, docs:, test:, refactor:, or chore:.
- Prefer small, reviewable pull requests; do not mix unrelated refactors with security or release-critical fixes.
- Document release candidates and maintain a traceable source commit.
- Validate test-env before promoting to prod.
- Store signing secrets in secured release tooling, not in the repository.
- Tag production source commits and provide release notes when releasing.
- Follow the [Release Process](RELEASE_PROCESS.md) for coordinated mobile and service releases.

## 8. Completion checklist

- [ ] Scope and acceptance criteria are clear.
- [ ] Required tests and relevant CI checks pass.
- [ ] Documentation and API contracts are updated as needed.
- [ ] Security, privacy, and accessibility implications were considered.
- [ ] Cross-repository dependencies were coordinated.
- [ ] Release and rollback requirements were documented when relevant.

For reporting and contribution guidance, see [CONTRIBUTING.md](../CONTRIBUTING.md), [SUPPORT.md](../SUPPORT.md), and [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md).
