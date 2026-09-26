---
document_id: ACME-SEC-010
title: Privacy Acknowledgement
category: security
department: information-security
applicable_roles: [all]
owner: Karthik Subramanian, GRC Analyst
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, privacy, gdpr, dpdp, data-subject-rights, fictional]
---

# Privacy Acknowledgement

> ACME Corp fictional onboarding library. Hostnames, mailboxes, and contact details in this document are fictional and illustrative. Regulatory references (GDPR, DPDP Act 2023, CCPA) are real statutes referenced for fictional compliance.

## 1. Purpose

This document states ACME Corp's privacy obligations and every workforce member's acknowledgement of them. It complements the [`confidentiality-agreement.md`](confidentiality-agreement.md) — confidentiality is about secrecy; privacy is about respecting individuals' rights over their personal data. Privacy applies to employee personal data, candidate personal data, and customer end-user personal data. Workforce members acknowledge this document via [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md).

## 2. Scope

This applies to:

- All ACME workforce members handling personal data of any kind.
- All personal data ACME processes, whether about employees, candidates, customers' end-users, or members of the public.
- All systems ACME uses to process personal data — Microsoft 365, `hr.acme.example`, `helpdesk.acme.example`, the ACME Cloud and ACME Workspace products (all hostnames fictional).

## 3. Definitions

- **Personal data** — any information relating to an identified or identifiable natural person.
- **Special-category (sensitive) personal data** — health, biometrics, racial/ethnic origin, religious belief, sexual orientation, trade-union membership, and similar. Treated as Restricted under [`data-classification.md`](data-classification.md).
- **Data subject** — the individual to whom the personal data relates.
- **Data controller** — the entity that determines the purposes and means of processing. ACME is the controller for employee data; ACME's customers are typically the controller for their end-users' data, with ACME as processor.
- **Data processor** — an entity that processes personal data on behalf of a controller. ACME is a processor for customer end-user data when providing ACME Cloud, ACME Intelligence, or ACME Workspace.

## 4. Lawful Basis

ACME processes personal data only where there is a lawful basis. Common lawful bases at ACME:

| Lawful Basis | Examples at ACME |
|--------------|------------------|
| **Contract** | Processing employee data to fulfil the employment contract; processing customer end-user data to provide the contracted service. |
| **Legal obligation** | Tax records, statutory filings, regulatory disclosures. |
| **Legitimate interest** | Security monitoring (with the balancing-test documentation), internal fraud prevention. |
| **Consent** | Optional marketing communications, optional cookies, certain cross-border data transfers. |
| **Vital interest** | Emergency contact information used in a medical emergency. |

Where ACME relies on consent, consent is freely given, specific, informed, and revocable. Revoking consent does not affect the lawfulness of processing before revocation.

## 5. Data Minimization

Workforce members collect and process only the minimum personal data necessary for the task. Concretely:

- Do not collect personal data "in case it's useful later."
- Do not copy personal data into systems not approved for it.
- Do not retain personal data past the period in the ACME retention schedule (see §8).
- Do not enter personal data into external AI tools — see [`ai-tool-acceptable-use.md`](ai-tool-acceptable-use.md).

If you are unsure whether a collection is minimal, ask the GRC Analyst (`Karthik Subramanian`).

## 6. Data Subject Rights

ACME recognizes the following rights of data subjects, in accordance with applicable law (GDPR, India's DPDP Act 2023, CCPA, and others):

| Right | Description |
|-------|-------------|
| **Access** | A data subject may request a copy of their personal data. |
| **Rectification** | A data subject may request correction of inaccurate data. |
| **Erasure** | A data subject may request deletion ("right to be forgotten"), subject to legal retention obligations. |
| **Restriction** | A data subject may request processing be restricted. |
| **Portability** | A data subject may request their data in a structured, machine-readable format. |
| **Objection** | A data subject may object to processing based on legitimate interest or for direct marketing. |
| **Withdrawal of consent** | A data subject may withdraw consent at any time. |
| **Complaint** | A data subject may lodge a complaint with the supervisory authority. |

### 6.1 Handling Requests at ACME

If you receive a data subject request (verbally or in writing):

1. Forward it to `privacy@acme.example` (fictional mailbox monitored by the GRC Analyst) within 1 business day.
2. Do not act on it directly — even a simple "yes, we have your data" requires the GRC Analyst to validate identity and scope.
3. The GRC Analyst acknowledges receipt to the data subject within 72 hours and completes the request within 30 days (extendable by 60 days for complex requests, with notice to the data subject).
4. For customer end-user requests received via the customer's support channel, route through the customer — ACME is the processor, the customer is the controller.

## 7. No Surveillance Without Cause

ACME does **not** conduct covert surveillance of employees without cause. Specifically:

- Email and chat content is monitored by Microsoft Purview for malware and DLP signals, not for general employee surveillance.
- Browsing activity on ACME networks or VPN is logged for security but is not routinely reviewed by managers.
- Camera footage in ACME offices is recorded for physical security, retained briefly, and accessed only on incident.
- Employee monitoring beyond the security baseline requires: (a) a documented cause (security incident, HR investigation, legal hold); (b) authorization from the Security Director (`Neha Saxena`) and the HR Business Partner; (c) the minimum scope and duration necessary; (d) a record in the monitoring register maintained by the GRC Analyst.

Personal phones used for MFA are not enrolled into Intune — see [`byod-policy.md`](byod-policy.md). The personal phone is used only to receive MFA pushes.

## 8. Retention

Personal data is retained only as long as necessary, per the ACME retention schedule (maintained by the GRC Analyst). Summary:

| Data Type | Default Retention |
|-----------|-------------------|
| Employee HR records | Duration of employment + 7 years |
| Payroll records | 7 years (statutory) |
| Candidate data (unsuccessful) | 12 months from decision, then deleted |
| CCTV footage | 30 days unless preserved for an incident |
| Security logs (sign-in, audit) | 13 months |
| Customer end-user data (as processor) | Per the customer's contract |
| Incident evidence | 7 years after closure |

Retention beyond these defaults requires an exception and a documented lawful basis.

## 9. International Transfers

ACME operates in India, the UK, and the US. Personal data may transfer between these jurisdictions under:

- **Intra-group transfers** — governed by the ACME intra-group data transfer agreement.
- **Standard Contractual Clauses (SCCs)** — for transfers from the UK/EEA to non-adequate jurisdictions.
- **Adequacy** — the UK and EEA are adequate for each other's residents; transfers to India rely on the DPDP Act's cross-border provisions plus SCCs where applicable.

The GRC Analyst maintains the transfer register. Workforce members do not transfer personal data outside ACME's approved systems without GRC approval.

## 10. Breach Notification

A privacy breach (unauthorized access to or disclosure of personal data) is a security incident — see [`security-incident-reporting.md`](security-incident-reporting.md). Notification timelines:

| Recipient | Timeline |
|-----------|----------|
| **Supervisory authority** (where required by GDPR/DPDP) | Within 72 hours of becoming aware |
| **Affected data subjects** (where high risk) | Without undue delay |
| **Customer (for processor incidents)** | Per the customer's contract — typically 72 hours |
| **Internal CISO and Legal** | Immediately on confirmation |

The GRC Analyst coordinates notifications; the CISO (`Rajan Mehta`) approves them.

## 11. Responsibilities

| Role | Responsibility |
|------|----------------|
| **Every workforce member** | Minimizes personal data collection. Reports privacy incidents promptly. Routes DSRs to GRC. |
| **GRC Analyst** (`Karthik Subramanian`) | Maintains this document and the retention/transfer registers. Handles DSRs. Coordinates breach notifications. |
| **Security Director** (`Neha Saxena`) | Approves cause-based monitoring. |
| **CISO** (`Rajan Mehta`) | Approves regulator notifications. |
| **HR Operations** | Maintains employee personal data accurately. Handles employee DSRs. |
| **Engineering Teams** | Implement privacy-by-design in ACME products. |

## 12. Enforcement

- Privacy-by-design is reviewed at design-doc stage by the GRC Analyst.
- DLP prevents exfiltration of personal data per [`data-classification.md`](data-classification.md).
- Privacy incidents follow the [`security-incident-reporting.md`](security-incident-reporting.md) workflow.

## 13. Exceptions

Exceptions require CISO (`Rajan Mehta`) approval and Legal review, are time-bound, and are logged in the risk register.

## 14. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`confidentiality-agreement.md`](confidentiality-agreement.md) — Companion secrecy obligations.
- [`data-classification.md`](data-classification.md) — Personal data is Restricted by default.
- [`customer-data-handling.md`](customer-data-handling.md) — Customer end-user personal data.
- [`security-incident-reporting.md`](security-incident-reporting.md) — Privacy breach workflow.
- [`byod-policy.md`](byod-policy.md) — Personal device privacy boundaries.
- [`ai-tool-acceptable-use.md`](ai-tool-acceptable-use.md) — No personal data in external AI.
- [`../01-hr/sample-employment-agreement.md`](../01-hr/sample-employment-agreement.md) — Signed employment agreement controls.
- [`../01-hr/employee-information-form.md`](../01-hr/employee-information-form.md) — Employee personal data collection.
- [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md) — Acknowledgement form.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — GRC Analyst contact.
- [`../metadata/glossary.md`](../metadata/glossary.md) — PII, GDPR, DSR definitions.
