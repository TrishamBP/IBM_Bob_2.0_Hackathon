---
document_id: ACME-WF-013
title: Onboarding Completion Workflow
category: workflow
department: human-resources
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [workflow, onboarding, completion]
---

# Onboarding Completion Workflow

> Fictional document. All systems (hr.acme.example, portal.acme.example, vault.acme.example) are illustrative.

## 1. Overview

Onboarding completion is the final gate that converts a probationary new hire's onboarding file into a permanent employee record. It compiles the 30/60/90-day reviews, the confirmation letter, the security training sign-off, the access review, the equipment assignment, the policy acknowledgements, and the manager + new hire feedback into a single archival record. The HRBP owns the close; Ananya Sharma (VP HR — `ananya.sharma@acme.example`) is the final approver for the file's archival.

This workflow assumes [`first-90-days.md`](./first-90-days.md) is fully `COMPLETED` (D90-008 HRBP sign-off recorded). Completion cannot begin while any of D30-010, D60-008, or D90-008 is `IN_PROGRESS` or `BLOCKED`.

## 2. Scope

- **Starts:** Day 90 (after D90-008 HRBP sign-off).
- **Ends:** Within 10 business days of day 90 (archival).
- **Roles involved:** HRBP, VP HR (Ananya Sharma), Hiring Manager, Security (GRC), IT Onboarding, New Hire.
- **Office-agnostic.**

## 3. Cross-References

- Handbook: [`../00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- Org structure: [`../00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- HR: [`../01-hr/probation-and-confirmation-process.md`](../01-hr/probation-and-confirmation-process.md), [`../01-hr/performance-review-policy.md`](../01-hr/performance-review-policy.md), [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md)
- IT: [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md), [`../02-it/device-acceptance-and-responsibility.md`](../02-it/device-acceptance-and-responsibility.md)
- Security: [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md)
- Forms: [`../08-forms/onboarding-feedback.md`](../08-forms/onboarding-feedback.md), [`../08-forms/access-review.md`](../08-forms/access-review.md), [`../08-forms/training-completion.md`](../08-forms/training-completion.md), [`../08-forms/manager-approval.md`](../08-forms/manager-approval.md)
- Contacts: [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)

## 4. Completion Task List

| Task ID | Description | Responsible | Prerequisites | Due | Approval | Completion Criteria | Default Status |
|---|---|---|---|---|---|---|---|
| CMP-001 | Final onboarding file review — compile all phase files (preboarding, day 1, week 1, 30/60/90 days) and verify every task is `COMPLETED` (or marked not-applicable with reason) | HRBP | D90-008 | Day 91 | HRBP | All phase files reviewed; any carry-over items listed | NOT_STARTED |
| CMP-002 | 90-day survey — new hire + manager comprehensive onboarding experience survey (different from D90-004 feedback; this one is the broader program survey) | New Hire + Hiring Manager | D90-008 | Day 95 | HR Operations (Priya Nair) | Both surveys submitted in HR Hub | NOT_STARTED |
| CMP-003 | HRBP sign-off on onboarding file — confirm probation outcome, confirmation letter, all training, all policy acknowledgements, all access grants, all equipment | HRBP | CMP-001, CMP-002, D90-007 | Day 95 | VP HR (Ananya Sharma) | Sign-off recorded; file ready for manager sign-off | NOT_STARTED |
| CMP-004 | Manager sign-off on onboarding file — manager attests that the new hire is meeting role expectations and the onboarding experience was satisfactory | Hiring Manager | CMP-003 | Day 95 | Skip-level director | Manager attestation recorded in HR Hub | NOT_STARTED |
| CMP-005 | Security sign-off — confirm all SEC-* training is `COMPLETED`, all POL-* acknowledgements on file, all ACC-* grants least-privilege and reviewed | Security (GRC) | CMP-001, [`security-training.md`](./security-training.md) SEC-010, [`policy-acknowledgement.md`](./policy-acknowledgement.md) POL-007, [`access-approval.md`](./access-approval.md) ACC-008 | Day 95 | CISO office (Rajan Mehta) | Security attestation recorded; no open security debt | NOT_STARTED |
| CMP-006 | IT sign-off — confirm equipment inventory is accurate, no open helpdesk tickets tied to onboarding, dev environment verified | IT Onboarding (Geetha Iyer) | CMP-001, [`it-provisioning.md`](./it-provisioning.md) IT-012, [`equipment-handover.md`](./equipment-handover.md) EQP-004 | Day 95 | IT Manager Hyderabad (Arjun Kapoor) | IT attestation recorded; no open IT debt | NOT_STARTED |
| CMP-007 | Archival — move onboarding file to permanent employee record; lock phase files; schedule first annual performance review | HR Operations (Priya Nair) | CMP-003, CMP-004, CMP-005, CMP-006 | Day 100 (within 10 business days of day 90) | VP HR (Ananya Sharma) | File archived in HR Hub; phase files locked; first annual review scheduled | NOT_STARTED |
| CMP-008 | Continuous improvement — feed onboarding survey results (CMP-002) into the quarterly onboarding program review chaired by the VP HR | HR Operations (Priya Nair) | CMP-002 | Quarterly | VP HR | Survey results aggregated; improvement actions tracked in HR Hub | NOT_STARTED |

## 5. Dependencies

- **D90-008 blocks CMP-001** — HRBP 90-day sign-off is the precondition for onboarding completion (canonical).
- **D90-007 (confirmation letter) blocks CMP-003** — The HRBP cannot sign off the file without the issued confirmation letter.
- **SEC-010 blocks CMP-005** — Security sign-off requires the security training completion sign-off.
- **POL-007 blocks CMP-005** — Security sign-off requires the manager attestation that all POL-* are `COMPLETED`.
- **ACC-008 blocks CMP-005** — Security sign-off requires the quarterly access review to be in good standing.
- **IT-012 blocks CMP-006** — IT sign-off requires the day-5 IT readiness check to be closed.
- **EQP-004 blocks CMP-006** — IT sign-off requires the equipment inventory to be assigned and accurate.
- **CMP-001 blocks CMP-003** — HRBP sign-off requires the file review.
- **CMP-002 blocks CMP-003** — HRBP sign-off requires the 90-day survey results.
- **CMP-003 blocks CMP-007** — Archival requires HRBP sign-off.
- **CMP-004 blocks CMP-007** — Archival requires manager sign-off.
- **CMP-005 blocks CMP-007** — Archival requires security sign-off.
- **CMP-006 blocks CMP-007** — Archival requires IT sign-off.
- **CMP-002 blocks CMP-008** — Continuous improvement feeds off the survey results.

## 6. Status Tracking

All CMP-* tasks are tracked in HR Hub under **Onboarding → Completion**. Allowed statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

If CMP-003 cannot close because of a carry-over from an earlier phase (e.g., extended probation, outstanding training debt), the HRBP documents the carry-over and re-opens the relevant earlier file (e.g., [`first-90-days.md`](./first-90-days.md)). The completion file stays `IN_PROGRESS` until the carry-over is resolved; if unresolved within 30 days of day 90, the HRBP escalates to the VP HR.

If CMP-005 (security sign-off) finds a real outstanding security debt (e.g., POL-004 not acknowledged), the GRC Analyst routes the new hire back through [`policy-acknowledgement.md`](./policy-acknowledgement.md) and the relevant access (ACC-004) is suspended until the debt is cleared.

## 7. RACI Matrix

| Activity | R | A | C | I |
|---|---|---|---|---|
| Final onboarding file review | HRBP | HRBP | Manager, IT, Security | VP HR |
| 90-day onboarding survey | New Hire + Hiring Manager | HR Operations | HRBP | VP HR |
| HRBP sign-off on onboarding file | HRBP | VP HR | Manager | VP HR |
| Manager sign-off | Hiring Manager | Skip-level director | HRBP | VP HR |
| Security sign-off | Security (GRC) | CISO office | HRBP | VP HR |
| IT sign-off | IT Onboarding | IT Manager Hyderabad | HRBP | VP IT |
| Archival | HR Operations | VP HR | Manager, IT, Security | VP HR |
| Continuous improvement (quarterly) | HR Operations | VP HR | HRBP | VP HR |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 8. Key Terms

- **Probation** — initial employment period (typically 90 days) before confirmation as a permanent employee. See [`../01-hr/probation-and-confirmation-process.md`](../01-hr/probation-and-confirmation-process.md).
- **Confirmation letter** — formal letter issued by VP HR converting the new hire from probationary to confirmed status.
- **HRBP** — HR Business Partner. See [`../metadata/glossary.md`](../metadata/glossary.md).
- **Archival** — moving an active onboarding file to a permanent employee record; phase files are locked against further edits.
- **Carry-over** — an item from an earlier phase still `IN_PROGRESS` or `BLOCKED` at completion; documented and tracked to resolution.
- **Attestation** — a formal assertion by a responsible party that a state of affairs is true.

## 9. Archival & Hand-off

When CMP-001 through CMP-008 are `COMPLETED`, the HR Operations team archives the onboarding file to the permanent employee record in HR Hub. Phase files (preboarding, day 1, week 1, 30/60/90 days, manager responsibilities, IT provisioning, security training, access approval, equipment handover, policy acknowledgement, completion) are locked against further edits. The new hire's first annual performance review is scheduled per [`../01-hr/performance-review-policy.md`](../01-hr/performance-review-policy.md). Quarterly continuous-improvement reviews (CMP-008) feed program-level changes back into this workflow library, versioned and owned by HR Operations.
