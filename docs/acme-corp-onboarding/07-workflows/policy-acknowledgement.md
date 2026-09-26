---
document_id: ACME-WF-012
title: Policy Acknowledgement Workflow
category: workflow
department: human-resources
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [workflow, onboarding, policy-acknowledgement]
---

# Policy Acknowledgement Workflow

> Fictional document. All systems (hr.acme.example, portal.acme.example) are illustrative.

## 1. Overview

Policy acknowledgement is the legal and operational backbone of onboarding. A new hire cannot be granted write repository access, AI tool licenses, or elevated access until the relevant policies are acknowledged. The canonical sequencing rule:

> Policy acknowledgement (POL-001) must complete before access approvals beyond read-only (ACC-002 is read-only; ACC-003 write requires POL-001).

HR Operations owns the tracking; the CISO office co-owns the security-related acknowledgements; the new hire owns the act of reading + acknowledging; the hiring manager is responsible for ensuring the new hire has time to read in good faith.

## 2. Scope

- **Starts:** Day 1 (HR welcome session, DAY1-007).
- **Ends:** End of week 1 (all acknowledgements filed).
- **Annual refresh:** All policies re-acknowledged annually on the new hire's anniversary.
- **Roles involved:** New Hire, HRBP, Security (GRC), CISO office, Hiring Manager.
- **Office-agnostic.**

## 3. Cross-References

- HR: [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md), [`../01-hr/anti-harassment-policy.md`](../01-hr/anti-harassment-policy.md), [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md), [`../01-hr/sample-employment-agreement.md`](../01-hr/sample-employment-agreement.md)
- Security: [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md), [`../03-security/acceptable-use-policy.md`](../03-security/acceptable-use-policy.md), [`../03-security/confidentiality-agreement.md`](../03-security/confidentiality-agreement.md), [`../03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md), [`../03-security/password-and-mfa-requirements.md`](../03-security/password-and-mfa-requirements.md), [`../03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- Training: [`../10-training/workplace-conduct.md`](../10-training/workplace-conduct.md), [`../10-training/security-awareness.md`](../10-training/security-awareness.md)
- Forms: [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md), [`../08-forms/manager-approval.md`](../08-forms/manager-approval.md)
- Contacts: [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)

## 4. Policy Acknowledgement Task List

| Task ID | Description | Responsible | Prerequisites | Due | Approval | Completion Criteria | Default Status |
|---|---|---|---|---|---|---|---|
| POL-001 | Acknowledge information security policy + acceptable use policy + password & MFA requirements (three-in-one acknowledgement pack) | New Hire | SEC-001 (security awareness training so the acknowledgement is informed) | End of day 5 | Security (GRC) + CISO office | Acknowledgement form submitted for all three policies in HR Hub | NOT_STARTED |
| POL-002 | Sign confidentiality agreement (NDA) + privacy acknowledgement | New Hire | DAY1-007 (HR welcome session) | End of day 2 | HRBP + CISO office | Both documents signed; countersigned by legal ops | NOT_STARTED |
| POL-003 | Acknowledge code of conduct + anti-harassment policy | New Hire | DAY1-007 | End of day 2 | HRBP | Acknowledgement form submitted for both policies in HR Hub | NOT_STARTED |
| POL-004 | Acknowledge AI tool acceptable use policy (required for GitHub Copilot seat) | New Hire | SEC-001, [`security-training.md`](./security-training.md) SEC-005 | End of day 5 | Manager + Director AI/ML (Anitha Rajan) | Acknowledgement form submitted in HR Hub | NOT_STARTED |
| POL-005 | Acknowledge remote / hybrid working policy (for hybrid and remote employees only) | New Hire | DAY1-007 | End of day 3 | HRBP | Acknowledgement form submitted in HR Hub | NOT_STARTED |
| POL-006 | Acknowledge data classification + customer data handling policies (for roles touching customer data — engineering, support, sales) | New Hire | SEC-003 (data classification training) | End of day 5 | Security (GRC) + CISO office | Acknowledgement form submitted in HR Hub | NOT_STARTED |
| POL-007 | Manager review of acknowledgements — manager confirms all applicable POL-* tasks are `COMPLETED` for the new hire before signing off week-1 file | Hiring Manager | POL-001 through POL-006 | End of day 5 | Manager | Manager attestation recorded in HR Hub | NOT_STARTED |
| POL-008 | Annual policy re-acknowledgement — schedule recurring annual re-acknowledgement of all policies on the new hire's anniversary | HR Operations | POL-001 through POL-006 | Day 30 (scheduling) | HRBP | Annual recurring re-acknowledgement tasks scheduled in HR Hub | NOT_STARTED |

## 5. Dependencies

- **DAY1-007 blocks POL-002, POL-003, POL-005** — The HR welcome session is where the new hire receives the policy packs; acknowledgements cannot precede it.
- **SEC-001 blocks POL-001** — Information security policy acknowledgement must be informed by security awareness training (canonical — see [`security-training.md`](./security-training.md)).
- **SEC-001 blocks POL-004** — AI tool acceptable use acknowledgement requires the foundational security training.
- **SEC-003 blocks POL-006** — Data classification + customer data handling acknowledgement requires the data classification training module.
- **POL-001 blocks ACC-002** — Wait, the canonical rule says policy acknowledgement is required for access **beyond read-only** (ACC-003 write). ACC-002 is read-only and does *not* require POL-001; ACC-003 (write) does.
- **POL-001 blocks ACC-003** — Write repository access requires the policy acknowledgement (canonical).
- **POL-004 blocks ACC-004** — AI coding assistant seat requires the AI tool acceptable use acknowledgement (canonical).
- **POL-006 blocks ACC-007** — Elevated / production access for customer-data roles requires the customer data handling acknowledgement.
- **POL-007 → WK1-015** — Manager's attestation that all POL-* are `COMPLETED` is a precondition for the week-1 sign-off.
- **POL-007 → MGR-010** — Manager attestation feeds the 30-day review (the manager confirms policy debt is clear).

## 6. Status Tracking

All POL-* tasks are tracked in HR Hub under **Onboarding → Policy Acknowledgement**. Allowed statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

If POL-001 or POL-004 is `BLOCKED` at end of day 5 because the new hire has not yet completed SEC-001, the GRC Analyst automatically extends the deadline to the next business day after SEC-001 closes — but write repository access (ACC-003) and AI tool seat (ACC-004) remain gated until POL-001 / POL-004 themselves are `COMPLETED`.

If a new hire declines to acknowledge a policy (rare), the HRBP opens a conversation with the new hire and the hiring manager. The file stays `BLOCKED` until the matter is resolved; if the new hire ultimately declines a non-negotiable policy (e.g., confidentiality agreement), the HRBP escalates to Ananya Sharma (VP HR) and the file may be routed to [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md).

## 7. RACI Matrix

| Activity | R | A | C | I |
|---|---|---|---|---|
| Infosec + AUP + password/MFA ack | New Hire | Security (GRC) + CISO office | HRBP | VP HR |
| NDA + privacy acknowledgement | New Hire | HRBP + CISO office | Legal Ops | VP HR |
| Code of conduct + anti-harassment ack | New Hire | HRBP | HR Onboarding Coordinator | VP HR |
| AI tool ack | New Hire | Manager + Director AI/ML | Security | CISO office |
| Remote/hybrid policy ack | New Hire | HRBP | HR Onboarding Coordinator | VP HR |
| Data classification + customer data ack | New Hire | Security (GRC) + CISO office | HRBP | VP Engineering |
| Manager attestation of POL-* completion | Hiring Manager | Manager | HRBP | VP HR |
| Annual re-acknowledgement scheduling | HR Operations | HRBP | Security (GRC) | VP HR |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 8. Key Terms

- **NDA** — Non-Disclosure Agreement (a.k.a. confidentiality agreement). See [`../03-security/confidentiality-agreement.md`](../03-security/confidentiality-agreement.md).
- **AUP** — Acceptable Use Policy. See [`../03-security/acceptable-use-policy.md`](../03-security/acceptable-use-policy.md).
- **PII** — Personally Identifiable Information.
- **HRBP** — HR Business Partner. See [`../metadata/glossary.md`](../metadata/glossary.md).
- **Legal Ops** — Legal Operations; the function that countersigns legal documents.
- **Attestation** — a formal assertion by a responsible party that a state of affairs is true (e.g., that all POL-* tasks are complete).

## 9. Hand-off

When POL-001 through POL-007 are `COMPLETED`, the policy portion of the onboarding file is closed. The annual re-acknowledgement (POL-008) schedule lives in HR Hub and fires automatically thereafter; HR Operations owns the annual re-acknowledgement tracking and reports exceptions to the HRBP quarterly.
