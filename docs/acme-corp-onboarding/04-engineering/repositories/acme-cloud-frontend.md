---
document_id: ACME-REPO-002
title: Repository Guide — acme-cloud-frontend
category: engineering
department: engineering
applicable_roles: [frontend-engineers, cloud-engineers, designers, qe-engineers]
owner: Manoj Pillai (EM, Cloud Frontend)
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [repository, acme-cloud, typescript-react-vite-playwright]
---

# Repository Guide — `acme-cloud-frontend`

> **Fictional repository.** The host `git.acme.example` does not resolve. All commands below are **simulated** and shown for onboarding orientation only. Do not attempt to execute them against any real system.

## 1. Repository Purpose

`acme-cloud-frontend` is the browser-based **ACME Cloud Console** — the web UI that customers use to manage cloud resources, view billing, configure IAM, and inspect telemetry. It is a single-page application that calls the gRPC-gateway REST projection of `acme-cloud-api`.

Key responsibilities:

- Tenant-scoped dashboard, resource browser, and console flows.
- Embedded Monaco-based editor for inline policy editing.
- Playwright end-to-end suite shared with `acme-quality-automation`.
- Web accessibility (WCAG 2.2 AA) conformance for all primary flows.

## 2. Owning Team and EM

| Field | Value |
|-------|-------|
| Owning Team | Cloud Frontend |
| Engineering Manager | Manoj Pillai (manoj.pillai@acme.example) |
| Product | ACME Cloud |
| Slack channel (fictional) | `#cloud-frontend` |
| On-call rotation | `cloud-frontend-oncall` (P-grade incidents only) |

## 3. Primary Technology Stack

- **Language:** TypeScript 5.4
- **Framework:** React 18, React Router 6, TanStack Query
- **Build tooling:** Vite 5, Vitest, Playwright
- **Styling:** Tailwind CSS, ACME design tokens published from `acme-shared-libraries`
- **Observability:** OpenTelemetry Web SDK, Real User Monitoring at `metrics.internal.acme.example`
- **Secrets:** Vault at `vault.acme.example`; build-time secrets injected via OIDC-federated GitHub Actions.

## 4. Access Requirements

- **Source access:** Read/write requires the **Engineering — Cloud** access tier.
- **CI access:** Self-hosted GitHub Actions runners at `runners.internal.acme.example`; ephemeral build cache scoped per branch.
- **Package registry:** Pulls design tokens and shared UI components from `packages.acme.example`.
- **Browser test matrix:** Managed Playwright grid at `playwright.internal.acme.example` (fictional).
- See [`../../08-forms/repository-access-request.md`](../../08-forms/repository-access-request.md) and [`../source-code-and-repository-access.md`](../source-code-and-repository-access.md).

## 5. Manager Approval Required

**Yes.** Access requires:

1. Hiring EM (Manoj Pillai) approval — auto-confirmed for home repository.
2. Receiving EM (Manoj Pillai or delegate) for cross-team contributors.
3. Security GRC review — required for roles that touch customer-data rendering components (`src/features/billing`, `src/features/iam`).

Production environment access for this repo is limited to deploying the static bundle to the CDN; engineers do **not** receive standing access to the CDN origin configuration. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md).

## 6. Local Setup

```bash
# fictional/simulated command — clone the repository
git clone git@git.acme.example:acme-cloud/acme-cloud-frontend.git
cd acme-cloud-frontend

# fictional/simulated command — install Node via the supported version manager
# See ../developer-workstation-setup.md for the supported Node LTS version.

# fictional/simulated command — install dependencies
npm ci

# fictional/simulated command — pull private shared packages (auth via OIDC)
npm run pull:tokens

# fictional/simulated command — start the dev server with mock API
npm run dev -- --mode mock

# fictional/simulated command — start the dev server pointed at staging API
npm run dev -- --mode staging --api=https://api.staging.acme.example
```

## 7. Branching Conventions

Trunk-based per [`../git-branching-strategy.md`](../practices/git-branching-strategy.md):

- `main` — always deployable; squash-merge PRs only.
- `feat/<jira-id>-<slug>` — feature work.
- `fix/<jira-id>-<slug>` — defect fixes.
- `chore/<slug>` — dependency bumps, config, refactor.
- `release/<YYYY.MM>` — cut monthly from `main`.

## 8. Build and Test Commands

```bash
# fictional/simulated command — type-check the project
npm run typecheck

# fictional/simulated command — production build
npm run build

# fictional/simulated command — unit tests
npm run test:unit

# fictional/simulated command — Playwright end-to-end suite
npm run test:e2e

# fictional/simulated command — accessibility audit (axe-core)
npm run test:a11y

# fictional/simulated command — linters (ESLint, Stylelint, Prettier)
npm run lint

# fictional/simulated command — bundle visualizer
npm run build:analyze
```

## 9. Pull-Request Requirements

- `CODEOWNERS` enforced via branch protection.
- **Two** approving reviews for `main`; at least one from a Cloud Frontend team member.
- Required status checks:
  - `ci/build`
  - `ci/typecheck`
  - `ci/unit-tests`
  - `ci/e2e-smoke`
  - `ci/a11y`
  - `ci/lint`
  - `ci/lighthouse-ci` (performance budget)
- PRs touching `src/features/billing/` or `src/features/iam/` require Security GRC approval.
- Visual regression snapshots must be reviewed and explicitly approved.
- See [`../pull-requests-and-code-review.md`](../practices/pull-requests-and-code-review.md) and [`../coding-standards.md`](../practices/coding-standards.md).

## 10. CODEOWNERS (Sample Structure)

```text
# Sample CODEOWNERS for acme-cloud-frontend (fictional)
*                                           @acme/cloud-frontend

# Design system consumers — design team co-review
/src/design-system/                         @acme/cloud-frontend @acme/design-system

# Sensitive customer-data components
/src/features/billing/                      @acme/cloud-frontend @acme/security-grc
/src/features/iam/                          @acme/cloud-frontend @acme/security-grc

# CI / build pipeline — platform co-review
/.github/workflows/                         @acme/cloud-frontend @acme/platform
```

## 11. Deployment Environments

| Environment | Purpose | Trigger | Approver |
|-------------|---------|---------|----------|
| `dev` | Branch preview deploys | Push to a feature branch | Auto (CI) |
| `staging` | Full-stack integration with `acme-cloud-api` staging | Merge to `main` | Cloud Frontend EM (Manoj Pillai) |
| `production` | Customer-facing CDN | Tagged release | Release Manager + on-call SRE |

**Sample deployment sequence (fictional):**

```bash
# fictional/simulated command — build the production bundle
npm run build -- --mode prod

# fictional/simulated command — upload to internal artifact store
npm run publish:bundle -- --tag=v2026.09.3

# fictional/simulated command — promote bundle to staging CDN origin
npm run cdn:promote -- --env=staging --tag=v2026.09.3

# fictional/simulated command — promote bundle to production (release managers only)
# npm run cdn:promote -- --env=prod --tag=v2026.09.3
```

> Engineers do **not** receive standing access to the production CDN origin or its WAF configuration. Just-in-time elevation is granted for a release window. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md) and [`../ci-cd-overview.md`](../practices/ci-cd-overview.md).

## 12. Documentation Links

- Internal Wiki (fictional): `https://wiki.acme.example/cloud/frontend/architecture`
- Component storybook (fictional): `https://storybook.cloud.acme.example`
- Runbooks (fictional): `https://wiki.acme.example/cloud/frontend/runbooks`
- Design tokens reference (fictional): `https://design.acme.example/tokens`
- Service catalog entry: `https://catalog.acme.example/services/acme-cloud-frontend`

## Related Documents

- [`../repository-catalog.md`](../repository-catalog.md)
- [`../developer-workstation-setup.md`](../developer-workstation-setup.md)
- [`../source-code-and-repository-access.md`](../source-code-and-repository-access.md)
- [`../git-branching-strategy.md`](../practices/git-branching-strategy.md)
- [`../pull-requests-and-code-review.md`](../practices/pull-requests-and-code-review.md)
- [`../ci-cd-overview.md`](../practices/ci-cd-overview.md)
- [`../coding-standards.md`](../practices/coding-standards.md)
- [`../observability-and-logging.md`](../practices/observability-and-logging.md)
- [`../incident-response-and-on-call-introduction.md`](../practices/incident-response-and-on-call-introduction.md)
- [`../../03-security/source-code-security.md`](../../03-security/source-code-security.md)
- [`../../03-security/secrets-management.md`](../../03-security/secrets-management.md)
- [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md)
- [`../../08-forms/repository-access-request.md`](../../08-forms/repository-access-request.md)
- [`../../08-forms/it-access-request.md`](../../08-forms/it-access-request.md)
- [`../../09-contacts/contact-directory.md`](../../09-contacts/contact-directory.md)
