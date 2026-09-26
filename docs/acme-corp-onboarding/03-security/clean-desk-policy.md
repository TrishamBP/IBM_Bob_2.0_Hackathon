---
document_id: ACME-SEC-013
title: Clean Desk and Clear Screen Policy
category: security
department: information-security
applicable_roles: [all]
owner: Fatima Sheikh, SOC Lead
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, clean-desk, clear-screen, physical-security, fictional]
---

# Clean Desk and Clear Screen Policy

> ACME Corp fictional onboarding library. Hostnames (`helpdesk.acme.example`, `vault.acme.example`) and mailboxes are fictional.

## 1. Purpose

This document defines ACME Corp's "clean desk and clear screen" expectations — the physical-world analogue of [`data-classification.md`](data-classification.md). The strongest digital controls do not matter if a printed customer list is left on a desk overnight, or if a laptop screen is visible to the person at the next café table. This policy sets the standard for handling Confidential and Restricted information in physical form.

## 2. Scope

This applies to:

- All ACME workforce members, contractors, and authorized third parties.
- All ACME offices (Hyderabad, Bengaluru, London, Seattle) and any co-working or customer site where ACME work is performed.
- All remote work and home-office locations used for ACME work (see [`../01-hr/remote-and-hybrid-working-policy.md`](../01-hr/remote-and-hybrid-working-policy.md)).
- All ACME devices, paper, whiteboards, and physical media in any location.

## 3. Core Principle

**No Confidential or Restricted data should be visible to anyone who does not have a need-to-know, at any time.** This applies whether the data is on a screen, on paper, on a whiteboard, or audible in a conversation. The default state is "clean" — clear screen, no paper, no whiteboard notes, no visible documents.

## 4. Clear Screen — Lock When You Step Away

| Requirement | Detail |
|-------------|--------|
| **Auto-lock after 5 minutes** | Enforced by Intune on every ACME-issued laptop. |
| **Manual lock** | Lock your screen manually (Win+L on Windows, Ctrl+Cmd+Q on macOS) every time you step away — do not wait for the 5-minute timer. |
| **In the office** | Lock before standing up. Lock before turning your back on the screen. |
| **In a café / public space** | Lock if you leave the table. Use a privacy screen filter (issued on request from IT) so the screen is not visible to others. |
| **In a meeting** | Lock before standing up to leave the room. Do not leave a laptop open in a meeting room when you walk out. |
| **At home** | Lock if family members can see your screen. Confidential and Restricted data should not be visible to family. |
| **On a video call** | Close Confidential and Restricted documents before sharing your screen. Re-check what is open before clicking "Share." |
| **Docking stations / monitors** | Lock the laptop before undocking. The external monitor may briefly continue showing the last frame — be aware of who can see it. |

## 5. Clean Desk — Paper and Whiteboards

| Item | Rule |
|------|------|
| **Printed Confidential or Restricted documents** | Do not leave on the desk overnight. Store in a locked cabinet. Shred when no longer needed (cross-cut shredder). |
| **Whiteboards with Confidential or Restricted content** | Erase before leaving the room. Photographs of whiteboards are stored at the appropriate classification tier — see [`data-classification.md`](data-classification.md). |
| **Sticky notes with passwords** | **Forbidden.** Passwords go in 1Password (see [`../02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md)). A sticky note with a password is a violation of [`password-and-mfa-requirements.md`](password-and-mfa-requirements.md). |
| **Customer documents** | Never printed in the office without a documented business need. Customer data is Restricted by default — see [`customer-data-handling.md`](customer-data-handling.md). |
| **Visitor badges** | Returned at the end of the visit. Visitors must be escorted at all times in restricted areas. |
| **Laptops** | Taken home or locked in a drawer overnight. Do not leave laptops in cars overnight. |
| **Phones and YubiKeys** | Taken with you. Never left on the desk unattended. |
| **Printed source code** | Not permitted. Source code is Confidential — see [`source-code-security.md`](source-code-security.md). |

## 6. Secure Disposal of Paper

- All Confidential and Restricted paper must be shredded in a cross-cut shredder (provides on each floor of every ACME office).
- Public and Internal paper may be recycled normally.
- When in doubt about classification, shred.
- Shredded paper is collected by the facilities vendor; the vendor is bound by NDA and the destruction is logged.

## 7. Home-Office Considerations

For remote workers and hybrid workers at home:

| Concern | Mitigation |
|---------|------------|
| **Family members can see the screen** | Privacy screen filter (issued on request). Lock when stepping away. Work in a separate room when handling Restricted data. |
| **Visitors at home** | Do not leave Confidential/Restricted documents out when visitors are present. Lock the laptop. |
| **Printing at home** | Discouraged. If unavoidable, treat printed Confidential/Restricted paper as in §5 — store locked, shred with a cross-cut shredder (not a strip-cut shredder). |
| **Voice calls** | Use a headset; do not use speakerphone for Confidential content if anyone else is in the room. |
| **Smart speakers / always-listening devices** | Disable the microphone when handling Confidential conversations, or work in a room without such devices. |
| **Doorstep deliveries of corporate assets** | Address to the office when possible. If shipped home, arrange for someone to receive, or use a secure pickup point. |

## 8. Whiteboards and Meeting Rooms

- Reserve meeting rooms via the corporate calendar system — do not assume a room is private.
- Erase whiteboards at the end of the meeting.
- Do not leave printed handouts in the meeting room.
- If a meeting room has glass walls, assume the content is visible — do not display Confidential/Restricted content where it is visible from outside the room.
- Book a "secure room" (no glass, no windows to common areas) for discussions of Confidential/Restricted content.

## 9. Public Spaces

- Do not open Confidential/Restricted documents on a laptop in a café, airport lounge, train, plane, or other public space.
- If you must work in public (e.g., during travel), use a privacy screen filter and sit with your back to a wall.
- Do not take confidential phone calls in public — reschedule or use a private space.
- Be aware of "shoulder surfing" — attackers photograph screens in public spaces.

## 10. Responsibilities

| Role | Responsibility |
|------|----------------|
| **Every workforce member** | Locks screen when stepping away. Keeps desk clean. Shreds Confidential paper. Reports violations. |
| **People Managers** | Reinforce the policy with their teams. Ensure team members have the equipment they need (privacy filters, lockable cabinets). |
| **Facilities** | Provides shredders, lockable cabinets, secure meeting rooms. |
| **IT** | Issues privacy screen filters on request. Enforces the 5-minute auto-lock via Intune. |
| **SOC Lead** (`Fatima Sheikh`) | Reviews physical-security incidents. Coordinates with Facilities on hardware. |

## 11. Enforcement

- Intune enforces the 5-minute auto-lock; users cannot extend it.
- Facilities runs occasional "clean desk audits" overnight — Confidential/Restricted paper left out is photographed, the owner is contacted, and repeated violations are escalated to the manager.
- Conference room booking system flags "secure room" bookings for review by the SOC if the meeting is unusually long or unusual hours.
- Violations are addressed under [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md).

## 12. Exceptions

Exceptions (e.g., a research lab that requires open whiteboards) require SOC Lead (`Fatima Sheikh`) approval and a documented compensating control (e.g., the lab is access-controlled, no external visitors). Email `security-oncall@acme.example` (fictional).

## 13. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`data-classification.md`](data-classification.md) — Drives which data the clean-desk rules apply to.
- [`acceptable-use-policy.md`](acceptable-use-policy.md) — Asset handling.
- [`device-encryption.md`](device-encryption.md) — At-rest control that complements clear-screen.
- [`password-and-mfa-requirements.md`](password-and-mfa-requirements.md) — Sticky notes are forbidden for passwords.
- [`customer-data-handling.md`](customer-data-handling.md) — Customer data is never printed casually.
- [`confidentiality-agreement.md`](confidentiality-agreement.md) — Underlying obligations.
- [`../01-hr/remote-and-hybrid-working-policy.md`](../01-hr/remote-and-hybrid-working-policy.md) — Home-office rules.
- [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md) — Enforcement.
- [`../02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md) — Where passwords go (not sticky notes).
- [`../02-it/windows-11-and-macos-workstation-setup.md`](../02-it/windows-11-and-macos-workstation-setup.md) — Auto-lock configuration.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — SOC Lead and Facilities contacts.
