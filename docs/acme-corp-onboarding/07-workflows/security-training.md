---
document_id: ACME-WF-009
title: Security Training Workflow
category: workflow
department: security
applicable_roles: [all]
owner: Security Operations (CISO Office)
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [workflow, onboarding, security-training]
---

# Security Training Workflow

> Fictional document. All systems, links, and addresses are illustrative.

## 1. Overview

Security training is the gating activity for most production-grade access at ACME Corp. A new hire cannot acknowledge the information security policy, receive repository write access, use GitHub Copilot Business, or participate in on-call rotation until the security training chain is `COMPLETED`. The chain is owned by the CISO office (Rajan Mehta — `rajan.mehta@acme.example`) and executed by GRC Analyst Karthik Subramanian (`karthik.subramanian@acme.example`) with the security on-call (`security-oncall@acme.example`) for incident-response drills.

Training is delivered through `wiki.acme.example` (training portal) and assessed through `hr.acme.example` (HR Hub training module). Assessments must score ≥ 80% to pass; retakes are unlimited but logged.

## 2. Scope

- **Starts:** Day 1 (security orientation introduction, DAY1-010).
- **Ends:** End of week 1 (formal security training completion, SEC-005 / SEC-006).
- **Refresher:** Annual (see [`../10-training/security-awareness.md`](../10-training/security-awareness.md) and [`../10-training/privacy-awareness.md`](../10-training/privacy-awareness.md)).
- **Roles involved:** New Hire, Security (GRC), CISO office, Hiring Manager (for the AI-tool acknowledgement review).
- **Office-agnostic.**

## 3. Cross-References

- Security: [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md), [`../03-security/acceptable-use-policy.md`](../03-security/acceptable-use-policy.md), [`../03-security/password-and-mfa-requirements.md`](../03-security/password-and-mfa-requirements.md), [`../03-security/data-classification.md`](../03-security/data-classification.md), [`../03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md), [`../03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md), [`../03-security/phishing-awareness.md`](../03-security/phishing-awareness.md), [`../03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md), [`../03-security/confidentiality-agreement.md`](../03-security/confidentiality-agreement.md)
- Training: [`../10-training/security-awareness.md`](../10-training/security-awareness.md), [`../10-training/privacy-awareness.md`](../10-training/privacy-awareness.md), [`../10-training/ai-coding-assistant-usage.md`](../10-training/ai-coding-assistant-usage.md), [`../10-training/workplace-conduct.md`](../10-training/workplace-conduct.md)
- Forms: [`../08-forms/training-completion.md`](../08-forms/training-completion.md), [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md)
- Contacts: [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)

## 4. Security Training Task List

| Task ID | Description | Responsible | Prerequisites | Due | Approval | Completion Criteria | Default Status |
|---|---|---|---|---|---|---|---|
| SEC-001 | Complete security awareness training module (phishing, password hygiene, social engineering, MFA recovery) | New Hire | DAY1-010 (security orientation intro) | End of day 4 | Security (GRC) sign-off | Module completed in HR Hub; assessment score ≥ 80% | NOT_STARTED |
| SEC-002 | Complete privacy awareness training module (PII handling, data subject rights, retention, cross-border transfer) | New Hire | DAY1-010 | End of day 4 | Security (GRC) sign-off | Module completed; assessment score ≥ 80% | NOT_STARTED |
| SEC-003 | Complete data classification training (Public / Internal / Confidential / Restricted handling) | New Hire | SEC-001 | End of day 4 | Security (GRC) sign-off | Module completed; assessment score ≥ 80% | NOT_STARTED |
| SEC-004 | Review + acknowledge information security policy, acceptable use policy, password & MFA requirements | New Hire | SEC-001 | End of day 5 | Security (GRC) + CISO office | Three policy acknowledgements recorded in HR Hub (see [`policy-acknowledgement.md`](./policy-acknowledgement.md) POL-001) | NOT_STARTED |
| SEC-005 | Review + acknowledge AI tool acceptable use policy + complete AI coding assistant usage training | New Hire | SEC-001, [`first-week-onboarding.md`](./first-week-onboarding.md) WK1-007 | End of day 5 | Manager + Director AI/ML (Anitha Rajan) | Policy acknowledged; AI usage training completed | NOT_STARTED |
| SEC-006 | Acknowledge confidentiality agreement (NDA) + privacy acknowledgement | New Hire | DAY1-007 | End of day 2 | HRBP + CISO office | Both documents signed in HR Hub; countersigned by legal ops | NOT_STARTED |
| SEC-007 | Complete security incident reporting walkthrough — how to file, what severity means, when to call security-oncall | New Hire | SEC-001 | End of day 5 | Security (GRC) sign-off | Walkthrough attended (live or recorded); acknowledgment recorded | NOT_STARTED |
| SEC-008 | Phishing simulation drill — first simulated phishing email sent; new hire must report within 24h | Security (GRC) | SEC-001 | Within 5 business days of SEC-001 completion | CISO office | Simulation reported via the report-phishing button; outcome logged | NOT_STARTED |
| SEC-009 | Annual refresher assignment — schedule recurring annual security awareness + privacy awareness refreshers | Security (GRC) | SEC-001, SEC-002 | Day 30 | CISO office | Annual recurring assignments scheduled in HR Hub | NOT_STARTED |
| SEC-010 | Security training completion sign-off — verify SEC-001 through SEC-008 all `COMPLETED`; unlock repository write access + AI tool license | Security (GRC) | SEC-001 through SEC-008 | End of day 5 | CISO office (Rajan Mehta) | Sign-off recorded; downstream workflows notified | NOT_STARTED |

## 5. Dependencies

- **DAY1-010 blocks SEC-001, SEC-002** — The day-1 security orientation introduction is the on-ramp to the formal modules.
- **SEC-001 blocks SEC-003, SEC-004, SEC-005, SEC-007, SEC-008** — Foundational security awareness training is the prerequisite for the deeper modules.
- **SEC-001 blocks ACC-003** — Repository write access requires security training completion (canonical dependency).
- **SEC-004 blocks ACC-002** — Write repository access and elevated app access require the security policy acknowledgements (canonical dependency — see [`access-approval.md`](./access-approval.md)).
- **SEC-005 blocks WK1-009** — AI coding assistant license requires the AI tool acceptable use acknowledgement and the AI usage training.
- **SEC-005 blocks IT-009** — Engineering entitlements (Copilot seat) require SEC-005 (see [`it-provisioning.md`](./it-provisioning.md)).
- **SEC-007 → D60-005** — Incident-reporting walkthrough is a prerequisite for the on-call shadow shift.
- **SEC-010 → D30-002** — Security training completion sign-off feeds into role-specific orientation training.

## 6. Status Tracking

All SEC-* tasks are tracked in HR Hub under **Onboarding → Security**. Allowed statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

If SEC-001 or SEC-002 assessment is failed twice, the GRC Analyst assigns a 1:1 coaching session before the third attempt. If SEC-008 (phishing simulation) is not reported within 24 hours, the new hire is auto-enrolled in a remedial phishing module; a second miss triggers an HRBP conversation. SEC-010 cannot close with any of SEC-001 through SEC-008 still `IN_PROGRESS` or `BLOCKED`.

## 7. RACI Matrix

| Activity | R | A | C | I |
|---|---|---|---|---|
| Security awareness training | New Hire | Security (GRC) | HRBP | CISO office |
| Privacy awareness training | New Hire | Security (GRC) | HRBP | CISO office |
| Data classification training | New Hire | Security (GRC) | HRBP | CISO office |
| Infosec/AUP/password-MFA acknowledgement | New Hire | Security (GRC) + CISO office | HRBP | VP HR |
| AI tool acknowledgement + AI usage training | New Hire | Manager + Director AI/ML | Security | CISO office |
| NDA + privacy acknowledgement signing | New Hire | HRBP + CISO office | Legal Ops | VP HR |
| Incident reporting walkthrough | New Hire | Security (GRC) | HRBP | CISO office |
| Phishing simulation drill | Security (GRC) | CISO office | New Hire | HRBP |
| Annual refresher scheduling | Security (GRC) | CISO office | HRBP | HR Operations |
| Security training sign-off | Security (GRC) | CISO office | HRBP, IT Onboarding | VP Engineering |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 8. Key Terms

- **GRC** — Governance, Risk, and Compliance; a function within Information Security. See [`../metadata/glossary.md`](../metadata/glossary.md).
- **SOC** — Security Operations Center; the team that monitors and responds to security events.
- **MFA** — Multi-Factor Authentication; at ACME, Microsoft Authenticator.
- **PII** — Personally Identifiable Information.
- **Phishing** — fraudulent communication (typically email) attempting to extract credentials or sensitive data.
- **RBAC / ABAC** — Role-Based / Attribute-Based Access Control.

## 9. Hand-off

When SEC-001 through SEC-010 are `COMPLETED`, the CISO office issues a security training completion certificate (stored in HR Hub) and unlocks the downstream workflows: repository write access, AI tool license, and (eventually) on-call eligibility. The new hire's annual refresher schedule (SEC-009) lives in HR Hub and fires automatically thereafter.
