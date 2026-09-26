---
document_id: ACME-FORM-007
title: Equipment Handover Form
category: form
department: it-operations
applicable_roles: [all]
owner: IT
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, it, equipment, laptop, handover, asset, signature]
---

# Equipment Handover Form

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. Asset tags, serial numbers, MAC addresses, and the ITSM endpoint `helpdesk.acme.example` below are illustrative. Do not submit real asset information against this template.

## 1. Form Purpose

This form records the physical handover of ACME-owned equipment (primarily a laptop and accessories) from the IT Onboarding Specialist to the employee. It is completed on the employee's first day on-site (see [`../07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) and [`../07-workflows/equipment-handover.md`](../07-workflows/equipment-handover.md)) and acts as the legal acknowledgement of receipt and responsibility per [`../02-it/device-acceptance-and-responsibility.md`](../02-it/device-acceptance-and-responsibility.md). The form is the source of truth for the asset register and is referenced during offboarding (see [`../12-offboarding/equipment-return.md`](../12-offboarding/equipment-return.md)).

## 2. Mandatory Fields

| # | Field | Type | Validation | Sample (fictional) |
|---|-------|------|------------|--------------------|
| 1 | Employee name | string | non-empty | Anika Rao |
| 2 | Employee ID | string | `ACME-YYYY-NNNN` | ACME-2026-0488 |
| 3 | Employee corporate email | email | `@acme.example` | anika.rao@acme.example |
| 4 | Office assignment | enum | Hyderabad / Bengaluru / London / Seattle / Remote | Bengaluru |
| 5 | Handover date | date (YYYY-MM-DD) | today or future | 2026-09-15 |
| 6 | Asset type | enum | laptop / monitor / dock / keyboard / mouse / headset / phone / yubikey / other | laptop |
| 7 | Asset tag | string | matches IT asset register (ACME-AST-NNNNN) | ACME-AST-10231 |
| 8 | Serial number | string | matches manufacturer format | C02XK1XYZJHG |
| 9 | Make & model | string | matches IT catalog | Apple MacBook Pro 14 (2024) |
| 10 | Operating system | enum | macOS Sonoma / Windows 11 Pro / Ubuntu 22.04 LTS | macOS Sonoma |
| 11 | Accessories handed over | text | non-empty list | USB-C power adapter, 2m cable, sleeve, Logitech MX Master 3S mouse |
| 12 | Employee signature | signature | captured in HR Hub | (signed) Anika Rao, 2026-09-15 |
| 13 | IT Onboarding Specialist signature | signature | captured in HR Hub | (signed) Geetha Iyer, 2026-09-15 |
| 14 | Handover location | string | office name | ACME Bengaluru — Floor 4 IT Bay |

## 3. Optional Fields

| # | Field | Type | Validation | Notes |
|---|-------|------|------------|-------|
| 1 | MAC address (Wi-Fi) | string | IEEE 802 MAC format | For network registration |
| 2 | MAC address (Ethernet) | string | IEEE 802 MAC format | For docked use |
| 3 | Hostname | string | matches Intune enrollment | e.g., `ACME-MBP-10231` |
| 4 | Disk encryption key fingerprint | string | matches FileVault / BitLocker record | Auto-captured by Intune |
| 5 | Pre-installed software list | text | matches standard image | Auto-captured by Intune |
| 6 | External monitor asset tag | string | matches asset register | If a monitor is also handed over |
| 7 | Yubikey serial | string | matches Yubikey registry | For engineers with prod-deploy |
| 8 | Notes | text | free text | e.g., "second laptop for travel", "replacement device" |
| 9 | Witness name (for off-hours handover) | string | ACME employee email | Only if handover outside business hours |

## 4. Validation Rules

1. Asset tag must match an active record in the IT asset register at `helpdesk.acme.example` (simulated). Stolen, retired, or already-assigned tags cause the form to be auto-rejected.
2. Serial number must match the asset tag's recorded serial. A mismatch triggers a hold-and-investigate flow.
3. Both signatures (employee + IT Onboarding Specialist) are mandatory. The form is `pending` until both are captured.
4. If the asset is a laptop, the operating system must match the laptop allocation policy at [`../02-it/laptop-and-workstation-allocation.md`](../02-it/laptop-and-workstation-allocation.md) — non-matching OS is auto-rejected.
5. Handover date must be on or after the employee's start date and on or before the start date + 5 business days (grace window for remote hires).
6. If a Yubikey is handed over, the Yubikey serial must be enrolled in the employee's Entra ID security info (see [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md)).

## 5. Responsible Owner

- **Form owner (IT):** IT Onboarding Specialist — Geetha Iyer (`geetha.iyer@acme.example`).
- **IT Manager Hyderabad (escalation):** Arjun Kapoor (`arjun.kapoor@acme.example`).
- **Asset register system:** ITSM at `https://helpdesk.acme.example` (simulated endpoint).
- **Storage location:** ACME HR Hub (`hr.acme.example`, fictional) with `confidential` classification.
- **Access:** Restricted to IT Onboarding Specialist + the employee + the employee's manager (read-only) + HR Operations (read-only).

## 6. Approval Requirements (Workflow)

1. **Employee acknowledgement (mandatory).** The employee reviews the device acceptance terms at [`../02-it/device-acceptance-and-responsibility.md`](../02-it/device-acceptance-and-responsibility.md) and signs the form on day 1. By signing, the employee acknowledges:
   - The device is ACME property.
   - The device is enrolled in Microsoft Intune for management.
   - Disk encryption is enabled (FileVault on macOS, BitLocker on Windows).
   - The employee will not install unapproved software (see [`../02-it/approved-software-installation.md`](../02-it/approved-software-installation.md)).
   - The device will be returned on separation (see [`../12-offboarding/equipment-return.md`](../12-offboarding/equipment-return.md)).
2. **IT Onboarding Specialist signature (mandatory).** The IT Onboarding Specialist confirms the device was prepared per the standard image, enrolled in Intune, and is being handed to the named employee.
3. **No further approvals.** This form does not route to managers or HR — the two signatures above are the only approval gates.
4. **Routing outcome.** Signed form triggers:
   - Asset register status update (`assigned` → employee ID).
   - Intune compliance check enabled for the device.
   - The device acceptance record is linked to ACME-FORM-008 ([`./policy-acknowledgement.md`](./policy-acknowledgement.md)) for the employee's overall acknowledgement file.
5. **Offboarding reference.** On separation, this form is pulled to confirm what equipment must be returned (see [`../12-offboarding/equipment-return.md`](../12-offboarding/equipment-return.md)).

## 7. Sample Filled Values (Fictional)

```yaml
form_id: ACME-FORM-007
submission_id: ACME-2026-0488-EQ-1
submitted_at: 2026-09-15T11:00:00+05:30
employee:
  name: Anika Rao
  employee_id: ACME-2026-0488
  corporate_email: anika.rao@acme.example
  office_assignment: Bengaluru
handover:
  date: 2026-09-15
  location: ACME Bengaluru — Floor 4 IT Bay
  asset_type: laptop
  asset_tag: ACME-AST-10231
  serial_number: C02XK1XYZJHG
  make_model: Apple MacBook Pro 14 (2024)
  operating_system: macOS Sonoma
  accessories:
    - USB-C 67W power adapter
    - 2m USB-C charge cable
    - MacBook sleeve
    - Logitech MX Master 3S mouse
  mac_address_wifi: "A4:83:E7:11:22:33"
  hostname: ACME-MBP-10231
  disk_encryption_key_fingerprint: "FV-9F2C1A8B7E6D5C4B"
  pre_installed_software: standard-cloud-api-image-v3.2
signatures:
  employee:
    name: Anika Rao
    signed_at: 2026-09-15T11:15:00+05:30
  it_onboarding_specialist:
    name: Geetha Iyer
    email: geetha.iyer@acme.example
    signed_at: 2026-09-15T11:20:00+05:30
asset_register_update:
  status: assigned
  assigned_to: ACME-2026-0488
  updated_at: 2026-09-15T11:21:00+05:30
```

## 8. Related Documents

- [`../02-it/laptop-and-workstation-allocation.md`](../02-it/laptop-and-workstation-allocation.md) — Allocation policy.
- [`../02-it/device-acceptance-and-responsibility.md`](../02-it/device-acceptance-and-responsibility.md) — Terms the employee signs against.
- [`../02-it/approved-software-installation.md`](../02-it/approved-software-installation.md) — Software install rules.
- [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md) — MFA / Yubikey context.
- [`../07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) — Day 1 workflow context.
- [`../07-workflows/equipment-handover.md`](../07-workflows/equipment-handover.md) — Handover workflow context.
- [`../12-offboarding/equipment-return.md`](../12-offboarding/equipment-return.md) — Offboarding return.
- [`./it-access-request.md`](./it-access-request.md) — Sibling form that triggered the laptop allocation.
- [`./policy-acknowledgement.md`](./policy-acknowledgement.md) — Companion acknowledgement form.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — IT Onboarding Specialist contact.
