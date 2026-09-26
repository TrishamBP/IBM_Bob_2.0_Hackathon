---
document_id: ACME-PROD-002
title: ACME Cloud Product Overview
category: product
department: cloud-bu
applicable_roles: [all]
owner: Product Management
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [product, cloud, overview]
---

# ACME Cloud Product Overview

ACME Cloud is the company's enterprise multi-cloud management platform. It is the largest of ACME's three products by revenue (in this fictional universe) and the one most engineering employees will encounter first.

## Business Purpose

Customers use ACME Cloud to manage their AWS, Azure, and GCP accounts from a single control plane. The platform handles provisioning, governance, cost management, and observability. The promise to customers: a single pane of glass for multi-cloud, with the audit and compliance rigor required by regulated industries.

## Intended Users

- **Cloud architects** — design landing zones, define governance policies.
- **Platform engineers** — provision infrastructure, manage IaC pipelines.
- **FinOps practitioners** — track cloud spend, allocate costs, identify savings.
- **Security and compliance officers** — audit access, generate compliance reports.
- **Engineering leadership** — observe SLOs, cost-per-service, governance posture.

## Major Capabilities

| Capability | Description |
|------------|-------------|
| Landing zones | Pre-architected, configurable multi-account structures for AWS, Azure, GCP. |
| Governance | Policy-as-code enforcement (guardrails) on every provisioning action. |
| Provisioning | Self-service catalog backed by Terraform and Bicep modules. |
| Cost management | Real-time spend visibility, anomaly detection, budget alerts, chargeback. |
| Observability | Unified metrics, logs, and traces across connected clouds. |
| Compliance reporting | Pre-built reports for SOC 2, ISO 27001, PCI DSS, HIPAA, FedRAMP. |
| Anomaly & threat detection | Detection of unusual cloud control-plane activity. |

## System Components

The fictional ACME Cloud architecture has these logical components:

| Component | Description | Owning Repository |
|-----------|-------------|-------------------|
| Cloud API | Multi-tenant API server, gRPC + REST, OpenAPI 3.1 spec | `acme-cloud-api` |
| Cloud Frontend | Single-page React application, customer-facing console | `acme-cloud-frontend` |
| Connectors | Per-cloud adapter services (AWS, Azure, GCP) | `acme-cloud-api` (subpackages) |
| Governance engine | Policy evaluation service | `acme-cloud-api` |
| FinOps service | Spend aggregation, anomaly detection | `acme-cloud-api` |
| Observability collector | Telemetry ingestion from connected clouds | `acme-platform-infrastructure` |
| Identity broker | Maps ACME identity to cloud-provider roles | `acme-cloud-api` |

## Owning Teams

- **Product:** Maheshwari Krishnan (Product Lead), reporting to Daniel Coelho (CPO).
- **Engineering (Cloud API):** Anjali Desai (EM), reporting to Sridhar Venkatesh (CTO).
- **Engineering (Cloud Frontend):** Manoj Pillai (EM), reporting to Sridhar Venkatesh (CTO).
- **Platform (shared):** Nikhil Joshi (Manager), reporting to Sridhar Venkatesh.
- **Quality Engineering:** Asha Reddy (Manager).
- **Design:** Sara Lindberg's UX team.

See [`00-company/organizational-structure.md`](../00-company/organizational-structure.md) for full names and [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for contacts.

## How Your Work Connects

- If you are joining the **Cloud API** team, you will work on the multi-tenant control plane — the API that customers call and that internal services depend on. Most of your work will be in `acme-cloud-api`.
- If you are joining **Cloud Frontend**, you will work on the customer-facing console. Most of your work will be in `acme-cloud-frontend`.
- If you are joining **Platform Infrastructure**, your work crosses all products — you build the foundation ACME Cloud, ACME Intelligence, and ACME Workspace all sit on. Most of your work will be in `acme-platform-infrastructure`.

## Customer-Facing URLs (Fictional)

| Surface | URL (fictional) |
|---------|-----------------|
| Cloud console | cloud.acme.example |
| Cloud status | status.acme.example/cloud |
| Cloud docs | docs.acme.example/cloud |
| Cloud API | api.cloud.acme.example |

## Related Documents

- [`06-product/product-catalog.md`](./product-catalog.md)
- [`06-product/acme-intelligence-overview.md`](./acme-intelligence-overview.md)
- [`06-product/acme-workspace-overview.md`](./acme-workspace-overview.md)
- [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md)
- [`00-company/products-and-business-units.md`](../00-company/products-and-business-units.md)
