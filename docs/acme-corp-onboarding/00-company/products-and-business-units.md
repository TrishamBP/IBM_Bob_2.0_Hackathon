---
document_id: ACME-COMP-004
title: ACME Corp Products and Business Units
category: company
department: all
applicable_roles: [all]
owner: Product Management
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [products, business-units, overview]
---

# ACME Corp Products and Business Units

This document summarizes ACME's three products and the business units that own them. Deep-dive product overviews live in [`06-product/`](../06-product/).

## Product Catalog

| Product | BU | Primary Customers | Stage | Owner |
|---------|----|-------------------|-------|-------|
| ACME Cloud | Cloud Business Unit | Enterprises running multi-cloud estates | GA | Maheshwari Krishnan (Product Lead) |
| ACME Intelligence | Intelligence Business Unit | Regulated-industry enterprises deploying AI agents and inference | GA | Omar Farouk (Product Lead) |
| ACME Workspace | Workspace Business Unit | Enterprises seeking productivity and collaboration software | GA | Elena Petrova (Product Lead) |

## ACME Cloud

ACME Cloud is a multi-cloud management platform. Customers connect their AWS, Azure, and GCP accounts; ACME Cloud provides a unified control plane for provisioning, governance, cost management, and observability. The product is sold via direct sales and partner channels, with a tiered pricing model based on connected cloud spend.

- **Engineering owners:** Sridhar Venkatesh (VP Engineering, Cloud), Anjali Desai (EM, Cloud API), Manoj Pillai (EM, Cloud Frontend).
- **Repositories:** `acme-cloud-api`, `acme-cloud-frontend`. See [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md).
- **Deep dive:** [`06-product/acme-cloud-overview.md`](../06-product/acme-cloud-overview.md).

## ACME Intelligence

ACME Intelligence is an enterprise AI platform. It lets customers deploy AI agents, run model inference inside their own tenancy, and use retrieval-augmented generation against their own corpora with policy guardrails. The product is targeted at regulated industries — financial services, healthcare, public sector.

- **Engineering owners:** Anitha Rajan (Director AI/ML), Rohan Bhat (EM, Intelligence Agents), Vivek Anand (EM, Intelligence Inference), Lakshmi Narayan (EM, Intelligence ML).
- **Repositories:** `acme-intelligence-agents`, `acme-intelligence-inference`, `acme-intelligence-ml`. See catalog.
- **Deep dive:** [`06-product/acme-intelligence-overview.md`](../06-product/acme-intelligence-overview.md).

## ACME Workspace

ACME Workspace is a productivity and collaboration suite. It combines documents, spreadsheets, video meetings, and project tracking in a single application. Workspace is sold per-seat to enterprises, with discounts for the Indian and Southeast Asian markets.

- **Engineering owners:** Sridhar Venkatesh (VP Engineering, Cloud, also oversees Workspace engineering), Thomas Buckley (EM, Workspace Web), Priya Menon (EM, Workspace API).
- **Repositories:** `acme-workspace-web`, `acme-workspace-api`. See catalog.
- **Deep dive:** [`06-product/acme-workspace-overview.md`](../06-product/acme-workspace-overview.md).

## Shared Engineering

In addition to product-specific BUs, ACME operates shared engineering functions:

| Team | Lead | Function |
|------|------|----------|
| Cloud Platform and DevOps | Nikhil Joshi | Shared platform, CI/CD, observability |
| Quality Engineering | Asha Reddy | Test automation, release validation |
| Shared Libraries | (managed within Platform team) | Cross-product libraries |

Shared repositories: `acme-platform-infrastructure`, `acme-shared-libraries`, `acme-quality-automation`. See [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md).

## Related Documents

- [`00-company/company-profile.md`](./company-profile.md)
- [`00-company/organizational-structure.md`](./organizational-structure.md)
- [`06-product/product-catalog.md`](../06-product/product-catalog.md)
- [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
