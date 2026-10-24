# Security Policy

Security and learner privacy matter across all Bilgin Apps products.

## Supported code

Security fixes are prioritized for actively maintained code and versions currently in use. Support for earlier versions is assessed case by case; no automatic support or response-time guarantee is implied.

## Report a vulnerability privately

**Do not disclose vulnerabilities in public issues, discussions, or pull requests.**

For a security issue in a product repository:

1. Open that repository's **Security** tab.
2. If private vulnerability reporting is enabled, use **Advisories → Report a vulnerability**.
3. If it is not available, contact an organization owner through an established **private** channel to arrange secure reporting.

Avoid sending secrets, real learner records, personal information, or exploit payloads through public channels. If possible, include the affected component, reproduction steps using test data, potential impact, and suggested mitigation.

## Security practices

- Keep secrets and signing keys out of the repository and client-delivered code.
- Apply least-privilege access and review dependency alerts.
- Protect authentication and session lifecycles; avoid logging sensitive information.
- Validate changes involving payments, publishing, learner data, and administrator permissions.
- Test only systems and environments you are authorized to assess.

## Coordination

Maintainers will review reports privately, determine impact, coordinate a fix, and share relevant updates when appropriate. This document does not promise a specific response or remediation timeline.

Repository-specific security policies take precedence if they provide additional reporting instructions.
