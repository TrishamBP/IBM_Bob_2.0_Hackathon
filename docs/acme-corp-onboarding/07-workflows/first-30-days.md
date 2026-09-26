---
document_id: ACME-WF-004
title: First 30 Days Workflow
category: workflow
department: human-resources
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [workflow, onboarding, first-30-days]
---

# First 30 Days Workflow

> Fictional document. All names, emails, systems, and URLs are illustrative only.

## 1. Overview

The first 30 days at ACME Corp are about the new hire's first meaningful contribution in their role. Each role has a different definition of "first contribution" — engineers ship their first merged PR; PMs write their first PRD section; designers ship their first reviewed Figma frame; sales reps shadow their first customer call; support engineers handle their first assigned ticket; cloud platform engineers deploy their first config change to staging.

This workflow assumes [`first-week-onboarding.md`](./first-week-onboarding.md) is fully `COMPLETED`. The hiring manager is the primary owner of the 30-day period. HR Operations owns the 30-day review and the 30-day feedback.

## 2. Scope

- **Starts:** Day 6 (first business day after week 1).
- **Ends:** End of day 30.
- **Roles involved:** New Hire, Hiring Manager, Buddy, HRBP, role-specific senior peer (shadowing partner).
- **Roles covered:** All. Role-specific first-contribution tasks (D30-005 through D30-008) are conditional — only the one matching the new hire's role applies.

## 3. Cross-References

- Handbook: [`../00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- Org structure: [`../00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- HR: [`../01-hr/probation-and-confirmation-process.md`](../01-hr/probation-and-confirmation-process.md), [`../01-hr/performance-review-policy.md`](../01-hr/performance-review-policy.md)
- Engineering: [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md), [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md)
- Team onboarding: `../05-teams/<role>-onboarding.md`
- Forms: [`../08-forms/onboarding-feedback.md`](../08-forms/onboarding-feedback.md), [`../08-forms/training-completion.md`](../08-forms/training-completion.md), [`../08-forms/access-review.md`](../08-forms/access-review.md)
- Training: [`../10-training/engineering-orientation.md`](../10-training/engineering-orientation.md), [`../10-training/cloud-platform-fundamentals.md`](../10-training/cloud-platform-fundamentals.md), [`../10-training/product-training.md`](../10-training/product-training.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)

## 4. Days 1-30 Task List

| Task ID | Description | Responsible | Prerequisites | Due | Approval | Completion Criteria | Default Status |
|---|---|---|---|---|---|---|---|
| D30-001 | 30-day review meeting — progress vs 30-day plan, role clarity, blockers, training completion | Hiring Manager + New Hire | WK1-014 | Day 30 | Manager + HRBP | Review held; notes saved in HR Hub; rating recorded (on-track / needs-attention) | NOT_STARTED |
| D30-002 | Complete role-specific orientation training (engineering orientation / cloud platform fundamentals / product training) | New Hire | WK1-013 | Day 20 | Manager | Training module completed; assessment passed | NOT_STARTED |
| D30-003 | Access review — confirm least-privilege access is appropriate, retire any unused read grants | Hiring Manager + IT Onboarding | WK1-007, [`access-approval.md`](./access-approval.md) | Day 25 | Manager + IT Manager Hyderabad (Arjun Kapoor) | Access review form submitted; any retirements actioned | NOT_STARTED |
| D30-004 | Establish recurring weekly 1:1 cadence with buddy → transition buddy 1:1s to monthly | Hiring Manager + Buddy | WK1-014 | Day 10 | Manager | Weekly 1:1s scheduled through day 30; monthly cadence set from day 31 | NOT_STARTED |
| D30-005 | (Engineers only) First merged PR — code reviewed by a senior peer, passing CI/CD, deployed to staging | New Hire | WK1-009, WK1-010 | Day 25 | CODEOWNERS + Manager | PR merged; deployment to staging verified | NOT_STARTED |
| D30-006 | (Product Managers only) First PRD section — drafted, reviewed by EM + design, accepted into the planning backlog | New Hire | WK1-012, D30-002 | Day 25 | Manager + Design Director | PRD section accepted in planning tool | NOT_STARTED |
| D30-007 | (Sales reps only) First customer call — shadowed with senior AE, debrief, CRM notes authored | New Hire | WK1-012, D30-002 | Day 30 | Manager + Sales enablement | Call shadowed; debrief notes filed in CRM | NOT_STARTED |
| D30-008 | (Support / QE / Cloud Platform roles only) First assigned ticket / first config change — pair-reviewed, closed within SLA | New Hire | D30-002 | Day 25 | Manager + on-call lead | Ticket closed or config deployed to staging; review passed | NOT_STARTED |
| D30-009 | 30-day feedback form — new hire rates onboarding experience, manager rates ramp | New Hire + Hiring Manager | D30-001 | Day 30 | HRBP | Two feedback forms submitted in HR Hub | NOT_STARTED |
| D30-010 | HRBP sign-off on 30-day file — verify training, policy acknowledgements, access, first contribution, feedback all `COMPLETED` | HRBP | D30-001, D30-002, D30-003, D30-009 | Day 30 | HRBP | 30-day file closed in HR Hub; carry-over list documented | NOT_STARTED |

## 5. Dependencies

- **WK1-009 blocks D30-005** — Engineers cannot merge a PR using GitHub Copilot until the Copilot license is set up (which itself requires WK1-007 policy acknowledgement).
- **WK1-013 → D30-002** — Role-specific orientation training continues from the week-1 start.
- **D30-002 blocks D30-005, D30-006, D30-007, D30-008** — The first-contribution tasks all require role-specific training completion.
- **D30-001 blocks D30-009, D30-010** — The 30-day review is the prerequisite for both the feedback form and the HRBP sign-off.
- **D30-003 → ACC-008 (quarterly access review)** — The 30-day access review feeds into the quarterly cadence in [`access-approval.md`](./access-approval.md).
- **D30-010 → D60-001** — HRBP 30-day sign-off gates entry to the 60-day phase; if any item is `BLOCKED`, the file is held and the HRBP escalates to Ananya Sharma (VP HR).

## 6. Status Tracking

All D30-* tasks are tracked in HR Hub under **Onboarding → First 30 Days**. Allowed statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

If D30-001 (30-day review) cannot be held on day 30 because the new hire is off (leave, holiday), the manager reschedules within 5 business days and the file stays `IN_PROGRESS` until completed. A 30-day review held more than 10 business days late triggers an HRBP escalation.

## 7. RACI Matrix

| Activity | R | A | C | I |
|---|---|---|---|---|
| 30-day review | Hiring Manager + New Hire | Manager + HRBP | Buddy | VP HR |
| Role-specific orientation training | New Hire | Manager | Engineering onboarding lead | HRBP |
| Access review | Hiring Manager + IT Onboarding | Manager + IT Manager Hyderabad | Security (GRC) | CISO office |
| Buddy 1:1 cadence change | Hiring Manager + Buddy | Manager | New Hire | HRBP |
| First merged PR (engineers) | New Hire | CODEOWNERS + Manager | Buddy | VP Engineering |
| First PRD section (PMs) | New Hire | Manager + Design Director | Product Manager | VP Engineering |
| First customer call shadow (sales) | New Hire | Manager + Sales enablement | Senior AE | VP Sales |
| First ticket / config (support/QE/cloud) | New Hire | Manager + on-call lead | Buddy | VP Engineering |
| 30-day feedback | New Hire + Hiring Manager | HRBP | Buddy | VP HR |
| 30-day sign-off | HRBP | HRBP | Manager, IT, Security | VP HR |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 8. Key Terms

- **Onboarding plan** — the 30/60/90-day plan a manager creates for a new hire. See [`../metadata/glossary.md`](../metadata/glossary.md).
- **PR** — Pull Request; the unit of code review at ACME.
- **PRD** — Product Requirements Document.
- **CODEOWNERS** — file in a repo declaring which teams own which paths.
- **AE** — Account Executive (sales role).
- **SLA** — Service-Level Agreement.

## 9. Hand-off to First 60 Days

When D30-001 through D30-010 are `COMPLETED`, the HRBP closes the 30-day file and hands off to [`first-60-days.md`](./first-60-days.md). The hand-off summary includes: 30-day rating, first-contribution URL/ticket ID, role-specific training completion certificate, access review delta, and any carry-over items.
