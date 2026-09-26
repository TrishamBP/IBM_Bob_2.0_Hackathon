---
document_id: ACME-REPO-007
title: Repository Guide — acme-workspace-api
category: engineering
department: engineering
applicable_roles: [backend-engineers, workspace-engineers, sres, platform-engineers]
owner: Priya Menon (EM, Workspace API)
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [repository, acme-workspace, java-springboot-postgres-kafka]
---

# Repository Guide — `acme-workspace-api`

> **Fictional repository.** The host `git.acme.example` does not resolve. All commands below are **simulated** and shown for onboarding orientation only. Do not attempt to execute them against any real system.

## 1. Repository Purpose

`acme-workspace-api` is the backend service for **ACME Workspace**. It owns the document CRDT authority, the signaling plane for WebRTC peer coordination, presence, permissions, and the audit pipeline that emits workspace events to Kafka for downstream consumers.

Key responsibilities:

- Workspace, document, and folder lifecycle.
- CRDT op-log authority and snapshot persistence.
- WebRTC signaling room management and TURN credential issuance.
- Permissions model (owner / editor / viewer), audit log to Kafka.

## 2. Owning Team and EM

| Field | Value |
|-------|-------|
| Owning Team | Workspace API |
| Engineering Manager | Priya Menon (priya.menon@acme.example) |
| Product | ACME Workspace |
| Slack channel (fictional) | `#workspace-api` |
| On-call rotation | `workspace-api-oncall` (P-grade incidents) |

## 3. Primary Technology Stack

- **Language:** Java 21 (LTS), GraalVM native-image optional for cold-start paths
- **Framework:** Spring Boot 3.3, Spring WebSocket, Spring Security OAuth2
- **Datastore:** PostgreSQL 16, Redis for presence
- **Streaming:** Apache Kafka at `kafka.internal.acme.example` (topic `workspace-events`)
- **Observability:** OpenTelemetry → `traces.internal.acme.example`; metrics → `metrics.internal.acme.example`
- **Secrets:** Vault at `vault.acme.example` (path `secret/workspace/api/*`)

## 4. Access Requirements

- **Source access:** Read/write requires the **Engineering — Workspace** access tier.
- **CI access:** Self-hosted GitHub Actions runners at `runners.internal.acme.example`.
- **Container registry:** Push to `registry.internal.acme.example/acme-workspace/api` is limited to CI plus release managers.
- **Kafka topic ACLs:** Engineers receive dev-cluster produce/consume ACLs; production topic ACLs are scoped to service accounts only.
- See [`../../08-forms/repository-access-request.md`](../../08-forms/repository-access-request.md) and [`../source-code-and-repository-access.md`](../source-code-and-repository-access.md).

## 5. Manager Approval Required

**Yes.** Access requires:

1. Hiring EM (Priya Menon) approval — auto-confirmed for home repository.
2. Receiving EM (Priya Menon or delegate) for cross-team contributors.
3. Security GRC review — required for changes touching permissions (`security/`), TURN credential issuance (`signaling/turn/`), or audit pipeline (`audit/`).

> **Production deploy repository.** Engineers do **not** receive standing production access by default. Production DB, Kafka topic admin, and TURN-server credentials are gated behind just-in-time elevation. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md).

## 6. Local Setup

```bash
# fictional/simulated command — clone the repository
git clone git@git.acme.example:acme-workspace/acme-workspace-api.git
cd acme-workspace-api

# fictional/simulated command — install JDK 21 via the supported version manager
# See ../developer-workstation-setup.md for the supported JDK version.

# fictional/simulated command — build dependencies (Gradle wrapper)
./gradlew --version

# fictional/simulated command — start local Postgres + Redis + Kafka dev container
docker compose up -d

# fictional/simulated command — apply DB migrations (Flyway)
./gradlew flywayMigrate

# fictional/simulated command — connect to dev Vault
export VAULT_ADDR=https://vault.acme.example
# vault login -method=oidp role=workspace-api-dev  # interactive
```

## 7. Branching Conventions

Trunk-based per [`../git-branching-strategy.md`](../practices/git-branching-strategy.md):

- `main` — always deployable; squash-merge PRs only.
- `feat/<jira-id>-<slug>` — feature work.
- `fix/<jira-id>-<slug>` — defects.
- `crdt/<slug>` — CRDT format changes that require a migration.
- `release/<YYYY.MM>` — cut monthly from `main`.

## 8. Build and Test Commands

```bash
# fictional/simulated command — compile all modules
./gradlew build -x test

# fictional/simulated command — run the unit test suite
./gradlew test

# fictional/simulated command — run integration tests (requires Postgres + Redis + Kafka)
./gradlew integrationTest

# fictional/simulated command — run contract tests (Pact consumers)
./gradlew contractTest

# fictional/simulated command — linters (spotless, spotbugs, detekt)
./gradlew spotlessCheck spotbugsMain detekt

# fictional/simulated command — build the container image
./gradlew jibDockerBuild --image=registry.internal.acme.example/acme-workspace/api:dev

# fictional/simulated command — run the API server on :8080
./gradlew bootRun
```

## 9. Pull-Request Requirements

- `CODEOWNERS` enforced via branch protection.
- **Two** approving reviews for `main`; at least one from the Workspace API team.
- Required status checks:
  - `ci/build`
  - `ci/unit-tests`
  - `ci/integration-tests`
  - `ci/contract-tests`
  - `ci/lint`
  - `ci/sast`
  - `ci/license-scan`
- PRs touching `security/`, `signaling/turn/`, or `audit/` additionally require Security GRC approval.
- CRDT-format changes must include a backward-compatibility statement and a load-test result.
- See [`../pull-requests-and-code-review.md`](../practices/pull-requests-and-code-review.md) and [`../coding-standards.md`](../practices/coding-standards.md).

## 10. CODEOWNERS (Sample Structure)

```text
# Sample CODEOWNERS for acme-workspace-api (fictional)
*                                           @acme/workspace-api

# Permissions and signaling — security co-review
/security/                                  @acme/workspace-api @acme/security-grc
/signaling/turn/                            @acme/workspace-api @acme/security-grc
/audit/                                     @acme/workspace-api @acme/security-grc

# CRDT authority — lead review
/crdt/                                      @acme/workspace-api-leads

# Kubernetes deployment — platform review
/deploy/                                    @acme/workspace-api @acme/platform

# Documentation — broader edit access
/docs/                                      @acme/workspace-api @acme/devrel
```

## 11. Deployment Environments

| Environment | Purpose | Trigger | Approver |
|-------------|---------|---------|----------|
| `dev` | Per-engineer namespace, ephemeral | Push to a feature branch | Auto (CI) |
| `staging` | Pre-prod Kafka + Postgres + TURN staging | Merge to `main` | Workspace API EM (Priya Menon) |
| `production` | Customer-facing workspace backend | Tagged release + change ticket | Release Manager + on-call SRE |

**Sample deployment sequence (fictional):**

```bash
# fictional/simulated command — promote image from staging to prod
./gradlew releasePromote --env=prod --image=registry.internal.acme.example/acme-workspace/api:v2026.09.3

# fictional/simulated command — render the prod Helm values
./gradlew helmRender --env=prod > deploy/manifests/prod.rendered.yaml

# fictional/simulated command — open a change ticket
# Use the ITSM portal: https://itsm.acme.example/change/new  (fictional)

# fictional/simulated command — deploy via ArgoCD (release managers and on-call only)
# argocd app sync acme-workspace-api-prod

# fictional/simulated command — run DB migrations against prod (on-call SRE only)
# ./gradlew flywayMigrate --env=prod
```

> Production DB, Kafka topic admin, and TURN credentials are **not** standing access. Just-in-time elevation is granted for a release window after change-ticket approval. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md) and [`../ci-cd-overview.md`](../practices/ci-cd-overview.md).

## 12. Documentation Links

- Internal Wiki (fictional): `https://wiki.acme.example/workspace/api/architecture`
- CRDT format spec (fictional): `https://wiki.acme.example/workspace/api/crdt`
- Permissions model (fictional): `https://wiki.acme.example/workspace/api/permissions`
- Runbooks (fictional): `https://wiki.acme.example/workspace/api/runbooks`
- Service catalog entry: `https://catalog.acme.example/services/acme-workspace-api`

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
