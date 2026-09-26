---
document_id: ACME-SEC-012
title: Device Encryption
category: security
department: information-security
applicable_roles: [all]
owner: Fatima Sheikh, SOC Lead
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, encryption, bitlocker, filevault, intune, fictional]
---

# Device Encryption

> ACME Corp fictional onboarding library. Hostnames (`vault.acme.example`, `helpdesk.acme.example`) and the recovery-key mailbox are fictional. BitLocker and FileVault are real OS features; the ACME key-escrow configuration is simulated.

## 1. Purpose

This document defines ACME Corp's device encryption requirements. Encryption is the single most important control protecting Confidential, Restricted, and Customer Data when a device is lost, stolen, or seized at a border. Without encryption, a stolen laptop is a breach. With it, the same loss is a non-event for the data on disk. This policy is enforced by Intune at provisioning time — there is no opt-out.

## 2. Scope

This applies to:

- Every ACME-issued Windows laptop and desktop (BitLocker).
- Every ACME-issued macOS laptop (FileVault).
- Every ACME-issued external drive (USB, SSD, magnetic) used to store ACME data.
- BYOD personal phones used for ACME work — MAM containerization provides encryption-at-rest for corporate data; see [`byod-policy.md`](byod-policy.md).
- Virtual machines and disk volumes in ACME's cloud subscriptions (Azure, AWS, GCP) — encrypted at rest per the cloud security baseline.

This does **not** apply to BYOD personal laptops — see [`byod-policy.md`](byod-policy.md) §4 (personal laptops are not permitted for Confidential/Restricted/Customer Data work).

## 3. Full-Disk Encryption Requirement

Every ACME-issued laptop and desktop must have full-disk encryption enabled at provisioning time. There is no opt-out and no grace period.

| OS | Encryption Technology | ACME Standard |
|----|-----------------------|---------------|
| Windows 11 | **BitLocker** with AES-256 (XTS-AES 256) | Enabled by Intune at provisioning; recovery key escrowed in Intune. TPM 2.0 required. |
| macOS 13+ | **FileVault** (AES-XTS) | Enabled by Intune at provisioning; institutional recovery key escrowed in Intune. |
| Linux (corporate workstations only) | LUKS2 with AES-256 | Enabled by the Linux baseline; recovery key escrowed in ACME Vault. |
| External USB / SSD | BitLocker To Go (Windows) or VeraCrypt (cross-platform) | Required for any ACME data on external media. Use is discouraged; see §6. |
| Cloud VM disks | Platform-managed encryption at rest (Azure Storage Service Encryption, AWS EBS encryption, GCP CMEK) | Enabled by default on every ACME subscription. |

### 3.1 Why TPM 2.0 Is Required on Windows

The Trusted Platform Module (TPM 2.0) chip stores the BitLocker encryption key in hardware, so the key never sits in software-readable memory on its own. This protects against "cold-boot" attacks and against simply reading the key off the disk. Every ACME-issued Windows laptop is provisioned with TPM 2.0.

### 3.2 Why We Escrow Recovery Keys

If your laptop's motherboard fails, the TPM is wiped, or you forget your PIN, ACME must be able to recover your data. ACME escrows BitLocker and FileVault recovery keys in Intune so that:

- IT can recover a failed laptop (with manager approval and audit logging).
- The SOC can recover a laptop that is the subject of an investigation.
- You can self-recover using your corporate credentials at the Intune Company Portal.

Recovery keys are themselves classified as Restricted. Access to the key escrow is logged and reviewed monthly by the IAM Engineer (`Abhishek Verma`).

## 4. Lost Recovery Key — User Self-Service

If you are prompted for a BitLocker or FileVault recovery key on boot (e.g., after a BIOS update, a hardware change, or a PIN typo lockout):

1. On another device (e.g., your phone), navigate to `https://myaccount.microsoft.com` (Microsoft-hosted).
2. Sign in with your ACME account (`<your-corporate-email>`).
3. Navigate to **Devices → [select your laptop] → BitLocker recovery key** (or **FileVault recovery key** for macOS).
4. Microsoft displays the 48-digit BitLocker key (or the FileVault institutional recovery key).
5. Type it in on your laptop to unlock.

If your device does not appear in the list, contact the IT Helpdesk at `helpdesk.acme.example` (fictional) — Identity Engineering can retrieve the key from Intune after manager verification.

## 5. Encryption Requirements Table

| Device Type | Encryption | Key Storage | Recovery Path |
|-------------|------------|-------------|----------------|
| ACME Windows laptop | BitLocker XTS-AES-256 | TPM 2.0 + Intune escrow | Self-service at `myaccount.microsoft.com` |
| ACME macOS laptop | FileVault AES-XTS | Intune institutional key escrow | Self-service at `myaccount.microsoft.com` |
| ACME Linux workstation | LUKS2 AES-256 | ACME Vault (vault.acme.example, fictional) | Helpdesk after manager verification |
| External USB / SSD | BitLocker To Go or VeraCrypt | ACME Vault | Helpdesk after manager verification |
| Cloud VM disk | Platform-managed encryption at rest | Cloud KMS (Azure Key Vault, AWS KMS, GCP KMS) | Cloud administrator |
| BYOD personal phone (corporate container) | Intune MAM encryption | Intune-managed | Not user-accessible; selective wipe on separation |

## 6. External Drives

External drives are discouraged for ACME data. The default position is: store ACME data in ACME-managed cloud storage (OneDrive, SharePoint, the approved customer-data site). If an external drive is unavoidable:

- The drive must be encrypted with BitLocker To Go (Windows) or VeraCrypt (cross-platform).
- The recovery key must be escrowed in ACME Vault (see [`secrets-management.md`](secrets-management.md)).
- The drive must never contain Customer Data — see [`customer-data-handling.md`](customer-data-handling.md).
- The drive must be returned to IT at separation per [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md).
- The drive must be reported lost within 1 hour per [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md).

## 7. Encryption in Transit

While this document focuses on encryption at rest, encryption in transit is mandatory too:

- All ACME-issued laptops enforce HTTPS/TLS for all web traffic; HTTP is blocked at the browser level (mixed-content blocking + Intune policy).
- All connections to ACME internal systems use TLS 1.2+ (TLS 1.0 and 1.1 are disabled).
- The corporate VPN uses TLS-based transport (see [`../02-it/corporate-vpn-configuration.md`](../02-it/corporate-vpn-configuration.md)).
- SSH to ACME systems uses ed25519 keys only (RSA is being retired).
- Code commits to `git.acme.example` (fictional) use HTTPS with personal access tokens or SSH with ed25519 keys.

## 8. Responsibilities

| Role | Responsibility |
|------|----------------|
| **SOC Lead** (`Fatima Sheikh`) | Owns this document. Monitors Intune encryption compliance reports. |
| **IAM Engineer** (`Abhishek Verma`) | Configures Intune encryption policy. Manages key escrow access. |
| **IT Helpdesk** | Performs key recovery with manager verification when self-service fails. |
| **Endpoint Engineering** | Provisions Windows with TPM 2.0 + BitLocker at imaging time; provisions macOS with FileVault at imaging time. |
| **Every workforce member** | Reports lost or stolen laptops immediately. Does not disable encryption. Does not store the recovery key outside ACME systems. |

## 9. Enforcement

- Intune compliance policy marks a non-encrypted laptop as non-compliant within 4 hours.
- Conditional access (see [`identity-and-access-management.md`](identity-and-access-management.md)) blocks non-compliant devices from SSO — meaning the user cannot access Microsoft 365, GitHub Enterprise, or any ACME app from the non-encrypted device.
- The user has 24 hours to remediate (re-enable encryption) before the device is force-locked.
- A user who disables encryption deliberately is subject to disciplinary action under [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md).

## 10. Lost or Stolen Encrypted Laptop

If an encrypted laptop is lost or stolen:

1. Report within 1 hour to `security-incident@acme.example` (fictional) — see [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md).
2. The SOC issues a remote lock via Intune (the laptop will require the BitLocker recovery key on next boot, which an attacker does not have).
3. The SOC issues a remote wipe if the laptop had Customer Data locally stored (rare — Customer Data must not be local per [`customer-data-handling.md`](customer-data-handling.md)).
4. The IAM Engineer revokes the user's refresh tokens and resets the password as a precaution.
5. The SOC reviews sign-in logs for the period the laptop was potentially in unauthorized hands.

The encryption is the control that turns a laptop loss into a non-event for the data on disk.

## 11. Exceptions

Exceptions to encryption are rare (e.g., a specialized lab device that cannot support encryption). They require SOC Lead (`Fatima Sheikh`) approval, a documented compensating control (e.g., physical safe storage, no Confidential/Restricted data on the device), and a time limit. Email `security-oncall@acme.example` (fictional).

## 12. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`acceptable-use-policy.md`](acceptable-use-policy.md) — Asset return obligations.
- [`data-classification.md`](data-classification.md) — Drives encryption requirement for Confidential/Restricted data.
- [`byod-policy.md`](byod-policy.md) — BYOD phones use MAM encryption, not full-disk.
- [`device-encryption.md`](device-encryption.md) — (this document)
- [`password-and-mfa-requirements.md`](password-and-mfa-requirements.md) — TPM 2.0 supports Windows Hello for Business.
- [`security-incident-reporting.md`](security-incident-reporting.md) — Lost device workflow.
- [`../02-it/windows-11-and-macos-workstation-setup.md`](../02-it/windows-11-and-macos-workstation-setup.md) — Encryption at provisioning.
- [`../02-it/laptop-and-workstation-allocation.md`](../02-it/laptop-and-workstation-allocation.md) — Hardware with TPM 2.0.
- [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md) — Lost device workflow.
- [`../02-it/corporate-vpn-configuration.md`](../02-it/corporate-vpn-configuration.md) — Encryption in transit.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — SOC Lead and Helpdesk contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — BitLocker, FileVault, TPM, Intune definitions.
