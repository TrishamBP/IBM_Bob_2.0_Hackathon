---
document_id: ACME-SEC-004
title: Password and MFA Requirements
category: security
department: information-security
applicable_roles: [all]
owner: Abhishek Verma, IAM Engineer
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, passwords, mfa, authentication, fictional]
---

# Password and MFA Requirements

> ACME Corp fictional onboarding library. ACME's tenant `acme.onmicrosoft.com` and mailbox `security-oncall@acme.example` are fictional and used for illustration only. No real credentials are shown.

## 1. Purpose

This document sets the minimum authentication requirements for every ACME Corp account. Authentication is the most-attacked control surface at ACME — over 90% of the incidents the SOC triages in a typical quarter begin with a credential. The rules below are mandatory, are enforced technically where possible, and apply to every workforce member without exception. If you have a question about an ACME account, the answer is in this document or in the linked IAM docs.

## 2. Scope

This applies to:

- Every ACME account — Microsoft 365 / Entra ID, GitHub Enterprise, internal portals (`portal.acme.example`, `hr.acme.example`, `helpdesk.acme.example`, `wiki.acme.example`, `vault.acme.example`, `packages.acme.example`, `status.acme.example`).
- Every ACME-issued service account and machine identity.
- Every shared mailbox, distribution list, and team account.
- Personal accounts used to receive ACME MFA pushes (your phone, your YubiKey).

## 3. Password Requirements

| Requirement | Standard |
|-------------|----------|
| Minimum length | **14 characters**. 16+ encouraged. |
| Complexity | At least three of: uppercase, lowercase, digit, symbol. Passphrases (e.g., `correct-horse-battery-staple-42`) are encouraged and are stronger than short complex passwords. |
| Uniqueness | **Never reuse** an ACME password on any non-ACME site, and never reuse any password you have ever used elsewhere. |
| Storage | Store every corporate password in the ACME 1Password Business vault (see [`../02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md)). |
| Sharing | Never share your password with anyone — including IT, the SOC, or the CISO. ACME will never ask you for your password. |
| Expiry | Passwords do **not** expire on a fixed rotation. They are rotated on suspected compromise, on role change, or after a confirmed phishing click. |
| Banned passwords | The Entra ID banned-password list blocks common, leaked, and ACME-specific words (e.g., `Acme`, `Hyderabad`, `Corp2025`). |
| Breach check | Entra ID continuously checks password hashes against the Have-I-Been-Pwned breach corpus. A password found in a known breach is rejected at set-time. |

## 4. Multi-Factor Authentication (MFA)

MFA is **mandatory** for every ACME sign-in. There is no role, no office, and no exception.

| Factor | Type | Use Case |
|--------|------|----------|
| Microsoft Authenticator push (number-matching) | Something you have | Default primary factor. See [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md). |
| FIDO2 hardware key (YubiKey 5C NFC) | Something you have | Recommended for engineers, anyone with privileged access, and frequent travelers. |
| SMS code | Something you have | Fallback only — weaker than push; do not rely on it as primary. |
| Voice call | Something you have | Last-resort fallback for account recovery. |
| Password | Something you know | The base factor — never sufficient alone. |

### 4.1 MFA Requirements

- **Primary:** Microsoft Authenticator push with number-matching and biometric unlock on your personal phone.
- **Fallback:** At least one of SMS or alternate-phone voice.
- **Optional but recommended:** FIDO2 YubiKey for privileged users.
- **MFA fatigue protection:** Number-matching is mandatory. Report any unexpected push to `security-incident@acme.example` (fictional) — never approve it.
- **Phishing-resistant:** For roles with privileged access, FIDO2 is required (see [`least-privilege-access.md`](least-privilege-access.md)).

### 4.2 Conditional Access

Entra ID conditional access (see [`identity-and-access-management.md`](identity-and-access-management.md)) enforces MFA on:

- Every interactive sign-in to Microsoft 365.
- Sign-ins from outside trusted locations (office IP ranges and the corporate VPN — see [`../02-it/corporate-vpn-configuration.md`](../02-it/corporate-vpn-configuration.md)).
- Sign-ins from non-compliant devices (not Intune-enrolled, not encrypted — see [`device-encryption.md`](device-encryption.md)).
- Access to Confidential or Restricted SharePoint sites.
- Privileged role activation through Entra ID PIM.

## 5. Service Accounts and Non-Human Identities

Service accounts, machine identities, and CI runners must:

- Use managed identities (Azure Managed Identity, Workload Identity Federation) wherever possible — no static secrets.
- Where a static secret is unavoidable, store it in ACME Vault (see [`secrets-management.md`](secrets-management.md)).
- Be scoped to a single workload — no shared service accounts across systems.
- Be rotated at least every 90 days (see [`secrets-management.md`](secrets-management.md) for rotation cadence by type).

There are **no shared human accounts** at ACME. If you believe you need one, request an exception from `security-oncall@acme.example` (fictional) — the answer will almost certainly be "use a service account with managed identity instead."

## 6. Account Recovery

If you lose access to your MFA factor:

1. **Phone lost with backup:** Restore on a new phone using the Authenticator recovery code (stored in 1Password) — see [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md).
2. **Phone lost without backup:** Use SMS or alternate-phone fallback.
3. **All factors lost:** Call the IT Helpdesk (`helpdesk.acme.example`, fictional). Identity Engineering will issue a Temporary Access Pass (TAP) after manager verification and a 15-minute cool-down for risk review.
4. **Suspected compromise:** Report immediately to `security-incident@acme.example` (fictional). Identity Engineering will reset the password, revoke all sessions, and require re-enrollment of MFA.

Account recovery is itself a high-risk moment — the SOC monitors every TAP issuance as a Tier-2 signal.

## 7. Responsibilities

| Role | Responsibility |
|------|----------------|
| **IAM Engineer** (`Abhishek Verma`) | Configures Entra ID password and MFA policy. Maintains the banned-password list. Reviews conditional access. |
| **SOC Lead** (`Fatima Sheikh`) | Monitors MFA-failure, impossible-travel, and TAP-issuance signals. |
| **People Managers** | Ensure reports complete MFA enrollment before access provisioning. |
| **Every workforce member** | Chooses a strong unique password. Stores it in 1Password. Never shares it. Approves pushes only for sign-ins they initiated. |

## 8. Enforcement

- Entra ID enforces password complexity and the banned list at set-time.
- Conditional access blocks sign-in without MFA. There is no override button a user can press.
- Intune device compliance (see [`../02-it/windows-11-and-macos-workstation-setup.md`](../02-it/windows-11-and-macos-workstation-setup.md)) blocks non-compliant devices.
- Failure to enroll MFA within 3 business days of identity provisioning results in account suspension by Identity Engineering.

## 9. Exceptions

Exceptions are rare and time-bound. To request one — for example, an automated system that cannot do push MFA — email `security-oncall@acme.example` (fictional). The IAM Engineer (`Abhishek Verma`) reviews, the CISO (`Rajan Mehta`) approves, and a compensating control is documented.

## 10. Prohibited Practices

The following are violations of this policy and may result in disciplinary action:

- Approving an MFA push you did not initiate.
- Sharing your password, even with IT.
- Storing passwords in plaintext files, browser autofill (outside 1Password's browser extension), or unencrypted notes.
- Using an ACME password on a non-ACME site.
- Disabling MFA, even temporarily, on your own account.
- Letting another person use your account, even to "just print something."
- Storing the Authenticator recovery code anywhere except the 1Password Business vault.

## 11. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`identity-and-access-management.md`](identity-and-access-management.md) — Entra ID, SSO, conditional access, PIM.
- [`least-privilege-access.md`](least-privilege-access.md) — FIDO2 requirements for privileged roles.
- [`secrets-management.md`](secrets-management.md) — Service account and machine-credential rotation.
- [`phishing-awareness.md`](phishing-awareness.md) — How credential theft happens.
- [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md) — Step-by-step MFA enrollment.
- [`../02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md) — 1Password setup.
- [`../02-it/microsoft-entra-id-and-sso.md`](../02-it/microsoft-entra-id-and-sso.md) — Entra ID and SSO mechanics.
- [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md) — If your phone or YubiKey is lost.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — IAM Engineer and Helpdesk contacts.
