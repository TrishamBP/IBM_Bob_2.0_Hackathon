---
document_id: ACME-SEC-001
title: Information Security Policy
category: security
department: information-security
applicable_roles: [all]
owner: Rajan Mehta, CISO
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, policy, governance, cia-triad, foundational, fictional]
---

# Information Security Policy

> ACME Corp fictional onboarding library. This policy is the parent document for the entire `03-security/` directory. Internal hostnames and mailboxes (for example `vault.acme.example`, `security-oncall@acme.example`) are fictional and used for illustration only.

## 1. Purpose

This policy establishes the foundation for protecting ACME Corp's information assets — the data, systems, source code, and customer information that the company creates, processes, stores, and transmits. It states why information security matters at ACME, who is accountable for it, and the principles every employee, contractor, and authorized third party must follow. All other security documents in this library (data classification, password and MFA requirements, incident reporting, BYOD, encryption, and so on) derive from this policy and must be read alongside it.

## 2. Scope

This policy applies to:

- All ACME Corp employees, interns, contractors, and temporary staff.
- All ACME-issued devices (laptops, workstations, mobile devices) and approved personal devices used for ACME work under [`byod-policy.md`](byod-policy.md).
- All ACME corporate systems, including the fictional `portal.acme.example`, `hr.acme.example`, `helpdesk.acme.example`, `wiki.acme.example`, `vault.acme.example`, `packages.acme.example`, and `status.acme.example`.
- All ACME source code repositories hosted at the fictional `git.acme.example` (GitHub Enterprise).
- All ACME data, regardless of where it is stored or transmitted, classified according to [`data-classification.md`](data-classification.md).
- All ACME-developed products — ACME Cloud, ACME Intelligence, and ACME Workspace — including their production and pre-production environments.

Where a customer or partner environment is involved, the more restrictive of ACME's policy or the customer's contracted security requirements applies.

## 3. Core Principle — the CIA Triad

ACME's information security program is built on the classic Confidentiality, Integrity, and Availability (CIA) triad:

| Property | Definition | ACME Commitment |
|----------|------------|-----------------|
| **Confidentiality** | Information is disclosed only to authorized parties. | Access is granted on a need-to-know basis using least privilege (see [`least-privilege-access.md`](least-privilege-access.md)). Customer data is treated as Restricted (see [`customer-data-handling.md`](customer-data-handling.md)). |
| **Integrity** | Information is accurate and unaltered in unauthorized ways. | All source code changes flow through pull requests with CODEOWNERS review (see [`source-code-security.md`](source-code-security.md)). Production deployments require CI checks (see [`../04-engineering/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md)). |
| **Availability** | Information and systems are accessible to authorized users when needed. | ACME publishes its uptime at `status.acme.example` (fictional) and runs an on-call rotation per product. Backups are tested quarterly. |

Trade-offs between the three are governed by the GRC Analyst (`Karthik Subramanian`) and escalated to the CISO (`Rajan Mehta`) when the trade-off is material to customers.

## 4. Governance

The Information Security function is owned by the Chief Information Security Officer (CISO), `Rajan Mehta` (`rajan.mehta@acme.example`). The CISO reports to the executive leadership and is the named accountable individual for the program. The Information Security team includes:

- **Security Director** — `Neha Saxena` (`neha.saxena@acme.example`). Owns policy, awareness, and the SOC.
- **IAM Engineer** — `Abhishek Verma` (`abhishek.verma@acme.example`). Owns identity, SSO, conditional access, and PIM.
- **SOC Lead** — `Fatima Sheikh` (`fatima.sheikh@acme.example`). Owns monitoring, detection, and incident triage.
- **GRC Analyst** — `Karthik Subramanian` (`karthik.subramanian@acme.example`). Owns risk register, audits, and policy maintenance.

The Information Security function:

- Reports to the executive team at least quarterly.
- Maintains a risk register reviewed quarterly.
- Carries out an annual policy review (the `review_date` field on every document).
- Coordinates internal and external audits.

## 5. Requirements

Every ACME workforce member must:

1. Complete mandatory security training within 14 days of joining and annually thereafter (see [`../07-workflows/security-training.md`](../07-workflows/security-training.md)).
2. Sign the policy acknowledgement (see [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md)) before access to ACME systems is provisioned beyond the onboarding baseline.
3. Use a unique, strong password and ACME-issued MFA on every ACME account (see [`password-and-mfa-requirements.md`](password-and-mfa-requirements.md)).
4. Classify information they create or receive (see [`data-classification.md`](data-classification.md)) and handle it according to the matrix in that document.
5. Lock their workstation whenever they step away (see [`clean-desk-policy.md`](clean-desk-policy.md)).
6. Report any suspected security incident within 1 hour of becoming aware (see [`security-incident-reporting.md`](security-incident-reporting.md)).
7. Never enter customer data, source code, secrets, or Restricted information into external AI tools (see [`ai-tool-acceptable-use.md`](ai-tool-acceptable-use.md)).

## 6. Responsibilities

| Role | Responsibilities |
|------|------------------|
| **CISO** (`Rajan Mehta`) | Owns the program. Approves exceptions. Reports to executive leadership. |
| **Security Director** (`Neha Saxena`) | Owns the policy library, awareness program, and SOC operations. |
| **IAM Engineer** (`Abhishek Verma`) | Maintains Entra ID, conditional access, PIM, SSO, and access reviews. |
| **SOC Lead** (`Fatima Sheikh`) | Monitors signals, triages incidents, runs the on-call rotation. |
| **GRC Analyst** (`Karthik Subramanian`) | Maintains the risk register, schedules audits, tracks exceptions. |
| **People Managers** | Ensure their reports complete training, sign acknowledgements, and follow least-privilege access. |
| **Every Employee** | Follows this policy and the documents under `03-security/`. Reports incidents promptly. |

## 7. Enforcement

This policy is enforced through technical and administrative controls:

- **Technical:** Conditional access in Entra ID enforces MFA and device compliance. Intune enforces encryption and patching. Microsoft Purview enforces data loss prevention. Microsoft Defender for Endpoint enforces EDR.
- **Administrative:** Annual security training, policy acknowledgement, access reviews, and audit findings.
- **Consequences:** Violations are handled under [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md) and may result in access revocation (see [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md)), disciplinary action up to termination, and where law has been broken, referral to law enforcement.

## 8. Exceptions

Exceptions to this policy are rare and time-bound. To request an exception:

1. Open a request through the security on-call mailbox `security-oncall@acme.example` (fictional).
2. The GRC Analyst (`Karthik Subramanian`) logs the request in the risk register.
3. The CISO (`Rajan Mehta`) approves or denies the exception in writing.
4. Approved exceptions include a compensating control, an expiry date no further than 12 months out, and a review owner.

No employee may self-grant an exception. "It was convenient" is not an acceptable rationale.

## 9. Definitions

- **ACME workforce** — employees, interns, contractors, and authorized third parties.
- **ACME system** — any system owned or operated by ACME, including the fictional hostnames listed in §2.
- **Customer data** — any data about, or belonging to, an ACME customer that ACME processes — always treated as Restricted (see [`customer-data-handling.md`](customer-data-handling.md)).
- **Restricted** — the highest data classification tier (see [`data-classification.md`](data-classification.md)).

## 10. Related Documents

- [`acceptable-use-policy.md`](acceptable-use-policy.md) — What you may and may not do with ACME systems.
- [`data-classification.md`](data-classification.md) — The 5-tier scheme that drives every handling rule.
- [`password-and-mfa-requirements.md`](password-and-mfa-requirements.md) — Mandatory authentication controls.
- [`identity-and-access-management.md`](identity-and-access-management.md) — Entra ID, SSO, conditional access, PIM.
- [`least-privilege-access.md`](least-privilege-access.md) — Default-deny, time-bound elevation.
- [`security-incident-reporting.md`](security-incident-reporting.md) — How to report and how ACME responds.
- [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md) — Behavioural baseline referenced for enforcement.
- [`../07-workflows/security-training.md`](../07-workflows/security-training.md) — Mandatory training workflow.
- [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md) — Acknowledgement form.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Security team contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — CIA, GRC, SOC, IAM, RBAC, ABAC definitions.
