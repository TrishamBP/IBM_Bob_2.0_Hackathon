---
document_id: ACME-IT-001
title: New Employee IT Request
category: it
department: it-operations
applicable_roles: [all]
owner: Geetha Iyer, IT Onboarding Specialist
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, onboarding, provisioning, request, sla, fictional]
---

# New Employee IT Request

> ACME Corp fictional onboarding library. All hostnames, emails, and identifiers below are simulated and use the reserved `acme.example` / `acme.onmicrosoft.com` domains. Do not treat them as live infrastructure.

## 1. Purpose

This document explains how a new hire's IT request is **triggered**, **what is provisioned** (laptop, Microsoft 365, Intune, network), the **service-level agreements (SLAs)** that apply, and the **approval workflow** between HR, the hiring manager, and IT Operations.

It is the canonical entry point referenced by the HR onboarding workflow ([`../07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md)) and the IT access form ([`../08-forms/it-access-request.md`](../08-forms/it-access-request.md)).

## 2. Who Triggers the IT Request

The IT request is triggered automatically once the HR system transitions a candidate to the **"Hired — Pending Onboarding"** state. The following parties are involved:

| Party | Responsibility |
|-------|----------------|
| **HRBP / HR Onboarding Coordinator** | Confirms offer acceptance, start date, and submits the HRIS record that auto-creates the IT request ticket. |
| **Hiring Manager** | Approves the requested role bundle, hardware tier, and software stack. Adds any role-specific access (e.g., GitHub Enterprise team, Datadog roles). |
| **IT Onboarding Specialist** (Geetha Iyer — `geetha.iyer@acme.example`) | Triage and orchestrate laptop imaging, M365 mailbox creation, Intune enrollment, and software entitlement. |
| **Identity Engineer** (Faisal Ahmed — `faisal.ahmed@acme.example`) | Creates and licenses the Entra ID account (`<firstname>.<lastname>@acme.example`) and assigns group memberships. |
| **Endpoint Engineer** (Suresh Babu — `suresh.babu@acme.example`) | Images, encrypts, and ships the laptop. |

## 3. What's Included in the Standard IT Request

The default IT request for any new knowledge worker includes the following bundles:

1. **Corporate identity** — a Microsoft Entra ID user object in the `acme.onmicrosoft.com` tenant with primary user principal name `<firstname>.<lastname>@acme.example`.
2. **Microsoft 365 license** — `M365 E5` (includes Exchange Online, OneDrive for Business 5 TB, SharePoint, Teams, Defender for Office 365, Purview).
3. **Device** — laptop per standard hardware tier (see [`laptop-and-workstation-allocation.md`](laptop-and-workstation-allocation.md)).
4. **Intune enrollment** — device auto-enrolled via Windows Autopilot / Apple Business Manager.
5. **Defender for Endpoint** — sensor onboarded automatically at first sign-in.
6. **Base group memberships** — `All-Staff`, `Office-<City>`, `MFA-Required`, `Conditional-Access-Baseline`.
7. **Productivity suite** — Outlook, Teams, Word, Excel, PowerPoint, OneDrive sync client, Edge for Business.
8. **Security tooling** — Microsoft Authenticator (push), 1Password Business (SSO-enrolled), VPN client.
9. **Onboarding channels** — auto-added to the Teams team `ACME-New-Hires` and the manager's team site.
10. **Peripheral kit** — dock, monitor, keyboard, mouse, headset (office staff only; see allocation doc).

The IT request form is [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md). Managers attach a completed copy to the HRIS record.

## 4. SLAs (Standard Lead Times)

> All durations are in **business days**. Clock starts when the HRIS record reaches "Hired — Pending Onboarding" and the manager has approved the role bundle.

| Stage | Owner | Target | Hard SLA |
|-------|-------|--------|----------|
| Entra ID account + M365 license provisioned | Identity Engineering | Same business day | 1 business day |
| Laptop imaged and encrypted | Endpoint Engineering | 2 business days before start date | 1 business day before start date |
| Laptop shipped to remote hire / staged for in-office pickup | Endpoint Engineering | 3 business days before start date | 2 business days before start date |
| Group memberships and app entitlements finalized | IT Onboarding Specialist | By 09:00 IST on start date | By 12:00 IST on start date |
| Welcome email with temporary password sent | IT Onboarding Specialist | By 09:00 IST on start date | By 09:30 IST on start date |

**Expedited requests** (e.g., backfill of a critical role within 5 business days) require VP-level approval — contact `arjun.kapoor@acme.example` (IT Manager Hyderabad) or `ramesh.khanna@acme.example` (VP IT).

## 5. Approval Workflow

1. **HR creates the record** in the HRIS once the offer is signed. This fires a webhook to the ITSM platform (ServiceNow-equivalent, fictional — `helpdesk.acme.example`).
2. **Hiring manager approval.** The manager receives an approval task in the ITSM portal. They confirm:
   - Hardware tier (Standard / Power / ML-Workstation / Executive).
   - Office location (Hyderabad / Bengaluru / London / Seattle / Remote).
   - Role-based software bundle (Engineering, Sales, Finance, Support).
   - Special access (production AWS role, GitHub Enterprise team, Datadog admin, etc.).
3. **IT Onboarding Specialist review.** Geetha Iyer validates the request against the role catalog and the security baseline. Discrepancies are bounced back to the manager.
4. **Security review (conditional).** Any request that includes production access, privileged role assignment, or non-standard software is routed to the CISO's delegate (`rajan.mehta@acme.example` or delegated reviewer). See [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md).
5. **VP IT sign-off (conditional).** Required for: hardware tier above Standard, BYOD exception, or any role requiring privileged Entra ID roles (e.g., Global Administrator, Privileged Role Administrator). Ramesh Khanna (`ramesh.khanna@acme.example`) is the approver.
6. **Provisioning.** Once approved, Identity and Endpoint engineering execute in parallel.
7. **Hand-off to new hire.** On day one, the new hire receives the welcome email with a temporary password and a link to [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md).

## 6. Prerequisites

Before the IT request can be fulfilled, the following must be true:

- The offer is signed and recorded in the HRIS.
- The hiring manager has completed the role bundle questionnaire (sent automatically).
- The new hire's legal name and preferred name are finalized (the UPN is derived from preferred name).
- The shipping address (if remote) is on file and confirmed.
- The start date is at least 5 business days away for Standard requests (3 business days for expedited with VP sign-off).

## 7. Expected Outcomes

By 09:00 IST on the new hire's start date, all of the following are true:

- An Entra ID user exists in `acme.onmicrosoft.com` and a license is assigned.
- The laptop is staged (in-office) or in transit (remote).
- The new hire has received a temporary password via SMS to the phone number on file.
- The new hire can sign in at `https://portal.office.com` and complete the steps in [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md).
- The new hire's manager and onboarding buddy are copied on a confirmation email.

## 8. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Temporary password SMS never arrives | Phone number on file incorrect, or DND active on the line | Contact `helpdesk@acme.example` with the ticket ID; IT will re-issue via an outbound call. |
| `portal.office.com` sign-in fails with "user not found" | Entra ID account not yet created | Verify with `faisal.ahmed@acme.example`; create a manual account if HRIS webhook failed. |
| Laptop not delivered on the scheduled date | Courier delay or address validation failure | Endpoint Engineering (`suresh.babu@acme.example`) will issue a loaner device; original delivery is re-tracked. |
| New hire missing expected Teams channels | Group membership sync lag (up to 60 minutes) | Force a sync via the ITSM portal or wait one hour; if still missing, raise a P3 ticket. |
| Manager approval task not received | Manager's email not in correct security group | Re-route via ITSM admin console; contact `latha.krishnamurthy@acme.example`. |

## 9. Approval Requirements Summary

- **Standard new-hire request:** Hiring manager + IT Onboarding Specialist. No VP sign-off.
- **Non-standard hardware tier (above Standard):** + VP IT (`ramesh.khanna@acme.example`).
- **Production / privileged access:** + CISO delegate (`rajan.mehta@acme.example`).
- **BYOD exception:** + VP IT and CISO; see [`../03-security/byod-policy.md`](../03-security/byod-policy.md).
- **Expedited (< 5 business days):** + VP IT.

## 10. Related Documents

- [`../07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) — Day-one workflow that consumes the IT request output.
- [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md) — The IT request form.
- [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) — Signed at device handover.
- [`laptop-and-workstation-allocation.md`](laptop-and-workstation-allocation.md) — Standard hardware tiers.
- [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md) — New hire's next step after the request is fulfilled.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — IT escalation contacts.
- [`../00-company/employee-support-and-escalation.md`](../00-company/employee-support-and-escalation.md) — Company-wide escalation principles.
- [`../metadata/glossary.md`](../metadata/glossary.md) — Terminology.
