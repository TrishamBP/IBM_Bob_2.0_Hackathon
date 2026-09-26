---
document_id: ACME-WF-001
title: Preboarding Workflow
category: workflow
department: human-resources
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [workflow, onboarding, preboarding]
---

# Preboarding Workflow

> Fictional document. All names, emails, systems, and URLs are illustrative only.

## 1. Overview

Preboarding is the window between **offer acceptance** and **day-one start date** at ACME Corp. The objective is to ensure that by the time the new hire walks through the door (or logs in remotely), their identity, equipment, calendar, buddy, and key documents are already staged. A well-run preboarding phase prevents day-one friction and lets the new hire focus on people, policy, and product — not paperwork.

This workflow is jointly owned by HR Operations (Priya Nair — `priya.nair@acme.example`) and IT Onboarding (Geetha Iyer — `geetha.iyer@acme.example`). The hiring manager is responsible for triggering it via the manager checklist (PRE-010) and for assigning a buddy (PRE-007).

## 2. Scope

- **Starts:** Offer acceptance is recorded in HR Hub (`hr.acme.example`).
- **Ends:** 17:00 IST on the business day before the start date.
- **Roles involved:** HRBP, IT Onboarding, Hiring Manager, Security (GRC), Facilities, New Hire.
- **Phases:** Information capture, document signing, equipment staging, identity staging, buddy & calendar setup, badge request, manager checklist.

## 3. Cross-References

- Welcome: [`../00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md)
- Handbook: [`../00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- Org structure: [`../00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- HR docs: [`../01-hr/welcome-letter.md`](../01-hr/welcome-letter.md), [`../01-hr/sample-employment-agreement.md`](../01-hr/sample-employment-agreement.md), [`../01-hr/employee-information-form.md`](../01-hr/employee-information-form.md), [`../01-hr/emergency-contact-form.md`](../01-hr/emergency-contact-form.md), [`../01-hr/payroll-and-bank-information-form.md`](../01-hr/payroll-and-bank-information-form.md), [`../01-hr/tax-declaration-form.md`](../01-hr/tax-declaration-form.md), [`../01-hr/benefits-enrollment-form.md`](../01-hr/benefits-enrollment-form.md)
- IT docs: [`../02-it/new-employee-it-request.md`](../02-it/new-employee-it-request.md), [`../02-it/laptop-and-workstation-allocation.md`](../02-it/laptop-and-workstation-allocation.md), [`../02-it/microsoft-365-account-activation.md`](../02-it/microsoft-365-account-activation.md), [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md)
- Forms: [`../08-forms/new-employee-information.md`](../08-forms/new-employee-information.md), [`../08-forms/emergency-contact.md`](../08-forms/emergency-contact.md), [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md), [`../08-forms/manager-approval.md`](../08-forms/manager-approval.md)
- Contacts: [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)

## 4. Preboarding Task List

| Task ID | Description | Responsible | Prerequisites | Due | Approval | Completion Criteria | Default Status |
|---|---|---|---|---|---|---|---|
| PRE-001 | Send welcome letter and preboarding pack to new hire | HR Onboarding Coordinator (Priya Nair) | Offer acceptance recorded in HR Hub | 5 business days before start date | HRBP approval | Welcome email sent and tracked in HR Hub | NOT_STARTED |
| PRE-002 | Collect Employee Information Form (legal name, address, IDs, dependents) | New Hire | PRE-001 | 4 business days before start date | HRBP review | Form submitted in HR Hub and acknowledged | NOT_STARTED |
| PRE-003 | Collect payroll & bank account information | New Hire | PRE-002 | 4 business days before start date | HRBP + Finance review | Form submitted; bank account verified by Finance | NOT_STARTED |
| PRE-004 | Collect emergency contact form (minimum 2 contacts) | New Hire | PRE-002 | 4 business days before start date | HRBP review | Form submitted and stored against employee record | NOT_STARTED |
| PRE-005 | Stage equipment (laptop, dock, monitor, peripherals) | IT Onboarding (Geetha Iyer) | PRE-010 (manager checklist) | 3 business days before start date | IT Manager Hyderabad (Arjun Kapoor) | Laptop configured, asset tagged, enrolled in Intune; stored at the assigned office | NOT_STARTED |
| PRE-006 | Stage Microsoft 365 / Entra ID identity (cloud-only, disabled sign-in) | IT Onboarding | PRE-002, PRE-010 | 3 business days before start date | IT Manager Hyderabad | Account created in Entra ID; license pre-assigned; sign-in disabled until day 1 | NOT_STARTED |
| PRE-007 | Assign onboarding buddy from same team | Hiring Manager | PRE-010 | 5 business days before start date | Manager | Buddy named in HR Hub; buddy has buddy-guide sent to them | NOT_STARTED |
| PRE-008 | Send day-1 calendar invite with agenda, location/MS Teams link, dress code, parking info | HR Onboarding Coordinator | PRE-006, PRE-007 | 2 business days before start date | Manager + HRBP | Calendar invite accepted by new hire; included in HR Hub | NOT_STARTED |
| PRE-009 | Raise physical access / badge request with Facilities | HR Onboarding Coordinator | PRE-002 | 3 business days before start date | Facilities Lead (Hyder Ali / Lakshmi Venkat / Olivia Carter / Marcus Chen) | Badge staged at the office reception; office access list updated | NOT_STARTED |
| PRE-010 | Hiring Manager preboarding checklist (role confirmed, buddy named, equipment spec approved, repo list prepared, first-week shadow plan) | Hiring Manager | Offer acceptance recorded | 5 business days before start date | Director-level skip approval | Checklist submitted in HR Hub; buddy + equipment + repo lists attached | NOT_STARTED |

## 5. Dependencies

- **PRE-010 blocks PRE-005** — IT cannot stage equipment without the manager's approved spec (machine model, role-specific software, monitor count).
- **PRE-010 blocks PRE-006** — IT cannot stage the M365 identity until the manager checklist confirms role, department, and license tier.
- **PRE-002 blocks PRE-003, PRE-004** — Payroll and emergency contact forms depend on the legal identity captured in the information form.
- **PRE-002 blocks PRE-009** — Facilities will not stage a badge without a verified employee name.
- **PRE-006 blocks PRE-008** — The day-1 calendar invite references the new hire's M365 identity; it cannot be sent until the identity exists.
- **PRE-007 blocks PRE-008** — The calendar invite names the buddy, so buddy assignment must happen first.
- **PRE-005 → DAY1-002** — Equipment staging feeds the day-1 handover task.
- **PRE-006 → DAY1-003** — Identity staging feeds the day-1 M365 activation task.
- **PRE-009 → DAY1-001** — Badge staging feeds the day-1 reception / badge handover.

## 6. Status Tracking

Status is tracked per-task in HR Hub (`hr.acme.example`) under **Onboarding → Preboarding**. The four allowed statuses are:

- `NOT_STARTED` — task has not been picked up.
- `IN_PROGRESS` — owner is actively working it.
- `BLOCKED` — owner is waiting on a prerequisite or external dependency; a comment explaining the blocker is required.
- `COMPLETED` — completion criteria met and approved.

If any task is still `NOT_STARTED` or `IN_PROGRESS` at 17:00 IST on the business day before start date, the HR Onboarding Coordinator escalates to the HRBP. Items still `BLOCKED` at 09:00 IST on start date automatically generate a helpdesk ticket (`helpdesk@acme.example`).

## 7. RACI Matrix

| Activity | R | A | C | I |
|---|---|---|---|---|
| Welcome letter + preboarding pack | HR Onboarding Coordinator | HRBP | New Hire, Hiring Manager | VP HR |
| Employee information form | New Hire | HRBP | HR Onboarding Coordinator | IT Onboarding |
| Payroll & bank form | New Hire | HRBP + Finance | HR Onboarding Coordinator | IT Onboarding |
| Emergency contact form | New Hire | HRBP | HR Onboarding Coordinator | Hiring Manager |
| Equipment staging | IT Onboarding Specialist | IT Manager Hyderabad | Facilities, Hiring Manager | Security |
| M365 / Entra ID staging | IT Onboarding Specialist | IT Manager Hyderabad | Security (GRC) | HRBP |
| Buddy assignment | Hiring Manager | Hiring Manager | Buddy, HRBP | New Hire |
| Day-1 calendar invite | HR Onboarding Coordinator | HRBP | Hiring Manager, Buddy | New Hire |
| Badge request | HR Onboarding Coordinator | Facilities Lead | IT Onboarding | Security |
| Manager checklist | Hiring Manager | Skip-level director | HRBP, IT Onboarding | VP HR |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 8. Key Terms

- **Preboarding** — activities that happen between offer acceptance and start date. See [`../metadata/glossary.md`](../metadata/glossary.md).
- **HRBP** — HR Business Partner; an HR specialist paired with each team. At ACME: Kavya Krishnan (Cloud/Workspace), Deepika Rao (Intelligence/QE/Support), Sanjay Patel (Platform/Sales).
- **Buddy** — a peer (not the manager) assigned to support a new hire's first 90 days.
- **Onboarding plan** — the 30/60/90-day plan a manager creates for a new hire.
- **SSO** — Single Sign-On; at ACME, Microsoft Entra ID.
- **MDM** — Mobile Device Management; at ACME, Microsoft Intune.

## 9. Hand-off to Day 1

When all PRE-001 through PRE-010 tasks are `COMPLETED`, the HR Onboarding Coordinator marks the preboarding phase closed and the file transitions to [`first-day-onboarding.md`](./first-day-onboarding.md). The HRBP receives a final readiness summary listing: badge number, asset tag, M365 UPN, buddy name, calendar acceptance, and signed forms on file.
