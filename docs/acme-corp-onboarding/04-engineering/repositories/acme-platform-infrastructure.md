---
document_id: ACME-REPO-008
title: Repository Guide — acme-platform-infrastructure
category: engineering
department: engineering
applicable_roles: [platform-engineers, sres, infra-engineers, security-engineers]
owner: Nikhil Joshi (EM, Platform Infrastructure)
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [repository, shared, terraform-go-kubernetes-crossplane]
---

# Repository Guide — `acme-platform-infrastructure`

> **Fictional repository.** The host `git.acme.example` does not resolve. All commands below are **simulated** and shown for onboarding orientation only. Do not attempt to execute them against any real system.

## 1. Repository Purpose

`acme-platform-infrastructure` is the **foundational infrastructure** repository for ACME Corp. It owns the Terraform + Crossplane control planes that provision the cloud accounts, networks, Kubernetes clusters, Vault namespaces, and observability stack used by every other product team.

Key responsibilities:

- Landing-zone, network, and account factory (AWS + Azure + GCP).
- Managed Kubernetes cluster provisioning and node-pool policy.
- Crossplane composite claims for per-team platform resources.
- Global Vault policy, OIDC federation, and CI runner-pool bootstrap.

## 2. Owning Team and EM

| Field | Value |
|-------|-------|
| Owning Team | Platform Infrastructure |
| Engineering Manager | Nikhil Joshi (nikhil.joshi@acme.example) |
| Product | Shared |
| Slack channel (fictional) | `#platform-infra` |
| On-call rotation | `platform-infra-oncall` (P-grade infra incidents) |

## 3. Primary Technology Stack

- **IaC:** Terraform 1.7, Terragrunt, OpenTofu mirror
- **Kubernetes-native control plane:** Crossplane (provider-aws, provider-azure, provider-gcp, provider-kubernetes)
- **Policy:** OPA Gatekeeper, HashiCorp Sentinel
- **Automation language:** Go 1.22 (controllers, custom Crossplane providers)
- **CI/CD:** Self-hosted GitHub Actions runners at `runners.internal.acme.example`; Atlantis-style plan/apply at `atlantis.internal.acme.example` (fictional)
- **Secrets:** Vault at `vault.acme.example` (root path `secret/platform/*`)

## 4. Access Requirements

- **Source access:** Read/write requires the **Engineering — Platform** access tier.
- **CI access:** Self-hosted GitHub Actions runners at `runners.internal.acme.example`. Plan/apply is gated through Atlantis with per-environment approval.
- **Cloud console access:** Engineers receive dev-account read-only console access. Production cloud accounts are gated behind break-glass.
- **Vault root:** No engineer has standing root. Production Vault paths are managed via CI only.
- See [`../../08-forms/repository-access-request.md`](../../08-forms/repository-access-request.md) and [`../source-code-and-repository-access.md`](../source-code-and-repository-access.md).

## 5. Manager Approval Required

**Yes.** Access requires:

1. Hiring EM (Nikhil Joshi) approval — auto-confirmed for home repository.
2. Receiving EM (Nikhil Joshi or delegate) for cross-team contributors.
3. Security GRC + Cloud COE review — required for any change to landing-zone, network, IAM, or OIDC federation code paths.

> **Production deploy repository.** Engineers do **not** receive standing production access by default. Production `terraform apply` and Crossplane composition changes require a change ticket and just-in-time elevation to the prod Atlantis project. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md).

## 6. Local Setup

```bash
# fictional/simulated command — clone the repository
git clone git@git.acme.example:acme-platform/acme-platform-infrastructure.git
cd acme-platform-infrastructure

# fictional/simulated command — install toolchain (tfenv, tgenv, go, kubectl, crossplane CLI)
# See ../developer-workstation-setup.md for the supported versions.

# fictional/simulated command — pin Terraform version
tfenv install

# fictional/simulated command — install Go controller dependencies
go mod download

# fictional/simulated command — assume a dev cloud role via OIDC (auto, no static keys)
make assume-role ENV=dev

# fictional/simulated command — connect to dev Vault
export VAULT_ADDR=https://vault.acme.example
# vault login -method=oidp role=platform-dev  # interactive
```

> Static cloud credentials are **not** issued. All local dev uses OIDC-federated roles issued via GitHub Actions or your SSO session.

## 7. Branching Conventions

Trunk-based per [`../git-branching-strategy.md`](../practices/git-branching-strategy.md):

- `main` — always plan-clean; per-environment `terraform apply` runs from tagged commits.
- `feat/<jira-id>-<slug>` — new module or composition.
- `fix/<jira-id>-<slug>` — defects.
- `drift/<slug>` — drift-remediation branches that reconcile state to expected config.
- `release/<YYYY.MM>` — cut monthly from `main`.

All changes go through Atlantis; no local `terraform apply` against shared state.

## 8. Build and Test Commands

```bash
# fictional/simulated command — format check
make fmt-check

# fictional/simulated command — validate Terraform (recursive)
make tf-validate

# fictional/simulated command — terraform plan against dev (via Atlantis PR comment)
# atlantis plan -d environments/dev/network

# fictional/simulated command — run OPA / Sentinel policy checks
make policy-check

# fictional/simulated command — run Go unit tests for custom Crossplane providers
make test-go

# fictional/simulated command — run Terratest smoke tests against dev
make test-integration

# fictional/simulated command — linters (tflint, tfsec, gosec)
make lint
```

## 9. Pull-Request Requirements

- `CODEOWNERS` enforced via branch protection.
- **Two** approving reviews for `main`; at least one from the Platform Infrastructure team.
- Required status checks:
  - `ci/tf-fmt`
  - `ci/tf-validate`
  - `ci/tflint`
  - `ci/tfsec`
  - `ci/policy-check`
  - `ci/go-test`
  - `ci/sast`
- PRs must contain an Atlantis-generated plan output as a comment.
- PRs touching `environments/prod/`, `modules/iam/`, `modules/network/`, or `compositions/` additionally require Security GRC + Cloud COE approval.
- See [`../pull-requests-and-code-review.md`](../practices/pull-requests-and-code-review.md) and [`../coding-standards.md`](../practices/coding-standards.md).

## 10. CODEOWNERS (Sample Structure)

```text
# Sample CODEOWNERS for acme-platform-infrastructure (fictional)
*                                           @acme/platform

# Landing-zone, network, IAM — security + cloud COE co-review
/modules/network/                          @acme/platform @acme/security-grc @acme/cloud-coe
/modules/iam/                              @acme/platform @acme/security-grc @acme/cloud-coe
/compositions/                             @acme/platform @acme/security-grc

# Production environments — release-manager + on-call co-review
/environments/prod/                        @acme/platform @acme/release-managers @acme/sre

# Custom Crossplane providers — Go review
/providers/                                @acme/platform @acme/go-leads

# Atlantis config — SRE co-review
/atlantis.yaml                             @acme/platform @acme/sre
```

## 11. Deployment Environments

| Environment | Purpose | Trigger | Approver |
|-------------|---------|---------|----------|
| `dev` | Per-feature sandbox account + dev cluster | Atlantis plan + apply on PR | Auto (CI) |
| `staging` | Pre-prod landing-zone + shared services | Apply on tagged `release/*` | Platform EM (Nikhil Joshi) |
| `production` | Customer-affecting cloud + cluster state | Tagged release + change ticket | Release Manager + on-call SRE + Cloud COE |

**Sample deployment sequence (fictional):**

```bash
# fictional/simulated command — cut a release tag (platform EM approval)
git tag -a v2026.09.3 -m "platform release v2026.09.3"
git push origin v2026.09.3

# fictional/simulated command — open a change ticket referencing the tag
# Use the ITSM portal: https://itsm.acme.example/change/new  (fictional)

# fictional/simulated command — Atlantis applies staging then prod (approver-gated)
# atlantis apply -d environments/staging/network
# atlantis apply -d environments/prod/network  # requires prod approval

# fictional/simulated command — reconcile Crossplane compositions (release managers only)
# kubectl -n crossplane-system apply -f compositions/prod/network.yaml
```

> Production `terraform apply` and Crossplane composition changes require a change ticket and just-in-time elevation to the prod Atlantis project. Engineers do **not** receive standing production access. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md) and [`../ci-cd-overview.md`](../practices/ci-cd-overview.md).

## 12. Documentation Links

- Internal Wiki (fictional): `https://wiki.acme.example/platform/infrastructure/architecture`
- Account factory (fictional): `https://wiki.acme.example/platform/infrastructure/account-factory`
- Crossplane compositions catalog (fictional): `https://wiki.acme.example/platform/infrastructure/compositions`
- Runbooks (fictional): `https://wiki.acme.example/platform/infrastructure/runbooks`
- Service catalog entry: `https://catalog.acme.example/services/acme-platform-infrastructure`

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
