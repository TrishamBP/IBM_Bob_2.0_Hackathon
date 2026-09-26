---
document_id: ACME-COMP-002
title: ACME Corp Company Profile
category: company
department: all
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [company, profile, factsheet]
---

# ACME Corp Company Profile

This document is the **canonical reference** for ACME Corp facts. Every other document in this library refers back to this profile for company-level details. If you are writing or updating another document, do not invent a different company profile — link here.

## Company Snapshot

| Attribute | Value |
|-----------|-------|
| Legal name (fictional) | ACME Corporation Pvt. Ltd. |
| Trade name | ACME Corp |
| Industry | Enterprise software, cloud computing, AI and developer tools |
| Headquarters | ACME Tower, Hitec City, Hyderabad, Telangana 500081, India |
| Other offices | Bengaluru (India), London (United Kingdom), Seattle (United States) |
| Founded (fictional) | 2014 |
| Employees (approx.) | 3,500 |
| Working model | Hybrid (in-office locations) and remote |
| Primary technology environment | Microsoft-oriented enterprise |
| Trading status (fictional) | Privately held |
| Domain (fictional) | acme.example |
| Source control host (fictional) | git.acme.example |
| Internal portal (fictional) | portal.acme.example |

> All identifiers above are fictional. They exist solely to make this knowledge base internally consistent.

## Products

ACME develops three products. Each product is owned by a dedicated business unit but supported by shared platform, security, and quality engineering teams.

| Product | Description | Primary Owner |
|---------|-------------|---------------|
| ACME Cloud | Enterprise cloud management platform | Cloud Business Unit |
| ACME Intelligence | AI agents and enterprise AI platform | Intelligence Business Unit |
| ACME Workspace | Enterprise productivity and collaboration software | Workspace Business Unit |

For full product details, see [`06-product/product-catalog.md`](../06-product/product-catalog.md).

## Departments

ACME has 13 departments. Each is led by a fictional leader named in [`00-company/organizational-structure.md`](./organizational-structure.md).

| # | Department | Function |
|---|------------|----------|
| 1 | Human Resources | People operations, payroll, benefits, employee relations |
| 2 | IT Operations | Endpoint, identity, network, productivity tooling, helpdesk |
| 3 | Information Security | Security policy, IAM, SOC, GRC, application security |
| 4 | Software Engineering | Cloud, Workspace, and shared libraries engineering |
| 5 | AI and Machine Learning | Intelligence agents, inference, ML platform |
| 6 | Cloud Platform and DevOps | Shared platform, CI/CD, observability, release |
| 7 | Product Management | Product strategy, roadmaps, requirements |
| 8 | UX and Design | Visual design, research, design systems |
| 9 | Quality Engineering | Test automation, release validation, performance |
| 10 | Sales | Direct sales, partner sales, sales engineering |
| 11 | Customer Support | Tier 1–3 support, customer success |
| 12 | Finance | Accounting, FP&A, procurement, tax |
| 13 | Legal and Compliance | Contracts, privacy, regulatory compliance |

## Office Locations

| Office | Address (fictional) | Approx. Headcount | Time Zone |
|--------|---------------------|-------------------|-----------|
| Hyderabad (HQ) | ACME Tower, Hitec City, Hyderabad, Telangana 500081, India | 1,400 | IST (UTC+05:30) |
| Bengaluru | ACME Tech Park, Outer Ring Road, Bengaluru, Karnataka 560103, India | 900 | IST (UTC+05:30) |
| London | ACME House, 120 Bishopsgate, London EC2N 4AG, United Kingdom | 450 | GMT/BST (UTC+00:00 / UTC+01:00) |
| Seattle | ACME Westlake, 400 Westlake Ave N, Seattle, WA 98109, United States | 750 | PT (UTC−08:00 / UTC−07:00 DST) |

See [`00-company/office-locations-and-working-arrangements.md`](./office-locations-and-working-arrangements.md) for full office details, in-office expectations, and remote-work eligibility.

## Working Model

- **Hybrid:** Employees assigned to an office are expected in-office a minimum of two days per week, with manager flexibility.
- **Remote:** Employees outside commuting distance of any office may be fully remote.
- **Time zones:** Core collaboration hours are 09:00–14:00 IST and 09:00–14:00 PT, with cross-region overlap between 18:00–21:00 IST and 05:30–08:30 PT for live cross-region meetings.
- The full policy is [`01-hr/remote-and-hybrid-working-policy.md`](../01-hr/remote-and-hybrid-working-policy.md).

## Primary Technology Environment

ACME operates a Microsoft-oriented enterprise stack. Standard productivity and identity tooling includes:

- **Microsoft 365 (M365)** — Exchange Online, SharePoint Online, OneDrive for Business, Microsoft Teams.
- **Microsoft Entra ID** (formerly Azure AD) — corporate identity provider, SSO.
- **Microsoft Intune** — endpoint management for Windows 11 and macOS devices.
- **Microsoft Defender for Endpoint** — endpoint detection and response.
- **Microsoft Authenticator** — MFA for all corporate accounts.
- **Microsoft Purview** — data classification and DLP.

Engineering, AI, and cloud-platform teams additionally use GitHub Enterprise, internal Kubernetes clusters, Python/Node toolchains, Docker, and internal observability stacks. Engineering tooling is documented in [`04-engineering/`](../04-engineering/).

## Internal Systems (Fictional)

| System | Purpose | URL (fictional) |
|--------|---------|-----------------|
| ACME Portal | Employee intranet | portal.acme.example |
| ACME IT Helpdesk | Ticketing | helpdesk.acme.example |
| ACME HR Hub | HR self-service | hr.acme.example |
| ACME Wiki | Knowledge base | wiki.acme.example |
| ACME Vault | Internal secrets and credentials | vault.acme.example |
| ACME Package | Internal package registry | packages.acme.example |
| ACME Status | Status pages | status.acme.example |
| git.acme.example | GitHub Enterprise | git.acme.example |

These systems are fictional. No endpoint listed here is reachable.

## Related Documents

- [`00-company/organizational-structure.md`](./organizational-structure.md)
- [`00-company/office-locations-and-working-arrangements.md`](./office-locations-and-working-arrangements.md)
- [`00-company/products-and-business-units.md`](./products-and-business-units.md)
- [`06-product/product-catalog.md`](../06-product/product-catalog.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- [`metadata/glossary.md`](../metadata/glossary.md)
