---
document_id: ACME-IT-005
title: Microsoft 365 Account Activation
category: it
department: it-operations
applicable_roles: [all]
owner: Faisal Ahmed, Identity Engineer
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, m365, activation, entra-id, onedrive, sharepoint, fictional]
---

# Microsoft 365 Account Activation

> ACME Corp fictional onboarding library. The portal `https://portal.office.com` is real Microsoft infrastructure, but every ACME-specific identifier below (tenant `acme.onmicrosoft.com`, UPN, group names) is fictional and simulated.

## 1. Purpose

Walks the new hire through the **first sign-in** to the Microsoft 365 portal, setting a permanent password, registering security info (MFA), activating the M365 desktop apps, and performing the SharePoint / OneDrive first-run experience. This is the identity anchor for every subsequent service.

## 2. Prerequisites

- The new hire has completed [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md) through first-time sign-in.
- The new hire has Microsoft Authenticator installed and enrolled per [`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md).
- The new hire has the temporary password delivered by IT (placeholder: `<temp-pass-from-helpdesk>`).
- The new hire's personal phone (for MFA) and a recovery phone number (for fallback) are accessible.

## 3. Step 1 — First Sign-In to the M365 Portal

1. Open a browser (Edge for Business is recommended; Chrome / Firefox / Safari are also supported).
2. Navigate to `https://portal.office.com` (the real Microsoft 365 portal). The simulated ACME tenant will respond at `acme.onmicrosoft.com`.
3. Enter your corporate user principal name: `<firstname>.<lastname>@acme.example`.
4. Enter the temporary password (`<temp-pass-from-helpdesk>`).
5. You will be prompted to **change the temporary password**. Choose a permanent password that meets the ACME baseline:
   - Minimum 16 characters.
   - At least one uppercase, one lowercase, one digit, one symbol.
   - Not a dictionary word; not derived from your name or date of birth.
   - Not a previously used password (Entra ID Password Protection enforces this against your last 10 passwords).
6. The portal loads. A welcome banner displays the ACME logo and the headline: "Welcome to ACME Corp M365."

## 4. Step 2 — Register Security Info

> Do not skip this step. Without registered security info, you will be locked out the next time you sign in from a new device or after 14 days.

1. In the M365 portal, click your avatar (top-right) → **View account → Security info → Add sign-in method**.
2. Select **Microsoft Authenticator (notification)** as the primary method. Approve the push notification on your phone to complete the binding.
3. Add a secondary method — **Phone (SMS)** — using your personal mobile number. This is the fallback if the Authenticator app is unavailable.
4. (Optional but recommended for engineers and any role with privileged access) Add a **FIDO2 security key** as a phishing-resistant second factor. See [`../03-security/password-and-mfa-requirements.md`](../03-security/password-and-mfa-requirements.md).
5. Verify each method by completing the test challenge Entra ID sends you.
6. Save. The portal should now show at least two methods under **Security info**.

## 5. Step 3 — Activate Microsoft 365 Apps

1. On the M365 portal home page, click **Install apps** (top-right).
2. The page shows the ACME-provisioned apps (M365 Apps for Enterprise — Word, Excel, PowerPoint, Outlook, Teams, OneDrive).
3. If you completed [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md), these apps are already installed via Intune — you only need to **activate** them:
   - Open any one of them (e.g., Word).
   - Click **Sign in** on the activation banner.
   - Enter `<firstname>.<lastname>@acme.example` and complete the MFA challenge.
   - The app confirms: "You're licensed through ACME Corp."
4. Repeat for Outlook, Excel, PowerPoint if they were not auto-activated.
5. (Optional) If you prefer to install the apps manually on a personal device for BYOD use, you can download the installer from the same page — but BYOD install requires the BYOD exception approval (see [`../03-security/byod-policy.md`](../03-security/byod-policy.md)).

## 6. Step 4 — SharePoint First-Run

1. From the M365 portal, click **SharePoint** in the app launcher (top-left waffle).
2. The first-run experience runs automatically:
   - You are auto-added to the **ACME All-Staff** SharePoint site.
   - You are auto-added to your business unit's site (e.g., **ACME Cloud Engineering**).
   - You are auto-added to your manager's team site.
3. When prompted, click **Stay signed in** to reduce re-auth prompts (this is fine on a managed corporate device; do not do this on shared/public machines).
4. Confirm by navigating to **Sites → Followed**. You should see at least three sites.

## 7. Step 5 — OneDrive First-Run

1. From the M365 portal, click **OneDrive**.
2. The first-run wizard sets up your cloud storage:
   - Confirms your 5 TB quota (the ACME baseline).
   - Asks whether to **sync** your OneDrive to the local device. Click **Sync** and the OneDrive sync client will activate.
   - Creates your "Files" root folder on the local device (Windows: `C:\Users\<you>\OneDrive - ACME Corp`; macOS: `/Users/<you>/OneDrive - ACME Corp`).
3. Test by dragging a small file into the OneDrive folder and verifying it uploads to the cloud version at `https://acme-my.sharepoint.com/personal/<firstname>_<lastname>_acme_example/`.

## 8. Step 6 — Set the Default "Files On-Demand" Behavior

1. In the OneDrive sync client (icon in the system tray / menu bar), click the gear → **Settings**.
2. Under **Files On-Demand**, confirm **"Save space and download files as you use them"** is enabled. This is the ACME baseline; it prevents confidential corporate data from being cached on local disk unnecessarily.
3. Under **Backup**, **do not** enable PC folder backup (this would mix personal folders with corporate storage). ACME's Intune policy disables this anyway, but the toggle may appear briefly.

## 9. Expected Outcomes

After activation:

- The new hire can sign in to `https://portal.office.com` using only the permanent password + MFA (no temporary password).
- At least two security info methods are registered.
- M365 apps (Word, Excel, PowerPoint, Outlook, Teams, OneDrive) are activated under the ACME license.
- OneDrive is syncing and the local OneDrive folder is created.
- SharePoint shows the ACME All-Staff site and the BU site as "Followed."

## 10. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| "Your account is disabled" on first sign-in | Entra ID account not yet activated; HRIS webhook lag | Wait 30 minutes; if persists, contact `faisal.ahmed@acme.example`. |
| MFA push never arrives during security info registration | Phone offline / Authenticator not enrolled | Use SMS fallback; or request a TAP from `helpdesk@acme.example`. |
| OneDrive sync client shows "Not signed in" | Intune policy sync lag | Open the client manually and sign in with `<firstname>.<lastname>@acme.example`. |
| "Your quota is 5 GB" instead of 5 TB | License not yet assigned | Identity Engineering will assign within 1 business day; raise a P3 ticket if it persists after 24 hours. |
| SharePoint does not show the BU site | Group membership sync lag | Wait 60 minutes; force a sync via the Company Portal; raise a P3 ticket if still missing. |
| Office activation banner keeps reappearing | Shared computer / licensing token expired | Re-sign-in; if persists, run `dsregcmd /status` (Windows) and confirm the device is Entra-joined. |

## 11. Approval Requirements

- **None for the standard flow.**
- **Quota increase above 5 TB** (e.g., for video / ML datasets): approved by IT Manager (`arjun.kapoor@acme.example`).
- **External sharing enabled** on a SharePoint site: approved by the site owner and validated against [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md).

## 12. Related Documents

- [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md) — Preceding step.
- [`microsoft-entra-id-and-sso.md`](microsoft-entra-id-and-sso.md) — IdP / SSO context.
- [`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md) — MFA enrollment.
- [`microsoft-teams-setup.md`](microsoft-teams-setup.md) — Teams next.
- [`outlook-and-company-calendar-setup.md`](outlook-and-company-calendar-setup.md) — Outlook next.
- [`../03-security/password-and-mfa-requirements.md`](../03-security/password-and-mfa-requirements.md) — Password baseline.
- [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md) — Acceptable use.
- [`../03-security/byod-policy.md`](../03-security/byod-policy.md) — Personal device install.
- [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md) — Request form.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Identity / IT Onboarding contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — TAP, FIDO2, conditional access definitions.
