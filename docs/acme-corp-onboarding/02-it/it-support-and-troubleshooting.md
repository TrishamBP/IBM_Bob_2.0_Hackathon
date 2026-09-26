---
document_id: ACME-IT-015
title: IT Support and Troubleshooting
category: it
department: it-operations
applicable_roles: [all]
owner: Latha Krishnamurthy, IT Helpdesk Lead
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, support, troubleshooting, ticketing, sla, fictional]
---

# IT Support and Troubleshooting

> ACME Corp fictional onboarding library. The ITSM portal `helpdesk.acme.example` and the ticketing reference numbers below are simulated.

## 1. Purpose

Explains how employees open IT tickets, the Service Level Targets (SLTs / SLAs) that apply, common self-service fixes for the most frequent issues, how to grant remote assistance to IT, the escalation paths, and the urgent phone numbers for time-critical incidents.

## 2. How to Open a Ticket

There are three intake channels:

1. **Self-service portal:** `https://helpdesk.acme.example` (simulated). Sign in with `<firstname>.<lastname>@acme.example`; pick the category; describe the issue; attach screenshots.
2. **Email:** `helpdesk@acme.example` — the message becomes a ticket automatically; the subject line becomes the ticket title.
3. **Phone (urgent only):** Hyderabad `+91-40-0000-0000`, Seattle `+1-206-555-0000`, Bengaluru and London use the Hyderabad line for urgent issues.

Each ticket gets a reference like `INC-2026-001234` (simulated). Quote this in any follow-up.

## 3. Ticket Priorities and Service Level Targets

| Priority | Definition | Response SLA | Resolution SLA |
|----------|------------|---------------|-----------------|
| **P1 — Critical** | Production down, all-hands outage, security incident in progress | 15 minutes | 4 hours |
| **P2 — High** | Major feature broken for many users; device non-functional | 1 hour | 1 business day |
| **P3 — Normal** | Single-user issue, workaround available | 4 business hours | 3 business days |
| **P4 — Low** | Informational / cosmetic / how-to question | 1 business day | 5 business days |

> SLA clock is **business hours** for P3 / P4 (Hyderabad: 09:00–18:00 IST Mon–Fri; Seattle: 09:00–18:00 PST Mon–Fri; London: 09:00–18:00 GMT Mon–Fri). P1 / P2 are 24×7.

## 4. Common Self-Service Fixes

> Try these before opening a P3 ticket — IT Helpdesk will ask you to do them anyway.

### 4.1 "I can't sign in to M365 / Teams / Outlook"

1. Verify you are using `<firstname>.<lastname>@acme.example` (not your personal email).
2. Clear the browser cache or try a private window.
3. Check `https://status.acme.example` (simulated status page) for an active incident.
4. If MFA push does not arrive: tap "I can't use my Authenticator app right now" in the sign-in flow and use SMS fallback.
5. If still failing: open a P3 ticket; include the time, the exact error message, and a screenshot.

### 4.2 "My laptop is slow"

1. Open Task Manager (Windows) / Activity Monitor (macOS) and identify the top CPU / memory consumer.
2. Reboot the laptop — many issues clear with a reboot.
3. Check Company Portal / Self Service for pending app installs that may be running.
4. Run a Defender quick scan to rule out malware.
5. If persisting after the reboot: open a P3 ticket; attach Task Manager screenshot and `dxdiag` (Windows) or `system_profiler` (macOS) output.

### 4.3 "I cannot reach an internal site"

1. Verify you are on the corporate Wi-Fi (per [`corporate-wifi-setup.md`](corporate-wifi-setup.md)) or the VPN is connected (per [`corporate-vpn-configuration.md`](corporate-vpn-configuration.md)).
2. Try a different browser; try private mode.
3. Check `https://status.acme.example` for the specific site.
4. If persisting: open a P3 ticket; include `tracert` (Windows) / `traceroute` (macOS) output to the failing hostname.

### 4.4 "My printer / dock / monitor is not detected"

1. Disconnect and reconnect the cable.
2. For docks: unplug the dock from power for 10 seconds; reconnect.
3. Update firmware via the Company Portal (if a firmware update is offered for your dock model).
4. If persisting: open a P3 ticket; bring the device to the IT depot for in-person diagnostic.

### 4.5 "I lost my phone / Authenticator"

1. **Immediately** contact IT Helpdesk and Identity Engineering — see [`lost-or-stolen-device-reporting.md`](lost-or-stolen-device-reporting.md) and [`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md) §troubleshooting.
2. IT will issue a Temporary Access Pass for the duration of the recovery.

## 5. Granting Remote Assistance

For P2 / P3 issues that require hands-on remediation, IT may ask you to grant remote assistance:

1. IT sends a Teams chat message with a link to the **Quick Assist** (Windows) / **Screen Sharing** (macOS) session.
2. Click the link — Quick Assist launches (Windows: type the 6-digit code IT provided).
3. You will see a prompt: "Allow `<IT-person-name>` to share control of your device?" Click **Allow**.
4. IT can now see your screen and control your mouse / keyboard for the duration of the session.
5. You can revoke access at any time by closing Quick Assist or pressing `Esc`.

> IT will **never** ask you for your password, MFA code, or recovery key. If anyone does — including someone claiming to be IT — deny the request and report to `security@acme.example` immediately. This is the canonical social-engineering warning; see [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md).

## 6. Escalation Paths

| Stage | Contact | When |
|-------|---------|------|
| L1 — Helpdesk | `helpdesk@acme.example`, `+91-40-0000-0000` / `+1-206-555-0000` | First point of contact for all issues |
| L2 — IT Onboarding / Endpoint / Identity | Geetha Iyer, Suresh Babu, Faisal Ahmed | When L1 cannot resolve in SLA, or for issues tied to a specific domain |
| L3 — Engineering / App owners | Per [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) | For app-specific outages (Jira, GitHub, Vault) |
| Manager — IT Manager Hyderabad | `arjun.kapoor@acme.example` | If SLA is breached and L1/L2 cannot resolve |
| VP — VP IT | `ramesh.khanna@acme.example` | For repeated SLA breaches or systemic issues |
| Security incident — CISO | `rajan.mehta@acme.example` | For suspected breach / data exfiltration |
| Out-of-band (if Entra ID itself is down) | Phone the Hyderabad office `+91-40-0000-0000` | The IVR routes to IT even when email / Teams are down |

## 7. Urgent Phone Numbers

| Office | Number (fictional) | Hours |
|--------|---------------------|-------|
| Hyderabad (HQ) | `+91-40-0000-0000` | 24×7 |
| Seattle | `+1-206-555-0000` | 24×7 |
| Bengaluru | routes to Hyderabad | business hours |
| London | routes to Hyderabad out-of-hours | business hours local |

> **Use the urgent phone for:** suspected security incidents, lost / stolen device (within 2 hours of discovery per [`lost-or-stolen-device-reporting.md`](lost-or-stolen-device-reporting.md)), exec / VIP outages, VIP-event-critical support, and when you cannot reach the ITSM portal because the network or Entra ID is down.

## 8. Self-Service Resources

- **Knowledge base:** `https://wiki.acme.example` (simulated) — runbooks, FAQ, how-tos.
- **Status page:** `https://status.acme.example` (simulated) — subscribe for incident notifications.
- **ACME Onboarding portal:** `https://portal.acme.example` (simulated) — links, day-one tasks.
- **ACME ServiceNow-equivalent ITSM:** `https://helpdesk.acme.example` (simulated) — self-service catalog, ticket history.
- **Self-service password reset:** `https://aka.ms/sspr` (real Microsoft URL).

## 9. Expected Outcomes

After this document:

- The new hire knows the three intake channels for tickets and the 4 priorities and their SLTs.
- The new hire can attempt self-service fixes before opening a P3 ticket.
- The new hire knows how to grant remote assistance safely and the canonical social-engineering warning.
- The new hire knows the escalation path and the urgent phone numbers.

## 10. Troubleshooting (Meta)

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| ITSM portal is down | IT-wide outage | Check `status.acme.example`; if down, phone `+91-40-0000-0000`. |
| Quick Assist fails to launch | App not installed (Windows) | Install via Company Portal; on macOS, Screen Sharing is built-in. |
| No reply from Helpdesk within SLA | Ticket mis-routed | Reply to your ticket email; escalate via phone. |
| Status page does not list your incident | It may not yet be detected | Phone the urgent line; report so IT can publish. |

## 11. Approval Requirements

- **Standard support:** no approval needed.
- **VIP / executive support:** handled by L2 directly (the IT Onboarding Specialist and IT Manager are the named contacts).
- **Out-of-scope requests (e.g., personal device support):** declined; consider the BYOD exception (see [`../03-security/byod-policy.md`](../03-security/byod-policy.md)).

## 12. Related Documents

- [`new-employee-it-request.md`](new-employee-it-request.md) — How requests begin.
- [`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md) — MFA / sign-in support.
- [`microsoft-entra-id-and-sso.md`](microsoft-entra-id-and-sso.md) — Conditional access / SSO support.
- [`corporate-vpn-configuration.md`](corporate-vpn-configuration.md) — VPN support.
- [`corporate-wifi-setup.md`](corporate-wifi-setup.md) — Wi-Fi support.
- [`lost-or-stolen-device-reporting.md`](lost-or-stolen-device-reporting.md) — Lost device urgent path.
- [`equipment-replacement.md`](equipment-replacement.md) — Hardware replacement path.
- [`../00-company/employee-support-and-escalation.md`](../00-company/employee-support-and-escalation.md) — Company-wide escalation principles.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Full contact list.
- [`../metadata/glossary.md`](../metadata/glossary.md) — SLA, P1–P4, PIM definitions.
