---
document_id: ACME-WF-011
title: Equipment Handover Workflow
category: workflow
department: information-technology
applicable_roles: [all]
owner: IT Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [workflow, onboarding, equipment-handover]
---

# Equipment Handover Workflow

> Fictional document. All systems (Intune, portal.acme.example) are illustrative.

## 1. Overview

Equipment handover is the physical + digital chain that moves a laptop and peripherals from the IT pool to the new hire's responsibility. The canonical sequencing rule:

> Equipment handover (EQP-001) must complete before device acceptance (EQP-002). Device acceptance (EQP-002) must complete before responsibility acknowledgement (EQP-003) and inventory update (EQP-004).

All ACME laptops are Microsoft Intune-enrolled, BitLocker / FileVault encrypted, and asset-tagged. The handover is owned by IT Onboarding Specialist Geetha Iyer (`geetha.iyer@acme.example`) and approved by IT Manager Hyderabad Arjun Kapoor (`arjun.kapoor@acme.example`). Facilities leads (Hyder Ali, Lakshmi Venkat, Olivia Carter, Marcus Chen) handle physical staging at the office reception.

## 2. Scope

- **Starts:** 3 business days before start date (pre-stage, EQP-001).
- **Ends:** Day 5 (responsibility acknowledgement filed, EQP-003; inventory updated, EQP-004).
- **Roles involved:** IT Onboarding, IT Manager Hyderabad, Facilities, New Hire, Hiring Manager (for spec approval).
- **Office-agnostic;** for remote new hires, equipment is couriered and handover happens over a video call with the IT Onboarding Specialist.
- **Replacement / return equipment** follows the same workflow on the way back in (EQP-005 through EQP-008).

## 3. Cross-References

- IT: [`../02-it/laptop-and-workstation-allocation.md`](../02-it/laptop-and-workstation-allocation.md), [`../02-it/device-acceptance-and-responsibility.md`](../02-it/device-acceptance-and-responsibility.md), [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md), [`../02-it/equipment-replacement.md`](../02-it/equipment-replacement.md), [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md)
- Security: [`../03-security/device-encryption.md`](../03-security/device-encryption.md), [`../03-security/byod-policy.md`](../03-security/byod-policy.md)
- Forms: [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md), [`../08-forms/manager-approval.md`](../08-forms/manager-approval.md)
- Contacts: [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)

## 4. Equipment Handover Task List

| Task ID | Description | Responsible | Prerequisites | Due | Approval | Completion Criteria | Default Status |
|---|---|---|---|---|---|---|---|
| EQP-001 | Pre-stage equipment — pull laptop + peripherals from IT pool, image, Intune-enroll, asset-tag, store at office reception or courier for remote | IT Onboarding (Geetha Iyer) | MGR-001 (manager spec approved), [`preboarding.md`](./preboarding.md) PRE-005 | 3 business days before start date | IT Manager Hyderabad (Arjun Kapoor) | Asset tags scanned; Intune shows compliant; staging receipt filed | NOT_STARTED |
| EQP-002 | Handover equipment to new hire — physical handover at office reception or courier delivery for remote; verify asset serial numbers on the spot | IT Onboarding + New Hire | EQP-001, [`first-day-onboarding.md`](./first-day-onboarding.md) DAY1-001 (badge active) | Day 1 by 10:00 IST | IT Onboarding verification | Equipment physically with new hire; serial numbers match the handover form | NOT_STARTED |
| EQP-003 | New hire signs device acceptance + responsibility acknowledgement form | New Hire | EQP-002 | Day 1 by 12:00 IST | New Hire + HRBP countersign | Form submitted in HR Hub; countersigned | NOT_STARTED |
| EQP-004 | Update inventory system — assign asset tags to new hire's UPN in Intune + IT asset DB | IT Onboarding | EQP-003 | Day 1 by 17:00 IST | IT Manager Hyderabad | Inventory shows laptop + peripherals assigned to new hire; status "in-use" | NOT_STARTED |
| EQP-005 | Equipment replacement — when standard machine cannot be staged or is faulty: pull loaner from loaner pool, follow EQP-002 through EQP-004 for the loaner | IT Onboarding | EQP-001 (original staging) | Same business day as discovery | IT Manager Hyderabad | Loaner assigned; original ticket held open until standard machine is ready | NOT_STARTED |
| EQP-006 | Lost / stolen device report — see [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md) | New Hire + IT Onboarding | Equipment was assigned (EQP-004) | Same business day as discovery | IT Manager Hyderabad + CISO | Report filed; remote lock + wipe triggered in Intune; GRC incident logged | NOT_STARTED |
| EQP-007 | Equipment return on separation — new hire returns laptop + peripherals; IT inspects, sanitizes, returns to pool | IT Onboarding + Facilities | Separation event in HR Hub, ACC-010 started | Last working day | IT Manager Hyderabad | Equipment returned, sanitized, asset status "available"; serial numbers logged | NOT_STARTED |
| EQP-008 | Annual physical inventory audit — verify all assigned laptops match Intune + asset DB; flag mismatches | IT Onboarding + Facilities | EQP-004 last-completed | Annually (recurring) | IT Manager Hyderabad + CISO | Audit report filed; mismatches resolved within 10 business days | NOT_STARTED |

## 5. Dependencies

- **MGR-001 blocks EQP-001** — Pre-stage requires the manager's approved equipment spec (machine model, monitor count, peripheral list).
- **EQP-001 blocks EQP-002** — Handover requires pre-staging.
- **EQP-002 blocks EQP-003** — Device acceptance requires the equipment to be physically with the new hire.
- **EQP-003 blocks EQP-004** — Inventory update requires the signed acceptance form (so the audit trail is intact).
- **EQP-001 (failure) → EQP-005** — A failed pre-stage triggers the loaner workflow as a fallback.
- **EQP-004 → EQP-006, EQP-007, EQP-008** — All downstream equipment tasks require the inventory assignment to be in place.
- **EQP-007 → ACC-010** — Equipment return is part of the access-revocation / separation sequence (canonical).
- **DAY1-002 ↔ EQP-002** — The day-1 laptop handover task (DAY1-002) is the same event as EQP-002; the day-1 file references EQP-002 for the physical handover.

## 6. Status Tracking

All EQP-* tasks are tracked in the IT asset DB (mirrored to HR Hub under **Onboarding → Equipment**). Allowed statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

If EQP-002 (handover) cannot be completed because the new hire is unexpectedly absent on day 1, IT holds the equipment at the reception and the file stays `IN_PROGRESS`; if the new hire does not arrive within 5 business days, IT returns the equipment to the pool and re-stages when the new start date is confirmed.

If EQP-006 (lost/stolen) is filed, the GRC Analyst opens a security incident per [`../03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md); remote wipe is triggered automatically by Intune within 1 hour of the report.

## 7. RACI Matrix

| Activity | R | A | C | I |
|---|---|---|---|---|
| Pre-stage equipment | IT Onboarding | IT Manager Hyderabad | Facilities, Hiring Manager | Security |
| Handover equipment | IT Onboarding + New Hire | IT Onboarding verification | Facilities | HRBP |
| Device acceptance + responsibility ack | New Hire | New Hire + HRBP | IT Onboarding | VP HR |
| Inventory update | IT Onboarding | IT Manager Hyderabad | HRBP | CISO office |
| Equipment replacement (loaner) | IT Onboarding | IT Manager Hyderabad | New Hire | HRBP |
| Lost/stolen report | New Hire + IT Onboarding | IT Manager Hyderabad + CISO | Security (GRC) | VP HR |
| Equipment return (separation) | IT Onboarding + Facilities | IT Manager Hyderabad | HRBP | CISO office |
| Annual physical inventory audit | IT Onboarding + Facilities | IT Manager Hyderabad + CISO | HRBP | VP IT |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 8. Key Terms

- **MDM** — Mobile Device Management; at ACME, Microsoft Intune. See [`../metadata/glossary.md`](../metadata/glossary.md).
- **EDR** — Endpoint Detection and Response; at ACME, Microsoft Defender for Endpoint.
- **BYOD** — Bring Your Own Device. See [`../03-security/byod-policy.md`](../03-security/byod-policy.md).
- **Asset tag** — unique physical identifier affixed to each ACME-owned device.
- **Remote wipe** — capability in Intune to remotely erase a lost or stolen device.
- **Sanitization** — secure data erasure performed before a device returns to the pool or is disposed of.

## 9. Hand-off

When EQP-001 through EQP-004 are `COMPLETED`, the equipment portion of the onboarding file is closed. The new hire's responsibility for the equipment continues until separation (EQP-007) or replacement (EQP-005). The annual audit (EQP-008) runs forever.
