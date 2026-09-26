---
document_id: ACME-IT-002
title: Laptop and Workstation Allocation
category: it
department: it-operations
applicable_roles: [all]
owner: Suresh Babu, Endpoint Engineer
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, hardware, laptop, workstation, allocation, fictional]
---

# Laptop and Workstation Allocation

> ACME Corp fictional onboarding library. Hardware model numbers, asset tags, and hostnames below are illustrative and used for training/onboarding purposes only.

## 1. Purpose

Defines the standard laptop and peripheral configurations allocated to ACME Corp employees, the hardware tiers by role, the difference between in-office and remote allocations, and the lead times for procurement and staging. This document supports [`new-employee-it-request.md`](new-employee-it-request.md) and is referenced during device handover ([`device-acceptance-and-responsibility.md`](device-acceptance-and-responsibility.md)).

## 2. Hardware Tiers by Role

| Tier | Standard Model | Typical Roles | RAM | Storage |
|------|----------------|---------------|-----|---------|
| **Standard** | Dell Latitude 5540 (Windows 11 Pro) | Engineering (backend, frontend, QE), Sales, HR, Finance, Support | 16 GB | 512 GB NVMe |
| **Power** | Dell Latitude 7450 (Windows 11 Pro) | Senior engineers, Tech leads, Architects | 32 GB | 1 TB NVMe |
| **ML-Workstation** | MacBook Pro 14" M3 Pro | AI/ML engineers, Research, Data Science | 36 GB | 1 TB SSD |
| **Design** | MacBook Pro 16" M3 Max | Design, Product Design, Brand | 48 GB | 2 TB SSD |
| **Executive** | MacBook Pro 14" M3 | VP and above, Director+ | 24 GB | 1 TB SSD |
| **Light / kiosk** | Dell OptiPlex 3000 micro | Front-desk, lab kiosks, shared workstations | 8 GB | 256 GB NVMe |

> All laptops ship with full-disk encryption enabled (BitLocker on Windows, FileVault on macOS) prior to handover. See [`../03-security/device-encryption.md`](../03-security/device-encryption.md).

## 3. Peripheral Kit (In-Office Staff)

Each in-office workstation is staged with the following kit, asset-tagged to the user:

- 1 × Dell WD19S USB-C dock (or CalDigit TS4 for MacBook tiers).
- 1 × 27" 1440p monitor (Dell U2723QE) — 2 monitors for Engineering and Design tiers.
- 1 × Logitech MX Keys S keyboard (US layout; regional layouts on request).
- 1 × Logitech MX Master 3S mouse.
- 1 × Jabra Evolve2 65 headset (USB-C + Bluetooth).
- 1 × Anker 100W USB-C charger (for remote workers only).

Peripheral kits are **not** shipped to remote workers by default; remote workers may expense a home-office kit up to USD 350 on the standard catalog (see [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) for the expense receipt template).

## 4. Remote vs. In-Office Allocation

| Aspect | In-Office | Remote |
|--------|-----------|--------|
| Laptop delivery | Staged at IT depot; collected on day one | Couriered to home address; signature on delivery |
| Peripheral kit | Standard kit above | Optional, expensed up to USD 350 |
| Wi-Fi config | Pre-staged profile via Intune | Manual or Intune-pushed profile on first VPN |
| VPN client | Installed and tested pre-handover | Installed; first-connect guided on day one |
| Insurance / loss coverage | Office premises policy applies | Remote worker rider attached to the asset record |
| Return on separation | Drop off at IT depot | Courier arranged by IT (pre-paid label) |

## 5. Lead Times

| Action | Standard | Expedited (VP-approved) |
|--------|----------|-------------------------|
| In-stock laptop imaging + encryption | 2 business days | 1 business day |
| Out-of-stock procurement (India) | 10–15 business days | Not available — substitute equivalent in-stock tier |
| Out-of-stock procurement (US/UK) | 7–12 business days | Not available — substitute equivalent in-stock tier |
| Peripheral kit assembly | 1 business day | Same day |
| Courier (domestic India) | 2–3 business days | 1 business day (air) |
| Courier (international) | 5–8 business days | 3–5 business days |

If the requested tier is out of stock, Endpoint Engineering will propose the nearest equivalent and the IT Onboarding Specialist (`geetha.iyer@acme.example`) will confirm with the hiring manager.

## 6. Standard Configuration (Imaging Baseline)

Every laptop, regardless of tier, ships with the following baseline:

- **Operating system** fully patched to the latest monthly CU.
- **Microsoft Intune** management agent enrolled and reporting to `acme.onmicrosoft.com`.
- **Microsoft Defender for Endpoint** sensor active and onboarded to the corporate tenant.
- **BitLocker / FileVault** recovery key escrowed to Entra ID.
- **Microsoft 365 Apps for Enterprise** (Word, Excel, PowerPoint, Outlook, Teams, OneDrive).
- **Microsoft Edge for Business** as the default browser, signed-in state pre-provisioned via Windows Hello for Business.
- **1Password Business** desktop app and browser extension (SSO-enrolled on first launch).
- **ACME VPN client** (custom-branded OpenVPN Connect build) pre-configured for `vpn.acme.example`.
- **Standard ACME wallpaper and lock screen** with the asset tag printed bottom-right.
- **Local admin disabled**; standard users are members of `ACME-Corp-Users` only.

## 7. Hostname and Asset Tag Conventions

- **Windows hostnames:** `ACME-<2-char-office>-<6-digit-asset>`, e.g., `ACME-HY-100432`. Office codes: `HY` (Hyderabad), `BL` (Bengaluru), `LN` (London), `SE` (Seattle).
- **macOS hostnames:** `ACME-<2-char-office>-M<6-digit-asset>`, e.g., `ACME-HY-M100432`.
- **Asset tag format:** `ACME-ASSET-<6-digit-sequential>`, physically etched on the underside and recorded in the ITAM database (`itam.acme.example` — fictional).

## 8. Prerequisites

- An approved IT request per [`new-employee-it-request.md`](new-employee-it-request.md).
- The new hire's office location confirmed in the HRIS.
- The role bundle confirmed by the hiring manager.
- A signed [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) if the device is being collected on day one.

## 9. Step-by-Step: Requesting an Allocation

1. Hiring manager completes and submits [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md).
2. IT Onboarding Specialist reviews and matches the role to a tier using the table in §2.
3. Endpoint Engineering (`suresh.babu@acme.example`) checks stock in the ITAM database and either allocates from inventory or raises a procurement request.
4. The laptop is imaged using the standard Intune Autopilot / Apple Business Manager profile.
5. BitLocker / FileVault is enabled and the recovery key is escrowed to Entra ID under the device object.
6. The peripheral kit (if in-office) is staged at the IT depot.
7. The device is handover-ready on the day before the start date.

## 10. Expected Outcomes

At handover, the new hire should observe:

- A laptop that powers on to the corporate OOBE screen, displaying the ACME logo and a "Sign in with your corporate account" prompt.
- An asset tag matching the number printed on the underside sticker.
- A peripheral kit (if in-office) with matching asset tags on the dock and monitors.
- An entry in the ITAM database linking the asset tag to the new hire's user principal name.

## 11. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Laptop boots to generic Windows OOBE, not ACME-branded | Autopilot profile not assigned | Contact Endpoint Engineering; re-import the device hardware hash into Intune. |
| BitLocker recovery key not in Entra ID | Key escrow failed during imaging | Re-run the escrow task from the Intune console; do not hand over until escrow is confirmed. |
| Wrong tier delivered | Role mis-classified in IT request | IT Onboarding Specialist will arrange a swap; the wrong-tier device is returned to inventory. |
| Peripheral kit missing monitor 2 | Engineering/Design tier mis-staged | Log a P3 ticket; missing monitor couriered same business day. |
| Asset tag on sticker does not match ITAM record | Sticker swapped during assembly | Endpoint Engineering will re-etch and re-sticker; the device is re-issued. |

## 12. Approval Requirements

- **Standard tier:** Hiring manager + IT Onboarding Specialist.
- **Power tier:** + Hiring manager's director.
- **ML-Workstation / Design / Executive tier:** + VP IT (`ramesh.khanna@acme.example`).
- **Second monitor for non-Engineering role:** + IT Manager (`arjun.kapoor@acme.example`).
- **Home-office kit above USD 350:** + IT Manager.

## 13. Related Documents

- [`new-employee-it-request.md`](new-employee-it-request.md) — The upstream request that drives allocation.
- [`device-acceptance-and-responsibility.md`](device-acceptance-and-responsibility.md) — Sign-off at handover.
- [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md) — First power-on and enrollment.
- [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) — The handover form.
- [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md) — The request form.
- [`../03-security/device-encryption.md`](../03-security/device-encryption.md) — Encryption baseline.
- [`../03-security/byod-policy.md`](../03-security/byod-policy.md) — For exceptions.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Endpoint Engineering contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — ITAM, OOBE, Autopilot definitions.
