---
document_id: ACME-WF-008
title: IT Provisioning Workflow
category: workflow
department: information-technology
applicable_roles: [it, hr, managers]
owner: IT Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [workflow, onboarding, it-provisioning]
---

# IT Provisioning Workflow

> Fictional document. All systems (portal.acme.example, hr.acme.example, vault.acme.example, packages.acme.example, git.acme.example) are illustrative.

## 1. Overview

IT provisioning is the end-to-end IT pipeline that takes a new hire from "no account exists" through "fully provisioned on day 5" — covering Entra ID staging, M365 licensing, Intune enrollment, equipment staging, VPN/Wi-Fi configuration, password manager rollout, and engineering-tool entitlements (GitHub Enterprise, package feeds, cloud subscriptions). The pipeline is owned by IT Onboarding Specialist Geetha Iyer (`geetha.iyer@acme.example`) with IT Manager Hyderabad Arjun Kapoor (`arjun.kapoor@acme.example`) as approver and the IT Helpdesk (`helpdesk@acme.example`) for break-fix.

Triggers and SLAs:

- **Trigger:** MGR-001 (manager checklist) submitted → IT-001 starts.
- **Trigger:** PRE-006 (identity staging) `COMPLETED` → IT-004 (day-1 activation) becomes available.
- **Day-1 SLA:** IT-004 through IT-008 must all be `COMPLETED` by 12:00 IST on day 1.
- **Week-1 SLA:** IT-009 through IT-012 must be `COMPLETED` by end of day 5.

## 2. Scope

- **Starts:** MGR-001 submission (5 business days before start date).
- **Ends:** Day 5 (end of week 1).
- **Roles involved:** IT Onboarding, IT Manager Hyderabad, New Hire, Hiring Manager (approver), Security (for elevated access).
- **Office-agnostic;** London and Seattle new hires are provisioned by the same Hyderabad team but follow local time-zone SLAs for day-1 activation.

## 3. Cross-References

- IT: [`../02-it/new-employee-it-request.md`](../02-it/new-employee-it-request.md), [`../02-it/laptop-and-workstation-allocation.md`](../02-it/laptop-and-workstation-allocation.md), [`../02-it/microsoft-365-account-activation.md`](../02-it/microsoft-365-account-activation.md), [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md), [`../02-it/corporate-vpn-configuration.md`](../02-it/corporate-vpn-configuration.md), [`../02-it/microsoft-entra-id-and-sso.md`](../02-it/microsoft-entra-id-and-sso.md), [`../02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md), [`../02-it/microsoft-teams-setup.md`](../02-it/microsoft-teams-setup.md), [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md), [`../02-it/it-support-and-troubleshooting.md`](../02-it/it-support-and-troubleshooting.md), [`../02-it/approved-software-installation.md`](../02-it/approved-software-installation.md)
- Engineering: [`../04-engineering/developer-workstation-setup.md`](../04-engineering/developer-workstation-setup.md), [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md), [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md)
- Forms: [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md), [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md), [`../08-forms/manager-approval.md`](../08-forms/manager-approval.md)
- Contacts: [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)

## 4. IT Task List

| Task ID | Description | Responsible | Prerequisites | Due | Approval | Completion Criteria | Default Status |
|---|---|---|---|---|---|---|---|
| IT-001 | Receive and validate new employee IT request (trigger: MGR-001) — confirm role, team, office, license tier | IT Onboarding (Geetha Iyer) | MGR-001 | 4 business days before start date | IT Manager Hyderabad (Arjun Kapoor) | Request validated; SLA clock started in ITSM tool | NOT_STARTED |
| IT-002 | Stage Entra ID identity (cloud-only, sign-in disabled) — see [`preboarding.md`](./preboarding.md) PRE-006 | IT Onboarding | IT-001, PRE-002 | 3 business days before start date | IT Manager Hyderabad | UPN created in Entra ID; M365 license pre-assigned; sign-in disabled | NOT_STARTED |
| IT-003 | Stage equipment (laptop, dock, monitor, headset, cables) — see [`preboarding.md`](./preboarding.md) PRE-005 and [`equipment-handover.md`](./equipment-handover.md) EQP-001 | IT Onboarding | IT-001, MGR-001 | 3 business days before start date | IT Manager Hyderabad | Laptop configured, Intune-enrolled, asset tagged, stored at office | NOT_STARTED |
| IT-004 | Activate Entra ID identity — enable sign-in, set temporary password, force MFA enrollment at first login | IT Onboarding | IT-002, DAY1-002 (laptop on hand) | Day 1 by 10:30 IST | IT Manager Hyderabad | Identity active; new hire signed in to `portal.acme.example` | NOT_STARTED |
| IT-005 | Enroll Microsoft Authenticator + MFA — see [`first-day-onboarding.md`](./first-day-onboarding.md) DAY1-004 | IT Onboarding + New Hire | IT-004 | Day 1 by 11:00 IST | IT Onboarding verification | Authenticator registered; MFA verified; recovery codes stored | NOT_STARTED |
| IT-006 | Configure corporate VPN + corporate Wi-Fi (802.1X) — see [`first-day-onboarding.md`](./first-day-onboarding.md) DAY1-005 | IT Onboarding + New Hire | IT-005 | Day 1 by 11:30 IST | IT Onboarding verification | VPN connects; Wi-Fi cert installed; DNS resolves internal hosts | NOT_STARTED |
| IT-007 | Install and configure password manager (vault, browser extension) — see [`first-day-onboarding.md`](./first-day-onboarding.md) DAY1-006 | IT Onboarding + New Hire | IT-005 | Day 1 by 12:00 IST | IT Onboarding verification | Password manager installed; first vault entries created | NOT_STARTED |
| IT-008 | Configure Microsoft Teams + Outlook + OneDrive — verify mailflow, calendar, file sync | IT Onboarding + New Hire | IT-004, IT-005 | Day 1 by 12:00 IST | IT Onboarding verification | Teams signed in; test email sent/received; OneDrive sync active | NOT_STARTED |
| IT-009 | Grant engineering entitlements — GitHub Enterprise seat, package feed tokens, cloud sandbox account | IT Onboarding | IT-005, WK1-007 (policy acknowledgements), [`access-approval.md`](./access-approval.md) ACC-002 | End of day 3 | Manager + IT Manager Hyderabad | GitHub Enterprise seat assigned; tokens stored in password manager; sandbox account active | NOT_STARTED |
| IT-010 | Install approved engineering software (IDE, runtime, Docker, language SDKs) — see [`../02-it/approved-software-installation.md`](../02-it/approved-software-installation.md) | IT Onboarding + New Hire | IT-006, IT-007 | End of day 3 | IT Manager Hyderabad | Software installed via Intune or approved installer; versions logged | NOT_STARTED |
| IT-011 | Verify dev environment boots (sample project builds and runs) — see [`first-week-onboarding.md`](./first-week-onboarding.md) WK1-008 | IT Onboarding + Engineering onboarding lead | IT-009, IT-010 | End of day 4 | Engineering onboarding lead | Sample app builds; local tests pass | NOT_STARTED |
| IT-012 | Day-5 IT readiness check — confirm no open helpdesk tickets, no missing entitlements; close IT portion of week-1 file | IT Onboarding | IT-004 through IT-011 | Day 5 by 17:30 IST | IT Manager Hyderabad | Readiness check passed; IT portion of file marked `COMPLETED` | NOT_STARTED |

## 5. Dependencies

- **MGR-001 blocks IT-001** — Manager approval precedes IT provisioning starts (canonical dependency per ACME policy).
- **IT-001 blocks IT-002, IT-003** — Identity and equipment staging both require a validated IT request.
- **IT-002 blocks IT-004** — Day-1 identity activation requires the staged identity.
- **IT-003 → DAY1-002** — Equipment staging feeds the day-1 handover task.
- **IT-004 blocks IT-005, IT-008** — MFA enrollment and Microsoft Teams/Outlook/OneDrive configuration all depend on an active identity.
- **IT-005 blocks IT-006, IT-007, IT-009** — VPN, password manager, and engineering entitlements all require MFA to be active.
- **IT-009 blocks WK1-010** — Cannot make a first commit without a GitHub Enterprise seat (this dependency is enforced on the GitHub Enterprise side via SSO gating).
- **WK1-007 (policy acknowledgements) blocks IT-009** — Engineering entitlements require the security + AI tool policy acknowledgements (see [`access-approval.md`](./access-approval.md) ACC-002 → ACC-003 sequence).
- **IT-009, IT-010 block IT-011** — Dev environment verification requires entitlements + installed software.
- **IT-011 → WK1-010** — The first commit task requires a verified dev environment.

## 6. SLA Tracking & Escalation

All IT-* tasks are tracked in the ITSM tool (`helpdesk.acme.example`) and mirrored to HR Hub under **Onboarding → IT**. Allowed statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

Escalation ladder:

1. **Helpdesk** (Tier 1) — any ticket not resolved within SLA window.
2. **IT Onboarding Specialist** (Geetha Iyer) — pattern issues across multiple new hires.
3. **IT Manager Hyderabad** (Arjun Kapoor) — single high-impact blocker on day 1.
4. **VP IT** (Ramesh Khanna) — policy-level issues or repeated SLA misses.

If MFA enrollment (IT-005) fails twice on day 1, IT escalates to `security-oncall@acme.example` for identity re-verification before issuing a temporary access key. If the laptop (IT-003) cannot be staged in time, IT issues a loaner and opens a follow-up ticket for the standard machine.

## 7. RACI Matrix

| Activity | R | A | C | I |
|---|---|---|---|---|
| Validate new employee IT request | IT Onboarding | IT Manager Hyderabad | HRBP | VP IT |
| Stage Entra ID identity | IT Onboarding | IT Manager Hyderabad | Security (GRC) | HRBP |
| Stage equipment | IT Onboarding | IT Manager Hyderabad | Facilities, Hiring Manager | Security |
| Activate identity on day 1 | IT Onboarding | IT Manager Hyderabad | New Hire | Security |
| Enroll MFA | IT Onboarding + New Hire | IT Onboarding verification | Security | HRBP |
| Configure VPN + Wi-Fi | IT Onboarding + New Hire | IT Onboarding verification | Security | HRBP |
| Install password manager | IT Onboarding + New Hire | IT Onboarding verification | Security | HRBP |
| Configure Teams/Outlook/OneDrive | IT Onboarding + New Hire | IT Onboarding verification | HRBP | New Hire |
| Grant engineering entitlements | IT Onboarding | Manager + IT Manager Hyderabad | Security (GRC) | VP Engineering |
| Install approved engineering software | IT Onboarding + New Hire | IT Manager Hyderabad | Engineering onboarding lead | VP Engineering |
| Verify dev environment | IT Onboarding + Engineering onboarding lead | Engineering onboarding lead | Buddy | VP Engineering |
| Day-5 IT readiness check | IT Onboarding | IT Manager Hyderabad | HRBP | VP IT |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 8. Key Terms

- **MDM** — Mobile Device Management; at ACME, Microsoft Intune. See [`../metadata/glossary.md`](../metadata/glossary.md).
- **EDR** — Endpoint Detection and Response; at ACME, Microsoft Defender for Endpoint.
- **DLP** — Data Loss Prevention; at ACME, Microsoft Purview.
- **SSO** — Single Sign-On; at ACME, Microsoft Entra ID.
- **SLA** — Service-Level Agreement.
- **L1 / L2 / L3** — support tiers (1 = first line, 3 = deepest engineering).

## 9. Hand-off

When IT-001 through IT-012 are `COMPLETED`, IT Onboarding closes the IT portion of the onboarding file and the new hire transitions to standard IT support via [`../02-it/it-support-and-troubleshooting.md`](../02-it/it-support-and-troubleshooting.md) and the helpdesk channel. Future IT-driven changes (software access requests, equipment replacement, access revocation) follow their own standalone workflows, not this provisioning pipeline.
