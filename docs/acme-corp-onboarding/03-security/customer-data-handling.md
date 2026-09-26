---
document_id: ACME-SEC-018
title: Customer Data Handling
category: security
department: information-security
applicable_roles: [all]
owner: Karthik Subramanian, GRC Analyst
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, customer-data, data-residency, erasure, breach-notification, fictional]
---

# Customer Data Handling

> ACME Corp fictional onboarding library. Hostnames (`portal.acme.example`, `vault.acme.example`, `wiki.acme.example`) and mailboxes (`privacy@acme.example`, `security-incident@acme.example`) are fictional. Customer examples are illustrative; no real customer records are referenced.

## 1. Purpose

This document defines ACME Corp's policy for handling customer data — any data about or belonging to an ACME customer that ACME creates, receives, processes, stores, or transmits. Customer data is treated as Restricted by default per [`data-classification.md`](data-classification.md), and carries additional obligations: residency rules, no-copies-outside-approved-systems, access logging, right-to-erasure, and breach notification. A leak of customer data is the most damaging incident ACME can have — both for the customer and for ACME's business.

## 2. Scope

This applies to:

- All ACME workforce members, contractors, and authorized third parties who may access customer data.
- All ACME products that process customer data — ACME Cloud, ACME Intelligence, ACME Workspace.
- All systems that store customer data — production databases, customer-tenant SharePoint sites, support ticketing systems, log systems (where customer data appears).
- All forms of customer data — configurations, telemetry, support tickets, customer-uploaded documents, customer end-user personal data.

The contract with each customer may add obligations on top of this policy. Where the contract is more restrictive, the contract controls; where this policy is more restrictive, this policy controls.

## 3. Definition — What Is Customer Data

"Customer Data" means any data that:

- An ACME customer provides to ACME (e.g., a customer's tenant configuration for ACME Cloud).
- ACME generates about a customer's use of an ACME product (e.g., telemetry, audit logs).
- An ACME customer's end-users provide to ACME (e.g., support tickets).
- ACME obtains about a customer through the relationship (e.g., billing records, the customer's user directory synced for SSO).

Customer Data is **not**:

- ACME's own product source code, even when a customer is using the product (that is Confidential — see [`source-code-security.md`](source-code-security.md)).
- ACME's own internal financials or strategy (those are Confidential — see [`data-classification.md`](data-classification.md)).
- Public information about a customer (e.g., the customer's public website content) — though combining public information with internal data may still be Confidential.

When in doubt, treat it as Customer Data — the default is restrictive.

## 4. Customer Data Is Restricted — Default

Per [`data-classification.md`](data-classification.md), Customer Data is treated as Restricted by default. This means:

- Access on a strictly need-to-know basis.
- Every access logged.
- Stored only on systems approved for Restricted data.
- Encrypted at rest and in transit (see [`device-encryption.md`](device-encryption.md)).
- Never on BYOD phones — see [`byod-policy.md`](byod-policy.md) §3.
- Never on personal laptops — see [`byod-policy.md`](byod-policy.md) §4.
- Never entered into any AI tool — see [`ai-tool-acceptable-use.md`](ai-tool-acceptable-use.md) §4.
- Never on USB drives — see [`device-encryption.md`](device-encryption.md) §6.

## 5. Data Residency

Customer data has residency obligations. ACME operates production regions in:

| Region | Customer Data Residency |
|--------|--------------------------|
| India (Mumbai) | Customer data of customers contracted for India residency stays in the India region. |
| EU (Ireland + Netherlands) | Customer data of EU customers stays in the EU region per GDPR adequacy. |
| UK (London) | UK customer data stays in the UK region per UK GDPR. |
| US (Virginia + Oregon) | US customer data stays in the US region. |

Rules:

- A customer's data **must not** be replicated outside the contracted region for production use.
- Backups may be cross-region for disaster recovery, but only within the contracted residency boundary (e.g., EU customer's backup is in another EU region).
- Support access may temporarily surface customer data in another region's support console, but only with a documented support ticket and only for the duration of the support case.
- **No customer data is sent to a non-approved jurisdiction for processing**, including for AI inference, batch processing, or human review.

If a customer contracts for residency in a region ACME does not currently operate, the deal is routed to Legal and Engineering for feasibility review before signing.

## 6. No Copies Outside Approved Systems

Customer data must not be copied outside the approved systems. Specifically:

- **No** copies to local laptop drives (even encrypted corporate laptops — see §10).
- **No** copies to personal cloud storage (Dropbox, personal OneDrive, personal Google Drive).
- **No** copies to non-production environments without masking or redaction.
- **No** copies to test fixtures, even with fake customer names — use synthetic data instead.
- **No** copies to ACME-internal wikis or documents at the Internal classification.
- **No** copies to AI tools — see [`ai-tool-acceptable-use.md`](ai-tool-acceptable-use.md).
- **No** exports to email except via the approved customer-data email path (encrypted, with the customer's prior consent for the specific data shared).
- **No** retention past the contracted retention period.

The approved systems for customer data are:

| System | Use |
|--------|-----|
| Production environment for the relevant product (ACME Cloud, ACME Intelligence, ACME Workspace) | The system of record. |
| Customer-tenant SharePoint site | Customer-specific documents shared with the customer. |
| CRM (Salesforce) | Customer account records, contractual metadata. |
| Support ticketing system (e.g., Zendesk) | Support tickets and case history. |
| ACME Vault (vault.acme.example, fictional) | Customer-specific credentials (e.g., a customer's API key for an integration) — restricted path, per-customer access. |

Anything not on this list requires GRC Analyst (`Karthik Subramanian`) approval.

## 7. Access Logging

Every read of customer data is logged:

- Production databases log SELECT queries against customer tables (with user, timestamp, query, rows returned).
- Customer-tenant SharePoint sites log file access.
- CRM logs record access.
- Support tickets log ticket view access.
- ACME Vault logs every read of a customer-specific secret.

Logs are:

- Classified as Confidential.
- Retained for 13 months.
- Reviewed daily by the SOC for anomalous patterns — e.g., a user reading 10× the typical number of customer records in an hour, or reading outside business hours.
- Available to the GRC Analyst for audit and to the customer on request (per contract).

The SOC Lead (`Fatima Sheikh`) owns the log review process.

## 8. Right to Erasure

Customers may request erasure of their data — for themselves (as a controller) or for their end-users (with the customer's authorization). The process:

1. The request arrives via the customer's contracted channel or via `privacy@acme.example` (fictional).
2. The GRC Analyst (`Karthik Subramanian`) acknowledges within 72 hours and validates the request scope and identity.
3. Engineering identifies the systems holding the data and executes erasure within 30 days (extendable to 90 for complex requests with notice).
4. Backups containing the data are not retroactively erased — they expire per the standard backup retention (typically 35 days). The customer is informed.
5. Erasure excludes data ACME must retain for legal, regulatory, or contractual reasons (e.g., tax records, fraud-prevention logs) — these are documented.
6. The GRC Analyst provides a completion attestation to the customer.

## 9. Breach Notification to Customers

If customer data is breached — unauthorized access, disclosure, alteration, or destruction — ACME notifies the affected customer:

| Recipient | Timeline |
|-----------|---------|
| Internal CISO (`Rajan Mehta`) | Immediately on confirmation |
| Internal Legal and GRC | Within 1 hour of confirmation |
| Affected customer(s) | Within 72 hours of confirmation, per the customer's contract (some contracts require 24 hours; the contract controls) |
| Supervisory authority (where required) | Within 72 hours of becoming aware, per GDPR/DPDP |
| Affected end-users (where high risk) | Without undue delay, coordinated with the customer |

The customer notification includes:

- A description of what happened.
- The categories of data involved.
- The approximate number of records (if known).
- What ACME has done to contain and remediate.
- What ACME is doing to prevent recurrence.
- A single point of contact at ACME for the customer (typically the GRC Analyst or the customer's Account Manager).
- Where required, credit-monitoring or equivalent remediation offer.

Notifications are coordinated by the GRC Analyst and approved by the CISO. Workforce members must not communicate with customers about an incident without authorization — see [`security-incident-reporting.md`](security-incident-reporting.md) §9.

## 10. Customer Data on Workstations

Customer data should not be on a local workstation. The default is: interact with customer data through the approved web console or API, in the browser, with no local copy.

If a workforce member has a documented business need to view customer data locally (e.g., a data engineer running a one-off analysis):

- The laptop must be corporate-issued, Intune-enrolled, BitLocker/FileVault-encrypted — see [`device-encryption.md`](device-encryption.md).
- The data must be in the ACME-managed container — not the personal part of the laptop.
- The data must be deleted within 7 days.
- The access is logged per §7.
- The business need is documented in a ticket and approved by the GRC Analyst.

Customer data on BYOD phones is **never** permitted. Customer data on personal laptops is **never** permitted.

## 11. Sub-processors

ACME uses sub-processors for some customer-data operations (e.g., a cloud-hosted email delivery service, a payment processor). Rules:

- Every sub-processor is bound by a Data Processing Agreement (DPA).
- The sub-processor list is published to customers and updated 30 days before any change.
- Sub-processors are reviewed annually by the GRC Analyst for compliance.
- No customer data is sent to a sub-processor not on the published list.

## 12. Responsibilities

| Role | Responsibility |
|------|----------------|
| **GRC Analyst** (`Karthik Subramanian`) | Owns this document. Coordinates erasure and breach notification. Maintains sub-processor list. |
| **CISO** (`Rajan Mehta`) | Approves customer notifications. Final accountable owner. |
| **Security Director** (`Neha Saxena`) | Approves exceptions. Coordinates with Legal. |
| **SOC Lead** (`Fatima Sheikh`) | Monitors customer-data access logs. Triage anomalous access. |
| **Engineering Teams** | Implement residency, masking, and erasure in ACME products. Build access logging. |
| **Customer Success / Account Managers** | Coordinate customer notifications with the GRC Analyst. |
| **Every workforce member** | Access only the customer data they need. Never copy to unapproved systems. Never enter into AI tools. Report suspected exposure. |

## 13. Enforcement

- Conditional access restricts customer-data systems to compliant, corporate-issued devices.
- DLP prevents copy-paste of customer data into email, chat, or external apps.
- Access logging catches anomalous reads.
- Audits (internal + customer-requested) sample customer-data access for legitimacy.
- Violations are handled under [`acceptable-use-policy.md`](acceptable-use-policy.md) §9 and [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md). A customer-data exposure is a SEV1 incident.

## 14. Exceptions

Exceptions (e.g., a customer pilot that requires cross-region data flow not currently in the contract) require CISO (`Rajan Mehta`) approval, the customer's written consent, a documented compensating control, and a time limit. Email `security-oncall@acme.example` (fictional).

## 15. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`data-classification.md`](data-classification.md) — Customer Data tier definition.
- [`acceptable-use-policy.md`](acceptable-use-policy.md) — Prohibitions on exfiltration.
- [`identity-and-access-management.md`](identity-and-access-management.md) — Per-customer access.
- [`least-privilege-access.md`](least-privilege-access.md) — Per-customer PIM activation.
- [`device-encryption.md`](device-encryption.md) — Encryption baseline for systems handling customer data.
- [`byod-policy.md`](byod-policy.md) — Customer data is never on BYOD.
- [`ai-tool-acceptable-use.md`](ai-tool-acceptable-use.md) — Customer data is never in any AI tool.
- [`secrets-management.md`](secrets-management.md) — Customer-specific secrets in ACME Vault.
- [`security-incident-reporting.md`](security-incident-reporting.md) — Incident workflow, including customer notification.
- [`privacy-acknowledgement.md`](privacy-acknowledgement.md) — End-user personal data, DSRs.
- [`confidentiality-agreement.md`](confidentiality-agreement.md) — Customer data is Confidential Information.
- [`../01-hr/sample-employment-agreement.md`](../01-hr/sample-employment-agreement.md) — Signed agreement controls.
- [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) — Customer-data access revoked on separation.
- [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) — Termination workflow.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — GRC Analyst, CISO, SOC Lead contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — Customer Data, Restricted, residency, DPA definitions.
