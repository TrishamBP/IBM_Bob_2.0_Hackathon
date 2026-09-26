---
document_id: ACME-IT-008
title: Microsoft Entra ID and Single Sign-On
category: it
department: it-operations
applicable_roles: [all]
owner: Faisal Ahmed, Identity Engineer
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, entra-id, sso, conditional-access, identity, fictional]
---

# Microsoft Entra ID and Single Sign-On

> ACME Corp fictional onboarding library. The tenant `acme.onmicrosoft.com` is simulated for documentation and training. Microsoft Entra ID (formerly Azure Active Directory) is real Microsoft infrastructure.

## 1. Purpose

Explains Microsoft Entra ID as ACME Corp's identity provider (IdP) and single sign-on (SSO) backbone, walks the new hire through registering security info, signing in via the My Apps portal (`myapps.microsoft.com`), understanding conditional-access prompts, and generating app passwords for legacy clients. This is the conceptual complement to [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md) and [`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md).

## 2. What Is Entra ID at ACME

| Concept | What it means at ACME |
|---------|------------------------|
| **Tenant** | `acme.onmicrosoft.com` — the ACME Corp Entra ID directory. |
| **User principal name (UPN)** | `<firstname>.<lastname>@acme.example` — your sign-in identifier. |
| **Groups** | Used to bundle entitlements: `All-Staff`, `Office-HY`, `MFA-Required`, `Engineers`, etc. |
| **Conditional Access (CA)** | Policies that evaluate each sign-in (location, device compliance, risk) and decide whether to allow, challenge with MFA, or block. |
| **Enterprise Applications** | SaaS apps integrated for SSO (e.g., Jira, Confluence, Salesforce, GitHub Enterprise, Datadog, 1Password Business). |
| **App roles / SCIM** | Auto-provisioning of user accounts in those SaaS apps from the ACME directory. |
| **PIM (Privileged Identity Management)** | Just-In-Time activation of admin roles — engineers may request temporary Global Reader or Network Administrator, for example. |

## 3. Prerequisites

- A provisioned Entra ID account (per [`new-employee-it-request.md`](new-employee-it-request.md)).
- Microsoft 365 activation completed ([`microsoft-365-account-activation.md`](microsoft-365-account-activation.md)).
- Microsoft Authenticator enrolled ([`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md)).
- A corporate-managed, Intune-compliant device (per [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md)) — conditional access uses device compliance as a primary signal.

## 4. The My Apps Portal

1. Navigate to `https://myapps.microsoft.com` (real Microsoft URL; ACME tenant responds).
2. Sign in with `<firstname>.<lastname>@acme.example` and complete MFA.
3. The portal shows the tiles for every enterprise application you have been granted. The default set for a new hire includes:
   - Microsoft 365
   - 1Password Business
   - GitHub Enterprise (for engineering)
   - Jira / Confluence (Atlassian Cloud)
   - ServiceNow-equivalent ITSM portal (`helpdesk.acme.example`)
   - ACME Wiki (`wiki.acme.example`)
4. Click any tile — you will be signed in via SSO (no second sign-in prompt).

## 5. Register Security Info (if Not Done During M365 Activation)

> If you completed the security info registration during [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md), you can skip this section. This is the canonical reference page for the same flow.

1. In the My Apps portal, click your avatar (top-right) → **View account**.
2. Navigate to **Security info**.
3. Ensure at least two methods are registered:
   - **Microsoft Authenticator (push)** — primary.
   - **Phone (SMS)** — fallback.
4. (Recommended for engineers) Add a **FIDO2 security key** — YubiKey 5C NFC is the ACME standard; available on request from the IT depot.

## 6. Conditional Access — What to Expect

ACME applies a baseline set of conditional-access policies. The new hire will see prompts in the following situations:

| Policy | Trigger | What you do |
|--------|---------|-------------|
| **MFA for all sign-ins** | Every sign-in to a new session | Approve the Authenticator push. |
| **Block legacy auth** | Older clients (IMAP, POP, older Office) | These are blocked by default; use modern clients (Outlook desktop, OWA, M365 apps). |
| **Require compliant device** | First-party Microsoft apps | The device must be Intune-compliant; non-compliant devices are blocked from M365 data. |
| **Block high-risk sign-in** | Sign-in from an unusual location, impossible travel, or anonymous IP | The sign-in is blocked; you must use a TAP or contact IT. |
| **Block non-corporate domains for M365 admin** | Attempt to access M365 admin centers from outside the corporate network or VPN | Connect to the corporate VPN first (see [`corporate-vpn-configuration.md`](corporate-vpn-configuration.md)). |
| **Require password reset on user-risk = High** | Entra ID Identity Protection detects a compromised account | You are forced through SSPR (self-service password reset) at next sign-in. |

If you see a CA block message unexpectedly, the message will reference a policy name (e.g., `CA-001-RequireCompliantDevice`). Quote it in your IT ticket.

## 7. App Passwords for Legacy Clients

> App passwords bypass MFA for a specific legacy client. They are issued sparingly and tracked in Entra ID.

1. In the My Account portal (`https://myaccount.microsoft.com`) → **Security info → Add sign-in method → App password**.
2. Name the password after the client (e.g., "SMTP-relay-for-<service>").
3. Entra ID displays a 16-character password once — copy it; you will not see it again.
4. Use it in place of your normal password in the legacy client.
5. App passwords **never expire** unless revoked; rotate them at least annually.

> App passwords are **disabled** by default for non-engineering roles. If your role requires one, request via [`software-access-requests.md`](software-access-requests.md).

## 8. Self-Service Password Reset (SSPR)

1. Navigate to `https://aka.ms/sspr` (real Microsoft URL).
2. Sign in with `<firstname>.<lastname>@acme.example`.
3. You can reset your password using any registered security info method (Authenticator, SMS, or alternate phone).
4. The new password must meet the ACME baseline (see [`../03-security/password-and-mfa-requirements.md`](../03-security/password-and-mfa-requirements.md)).
5. After SSPR, you may need to re-sign-in to all clients (Outlook, Teams, OneDrive, Edge, VPN) — this is expected.

## 9. Managing Devices in Entra ID

1. Navigate to `https://myaccount.microsoft.com → Devices`.
2. You should see your corporate laptop listed as a **Microsoft Entra ID joined / hybrid joined** device.
3. You can also see BitLocker / FileVault recovery keys for each of your devices — this is the canonical place to look if you ever need to unlock the disk.

## 10. Expected Outcomes

After this document:

- The new hire understands Entra ID is the IdP behind every ACME sign-in.
- The My Apps portal is set as a bookmark.
- Security info is registered with at least two methods.
- The new hire knows what a conditional-access prompt means and what to do.
- The new hire knows how to perform SSPR.

## 11. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| "You cannot access this application" when clicking an app tile | Group membership for that app not granted | Raise a P3 ticket via [`software-access-requests.md`](software-access-requests.md). |
| App password not visible as an option | Disabled by policy for your role | Use modern auth; if a legacy client is unavoidable, request an exception. |
| Sign-in blocked with "CA-002-BlockHighRisk" | Identity Protection flagged your sign-in | Use a TAP from IT (`helpdesk@acme.example`) or sign in from a known location / compliant device. |
| My Apps portal shows only M365 | Group sync lag (apps granted but membership not yet propagated) | Wait 30 minutes; force sync via Company Portal; raise P3 if persists. |
| FIDO2 key fails to enroll | Key not yet registered in Entra ID tenant | Contact Identity Engineering (`faisal.ahmed@acme.example`) to register the key's attestation. |
| SSPR fails with "Not enough info" | Only one method registered | Re-open Security info; add a second method. |

## 12. Approval Requirements

- **Standard SSO access to an enterprise app:** granted by group membership per role bundle; no extra approval needed.
- **App password:** IT Manager (`arjun.kapoor@acme.example`) approval for non-engineering roles.
- **Privileged role activation (PIM):** requires a documented change ticket; activation requires MFA + business justification; activations are time-boxed (default 4 hours).
- **FIDO2 key issue:** Endpoint Engineering (`suresh.babu@acme.example`) issues the key; Identity Engineering (`faisal.ahmed@acme.example`) registers it.

## 13. Related Documents

- [`new-employee-it-request.md`](new-employee-it-request.md) — Account creation.
- [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md) — First sign-in / password set.
- [`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md) — MFA enrollment.
- [`corporate-vpn-configuration.md`](corporate-vpn-configuration.md) — Required for some CA policies.
- [`software-access-requests.md`](software-access-requests.md) — How to get an app tile.
- [`password-manager-configuration.md`](password-manager-configuration.md) — 1Password SSO context.
- [`../03-security/password-and-mfa-requirements.md`](../03-security/password-and-mfa-requirements.md) — Password baseline.
- [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md) — CA / risk policy.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Identity Engineering contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — IdP, SSO, CA, PIM, FIDO2, SCIM definitions.
