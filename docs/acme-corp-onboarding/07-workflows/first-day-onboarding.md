---
document_id: ACME-WF-002
title: First Day Onboarding Workflow
category: workflow
department: human-resources
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [workflow, onboarding, first-day]
---

# First Day Onboarding Workflow

> Fictional document. All names, emails, systems, and URLs are illustrative only.

## 1. Overview

Day one at ACME Corp is the highest-leverage day in onboarding. The new hire should leave the office (or close the laptop at end of day) having met their manager, their buddy, and at least one teammate; signed onto the corporate network; enrolled in MFA; installed the password manager; and understood the shape of the week ahead. Day one is owned by HR Operations (Priya Nair — `priya.nair@acme.example`) for the morning HR block and by the hiring manager for the afternoon.

This workflow assumes [`preboarding.md`](./preboarding.md) is fully `COMPLETED`. If any preboarding task is `BLOCKED` at 09:00 IST on start date, escalate per the preboarding hand-off rules.

## 2. Scope

- **Starts:** 09:00 IST on start date.
- **Ends:** 17:30 IST on start date.
- **Roles involved:** HR Onboarding Coordinator, IT Onboarding Specialist, Hiring Manager, Buddy, Facilities, New Hire.
- **Time zones:** IST (Hyderabad / Bengaluru), GMT (London), PST (Seattle). For London and Seattle start dates, the morning HR block is shifted to 09:00 local time; the IT and manager blocks follow accordingly.

## 3. Cross-References

- Welcome: [`../00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md)
- Handbook: [`../00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- Employee support: [`../00-company/employee-support-and-escalation.md`](../00-company/employee-support-and-escalation.md)
- HR: [`../01-hr/welcome-letter.md`](../01-hr/welcome-letter.md), [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md)
- IT: [`../02-it/microsoft-365-account-activation.md`](../02-it/microsoft-365-account-activation.md), [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md), [`../02-it/corporate-vpn-configuration.md`](../02-it/corporate-vpn-configuration.md), [`../02-it/device-acceptance-and-responsibility.md`](../02-it/device-acceptance-and-responsibility.md), [`../02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md), [`../02-it/it-support-and-troubleshooting.md`](../02-it/it-support-and-troubleshooting.md)
- Forms: [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md), [`../08-forms/onboarding-feedback.md`](../08-forms/onboarding-feedback.md), [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md)
- Contacts: [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)

## 4. Day 1 Task List

| Task ID | Description | Responsible | Prerequisites | Due | Approval | Completion Criteria | Default Status |
|---|---|---|---|---|---|---|---|
| DAY1-001 | Reception welcome, badge handover, ID photo, Wi-Fi guest credentials | Facilities + HR Onboarding | PRE-009 | Day 1 by 09:30 IST | Facilities Lead | Badge activated in access-control system; guest Wi-Fi connected | NOT_STARTED |
| DAY1-002 | Laptop and peripherals handover (laptop, dock, monitor, headset, cables) | IT Onboarding Specialist (Geetha Iyer) | PRE-005, DAY1-001 | Day 1 by 10:00 IST | IT Onboarding lead | Equipment handover form signed; asset tags scanned into Intune | NOT_STARTED |
| DAY1-003 | Microsoft 365 / Entra ID account activation — sign-in enabled, password set on first login | IT Onboarding Specialist | PRE-006, DAY1-002 | Day 1 by 10:30 IST | IT Manager Hyderabad (Arjun Kapoor) | New hire signs in to `portal.acme.example` with UPN; temporary password consumed | NOT_STARTED |
| DAY1-004 | Microsoft Authenticator + MFA enrollment (passwordless + push) | New Hire (with IT Onboarding) | DAY1-003 | Day 1 by 11:00 IST | IT Onboarding verification | Authenticator app registered; MFA methods verified; recovery codes stored in password manager | NOT_STARTED |
| DAY1-005 | Corporate VPN configuration + corporate Wi-Fi (802.1X) enrollment | New Hire (with IT Onboarding) | DAY1-004 | Day 1 by 11:30 IST | IT Onboarding verification | VPN connects; Wi-Fi certificate installed; DNS resolves `vault.acme.example` | NOT_STARTED |
| DAY1-006 | Password manager installation + first vault entries (corporate, HR Hub, VPN) | New Hire (with IT Onboarding) | DAY1-004 | Day 1 by 12:00 IST | IT Onboarding verification | Password manager desktop + browser extension installed; 3+ entries saved | NOT_STARTED |
| DAY1-007 | HR welcome session — handbook walkthrough, code of conduct, day-1 paperwork, payroll + benefits sign-up kickoff | HR Onboarding Coordinator (Priya Nair) | DAY1-001 | Day 1 by 12:30 IST | HRBP | Welcome session attended; benefits enrollment form initiated | NOT_STARTED |
| DAY1-008 | Manager 1:1 — role, expectations, first 30-day plan, calendar review | Hiring Manager | DAY1-003 | Day 1 by 14:00 IST | Manager | 1:1 held; 30-day plan shared; recurring 1:1 scheduled | NOT_STARTED |
| DAY1-009 | Lunch with onboarding buddy (informal) | Buddy + New Hire | PRE-007 | Day 1 by 13:00 IST | None | Lunch completed; buddy shared "what to expect in week 1" notes | NOT_STARTED |
| DAY1-010 | Security orientation introduction — CISO welcome video, infosec policy summary, MFA recovery procedure, incident reporting basics | Security (GRC Analyst, Karthik Subramanian) | DAY1-004 | Day 1 by 15:30 IST | CISO office (Rajan Mehta) | Video watched live; infosec policy link shared; MFA recovery procedure understood | NOT_STARTED |
| DAY1-011 | Team introduction — manager introduces new hire in team channel + team standup | Hiring Manager + Buddy | DAY1-003 | Day 1 by 16:30 IST | Manager | Introduction message posted in team Teams channel; new hire attended team standup | NOT_STARTED |
| DAY1-012 | End-of-day recap + day-1 feedback form | HR Onboarding Coordinator | DAY1-001 through DAY1-011 | Day 1 by 17:30 IST | HRBP | Recap completed; feedback form submitted in HR Hub | NOT_STARTED |

## 5. Dependencies

- **DAY1-001 blocks DAY1-002** — Equipment is staged at the office reception and cannot be handed over until the badge is activated (so the new hire can physically enter the IT staging area).
- **DAY1-002 blocks DAY1-003** — M365 activation requires a working, Intune-enrolled laptop.
- **DAY1-003 blocks DAY1-004** — MFA enrollment requires the new hire's identity to be activated.
- **DAY1-004 blocks DAY1-005, DAY1-006, DAY1-008, DAY1-010** — VPN enrollment, password manager installation, manager 1:1 (uses Teams), and security orientation (uses secure links) all depend on MFA being active.
- **DAY1-007 → WK1-001** — The HR welcome session is where the benefits enrollment form is initiated; it completes during week 1.
- **DAY1-010 → SEC-001** — The day-1 security orientation introduction precedes the formal security training block in week 1.
- **DAY1-012 → WK1-015** — Day-1 feedback feeds into the week-1 feedback task; if day-1 feedback flags a blocker (e.g., MFA recovery codes lost), week-1 feedback re-surfaces it.

## 6. Status Tracking

All DAY1-* tasks are tracked in HR Hub under **Onboarding → Day 1**. Allowed statuses:

- `NOT_STARTED`
- `IN_PROGRESS`
- `BLOCKED`
- `COMPLETED`

If MFA enrollment (DAY1-004) fails twice, IT Onboarding escalates to `security-oncall@acme.example` to confirm identity verification before issuing a temporary access key. If the laptop (DAY1-002) is not staged, IT issues a loaner machine from the loaner pool and opens a helpdesk ticket to follow up.

## 7. RACI Matrix

| Activity | R | A | C | I |
|---|---|---|---|---|
| Badge handover + Wi-Fi guest | Facilities + HR Onboarding | Facilities Lead | New Hire | IT Onboarding |
| Equipment handover | IT Onboarding Specialist | IT Onboarding lead | New Hire, Facilities | HRBP |
| M365 / Entra ID activation | IT Onboarding Specialist | IT Manager Hyderabad | New Hire | Security |
| MFA enrollment | New Hire (with IT) | IT Onboarding verification | Security | HRBP |
| VPN + Wi-Fi configuration | New Hire (with IT) | IT Onboarding verification | Security | HRBP |
| Password manager install | New Hire (with IT) | IT Onboarding verification | Security | HRBP |
| HR welcome session | HR Onboarding Coordinator | HRBP | New Hire | VP HR |
| Manager 1:1 | Hiring Manager | Hiring Manager | New Hire | HRBP |
| Lunch with buddy | Buddy + New Hire | Buddy | New Hire | Hiring Manager |
| Security orientation intro | Security (GRC Analyst) | CISO office | New Hire | HRBP |
| Team introduction | Hiring Manager + Buddy | Hiring Manager | New Hire | HRBP |
| End-of-day recap + feedback | HR Onboarding Coordinator | HRBP | New Hire, Hiring Manager | VP HR |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 8. Key Terms

- **MFA** — Multi-Factor Authentication; at ACME, Microsoft Authenticator. See [`../metadata/glossary.md`](../metadata/glossary.md).
- **SSO** — Single Sign-On; at ACME, Microsoft Entra ID.
- **Buddy** — a peer assigned to support a new hire's first 90 days.
- **HRBP** — HR Business Partner.
- **EM** — Engineering Manager; owns a team and its repositories.
- **UPN** — User Principal Name; the new hire's corporate sign-in (e.g., `firstname.lastname@acme.example`).

## 9. Hand-off to Week 1

When DAY1-001 through DAY1-012 are `COMPLETED`, the HR Onboarding Coordinator closes the day-1 file and hands off to [`first-week-onboarding.md`](./first-week-onboarding.md). A summary email is sent to the new hire, the manager, the buddy, and the HRBP confirming completion and listing any carry-over items (e.g., benefits enrollment pending final bank verification).
