---
document_id: ACME-SEC-002
title: Acceptable Use Policy
category: security
department: information-security
applicable_roles: [all]
owner: Rajan Mehta, CISO
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, policy, acceptable-use, aup, fictional]
---

# Acceptable Use Policy

> ACME Corp fictional onboarding library. All hostnames, mailboxes, and systems in this document are fictional and used for illustration. No real credentials or live traffic are referenced.

## 1. Purpose

This Acceptable Use Policy (AUP) defines what ACME Corp considers acceptable and unacceptable use of its corporate systems, networks, accounts, and data. It exists to protect ACME, its employees, and its customers from harm — whether that harm is a security breach, a legal liability, or a hostile workplace. Every workforce member agrees to this policy as a condition of receiving access to ACME systems.

## 2. Scope

This AUP applies to:

- All ACME-issued devices and accounts (Microsoft 365, Entra ID, GitHub Enterprise at `git.acme.example`, internal portals).
- All ACME networks — office Wi-Fi, the corporate VPN (see [`../02-it/corporate-vpn-configuration.md`](../02-it/corporate-vpn-configuration.md)), and ACME datacenter networks.
- All approved personal devices used for ACME work under [`byod-policy.md`](byod-policy.md).
- All ACME data classified according to [`data-classification.md`](data-classification.md).
- All ACME-developed products — ACME Cloud, ACME Intelligence, ACME Workspace — and their production, staging, and development environments.

This AUP applies during and outside of working hours. Using an ACME device for personal activity outside work hours does not exempt the activity from this policy.

## 3. Acceptable Uses

Workforce members may use ACME systems for:

- Performing their job duties.
- Limited, incidental personal use that does not interfere with their work, does not consume disproportionate resources, and is not prohibited by §4.
- Communicating with colleagues, customers, and partners in accordance with [`../00-company/communication-guidelines.md`](../00-company/communication-guidelines.md).
- Storing and processing ACME data classified up to Confidential on ACME-managed systems, and Restricted data only on systems approved for that classification (see [`data-classification.md`](data-classification.md)).

## 4. Prohibited Uses

The following are expressly prohibited. The list is non-exhaustive — when in doubt, ask `security-oncall@acme.example` (fictional).

| Category | Examples of Prohibited Activity |
|----------|-------------------------------|
| **Illegal activity** | Any activity that violates Indian, UK, US, or other applicable law — including copyright infringement, software piracy, and accessing systems without authorization. |
| **Harassment** | Using ACME systems to harass, threaten, or demean anyone — see [`../01-hr/anti-harassment-policy.md`](../01-hr/anti-harassment-policy.md). |
| **Malware** | Intentionally introducing malware, ransomware, cryptominers, or unauthorized remote-access tools. |
| **Credential abuse** | Sharing passwords, MFA factors, or hardware keys. Reusing ACME credentials on external sites. Bypassing MFA. |
| **Data exfiltration** | Copying Confidential or Restricted data to personal cloud storage, personal email, USB drives, or unmanaged devices. |
| **External AI tools** | Entering customer data, source code, secrets, or Restricted information into any external AI tool. See [`ai-tool-acceptable-use.md`](ai-tool-acceptable-use.md). |
| **Circumventing controls** | Disabling Defender for Endpoint, removing Intune management, blocking DLP, or using personal VPNs to evade monitoring. |
| **Sharing access** | Letting another person — including a colleague — use your ACME account or device. |
| **Unapproved software** | Installing software that is not on the approved list (see [`../02-it/approved-software-installation.md`](../02-it/approved-software-installation.md)) on a managed device. |
| **Cryptocurrency** | Mining cryptocurrency on ACME devices or networks. |
| **Bypassing review** | Committing directly to `main`, force-pushing, or disabling branch protection. See [`source-code-security.md`](source-code-security.md). |
| **Personal business** | Running a personal business venture on ACME time, devices, or resources. |

## 5. Privacy Expectations

Workforce members should have **no expectation of privacy** when using ACME systems, networks, or accounts. ACME may, at its discretion and in accordance with applicable law:

- Monitor network traffic and authentication logs.
- Scan emails and chat for malicious content or data leakage (via Microsoft Purview).
- Review file access logs on Confidential and Restricted data repositories.
- Inspect a managed device if it is suspected of compromise.
- Review browsing activity conducted through ACME networks or VPN.

ACME does **not** conduct covert surveillance of employees without cause. Where cause exists — for example, a security incident, an HR investigation, or a legal hold — the request is reviewed by the Security Director (`Neha Saxena`) and the relevant HR Business Partner before collection begins. See [`privacy-acknowledgement.md`](privacy-acknowledgement.md) for the employee's privacy rights.

## 6. Monitoring

ACME operates the following monitoring, all of which is logged and reviewed by the SOC:

| Signal | Tool | Owner |
|--------|------|-------|
| Sign-ins, MFA, conditional access | Microsoft Entra ID | IAM Engineer (`Abhishek Verma`) |
| Endpoint telemetry | Microsoft Defender for Endpoint | SOC Lead (`Fatima Sheikh`) |
| DLP signals on email, chat, files | Microsoft Purview | SOC Lead |
| Repository activity (push, PR, secret) | GitHub Enterprise at `git.acme.example` (fictional) | Security Director (`Neha Saxena`) |
| Secrets in repos | Pre-commit hook + ACME Vault scan | IAM Engineer |
| Cloud configuration | Cloud Security Posture Management | SOC Lead |

Logs are retained per the ACME data retention schedule and are themselves classified Confidential.

## 7. Account and Password Hygiene

- Use a unique, strong passphrase (≥ 14 characters) for every ACME account. See [`password-and-mfa-requirements.md`](password-and-mfa-requirements.md).
- Store all corporate credentials in the 1Password Business vault (see [`../02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md)).
- Enable MFA on every account that supports it; MFA is mandatory on all ACME accounts.
- Lock your screen whenever you step away (5-minute idle lock is enforced by Intune — see [`clean-desk-policy.md`](clean-desk-policy.md)).
- Report any suspected credential compromise immediately to `security-incident@acme.example` (fictional).

## 8. Asset Return

ACME-issued assets — laptops, monitors, YubiKeys, phones, peripherals — remain ACME property. They must be returned:

- On the employee's last working day, per [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md).
- On request by IT or the manager.
- When the asset is being replaced (see [`../02-it/equipment-replacement.md`](../02-it/equipment-replacement.md)).
- When the asset is lost or stolen (see [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md)).

Failure to return assets may result in the cost being recovered from final pay, where permitted by local law.

## 9. Enforcement

Violations of this AUP are handled through the procedures in [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md) and may include:

- Access revocation (see [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md)).
- Disciplinary action, up to and including termination of employment.
- Civil or criminal referral where the law has been broken.

The CISO (`Rajan Mehta`) is the named owner of this AUP. Day-to-day enforcement is delegated to the Security Director (`Neha Saxena`) and the SOC Lead (`Fatima Sheikh`).

## 10. Exceptions

Exceptions are granted by the CISO or designee, in writing, for a defined period, with a compensating control. To request an exception, email `security-oncall@acme.example` (fictional). Self-granted exceptions are not valid.

## 11. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`data-classification.md`](data-classification.md) — What data can go where.
- [`password-and-mfa-requirements.md`](password-and-mfa-requirements.md) — Credential hygiene.
- [`byod-policy.md`](byod-policy.md) — Personal device rules.
- [`ai-tool-acceptable-use.md`](ai-tool-acceptable-use.md) — AI tools (a sub-AUP).
- [`source-code-security.md`](source-code-security.md) — Repository rules.
- [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md) — Behavioural baseline.
- [`../02-it/approved-software-installation.md`](../02-it/approved-software-installation.md) — What you can install.
- [`../02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md) — Where credentials live.
- [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md) — Acknowledgement form.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Security team contacts.
