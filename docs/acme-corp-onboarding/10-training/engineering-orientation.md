---
document_id: ACME-TRN-004
title: Engineering Orientation
category: training
department: engineering
applicable_roles: [backend-engineer, frontend-engineer, full-stack-engineer, cloud-platform-engineer, devops-engineer, ai-ml-engineer, ai-research-engineer, quality-engineer, customer-support-engineer]
owner: Engineering Enablement
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [training, engineering, orientation, mandatory]
---

# Engineering Orientation (ACME-TRN-004)

> Fictional document. All systems, links, and addresses are illustrative.

## 1. Module Overview

Engineering Orientation is the mandatory entry point to the ACME Corp engineering culture, tooling, and operating model. It is required of every engineer across Cloud, Intelligence, Workspace, Platform Infrastructure, Quality, and Support. The module walks the new hire through the engineering organisation structure, the canonical repository catalogue, the branch/PR/CI/CD pipeline, the testing philosophy, debugging practices, the development/staging/production environment model, release management, and an introduction to incident response and on-call.

The module is owned by Engineering Enablement, led by Aditi Ghosh (`aditi.ghosh@acme.example`, also Tech Lead Cloud API), and is delivered in coordination with VP Engineering / CTO Sridhar Venkatesh (`sridhar.venkatesh@acme.example`) and Director AI/ML Anitha Rajan (`anitha.rajan@acme.example`) for product-specific content.

## 2. Learning Objectives

By the end of this module, the engineer will be able to:

1. Map the ACME engineering organisation: business units, canonical repositories, owning teams, and primary tech stacks.
2. Explain trunk-based development, the ACME branch strategy, and the rules for PR merge including CODEOWNERS review.
3. Describe the CI/CD pipeline end-to-end: trigger → build → unit/integration tests → security scans → artifact publish → deploy.
4. Locate the three canonical environments (development, staging, production) and the rules for promoting changes between them.
5. Identify the observability stack (logs, metrics, traces, dashboards, alerts) and the runbook pattern for on-call incidents.
6. Recall the ACME release management cadence, versioning scheme, and rollback procedure.

## 3. Target Audience

| Role | Required? | Notes |
|---|---|---|
| Backend, Frontend, Full-stack engineers | **Mandatory** | Gates repository write access. |
| Cloud Platform Engineers, DevOps engineers | **Mandatory** | Plus mandatory [`cloud-platform-fundamentals.md`](./cloud-platform-fundamentals.md) (ACME-TRN-007). |
| AI/ML Engineers, AI Research Engineers | **Mandatory** | Plus product training for ACME Intelligence. |
| Quality Engineers | **Mandatory** | Special focus on test strategy and `acme-quality-automation`. |
| Customer Support Engineers | **Mandatory** | Special focus on incident response and observability. |
| Engineering Managers / Tech Leads | **Mandatory** | Plus the manager supplement (delivered separately). |
| Non-engineers (PM, HR, Sales) | Optional | A 90-minute "engineering culture for non-engineers" is offered. |

## 4. Prerequisites

- Completion of [`security-awareness.md`](./security-awareness.md) (ACME-TRN-002) — gating.
- Completion of [`privacy-awareness.md`](./privacy-awareness.md) (ACME-TRN-003) — gating for any customer-data access.
- Developer workstation setup complete — see [`../04-engineering/developer-workstation-setup.md`](../04-engineering/developer-workstation-setup.md).
- Source code & repository access request submitted — see [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md).

## 5. Duration

**Total: 6 hours**, all self-paced in `wiki.acme.example` with a 30-minute live welcome by Aditi Ghosh.

| Block | Duration | Modality |
|---|---|---|
| Live welcome & engineering culture | 30 min | Instructor-led (recorded) |
| Engineering org & repository catalogue | 60 min | Self-paced |
| Branching & PRs | 60 min | Self-paced |
| CI/CD overview | 45 min | Self-paced |
| Testing & debugging | 60 min | Self-paced |
| Environments & release management | 45 min | Self-paced |
| Incident response & on-call introduction | 45 min | Self-paced |
| Knowledge check (20 questions) | 15 min | Self-paced |

## 6. Outline of Topics Covered

### Block A — Welcome & Engineering Culture (Instructor-led, 30 min)

- Engineering at ACME: mission, principles, decision-making norms.
- The "build for the next decade" mindset.
- On-call as a first-class engineering activity.
- Who's who: Aditi Ghosh (Engineering Enablement + Cloud API lead), Anitha Rajan (AI/ML), Sridhar Venkatesh (CTO).

### Block B — Engineering Org & Repository Catalogue (60 min)

- Engineering organisation structure — see [`../00-company/organizational-structure.md`](../00-company/organizational-structure.md).
- Repository catalogue — see [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md).
- The ten canonical repositories: `acme-cloud-api`, `acme-cloud-frontend`, `acme-intelligence-agents`, `acme-intelligence-inference`, `acme-intelligence-ml`, `acme-workspace-web`, `acme-workspace-api`, `acme-platform-infrastructure`, `acme-shared-libraries`, `acme-quality-automation` — all on `git.acme.example` (fictional).
- Per-repo deep dives in [`../04-engineering/repositories/`](../04-engineering/repositories/).

### Block C — Branching & Pull Requests (60 min)

- Trunk-based development at ACME.
- Branch strategy — see [`../04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md).
- Pull requests and code review — see [`../04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md).
- Commit message conventions — see [`../04-engineering/practices/commit-message-conventions.md`](../04-engineering/practices/commit-message-conventions.md).
- Coding standards — see [`../04-engineering/practices/coding-standards.md`](../04-engineering/practices/coding-standards.md).

### Block D — CI/CD Overview (45 min)

- The ACME CI/CD pipeline — see [`../04-engineering/practices/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md).
- Build artifacts, internal package registry (`packages.acme.example`), and internal package management — see [`../04-engineering/practices/internal-package-management.md`](../04-engineering/practices/internal-package-management.md).
- Security scans, license checks, SAST, dependency review.

### Block E — Testing & Debugging (60 min)

- Unit and integration testing philosophy — see [`../04-engineering/practices/unit-and-integration-testing.md`](../04-engineering/practices/unit-and-integration-testing.md).
- Quality engineering and `acme-quality-automation`.
- Debugging practices — see [`../04-engineering/practices/debugging.md`](../04-engineering/practices/debugging.md).

### Block F — Environments & Release Management (45 min)

- Development, staging, production — see [`../04-engineering/practices/development-staging-production.md`](../04-engineering/practices/development-staging-production.md).
- Release management — see [`../04-engineering/practices/release-management.md`](../04-engineering/practices/release-management.md).
- Observability & logging — see [`../04-engineering/practices/observability-and-logging.md`](../04-engineering/practices/observability-and-logging.md).

### Block G — Incident Response & On-Call (45 min)

- Incident response and on-call introduction — see [`../04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md).
- Severity definitions, pager rotation, post-incident review (PIR) process.
- Status page (`status.acme.example`) ownership and updates during incidents.

### Block H — Knowledge Check (15 min)

- 20-question quiz across all blocks; passing threshold 80%.

## 7. Format

**Mixed.** Self-paced content dominates (5.5 hours) with a 30-minute live welcome hosted by Aditi Ghosh on the second Wednesday of each month. The live session is recorded and posted within two business days for off-cycle hires.

## 8. Completion Criteria

- All seven content blocks marked `COMPLETED` in the LMS.
- Knowledge-check quiz score **≥ 80%** (≥ 16 of 20 correct). Retakes are unlimited but logged.
- Acknowledgement of source code security — see [`../03-security/source-code-security.md`](../03-security/source-code-security.md) — and secrets management — see [`../03-security/secrets-management.md`](../03-security/secrets-management.md) — recorded via [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md).
- [`../08-forms/training-completion.md`](../08-forms/training-completion.md) submitted and signed off by Engineering Enablement.

## 9. Follow-up / Next Steps

- Proceed to [`git-and-repository-workflows.md`](./git-and-repository-workflows.md) (ACME-TRN-005) — hands-on lab gates first real PR.
- For Copilot-licensed engineers: proceed to [`ai-coding-assistant-usage.md`](./ai-coding-assistant-usage.md) (ACME-TRN-006).
- For Platform Infrastructure, Cloud API, and Workspace API engineers: proceed to [`cloud-platform-fundamentals.md`](./cloud-platform-fundamentals.md) (ACME-TRN-007).
- For product-specific deep dives: [`product-training.md`](./product-training.md) (ACME-TRN-008).
- On-call shadowing rotation is scheduled after the first 60 days — see [`../07-workflows/first-60-days.md`](../07-workflows/first-60-days.md) and [`../07-workflows/first-90-days.md`](../07-workflows/first-90-days.md).

## 10. Trainer / Owner

| Role | Person | Responsibility |
|---|---|---|
| Module owner | Aditi Ghosh, Engineering Enablement lead (`aditi.ghosh@acme.example`) | Content strategy, live welcome, annual review. |
| Executive sponsor | Sridhar Venkatesh, VP Engineering / CTO (`sridhar.venkatesh@acme.example`) | Sponsorship, escalations. |
| AI/ML content co-owner | Anitha Rajan, Director AI/ML (`anitha.rajan@acme.example`) | Intelligence-track content review. |
| Delivery coordinator | Anjali Iyer, Training Operations (`anjali.iyer@acme.example`) | LMS tracking, sign-off. |

Escalation contacts are in [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md). Glossary terms are in [`../metadata/glossary.md`](../metadata/glossary.md).
