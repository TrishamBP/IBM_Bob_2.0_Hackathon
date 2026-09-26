---
document_id: ACME-WF-005
title: First 60 Days Workflow
category: workflow
department: human-resources
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [workflow, onboarding, first-60-days]
---

# First 60 Days Workflow

> Fictional document. All names, emails, systems, and URLs are illustrative only.

## 1. Overview

Days 31-60 at ACME Corp move the new hire from "first contribution" to "first feature-sized change" and "first independent ownership". Engineers participate in code reviews as reviewers (not just submitters), ship a feature-sized change, and shadow an on-call shift. Non-engineering roles ship their equivalent feature-sized milestone: PMs own a small epic; designers ship a feature flow; sales reps run their first independent discovery call; support engineers own a queue segment for a week; cloud platform engineers ship a production config change under shadow.

This workflow assumes [`first-30-days.md`](./first-30-days.md) is fully `COMPLETED` (D30-010 HRBP sign-off recorded).

## 2. Scope

- **Starts:** Day 31.
- **Ends:** End of day 60.
- **Roles involved:** New Hire, Hiring Manager, Buddy (now monthly cadence), Senior peer (code-review mentor for engineers), On-call lead (for shadow).
- **Office-agnostic.**

## 3. Cross-References

- Handbook: [`../00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- Org structure: [`../00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- HR: [`../01-hr/probation-and-confirmation-process.md`](../01-hr/probation-and-confirmation-process.md), [`../01-hr/performance-review-policy.md`](../01-hr/performance-review-policy.md)
- Engineering: [`../04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md), [`../04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md)
- Team onboarding: `../05-teams/<role>-onboarding.md`
- Forms: [`../08-forms/onboarding-feedback.md`](../08-forms/onboarding-feedback.md), [`../08-forms/training-completion.md`](../08-forms/training-completion.md)
- Training: [`../10-training/cloud-platform-fundamentals.md`](../10-training/cloud-platform-fundamentals.md), [`../10-training/product-training.md`](../10-training/product-training.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)

## 4. Days 31-60 Task List

| Task ID | Description | Responsible | Prerequisites | Due | Approval | Completion Criteria | Default Status |
|---|---|---|---|---|---|---|---|
| D60-001 | 60-day review meeting — progress vs 60-day plan, ownership scope, blockers, on-call readiness | Hiring Manager + New Hire | D30-010 | Day 60 | Manager + HRBP | Review held; notes saved in HR Hub; rating recorded | NOT_STARTED |
| D60-002 | Code-review participation (engineers): review at least 3 PRs from peers, with substantive comments accepted by authors | New Hire | D30-005 | Day 55 | CODEOWNERS + Manager | 3 reviewed PRs listed; at least 2 with accepted substantive comments | NOT_STARTED |
| D60-003 | First feature-sized change (engineers): a multi-file change spanning 2+ days of work, with tests, deployed to staging | New Hire | D30-005, D60-002 | Day 60 | CODEOWNERS + Manager | Feature PR merged; tests pass; deployed to staging | NOT_STARTED |
| D60-004 | First independent ownership milestone (non-engineering roles): PM owns a small epic; designer ships a feature flow; sales rep runs a discovery call; support owns a queue segment for a week; cloud platform engineer ships a production config change under shadow | New Hire | D30-005 / D30-006 / D30-007 / D30-008 (whichever applied) | Day 60 | Manager + relevant function director | Milestone artifact (epic link / Figma link / call recording / queue report / config PR) attached | NOT_STARTED |
| D60-005 | On-call shadow shift (engineering and support roles only): shadow primary on-call for one full shift; attend incident simulation drill | New Hire + On-call lead | D30-002, [`../03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md) | Day 50 | Manager + CISO office (Rajan Mehta) | Shadow completed; drill attended; debrief notes filed | NOT_STARTED |
| D60-006 | Cloud platform fundamentals certification (if role requires — cloud platform engineers, devops, SRE-adjacent) | New Hire | D30-002 | Day 55 | Director AI/ML (Anitha Rajan) or VP Engineering | Certification passed; certificate stored in HR Hub | NOT_STARTED |
| D60-007 | 60-day feedback form — new hire + manager | New Hire + Hiring Manager | D60-001 | Day 60 | HRBP | Two feedback forms submitted in HR Hub | NOT_STARTED |
| D60-008 | HRBP sign-off on 60-day file — verify all D60-* tasks `COMPLETED`; confirm no open policy/training/access debt | HRBP | D60-001 through D60-007 (excluding conditional) | Day 60 | HRBP | 60-day file closed; carry-over list documented | NOT_STARTED |

## 5. Dependencies

- **D30-010 blocks D60-001** — The HRBP 30-day sign-off gates entry to the 60-day phase.
- **D30-005 blocks D60-002, D60-003** — Engineers cannot review others' PRs or ship a feature-sized change without their own first merged PR.
- **D60-002 blocks D60-003** — Engineering practice at ACME requires new hires to participate in code reviews (as reviewer) before submitting a feature-sized change of their own — this ensures exposure to house style.
- **D30-002 blocks D60-006** — Cloud platform fundamentals training must be complete before taking the certification.
- **D60-005 → D90-003** — On-call shadow is a prerequisite for the primary on-call shift in the 90-day phase.
- **D60-008 → D90-001** — HRBP 60-day sign-off gates entry to the 90-day phase.

## 6. Status Tracking

All D60-* tasks are tracked in HR Hub under **Onboarding → First 60 Days**. Allowed statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

Conditional tasks (D60-002, D60-003, D60-005, D60-006) for roles where they do not apply are marked `COMPLETED` at workflow start with a note "Not applicable to role" — they do not block D60-008 sign-off. The HRBP verifies applicability against the role definition in `../05-teams/<role>-onboarding.md`.

If D60-005 (on-call shadow) cannot be scheduled within the window because the team is in a release freeze, the on-call lead schedules the shadow within 10 business days of day 60; D60-008 may close with D60-005 explicitly `BLOCKED` and a documented reason.

## 7. RACI Matrix

| Activity | R | A | C | I |
|---|---|---|---|---|
| 60-day review | Hiring Manager + New Hire | Manager + HRBP | Buddy | VP HR |
| Code-review participation (engineers) | New Hire | CODEOWNERS + Manager | Buddy | VP Engineering |
| First feature-sized change (engineers) | New Hire | CODEOWNERS + Manager | Buddy | VP Engineering |
| First independent ownership (non-engineering) | New Hire | Manager + relevant function director | Buddy | VP Engineering / VP Sales |
| On-call shadow shift (eng + support) | New Hire + on-call lead | Manager + CISO office | Security (GRC) | VP Engineering |
| Cloud platform fundamentals cert | New Hire | Director AI/ML or VP Engineering | Engineering onboarding lead | HRBP |
| 60-day feedback | New Hire + Hiring Manager | HRBP | Buddy | VP HR |
| 60-day sign-off | HRBP | HRBP | Manager, IT, Security | VP HR |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 8. Key Terms

- **On-call** — the engineer currently responsible for responding to incidents for a team. See [`../metadata/glossary.md`](../metadata/glossary.md).
- **SEV1 / SEV2 / SEV3** — incident severity levels (1 = highest).
- **Runbook** — a documented procedure for operating a service, especially during incidents.
- **Design Doc** — a pre-implementation document describing a non-trivial change.
- **IaC** — Infrastructure as Code; typically Terraform or Bicep at ACME.
- **FinOps** — cloud financial operations practice; managing cloud spend.

## 9. Hand-off to First 90 Days

When D60-001 through D60-008 are `COMPLETED` (or conditional tasks explicitly not-applicable), the HRBP closes the 60-day file and hands off to [`first-90-days.md`](./first-90-days.md). The hand-off summary includes: 60-day rating, feature-sized change URL/epic link, on-call shadow debrief notes, access review status (no changes expected), and any carry-over items.
