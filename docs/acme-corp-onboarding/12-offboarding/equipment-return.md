---
document_id: ACME-OFF-002
title: Equipment Return Process
category: offboarding
department: it-operations
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [offboarding, equipment, asset-return, device-wipe, intune]
---

# Equipment Return Process

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. The ITSM endpoints (`helpdesk.acme.example`), Intune tenant configuration, asset tags, and serial numbers below are illustrative. Microsoft Intune and Microsoft Entra ID are real infrastructure; the ACME tenant configuration is fictional.

## 1. Purpose

This document defines the process for returning ACME-owned equipment at the end of employment — primarily the laptop, monitor, peripherals, and physical access badge. It is the **inverse** of the onboarding equipment handover defined in [`../07-workflows/equipment-handover.md`](../07-workflows/equipment-handover.md) and uses the **same form** ([`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md)) filled out in **reverse**: the return section of the form signed on day 1 is the source of truth for what must be returned on the last working day (LWD).

This process is consistent with [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §3.1 (Pre-LWD), §3.2 (LWD device return), and [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) §Access Revocation. The canonical sequencing rule:

> Device return (EQP-007) must complete on the LWD; the device wipe (DEP-021) must complete on the LWD; the Entra ID account disable (DEP-022) executes at end-of-business on the LWD after the device is in IT's possession.

## 2. Scope

This applies to:

- All ACME-owned laptops (macOS and Windows).
- External monitors, docks, keyboards, mice, headsets, and webcams.
- Yubikeys and hardware security keys.
- Office badges and physical access tokens.
- Loaner equipment (must be returned separately, even if the standard device has already been returned).
- Equipment held by remote employees in any ACME office location (Hyderabad, Bengaluru, London, Seattle) or fully remote.

This does **not** cover:

- BYOD devices — those are governed by [`../03-security/byod-policy.md`](../03-security/byod-policy.md) and require only selective wipe of corporate data via Intune app protection policies.
- Replacement-equipment mid-tenure swaps — those follow [`../02-it/equipment-replacement.md`](../02-it/equipment-replacement.md) and use the forward equipment-handover workflow.
- Lost or stolen devices — those follow [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md) (remote wipe + insurance + GRC incident, no physical return possible).

## 3. Owner and SLA

- **Process owner:** IT Onboarding Specialist — Geetha Iyer (`geetha.iyer@acme.example`).
- **Escalation:** IT Manager Hyderabad — Arjun Kapoor (`arjun.kapoor@acme.example`).
- **SLA:** Equipment return is **completed within 5 business days of the LWD** (i.e., by T+5). For on-site employees, return is expected **on the LWD itself** (T-0). For remote employees, the courier process (§7) governs and may take up to 5 business days.
- **Audit:** The GRC Analyst (Karthik Subramanian, `karthik.subramanian@acme.example`) reviews equipment-return compliance quarterly. Any return older than 5 business days is flagged in the access-review report — see [`../08-forms/access-review.md`](../08-forms/access-review.md).

## 4. Equipment Covered

| Asset type | Examples | Return mechanism | Condition check |
|------------|----------|------------------|------------------|
| Laptop | Apple MacBook Pro 14, Dell Latitude 7450, Lenovo ThinkPad T14 | Physical return or courier (remote) | Visual + functional; Intune wipe |
| Monitor | Dell U2723QE, LG 27UP850 | Physical return | Visual + power-on test |
| Dock | CalDigit TS4, Dell WD19 | Physical return | Visual + USB connectivity test |
| Peripherals | Logitech MX Master 3S, MX Keys, Anker headset, webcam | Physical return | Visual + functional |
| Yubikey | YubiKey 5C NFC, YubiKey 5 Nano | Physical return | Serial verified; FIDO2 entry removed from Entra ID |
| Badge | Physical building access card | Physical return | De-activated in PACS; visual inspection |
| Loaner equipment | Same categories as standard | Physical return | Same checks; flagged as loaner |

## 5. Asset Tag Reconciliation

Every ACME-owned device carries an asset tag in the format `ACME-AST-NNNNN`. The asset tag is the primary key for reconciliation.

1. IT Onboarding pulls the employee's original equipment-handover form ([`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md)) from HR Hub.
2. The form lists every asset tag handed to the employee on day 1.
3. As each item is returned, IT Onboarding scans the asset tag and matches it to the original form.
4. The IT asset register (`helpdesk.acme.example`, simulated) is updated from status `in-use` → `returned-pending-sanitization` → `available`.
5. **Mismatches** trigger a hold-and-investigate flow:
   - **Wrong asset tag returned** (e.g., a colleague's laptop) — IT Helpdesk opens an investigation; the original laptop is flagged as lost/stolen per [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md).
   - **Serial-number mismatch** — same investigation flow; BitLocker/FileVault recovery key is rotated immediately as a precaution.
   - **Missing peripherals** — recorded as "pending return"; HRBP is notified; the offboarding ticket stays `IN_PROGRESS` until resolved or until the 5-business-day SLA forces a write-off (and HR holds the equivalent cost against the final settlement per [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md)).

## 6. Condition Check and Data Wipe Verification

### 6.1 Condition check

| Component | Check | Pass criteria |
|-----------|-------|---------------|
| Laptop chassis | Visual | No cracked chassis, missing keys, or liquid damage; hinges intact |
| Display | Power-on | No dead pixels >5 mm, no backlight bleed, brightness uniform |
| Keyboard | Functional | Every key registers; no stuck keys |
| Trackpad | Functional | Click + drag work; no ghost clicks |
| Ports | Functional | USB-C / Thunderbolt / HDMI all functional with a dock |
| Battery | Health | Cycle count < 1000; capacity > 80% of original (Intune report) |
| Monitor | Power-on | No dead pixels; backlight uniform; stand intact |
| Dock | USB connectivity | All downstream ports enumerate; power delivery verified |
| Yubikey | Functional | Touch + OTP works; serial enrolled in Entra ID |
| Badge | Visual | Photo + name legible; no damage to RFID coil |

### 6.2 Data wipe

The data wipe is initiated from Intune (Microsoft Endpoint Manager admin center) by IT Onboarding as soon as the asset tag is reconciled. The wipe:

- Issues an Intune **Wipe** command (full reset to factory; for FileVault-encrypted macOS the recovery key is rotated first so the device cannot be re-activated without IT involvement).
- Removes the device from Intune enrollment.
- Removes the device from the Entra ID device list (after a 30-day soft-delete window during which it can be re-stated if returned to active use).
- Marks the disk-encryption key fingerprint in the asset register as **revoked**.

### 6.3 Wipe verification

| Step | Owner | Evidence |
|------|-------|----------|
| Wipe command issued in Intune | IT Onboarding (Geetha Iyer) | Intune action log entry |
| Device confirms wipe on next check-in | Endpoint Engineering | Intune device action history shows "Wipe complete" |
| BitLocker / FileVault recovery key rotated | Identity Engineering | Key rotation event in Entra ID audit log |
| Device removed from Entra ID device list | Identity Engineering | Device object state = `deleted` |
| Asset register status → `available` | IT Onboarding | ITSM asset record updated |

If the device **does not check in within 24 hours** (e.g., powered off, no network), IT falls back to:

- BitLocker/FileVault recovery key revocation (the device is bricked for corporate use at next sign-in).
- Local physical destruction if the device is subsequently recovered damaged — see [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md) for the insurance + write-off flow.

## 7. Remote-Employee Courier Process

For employees not within commuting distance of an ACME office (Hyderabad, Bengaluru, London, Seattle), the equipment return uses a courier process. The process starts at T-5 (five business days before the LWD) so the kit arrives at the Hyderabad IT depot on or before the LWD.

| # | Step | Owner | Timing |
|---|------|-------|--------|
| 1 | IT Onboarding ships an empty, pre-paid, tamper-evident courier box to the employee's home address on file | IT Onboarding (Geetha Iyer) | T-5 |
| 2 | Employee packs the laptop, peripherals, Yubikey, and badge into the box; seals the tamper-evident seal | Employee | T-2 |
| 3 | Employee hands the box to the courier (pickup scheduled by IT) | Employee | T-1 |
| 4 | Courier delivers to the Hyderabad IT depot | Courier | T-0 to T+3 |
| 5 | IT Onboarding opens the box in the presence of a witness (HRBP or a second IT staff member), photographs contents, and starts §5 (asset tag reconciliation) | IT Onboarding + Witness | T+1 to T+4 |
| 6 | §6 (condition check + data wipe) runs on the returned kit | IT Onboarding | T+1 to T+5 |
| 7 | IT Onboarding certifies the return section of [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) | IT Onboarding | T+5 (SLA) |

If the courier box does not arrive by T+3, IT Onboarding escalates to:

- The HRBP (for employee follow-up).
- IT Manager Hyderabad — Arjun Kapoor (for an exception to extend the SLA or trigger a write-off).
- GRC Analyst — Karthik Subramanian (if the device is suspected lost/stolen — open a security incident per [`../03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md)).

## 8. Peripheral Return and Replacement Handling

- **Peripherals** (dock, monitor, keyboard, mouse, headset, webcam) are returned with the laptop and checked against the original equipment-handover form. Missing peripherals are flagged for follow-up; HR holds replacement cost against the final settlement per [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) §Final Settlement if not returned within the SLA.
- **Replacement handling during the SLA window:** if a peripheral is returned damaged but the laptop is intact, IT Onboarding issues a like-for-like replacement from the IT pool (not for the employee to keep — for the IT pool). The damaged peripheral is written off per the asset-write-off policy.
- **Yubikey and badge:** these are non-reusable for the departing employee. The Yubikey serial is de-registered from Entra ID security info at the same time as the FIDO2 entry removal (see [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md) for the onboarding counterpart). The badge is de-activated in the physical access control system at EOB on the LWD (see [`./employee-departure-checklist.md`](./employee-departure-checklist.md) DEP-029). The badge may be **re-issued** to a future employee after visual refurbishment; the Yubikey is destroyed because it cannot be reliably re-keyed.

## 9. Loaner Equipment

If the departing employee holds a loaner (issued mid-tenure via [`../02-it/equipment-replacement.md`](../02-it/equipment-replacement.md) when their primary device was being repaired), the loaner must be returned **separately** from the primary device. The loaner's asset tag is logged against a separate row in the return section of the equipment-handover form. Loaner returns follow the same condition-check and wipe flow but are returned to the **loaner pool**, not the standard pool.

## 10. Status Tracking

All return tasks are tracked in the ITSM offboarding ticket (`OFFBD-YYYY-NNNNNN`) and mirrored to the HR Hub offboarding record. Allowed statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

The return subtasks (mapped to [`./employee-departure-checklist.md`](./employee-departure-checklist.md) DEP-* task IDs):

| Sub-task | Mapped DEP ID | Default status |
|----------|---------------|----------------|
| Pull original equipment-handover form | (prep, T-5) | NOT_STARTED |
| Physical return or courier box issued | DEP-016 / DEP-020 | NOT_STARTED |
| Asset tag reconciliation | DEP-020 | NOT_STARTED |
| Condition check | DEP-021 | NOT_STARTED |
| Data wipe initiated | DEP-021 | NOT_STARTED |
| Wipe verified | DEP-021 | NOT_STARTED |
| IT certifies return complete | DEP-026 | NOT_STARTED |

## 11. RACI Matrix

| Activity | R | A | C | I |
|----------|---|---|---|---|
| Trigger return (HRIS state change) | HRBP | HR Operations | IT Onboarding | VP HR |
| Pull original handover form | IT Onboarding | IT Onboarding | HRBP | Employee |
| Physical return (on-site) | Employee + IT Onboarding | IT Manager Hyderabad | HRBP | VP IT |
| Courier process (remote) | Employee + IT Onboarding | IT Manager Hyderabad | HRBP | VP IT |
| Asset tag reconciliation | IT Onboarding | IT Manager Hyderabad | GRC Analyst | CISO office |
| Condition check | IT Onboarding | IT Manager Hyderabad | HRBP | CISO office |
| Data wipe + verification | IT Onboarding + Identity Engineering | IT Manager Hyderabad | GRC Analyst | CISO office |
| Badge de-activation | Facilities + IT Helpdesk | IT Manager Hyderabad | HRBP | VP IT |
| Yubikey de-registration | Identity Engineering | IT Manager Hyderabad | GRC Analyst | CISO office |
| Loaner return | IT Onboarding | IT Manager Hyderabad | HRBP | VP IT |
| Final certification | IT Onboarding | IT Manager Hyderabad | HRBP + GRC Analyst | VP IT + CISO |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 12. Expected Outcomes

After this document:

- The IT Onboarding Specialist knows the asset-tag reconciliation flow, the condition-check matrix, the data-wipe verification steps, and the remote courier process.
- The GRC Analyst knows what evidence to demand for quarterly access reviews of offboarded employees' equipment returns.
- The HRBP knows how to handle missing peripherals (cost-hold against final settlement) and the SLA extension path.

## 13. Troubleshooting

| Symptom | Likely cause | Resolution |
|---------|--------------|------------|
| Returned laptop asset tag does not match the original handover form | Wrong laptop returned; colleague swap | IT Helpdesk opens investigation; original laptop flagged lost/stolen; BitLocker recovery key rotated; HRBP notified |
| Intune wipe command shows "pending" for >24 hours | Device powered off, no network | Fall back to key revocation; device bricks at next sign-in; if recovered later, physical destruction per write-off policy |
| Yubikey returned but FIDO2 entry still active in Entra ID | Identity Engineering did not de-register in time | Identity Engineering removes the FIDO2 entry; GRC logs as audit finding; root cause: SCIM cycle delay (postmortem within 5 business days) |
| Courier box arrives with broken tamper-evident seal | Tampering in transit | IT Onboarding opens in the presence of HRBP + a second witness; photographs; contents reconciled item-by-item; GRC opens a security incident if anything is missing per [`../03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md) |
| Remote employee cannot courier (international move, address change) | Logistics blocker | IT Onboarding arranges a FedEx/DHL international pickup; SLA extended to T+10; HRBP approves extension; CISO office informed |
| Employee returns equipment before the LWD (early departure) | Mutual shortening of notice | Standard flow applies; access is **not** revoked early unless emergency revocation (§5 of [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md)) applies |

## 14. Related Documents

- HR: [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md)
- IT: [`../02-it/device-acceptance-and-responsibility.md`](../02-it/device-acceptance-and-responsibility.md), [`../02-it/equipment-replacement.md`](../02-it/equipment-replacement.md), [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md), [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md), [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md)
- Security: [`../03-security/byod-policy.md`](../03-security/byod-policy.md), [`../03-security/device-encryption.md`](../03-security/device-encryption.md), [`../03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md)
- Workflows: [`../07-workflows/equipment-handover.md`](../07-workflows/equipment-handover.md)
- Forms: [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md), [`../08-forms/access-review.md`](../08-forms/access-review.md)
- Contacts: [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)
