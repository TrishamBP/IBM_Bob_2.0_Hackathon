---
document_id: ACME-WF-003
title: First Week Onboarding Workflow
category: workflow
department: human-resources
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [workflow, onboarding, first-week]
---

# First Week Onboarding Workflow

> Fictional document. All names, emails, systems, and URLs are illustrative only.

## 1. Overview

Week one at ACME Corp turns access into momentum. The new hire moves from "I can log in" to "I have made my first commit / first ticket / first customer-shadow". The week is jointly owned by HR Operations (benefits, payroll verification, week-1 feedback) and the hiring manager (role-specific ramp, first 1:1 cadence, first contribution). Security training and policy acknowledgement are mandatory gates — repository write access and elevated app access cannot be granted until they are `COMPLETED`.

This workflow assumes [`first-day-onboarding.md`](./first-day-onboarding.md) is fully `COMPLETED`.

## 2. Scope

- **Starts:** 09:00 IST on day 2 (the business day after start date).
- **Ends:** 17:30 IST on day 5 (end of week 1).
- **Roles involved:** New Hire, Hiring Manager, Buddy, HR Onboarding Coordinator, Security (GRC), IT Onboarding, Engineering Onboarding lead.
- **Office-agnostic:** all tasks apply equally to Hyderabad, Bengaluru, London, Seattle; time zones are adjusted.

## 3. Cross-References

- Handbook: [`../00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- Employee support: [`../00-company/employee-support-and-escalation.md`](../00-company/employee-support-and-escalation.md)
- HR: [`../01-hr/benefits-enrollment-form.md`](../01-hr/benefits-enrollment-form.md), [`../01-hr/tax-declaration-form.md`](../01-hr/tax-declaration-form.md), [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md), [`../01-hr/anti-harassment-policy.md`](../01-hr/anti-harassment-policy.md)
- Security: [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md), [`../03-security/acceptable-use-policy.md`](../03-security/acceptable-use-policy.md), [`../03-security/confidentiality-agreement.md`](../03-security/confidentiality-agreement.md), [`../03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md), [`../03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- Engineering: [`../04-engineering/developer-workstation-setup.md`](../04-engineering/developer-workstation-setup.md), [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md), [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md)
- Forms: [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md), [`../08-forms/repository-access-request.md`](../08-forms/repository-access-request.md), [`../08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md), [`../08-forms/onboarding-feedback.md`](../08-forms/onboarding-feedback.md), [`../08-forms/training-completion.md`](../08-forms/training-completion.md)
- Training: [`../10-training/security-awareness.md`](../10-training/security-awareness.md), [`../10-training/privacy-awareness.md`](../10-training/privacy-awareness.md), [`../10-training/git-and-repository-workflows.md`](../10-training/git-and-repository-workflows.md), [`../10-training/ai-coding-assistant-usage.md`](../10-training/ai-coding-assistant-usage.md), [`../10-training/product-training.md`](../10-training/product-training.md), [`../10-training/workplace-conduct.md`](../10-training/workplace-conduct.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)

## 4. Week 1 Task List

| Task ID | Description | Responsible | Prerequisites | Due | Approval | Completion Criteria | Default Status |
|---|---|---|---|---|---|---|---|
| WK1-001 | Complete benefits enrollment form (medical, dental, life, provident fund nominations) | New Hire | DAY1-007 | End of day 3 | HRBP review | Form submitted in HR Hub; nominations acknowledged | NOT_STARTED |
| WK1-002 | Submit tax declaration form (India: Form 12BB; UK/US: equivalent local form) | New Hire | DAY1-007 | End of day 5 | HRBP + Finance review | Form submitted; verified against payroll system | NOT_STARTED |
| WK1-003 | Sign confidentiality agreement (NDA) and privacy acknowledgement | New Hire (with HR) | DAY1-007 | End of day 2 | HRBP + CISO office | Both documents signed in HR Hub; countersigned by legal ops | NOT_STARTED |
| WK1-004 | Acknowledge code of conduct + anti-harassment policy | New Hire | DAY1-007 | End of day 2 | HRBP | Policy acknowledgement form submitted for both policies | NOT_STARTED |
| WK1-005 | Complete security awareness training (phishing, password hygiene, data classification, MFA recovery) | New Hire | DAY1-010 | End of day 4 | Security (GRC) sign-off | Training module completed; assessment score ≥ 80% | NOT_STARTED |
| WK1-006 | Complete privacy awareness training (PII handling, data subject rights, retention) | New Hire | DAY1-010 | End of day 4 | Security (GRC) sign-off | Training module completed; assessment score ≥ 80% | NOT_STARTED |
| WK1-007 | Acknowledge information security policy + acceptable use policy + AI tool acceptable use | New Hire | WK1-005 | End of day 5 | Security (GRC) + CISO office | All three policy acknowledgements recorded in HR Hub | NOT_STARTED |
| WK1-008 | Developer workstation setup — IDE, terminal, language runtime, package manager, Docker | New Hire (with Engineering Onboarding) | DAY1-005, DAY1-006 | End of day 3 | Engineering onboarding lead | Local dev environment boots; sample app runs locally | NOT_STARTED |
| WK1-009 | AI coding assistant (GitHub Copilot Business) license request + setup | New Hire + Hiring Manager | WK1-007, WK1-008 | End of day 4 | Manager + Director AI/ML (Anitha Rajan) | License assigned in GitHub Enterprise; IDE plugin authenticated | NOT_STARTED |
| WK1-010 | First commit — clone primary repo, create a `docs/onboarding/<username>.md` "about me" stub, push, open PR | New Hire | WK1-005, WK1-008 | End of day 5 | Manager + repo CODEOWNERS | PR merged; commit visible on `git.acme.example` | NOT_STARTED |
| WK1-011 | Attend team standups every day (Mon–Fri) | New Hire | DAY1-011 | Daily, 09:30 IST | Manager | New hire present at all standups in week 1 | NOT_STARTED |
| WK1-012 | Product overview session — assigned product(s), customer personas, architecture 101 | Hiring Manager + Product Manager | DAY1-008 | End of day 5 | Manager | Session attended; product overview notes shared with new hire | NOT_STARTED |
| WK1-013 | Begin role-specific training per `../05-teams/<role>-onboarding.md` (engineering roles → engineering orientation; non-engineering → product training) | New Hire | WK1-008 or DAY1-008 | End of day 5 | Manager | Role-specific training checklist item 1 `COMPLETED` | NOT_STARTED |
| WK1-014 | Weekly 1:1 with manager — week-1 retro, blockers, week-2 plan | Hiring Manager | DAY1-008 | End of day 5 | Manager | 1:1 held; notes saved in manager's 1:1 doc | NOT_STARTED |
| WK1-015 | Week-1 feedback form | New Hire | DAY1-012 | End of day 5 | HRBP | Feedback form submitted in HR Hub | NOT_STARTED |

## 5. Dependencies

- **WK1-005 blocks WK1-007** — The new hire cannot acknowledge the information security policy until they have completed security awareness training (so the acknowledgement is informed).
- **WK1-007 blocks WK1-009** — AI coding assistant license requires the AI tool acceptable use acknowledgement.
- **WK1-007 blocks ACC-002** — Write repository access requires the security + AI tool policy acknowledgements (see [`access-approval.md`](./access-approval.md)).
- **WK1-005 blocks ACC-003** — Repository write access requires security training completion (see [`access-approval.md`](./access-approval.md)).
- **WK1-008 blocks WK1-010** — Cannot make a first commit without a working dev environment.
- **WK1-005 blocks WK1-010** — Cannot push to a repo without security training completion (gated by repository webhook).
- **WK1-009 blocks D30-001** — The 30-day review includes "first merged PR using Copilot where appropriate" — Copilot must be set up first.
- **WK1-013 → D30-001** — Role-specific training carries over to the 30-day milestone.
- **DAY1-010 → WK1-005, WK1-006** — The day-1 security orientation introduction precedes the formal security + privacy training modules.

## 6. Status Tracking

All WK1-* tasks are tracked in HR Hub under **Onboarding → Week 1**. Allowed statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

If the new hire does not complete WK1-005 (security training) by end of day 4, repository write access (gated on the GitHub Enterprise side) remains read-only and the new hire cannot merge PRs. IT will not extend the deadline — the new hire's manager must reschedule or escalate to the HRBP for a documented exception.

## 7. RACI Matrix

| Activity | R | A | C | I |
|---|---|---|---|---|
| Benefits enrollment | New Hire | HRBP | Finance | VP HR |
| Tax declaration | New Hire | HRBP + Finance | HR Onboarding Coordinator | VP HR |
| NDA + privacy acknowledgement | New Hire (with HR) | HRBP + CISO office | Legal Ops | VP HR |
| Code of conduct + anti-harassment ack | New Hire | HRBP | HR Onboarding Coordinator | VP HR |
| Security awareness training | New Hire | Security (GRC) | HRBP | CISO office |
| Privacy awareness training | New Hire | Security (GRC) | HRBP | CISO office |
| Infosec + AUP + AI-tool ack | New Hire | Security (GRC) + CISO office | HRBP | VP HR |
| Dev workstation setup | New Hire (with Eng Onboarding) | Engineering onboarding lead | IT Onboarding | VP Engineering |
| AI assistant license request | New Hire + Hiring Manager | Manager + Director AI/ML | Security | VP Engineering |
| First commit | New Hire | Manager + CODEOWNERS | Buddy | VP Engineering |
| Product overview | Hiring Manager + Product Manager | Hiring Manager | New Hire | VP Engineering |
| Role-specific training start | New Hire | Manager | Buddy | HRBP |
| Weekly 1:1 | Hiring Manager | Hiring Manager | New Hire | HRBP |
| Week-1 feedback | New Hire | HRBP | Hiring Manager | VP HR |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 8. Key Terms

- **PR** — Pull Request; the unit of code review at ACME. See [`../metadata/glossary.md`](../metadata/glossary.md).
- **CODEOWNERS** — file in a repo declaring which teams own which paths.
- **CI/CD** — Continuous Integration / Continuous Delivery.
- **GRC** — Governance, Risk, and Compliance; a function within Information Security.
- **JIT** — Just-In-Time access; temporary elevated access for a specific task.
- **Buddy review** — a non-blocking review from a peer, distinct from a formal CODEOWNERS review.

## 9. Hand-off to First 30 Days

When WK1-001 through WK1-015 are `COMPLETED`, the HR Onboarding Coordinator closes week 1 and hands off to [`first-30-days.md`](./first-30-days.md). A summary email lists: training completion certificates, policy acknowledgements on file, first commit URL, role-specific training progress percentage, and any carry-over items (e.g., benefits enrollment pending bank verification).
