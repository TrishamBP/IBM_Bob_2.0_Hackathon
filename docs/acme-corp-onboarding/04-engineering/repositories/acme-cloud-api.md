---
document_id: ACME-REPO-001
title: Repository Guide — acme-cloud-api
category: engineering
department: engineering
applicable_roles: [backend-engineers, cloud-engineers, sres, platform-engineers]
owner: Anjali Desai (EM, Cloud API)
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [repository, acme-cloud, go-grpc-postgres-kafka]
---

# Repository Guide — `acme-cloud-api`

> **Fictional repository.** The host `git.acme.example` does not resolve. All commands below are **simulated** and shown for onboarding orientation only. Do not attempt to execute them against any real system.

## 1. Repository Purpose

`acme-cloud-api` is the core backend service for **ACME Cloud**. It exposes the public gRPC and REST APIs that customers use to provision cloud resources, manage tenants, and stream telemetry. The service is the system of record for tenant metadata, billing events, and quota state.

Key responsibilities:

- Tenant onboarding and identity federation.
- Resource provisioning (compute, network, storage abstractions).
- Quota enforcement and metering event publication to Kafka.
- Public API surface for the ACME Cloud Console and partner integrations.

## 2. Owning Team and EM

| Field | Value |
|-------|-------|
| Owning Team | Cloud API |
| Engineering Manager | Anjali Desai (anjali.desai@acme.example) |
| Product | ACME Cloud |
| Slack channel (fictional) | `#cloud-api` |
| On-call rotation | `cloud-api-oncall` PagerDuty-style schedule |

## 3. Primary Technology Stack

- **Language:** Go 1.22
- **API:** gRPC + grpc-gateway (REST projection), protobuf definitions under `proto/`
- **Datastore:** PostgreSQL 16 (primary), read replicas in each region
- **Streaming:** Apache Kafka (managed, fictional cluster `kafka.internal.acme.example`)
- **Observability:** OpenTelemetry traces to `traces.internal.acme.example`, metrics to `metrics.internal.acme.example`
- **Secrets:** HashiCorp Vault at `vault.acme.example`

## 4. Access Requirements

- **Source access:** Read/write to `acme-cloud-api` requires the **Engineering — Cloud** access tier.
- **CI access:** GitHub Actions runners at `runners.internal.acme.example` are self-hosted; logs are restricted to the owning team plus Security/GRC.
- **Container registry:** Push access to `registry.internal.acme.example/acme-cloud/api` is granted only to the CI service account and the release manager role.
- **Vault secrets:** Engineers receive a personal Vault token scoped to `secret/cloud-api/dev/*`. Staging and production paths require a separate, time-boxed approval.
- See [`../../08-forms/repository-access-request.md`](../../08-forms/repository-access-request.md) and [`../source-code-and-repository-access.md`](../source-code-and-repository-access.md).

## 5. Manager Approval Required

**Yes.** Access to `acme-cloud-api` requires approval from:

1. The hiring EM (Anjali Desai) — auto-confirmed for the new hire's home repository.
2. The receiving EM (Anjali Desai or her delegate) — for cross-team contributors.
3. Security GRC review — for any role that includes production deploy permissions.

For production environment credentials, see [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md). Engineers do **not** receive standing production access by default.

## 6. Local Setup

```bash
# fictional/simulated command — clone the repository
git clone git@git.acme.example:acme-cloud/acme-cloud-api.git
cd acme-cloud-api

# fictional/simulated command — install Go toolchain (if not preinstalled)
# See ../developer-workstation-setup.md for the supported Go version.

# fictional/simulated command — bootstrap local dependencies
make bootstrap

# fictional/simulated command — start local Postgres + Kafka + Vault dev container
docker compose up -d

# fictional/simulated command — generate protobuf and gRPC bindings
make generate

# fictional/simulated command — connect to dev Vault and export a dev token
export VAULT_ADDR=https://vault.acme.example
# vault login -method=oidp role=cloud-api-dev  # interactive; use your corp SSO
```

## 7. Branching Conventions

This repository follows the trunk-based model documented in [`../git-branching-strategy.md`](../practices/git-branching-strategy.md).

- `main` — always deployable. Direct commits are forbidden; changes land via squash-merge PRs.
- `release/<YYYY.MM>` — long-lived release branch cut monthly.
- `feat/<jira-id>-<slug>` — feature branches, short-lived.
- `fix/<jira-id>-<slug>` — bugfix branches.
- `hotfix/<jira-id>-<slug>` — branched from `release/*` for urgent prod fixes.

All branches must be rebased onto the latest `main` before merge.

## 8. Build and Test Commands

```bash
# fictional/simulated command — compile all packages
make build

# fictional/simulated command — run the unit test suite
make test

# fictional/simulated command — run integration tests (requires local Postgres + Kafka)
make test-integration

# fictional/simulated command — run linters (golangci-lint, buf lint, gosec)
make lint

# fictional/simulated command — build the container image
make docker-build IMG=registry.internal.acme.example/acme-cloud/api:dev

# fictional/simulated command — run the local API server on :8443
make run
```

## 9. Pull-Request Requirements

- A `CODEOWNERS` file (see below) is enforced via GitHub Enterprise branch protection.
- Minimum **two** approving reviews for `main`, of which at least one must be from a Cloud API team member.
- All status checks must pass:
  - `ci/build`
  - `ci/unit-tests`
  - `ci/lint`
  - `ci/buf-breaking` (protobuf backward-compatibility)
  - `ci/license-scan`
  - `ci/sast` (static analysis)
- PRs touching `proto/` or `internal/quota/` additionally require a Security GRC approval.
- Conventional Commit prefixes (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`) are required; the CI `commit-lint` job will fail otherwise.
- See [`../pull-requests-and-code-review.md`](../practices/pull-requests-and-code-review.md) and [`../coding-standards.md`](../practices/coding-standards.md).

## 10. CODEOWNERS (Sample Structure)

Sample `.github/CODEOWNERS` content:

```text
# Sample CODEOWNERS for acme-cloud-api (fictional)
# Each line maps a path to the GitHub team handle that owns it.

*                                           @acme/cloud-api

# Protobuf and public API surface — requires Cloud API tech-lead approval.
/proto/                                     @acme/cloud-api-leads
/api/                                       @acme/cloud-api-leads

# Quota and billing flows — extra Security GRC review required.
/internal/quota/                            @acme/cloud-api @acme/security-grc
/internal/billing/                          @acme/cloud-api @acme/security-grc

# Terraform for the service's own infrastructure — platform review required.
/deploy/terraform/                          @acme/cloud-api @acme/platform

# Documentation — broader edit access.
/docs/                                      @acme/cloud-api @acme/devrel
```

## 11. Deployment Environments

| Environment | Purpose | Trigger | Approver |
|-------------|---------|---------|----------|
| `dev` | Per-engineer sandbox, ephemeral namespace | Push to `main` | Auto (CI) |
| `staging` | Pre-prod integration with partners | Tag `v*` on `main` | Cloud API EM (Anjali Desai) |
| `production` | Customer-facing | Tagged release + change ticket | Release Manager + on-call SRE |

**Sample deployment sequence (fictional):**

```bash
# fictional/simulated command — promote image from staging to prod
make release-promote ENV=prod IMG=registry.internal.acme.example/acme-cloud-api:v2026.09.3

# fictional/simulated command — render the prod Helm values (does not deploy)
make helm-render ENV=prod > deploy/manifests/prod.rendered.yaml

# fictional/simulated command — open a change ticket referencing the tag
# Use the ITSM portal: https://itsm.acme.example/change/new  (fictional)

# fictional/simulated command — deploy via ArgoCD (pulls the rendered manifest)
# argocd app sync acme-cloud-api-prod  # only release managers and on-call have RBAC
```

> **Production access policy.** Engineers do **not** receive standing production access. Prod deploy rights are granted just-in-time for a release window and expire automatically. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md) and [`../ci-cd-overview.md`](../practices/ci-cd-overview.md).

## 12. Documentation Links

- Internal Wiki (fictional): `https://wiki.acme.example/cloud/api/architecture`
- Runbooks (fictional): `https://wiki.acme.example/cloud/api/runbooks`
- API reference (fictional): `https://docs.acme.example/cloud/api/reference`
- Architecture decision records: `docs/adr/` in this repository
- Service catalog entry: `https://catalog.acme.example/services/acme-cloud-api`

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
