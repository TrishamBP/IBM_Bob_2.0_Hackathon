---
document_id: ACME-SEC-009
title: Confidentiality Agreement
category: security
department: information-security
applicable_roles: [all]
owner: Karthik Subramanian, GRC Analyst
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, confidentiality, nda, employment, fictional]
---

# Confidentiality Agreement

> ACME Corp fictional onboarding library. This document restates and elaborates the confidentiality obligations in the fictional ACME employment agreement ([`../01-hr/sample-employment-agreement.md`](../01-hr/sample-employment-agreement.md)) for the onboarding library. It is illustrative; the signed employment agreement controls in case of conflict. All hostnames, customer names, and figures are fictional.

## 1. Purpose

This document defines ACME Corp's confidentiality obligations for every workforce member. It exists alongside the employment agreement and the parent [`information-security-policy.md`](information-security-policy.md). It restates what counts as Confidential Information, the obligations that attach to it, how long those obligations last, and what happens during and after separation. New workforce members acknowledge this document via [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md) on or before day one.

## 2. Scope

This applies to:

- All ACME Corp employees, contractors, interns, and temporary staff.
- All ACME Confidential Information as defined in §3, regardless of medium — spoken, written, electronic, observed, or derived.
- The period of engagement at ACME and the period after separation as set out in §6.

## 3. What Counts as Confidential Information

"Confidential Information" includes — but is not limited to — the following categories, all of which appear in the ACME data classification scheme as Internal, Confidential, Restricted, or Customer Data tiers (see [`data-classification.md`](data-classification.md)):

| Category | Examples |
|----------|----------|
| **Business strategy & financials** | Unpublished financial results, M&A plans, fundraising plans, board materials, executive-level OKRs. |
| **Customer information** | Customer names, contracts, configurations, support tickets, customer-uploaded data. Treated as Customer Data per [`customer-data-handling.md`](customer-data-handling.md). |
| **Product information** | Source code (see [`source-code-security.md`](source-code-security.md)), design documents, roadmaps, architecture diagrams, internal AI model weights, training data composition. |
| **Security information** | Security postmortems, the risk register, vulnerability scan results, the ACME Vault contents (see [`secrets-management.md`](secrets-management.md)), incident evidence, the SOC playbook. |
| **Employee information** | Payroll data, performance reviews, the contents of `hr.acme.example` (fictional), salary bands, disciplinary records. |
| **Partner / vendor information** | Contracts, pricing, integration details, roadmaps shared under NDA. |
| **Operational information** | Internal hostnames (`vault.acme.example`, etc., fictional), IP address ranges, internal runbooks, on-call schedules. |

Information is Confidential Information whether or not it is marked as such. The classification tier (see [`data-classification.md`](data-classification.md)) tells you the handling rules; the obligations in this document apply to anything that is not explicitly Public.

## 4. Obligations

Every workforce member agrees to:

1. **Hold Confidential Information in trust** and use it only for the purpose of performing their role at ACME.
2. **Not disclose** Confidential Information to anyone outside ACME except as required by their role and in accordance with this policy.
3. **Not disclose** Confidential Information to anyone inside ACME except those with a need-to-know.
4. **Protect** Confidential Information with the controls specified for its tier in [`data-classification.md`](data-classification.md) — encryption, access controls, DLP, and so on.
5. **Not use** Confidential Information for personal gain, for the benefit of any other employer, or for the benefit of any person or entity outside ACME.
6. **Not enter** Confidential Information (especially Customer Data) into external AI tools — see [`ai-tool-acceptable-use.md`](ai-tool-acceptable-use.md).
7. **Return or destroy** Confidential Information at the end of engagement per [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) and [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md).
8. **Report** any actual or suspected disclosure per [`security-incident-reporting.md`](security-incident-reporting.md).
9. **Cooperate** with ACME's investigations into any suspected disclosure.

## 5. Permitted Disclosures

Disclosure of Confidential Information is permitted only in the following circumstances:

| Circumstance | Conditions |
|---------------|------------|
| **Job duties** | Disclosure to colleagues with a need-to-know, in the course of performing assigned work. |
| **Customer support** | Disclosure to a customer of their own data, per [`customer-data-handling.md`](customer-data-handling.md). |
| **Regulator / law enforcement** | Disclosure required by law, after notice to the CISO (`Rajan Mehta`) and the Legal team, except where prohibited. |
| **Court order** | Disclosure in response to a valid court order, after notice to the Legal team. |
| **Written authorization** | Disclosure with the written authorization of the CISO or an executive officer. |

When disclosure is compelled by law, the workforce member must notify the GRC Analyst (`Karthik Subramanian`) immediately so that ACME can seek a protective order.

## 6. Term and Survival

This agreement's obligations:

- Begin on the first day of engagement with ACME.
- Continue throughout the engagement without interruption.
- **Survive separation indefinitely** for trade secrets and Customer Data.
- **Survive separation for 5 years** for all other Confidential Information.
- **Survive separation indefinitely** for the obligation not to disclose customer-uploaded data to external parties.

Separation does not relieve the workforce member of obligations under this agreement. The separation process (see [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md)) includes a reaffirmation of these obligations and a return-or-destroy attestation.

## 7. Remedies

Breach of this agreement may result in:

- Civil action for damages and injunctive relief.
- Termination of employment or contract, per [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md).
- Referral to law enforcement where criminal conduct is suspected (e.g., theft of trade secrets).
- Coordination with the affected customer where customer data was disclosed.

The GRC Analyst (`Karthik Subramanian`) maintains the breach register and coordinates with Legal and HR.

## 8. Whistleblower Carve-Out

Nothing in this agreement prevents a workforce member from:

- Reporting a violation of law to a competent authority (a regulator, law enforcement).
- Participating in an investigation by a competent authority.
- Disclosing Confidential Information to legal counsel for the purpose of seeking legal advice.
- Disclosing Confidential Information that is specifically authorized to be disclosed under applicable whistleblower protection laws.

These carve-outs are bounded by applicable law — when in doubt, the GRC Analyst can advise.

## 9. Responsibilities

| Role | Responsibility |
|------|----------------|
| **Every workforce member** | Read this document. Acknowledge it. Follow it. |
| **GRC Analyst** (`Karthik Subramanian`) | Maintains this document. Coordinates breach response. |
| **CISO** (`Rajan Mehta`) | Approves exceptions. Coordinates with Legal on enforcement. |
| **HR Operations** | Ensures acknowledgement is captured during onboarding and at separation. |
| **People Managers** | Reinforce the obligations with their teams. |

## 10. Enforcement

- Acknowledgement is captured via [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md) on or before day one.
- DLP and conditional access enforce the technical controls.
- The GRC Analyst coordinates with HR and Legal on suspected breaches.

## 11. Exceptions

Exceptions to this agreement require written authorization from the CISO (`Rajan Mehta`) and, where customer data is involved, the affected customer. There is no general exception for "convenience" or "speed."

## 12. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`acceptable-use-policy.md`](acceptable-use-policy.md) — Operational rules that implement this agreement.
- [`data-classification.md`](data-classification.md) — Tier definitions referenced throughout.
- [`customer-data-handling.md`](customer-data-handling.md) — Customer data is a special case.
- [`source-code-security.md`](source-code-security.md) — Source code is Confidential by default.
- [`secrets-management.md`](secrets-management.md) — Credentials are Restricted.
- [`privacy-acknowledgement.md`](privacy-acknowledgement.md) — Companion privacy obligations.
- [`../01-hr/sample-employment-agreement.md`](../01-hr/sample-employment-agreement.md) — The signed employment agreement controls.
- [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md) — Behavioural baseline.
- [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) — Separation reaffirmation.
- [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md) — Acknowledgement form.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — GRC Analyst contact.
