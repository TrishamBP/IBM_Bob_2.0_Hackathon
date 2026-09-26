---
document_id: ACME-IT-004
title: Windows 11 and macOS Workstation Setup
category: it
department: it-operations
applicable_roles: [all]
owner: Suresh Babu, Endpoint Engineer
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, setup, windows-11, macos, intune, bitlocker, filevault, fictional]
---

# Windows 11 and macOS Workstation Setup

> ACME Corp fictional onboarding library. The tenant name `acme.onmicrosoft.com` and all endpoints are simulated for training purposes.

## 1. Purpose

Walks the new hire through the first power-on, Intune enrollment confirmation, Windows Hello / Touch ID setup, BitLocker / FileVault verification, and first-time corporate sign-in. This is the first technical step after [`device-acceptance-and-responsibility.md`](device-acceptance-and-responsibility.md) and immediately precedes [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md).

## 2. Prerequisites

- The new hire has accepted the device per [`device-acceptance-and-responsibility.md`](device-acceptance-and-responsibility.md).
- The new hire has the temporary password delivered by IT (via SMS to the phone on file, or printed on the welcome envelope for in-office handover).
- The new hire is on a network with internet access (home Wi-Fi, mobile hotspot, or the office `ACME-Corporate` SSID).
- The new hire has installed Microsoft Authenticator on their personal phone (per [`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md)) — this is required because the first corporate sign-in will trigger an MFA challenge.

> If the personal phone is not yet set up, IT can issue a Temporary Access Pass (TAP) for the first sign-in. Contact `helpdesk@acme.example`.

## 3. Initial Power-On

### 3.1 Windows 11 (Dell Latitude tiers)

1. Plug the laptop into power and open the lid.
2. Press the power button. The Dell logo appears, then the ACME-branded Windows 11 OOBE screen.
3. The OOBE screen will display: "Welcome to ACME Corp. Sign in with your corporate account."
4. Connect to Wi-Fi when prompted. For office staff, select `ACME-Corporate` (see [`corporate-wifi-setup.md`](corporate-wifi-setup.md)); for remote staff, select your home network.
5. On the "Let's set things up" screen, the device will check in with Intune automatically (this is the Autopilot profile; no action needed).

### 3.2 macOS (MacBook Pro tiers)

1. Plug the MacBook into power and open the lid.
2. Press the power button. After the Apple logo, the ACME-branded Setup Assistant launches (Remote Management via Apple Business Manager).
3. The screen displays: "This Mac is being set up for you by ACME Corp."
4. Connect to Wi-Fi (same guidance as above).
5. The device checks in with Apple Business Manager and pulls the ACME MDM profile. Confirm the MDM enrollment when prompted — **this is mandatory**; declining it will brick the device for corporate use.

## 4. First-Time Corporate Sign-In

1. At the sign-in prompt, enter your corporate user principal name: `<firstname>.<lastname>@acme.example` (the same address used to receive the welcome email).
2. Enter the temporary password provided by IT (placeholder: `<temp-pass-from-helpdesk>`). You will be required to change it on first use.
3. A Microsoft Entra ID conditional-access challenge will appear. Complete the MFA prompt in Microsoft Authenticator (see [`microsoft-entra-id-and-sso.md`](microsoft-entra-id-and-sso.md)).
4. Set a new permanent password that meets the ACME baseline (16+ characters, mix of upper/lower/digits/symbols, no dictionary words). See [`../03-security/password-and-mfa-requirements.md`](../03-security/password-and-mfa-requirements.md).
5. The desktop loads. A toast notification appears: "Welcome, `<firstname>`. Your device is managed by ACME Corp."

## 5. Windows Hello (Windows 11) / Touch ID (macOS)

### 5.1 Windows Hello (Windows 11)

1. Open **Settings → Accounts → Sign-in options**.
2. Select **Windows Hello Face** or **Windows Hello Fingerprint** (depending on device capability — Latitude 5540/7450 have both).
3. Follow the prompts to enroll your face / fingerprint. The device may ask for an additional PIN — set a 6-digit PIN (this is the fallback when biometrics fail).
4. The PIN is bound to the hardware via the TPM. Do not write it down on the device or in any unencrypted note app.

### 5.2 Touch ID (macOS)

1. Open **System Settings → Touch ID & Password**.
2. Click **Add Fingerprint** and follow the prompts. Enroll at least two fingers.
3. Set a login password as the fallback (16+ characters per ACME baseline).

## 6. BitLocker / FileVault Verification

> Do not skip this step. Encryption must be verified as active before you store any corporate data on the device.

### 6.1 Windows 11 / BitLocker

1. Open **Settings → Privacy & security → Device encryption**.
2. The status should read **"BitLocker is on"** with the C: drive showing a padlock icon.
3. Verify the recovery key is escrowed: open a browser, go to `https://myaccount.microsoft.com` (simulated Microsoft Entra ID My Account), sign in, navigate to **Security info → Devices → BitLocker recovery keys**. Your device's recovery key should be listed there.
4. If the recovery key is missing, raise a P3 ticket — do not continue using the device for sensitive work until escrow is verified.

### 6.2 macOS / FileVault

1. Open **System Settings → Privacy & Security → FileVault**.
2. The status should read **"FileVault is turned on for the disk 'Macintosh HD'."**
3. Confirm the recovery key is escrowed: in the same `myaccount.microsoft.com` portal, under **Devices**, find your Mac — the FileVault recovery key should be listed under the device details.

## 7. Intune Enrollment Verification

### 7.1 Windows 11

1. Open **Settings → Accounts → Access work or school**.
2. You should see: `<firstname>.<lastname>@acme.example`, **"Connected to ACME Corp"** with the MDM flag enabled.
3. Open the **Company Portal** app (pre-installed), sign in, and confirm the device appears under **Devices** with status **"Compliant."**

### 7.2 macOS

1. Open **System Settings → Privacy & Security → Profiles**.
2. Under **MDM Profile**, you should see the **ACME Corp Management** profile with a green check.
3. Open the **Company Portal** app (in /Applications), sign in, and confirm the device is compliant.

## 8. Defender for Endpoint Verification

On both platforms, the Defender sensor should start automatically within 5 minutes of first sign-in. To verify:

- **Windows 11:** Open **Task Manager → Details** and confirm `MsMpEng.exe` is running. Open **Windows Security** and confirm the tile reads "No threats found" and "Managed by ACME Corp."
- **macOS:** Open **Microsoft Defender** from the menu bar. The icon should show a green shield. **Sign in** with your corporate account when prompted.

## 9. First-Time Application Launches

After enrollment, the M365 apps will be available from the Start menu (Windows) or Launchpad (macOS). On first launch of each, sign in with `<firstname>.<lastname>@acme.example` and complete the MFA challenge.

- **Outlook** — proceed to [`outlook-and-company-calendar-setup.md`](outlook-and-company-calendar-setup.md).
- **Teams** — proceed to [`microsoft-teams-setup.md`](microsoft-teams-setup.md).
- **OneDrive** — proceed to [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md) §SharePoint/OneDrive first-run.
- **Edge for Business** — already signed in via Windows Hello; bookmarks and favorites are pushed via Intune.

## 10. Expected Outcomes

After completing this document:

- The device shows as **Compliant** in Intune.
- BitLocker / FileVault is active and the recovery key is escrowed to Entra ID.
- Windows Hello / Touch ID is enrolled.
- The new hire has signed in to the device at least once and changed the temporary password.
- Defender for Endpoint is reporting to the corporate tenant.

## 11. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| OOBE shows generic Microsoft screen, not ACME branding | Autopilot / Apple Business Manager profile not assigned | Contact Endpoint Engineering (`suresh.babu@acme.example`); the device hash may need re-import. |
| "Your account does not exist in this tenant" | Wrong UPN entered — check spelling | Use exactly `<firstname>.<lastname>@acme.example`. |
| MFA prompt does not appear on personal phone | Authenticator not enrolled, or push notification missed | Tap "I can't use my Microsoft Authenticator app right now" and use the TAP fallback (contact helpdesk). |
| BitLocker status shows "Off" | TPM not initialized at imaging | Endpoint Engineering will trigger encryption remotely; reboot may be required. |
| FileVault prompts for personal recovery key | Mac not bound to corporate MDM at imaging | Do not enter a personal key; raise a P2 ticket — device must be re-imaged. |
| Defender for Endpoint sensor stuck on "Starting" | Network firewall blocking the sensor's cloud endpoint | Connect to corporate VPN (see [`corporate-vpn-configuration.md`](corporate-vpn-configuration.md)); if persists, raise a P2 ticket. |
| "Compliance pending" in Company Portal after 30 minutes | Intune policy sync lag | Force a sync: Company Portal → Settings → Sync. |

## 12. Approval Requirements

- None for the standard flow described above.
- **Exception:** If a new hire needs local administrator rights on the device (e.g., for certain DevOps roles), this requires VP IT approval (`ramesh.khanna@acme.example`) and is granted via a Just-In-Time Entra ID Privileged Identity Management assignment. See [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md).

## 13. Related Documents

- [`device-acceptance-and-responsibility.md`](device-acceptance-and-responsibility.md) — Preceding step.
- [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md) — Following step.
- [`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md) — Required prerequisite for MFA.
- [`microsoft-entra-id-and-sso.md`](microsoft-entra-id-and-sso.md) — IdP / conditional access context.
- [`corporate-wifi-setup.md`](corporate-wifi-setup.md) — Office Wi-Fi.
- [`corporate-vpn-configuration.md`](corporate-vpn-configuration.md) — Remote access.
- [`../03-security/device-encryption.md`](../03-security/device-encryption.md) — Encryption baseline.
- [`../03-security/password-and-mfa-requirements.md`](../03-security/password-and-mfa-requirements.md) — Password rules.
- [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) — Handover form.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Endpoint Engineering contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — OOBE, MDM, TPM, Autopilot definitions.
