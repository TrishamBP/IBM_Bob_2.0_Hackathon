---
document_id: ACME-TRN-007
title: Cloud Platform Fundamentals
category: training
department: engineering
applicable_roles: [cloud-platform-engineer, devops-engineer, backend-engineer, full-stack-engineer, quality-engineer]
owner: Engineering Enablement
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [training, platform, infrastructure, ci-cd, observability, secrets]
---

# Cloud Platform Fundamentals (ACME-TRN-007)

> Fictional document. All systems, links, and addresses are illustrative.

## 1. Module Overview

Cloud Platform Fundamentals is the internal-platform onboarding module for engineers working on the ACME internal platform — the shared infrastructure that every product team builds on. The module covers the internal CI/CD service, the package registry, the observability stack, the secrets manager, and the canonical environment topology. It is mandatory for engineers on Platform Infrastructure, Cloud API, and Workspace API; optional but recommended for every other engineer.

The module is owned by Engineering Enablement (Aditi Ghosh, `aditi.ghosh@acme.example`) in partnership with the Platform Infrastructure team lead and the CISO office (for secrets management content). It uses the `acme-platform-infrastructure` repository (fictional, on `git.acme.example`) as the primary reference.

## 2. Learning Objectives

By the end of this module, the engineer will be able to:

1. Describe the ACME internal platform topology: the CI/CD service, the package registry, the observability stack, the secrets manager, and the three environments.
2. Trigger, observe, and debug a CI/CD pipeline run end-to-end, including reading build logs, surfacing test failures, and re-running failed jobs.
3. Publish and consume an internal package via `packages.acme.example` (fictional) following the versioning rules.
4. Locate logs, metrics, traces, and dashboards in the observability stack and write a SLO/alert for a sample service.
5. Retrieve and rotate a secret from `vault.acme.example` (fictional) using approved CLI and SDK patterns, without exposing the secret in source or logs.
6. Promote a change from development to staging to production using the ACME promotion rules.

## 3. Target Audience

| Role | Required? | Notes |
|---|---|---|
| Platform Infrastructure engineers | **Mandatory** | Gates on-call eligibility. |
| Cloud API engineers | **Mandatory** | Gates production deploy permissions. |
| Workspace API engineers | **Mandatory** | Gates production deploy permissions. |
| Cloud Frontend engineers | Optional | Recommended; 2-hour condensed version. |
| Workspace Web engineers | Optional | Recommended; 2-hour condensed version. |
| Intelligence (agents/inference/ML) engineers | Optional | Recommended; covers observability and secrets. |
| Quality Engineers | Optional | Recommended; covers CI/CD and observability for test infra. |
| Customer Support Engineers | Optional | Read-only observability module only. |

## 4. Prerequisites

- Completion of [`engineering-orientation.md`](./engineering-orientation.md) (ACME-TRN-004).
- Completion of [`git-and-repository-workflows.md`](./git-and-repository-workflows.md) (ACME-TRN-005).
- Completion of [`security-awareness.md`](./security-awareness.md) (ACME-TRN-002) — gating for secrets content.
- Acknowledgement of secrets management — see [`../03-security/secrets-management.md`](../03-security/secrets-management.md).
- `acme-platform-infrastructure` repository access granted — see [`../04-engineering/repositories/acme-platform-infrastructure.md`](../04-engineering/repositories/acme-platform-infrastructure.md).

## 5. Duration

**Total: 4 hours**, all self-paced in `wiki.acme.example` with a 30-minute live lab review.

| Block | Duration | Modality |
|---|---|---|
| Platform topology overview | 30 min | Self-paced |
| CI/CD service deep-dive | 50 min | Self-paced |
| Package registry (`packages.acme.example`) | 40 min | Self-paced |
| Observability stack (logs, metrics, traces, alerts) | 50 min | Self-paced |
| Secrets manager (`vault.acme.example`) | 40 min | Self-paced |
| Environments & promotion | 30 min | Self-paced |
| Live lab review + 10-question quiz | 20 min | Mixed |

## 6. Outline of Topics Covered

### Block A — Platform Topology Overview (30 min)

- The internal platform: shared services that every product team builds on.
- Service inventory: CI/CD runner, package registry, observability stack, secrets manager, feature-flag service, internal developer portal.
- Ownership: Platform Infrastructure team (Tech Lead reports to CTO Sridhar Venkatesh). Reference: [`../04-engineering/repositories/acme-platform-infrastructure.md`](../04-engineering/repositories/acme-platform-infrastructure.md).

### Block B — CI/CD Service Deep-Dive (50 min)

- Pipeline as code: `.acme/pipeline.yml` convention.
- Runner pools: Linux and Windows runners; self-hosted for `acme-platform-infrastructure`.
- Stages: build → unit tests → integration tests → security scans → package publish → deploy to dev → integration smoke → deploy to staging → staging smoke → manual approval → deploy to production.
- Reference: [`../04-engineering/practices/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md).
- Re-run, cancel, and re-trigger rules; concurrency control.

### Block C — Package Registry (`packages.acme.example`) (40 min)

- Internal NuGet, npm, Maven, and Python feeds — all under `packages.acme.example`.
- Versioning: SemVer; pre-release suffixes (`-alpha.1`, `-beta.2`, `-rc.1`).
- Promoting a package from `dev` to `stable` feed; immutability rules.
- Reference: [`../04-engineering/practices/internal-package-management.md`](../04-engineering/practices/internal-package-management.md).
- Cross-reference: `acme-shared-libraries` repository — see [`../04-engineering/repositories/acme-shared-libraries.md`](../04-engineering/repositories/acme-shared-libraries.md).

### Block D — Observability Stack (50 min)

- Logs: structured logging conventions and the central log store.
- Metrics: service-level metrics, RED metrics (Rate, Errors, Duration).
- Traces: distributed tracing across services.
- Dashboards and SLOs.
- Alerting: PagerDuty integration; on-call rotation; runbook links.
- Reference: [`../04-engineering/practices/observability-and-logging.md`](../04-engineering/practices/observability-and-logging.md) and [`../04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md).
- Status page (`status.acme.example`): how the on-call updates the public status during incidents.

### Block E — Secrets Manager (`vault.acme.example`) (40 min)

- The ACME secrets manager (`vault.acme.example` — fictional): what it stores (DB credentials, API keys, certificates, signing keys), what it does not (passwords for human accounts — see [`../02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md)).
- Access patterns: CLI, SDK, CI-injected credentials; never check secrets into Git.
- Rotation cadence and break-glass procedures.
- Reference: [`../03-security/secrets-management.md`](../03-security/secrets-management.md) and [`../03-security/data-classification.md`](../03-security/data-classification.md).

### Block F — Environments & Promotion (30 min)

- Development, staging, production — see [`../04-engineering/practices/development-staging-production.md`](../04-engineering/practices/development-staging-production.md).
- Promotion gates: CI green, security scans clean, CODEOWNERS approval, staging smoke pass, manual approval for production.
- Release management — see [`../04-engineering/practices/release-management.md`](../04-engineering/practices/release-management.md).
- Rollback procedure: versioned artifacts, one-click rollback to the previous stable, post-rollback RCA.

### Block G — Live Lab Review + Knowledge Check (20 min)

- 30-minute live lab review with a Platform Infrastructure mentor (scheduled monthly).
- 10-question quiz covering all six blocks; threshold 80%.

## 7. Format

**Mixed.** Self-paced content (3.5 hours) plus a 30-minute live lab review hosted by a Platform Infrastructure mentor on the second Thursday of each month. The lab review is recorded for off-cycle hires.

## 8. Completion Criteria

- All six content blocks marked `COMPLETED` in the LMS.
- 10-question quiz score **≥ 80%** (≥ 8 of 10 correct).
- Live lab review attended (or recording watched within 5 business days).
- Acknowledgement of secrets management — see [`../03-security/secrets-management.md`](../03-security/secrets-management.md) — recorded via [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md).
- [`../08-forms/training-completion.md`](../08-forms/training-completion.md) submitted and signed off by Engineering Enablement.

## 9. Follow-up / Next Steps

- On-call eligibility for Platform Infrastructure engineers is granted after a shadow rotation — see [`../07-workflows/first-60-days.md`](../07-workflows/first-60-days.md).
- Production deploy permissions are granted via [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md) after this module and the first 30 days.
- Cross-reference product-specific training in [`product-training.md`](./product-training.md) (ACME-TRN-008).
- Annual refresher: 60-minute platform changes briefing plus 5-question quiz, scheduled 11 months after completion.

## 10. Trainer / Owner

| Role | Person | Responsibility |
|---|---|---|
| Module owner | Aditi Ghosh, Engineering Enablement lead (`aditi.ghosh@acme.example`) | Content strategy, annual review. |
| Platform Infrastructure mentor | Senior engineer from the Platform Infrastructure team | Live lab review, sign-off. |
| Security content co-owner | Rajan Mehta, CISO (`rajan.mehta@acme.example`) | Secrets manager content, audit oversight. |
| LMS coordinator | Anjali Iyer, Training Operations (`anjali.iyer@acme.example`) | Tracking, sign-off. |

Escalation contacts are in [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md). Glossary terms are in [`../metadata/glossary.md`](../metadata/glossary.md).
