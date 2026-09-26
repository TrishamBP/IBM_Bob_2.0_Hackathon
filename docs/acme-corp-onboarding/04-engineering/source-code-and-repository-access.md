---
document_id: ACME-ENG-016
title: ACME Corp Source Code and Repository Access
category: engineering
department: engineering
applicable_roles: [engineers]
owner: Engineering
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [engineering, repositories, access, overview]
---

# ACME Corp Source Code and Repository Access

This document defines how engineers request and obtain access to ACME source code repositories, how access is approved, what each repository is for, and how new engineers are onboarded to their first repository. It is the **overview**; per-repository details are in [`04-engineering/repositories/`](./repositories/) and the canonical catalog is [`04-engineering/repository-catalog.md`](./repository-catalog.md).

## Repository Access Model

ACME uses **role-based access control (RBAC)** on GitHub Enterprise, mapped to Microsoft Entra ID groups. Engineers do not get individual repository permissions; they get group membership, and groups get repository permissions.

| Group (fictional) | Members | Repositories |
|-------------------|---------|--------------|
| `eng-cloud-api` | Cloud API engineers | `acme-cloud-api` (read/write), `acme-shared-libraries` (read) |
| `eng-cloud-frontend` | Cloud Frontend engineers | `acme-cloud-frontend` (read/write), `acme-shared-libraries` (read) |
| `eng-intelligence-agents` | Intelligence Agents engineers | `acme-intelligence-agents` (read/write), `acme-shared-libraries` (read) |
| `eng-intelligence-inference` | Intelligence Inference engineers | `acme-intelligence-inference` (read/write), `acme-shared-libraries` (read) |
| `eng-intelligence-ml` | Intelligence ML engineers | `acme-intelligence-ml` (read/write), `acme-shared-libraries` (read) |
| `eng-workspace-web` | Workspace Web engineers | `acme-workspace-web` (read/write), `acme-shared-libraries` (read) |
| `eng-workspace-api` | Workspace API engineers | `acme-workspace-api` (read/write), `acme-shared-libraries` (read) |
| `eng-platform` | Platform Infrastructure engineers | `acme-platform-infrastructure`, `acme-shared-libraries` (read/write) |
| `eng-qe` | Quality Engineering | `acme-quality-automation` (read/write), all repos (read) |
| `eng-all-read` | All engineers | All repos (read-only on production repos) |
| `prod-deploy-<repo>` | On-call engineers for that repo | Production deployment credentials (time-bound via PIM) |
| `release-managers` | Rotating release managers | Tagging + deploy permissions |

## Access Tiers (Restated)

See [`04-engineering/repository-catalog.md`](./repository-catalog.md) for the canonical tier definitions. Restated:

1. **All Engineers** — read access to `acme-shared-libraries` and `acme-quality-automation`.
2. **Engineering — <BU>** — read/write to the BU's repositories.
3. **Production deploy** — restricted to on-call and release managers; time-bound PIM elevation required.

> New engineers do **not** receive standing production access. This is non-negotiable; see [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).

## Requesting Repository Access

### For your home repository (auto-approved)

Your home repository is the one owned by your team. The hiring EM approves it during onboarding.

1. Hiring EM submits the [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md) form on your behalf, pre-day-one.
2. IT Onboarding adds you to the corresponding Entra ID group via SCIM.
3. Within 4 business hours of your M365 account activation, you should have access.

### For a cross-team repository (requires two approvals)

If you need access to a repository owned by another team:

1. You submit the [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md) form.
2. Your EM reviews and either approves or rejects.
3. The receiving EM reviews and either approves or rejects.
4. For production-deploy repos, the GRC analyst (Karthik Subramanian) reviews for least-privilege compliance.
5. IT Onboarding adds you to the corresponding Entra ID group.
6. You receive an email confirmation.

Typical turnaround: 3 business days for read access, 5 business days for write access.

### For production-deploy access (PIM required)

Production-deploy access is **never standing**. It is granted via Microsoft Entra ID PIM (Privileged Identity Management) for a maximum of 4 hours per request.

1. Submit [`08-forms/it-access-request.md`](../08-forms/it-access-request.md) with `access_type: production-deploy`, target repo, target environment, requested duration (max 4h), and justification (link to incident or change ticket).
2. Your EM approves.
3. The GRC analyst approves (during business hours) or the on-call security engineer approves (after hours for SEV1/SEV2 incidents).
4. PIM activates your membership in the `prod-deploy-<repo>` Entra ID group for the requested duration.
5. At expiry, your membership is automatically removed and an audit log entry is written to `logs.internal.acme.example`.

## Repository Access Audit

- Group membership changes are logged to `logs.internal.acme.example` for 1 year.
- PIM activations are logged for 2 years.
- A quarterly access review is conducted by the GRC analyst with each EM — see [`03-security/identity-and-access-management.md`](../03-security/identity-and-access-management.md) for the policy.

## Per-Repository Documentation

For each repository, see the per-repo doc in [`04-engineering/repositories/`](./repositories/):

- [`repositories/acme-cloud-api.md`](./repositories/acme-cloud-api.md)
- [`repositories/acme-cloud-frontend.md`](./repositories/acme-cloud-frontend.md)
- [`repositories/acme-intelligence-agents.md`](./repositories/acme-intelligence-agents.md)
- [`repositories/acme-intelligence-inference.md`](./repositories/acme-intelligence-inference.md)
- [`repositories/acme-intelligence-ml.md`](./repositories/acme-intelligence-ml.md)
- [`repositories/acme-workspace-web.md`](./repositories/acme-workspace-web.md)
- [`repositories/acme-workspace-api.md`](./repositories/acme-workspace-api.md)
- [`repositories/acme-platform-infrastructure.md`](./repositories/acme-platform-infrastructure.md)
- [`repositories/acme-shared-libraries.md`](./repositories/acme-shared-libraries.md)
- [`repositories/acme-quality-automation.md`](./repositories/acme-quality-automation.md)

Each per-repo document includes:

- Repository purpose
- Owning team and EM
- Primary technology stack
- Access requirements
- Manager approval required
- Local setup commands
- Branching conventions
- Build and test commands
- Pull-request requirements (CODEOWNERS, reviewers, status checks)
- Sample CODEOWNERS file
- Deployment environments
- Documentation links (internal Wiki references — fictional)

## Local Setup Overview

For full workstation setup, see [`04-engineering/developer-workstation-setup.md`](./developer-workstation-setup.md). The minimal sequence for cloning and running a repo:

```bash
# fictional/simulated
# 1. Connect to ACME VPN
# 2. Clone
git clone git@git.acme.example:acme/acme-cloud-api.git
cd acme-cloud-api

# 3. Set up local environment
make setup

# 4. Build
make build

# 5. Run tests
make test

# 6. Run locally
make run
```

## Branching Conventions (Summary)

ACME uses **trunk-based development** with short-lived feature branches. The full policy is [`04-engineering/practices/git-branching-strategy.md`](./practices/git-branching-strategy.md). Key points:

- Default branch: `main`.
- Feature branches: `feat/<topic>` or `fix/<topic>` from `main`.
- Release branches: `release/<YYYY.MM>` cut from `main` by release managers.
- No long-lived dev branches; if a branch lives > 2 weeks, escalate.
- Squash merges for feature branches; fast-forward for release branches.
- Force-push to `main` or `release/*` is forbidden; CODEOWNERS required on every PR.

## Pull-Request Requirements (Summary)

The full PR and code review policy is [`04-engineering/practices/pull-requests-and-code-review.md`](./practices/pull-requests-and-code-review.md). Key points:

- Minimum 2 reviewers for production-deploy repos (`acme-cloud-api`, `acme-intelligence-inference`, `acme-workspace-api`, `acme-platform-infrastructure`).
- Minimum 1 reviewer for non-production repos.
- CODEOWNERS must approve.
- All required CI checks must pass: lint, unit, integration, license-scan, secret-scan, SAST.
- No direct commits to `main` or `release/*`.
- PRs are squash-merged; the squash commit message must follow [`04-engineering/practices/commit-message-conventions.md`](./practices/commit-message-conventions.md).

## CODEOWNERS (Summary)

Each repository has a `CODEOWNERS` file at the root. The file declares which teams own which paths. A sample:

```
# fictional/simulated
*                                  @acme/eng-cloud-api-leads
/src/api/                          @acme/eng-cloud-api-leads @acme/eng-cloud-api-oncall
/src/connectors/aws/               @acme/eng-cloud-api-aws
/src/connectors/azure/             @acme/eng-cloud-api-azure
/src/connectors/gcp/               @acme/eng-cloud-api-gcp
/docs/                             @acme/eng-cloud-api-docs
/.github/                          @acme/eng-platform-release
```

The CODEOWNERS file is reviewed by the owning EM quarterly.

## Deployment Environments (Summary)

Each repository has three environments:

| Environment | Purpose | Auto-deploy? | Access |
|-------------|---------|---------------|--------|
| `dev` | Per-developer or ephemeral test envs | Yes — on every merge to `main` | All engineers in the repo's group |
| `staging` | Shared pre-production | Yes — on every release branch update | Engineers + QE + Release Managers |
| `production` | Customer-facing | No — manual approval required | On-call + Release Managers only (PIM) |

See [`04-engineering/practices/development-staging-production.md`](./practices/development-staging-production.md) and [`04-engineering/practices/release-management.md`](./practices/release-management.md).

## Documentation Links

Each repository maintains:

- A `README.md` at the repo root, with quickstart.
- An `OPERATIONS.md` for runbooks and on-call procedures.
- A `CONTRIBUTING.md` linking to [`04-engineering/practices/coding-standards.md`](./practices/coding-standards.md), [`04-engineering/practices/pull-requests-and-code-review.md`](./practices/pull-requests-and-code-review.md), [`04-engineering/practices/git-branching-strategy.md`](./practices/git-branching-strategy.md).
- A Wiki page on `wiki.acme.example/eng/<repo>` (fictional) for design docs and decision records.

## Related Documents

- [`04-engineering/developer-workstation-setup.md`](./developer-workstation-setup.md)
- [`04-engineering/ai-coding-assistant-setup.md`](./ai-coding-assistant-setup.md)
- [`04-engineering/repository-catalog.md`](./repository-catalog.md)
- [`04-engineering/repositories/`](./repositories/) (per-repo docs)
- [`04-engineering/practices/git-branching-strategy.md`](./practices/git-branching-strategy.md)
- [`04-engineering/practices/pull-requests-and-code-review.md`](./practices/pull-requests-and-code-review.md)
- [`04-engineering/practices/coding-standards.md`](./practices/coding-standards.md)
- [`04-engineering/practices/commit-message-conventions.md`](./practices/commit-message-conventions.md)
- [`04-engineering/practices/ci-cd-overview.md`](./practices/ci-cd-overview.md)
- [`04-engineering/practices/development-staging-production.md`](./practices/development-staging-production.md)
- [`04-engineering/practices/release-management.md`](./practices/release-management.md)
- [`03-security/source-code-security.md`](../03-security/source-code-security.md)
- [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md)
- [`03-security/identity-and-access-management.md`](../03-security/identity-and-access-management.md)
- [`02-it/it-access-revocation.md`](../02-it/it-access-revocation.md)
- [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md)
- [`08-forms/it-access-request.md`](../08-forms/it-access-request.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
