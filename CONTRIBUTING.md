# Contributing to Bilgin Apps

Thank you for helping improve Bilgin Apps. Our product repositories may be private, and contributions are currently coordinated with authorized collaborators.

This is the **organization-wide baseline**. Repository-specific contribution instructions take precedence when they are more detailed.

## Before you begin

1. Read the target repository's `README.md`, `CONTRIBUTING.md`, and applicable architecture notes.
2. Check existing issues and pull requests to avoid duplicate work.
3. For substantial changes, confirm the intended scope with a maintainer before implementation.
4. Never include credentials, access tokens, signing keys, personal information, or production data in commits, issues, or screenshots.

## Branch and pull request workflow

- Branch from the appropriate development branch, usually `main`.
- Use descriptive names such as `feat/lesson-progress`, `fix/session-timeout`, or `docs/contribution-guide`.
- Keep pull requests focused and clearly explain **why** a change is needed.
- Include tests, documentation updates, and screenshots when relevant.
- Describe the validation performed and any rollout or rollback risks.
- Request review before merging. Do not bypass repository branch protection, CI, or required approvals.

### Branch environments

Product repositories may maintain the following branches:

| Branch | Intended role |
| --- | --- |
| `main` | Ongoing development and integration |
| `test-env` | QA, validation, and beta testing |
| `prod` | Approved production release baseline |

These names describe the **intended workflow**; a branch alone does not deploy an app or release it to an app store. Deployment and release automation must be configured separately.

## Engineering principles

- Favor readable, maintainable solutions over unnecessary complexity.
- Follow established code style and architecture in each repository.
- Preserve API and data compatibility where required; document breaking changes.
- Treat authentication, payments, learner data, and content publishing as sensitive areas requiring extra care.
- Do not modify another product's code or infrastructure without an explicit reason.
- Use the instructions and test commands documented in the specific repository.

## Reporting bugs or security issues

For normal defects or feature requests, use the appropriate product repository's issues when available. For possible vulnerabilities, **do not open a public issue**; follow [SECURITY.md](SECURITY.md) instead.
