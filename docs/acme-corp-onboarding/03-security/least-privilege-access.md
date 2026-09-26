---
document_id: ACME-SEC-006
title: Least Privilege Access
category: security
department: information-security
applicable_roles: [all]
owner: Abhishek Verma, IAM Engineer
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, least-privilege, pim, jit, default-deny, fictional]
---

# Least Privilege Access

> ACME Corp fictional onboarding library. The Entra ID tenant `acme.onmicrosoft.com`, hostnames `vault.acme.example` and `git.acme.example`, and mailbox `security-oncall@acme.example` are fictional. No real credentials or live access tokens are shown.

## 1. Purpose

This document codifies the principle of least privilege at ACME Corp. Least privilege means: every user, service, and system has the minimum access required to do its job — and no more. It is the operational expression of the Confidentiality principle in [`information-security-policy.md`](information-security-policy.md). Without least privilege, a single compromised account becomes a full breach. With it, an attacker must chain many compromises to reach anything valuable.

## 2. Scope

This applies to:

- Every ACME workforce identity.
- Every service account and workload identity.
- Every privileged role in Entra ID, GitHub Enterprise, the three ACME product environments (ACME Cloud, ACME Intelligence, ACME Workspace), and the underlying cloud subscriptions (Azure, AWS, GCP).
- Every Confidential and Restricted data store listed in [`data-classification.md`](data-classification.md).

## 3. Core Principle — Default Deny

The default state of every ACME resource is **denied**. Access must be explicitly requested, justified, approved, and time-bound. Specifically:

- A new hire joins with only the baseline access defined in [`../02-it/new-employee-it-request.md`](../02-it/new-employee-it-request.md).
- Access to Confidential or Restricted data requires a separate request per data set.
- Access to production environments requires activation through PIM (see §5).
- Access to ACME Vault (secrets) requires a per-secret request — see [`secrets-management.md`](secrets-management.md).
- Access to customer data requires a per-customer request — see [`customer-data-handling.md`](customer-data-handling.md).

"No access" is not a defect. It is the correct starting state.

## 4. Privileged Roles at ACME

| Privileged Role | Standing? | Activation | Approver |
|-----------------|-----------|------------|----------|
| Entra ID Global Administrator | No | PIM, max 4h | CISO (`Rajan Mehta`) |
| Entra ID Security Administrator | No | PIM, max 4h | CISO |
| Entra ID Exchange / SharePoint Administrator | No | PIM, max 4h | Security Director (`Neha Saxena`) |
| GitHub Enterprise Organization Owner | No | PIM, max 4h | Security Director |
| GitHub Enterprise Repository Administrator | No | PIM, max 4h | Repository Owner + Security Director |
| Production Cloud Subscription Contributor (Azure, AWS, GCP) | No | PIM, max 4h | Security Director + Cloud Platform Lead |
| Production Database Administrator | No | PIM, max 4h | Database Lead + Security Director |
| ACME Vault Administrator | No | PIM, max 2h | IAM Engineer (`Abhishek Verma`) + CISO |
| Customer Support Tools — elevated | No | PIM, max 4h | Support Lead + Security Director |
| Break-glass account | Reserved for incident use only — see §8 | — | — |

There is **no standing production access** for engineers. Engineers receive time-bound, task-specific access through PIM. This is enforced by the cloud subscriptions' RBAC and by the GitHub Enterprise SSO-to-role mapping.

## 5. PIM — Time-Bound Elevation

Privileged Identity Management (PIM) is the mechanism for time-bound elevation. To request elevated access:

1. Open the Entra ID PIM portal (`https://myaccount.microsoft.com → Privileged Identity Management → My roles`, fictional URL).
2. Select the role you need to activate.
3. Choose a duration (default 4 hours, max 8 hours).
4. Provide a justification — link the ticket, the incident, or the change request.
5. The activation request is routed to the approver (see table in §4).
6. Approver reviews and approves (or denies) within 30 minutes during business hours; the on-call approver handles out-of-hours requests.
7. On approval, the role is active for the chosen duration. MFA reauthentication is required.
8. At the end of the duration, the role is automatically removed.

All activations are logged and reviewed monthly by the IAM Engineer (`Abhishek Verma`) and quarterly by the GRC Analyst (`Karthik Subramanian`).

For access request workflow details, see [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md). To raise an access request, see [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md) and [`../08-forms/repository-access-request.md`](../08-forms/repository-access-request.md).

## 6. No Standing Production Access

The phrase "no standing production access" deserves its own section because it is the most-violated least-privilege rule across the industry. At ACME:

- Engineers do **not** have standing `Contributor` or `Owner` roles on production cloud subscriptions.
- Engineers do **not** have standing database-administrator roles on production databases.
- Engineers do **not** have standing administrative access to production Kubernetes clusters.
- Engineers do **not** have standing write access to production secrets in ACME Vault.
- Engineers **do** have standing read access to non-PII production telemetry, logs (without PII fields), and runbooks, sufficient for on-call triage. Anything beyond that requires PIM activation.

If you believe you need standing production access, raise the request through `security-oncall@acme.example` (fictional). The answer will be PIM activation, with one exception: the break-glass account (§8).

## 7. Access Review Cadence

- **Quarterly:** Every privileged role and every Confidential/Restricted data store is reviewed. The IAM Engineer (`Abhishek Verma`) runs the review; managers attest. See [`identity-and-access-management.md`](identity-and-access-management.md) §7.
- **On role change:** Manager initiates a removal request for access no longer needed. IAM Engineer verifies within 5 business days.
- **On exception expiry:** The exception owner attests renewal or it lapses.
- **Continuous:** SOC monitors for anomalous access patterns — e.g., a PIM activation outside business hours with no associated ticket — and triggers review.

Stale access is the most common audit finding. Do not let your access be one of them — if you no longer need something, ask for it to be removed.

## 8. Break-Glass Account

For incidents where the normal PIM flow is unavailable (e.g., Entra ID itself is degraded), ACME maintains a break-glass account:

- Stored credentials are in a physical sealed envelope in the Hyderabad and London offices, plus a sealed digital copy in ACME Vault (`vault.acme.example`, fictional).
- Use requires CISO (`Rajan Mehta`) or designee authorization.
- Use is logged at the highest severity and triggers a post-incident review.
- The password is rotated after every use.

This account exists for emergencies, not for convenience.

## 9. Responsibilities

| Role | Responsibility |
|------|----------------|
| **IAM Engineer** (`Abhishek Verma`) | Configures PIM roles and approval workflows. Runs quarterly access reviews. Approves routine access requests. |
| **Security Director** (`Neha Saxena`) | Approves privileged role activations per the matrix in §4. |
| **CISO** (`Rajan Mehta`) | Approves Global Administrator and break-glass use. Owns exception policy. |
| **GRC Analyst** (`Karthik Subramanian`) | Audits PIM activation logs quarterly. Maintains the risk register entry for least-privilege risk. |
| **SOC Lead** (`Fatima Sheikh`) | Monitors for anomalous PIM activations. |
| **People Managers** | Initiate removal of stale access. Attest quarterly reviews. |
| **Every workforce member** | Requests only the access they need. Activates PIM only for the task at hand. Deactivates when done. |

## 10. Enforcement

- Cloud subscriptions enforce RBAC; standing `Contributor` or `Owner` assignments are blocked at the management group level by Azure Policy.
- GitHub Enterprise enforces SSO-to-role mapping; standing admin assignments require an exception.
- PIM is enforced at the IdP level; there is no client-side bypass.
- Audit findings from access reviews are tracked to closure by the GRC Analyst.

## 11. Exceptions

Exceptions are rare and time-bound, with a documented compensating control. To request one (e.g., a vendor integration that requires a long-lived service principal), email `security-oncall@acme.example` (fictional). The IAM Engineer reviews, the Security Director or CISO approves, and the exception is logged in the risk register.

## 12. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`identity-and-access-management.md`](identity-and-access-management.md) — Entra ID, conditional access, PIM mechanics.
- [`password-and-mfa-requirements.md`](password-and-mfa-requirements.md) — Authentication factors, including FIDO2 for privileged roles.
- [`data-classification.md`](data-classification.md) — Drives Confidential/Restricted handling rules.
- [`secrets-management.md`](secrets-management.md) — Per-secret access for Restricted-tier credentials.
- [`customer-data-handling.md`](customer-data-handling.md) — Per-customer access for Customer Data tier.
- [`source-code-security.md`](source-code-security.md) — Repository access and CODEOWNERS.
- [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) — Termination workflow.
- [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md) — Access request workflow.
- [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md) — Access request form.
- [`../08-forms/repository-access-request.md`](../08-forms/repository-access-request.md) — Repository access form.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — IAM Engineer, Security Director, CISO contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — JIT, PIM, RBAC, ABAC, default-deny definitions.
