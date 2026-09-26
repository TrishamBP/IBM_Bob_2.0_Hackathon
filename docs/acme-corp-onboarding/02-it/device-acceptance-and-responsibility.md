---
document_id: ACME-IT-003
title: Device Acceptance and Responsibility
category: it
department: it-operations
applicable_roles: [all]
owner: Geetha Iyer, IT Onboarding Specialist
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, device, acceptance, responsibility, encryption, fictional]
---

# Device Acceptance and Responsibility

> ACME Corp fictional onboarding library. Asset numbers and signatures below are illustrative. The actual acceptance record is the signed [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) stored in the ITAM system.

## 1. Purpose

Defines the act of accepting a corporate-issued laptop (and peripheral kit), the employee's ongoing responsibility for the device, the encryption acknowledgment, and the loss/damage process. Signing the handover form is a **mandatory** gate before the device is released; failure to sign within two business days of delivery triggers a recall of the device.

## 2. Scope

Applies to every ACME Corp employee, contractor, and intern who is issued a corporate device, regardless of:

- Employment type (full-time, fixed-term, contractor, intern).
- Work location (Hyderabad, Bengaluru, London, Seattle, or remote).
- Device tier (see [`laptop-and-workstation-allocation.md`](laptop-and-workstation-allocation.md)).

BYOD devices are out of scope; see [`../03-security/byod-policy.md`](../03-security/byod-policy.md).

## 3. Prerequisites

Before acceptance, the following must be true:

1. An approved IT request exists per [`new-employee-it-request.md`](new-employee-it-request.md).
2. The device is staged and encrypted per [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md) and [`../03-security/device-encryption.md`](../03-security/device-encryption.md).
3. The new hire's identity (`<firstname>.<lastname>@acme.example`) is provisioned in Entra ID.
4. A signed copy of [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) is ready (printed for in-office handover; DocuSign-equivalent for remote).
5. The asset tag is physically verified to match the ITAM record.

## 4. The Equipment Handover Form

The form ([`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md)) captures:

- **Recipient name** and user principal name (`<firstname>.<lastname>@acme.example`).
- **Device make / model / serial number / asset tag.**
- **Peripheral kit** line items (dock, monitors, headset, keyboard, mouse) with serial numbers where applicable.
- **Imaging baseline version** (e.g., `ACME-Image-Win11-2026.09`).
- **Encryption acknowledgment** (the recipient acknowledges that BitLocker / FileVault is active and that they will not disable it).
- **Acceptance checkbox** for the ACME acceptable use policy ([`../03-security/information-security-policy.md`](../03-security/information-security-policy.md)).
- **Recipient signature + date.**
- **IT representative signature + date** (for in-office: Endpoint Engineer; for remote: IT Onboarding Specialist).

## 5. Step-by-Step: In-Office Acceptance

1. The new hire arrives at the IT depot (Hyderabad: Block-C, 1st floor; Bengaluru: Tower-B, 2nd floor; London: 4th floor "Tech Bar"; Seattle: Building 2, suite 200).
2. The Endpoint Engineer retrieves the staged device and peripheral kit.
3. The new hire and the engineer jointly inspect the device for cosmetic damage and verify the asset tag on the underside.
4. The new hire verifies the device boots to the ACME-branded OOBE / FileVault recovery screen (this confirms encryption is active).
5. The new hire and the engineer complete [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) on a tablet at the depot.
6. Both parties sign; the ITAM system is updated with the timestamp and signatures.
7. The new hire collects the device and proceeds to [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md).

## 6. Step-by-Step: Remote Acceptance

1. The courier delivers the device to the address on file; signature on delivery is required.
2. The new hire opens the ACME Onboarding portal (`portal.acme.example`) and navigates to **"Accept My Device"** (a fictional simulated page).
3. The new hire enters the asset tag (printed on the underside sticker) and verifies against the ITAM record.
4. The new hire completes the digital [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) via DocuSign-equivalent workflow.
5. The new hire proceeds to [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md).
6. If the device arrives damaged or fails to boot, the new hire must **not** sign the form and must immediately raise a ticket (see §9).

## 7. Responsibility During the Term of Issue

The recipient acknowledges and agrees to the following ongoing responsibilities:

- **Custody.** The device is issued to the named recipient only. It may not be lent to family, friends, or other employees.
- **Encryption.** BitLocker / FileVault must remain enabled. Disabling it, suspending it indefinitely, or attempting to bypass it is a violation of [`../03-security/device-encryption.md`](../03-security/device-encryption.md) and may result in disciplinary action.
- **Patching.** The device must remain powered on and connected at least once every 14 days so that Intune can apply patches and configuration baselines.
- **Physical security.** When travelling, the device must be in the recipient's physical possession or stored in a locked location. Unattended devices in public spaces are not permitted.
- **Software.** Only approved software may be installed (see [`approved-software-installation.md`](approved-software-installation.md)).
- **Data.** All corporate data must remain in OneDrive for Business or the corporate SharePoint; local-only storage of confidential data is not permitted.
- **Return on separation.** The device and peripheral kit must be returned on or before the last working day per [`it-access-revocation.md`](it-access-revocation.md) and [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md).

## 8. Loss, Damage, and Theft

| Scenario | Required action | Timeframe |
|----------|-----------------|-----------|
| Minor cosmetic damage (no functional impact) | Raise a P4 ticket; IT will note the damage on the asset record. | Within 2 business days |
| Functional damage (device unusable) | Raise a P2 ticket; drop off at IT depot for repair or replacement (see [`equipment-replacement.md`](equipment-replacement.md)). | Within 1 business day |
| Lost device (whereabouts unknown) | Notify IT Helpdesk (`helpdesk@acme.example`) and Security (`security@acme.example`) immediately; see [`lost-or-stolen-device-reporting.md`](lost-or-stolen-device-reporting.md). | Within 2 hours of discovery |
| Stolen device | File a police report; notify IT and Security; remote wipe is initiated immediately. | Within 24 hours |
| Accidental damage on travel | Same as functional damage; travel insurance rider covers up to USD 1,500 with the police report. | Within 3 business days |

## 9. Encryption Acknowledgment (Required Statement)

By signing the handover form, the recipient attests:

> "I confirm that I have received the ACME Corp-issued device described in this form. I acknowledge that the device is encrypted with BitLocker / FileVault and that the recovery key is escrowed to Microsoft Entra ID. I will not disable, suspend, or bypass disk encryption. I understand that disabling encryption is a violation of ACME security policy and may result in disciplinary action up to and including termination of employment."

## 10. Expected Outcomes

After acceptance is complete:

- The ITAM record for the asset shows `Status: Issued`, `Custodian: <user principal name>`, `Issued On: <date>`.
- The recipient's Entra ID user object has the device listed under "Registered devices."
- The recipient has a signed PDF copy of [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) emailed to their `@acme.example` address.
- The recipient can proceed to first-time login ([`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md)).

## 11. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Asset tag does not match ITAM record | Sticker or DB mismatch | Endpoint Engineering re-verifies; do not sign until corrected. |
| Device boots to standard Windows / macOS OOBE, not ACME-branded | Imaging failed; encryption may not be active | Do not sign; return to IT depot for re-imaging. |
| Courier delivered wrong device | Order mis-picked | Raise a P2 ticket; courier will collect and re-deliver the correct device. |
| Signature tablet at depot is offline | Network outage | Use the offline handover form (paper backup); IT will digitize within 2 business days. |
| Digital signature link expired | Token older than 24 hours | IT Onboarding Specialist re-issues via `portal.acme.example`. |

## 12. Approval Requirements

- **Standard issuance:** No additional approval beyond the originating IT request.
- **Replacement for loss/damage:** See [`lost-or-stolen-device-reporting.md`](lost-or-stolen-device-reporting.md) and [`equipment-replacement.md`](equipment-replacement.md).
- **Transfer of custody (employee-to-employee):** Not permitted. The device must be returned to IT and re-issued through the standard process.

## 13. Related Documents

- [`new-employee-it-request.md`](new-employee-it-request.md) — Upstream request.
- [`laptop-and-workstation-allocation.md`](laptop-and-workstation-allocation.md) — Hardware tiers.
- [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md) — Next step after acceptance.
- [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) — The form referenced throughout.
- [`../03-security/device-encryption.md`](../03-security/device-encryption.md) — Encryption baseline.
- [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md) — Acceptable use.
- [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) — Return on separation.
- [`lost-or-stolen-device-reporting.md`](lost-or-stolen-device-reporting.md) — Loss/theft process.
- [`equipment-replacement.md`](equipment-replacement.md) — Functional damage / repair path.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Endpoint Engineering contacts.
