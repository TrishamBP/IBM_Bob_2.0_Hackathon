---
document_id: ACME-REPO-009
title: Repository Guide — acme-shared-libraries
category: engineering
department: engineering
applicable_roles: [all-engineers, platform-engineers, library-owners]
owner: Nikhil Joshi (acting EM, Platform Infrastructure)
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [repository, shared, multi-language-libs]
---

# Repository Guide — `acme-shared-libraries`

> **Fictional repository.** The host `git.acme.example` does not resolve. All commands below are **simulated** and shown for onboarding orientation only. Do not attempt to execute them against any real system.

## 1. Repository Purpose

`acme-shared-libraries` is the **monorepo of cross-team shared libraries** for ACME Corp. It contains per-language utility libraries, the ACME design-token package, common observability SDK wrappers, and opinionated scaffolding for new services. Every product team consumes at least one library from this repo.

Key responsibilities:

- Per-language client SDKs for ACME platform services (Go, TypeScript, Python, Java).
- ACME design tokens + React component primitives consumed by the web frontends.
- OpenTelemetry wrapper libraries with ACME-default resource attributes.
- Scaffolding templates (`go-service`, `ts-service`, `py-service`, `java-service`).

## 2. Owning Team and EM

| Field | Value |
|-------|-------|
| Owning Team | Platform Infrastructure (acting owner) |
| Engineering Manager | Nikhil Joshi (nikhil.joshi@acme.example) |
| Product | Shared |
| Slack channel (fictional) | `#shared-libs` |
| On-call rotation | `shared-libs-oncall` (consumer-blocking incidents only) |

> Per-language sub-teams own the deep expertise:
> - Go: `acme/go-libs` reviewers
> - TypeScript: `acme/ts-libs` reviewers (with the Design System team for `tokens/`)
> - Python: `acme/py-libs` reviewers
> - Java: `acme/java-libs` reviewers

## 3. Primary Technology Stack

- **Languages:** Go 1.22, TypeScript 5.4, Python 3.11, Java 21
- **Build tooling:** per language (`make`, `npm`, `poetry`, `gradle`)
- **Publishing:** internal package registry at `packages.acme.example` (Go module proxy, npm registry, PyPI simple index, Maven repo)
- **CI/CD:** GitHub Actions matrix builds on `runners.internal.acme.example`; auto-publishing on tagged release
- **Secrets:** Vault at `vault.acme.example`; publishing credentials are CI-scoped OIDC tokens, not personal.

## 4. Access Requirements

- **Source access:** Read access is granted to **all engineers** (the only repo with default-open read). Write access requires the **Engineering — Platform** access tier plus membership in the relevant per-language reviewers team.
- **CI access:** Self-hosted GitHub Actions runners at `runners.internal.acme.example`.
- **Package registry:** Pull is open to all engineers; publish is limited to the CI service account.
- See [`../../08-forms/repository-access-request.md`](../../08-forms/repository-access-request.md) and [`../source-code-and-repository-access.md`](../source-code-and-repository-access.md).

## 5. Manager Approval Required

**Yes — for write access.** Read access is granted to all engineers by default.

1. Read access — auto-granted at onboarding via the SSO group `acme-all-engineers`.
2. Write access — requires the **Engineering — Platform** tier and approval from Nikhil Joshi (acting EM).
3. Per-language reviewer status — additionally requires nomination by the relevant per-language sub-team lead.
4. Security GRC review — required for changes touching crypto, auth helpers, or the OpenTelemetry PII-redaction library.

There is no production environment in this repository; "deployment" is package publishing. Publish credentials are CI-scoped only — no engineer receives standing publish rights. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md).

## 6. Local Setup

```bash
# fictional/simulated command — clone the repository
git clone git@git.acme.example:acme-platform/acme-shared-libraries.git
cd acme-shared-libraries

# fictional/simulated command — install the supported toolchains per language
# See ../developer-workstation-setup.md for supported Go/Node/Python/JDK versions.

# fictional/simulated command — bootstrap all language workspaces
make bootstrap

# fictional/simulated command — pull latest published tokens (for TS workspace)
npm ci --workspace=ts/tokens

# fictional/simulated command — connect to dev Vault (publishing tokens are CI-only)
export VAULT_ADDR=https://vault.acme.example
# vault login -method=oidp role=shared-libs-dev  # interactive, read-only
```

## 7. Branching Conventions

Trunk-based per [`../git-branching-strategy.md`](../practices/git-branching-strategy.md):

- `main` — always publishable; squash-merge PRs only.
- `feat/<jira-id>-<slug>` — new library or major version.
- `fix/<jira-id>-<slug>` — defects.
- `chore/<slug>` — dependency bumps, config, refactor.
- `release/<lang>/<version>` — per-language release branches cut on major/minor bumps.

## 8. Build and Test Commands

```bash
# fictional/simulated command — build all language workspaces
make build

# fictional/simulated command — run all unit tests across languages
make test

# fictional/simulated command — run a single language suite (e.g., Go)
make test-go

# fictional/simulated command — run a single language suite (e.g., TypeScript)
make test-ts

# fictional/simulated command — linters across all languages
make lint

# fictional/simulated command — publish dry-run (does not push to registry)
make publish-dry-run -- --lang=go --version=0.4.0

# fictional/simulated command — publish for real (CI-only; uses OIDC token)
# make publish -- --lang=go --version=0.4.0
```

## 9. Pull-Request Requirements

- `CODEOWNERS` enforced via branch protection — paths are split per language and per concern.
- **Two** approving reviews for `main`; at least one from the relevant per-language reviewers team.
- Required status checks (matrix):
  - `ci/build-go`, `ci/build-ts`, `ci/build-py`, `ci/build-java`
  - `ci/test-go`, `ci/test-ts`, `ci/test-py`, `ci/test-java`
  - `ci/lint` (per language)
  - `ci/sast` (per language)
  - `ci/license-scan`
- PRs touching `go/crypto/`, `ts/otel-pii/`, `py/auth/`, or `java/auth/` additionally require Security GRC approval.
- PRs that bump a major version require a consumer-impact statement and a deprecation window per [`../coding-standards.md`](../practices/coding-standards.md).
- See [`../pull-requests-and-code-review.md`](../practices/pull-requests-and-code-review.md).

## 10. CODEOWNERS (Sample Structure)

```text
# Sample CODEOWNERS for acme-shared-libraries (fictional)
# Read access is open to all engineers; write access is per-language gated.

# Go libraries
/go/                                        @acme/platform @acme/go-libs
/go/crypto/                                 @acme/go-libs @acme/security-grc

# TypeScript libraries + design tokens
/ts/                                        @acme/platform @acme/ts-libs
/ts/tokens/                                 @acme/ts-libs @acme/design-system
/ts/otel-pii/                               @acme/ts-libs @acme/security-grc

# Python libraries
/py/                                        @acme/platform @acme/py-libs
/py/auth/                                   @acme/py-libs @acme/security-grc

# Java libraries
/java/                                      @acme/platform @acme/java-libs
/java/auth/                                 @acme/java-libs @acme/security-grc

# CI / publishing pipeline — platform co-review
/.github/workflows/                         @acme/platform @acme/release-managers
```

## 11. Deployment Environments

This repository has **no runtime environments**. The "deploy" operation is **package publishing** to `packages.acme.example`.

| Stage | Purpose | Trigger | Approver |
|-------|---------|---------|----------|
| `dev` snapshot | Per-branch snapshot packages for consumer testing | Push to a feature branch | Auto (CI) |
| `rc` | Release-candidate packages for staging consumers | Tag `v*-rc.*` on `main` | Per-language reviewers |
| `release` | Customer-consumable published packages | Tagged release + change ticket | Release Manager + on-call SRE |

**Sample publish sequence (fictional):**

```bash
# fictional/simulated command — cut a release tag (per-language reviewers approved)
git tag -a go/v0.4.0 -m "go-libs v0.4.0"
git push origin go/v0.4.0

# fictional/simulated command — open a change ticket for downstream consumers
# Use the ITSM portal: https://itsm.acme.example/change/new  (fictional)

# fictional/simulated command — CI publishes via OIDC token (no static credential)
# make publish -- --lang=go --version=0.4.0

# fictional/simulated command — broadcast the release to consumer teams
# acme-notify --channel=#release-announce --msg="go-libs v0.4.0 published"
```

> Publish credentials are **CI-scoped OIDC tokens only**. No engineer receives standing publish rights. Consumer-impacting major bumps require a deprecation window of at least 90 days. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md) and [`../ci-cd-overview.md`](../practices/ci-cd-overview.md).

## 12. Documentation Links

- Internal Wiki (fictional): `https://wiki.acme.example/shared-libs/overview`
- Per-language catalogs (fictional): `https://wiki.acme.example/shared-libs/{go,ts,py,java}`
- Consumer migration guide (fictional): `https://wiki.acme.example/shared-libs/migrations`
- Design tokens reference (fictional): `https://design.acme.example/tokens`
- Service catalog entry: `https://catalog.acme.example/services/acme-shared-libraries`

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
