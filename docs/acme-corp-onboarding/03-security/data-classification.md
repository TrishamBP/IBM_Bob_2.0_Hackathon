---
document_id: ACME-SEC-003
title: Data Classification
category: security
department: information-security
applicable_roles: [all]
owner: Neha Saxena, Security Director
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, data, classification, handling, fictional]
---

# Data Classification

> ACME Corp fictional onboarding library. Hostnames and mailboxes shown are fictional. Customer data referenced is illustrative; no real customer records are used.

## 1. Purpose

This document defines ACME Corp's five-tier data classification scheme and the handling rules that apply to each tier. Classification is the foundation of every other security control at ACME — it tells you how sensitive a piece of information is, who may see it, where it may live, and what to do when it leaks. Read this document first if you are unsure where some data may be stored or shared.

## 2. Scope

This scheme applies to all data ACME creates, receives, processes, stores, or transmits, in any form — electronic, printed, spoken, or otherwise. It applies regardless of location: corporate laptop, BYOD device, cloud service, on-prem server, paper notebook, or chat message. It applies to:

- Employee data (HR records, payroll, performance).
- Customer data (telemetry, configurations, support tickets, customer source code).
- ACME intellectual property (product source code, designs, roadmaps).
- ACME operational data (logs, configs, secrets, runbooks).

## 3. The Five Tiers

ACME uses five tiers, in ascending order of sensitivity. The fifth tier — Customer Data — is a special category of Restricted that draws additional handling rules from [`customer-data-handling.md`](customer-data-handling.md).

| Tier | Definition | Examples | Default Sharing |
|------|------------|----------|------------------|
| **Public** | Approved for public release. | Product marketing pages, published API docs, public roadmap, press releases. | May be shared with anyone, anywhere, without restriction. |
| **Internal** | Default classification for business information. Safe to share within ACME. | Team meeting notes, internal wiki articles, org charts, department KPIs, internal newsletters. | All ACME workforce; no external sharing without manager approval. |
| **Confidential** | Sensitive business information. Access on need-to-know. | Unpublished financials, M&A documents, salary bands, security postmortems, customer contracts (under NDA). | Only named individuals with explicit need-to-know. Never external. |
| **Restricted** | Source code, secrets, regulated data, regulated infrastructure configurations. | Production credentials, customer PII fields, encryption keys, signing keys, security incident evidence. | Strictly need-to-know; every access logged. |
| **Customer Data** | Any data about or belonging to an ACME customer that ACME processes. Treated as Restricted by default with extra residency and erasure rules. | Customer's tenant configuration, customer's uploaded documents, customer's user activity, customer's support tickets. | Restricted plus customer-specific obligations — see [`customer-data-handling.md`](customer-data-handling.md). |

> Rule of thumb: **any customer data brought into ACME systems is Restricted by default** and inherits the rules of [`customer-data-handling.md`](customer-data-handling.md) on top of the Restricted rules below.

## 4. Handling Matrix

| Activity | Public | Internal | Confidential | Restricted | Customer Data |
|-----------|--------|----------|--------------|------------|---------------|
| Store on ACME-managed laptop | Allowed | Allowed | Allowed with disk encryption (see [`device-encryption.md`](device-encryption.md)) | Allowed only via managed app, never local | Only via managed app; never local |
| Store in ACME Microsoft 365 / SharePoint | Allowed | Allowed | Allowed in approved sites | Only in approved Restricted sites | Only in approved Customer Data sites |
| Send via corporate email | Allowed | Allowed | Internal recipients only | Only named recipients; encrypted | Only via approved CRM; encrypted |
| Share in Teams chat | Allowed | Allowed | Internal channel only | 1:1 with named individual; logged | Not in chat — use approved CRM |
| Store on personal cloud (Dropbox, personal OneDrive) | Allowed | Not allowed | Not allowed | Not allowed — violation of [`acceptable-use-policy.md`](acceptable-use-policy.md) | Not allowed — violation of [`customer-data-handling.md`](customer-data-handling.md) |
| Print | Allowed | Allowed | Allowed with shredder disposal (see [`clean-desk-policy.md`](clean-desk-policy.md)) | Not recommended; shred if printed | Not allowed |
| Enter into external AI tool | Allowed (public data) | Not allowed | Not allowed | Not allowed | Not allowed — see [`ai-tool-acceptable-use.md`](ai-tool-acceptable-use.md) |
| Enter into ACME Internal LLM sandbox | Allowed | Allowed | Allowed with redaction | Not allowed | Not allowed |
| Take home on USB | Allowed | Not allowed | Not allowed | Not allowed | Not allowed |
| Discuss in public (cafe, plane) | Allowed | Use discretion | Not allowed | Not allowed | Not allowed |

## 5. Labeling Requirements

Data must be labeled so that recipients understand its tier. Labeling rules:

- **Documents** (Word, Excel, PowerPoint, PDF): apply a Microsoft Purview sensitivity label. The label appears in the document header and is enforced by DLP.
- **Emails**: apply a Purview label in Outlook; the subject line is decorated with `[Internal]`, `[Confidential]`, `[Restricted]`, or `[Customer Data]`.
- **Source code repositories**: declare classification in `README.md` and in `CODEOWNERS` (see [`source-code-security.md`](source-code-security.md)). All ACME source code is **Confidential** unless explicitly labeled otherwise — customer-shared code is **Customer Data**.
- **Spreadsheets containing PII**: at minimum Restricted; treated as Customer Data if the PII belongs to a customer.
- **Chat messages**: rely on the channel's tier — do not paste higher-tier content into a lower-tier channel.

If you are unsure of the tier, treat it as the next-higher tier until you confirm with the data owner or the GRC Analyst (`Karthik Subramanian`).

## 6. Special Rules — Customer Data

Customer data is treated as Restricted by default and additionally:

- Must not leave the approved customer-data system (typically the customer's CRM tenant in ACME Workspace, or the production environment for the relevant product).
- Must not be copied to non-production environments without redaction or masking.
- Carries residency obligations — see [`customer-data-handling.md`](customer-data-handling.md).
- Triggers a 72-hour customer notification obligation if breached — see [`security-incident-reporting.md`](security-incident-reporting.md).
- Is subject to right-to-erasure requests processed by the GRC Analyst.

## 7. Responsibilities

| Role | Responsibility |
|------|----------------|
| **Data Owner** (typically the executive responsible for the function) | Classifies the data they own. Approves access requests for that data. |
| **Data Custodian** (IT/Engineering team operating the system) | Implements the technical controls matching the tier — encryption, logging, DLP. |
| **Every workforce member** | Labels the data they create. Handles data per its tier. Reports misclassification to `security-oncall@acme.example`. |
| **GRC Analyst** (`Karthik Subramanian`) | Maintains this scheme. Resolves ambiguity. Runs annual review of examples. |
| **Security Director** (`Neha Saxena`) | Approves new labels and exception requests. |

## 8. Enforcement

- Purview sensitivity labels are enforced in Microsoft 365 — you cannot send a Confidential email externally without a label being applied.
- DLP policies block pasting Customer Data into chat, external email, or unmanaged USB drives.
- Conditional access (see [`identity-and-access-management.md`](identity-and-access-management.md)) restricts which devices may access Confidential and Restricted SharePoint sites.
- Quarterly access reviews (see [`least-privilege-access.md`](least-privilege-access.md)) confirm that access lists still match need-to-know.

## 9. Exceptions

If a control prevents legitimate business activity, request an exception via `security-oncall@acme.example` (fictional). Exceptions are time-bound, compensating-controlled, and signed off by the Security Director (`Neha Saxena`) or the CISO (`Rajan Mehta`).

## 10. Examples (illustrative, not real)

- Public: the ACME Cloud public pricing page on `acme.example/pricing` (fictional).
- Internal: the Q3 engineering OKR sheet in the team's SharePoint site.
- Confidential: the unannounced acquisition term sheet stored in the CFO's Restricted site.
- Restricted: the production database connection string stored in ACME Vault at `vault.acme.example` (fictional).
- Customer Data: a customer's tenant configuration dump from ACME Cloud, stored in the approved customer-data site.

## 11. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`acceptable-use-policy.md`](acceptable-use-policy.md) — What you may and may not do.
- [`customer-data-handling.md`](customer-data-handling.md) — Special rules for the Customer Data tier.
- [`device-encryption.md`](device-encryption.md) — Encryption control for Confidential and Restricted data at rest.
- [`source-code-security.md`](source-code-security.md) — How source code is classified.
- [`ai-tool-acceptable-use.md`](ai-tool-acceptable-use.md) — What data may go into which AI tools.
- [`secrets-management.md`](secrets-management.md) — Restricted-tier credential handling.
- [`clean-desk-policy.md`](clean-desk-policy.md) — Paper and screen handling.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — GRC and Security Director contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — PII, DLP, sensitivity label definitions.
