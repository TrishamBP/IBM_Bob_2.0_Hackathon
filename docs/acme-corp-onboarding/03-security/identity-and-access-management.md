---
document_id: ACME-SEC-005
title: Identity and Access Management
category: security
department: information-security
applicable_roles: [all]
owner: Abhishek Verma, IAM Engineer
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, iam, entra-id, sso, pim, conditional-access, fictional]
---

# Identity and Access Management

> ACME Corp fictional onboarding library. The Entra ID tenant `acme.onmicrosoft.com`, hostnames `portal.acme.example` and `vault.acme.example`, and the mailbox `security-oncall@acme.example` are fictional. No real tokens, secrets, or live traffic are referenced.

## 1. Purpose

This document describes how ACME Corp manages digital identities — who a user is, what they can access, and for how long. It explains the systems in use (Microsoft Entra ID as the identity provider, Microsoft Intune for device identity, Entra ID PIM for privileged role activation), and the lifecycle of access from joiner to mover to leaver. It is the canonical reference for every other document that mentions "access requests," "conditional access," or "PIM activation."

## 2. Scope

IAM at ACME covers:

- Every ACME workforce identity (employee, contractor, intern).
- Every ACME-issued service account and workload identity.
- Every application that integrates with ACME's identity provider.
- Every ACME system that uses identity-based access control — Microsoft 365, GitHub Enterprise at `git.acme.example` (fictional), internal portals (`portal`, `hr`, `helpdesk`, `wiki`, `vault`, `packages`, `status` — all fictional hostnames).

Physical access (badges) is governed separately by Facilities and is out of scope here.

## 3. Identity Provider

ACME's identity provider (IdP) is **Microsoft Entra ID** (formerly Azure Active Directory). The ACME tenant is `acme.onmicrosoft.com` (fictional). All ACME accounts are created in this tenant. All applications integrate with Entra ID for single sign-on (SSO).

Every workforce member has exactly one Entra ID account:

- Format: `<firstname>.<lastname>@acme.example`.
- Provisioned by IT on the basis of a manager-approved request from `hr.acme.example` (fictional).
- De-provisioned on the last working day per [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md).

There are no per-application accounts — your ACME identity works everywhere ACME operates.

## 4. Single Sign-On (SSO)

All ACME applications use Entra ID-based SSO. Supported protocols:

| Protocol | Used For |
|----------|----------|
| SAML 2.0 | Microsoft 365, Salesforce (CRM), internal portals |
| OpenID Connect (OIDC) | GitHub Enterprise, modern internal apps |
| SCIM 2.0 | Automated user provisioning/de-provisioning (see §6) |
| LDAP | Legacy apps being retired (deprecated) |

Workforce members sign in at `https://myaccount.microsoft.com` (Microsoft-hosted) and are then routed to the appropriate application without re-entering credentials. MFA is enforced on every sign-in per [`password-and-mfa-requirements.md`](password-and-mfa-requirements.md).

## 5. Conditional Access

Conditional access is the policy engine that decides whether a sign-in is allowed. It evaluates:

- **Who** — the user, their group memberships, their role.
- **Where** — trusted locations (office IP ranges, the corporate VPN — see [`../02-it/corporate-vpn-configuration.md`](../02-it/corporate-vpn-configuration.md)).
- **What device** — Intune-enrolled, compliant, encrypted (see [`device-encryption.md`](device-encryption.md)).
- **What app** — the application being accessed and its data classification (see [`data-classification.md`](data-classification.md)).
- **What risk** — Entra ID Identity Protection signals (impossible travel, leaked credentials, anonymous IP, unfamiliar sign-in properties).

Default conditional access policies (cannot be overridden by users):

1. **Block** sign-in from non-compliant devices.
2. **Require MFA** for every interactive sign-in.
3. **Require MFA** for access to Confidential or Restricted SharePoint sites.
4. **Block** legacy authentication (POP, IMAP, SMTP — except for documented service accounts).
5. **Require FIDO2 or push MFA** (no SMS) for privileged role activation.
6. **Block** sign-in from countries outside ACME's allowed list (India, UK, US, plus employee's recorded travel destinations).
7. **Require reauthentication** for high-impact actions (configuring MFA, adding a federated domain, modifying conditional access itself).

Conditional access policies are reviewed quarterly by the IAM Engineer (`Abhishek Verma`) and the Security Director (`Neha Saxena`).

## 6. Provisioning and De-provisioning (SCIM)

ACME uses SCIM 2.0 to automate identity lifecycle:

- **Joiner:** When HR completes onboarding in `hr.acme.example` (fictional), the user is provisioned in Entra ID. SCIM then propagates the user to integrated apps within 30 minutes. The new hire signs in for the first time per [`../02-it/microsoft-365-account-activation.md`](../02-it/microsoft-365-account-activation.md).
- **Mover:** When an employee changes role, HR updates the role in `hr.acme.example`. SCIM adds the user to the new team's groups and removes them from the old team's groups. Stale access is caught by the quarterly access review (see §7).
- **Leaver:** On the last working day, HR marks the employee as separated. SCIM deactivates the Entra ID account within 15 minutes and propagates deactivation to all integrated apps. Manager-approved exceptions for read-only access for handover may extend this by up to 7 days — see [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md).

Emergency de-provisioning (e.g., for a security incident) is performed by the SOC Lead (`Fatima Sheikh`) via the Entra ID admin console and is propagated within seconds. See [`security-incident-reporting.md`](security-incident-reporting.md) for the incident workflow.

## 7. Access Reviews

- **Quarterly:** IAM Engineer (`Abhishek Verma`) runs an Entra ID access review for every privileged role and every Confidential/Restricted resource. Managers attest that each direct report still needs their access.
- **On role change:** Manager requests removal of access no longer needed; IAM Engineer verifies.
- **On termination:** Automatic via SCIM (see §6).
- **On exception expiry:** The exception owner attests that the exception is still required or it lapses.

Failure to complete the quarterly access review within 14 days results in access suspension for the unaudited role — this is enforced, not optional.

## 8. Privileged Identity Management (PIM)

For roles with privileged access (Global Administrator, Security Administrator, Exchange Administrator, GitHub Organization Owner, production cloud subscription Contributor, etc.):

- **No standing access.** The role is "eligible" but not "active."
- **Time-bound activation.** The user activates the role for a specific duration (default 4 hours, max 8 hours) through the Entra ID PIM portal. Activation requires MFA and a justification.
- **Approval workflow.** Most privileged roles require approver sign-off (the approver is the Security Director or CISO). See [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md).
- **Full audit.** Every activation is logged with user, role, justification, start time, end time, and approver.
- **Auto-deactivation.** The role is removed automatically at end of duration.

This implements the principle in [`least-privilege-access.md`](least-privilege-access.md): no standing production access for engineers.

## 9. Service Accounts and Workload Identities

Service accounts follow the rules in [`password-and-mfa-requirements.md`](password-and-mfa-requirements.md) §5:

- Prefer managed identities (Azure Managed Identity, Workload Identity Federation).
- Static secrets are stored in ACME Vault (see [`secrets-management.md`](secrets-management.md)) and rotated per that document.
- Service accounts cannot be used for interactive sign-in — conditional access blocks it.
- Service accounts are scoped to a single workload.

## 10. Responsibilities

| Role | Responsibility |
|------|----------------|
| **IAM Engineer** (`Abhishek Verma`) | Operates Entra ID, conditional access, PIM, SCIM. Runs access reviews. Approves access requests. |
| **Security Director** (`Neha Saxena`) | Approves new application SSO integrations. Reviews conditional access changes. |
| **SOC Lead** (`Fatima Sheikh`) | Monitors identity signals. Performs emergency de-provisioning during incidents. |
| **People Managers** | Approve access requests for their reports. Complete quarterly access review attestation. |
| **Every workforce member** | Activates PIM only for the task at hand. Deactivates when done. Reports unexpected access to `security-oncall@acme.example`. |

## 11. Enforcement

- Conditional access is enforced at the IdP level — there is no client-side bypass.
- PIM is enforced for all roles in the privileged roles group.
- Access reviews are enforced by the quarterly review run; unaudited access is suspended.
- SCIM is enforced through the HR feed; manual account creation outside HR is prohibited.

## 12. Exceptions

Exceptions to conditional access or PIM are rare. To request one, email `security-oncall@acme.example` (fictional). The IAM Engineer reviews, the Security Director (`Neha Saxena`) approves, and a compensating control is documented. The CISO (`Rajan Mehta`) is notified of all exceptions for the risk register.

## 13. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`password-and-mfa-requirements.md`](password-and-mfa-requirements.md) — Authentication factors.
- [`least-privilege-access.md`](least-privilege-access.md) — PIM philosophy and detailed rules.
- [`data-classification.md`](data-classification.md) — Classification drives access decisions.
- [`secrets-management.md`](secrets-management.md) — Service account credentials.
- [`../02-it/microsoft-entra-id-and-sso.md`](../02-it/microsoft-entra-id-and-sso.md) — SSO mechanics for end users.
- [`../02-it/microsoft-365-account-activation.md`](../02-it/microsoft-365-account-activation.md) — First sign-in.
- [`../02-it/corporate-vpn-configuration.md`](../02-it/corporate-vpn-configuration.md) — Trusted locations.
- [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) — Termination workflow.
- [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md) — Access request approval workflow.
- [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md) — Access request form.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — IAM Engineer contact.
- [`../metadata/glossary.md`](../metadata/glossary.md) — IdP, SSO, SCIM, PIM, MFA definitions.
