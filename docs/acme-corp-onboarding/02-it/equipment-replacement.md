---
document_id: ACME-IT-017
title: Equipment Replacement
category: it
department: it-operations
applicable_roles: [all]
owner: Suresh Babu, Endpoint Engineer
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, equipment, replacement, rma, loaner, fictional]
---

# Equipment Replacement

> ACME Corp fictional onboarding library. The RMA workflow, ITAM references, and loaner inventory numbers are simulated.

## 1. Purpose

Explains the four primary reasons for replacing a corporate device — failure, upgrade, role change, and return-to-office — and the workflows for each: the **RMA (Return Merchandise Authorization)** process with the manufacturer, the **loaner laptop** pool, the **data migration** plan to preserve user data, and the typical **turn-around time (TAT)** for each scenario. This document pairs with [`laptop-and-workstation-allocation.md`](laptop-and-workstation-allocation.md) (allocation), [`device-acceptance-and-responsibility.md`](device-acceptance-and-responsibility.md) (handover), and [`lost-or-stolen-device-reporting.md`](lost-or-stolen-device-reporting.md) (loss path).

## 2. Prerequisites

- A signed [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) for the device being replaced.
- An approved replacement request (see §6 approval requirements).
- The device's asset tag for the RMA / migration steps.

## 3. Reasons for Replacement

### 3.1 Hardware Failure

- Examples: dead motherboard, failed SSD, broken hinge, liquid damage, display failure.
- Trigger: the device does not boot or is functionally unusable.
- Path: in §4 (RMA) + §5 (loaner).

### 3.2 Upgrade (Lifecycle Refresh)

- ACME refreshes laptops every **36 months** for Standard / Power tiers, every **30 months** for ML-Workstation / Design tiers (the shorter cycle reflects the heavier compute load).
- Trigger: refresh schedule reaches the asset.
- Path: §5 (loaner optional, often same-day swap) + §6 (data migration).

### 3.3 Role Change

- Example: an engineer moves from a backend role (Standard tier, Dell Latitude 5540) to an AI/ML role (ML-Workstation tier, MacBook Pro 14" M3 Pro).
- Trigger: HR-driven role change in the HRIS; IT Onboarding Specialist detects and queues the swap.
- Path: §5 (loaner optional) + §6 (data migration) + §7 (old-device return).

### 3.4 Return-to-Office

- A remote worker transitions to in-office and the device configuration needs to be updated (e.g., peripheral kit assignment, office Wi-Fi profile reload).
- Often does **not** require a device swap — only a profile update — but in some cases the existing device is recalled and a fresh-build office device is issued.
- Path: §6 (data migration is minimal — OneDrive / SharePoint carries the data) + §7 (old-device return).

## 4. The RMA Process (Hardware Failure)

> RMA applies when the device is under manufacturer warranty. ACME maintains a 3-year ProSupport Plus on Dell tiers and AppleCare+ for Enterprise on MacBook tiers.

1. **Diagnostic.** The Endpoint Engineer runs the manufacturer's diagnostic tool (Dell SupportAssist / Apple Diagnostics) to confirm a hardware fault. The diagnostic log is attached to the RMA.
2. **Approval.** The IT Manager (`arjun.kapoor@acme.example`) signs off on the RMA submission (this is a one-click approval — no policy review).
3. **RMA submission.** The Endpoint Engineer submits the RMA via the manufacturer's enterprise portal (Dell TechDirect / Apple Business Manager RMA), referencing the ACME PO number.
4. **Manufacturer response.** The manufacturer typically:
   - Approves the RMA within 1 business day (Dell) or 1–2 business days (Apple).
   - Provides an advance-ship replacement for ProSupport Plus (Dell) — a new device arrives before the old one is sent back.
   - Or provides a depot-repair for AppleCare+ — the device is shipped to Apple and returned in 5–7 business days.
5. **Replacement device received.** Endpoint Engineering images the replacement per [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md) and stages it for handover.
6. **Old device disposition.** The faulty device is shipped back to the manufacturer (advance-ship case) or returned to the user (depot-repair case) with the original disk wiped.

## 5. The Loaner Laptop Pool

> ACME maintains a pool of ~5% of fleet size as loaners (roughly 175 devices across the four offices) for use during RMA, refresh swaps, and short-term needs (e.g., a visitor, a training-room).

1. **Pool inventory.** Loaners are Standard-tier Dell Latitude 5540 devices; MacBook Pro 14" M3 loaners are reserved for ML / Design roles that cannot use a Windows substitute.
2. **Loan duration.** Up to 10 business days; extensions require IT Manager approval.
3. **Configuration.** Loaners are auto-enrolled in Intune; the user signs in with their corporate identity; their OneDrive / SharePoint data syncs automatically.
4. **Return.** The loaner is wiped (auto-wipe on next user sign-out via Intune) and returned to the pool.

## 6. Data Migration Plan

> The ACME baseline is "the cloud holds the data, the device is a thin client." Most migrations complete in under 2 hours because data is in OneDrive / SharePoint, not on the local disk.

| Data class | Where it lives | Migration step |
|------------|----------------|----------------|
| Documents, spreadsheets, presentations | OneDrive for Business | OneDrive sync client downloads on new device |
| Team / project files | SharePoint | Synced via OneDrive sync client on new device |
| Email | Exchange Online | Outlook re-syncs automatically |
| Chat history | Microsoft Teams | Teams client shows history on new device |
| Browser bookmarks | Edge for Business (synced via Entra ID) | Auto-sync on new device |
| Source code | GitHub Enterprise (`git.acme.example`) | `git clone` from the new device; nothing local-only |
| Local-only files (deviations from baseline) | Local disk | IT runs a `USMT` (Windows) or `Migration Assistant` (macOS) capture before wipe; restored on new device |

> If the device is non-bootable (failed SSD), local-only files cannot be recovered. The employee should keep all work in OneDrive / SharePoint / GitHub to avoid this. IT cannot recover a dead disk without specialist forensics, which costs USD 2,000+ and is only approved for legal / compliance cases.

## 7. Old-Device Return

1. The old device is wiped via Intune (Wipe command — full reset, no management retained).
2. For refresh / upgrade / role change, the old device returns to the ITAM inventory and is either:
   - Re-imaged and re-issued to a new hire (if within refresh window).
   - Surplus-sold via ACME's asset-disposal partner (with a certified data-destruction certificate).
3. For role change cases where the old tier is no longer needed (e.g., the engineer moves from Power tier to Standard tier — rare), the old device is recalled and re-issued to the next eligible new hire.

## 8. Turn-Around Time (TAT)

| Scenario | TAT (target) |
|----------|---------------|
| Loaner device issued (any scenario) | Same business day |
| RMA advance-ship replacement (Dell ProSupport Plus) | 2–3 business days from approval |
| RMA depot-repair return (AppleCare+ for Enterprise) | 5–7 business days from approval |
| Refresh swap (in-office) | Same business day |
| Refresh swap (remote) | 2–3 business days (courier) |
| Role-change swap (in-office) | 1–2 business days |
| Role-change swap (remote) | 3–5 business days |
| Data migration on new device | 1–2 hours (cloud-first) |

## 9. Expected Outcomes

After this document:

- The employee knows the four replacement scenarios and which workflow applies.
- The employee knows the RMA, loaner, migration, and TAT expectations.
- The employee knows the cloud-first data philosophy that makes migrations fast.

## 10. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| RMA rejected by manufacturer | Out of warranty or damage classed as "customer-induced" | IT Manager reviews; if customer-induced, employee may be charged (see [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md)); ACME may self-fund the repair. |
| Loaner pool depleted | Peak demand (e.g., a refresh wave) | Endpoint Engineering borrows from a sister office or issues a higher-tier loaner; TAT extends by 1–2 business days. |
| OneDrive migration stalls | Large file count / quota low | Run the OneDrive "Reset" tool; or temporarily increase quota via Identity Engineering. |
| Edge sync bookmarks do not appear | Sign-in issue on new device | Sign out / sign in to Edge for Business; verify sync is enabled in Settings → Profiles → Sync. |
| Old device will not wipe (offline) | Device not checking in | The device is RMA-shipped without wipe — IT confirms via manufacturer that the disk is destroyed on receipt. |
| GitHub Enterprise cannot clone on new device | Not on VPN or new SSH key not added | Connect VPN per [`corporate-vpn-configuration.md`](corporate-vpn-configuration.md); add new SSH key to GitHub Enterprise profile. |

## 11. Approval Requirements

- **Standard refresh swap:** no approval — driven by the refresh schedule.
- **Out-of-cycle upgrade (e.g., user requests an early refresh):** IT Manager (`arjun.kapoor@acme.example`) + the user's manager.
- **Role-change swap:** HRBP + IT Onboarding Specialist.
- **Loaner extension beyond 10 business days:** IT Manager.
- **Specialist forensic recovery (dead-disk data):** CISO (`rajan.mehta@acme.example`) + Legal (`hemant.joshi@acme.example`).
- **Surplus-sale of old devices:** IT Manager + Procurement + Legal (data-destruction certificate required).

## 12. Related Documents

- [`laptop-and-workstation-allocation.md`](laptop-and-workstation-allocation.md) — Standard tiers.
- [`device-acceptance-and-responsibility.md`](device-acceptance-and-responsibility.md) — Handover for the replacement.
- [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md) — Imaging baseline.
- [`lost-or-stolen-device-reporting.md`](lost-or-stolen-device-reporting.md) — If replacement is due to loss.
- [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md) — OneDrive / SharePoint first-run on the replacement.
- [`corporate-vpn-configuration.md`](corporate-vpn-configuration.md) — VPN on the replacement.
- [`corporate-wifi-setup.md`](corporate-wifi-setup.md) — Wi-Fi on the replacement.
- [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) — Handover form.
- [`../03-security/device-encryption.md`](../03-security/device-encryption.md) — Disk encryption on the replacement.
- [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md) — Customer-induced damage.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Endpoint Engineering contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — RMA, TAT, USMT definitions.
