---
document_id: ACME-IT-016
title: Lost or Stolen Device Reporting
category: it
department: it-operations
applicable_roles: [all]
owner: Arjun Kapoor, IT Manager Hyderabad
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, lost-device, stolen, security, remote-wipe, fictional]
---

# Lost or Stolen Device Reporting

> ACME Corp fictional onboarding library. All hostnames, ticket references, and incident numbers are simulated. The Microsoft Intune remote-wipe capability is real Microsoft infrastructure; the ACME tenant integration is fictional.

## 1. Purpose

Defines the **immediate** steps an employee must take when a corporate-issued laptop (or other managed device) is lost or stolen. Time is critical — the goal is to limit data exposure to minutes, not hours. This document pairs with [`device-acceptance-and-responsibility.md`](device-acceptance-and-responsibility.md) (which the employee signed at handover) and [`equipment-replacement.md`](equipment-replacement.md) (the path to a replacement device).

> **If you are reading this because a device is missing right now:** skip to §3 immediately. The rest can wait.

## 2. Prerequisites

None — this document is intended to be **actionable** by any employee at any time, with no prerequisite reading.

> The single most important action is the **first phone call** in §3.1. Everything else can follow.

## 3. Immediate Actions (Within 2 Hours of Discovery)

### 3.1 Call IT + Security — the FIRST action

1. Phone the IT Helpdesk:
   - **Hyderabad:** `+91-40-0000-0000`
   - **Seattle:** `+1-206-555-0000`
   - **Other offices (out-of-hours):** the Hyderabad line is 24×7.
2. State clearly: "I have lost / had stolen my ACME corporate laptop."
3. Provide:
   - Your name and user principal name (`<firstname>.<lastname>@acme.example`).
   - The device's asset tag (printed on the underside sticker — e.g., `ACME-ASSET-100432`).
   - The location and approximate time of loss / theft.
   - A contact number where IT can reach you in the next 4 hours.
4. IT will:
   - Open a P1 ticket (e.g., `INC-2026-009999` — simulated).
   - Notify the on-call Endpoint Engineer (Suresh Babu or delegate) and the Security on-call (`security@acme.example` / CISO delegate).
   - Trigger the remote-wipe + disable + key-rotate sequence in §4.

### 3.2 File a Police Report (If Stolen)

- Within 24 hours, file a police report at the local station where the theft occurred.
- Obtain the report number; email it to `security@acme.example` and `helpdesk@acme.example` quoting the P1 ticket number.
- The report is required for:
  - Insurance claim processing (for devices with the remote-worker rider).
  - Travel-insurance reimbursement (for devices lost on travel).

### 3.3 Change Your Passwords

1. As soon as IT confirms the remote-wipe is queued (see §4.1), change your corporate password:
   - Navigate to `https://aka.ms/sspr` (real Microsoft URL).
   - Reset using any registered security info method.
2. Sign out of all active sessions:
   - `https://myaccount.microsoft.com → Sign-in everywhere → Sign out`.
3. Revoke active app passwords (if any) at `https://myaccount.microsoft.com → Security info → App passwords → Revoke`.
4. Revoke active MFA sessions at the same portal.
5. Rotate any 1Password vault secrets that may have been stored in browser autofill (the device was encrypted, but defense-in-depth applies).

## 4. IT Actions (Triggered Remotely)

> These are performed by IT on the corporate tenant; the employee does not need to do them. The employee should still understand them.

### 4.1 Remote Wipe via Intune

1. IT locates the device object in the Intune console (asset tag → device).
2. IT issues a **Wipe** command (not Retire — Wipe removes data and forces a reset; Retire only removes management).
3. Intune pushes the wipe command to the device at the next check-in.
   - If the device is online, the wipe executes within minutes.
   - If the device is offline, the wipe executes on next power-on / network connect (this may take days — hence the password rotation in §3.3).
4. The BitLocker / FileVault recovery key is rotated in Entra ID — the old key cannot unlock the disk even if an attacker extracts it.

### 4.2 Disable and Revoke

1. The Entra ID user object's "device registrations" list is pruned — the lost device is removed from the registered devices list.
2. Conditional Access refresh tokens issued to that device are revoked — any in-flight M365 sessions on that device fail at next refresh (within 1 hour).
3. The Wi-Fi SCEP certificate on the device is revoked in the CA's CRL — the device can no longer authenticate to `ACME-Corporate` Wi-Fi (per [`corporate-wifi-setup.md`](corporate-wifi-setup.md) §off-boarding).
4. The VPN profile is rotated; any cached VPN tokens are invalidated.

### 4.3 Audit and Forensic Review

1. Security pulls the device's Defender for Endpoint telemetry from the last 30 days.
2. Security reviews any unusual file access, USB ejection events, or off-network activity in the 72 hours before loss.
3. If anomalies are detected, the CISO is notified within 4 hours.

## 5. Timeline and Reporting

| Step | Owner | Timeframe |
|------|-------|-----------|
| Employee reports loss/theft | Employee | Within 2 hours of discovery |
| P1 ticket created | IT Helpdesk | Within 15 minutes of phone call |
| Remote wipe queued | Endpoint Engineering | Within 30 minutes of ticket |
| Password reset by employee | Employee | Within 60 minutes of ticket |
| Security review of telemetry | Security | Within 4 hours |
| Police report filed (stolen) | Employee | Within 24 hours |
| Insurance claim filed | Employee + IT | Within 5 business days |
| Replacement device provisioned | Endpoint Engineering | Within 2 business days (see [`equipment-replacement.md`](equipment-replacement.md)) |
| Post-incident review | IT Manager | Within 10 business days |

## 6. Insurance and Police

- **Office premises loss:** covered by ACME's office premises policy; no deductible to the employee.
- **Remote-worker rider:** attached to the asset record at allocation; covers up to USD 1,500 with a police report.
- **Travel loss:** travel insurance rider covers up to USD 1,500 with a police report.
- **Negligence:** if IT / Security determines the loss was due to negligence (e.g., device left visible in a parked car), the employee may be responsible for the deductible; this is reviewed case-by-case by HR + IT Manager.

## 7. Replacement Process

After §3 actions are complete and the immediate risk is contained, follow [`equipment-replacement.md`](equipment-replacement.md) for the replacement device flow:

1. The P1 ticket is converted to a replacement request.
2. Endpoint Engineering stages a replacement device (same tier) — typically within 2 business days.
3. For remote workers, the replacement is couriered; for in-office, it is staged at the IT depot.
4. The replacement is handed over per [`device-acceptance-and-responsibility.md`](device-acceptance-and-responsibility.md).
5. The old device's asset record in ITAM is marked `Lost` / `Stolen`; the device is added to the corporate block-list.

## 8. Expected Outcomes

After the lost-or-stolen flow:

- The lost device has been remote-wiped (or will be on next network connect).
- The employee's password is rotated; refresh tokens revoked.
- The Wi-Fi cert and VPN profile are revoked.
- A P1 ticket is on record with the timeline.
- A replacement device has been provisioned or is in flight.
- The lost device's asset record reflects the loss.

## 9. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Remote wipe stuck "pending" | Device offline; Intune waiting for check-in | Confirm with Endpoint Engineering; rely on password + token revocation as the primary defense (encryption protects data at rest). |
| Cannot reach IT Helpdesk phone (out-of-hours) | All agents busy | Use the ITSM portal `https://helpdesk.acme.example` and select the "Lost / Stolen Device" template — it auto-escalates to the on-call. |
| Employee cannot change password (no MFA device available) | Lost phone + lost laptop | Phone IT Helpdesk; IT will issue a TAP after manager identity verification. |
| Insurance claim rejected | Police report missing or filed late | File the report retroactively (better late than never); insurers accept reports filed within 7 days for theft claims. |
| Replacement tier unavailable (out of stock) | Procurement lag | Endpoint Engineering issues an equivalent or higher tier as a loaner; original tier ships when available. |

## 10. Approval Requirements

- **Remote wipe:** performed by Endpoint Engineering; no separate approval — the Helpdesk L2 can trigger.
- **Privileged device wipe (e.g., a server, a kiosk with prod access):** + Security on-call approval.
- **Replacement device:** standard flow per [`equipment-replacement.md`](equipment-replacement.md); no separate approval if same tier.
- **Negligence finding:** reviewed by IT Manager + HR (see [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md)).

## 11. Related Documents

- [`device-acceptance-and-responsibility.md`](device-acceptance-and-responsibility.md) — Responsibilities signed at handover.
- [`equipment-replacement.md`](equipment-replacement.md) — Replacement flow.
- [`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md) — Lost phone + MFA recovery.
- [`microsoft-entra-id-and-sso.md`](microsoft-entra-id-and-sso.md) — Token revocation.
- [`corporate-vpn-configuration.md`](corporate-vpn-configuration.md) — VPN token rotation.
- [`corporate-wifi-setup.md`](corporate-wifi-setup.md) — Wi-Fi cert revocation.
- [`it-support-and-troubleshooting.md`](it-support-and-troubleshooting.md) — How to open the ticket.
- [`it-access-revocation.md`](it-access-revocation.md) — Access revocation context.
- [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md) — Incident response.
- [`../03-security/device-encryption.md`](../03-security/device-encryption.md) — Encryption that protects the data.
- [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md) — Negligence review.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — IT / Security on-call contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — Remote wipe, TAP, SCEP, conditional access definitions.
