---
document_id: ACME-OFF-001
title: Employee Departure Checklist
category: offboarding
department: human-resources
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [offboarding, checklist, departure, separation]
---

# Employee Departure Checklist

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. The HRIS endpoints (`hr.acme.example`), ITSM ticketing (`helpdesk.acme.example`), GitHub Enterprise (`git.acme.example`), ACME Vault (`vault.acme.example`), and all employee identifiers below are illustrative. No real personal data is represented.

## 1. Purpose

This checklist is the end-to-end master workflow for offboarding an ACME Corp employee — from receipt of resignation through the last working day (LWD) and post-separation closeout. It is the canonical sequencing reference cited by [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md). Each task has an owner, a due date expressed **relative to the last working day (T-0)**, explicit completion criteria, and one of four statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

The checklist is consistent with the access policies established in [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md), [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md), and [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md). Specifically:

- All corporate identity access (Microsoft Entra ID, GitHub Enterprise, ACME Vault, VPN, SaaS apps) is revoked at **end-of-business on the LWD**.
- Standing production access was never granted during employment (only time-bound PIM), so there is no production access to revoke — see §3.4.
- Equipment return uses [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) **in reverse** (the return section of the same form the employee signed on day 1).
- Knowledge transfer is mandatory and documented before the LWD.
- Final settlement is processed per [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) §Final Settlement and detailed in [`./final-hr-and-payroll-procedures.md`](./final-hr-and-payroll-procedures.md).

## 2. Roles and Contacts

| Role | Name | Email |
|------|------|-------|
| VP HR | Ananya Sharma | ananya.sharma@acme.example |
| HR Onboarding Coordinator | Priya Nair | priya.nair@acme.example |
| HRBP (Cloud/Workspace) | Kavya Krishnan | kavya.krishnan@acme.example |
| HRBP (Intelligence/QE/Support) | Deepika Rao | deepika.rao@acme.example |
| HRBP (Platform/Sales) | Sanjay Patel | sanjay.patel@acme.example |
| VP IT | Ramesh Khanna | ramesh.khanna@acme.example |
| IT Manager Hyderabad | Arjun Kapoor | arjun.kapoor@acme.example |
| IT Onboarding Specialist | Geetha Iyer | geetha.iyer@acme.example |
| IT Helpdesk | — | helpdesk@acme.example |
| CISO | Rajan Mehta | rajan.mehta@acme.example |
| GRC Analyst | Karthik Subramanian | karthik.subramanian@acme.example |
| Payroll Lead | Sanjay Patel | sanjay.patel@acme.example |
| Benefits Specialist | Rohit Sharma | rohit.sharma@acme.example |
| Legal | Hemant Joshi | hemant.joshi@acme.example |

The HRBP assignment is by business unit; see [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for the full directory.

## 3. Pre-Departure Tasks (T-30 to T-6 business days)

These tasks run from the resignation receipt date through the start of the final week. The HRBP is the overall owner of this phase.

| # | Task ID | Description | Owner | Due | Completion Criteria | Default Status |
|---|---------|-------------|-------|-----|--------------------|----------------|
| 1 | DEP-001 | Employee submits written resignation to manager and HRBP | Employee | T-30 (or at resignation) | Resignation letter received in HR Hub; manager copied | NOT_STARTED |
| 2 | DEP-002 | Manager acknowledges resignation within 1 business day and triggers the offboarding workflow | Hiring Manager | T-29 | HRIS state changed to "Pending Separation"; offboarding ticket `OFFBD-YYYY-NNNNNN` created in ITSM | NOT_STARTED |
| 3 | DEP-003 | HRBP issues formal acceptance letter and separation packet to the employee | HRBP | T-25 | Acceptance letter sent; packet includes final-settlement overview, leave encashment, benefits continuation, exit-interview scheduling | NOT_STARTED |
| 4 | DEP-004 | HRBP confirms the LWD in the HRIS and notifies IT, Payroll, Benefits, and Legal | HRBP | T-25 | LWD recorded; notification emails sent to IT Manager, Payroll Lead, Benefits Specialist, Legal | NOT_STARTED |
| 5 | DEP-005 | HRBP confirms notice period per [`../01-hr/sample-employment-agreement.md`](../01-hr/sample-employment-agreement.md) and applicable jurisdiction (India 60d / UK 4wk / US 2wk) | HRBP | T-24 | Notice period verified; any mutual shortening recorded in writing | NOT_STARTED |
| 6 | DEP-006 | Hiring Manager drafts Knowledge Transfer (KT) plan and assigns a successor or coverage owner | Hiring Manager | T-15 | KT plan delivered to hiring EM — see [`./knowledge-transfer.md`](./knowledge-transfer.md) §KT plan template | NOT_STARTED |
| 7 | DEP-007 | Employee transfers ownership of SharePoint sites, Jira/Confluence spaces, dashboards, and 1Password shared vaults to the successor | Employee + Hiring Manager | T-10 | Ownership transfers logged in HR Hub; successor confirmed as new owner in each system | NOT_STARTED |
| 8 | DEP-008 | Employee reviews and finalizes outstanding design docs, runbooks, and on-call playbooks | Employee | T-7 | All owned runbooks updated and merged; design docs marked final | NOT_STARTED |
| 9 | DEP-009 | Employee introduces successor to key customers, stakeholders, and cross-team partners | Employee | T-7 | Introduction emails sent; calendar holds set for transition meetings | NOT_STARTED |
| 10 | DEP-010 | HRBP schedules the exit interview with the employee (HRBP or HR Director conducts — never the direct manager) | HRBP | T-7 | Exit interview scheduled for LWD or T-1; calendar invite sent | NOT_STARTED |

## 4. Final-Week Tasks (T-5 to T-1 business days)

The final week is where KT execution, data handover, and pre-positioning of revocation happen. This phase is owned jointly by the Hiring Manager and IT Onboarding Specialist.

| # | Task ID | Description | Owner | Due | Completion Criteria | Default Status |
|---|---------|-------------|-------|-----|--------------------|----------------|
| 11 | DEP-011 | IT Onboarding Specialist reviews the departing employee's role bundle, Entra ID group memberships, and SaaS app entitlements; prepares the revocation checklist | IT Onboarding (Geetha Iyer) | T-5 | Revocation checklist filed in the offboarding ticket; reviewed by IT Manager Hyderabad | NOT_STARTED |
| 12 | DEP-012 | Hiring Manager sign-off on the offboarding plan — specifically: which data to hand off, which repos to archive, which dashboards to transfer | Hiring Manager | T-5 | Manager sign-off recorded in ITSM ticket; offboarding plan locked | NOT_STARTED |
| 13 | DEP-013 | Employee executes the KT plan — code handover, runbook walkthroughs, customer/stakeholder meetings | Employee + Hiring Manager | T-1 | KT checklist 100% complete; successor signs off in HR Hub — see [`./knowledge-transfer.md`](./knowledge-transfer.md) | NOT_STARTED |
| 14 | DEP-014 | Hiring Manager removes the departing employee from on-call rotation(s) and confirms backup coverage plan | Hiring Manager | T-2 | PagerDuty / Opsgenie rotation updated; backup coverage documented — see [`./knowledge-transfer.md`](./knowledge-transfer.md) §6 | NOT_STARTED |
| 15 | DEP-015 | IT Onboarding sets up Out-of-Office message and email forwarding (manager chooses: forward to a colleague, auto-reply-only, or both) | IT Onboarding (Geetha Iyer) | T-1 | OOO message active; mailbox not deleted — retained 90 days per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §3.1 | NOT_STARTED |
| 16 | DEP-016 | Employee returns any loaner equipment, Yubikeys, hardware security keys, and office keys to IT depot | Employee + IT Onboarding | T-1 | Loaners and keys logged in IT asset register; serial numbers recorded | NOT_STARTED |
| 17 | DEP-017 | Hiring Manager confirms KT plan complete and signs the KT sign-off in HR Hub | Hiring Manager | T-1 | KT sign-off form submitted; status `COMPLETED` | NOT_STARTED |
| 18 | DEP-018 | Payroll Lead reviews pending reimbursements, bonus pro-rata, and PTO balance for the final settlement | Payroll Lead (Sanjay Patel) | T-1 | Settlement worksheet prepared; reviewed by Benefits Specialist — see [`./final-hr-and-payroll-procedures.md`](./final-hr-and-payroll-procedures.md) | NOT_STARTED |
| 19 | DEP-019 | Benefits Specialist prepares benefits continuation packets (COBRA for US, statutory continuation for India, pension continuation for UK) | Benefits Specialist (Rohit Sharma) | T-1 | Continuation packets queued for dispatch on LWD — see [`./final-hr-and-payroll-procedures.md`](./final-hr-and-payroll-procedures.md) §5 | NOT_STARTED |

## 5. Last Working Day Tasks (T-0)

These tasks all execute on the LWD itself. Access is revoked at end-of-business (18:00 local time) per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §3.2.

| # | Task ID | Description | Owner | Due | Completion Criteria | Default Status |
|---|---------|-------------|-------|-----|--------------------|----------------|
| 20 | DEP-020 | Employee returns laptop, monitor, peripherals, and badge to IT depot — uses [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) **in reverse** | Employee + IT Onboarding | T-0 by 16:00 local | Return section of equipment-handover form signed by both parties; asset tags reconciled — see [`./equipment-return.md`](./equipment-return.md) | NOT_STARTED |
| 21 | DEP-021 | IT depot verifies asset tags, performs condition check, and issues Intune **Wipe** command | IT Onboarding (Geetha Iyer) | T-0 by 17:00 local | Wipe initiated; BitLocker/FileVault recovery key rotated — see [`./equipment-return.md`](./equipment-return.md) §condition check | NOT_STARTED |
| 22 | DEP-022 | Identity Engineering disables the Entra ID account (`AccountEnabled=false`), revokes all refresh tokens (`RevokeSignInSessions`), preserves group memberships for audit | Identity Engineering | T-0 EOB (18:00 local) | Account disabled; refresh tokens revoked; sign-in logs captured — see [`./repository-and-system-access-revocation.md`](./repository-and-system-access-revocation.md) §3 | NOT_STARTED |
| 23 | DEP-023 | SCIM de-provisions SaaS apps (Jira, Confluence, GitHub Enterprise, Datadog, Figma, Notion, 1Password, Salesforce) within 60 minutes | IT Onboarding + Identity Engineering | T-0 EOB + 60 min | SCIM cycle complete; each app shows deactivated user — see [`./repository-and-system-access-revocation.md`](./repository-and-system-access-revocation.md) §4 | NOT_STARTED |
| 24 | DEP-024 | ACME Vault tokens revoked; VPN client certificate revoked; Wi-Fi RADIUS auth revoked | IT Onboarding + GRC Analyst (Karthik Subramanian) | T-0 EOB | Vault tokens revoked; VPN cert revoked; Wi-Fi profile removed — see [`./repository-and-system-access-revocation.md`](./repository-and-system-access-revocation.md) §5 and §6 | NOT_STARTED |
| 25 | DEP-025 | GitHub Enterprise seat removed via SCIM (de-provisions org membership and SSO mapping); repo ownership already transferred in DEP-007 | Engineering IT | T-0 EOB + 60 min | GitHub Enterprise seat removed; org membership shows no active user — see [`./repository-and-system-access-revocation.md`](./repository-and-system-access-revocation.md) §4 | NOT_STARTED |
| 26 | DEP-026 | IT certifies that no corporate device or access remains outstanding (closes the IT portion of the offboarding ticket) | IT Onboarding (Geetha Iyer) | T-0 EOB | IT portion of offboarding ticket marked `COMPLETED` | NOT_STARTED |
| 27 | DEP-027 | HRBP conducts the exit interview (or schedules it for T+1 if not done on LWD) | HRBP | T-0 or T+1 | Exit-interview form submitted in HR Hub; anonymized for quarterly aggregation | NOT_STARTED |
| 28 | DEP-028 | Communications removes the departing employee from mailing lists, distribution groups, Teams chats, and DLs | IT Helpdesk | T-0 EOB + 1 business day | All mailing lists and DLs updated; no residual membership — see [`./repository-and-system-access-revocation.md`](./repository-and-system-access-revocation.md) §7 | NOT_STARTED |
| 29 | DEP-029 | Badging / physical access: building badge de-activated at EOB | Facilities + IT Helpdesk | T-0 EOB | Badge deactivated in physical access control system | NOT_STARTED |

## 6. Post-Separation Tasks (T+1 to T+90 days)

These tasks complete the lifecycle after the LWD. They are owned by HR Operations and IT.

| # | Task ID | Description | Owner | Due | Completion Criteria | Default Status |
|---|---------|-------------|-------|-----|--------------------|----------------|
| 30 | DEP-030 | Payroll Lead processes the final settlement (salary through LWD, PTO encashment, reimbursements, bonus pro-rata, statutory gratuity for India, severance per individual agreement) | Payroll Lead (Sanjay Patel) | T+30 to T+45 (jurisdiction dependent) | Final settlement disbursed; payslip delivered — see [`./final-hr-and-payroll-procedures.md`](./final-hr-and-payroll-procedures.md) | NOT_STARTED |
| 31 | DEP-031 | Benefits Specialist dispatches benefits continuation packets and confirms enrolment in COBRA / statutory continuation / pension continuation | Benefits Specialist (Rohit Sharma) | T+5 | Packets delivered; enrolment confirmations filed — see [`./final-hr-and-payroll-procedures.md`](./final-hr-and-payroll-procedures.md) §5 | NOT_STARTED |
| 32 | DEP-032 | OneDrive / SharePoint personal-site content transferred to the manager (manager becomes site collection administrator) | IT Onboarding | T+30 | Personal-site ownership transferred to manager; content preserved 7 years | NOT_STARTED |
| 33 | DEP-033 | Mailbox archived to Exchange Online inactive mailbox (retained 7 years for compliance) | Identity Engineering | T+90 | Mailbox archived; inactive-mailbox record created — see [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §3.3 | NOT_STARTED |
| 34 | DEP-034 | Audit logs retained per schedule (Entra ID 7y, Intune 7y, GitHub Enterprise 7y, VPN 7y, Wi-Fi RADIUS 1y, PIM activations 2y, group membership changes 1y) | Compliance + GRC Analyst | Continuous | Logs preserved immutably in Microsoft Purview audit pipeline — see [`./repository-and-system-access-revocation.md`](./repository-and-system-access-revocation.md) §8 | NOT_STARTED |
| 35 | DEP-035 | HRBP closes the offboarding ticket once IT, Payroll, Benefits, and Legal all sign off | HRBP | T+45 | Offboarding ticket `OFFBD-YYYY-NNNNNN` closed; employee record set to "Separated" in HRIS | NOT_STARTED |

## 7. Production Access Note (No Revocation Required)

Per [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) §6, ACME engineers never received standing production access during employment. All elevated production access was time-bound via Privileged Identity Management (PIM), with a default 4-hour maximum and an approver in the loop. Therefore, at offboarding:

- There is **no standing production RBAC assignment** to revoke.
- The employee's **PIM eligibility** (if any) for privileged roles is removed as part of DEP-022/DEP-023 (disabling the Entra ID account renders PIM eligibility moot; the eligibility records are preserved in audit logs for 2 years per [`./repository-and-system-access-revocation.md`](./repository-and-system-access-revocation.md) §8).
- The employee's **per-secret Vault requests** are revoked in DEP-024.
- The employee's **break-glass access** (if ever granted — extremely rare) is reviewed by the CISO and rotated.

This is the inverse of the onboarding principle: "no access" is the correct starting state, and "no standing access to revoke" is the correct ending state.

## 8. Emergency / For-Cause Termination

For terminations with immediate effect or suspected insider threat, follow the emergency revocation path in [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §5. In that path, the standard T-5/T-1 pre-positioning steps are skipped — Identity Engineering performs all of DEP-022 through DEP-025 **simultaneously within 15 minutes** at the CISO's direction, and Physical Security may be asked to escort the employee off-site per [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md). The post-incident review is scheduled within 5 business days.

## 9. Status Tracking and Escalation

All DEP-* tasks are tracked in the ITSM offboarding ticket (`OFFBD-YYYY-NNNNNN`) and mirrored to the HR Hub offboarding record. Allowed statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

If any task is `BLOCKED` for more than 2 business days, escalate as follows:

| Blocker | Escalate to |
|---------|-------------|
| IT-side delay (provisioning, SCIM, wipe) | IT Manager Hyderabad — Arjun Kapoor (`arjun.kapoor@acme.example`) |
| Payroll / settlement delay | Payroll Lead — Sanjay Patel (`sanjay.patel@acme.example`) |
| Benefits delay | Benefits Specialist — Rohit Sharma (`rohit.sharma@acme.example`) |
| KT plan incomplete | Hiring EM (engineering manager per team — see [`../00-company/organizational-structure.md`](../00-company/organizational-structure.md)) |
| Access-revocation non-compliance | GRC Analyst — Karthik Subramanian (`karthik.subramanian@acme.example`); for systemic issues, CISO — Rajan Mehta (`rajan.mehta@acme.example`) |
| Cross-functional or unclear owner | HRBP, then VP HR — Ananya Sharma (`ananya.sharma@acme.example`) |

For broader support and escalation paths, see [`../00-company/employee-support-and-escalation.md`](../00-company/employee-support-and-escalation.md).

## 10. Related Documents

- HR: [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md), [`../01-hr/payroll-and-bank-information-form.md`](../01-hr/payroll-and-bank-information-form.md), [`../01-hr/probation-and-confirmation-process.md`](../01-hr/probation-and-confirmation-process.md), [`../01-hr/leave-and-attendance-policy.md`](../01-hr/leave-and-attendance-policy.md)
- IT: [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md), [`../02-it/device-acceptance-and-responsibility.md`](../02-it/device-acceptance-and-responsibility.md), [`../02-it/equipment-replacement.md`](../02-it/equipment-replacement.md), [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md)
- Security: [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md), [`../03-security/identity-and-access-management.md`](../03-security/identity-and-access-management.md), [`../03-security/confidentiality-agreement.md`](../03-security/confidentiality-agreement.md), [`../03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md)
- Engineering: [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md), [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md)
- Workflows: [`../07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md), [`../07-workflows/equipment-handover.md`](../07-workflows/equipment-handover.md), [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md)
- Forms: [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md), [`../08-forms/access-review.md`](../08-forms/access-review.md), [`../08-forms/manager-approval.md`](../08-forms/manager-approval.md)
- Contacts: [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)
