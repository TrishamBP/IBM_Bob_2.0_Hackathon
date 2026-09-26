---
document_id: ACME-WF-006
title: First 90 Days Workflow
category: workflow
department: human-resources
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [workflow, onboarding, first-90-days, probation]
---

# First 90 Days Workflow

> Fictional document. All names, emails, systems, and URLs are illustrative only.

## 1. Overview

Days 61-90 close out the probation period at ACME Corp. The new hire takes their first primary on-call shift (for engineering and support roles), receives a final probation review, completes the 90-day feedback, and — if the review is positive — receives a confirmation letter converting them from probationary to confirmed employee. The confirmation letter is issued by Ananya Sharma (VP HR) on the recommendation of the hiring manager and HRBP.

This workflow assumes [`first-60-days.md`](./first-60-days.md) is fully `COMPLETED` (D60-008 HRBP sign-off recorded).

## 2. Scope

- **Starts:** Day 61.
- **Ends:** Day 90 (or the next business day if day 90 falls on a weekend/holiday).
- **Roles involved:** New Hire, Hiring Manager, HRBP, On-call lead, CISO office (for on-call verification), VP HR (Ananya Sharma).
- **Probation outcomes:** Confirmed (most common), extended probation (rare, requires HRBP + VP HR approval), or separation (extremely rare; follows [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md)).

## 3. Cross-References

- Handbook: [`../00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- HR: [`../01-hr/probation-and-confirmation-process.md`](../01-hr/probation-and-confirmation-process.md), [`../01-hr/performance-review-policy.md`](../01-hr/performance-review-policy.md), [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md)
- Engineering: [`../04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md)
- Forms: [`../08-forms/onboarding-feedback.md`](../08-forms/onboarding-feedback.md), [`../08-forms/manager-approval.md`](../08-forms/manager-approval.md)
- Training: [`../10-training/product-training.md`](../10-training/product-training.md), [`../10-training/workplace-conduct.md`](../10-training/workplace-conduct.md)
- Contacts: [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)

## 4. Days 61-90 Task List

| Task ID | Description | Responsible | Prerequisites | Due | Approval | Completion Criteria | Default Status |
|---|---|---|---|---|---|---|---|
| D90-001 | Final probation review meeting — comprehensive review against role expectations, contributions, feedback, training completion | Hiring Manager + New Hire + HRBP | D60-008 | Day 85 | Manager + HRBP + skip-level director | Review held; recommendation recorded (confirm / extend / separate) | NOT_STARTED |
| D90-002 | Workplace conduct refresher training — anti-harassment, code of conduct scenarios, escalation channels | New Hire | WK1-004 | Day 75 | HRBP | Training module completed; assessment passed | NOT_STARTED |
| D90-003 | Primary on-call shift (engineering and support roles only) — new hire is primary on-call for one full rotation with on-call lead as backup | New Hire + On-call lead | D60-005 | Day 80 | Manager + CISO office (Rajan Mehta) | Shift completed; any incidents handled per playbook; debrief filed | NOT_STARTED |
| D90-004 | 90-day feedback form — new hire rates full onboarding experience; manager rates ramp + cultural fit | New Hire + Hiring Manager | D90-001 | Day 90 | HRBP | Two feedback forms submitted in HR Hub | NOT_STARTED |
| D90-005 | Manager recommendation form — manager formally recommends confirm / extend / separate with rationale | Hiring Manager | D90-001 | Day 87 | Manager + skip-level director | Form submitted in HR Hub; routed to HRBP | NOT_STARTED |
| D90-006 | HRBP + VP HR review of recommendation — decision recorded, comments attached | HRBP (Kavya / Deepika / Sanjay) + VP HR (Ananya Sharma) | D90-005 | Day 90 | VP HR | Decision recorded in HR Hub | NOT_STARTED |
| D90-007 | Issue confirmation letter (if approved) — signed by VP HR, countersigned by new hire | HR Operations (Priya Nair) | D90-006 | Day 90 (or next business day) | VP HR | Letter issued in HR Hub; employee countersigns | NOT_STARTED |
| D90-008 | HRBP sign-off on 90-day file — verify all D90-* tasks `COMPLETED`; trigger archival | HRBP | D90-001 through D90-007 | Day 90 | HRBP | 90-day file closed; carry-over (e.g., extended probation) documented | NOT_STARTED |

## 5. Dependencies

- **D60-008 blocks D90-001** — HRBP 60-day sign-off gates entry to the 90-day phase.
- **D60-005 blocks D90-003** — Primary on-call shift requires the day-60 on-call shadow to be complete.
- **D90-001 blocks D90-004, D90-005, D90-008** — The final probation review is the prerequisite for the feedback, the manager recommendation, and the HRBP sign-off.
- **D90-005 blocks D90-006** — VP HR cannot review a recommendation that has not been submitted.
- **D90-006 blocks D90-007** — The confirmation letter cannot be issued until the decision is recorded.
- **D90-007 → CMP-001** — The confirmation letter is one of the artifacts reviewed in [`onboarding-completion.md`](./onboarding-completion.md).
- **D90-008 → CMP-001** — HRBP 90-day sign-off is a precondition for onboarding completion.

## 6. Status Tracking

All D90-* tasks are tracked in HR Hub under **Onboarding → First 90 Days**. Allowed statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

If D90-006 records an "extend probation" decision, the HRBP opens an extension record with a defined end date (typically 30-60 days) and the file stays `IN_PROGRESS` past day 90; the HRBP documents the extension in the new hire's record. If D90-006 records a "separate" decision, the HRBP immediately routes the file to [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) and the IT revocation workflow in [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md).

D90-003 (primary on-call) is conditional for engineering and support roles only; for other roles it is marked `COMPLETED` at workflow start with the note "Not applicable to role".

## 7. RACI Matrix

| Activity | R | A | C | I |
|---|---|---|---|---|
| Final probation review | Hiring Manager + New Hire + HRBP | Manager + HRBP + skip-level director | Buddy | VP HR |
| Workplace conduct refresher | New Hire | HRBP | Security | VP HR |
| Primary on-call shift (eng + support) | New Hire + on-call lead | Manager + CISO office | Security (GRC) | VP Engineering |
| 90-day feedback | New Hire + Hiring Manager | HRBP | Buddy | VP HR |
| Manager recommendation | Hiring Manager | Manager + skip-level director | HRBP | VP HR |
| VP HR decision | HRBP + VP HR | VP HR | Manager | Skip-level director |
| Confirmation letter | HR Operations | VP HR | New Hire | VP HR |
| 90-day sign-off | HRBP | HRBP | Manager, IT, Security | VP HR |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 8. Key Terms

- **Probation** — initial employment period (typically 90 days) before confirmation as a permanent employee. See [`../01-hr/probation-and-confirmation-process.md`](../01-hr/probation-and-confirmation-process.md).
- **On-call** — the engineer currently responsible for responding to incidents for a team. See [`../metadata/glossary.md`](../metadata/glossary.md).
- **SEV1 / SEV2 / SEV3** — incident severity levels (1 = highest).
- **Runbook** — a documented procedure for operating a service, especially during incidents.
- **HRBP** — HR Business Partner.
- **Skip-level** — the manager's manager (typically a Director).

## 9. Hand-off to Onboarding Completion

When D90-001 through D90-008 are `COMPLETED`, the HRBP closes the 90-day file and hands off to [`onboarding-completion.md`](./onboarding-completion.md). The hand-off summary includes: confirmation letter reference number, on-call shift debrief notes, 90-day rating, and any carry-over items (e.g., extended probation, outstanding training debt).
