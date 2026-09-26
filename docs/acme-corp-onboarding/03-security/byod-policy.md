---
document_id: ACME-SEC-011
title: BYOD (Bring Your Own Device) Policy
category: security
department: information-security
applicable_roles: [all]
owner: Abhishek Verma, IAM Engineer
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, byod, mobile, intune, mam, fictional]
---

# BYOD (Bring Your Own Device) Policy

> ACME Corp fictional onboarding library. Hostnames (`portal.acme.example`, `vault.acme.example`) and mailboxes are fictional. Microsoft Intune and Microsoft Authenticator are real Microsoft products; the ACME deployment is simulated.

## 1. Purpose

This document defines the rules for using a personal device — typically a personal smartphone, but in limited cases a personal laptop — for ACME Corp work. ACME prefers corporate-issued devices for any work that touches Confidential, Restricted, or Customer Data. BYOD is permitted for limited scenarios where the data stays in the ACME-managed app container, and the personal device is never enrolled into full Mobile Device Management (MDM).

## 2. Scope

This applies to:

- All ACME workforce members who use a personal device for ACME work.
- All personal iOS (iOS 16+) and Android (Android 10+) smartphones used to receive MFA pushes, access Outlook mobile, or use Microsoft Teams mobile.
- Personal laptops — **only** permitted with explicit approval per §4 and never for Confidential, Restricted, or Customer Data work.

ACME-issued laptops and ACME-issued mobile devices are governed by [`../02-it/laptop-and-workstation-allocation.md`](../02-it/laptop-and-workstation-allocation.md) and [`../02-it/device-acceptance-and-responsibility.md`](../02-it/device-acceptance-and-responsibility.md), not by this policy.

## 3. BYOD Tiers and What Is Permitted

| Use Case | Permitted on BYOD? | Mechanism |
|----------|-------------------|-----------|
| Receive MFA push | Yes (encouraged) | Microsoft Authenticator app — no MDM enrollment of the personal phone. See [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md). |
| Outlook mobile (email + calendar) | Yes | Intune MAM (App Protection Policy) — corporate account enrolled, no full MDM. |
| Microsoft Teams mobile (chat + calls) | Yes | Intune MAM. |
| OneDrive mobile / SharePoint mobile | Yes | Intune MAM; data is containerized. |
| Browse `portal.acme.example`, `wiki.acme.example` | Yes | Browser-based; Entra ID SSO with conditional access. |
| View Confidential documents | Yes, via the managed app container | Intune MAM prevents copy-paste out / save-to-personal. |
| **View Restricted documents** | **No** | Must use a corporate-issued, Intune-enrolled device. |
| **View Customer Data** | **No** | Must use a corporate-issued, Intune-enrolled device with encryption. See [`customer-data-handling.md`](customer-data-handling.md). |
| **Develop or test code from `git.acme.example`** | **No** | Must use a corporate-issued developer workstation. See [`source-code-security.md`](source-code-security.md). |
| **Use a personal laptop for ACME work** | **No by default; exception only** | See §4. |

## 4. Personal Laptops — Exception Only

Personal laptops are **not** permitted for ACME work by default. The risk profile is materially higher than a personal phone:

- Personal laptops store data locally (browser cache, downloads folder, IDE workspace).
- Personal laptops are not patched, encrypted, or backed up to ACME standards.
- Personal laptops are more likely to be shared with family.

A workforce member may request an exception only in narrow cases (e.g., a remote contractor waiting for a corporate laptop to be shipped). Exception process:

1. Manager approval.
2. Email `security-oncall@acme.example` (fictional) with the business case and duration.
3. IAM Engineer (`Abhishek Verma`) approves with a compensating control — typically, conditional access restricting the personal laptop to web-only access of approved apps, no local data, and time-bound to ≤ 14 days.
4. The exception is logged in the risk register by the GRC Analyst (`Karthik Subramanian`).

No exception allows Confidential, Restricted, or Customer Data on a personal laptop.

## 5. Mobile Application Management (MAM) Containerization

For personal phones used for Outlook, Teams, OneDrive, or SharePoint mobile, ACME uses Microsoft Intune **App Protection Policies (MAM)** — not full MDM enrollment. This means:

- ACME does **not** manage the personal phone.
- ACME does **not** see the personal phone's location, photos, personal apps, or personal messages.
- ACME does **not** enforce a passcode on the personal phone (Authenticator requires biometrics for push approval, but that's a Microsoft Authenticator app rule, not an Intune rule).
- The corporate account enrolled in Outlook/Teams/OneDrive mobile is **containerized** — corporate data is encrypted in an app-local sandbox separate from personal data.
- The MAM policy enforces: no copy-paste of corporate data into personal apps, no "save to personal cloud," no screen capture of corporate content (where the OS supports it), and require biometric or PIN to open the corporate app.
- On separation, ACME can issue a **selective wipe** that removes only the corporate container — leaving personal data, photos, and apps untouched. See [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md).

## 6. Responsibilities of BYOD Users

A workforce member using a personal phone for ACME work agrees to:

1. Keep the operating system up to date (install OS updates within 30 days of release).
2. Enable biometric unlock (Face ID / Touch ID / fingerprint) on the phone — required by Authenticator.
3. Enable a phone-level screen lock.
4. Not root (Android) or jailbreak (iOS) the phone. A rooted or jailbroken phone is blocked by Intune MAM from accessing corporate data.
5. Not share the phone with family members in a way that allows them to see Outlook or Teams notifications.
6. Report a lost or stolen phone within 1 hour to `security-incident@acme.example` (fictional) — see [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md).
7. Approve MFA pushes only for sign-ins they initiated (see [`phishing-awareness.md`](phishing-awareness.md)).
8. Allow the selective wipe if they leave ACME or if the phone is compromised.

## 7. Selective Wipe

If a workforce member leaves ACME, the corporate container on their personal phone is selectively wiped:

- Outlook corporate account is removed; corporate emails and calendar entries are deleted.
- Teams corporate account is removed; corporate chat history is deleted.
- OneDrive corporate files are removed; personal files are untouched.
- Authenticator corporate account is removed; personal accounts (e.g., personal Microsoft account) are untouched.

The selective wipe does **not** affect the personal phone's photos, personal apps, personal messages, or personal accounts. The workforce member should review and accept this before enrolling the corporate account.

## 8. Lost or Stolen BYOD Phone

If a personal phone used for ACME work is lost or stolen:

1. Report immediately to `security-incident@acme.example` (fictional) and follow [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md).
2. The IAM Engineer (`Abhishek Verma`) issues a remote selective wipe from Intune, removes the corporate account from the phone, and revokes the user's refresh tokens.
3. The IAM Engineer resets the user's password and re-enrolls MFA on a new device.
4. The SOC (`Fatima Sheikh`) reviews sign-in logs for the period the phone was potentially in unauthorized hands.

## 9. BYOD and External AI Tools

Personal phones are not exempt from [`ai-tool-acceptable-use.md`](ai-tool-acceptable-use.md). Customer data, source code, secrets, and Restricted information must not be entered into external AI tools — even from a personal phone, even on personal cellular data, even "just to try it."

## 10. Responsibilities

| Role | Responsibility |
|------|----------------|
| **IAM Engineer** (`Abhishek Verma`) | Configures Intune MAM policies. Issues selective wipes. Reviews exception requests. |
| **Security Director** (`Neha Saxena`) | Approves new app onboarding for MAM. |
| **SOC Lead** (`Fatima Sheikh`) | Reviews lost-phone incidents. Monitors MAM non-compliance. |
| **Every BYOD user** | Keeps OS updated. Reports loss immediately. Approves MFA pushes only for sign-ins they initiated. |

## 11. Enforcement

- Intune MAM policies are enforced by Microsoft — non-compliant phones (jailbroken, rooted, outdated OS) cannot open corporate apps.
- Conditional access in Entra ID blocks non-compliant devices from SSO — see [`identity-and-access-management.md`](identity-and-access-management.md).
- DLP prevents copy-paste of corporate data into personal apps.
- A user who repeatedly refuses to update their personal phone's OS will have the corporate account removed from the phone until they update.

## 12. Exceptions

Exceptions to this policy (e.g., a personal tablet used for a specific accessibility need) require IAM Engineer approval and a documented compensating control. Email `security-oncall@acme.example` (fictional).

## 13. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`acceptable-use-policy.md`](acceptable-use-policy.md) — What you may and may not do.
- [`device-encryption.md`](device-encryption.md) — Encryption requirement for corporate devices (not BYOD).
- [`password-and-mfa-requirements.md`](password-and-mfa-requirements.md) — MFA on a personal phone.
- [`data-classification.md`](data-classification.md) — Drives what data is allowed on BYOD.
- [`customer-data-handling.md`](customer-data-handling.md) — Customer data is never on BYOD.
- [`ai-tool-acceptable-use.md`](ai-tool-acceptable-use.md) — AI tool rules apply on BYOD.
- [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md) — MFA enrollment on personal phone.
- [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md) — Lost personal phone workflow.
- [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) — Selective wipe on separation.
- [`../02-it/laptop-and-workstation-allocation.md`](../02-it/laptop-and-workstation-allocation.md) — Preferred corporate-issued device path.
- [`../01-hr/remote-and-hybrid-working-policy.md`](../01-hr/remote-and-hybrid-working-policy.md) — Remote work context for BYOD.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — IAM Engineer and SOC contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — BYOD, MDM, MAM, MFA definitions.
