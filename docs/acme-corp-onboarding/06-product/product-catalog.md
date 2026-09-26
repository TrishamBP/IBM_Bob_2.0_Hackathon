---
document_id: ACME-PROD-001
title: ACME Corp Product Catalog
category: product
department: all
applicable_roles: [all]
owner: Product Management
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [products, catalog, canonical]
---

# ACME Corp Product Catalog

This is the **canonical product catalog** for ACME Corp. All product names, customer names, and pricing references are fictional. For per-product deep dives, follow the links in the table below.

## Catalog

| Product | Description | Lifecycle Stage | Owner | Deep Dive |
|---------|-------------|------------------|-------|-----------|
| ACME Cloud | Enterprise multi-cloud management platform | GA | Maheshwari Krishnan (Product Lead) | [`acme-cloud-overview.md`](./acme-cloud-overview.md) |
| ACME Intelligence | Enterprise AI agents and inference platform | GA | Omar Farouk (Product Lead) | [`acme-intelligence-overview.md`](./acme-intelligence-overview.md) |
| ACME Workspace | Enterprise productivity and collaboration suite | GA | Elena Petrova (Product Lead) | [`acme-workspace-overview.md`](./acme-workspace-overview.md) |

## Pricing Tiers (Fictional)

| Product | Tier | Indicative Price | Notes |
|---------|------|------------------|-------|
| ACME Cloud | Starter | 2% of managed cloud spend | Up to $50K/month managed spend |
| ACME Cloud | Business | 1.5% of managed cloud spend + $5K/mo platform fee | Up to $500K/month managed spend |
| ACME Cloud | Enterprise | Custom, volume-based | >$500K/month managed spend |
| ACME Intelligence | Starter | $2,500/mo per 1M tokens inference | Up to 10M tokens/month |
| ACME Intelligence | Business | $8,000/mo per 1M tokens + dedicated inference capacity | Up to 100M tokens/month |
| ACME Intelligence | Enterprise | Custom | Dedicated tenancy |
| ACME Workspace | Starter | $6/user/month | Up to 50 users |
| ACME Workspace | Business | $10/user/month | Up to 5,000 users |
| ACME Workspace | Enterprise | Custom, volume-based | >5,000 users |

Pricing is fictional. Sales representatives should refer to the latest fictional price book in Salesforce before quoting any customer.

## Customer Segments

ACME targets enterprises in the following (fictional) segments:

- Financial services (banking, insurance, asset management)
- Healthcare (providers, payers, life sciences)
- Public sector (national and regional government bodies)
- Telecommunications and media
- Manufacturing and industrial
- Retail and consumer goods

Sample fictional customers (do not assume these are real):

- Northwind Bank (financial services)
- Contoso Health (healthcare)
- Tailspin Telecom (telecommunications)
- Fabrikam Manufacturing (manufacturing)
- Adventure Works Retail (retail)

## Repositories by Product

See [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md) for the canonical mapping of repositories to products.

| Product | Repositories |
|---------|-------------|
| ACME Cloud | `acme-cloud-api`, `acme-cloud-frontend` |
| ACME Intelligence | `acme-intelligence-agents`, `acme-intelligence-inference`, `acme-intelligence-ml` |
| ACME Workspace | `acme-workspace-web`, `acme-workspace-api` |
| Shared | `acme-platform-infrastructure`, `acme-shared-libraries`, `acme-quality-automation` |

## Roadmap Cadence

- **Quarterly planning:** Each BU publishes a quarterly plan, aligned with the company-wide OKR cycle.
- **Monthly release:** Each product ships at least one minor release per month.
- **Patch releases:** As needed for security or critical defects.
- **Major releases:** Twice per year per product, with a 3-month customer preview.

## Related Documents

- [`00-company/products-and-business-units.md`](../00-company/products-and-business-units.md)
- [`00-company/company-profile.md`](../00-company/company-profile.md)
- [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
