---
document_id: ACME-WF-007
title: Manager Onboarding Responsibilities Workflow
category: workflow
department: human-resources
applicable_roles: [managers]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [workflow, onboarding, manager-responsibilities]
---

# Manager Onboarding Responsibilities Workflow

> Fictional document. All names, emails, systems, and URLs are illustrative only.

## 1. Overview

The hiring manager is the single accountable owner of a new hire's onboarding experience from offer acceptance through day 90. While HR, IT, and Security own specific execution steps, the manager owns: (a) the buddy assignment, (b) the access request list, (c) the recurring 1:1 cadence, (d) the 30/60/90-day reviews, and (e) the confirmation recommendation. This workflow consolidates those responsibilities into one place so that managers — especially first-time managers at ACME — have a single checklist to follow.

The Director AI/ML (Anitha Rajan — `anitha.rajan@acme.example`) and VP Engineering / CTO (Sridhar Venkatesh — `sridhar.venkatesh@acme.example`) own skip-level review of recommendations at day 90. HR Operations owns tracking of manager tasks.

## 2. Scope

- **Starts:** Offer acceptance.
- **Ends:** Day 90 (or the next business day if day 90 falls on a weekend/holiday).
- **Roles involved:** Hiring Manager, HRBP, Buddy (peer), Skip-level director, VP HR.
- **Office-agnostic.**

## 3. Cross-References

- Handbook: [`../00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- Org structure: [`../00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- Employee support: [`../00-company/employee-support-and-escalation.md`](../00-company/employee-support-and-escalation.md)
- HR: [`../01-hr/probation-and-confirmation-process.md`](../01-hr/probation-and-confirmation-process.md), [`../01-hr/performance-review-policy.md`](../01-hr/performance-review-policy.md), [`../01-hr/welcome-letter.md`](../01-hr/welcome-letter.md)
- IT: [`../02-it/new-employee-it-request.md`](../02-it/new-employee-it-request.md), [`../02-it/laptop-and-workstation-allocation.md`](../02-it/laptop-and-workstation-allocation.md)
- Security: [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md), [`../03-security/acceptable-use-policy.md`](../03-security/acceptable-use-policy.md)
- Engineering: [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md), [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md)
- Team onboarding: `../05-teams/<role>-onboarding.md`
- Forms: [`../08-forms/manager-approval.md`](../08-forms/manager-approval.md), [`../08-forms/repository-access-request.md`](../08-forms/repository-access-request.md), [`../08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md), [`../08-forms/onboarding-feedback.md`](../08-forms/onboarding-feedback.md), [`../08-forms/access-review.md`](../08-forms/access-review.md)
- Contacts: [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)

## 4. Manager Task List

| Task ID | Description | Responsible | Prerequisites | Due | Approval | Completion Criteria | Default Status |
|---|---|---|---|---|---|---|---|
| MGR-001 | Submit preboarding checklist (role, team, equipment spec, repo list, first-week shadow plan) — see [`preboarding.md`](./preboarding.md) PRE-010 | Hiring Manager | Offer acceptance | 5 business days before start date | Skip-level director | Checklist submitted in HR Hub | NOT_STARTED |
| MGR-002 | Assign onboarding buddy (peer, not manager) — see [`preboarding.md`](./preboarding.md) PRE-007 | Hiring Manager | MGR-001 | 5 business days before start date | Manager | Buddy named in HR Hub; buddy-guide email sent | NOT_STARTED |
| MGR-003 | Approve access request list (repos, vault paths, package feeds, cloud subscriptions) for IT/Security provisioning | Hiring Manager | MGR-001, [`access-approval.md`](./access-approval.md) ACC-001 | 3 business days before start date | Manager + skip-level director (for elevated access) | Repository access request forms submitted; approved in HR Hub | NOT_STARTED |
| MGR-004 | Prepare day-1 1:1 agenda and 30-day plan — see [`first-day-onboarding.md`](./first-day-onboarding.md) DAY1-008 | Hiring Manager | MGR-001 | Day 1 by 09:00 IST | None | Agenda + 30-day plan doc ready in manager's 1:1 folder | NOT_STARTED |
| MGR-005 | Hold day-1 1:1 — see [`first-day-onboarding.md`](./first-day-onboarding.md) DAY1-008 | Hiring Manager | MGR-004, DAY1-003 | Day 1 by 14:00 IST | None | 1:1 held; 30-day plan shared; recurring weekly 1:1 scheduled | NOT_STARTED |
| MGR-006 | Schedule recurring weekly 1:1 (default: 30 minutes, same time each week) | Hiring Manager | MGR-005 | Day 1 by 17:00 IST | None | Recurring calendar series created through day 90 | NOT_STARTED |
| MGR-007 | Introduce new hire in team channel + team standup — see [`first-day-onboarding.md`](./first-day-onboarding.md) DAY1-011 | Hiring Manager | DAY1-003 | Day 1 by 16:30 IST | None | Introduction message posted; new hire attended standup | NOT_STARTED |
| MGR-008 | Define and assign role-specific first-contribution task — see [`first-30-days.md`](./first-30-days.md) D30-005/D30-006/D30-007/D30-008 | Hiring Manager | WK1-013 | Day 7 | None | First-contribution task documented in 1:1 doc; mentor named | NOT_STARTED |
| MGR-009 | Hold week-1 1:1 retro — see [`first-week-onboarding.md`](./first-week-onboarding.md) WK1-014 | Hiring Manager | MGR-006 | Day 5 by 17:30 IST | None | Retro notes saved; week-2 plan shared | NOT_STARTED |
| MGR-010 | Hold 30-day review — see [`first-30-days.md`](./first-30-days.md) D30-001 | Hiring Manager | D30-002, D30-003 | Day 30 | Manager + HRBP | Review held; rating recorded | NOT_STARTED |
| MGR-011 | Conduct 30-day access review — see [`first-30-days.md`](./first-30-days.md) D30-003 | Hiring Manager | [`access-approval.md`](./access-approval.md) ACC-008 cadence | Day 25 | Manager + IT Manager Hyderabad (Arjun Kapoor) | Access review form submitted | NOT_STARTED |
| MGR-012 | Hold 60-day review — see [`first-60-days.md`](./first-60-days.md) D60-001 | Hiring Manager | D30-010 | Day 60 | Manager + HRBP | Review held; rating recorded | NOT_STARTED |
| MGR-013 | Hold final 90-day probation review — see [`first-90-days.md`](./first-90-days.md) D90-001 | Hiring Manager + HRBP | D60-008 | Day 85 | Manager + HRBP + skip-level director | Review held; recommendation recorded | NOT_STARTED |
| MGR-014 | Submit manager recommendation form (confirm / extend / separate) — see [`first-90-days.md`](./first-90-days.md) D90-005 | Hiring Manager | MGR-013 | Day 87 | Skip-level director | Form submitted in HR Hub | NOT_STARTED |
| MGR-015 | Submit manager onboarding feedback form — what worked, what didn't, suggestions for HR/IT/Security | Hiring Manager | D90-007 | Day 90 | HRBP | Feedback form submitted in HR Hub | NOT_STARTED |

## 5. Dependencies

- **MGR-001 blocks PRE-005, PRE-006** — IT cannot stage equipment or the M365 identity without the manager checklist (see [`preboarding.md`](./preboarding.md) dependencies).
- **MGR-001 blocks MGR-002, MGR-003, MGR-004** — The checklist is the master input.
- **MGR-002 blocks PRE-008** — The day-1 calendar invite names the buddy, so buddy assignment must happen first.
- **MGR-003 blocks ACC-002, ACC-003** — Write repository access and elevated app access require the manager-approved access request list (see [`access-approval.md`](./access-approval.md)).
- **MGR-003 blocks IT-001** — Manager approval precedes IT provisioning starts (see [`it-provisioning.md`](./it-provisioning.md)).
- **MGR-005 blocks MGR-006** — The recurring 1:1 cadence is scheduled after the day-1 1:1 establishes the cadence rhythm.
- **WK1-013 blocks MGR-008** — The first-contribution task can only be defined once role-specific training has begun.
- **MGR-010 → MGR-012 → MGR-013** — The 30/60/90-day reviews form a chain; each is the prerequisite for the next.
- **MGR-013 blocks MGR-014** — The recommendation follows the review.

## 6. Status Tracking

All MGR-* tasks are tracked in HR Hub under **Onboarding → Manager Responsibilities**. Allowed statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

If the manager is on leave for any phase transition, the skip-level director is the automatic delegate; the manager must nominate an alternate in the HR Hub record before going on leave. A phase transition with no owner present triggers an HRBP escalation and a brief pause of the file (not a reset).

## 7. RACI Matrix

| Activity | R | A | C | I |
|---|---|---|---|---|
| Preboarding checklist | Hiring Manager | Skip-level director | HRBP, IT Onboarding | VP HR |
| Buddy assignment | Hiring Manager | Hiring Manager | Buddy, HRBP | New Hire |
| Access request list | Hiring Manager | Manager + skip-level director (elevated) | IT Onboarding, Security | VP HR |
| Day-1 1:1 agenda + 30-day plan | Hiring Manager | Hiring Manager | HRBP | New Hire |
| Day-1 1:1 | Hiring Manager | Hiring Manager | New Hire | HRBP |
| Recurring weekly 1:1 | Hiring Manager | Hiring Manager | New Hire | HRBP |
| Team introduction | Hiring Manager | Hiring Manager | Buddy, New Hire | HRBP |
| First-contribution task | Hiring Manager | Manager | Buddy, mentor | VP Engineering |
| Week-1 1:1 retro | Hiring Manager | Hiring Manager | New Hire | HRBP |
| 30/60/90-day reviews | Hiring Manager + New Hire | Manager + HRBP | Buddy | VP HR |
| Recommendation form | Hiring Manager | Manager + skip-level director | HRBP | VP HR |
| Manager onboarding feedback | Hiring Manager | HRBP | HR Operations | VP HR |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 8. Key Terms

- **Onboarding plan** — the 30/60/90-day plan a manager creates for a new hire. See [`../metadata/glossary.md`](../metadata/glossary.md).
- **Buddy** — a peer (not the manager) assigned to support a new hire's first 90 days.
- **Skip-level** — the manager's manager (typically a Director).
- **HRBP** — HR Business Partner.
- **CODEOWNERS** — file in a repo declaring which teams own which paths.
- **OKR** — Objectives and Key Results; ACME's quarterly goal framework.

## 9. Hand-off

When MGR-001 through MGR-015 are `COMPLETED` and D90-007 (confirmation letter) is issued, the manager's responsibilities for this new hire are complete. The HRBP moves the file to [`onboarding-completion.md`](./onboarding-completion.md) for archival. The manager's ongoing (non-onboarding) responsibilities — annual performance review, quarterly 1:1 cadence — are governed by [`../01-hr/performance-review-policy.md`](../01-hr/performance-review-policy.md) and not by this workflow.
