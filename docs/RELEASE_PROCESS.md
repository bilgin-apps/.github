# Bilgin Apps — Release Process

This is a **release policy and operational checklist**, not a claim that app-store distribution, CI/CD, or production infrastructure is already configured.

## Overview

Bilgin Apps maintains product-specific release trains. Bilgin Exam TR and Bilgin ABC must not share build numbers, store releases, or production credentials simply because they belong to the same organization.

The intended code promotion path is:

1. **main:** integrate approved work and run relevant quality checks.
2. **test-env:** select a release candidate, test the integrated product, and distribute beta builds if configured.
3. **prod:** promote an approved candidate as the production source baseline.
4. **Distribution:** perform platform-specific deployment and store submission using configured tooling.

A successful merge into prod is **not** equivalent to a successful deployment or app-store publication.

## Release candidate checklist

- [ ] Candidate scope, issue list, and source commit are recorded.
- [ ] Automated checks are green or explicitly reviewed exceptions are documented.
- [ ] API compatibility between deployed services and installed mobile clients is confirmed.
- [ ] Database migrations and backward compatibility have been reviewed.
- [ ] Payment, login, onboarding, and learner progress flows have been tested if affected.
- [ ] Educational content and answer keys have passed editorial and subject-matter review if changed.
- [ ] Secrets, app signing assets, and store permissions are configured securely.
- [ ] QA results and release blockers are recorded.
- [ ] Rollout, monitoring, and rollback plans are approved.

## Environment responsibilities

| Surface | QA / test-env | Production / prod |
| --- | --- | --- |
| Backend | Isolated test data and credentials | Production data and least-privilege credentials |
| Admin | Test environment and verified admin roles | Production authentication and operational controls |
| Website | Preview or staging deployment | Public production site |
| iOS | Internal testing or TestFlight, when configured | App Store distribution |
| Android | Internal or closed testing, when configured | Google Play production rollout |

Never point QA automation at live learner records by default. Maintain distinct environment variables, tokens, and credentials.

## Mobile release identifiers

Use semantic versioning as a planning convention where appropriate; mobile build numbers must also follow each store's rules.

Examples of **naming only**, not already published versions:

- v0.1.0-alpha — early internal verification.
- v0.2.0-beta — candidate for testing distribution.
- v1.0.0 — first stable public release.

Choose actual version and build numbers separately per product and platform.

## Release ownership and approvals

Before publishing:

1. The responsible product maintainer confirms acceptance criteria.
2. The engineering owner reviews quality checks, compatibility, and deployment readiness.
3. Authorized release personnel approve the production promotion and platform submission.
4. A release record links the source commit, build identifier, release notes, and deployment outcome.

GitHub rulesets and environment reviewer gates should enforce these controls where the organization's plan and tooling support them. Written policy alone does not enforce access restrictions.

## Monitoring and rollback

- Record what was deployed, when, and by whom.
- Monitor crashes, API failures, authentication, payments, and learner progress after rollout.
- Pause or halt rollout if a severe regression is detected.
- For server components, deploy a known-safe compatible build; avoid assuming database schema rollback is safe.
- For mobile apps, prefer a tested hotfix and staged rollout controls. An already-installed app generally cannot be instantly downgraded remotely.
- Review incidents and document preventive action items after stabilization.

## Release notes template

### Version and platform
- Product:
- Version/build:
- Source commit/tag:
- Environment:
- Release date:

### Summary
- Features:
- Fixes:
- Content changes:
- Breaking changes or migrations:

### Validation
- Automated checks:
- Manual QA:
- Approvers:

### Operations
- Deployment/store status:
- Monitoring:
- Rollback or hotfix plan:

For engineering policy, see [Development Standards](DEVELOPMENT_STANDARDS.md).
