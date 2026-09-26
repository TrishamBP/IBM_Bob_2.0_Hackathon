---
document_id: ACME-IT-012
title: Password Manager Configuration
category: it
department: it-operations
applicable_roles: [all]
owner: Faisal Ahmed, Identity Engineer
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, password-manager, 1password, sso, vaults, fictional]
---

# Password Manager Configuration

> ACME Corp fictional onboarding library. ACME uses **1Password Business** (a real product; the ACME tenant configuration below is fictional and simulated). The SSO endpoint `acme.1password.com` is illustrative.

## 1. Purpose

Walks the new hire through installing the 1Password desktop app and browser extension, signing in with the corporate SSO identity, joining the standard shared vaults, generating and storing the **Emergency Kit**, and recovering access in case of device loss. The corporate password manager is the **single source of truth** for shared secrets at ACME — no shared secrets should be in chat, email, or spreadsheets.

## 2. Prerequisites

- An activated Entra ID identity (per [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md)).
- Microsoft Authenticator enrolled (per [`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md)).
- A corporate-managed, Intune-compliant device.
- A printed or saved location for the Emergency Kit (e.g., a personal safe or a trusted family member).

## 3. Step 1 — Install the 1Password Desktop App

> On managed corporate devices, 1Password is pre-installed via Intune. The steps below are for verification or for reinstall.

1. On the corporate device, verify **1Password** is in your Start menu / Launchpad. If not:
   - Download from `https://packages.acme.example/1password/` (simulated internal mirror) for the managed installer; or
   - Use `https://1password.com/downloads/` (real) for personal-device BYOD install (requires BYOD exception — see [`../03-security/byod-policy.md`](../03-security/byod-policy.md)).
2. Install with default options. On managed devices, no admin prompt appears.
3. Launch 1Password.

## 4. Step 2 — Install the Browser Extension

1. Open Microsoft Edge for Business (default browser on ACME devices).
2. Open the **Edge Add-ons** store and search for "1Password".
3. Install the official **1Password Edge extension** (publisher: AgileBits).
4. Click the 1Password icon in the toolbar → **Sign In**.
5. Select **"Sign in with SSO"** (this is the ACME-integrated path).
6. The browser opens a sign-in page at `https://acme.1password.com` (simulated).
7. Sign in with `<firstname>.<lastname>@acme.example`; complete the MFA push.
8. The extension confirms: "Connected to ACME Corp."
9. Repeat for Chrome / Firefox if you use them as secondary browsers.

## 5. Step 3 — Generate Your Emergency Kit

> The Emergency Kit is a one-page PDF with your account details, secret key, and a place for your master password. Without it, recovery is significantly harder — store it safely.

1. After SSO sign-in, the 1Password desktop app shows a banner: "Download your Emergency Kit."
2. Click **Download**. The PDF saves to your Downloads folder.
3. Open the PDF. It contains:
   - **Account URL:** `acme.1password.com` (simulated).
   - **Email:** `<firstname>.<lastname>@acme.example`.
   - **Secret Key:** a 34-character alphanumeric string (e.g., `A3-XXXXXX-XXXXXX-XXXXXX-XXXXXX-XXXXXX-XXXXXX` — simulated; treat your real one as confidential).
   - A blank line for your **Master Password** (do **not** write it on the PDF — see §6).
4. Store the PDF:
   - In your **Personal vault** in 1Password itself (auto-stored).
   - On a USB drive in a personal safe or safety deposit box.
   - With a trusted family member in a sealed envelope.
5. Do **not** email the Emergency Kit. Do **not** upload it to a personal cloud drive (Google Drive, Dropbox, iCloud).

## 6. Step 4 — Set Your Master Password

> The master password is the only password that 1Password cannot reset for you. ACME enforces a master-password baseline aligned with [`../03-security/password-and-mfa-requirements.md`](../03-security/password-and-mfa-requirements.md).

1. On first launch after SSO sign-in, the app prompts: "Set your Master Password."
2. Choose a master password that:
   - Is **35+ characters** long.
   - Is a **passphrase** (4–6 random words plus digits / symbols).
   - Is **not** a password you have ever used elsewhere.
   - Is **memorable** to you — write down only a hint, not the password itself.
3. Confirm the password.
4. **Write a non-revealing hint** in the hint field (e.g., "first concert + middle-school teacher"). Do **not** write the password itself.
5. Save. The vault encrypts with the master password + secret key.

## 7. Step 5 — Join the Standard Shared Vaults

You are auto-added to the following vaults based on your role bundle:

| Vault | Purpose | Access |
|-------|---------|--------|
| `Shared-ACME-Corporate` | Company-wide shared secrets (e.g., demo license keys, sandbox accounts) | Read |
| `Shared-<BU>` (e.g., `Shared-Cloud-Engineering`) | BU-level secrets (e.g., staging API keys, shared service accounts) | Read |
| `<Your-Team>` (e.g., `Shared-Cloud-Platform`) | Team-level production secrets | Read / Write |
| `Personal` | Your personal vault (private to you) | Read / Write |

To verify:

1. Open the 1Password app → left rail → **Vaults**.
2. Confirm the list matches the table above.
3. If a vault is missing, raise a P3 ticket per [`software-access-requests.md`](software-access-requests.md) — group-membership sync lag.

## 8. Step 6 — Generate and Use a Password

1. In a browser, navigate to a sign-up form (e.g., a SaaS service you are provisioning for ACME).
2. Click the 1Password icon in the form's password field → **Generate Password**.
3. Choose the recipe:
   - **Length:** 32 characters (default).
   - **Character set:** upper + lower + digits + symbols.
4. Click **Fill** — the new password is inserted in the form and saved to your `Personal` vault (or the appropriate shared vault if you select one).
5. **Always** file shared corporate credentials in the correct shared vault, not in your Personal vault.

## 9. Step 7 — Recovery If You Forget Your Master Password

> ACME's 1Password Business plan includes **Account Recovery** — IT can re-onboard your account without your master password, after verifying your identity.

1. Contact the IT Helpdesk (`helpdesk@acme.example` or +91-40-0000-0000).
2. The Helpdesk verifies identity (video call with the user's manager or HRBP).
3. The Helpdesk triggers **Account Recovery** from the 1Password admin console.
4. You receive an email at `<firstname>.<lastname>@acme.example` with a recovery link.
5. Open the link from your corporate device, complete MFA, and set a new master password.
6. Re-download your Emergency Kit (the Secret Key changes after recovery).

> If you lose your device entirely (with no access to your master password and no Emergency Kit), recovery takes 24–48 hours because IT must escalate to the Identity Engineering team for additional verification.

## 10. Expected Outcomes

After this document:

- 1Password desktop app + browser extension are installed and signed in via SSO.
- The Emergency Kit PDF is stored safely (personal safe / family member).
- The master password meets the ACME baseline and is memorable to the user alone.
- The user is a member of the standard shared vaults.
- The user can generate and store passwords in the correct vault.

## 11. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| SSO sign-in fails with "Not in this account" | 1Password Business account not yet provisioned | Wait 30 minutes after M365 activation; if persists, contact `faisal.ahmed@acme.example`. |
| Browser extension shows "Locked" constantly | Master password not entered recently | Unlock with master password; enable "Keep 1Password unlocked for X hours" (max 8 hours). |
| Cannot see the BU shared vault | Group membership sync lag | Wait 30 minutes; force-sync via Company Portal; raise P3 if persists. |
| Secret Key appears as `XXXX` (masked) | Account Recovery mode active | Complete the recovery flow; re-download the Emergency Kit. |
| "Permission denied" when writing to a shared vault | Read-only access on that vault | File a request via [`software-access-requests.md`](software-access-requests.md) for write access; vault owner approves. |
| New password does not save to the form | Extension not detecting the right field | Right-click the field → 1Password → Save Login; or use the desktop app's "Save new item" then fill. |
| Traveling with sensitive vault access | Border-search risk | Activate "Travel Mode" from the admin console before travel; sensitive vaults are removed from the device until you disable Travel Mode. |

## 12. Approval Requirements

- **Standard 1Password Business access:** no extra approval — included in role bundle.
- **Write access to a shared vault:** vault owner (typically a staff-plus engineer or the team lead) approves via [`software-access-requests.md`](software-access-requests.md).
- **Provisioning a new shared vault:** IT Manager (`arjun.kapoor@acme.example`) + the data owner; vault is created with an explicit review date.
- **Account Recovery:** IT Helpdesk with manager / HRBP identity verification.
- **Travel Mode activation:** user-initiated; no approval, but must be enabled before travel and disabled within 24 hours of return.

## 13. Related Documents

- [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md) — Preceding step.
- [`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md) — MFA for SSO sign-in.
- [`microsoft-entra-id-and-sso.md`](microsoft-entra-id-and-sso.md) — SSO context.
- [`software-access-requests.md`](software-access-requests.md) — Vault write access.
- [`../03-security/password-and-mfa-requirements.md`](../03-security/password-and-mfa-requirements.md) — Password baseline.
- [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md) — Secrets-handling policy.
- [`../03-security/byod-policy.md`](../03-security/byod-policy.md) — 1Password on personal devices.
- [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md) — Vault creation request.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Identity Engineering / Helpdesk contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — SSO, SAML, vault, Emergency Kit definitions.
