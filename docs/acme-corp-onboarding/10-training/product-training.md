---
document_id: ACME-TRN-008
title: Product Training
category: training
department: product
applicable_roles: [all]
owner: Product Management
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [training, product, acme-cloud, acme-intelligence, acme-workspace]
---

# Product Training (ACME-TRN-008)

> Fictional document. All systems, links, and addresses are illustrative.

## 1. Module Overview

The Product Training module covers the three ACME Corp products: ACME Cloud (multi-cloud management platform), ACME Intelligence (enterprise AI platform — agents, inference, ML), and ACME Workspace (productivity and collaboration suite). All employees complete a 2-hour product overview covering all three products. Engineers and product-facing roles additionally complete a 4-hour product-specific deep dive for the product their team ships.

The module is owned by Product Management and coordinated by Anjali Iyer (Training Operations, `anjali.iyer@acme.example`) in partnership with the product business-unit leads: the ACME Cloud lead under the CTO office (Sridhar Venkatesh), the ACME Intelligence lead under Director AI/ML Anitha Rajan (`anitha.rajan@acme.example`), and the ACME Workspace lead under the CTO office.

## 2. Learning Objectives

By the end of the overview, every learner will be able to:

1. Describe each ACME product in one sentence, name the primary buyer, and identify the canonical repository(s).
2. Articulate the value proposition and the top three differentiators of each product.
3. Identify the leadership, business unit, and HRBP for each product.

By the end of the product-specific deep dive, the engineer will additionally be able to:

4. Describe the architecture of their assigned product, including its primary components and key interfaces.
5. Locate the canonical repositories for the product, set up a local dev environment, and run the build and tests.
6. Identify the customer-facing surfaces (UI, API, SDK, agents) and the support model for each.

## 3. Target Audience

| Role | Overview (2h) | Deep Dive (4h) | Notes |
|---|---|---|---|
| All employees | **Mandatory** | — | Overview gates HR sign-off. |
| Cloud API engineers | Mandatory | **Mandatory** — ACME Cloud | Deep dive gates production deploy. |
| Cloud Frontend engineers | Mandatory | **Mandatory** — ACME Cloud | Deep dive gates production deploy. |
| Intelligence (agents/inference/ML) engineers | Mandatory | **Mandatory** — ACME Intelligence | Deep dive gates production deploy. |
| Workspace Web engineers | Mandatory | **Mandatory** — ACME Workspace | Deep dive gates production deploy. |
| Workspace API engineers | Mandatory | **Mandatory** — ACME Workspace | Deep dive gates production deploy. |
| Platform Infrastructure engineers | Mandatory | Optional | Optional because the platform spans all three products. |
| Quality Engineers | Mandatory | **Mandatory** — their assigned product | |
| Customer Support Engineers | Mandatory | **Mandatory** — their assigned product | Support-focused deep dive variant. |
| Product Managers, Sales, HR, Finance | Mandatory | Recommended | |

## 4. Prerequisites

- Completion of [`company-orientation.md`](./company-orientation.md) (ACME-TRN-001).
- Completion of [`security-awareness.md`](./security-awareness.md) (ACME-TRN-002) for engineers.
- For deep dives: completion of [`engineering-orientation.md`](./engineering-orientation.md) (ACME-TRN-004) and [`git-and-repository-workflows.md`](./git-and-repository-workflows.md) (ACME-TRN-005).
- Product overview documents: [`../06-product/acme-cloud-overview.md`](../06-product/acme-cloud-overview.md), [`../06-product/acme-intelligence-overview.md`](../06-product/acme-intelligence-overview.md), [`../06-product/acme-workspace-overview.md`](../06-product/acme-workspace-overview.md).

## 5. Duration

| Block | Audience | Duration | Modality |
|---|---|---|---|
| Product overview (all three products) | All | 120 min | Self-paced + 30-min live demo |
| ACME Cloud deep dive | Cloud engineers, QE, Support | 240 min | Mixed (self-paced + hands-on) |
| ACME Intelligence deep dive | Intelligence engineers, QE, Support | 240 min | Mixed (self-paced + hands-on) |
| ACME Workspace deep dive | Workspace engineers, QE, Support | 240 min | Mixed (self-paced + hands-on) |

## 6. Outline of Topics Covered

### Block O — Product Overview (All employees, 2 hours)

- ACME Cloud: multi-cloud management platform; primary buyer = enterprise IT / platform engineering.
  - Reference: [`../06-product/acme-cloud-overview.md`](../06-product/acme-cloud-overview.md).
  - Repositories: `acme-cloud-api`, `acme-cloud-frontend`.
- ACME Intelligence: enterprise AI platform (agents, inference, ML); primary buyer = enterprise AI / data leadership.
  - Reference: [`../06-product/acme-intelligence-overview.md`](../06-product/acme-intelligence-overview.md).
  - Repositories: `acme-intelligence-agents`, `acme-intelligence-inference`, `acme-intelligence-ml`.
- ACME Workspace: productivity and collaboration suite; primary buyer = CIO / IT / workplace.
  - Reference: [`../06-product/acme-workspace-overview.md`](../06-product/acme-workspace-overview.md).
  - Repositories: `acme-workspace-web`, `acme-workspace-api`.
- Leadership and HRBP mapping — see [`../00-company/organizational-structure.md`](../00-company/organizational-structure.md):
  - Cloud/Workspace HRBP: Kavya Krishnan.
  - Intelligence/QE/Support HRBP: Deepika Rao.
  - Platform/Sales HRBP: Sanjay Patel.
- Live demo: 30-minute walkthrough of each product (recorded).

### Block C — ACME Cloud Deep Dive (4 hours)

- Architecture: cloud connectors, resource graph, policy engine, cost telemetry, RBAC layer.
- Repositories: `acme-cloud-api` (see [`../04-engineering/repositories/acme-cloud-api.md`](../04-engineering/repositories/acme-cloud-api.md)), `acme-cloud-frontend` (see [`../04-engineering/repositories/acme-cloud-frontend.md`](../04-engineering/repositories/acme-cloud-frontend.md)).
- Local dev setup: prerequisites, build, run, test.
- Customer-facing surfaces: REST API, GraphQL API, web UI, Terraform provider.
- Support model: customer support engineers on the Cloud pod; escalation to Cloud API on-call.
- Cross-reference: [`../04-engineering/practices/development-staging-production.md`](../04-engineering/practices/development-staging-production.md).

### Block I — ACME Intelligence Deep Dive (4 hours)

- Architecture: agent runtime, inference gateway, ML training and serving pipelines, evaluation harness, guardrails.
- Repositories: `acme-intelligence-agents` (see [`../04-engineering/repositories/acme-intelligence-agents.md`](../04-engineering/repositories/acme-intelligence-agents.md)), `acme-intelligence-inference` (see [`../04-engineering/repositories/acme-intelligence-inference.md`](../04-engineering/repositories/acme-intelligence-inference.md)), `acme-intelligence-ml` (see [`../04-engineering/repositories/acme-intelligence-ml.md`](../04-engineering/repositories/acme-intelligence-ml.md)).
- Local dev setup: prerequisites, model artifacts, evaluation runs.
- Customer-facing surfaces: agent SDK, inference REST API, model registry API.
- AI governance: every customer-facing agent is reviewed by the AI/ML Director's office (Anitha Rajan) — see [`../03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md).
- Support model: customer support engineers on the Intelligence pod; escalation to Intelligence on-call.

### Block W — ACME Workspace Deep Dive (4 hours)

- Architecture: real-time collaboration service, document store, identity bridge, calendar, mail bridge.
- Repositories: `acme-workspace-web` (see [`../04-engineering/repositories/acme-workspace-web.md`](../04-engineering/repositories/acme-workspace-web.md)), `acme-workspace-api` (see [`../04-engineering/repositories/acme-workspace-api.md`](../04-engineering/repositories/acme-workspace-api.md)).
- Local dev setup: prerequisites, build, run, test.
- Customer-facing surfaces: web app, REST API, calendar/mail integration endpoints.
- Support model: customer support engineers on the Workspace pod; escalation to Workspace API on-call.
- Cross-reference: [`../04-engineering/practices/observability-and-logging.md`](../04-engineering/practices/observability-and-logging.md).

## 7. Format

**Mixed.** The overview is self-paced plus a 30-minute live demo (recorded). Each deep dive is self-paced (3 hours) plus a 1-hour hands-on lab (build + run + a small change). Deep-dive labs are graded pass/fail by a senior engineer from the product team.

## 8. Completion Criteria

### Overview

- All three product overview blocks marked `COMPLETED` in the LMS.
- 10-question quiz (≥ 80%) covering all three products.
- [`../08-forms/training-completion.md`](../08-forms/training-completion.md) submitted and signed off by Training Operations.

### Deep Dive

- All four deep-dive blocks for the assigned product marked `COMPLETED`.
- Hands-on lab: local build green; a small change made and tested; mentor sign-off.
- 10-question deep-dive quiz (≥ 80%).
- [`../08-forms/training-completion.md`](../08-forms/training-completion.md) submitted and signed off by Engineering Enablement.

## 9. Follow-up / Next Steps

- Overview completion unlocks the product-specific deep dive for engineers.
- Deep-dive completion unlocks production deploy permissions via [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md).
- Cross-product electives (e.g., "ACME Cloud for Workspace engineers") are offered quarterly.
- Annual refresher: 60-minute product changes briefing per product the engineer works on.

## 10. Trainer / Owner

| Role | Person | Responsibility |
|---|---|---|
| Module owner | Product Management (under CTO office) | Content strategy, annual review. |
| ACME Cloud deep dive owner | ACME Cloud business-unit lead (under Sridhar Venkatesh) | Cloud content, lab grading. |
| ACME Intelligence deep dive owner | Anitha Rajan, Director AI/ML (`anitha.rajan@acme.example`) | Intelligence content, AI governance. |
| ACME Workspace deep dive owner | ACME Workspace business-unit lead (under CTO office) | Workspace content, lab grading. |
| LMS coordinator | Anjali Iyer, Training Operations (`anjali.iyer@acme.example`) | Tracking, sign-off. |

Escalation contacts are in [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md). Glossary terms are in [`../metadata/glossary.md`](../metadata/glossary.md).
