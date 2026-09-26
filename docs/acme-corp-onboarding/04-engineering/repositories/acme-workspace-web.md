---
document_id: ACME-REPO-006
title: Repository Guide — acme-workspace-web
category: engineering
department: engineering
applicable_roles: [frontend-engineers, workspace-engineers, designers, qe-engineers]
owner: Thomas Buckley (EM, Workspace Web)
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [repository, acme-workspace, typescript-react-webrtc]
---

# Repository Guide — `acme-workspace-web`

> **Fictional repository.** The host `git.acme.example` does not resolve. All commands below are **simulated** and shown for onboarding orientation only. Do not attempt to execute them against any real system.

## 1. Repository Purpose

`acme-workspace-web` is the browser client for **ACME Workspace**, the collaborative canvas product. It renders real-time whiteboards, multi-user cursors, voice rooms, and screen-share sessions on top of WebRTC and the ACME Workspace signaling backend (`acme-workspace-api`).

Key responsibilities:

- Real-time canvas rendering (CRDT-backed, conflict-free replicated document).
- WebRTC peer connection management, simulcast, and bandwidth adaptation.
- Voice-room audio routing with echo cancellation and noise suppression.
- Offline-first sync with replayable op-log.

## 2. Owning Team and EM

| Field | Value |
|-------|-------|
| Owning Team | Workspace Web |
| Engineering Manager | Thomas Buckley (thomas.buckley@acme.example) |
| Product | ACME Workspace |
| Slack channel (fictional) | `#workspace-web` |
| On-call rotation | `workspace-web-oncall` (P-grade real-time incidents) |

## 3. Primary Technology Stack

- **Language:** TypeScript 5.4
- **Framework:** React 18, Zustand, Yjs (CRDT), Whisper (WebRTC mesh)
- **Build tooling:** Vite 5, Vitest, Playwright
- **Real-time:** WebRTC + WebSocket signaling; custom TURN/STUN at `turn.internal.acme.example`
- **Observability:** OpenTelemetry Web SDK; WebRTC stats → `metrics.internal.acme.example`
- **Secrets:** Vault at `vault.acme.example`; build-time TURN credentials injected via OIDC-federated GitHub Actions.

## 4. Access Requirements

- **Source access:** Read/write requires the **Engineering — Workspace** access tier.
- **CI access:** Self-hosted GitHub Actions runners at `runners.internal.acme.example`.
- **Package registry:** Pulls the ACME design tokens and shared CRDT utilities from `packages.acme.example`.
- **TURN/STUN test matrix:** Managed WebRTC test grid at `webrtc-test.internal.acme.example` (fictional).
- See [`../../08-forms/repository-access-request.md`](../../08-forms/repository-access-request.md) and [`../source-code-and-repository-access.md`](../source-code-and-repository-access.md).

## 5. Manager Approval Required

**Yes.** Access requires:

1. Hiring EM (Thomas Buckley) approval — auto-confirmed for home repository.
2. Receiving EM (Thomas Buckley or delegate) for cross-team contributors.
3. Security GRC review — required for changes touching `src/realtime/`, `src/voice/`, or `src/sync/` (CRDT op-log) due to cross-tenant data isolation requirements.

Production access for the static bundle deploy is limited; engineers do **not** receive standing access to the CDN origin or TURN server configuration. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md).

## 6. Local Setup

```bash
# fictional/simulated command — clone the repository
git clone git@git.acme.example:acme-workspace/acme-workspace-web.git
cd acme-workspace-web

# fictional/simulated command — install Node via the supported version manager
# See ../developer-workstation-setup.md for the supported Node LTS version.

# fictional/simulated command — install dependencies
npm ci

# fictional/simulated command — pull shared design tokens + CRDT utilities (auth via OIDC)
npm run pull:tokens

# fictional/simulated command — start the dev server pointed at local mock signaling
npm run dev -- --mode=mock

# fictional/simulated command — start the dev server pointed at staging signaling
npm run dev -- --mode=staging --signaling=https://api.staging.acme.example
```

> Local WebRTC needs a valid STUN/TURN pair; the dev profile auto-injects the dev TURN credentials from Vault.

## 7. Branching Conventions

Trunk-based per [`../git-branching-strategy.md`](../practices/git-branching-strategy.md):

- `main` — always deployable; squash-merge PRs only.
- `feat/<jira-id>-<slug>` — feature work.
- `fix/<jira-id>-<slug>` — defects.
- `crdt/<slug>` — CRDT/format changes that require a migration.
- `release/<YYYY.MM>` — cut monthly from `main`.

CRDT-format branches must include a migration + compatibility window in the PR description.

## 8. Build and Test Commands

```bash
# fictional/simulated command — type-check
npm run typecheck

# fictional/simulated command — production build
npm run build

# fictional/simulated command — unit tests
npm run test:unit

# fictional/simulated command — Playwright e2e suite (single browser)
npm run test:e2e

# fictional/simulated command — multi-browser WebRTC matrix
npm run test:webrtc-matrix

# fictional/simulated command — accessibility audit (axe-core)
npm run test:a11y

# fictional/simulated command — linters (ESLint, Stylelint, Prettier)
npm run lint

# fictional/simulated command — bundle visualizer
npm run build:analyze
```

## 9. Pull-Request Requirements

- `CODEOWNERS` enforced via branch protection.
- **Two** approving reviews for `main`; at least one from the Workspace Web team.
- Required status checks:
  - `ci/build`
  - `ci/typecheck`
  - `ci/unit-tests`
  - `ci/e2e-smoke`
  - `ci/webrtc-matrix`
  - `ci/a11y`
  - `ci/lint`
  - `ci/lighthouse-ci`
- PRs touching `src/realtime/`, `src/voice/`, or `src/sync/` require Security GRC approval.
- CRDT-format changes require a load-test result from `acme-quality-automation` linked in the PR.
- See [`../pull-requests-and-code-review.md`](../practices/pull-requests-and-code-review.md) and [`../coding-standards.md`](../practices/coding-standards.md).

## 10. CODEOWNERS (Sample Structure)

```text
# Sample CODEOWNERS for acme-workspace-web (fictional)
*                                           @acme/workspace-web

# Real-time + voice code — security co-review
/src/realtime/                             @acme/workspace-web @acme/security-grc
/src/voice/                                @acme/workspace-web @acme/security-grc
/src/sync/                                 @acme/workspace-web @acme/security-grc

# Design system consumers — design team co-review
/src/design-system/                        @acme/workspace-web @acme/design-system

# CI / build pipeline — platform co-review
/.github/workflows/                        @acme/workspace-web @acme/platform
```

## 11. Deployment Environments

| Environment | Purpose | Trigger | Approver |
|-------------|---------|---------|----------|
| `dev` | Branch preview deploys | Push to a feature branch | Auto (CI) |
| `staging` | Full-stack integration with `acme-workspace-api` staging | Merge to `main` | Workspace Web EM (Thomas Buckley) |
| `production` | Customer-facing CDN | Tagged release | Release Manager + on-call SRE |

**Sample deployment sequence (fictional):**

```bash
# fictional/simulated command — build the production bundle
npm run build -- --mode=prod

# fictional/simulated command — upload to internal artifact store
npm run publish:bundle -- --tag=v2026.09.3

# fictional/simulated command — promote bundle to staging CDN origin
npm run cdn:promote -- --env=staging --tag=v2026.09.3

# fictional/simulated command — promote bundle to production (release managers only)
# npm run cdn:promote -- --env=prod --tag=v2026.09.3
```

> Engineers do **not** receive standing access to the production CDN origin or the TURN/STUN server configuration. Just-in-time elevation is granted for a release window. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md) and [`../ci-cd-overview.md`](../practices/ci-cd-overview.md).

## 12. Documentation Links

- Internal Wiki (fictional): `https://wiki.acme.example/workspace/web/architecture`
- CRDT format reference (fictional): `https://wiki.acme.example/workspace/web/crdt`
- WebRTC runbooks (fictional): `https://wiki.acme.example/workspace/web/runbooks`
- Component storybook (fictional): `https://storybook.workspace.acme.example`
- Service catalog entry: `https://catalog.acme.example/services/acme-workspace-web`

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
