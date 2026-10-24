# Bilgin Apps · Organization Hub

Welcome to the GitHub organization for **Bilgin Apps** — a family of learning experiences designed to make education more engaging, approachable, and enjoyable.

**Our products**
- **Bilgin Exam TR** — gamified exam preparation for learners in Türkiye.
- **Bilgin ABC** — playful early literacy and reading activities in Turkish.

## Organization profile

The public-facing organization introduction lives at [`profile/README.md`](profile/README.md). GitHub displays this file on the organization's overview page when this repository is **public**.

## How we work

Our product repositories are maintained separately to keep responsibilities clear. Contributions, security reports, and software changes should follow:

- [Contribution guidelines](CONTRIBUTING.md)
- [Security policy](SECURITY.md)

Each product repository can also maintain its own more specific documentation, development instructions, and workflows.

## Repository layout

```text
.github/
├── README.md                 # About this organization configuration repository
├── CONTRIBUTING.md           # Organization-wide contribution principles
├── SECURITY.md               # Organization-wide security reporting guidance
├── profile/
│   └── README.md             # Public organization homepage
└── .github/
    └── PULL_REQUEST_TEMPLATE.md
```

> This is an organization configuration repository. No application code, production credentials, or private keys should be committed here.

## Project management

Bilgin Apps maintains a private, three-board GitHub Projects V2 operating model for:

- **Bilgin Exam TR** — backend, admin, mobile, web, content, QA and release work.
- **Bilgin ABC** — Turkish early-literacy product planning, initially as private Project draft items.
- **Bilgin Apps Roadmap** — cross-product milestones, dependencies and release governance.

- [Project management standards](docs/PROJECT_MANAGEMENT.md)
- [Projects provisioning and verification](docs/PROJECTS_SETUP.md)
- [Repeatable GitHub Projects bootstrap](scripts/bootstrap_projects.py)

> GitHub Projects must be provisioned with an organization account with Projects write access. Committing the configuration is not equivalent to creating the live boards.
