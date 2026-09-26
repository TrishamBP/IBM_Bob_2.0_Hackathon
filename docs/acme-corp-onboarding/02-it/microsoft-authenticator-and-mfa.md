---
document_id: ACME-IT-009
title: Microsoft Authenticator and MFA
category: it
department: it-operations
applicable_roles: [all]
owner: Faisal Ahmed, Identity Engineer
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, mfa, authenticator, security, entra-id, fictional]
---

# Microsoft Authenticator and MFA

> ACME Corp fictional onboarding library. The Microsoft Authenticator app is real Microsoft software. The tenant `acme.onmicrosoft.com` is simulated. No live credentials are demonstrated.

## 1. Purpose

Walks the new hire through installing Microsoft Authenticator on a personal iOS / Android phone, enrolling for push MFA against the ACME Entra ID tenant, backing up the Authenticator account, registering an optional hardware second factor (FIDO2 / YubiKey), and configuring fallback methods. MFA is **mandatory** for every ACME sign-in — there is no exemption.

## 2. Prerequisites

- A personal iOS device (iOS 16+) or Android device (Android 10+). ACME does **not** manage your personal phone; the device is used only to receive push notifications.
- Biometric unlock on the personal phone (Face ID, Touch ID, or fingerprint) — required by Authenticator to approve push notifications.
- The corporate identity (`<firstname>.<lastname>@acme.example`) provisioned and activated per [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md).
- A temporary password or TAP (Temporary Access Pass) from IT to complete the binding.

## 3. Step 1 — Install Microsoft Authenticator

1. On your personal phone, open the App Store (iOS) or Google Play (Android).
2. Search for "Microsoft Authenticator" (publisher: Microsoft Corporation).
3. Install the app. Grant the requested permissions:
   - **Notifications** — required for push MFA prompts.
   - **Camera** — required for scanning QR codes during enrollment.
   - **Biometrics** — required to approve pushes with Face ID / Touch ID / fingerprint.

> ACME does **not** enroll your personal phone into Intune. The Authenticator app runs on the personal device; only the corporate identity is bound to it.

## 4. Step 2 — Enroll for Push MFA

> The simplest path is to enroll during the security-info registration in [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md). The steps below are the canonical reference.

1. On your **corporate laptop**, open a browser and navigate to `https://myaccount.microsoft.com`.
2. Sign in with `<firstname>.<lastname>@acme.example` and the temporary password / TAP.
3. Navigate to **Security info → Add sign-in method → Microsoft Authenticator (notification)**.
4. On the next screen, choose:
   - **Account type:** "Work or school account".
5. The page shows a QR code.
6. On your **personal phone**, open Microsoft Authenticator, tap **Add account → Work or school account**, and scan the QR code on the laptop screen.
7. The phone displays a verification prompt. Approve it.
8. Back on the laptop, Entra ID sends a test push to your phone. Approve it (you'll be asked to enter the on-screen number — e.g., "42" — into the phone, which is the **number-matching** feature that prevents push fatigue / MFA fatigue attacks).
9. Enrollment complete.

## 5. Step 3 — Back Up the Authenticator Account

> If you lose your phone or upgrade, a backup allows you to restore your corporate MFA account without calling IT. Backups are encrypted with a recovery code you control.

1. In Microsoft Authenticator: **Settings → Backup**.
2. The app stores the encrypted backup in:
   - **iOS:** iCloud Keychain.
   - **Android:** Microsoft account (or Samsung account on Samsung devices).
3. **Write down the recovery code** displayed on screen. Store it only in your 1Password Business vault (see [`password-manager-configuration.md`](password-manager-configuration.md)) — never in an unencrypted note app, email, or chat.

## 6. Step 4 — Register an Optional Hardware Second Factor (FIDO2)

> Recommended for engineers, anyone with privileged access, and anyone who travels frequently. YubiKey 5C NFC is the ACME standard. Issued by Endpoint Engineering.

1. Obtain a YubiKey from the IT depot (in-office) or by raising a P3 ticket (remote).
2. On your **corporate laptop**, navigate to `https://myaccount.microsoft.com → Security info → Add sign-in method → Security key (FIDO2)`.
3. Tap the key on the laptop's NFC reader (or insert into a USB-C port).
4. The browser prompts you to set a PIN on the key (6–8 digits).
5. Touch the key's gold contact when prompted.
6. Entra ID saves the FIDO2 credential against your user object.
7. Test by signing out and signing back in using the security key as the sign-in method.

> A lost YubiKey does **not** lock you out — your Authenticator push remains valid and you can enroll a replacement key immediately.

## 7. Step 5 — Configure Fallback Methods

At minimum, the new hire must have:

- **Primary:** Microsoft Authenticator (push, number-matching).
- **Fallback 1:** SMS to the personal phone (`+91-...` / `+1-...` / `+44-...`).
- **Fallback 2:** An alternate phone number — typically a spouse, parent, or trusted contact — that Entra ID can call with an automated voice code.
- **Optional:** FIDO2 security key.

To configure:

1. In `https://myaccount.microsoft.com → Security info → Add method`:
   - **Phone** → select "Mobile phone" → enter number → select "Send me a code by text message" → verify the SMS.
   - **Phone** → select "Alternate phone" → enter a different number → verify the voice call.
2. Save. The list should now show 3 (or 4) methods.

## 8. What an MFA Prompt Looks Like

When you sign in to any ACME app, the prompt appears on your phone:

- The push notification displays **"ACME Corp"`**, the **app name** you are signing in to, and a **number** (e.g., 42).
- The phone app shows three number buttons; tap the matching number.
- Authenticator then asks for your biometric (Face ID / Touch ID) to confirm.
- The sign-in proceeds on the laptop.

**Never approve a push you did not initiate.** If you receive an unexpected push, deny it and report to `security@acme.example` immediately — it may indicate password compromise (see [`../03-security/password-and-mfa-requirements.md`](../03-security/password-and-mfa-requirements.md)).

## 9. Expected Outcomes

After this document:

- The new hire has Authenticator installed on a personal phone and enrolled for push MFA against `acme.onmicrosoft.com`.
- A backup is enabled with the recovery code stored in 1Password.
- At least one fallback method (SMS) is registered.
- The new hire understands number-matching and the MFA-fatigue risk.

## 10. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Push notification never arrives | Phone in airplane mode / Do-Not-Disturb / Authenticator background-restricted | Disable DND; on Android, allow Authenticator to run in background; reboot phone. |
| "Cannot connect to service" in Authenticator | Phone time skew > 5 min from NTP | Sync phone clock to network time. |
| Lost phone, no backup, no fallback | MFA enrollment incomplete | Call IT Helpdesk (`helpdesk@acme.example`, +91-40-0000-0000); Identity Engineering will issue a TAP after manager verification. |
| Lost phone with backup | Restore on a new phone using the recovery code | Restore → re-enroll corporate identity → approve the verification push from any remaining fallback. |
| YubiKey not recognized on macOS | Browser not WebAuthn-enabled, or USB-C port restriction | Use Safari / Chrome; on managed Macs, USB-C is enabled by policy. |
| Number-matching screen shows no numbers | Old Authenticator version | Update Authenticator from the App Store / Play Store. |
| Authenticator prompts for every Teams launch | Token cache issue on the corporate device | Sign out and back in to Teams; clear the SSO token cache via Settings → Accounts → Access work or school → Disconnect / Reconnect. |

## 11. Approval Requirements

- **Authenticator enrollment:** no approval — it is mandatory for every account.
- **SMS / alternate phone fallback:** no approval — personal choice (the phone numbers are stored encrypted in Entra ID).
- **FIDO2 / YubiKey issuance:** Endpoint Engineering issues the device; the user pays nothing; lost YubiKeys incur a USD 50 replacement fee unless lost via theft (with a police report).
- **Exemption from MFA:** not available. MFA is enforced by conditional access; there is no role without it.

## 12. Related Documents

- [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md) — When MFA is first triggered.
- [`microsoft-entra-id-and-sso.md`](microsoft-entra-id-and-sso.md) — Conditional access and IdP context.
- [`password-manager-configuration.md`](password-manager-configuration.md) — Where to store the Authenticator recovery code.
- [`../03-security/password-and-mfa-requirements.md`](../03-security/password-and-mfa-requirements.md) — Policy baseline.
- [`../03-security/device-encryption.md`](../03-security/device-encryption.md) — Related device-level control.
- [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md) — Where to record hardware-key requests.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Identity Engineering and Helpdesk contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — MFA, TAP, FIDO2, number-matching definitions.
