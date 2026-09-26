---
document_id: ACME-FORM-002
title: Emergency Contact Form
category: form
department: human-resources
applicable_roles: [all]
owner: HR
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, hr, emergency, preboarding, personal-data]
---

# Emergency Contact Form

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. This form is a template for demonstration only. Do not submit real personal information against this template. Names, phone numbers, and addresses below are illustrative.

## 1. Form Purpose

This form captures emergency contact information for an ACME Corp employee. The information is used **only** in the case of an emergency involving the employee at an ACME office or during ACME-sponsored travel — e.g., medical event, workplace incident, or natural disaster. The form is mandatory during preboarding (see [`../07-workflows/preboarding.md`](../07-workflows/preboarding.md)) and is reviewed at each onboarding milestone (day 1, day 30) so the data is current. A separate copy can be re-submitted any time a contact changes.

## 2. Mandatory Fields

| # | Field | Type | Validation | Sample (fictional) |
|---|-------|------|------------|--------------------|
| 1 | Employee name | string | non-empty | Anika Rao |
| 2 | Employee ID | string | matches HR record (ACME-YYYY-NNNN) | ACME-2026-0488 |
| 3 | Employee corporate email | email | matches `@acme.example` pattern | anika.rao@acme.example |
| 4 | Primary emergency contact name | string | non-empty | Sumith Rao |
| 5 | Relationship to employee | enum | Parent / Spouse / Sibling / Partner / Guardian / Other | Spouse |
| 6 | Primary phone | string (E.164) | non-empty, ≠ employee's own phone | +91-9876509876 |
| 7 | Primary contact address | text | non-empty | 14 Brigade Road, Bengaluru 560025 |
| 8 | Language preference | string | non-empty (English / Hindi / Kannada / Telugu / etc.) | English / Kannada |
| 9 | Submission date | date (YYYY-MM-DD) | today or earlier | 2026-09-10 |

## 3. Optional Fields

| # | Field | Type | Validation | Notes |
|---|-------|------|------------|-------|
| 1 | Secondary phone for primary contact | string (E.164) | non-empty if provided | Landline, alternate mobile |
| 2 | Secondary emergency contact name | string | non-empty if block is used | Recommended |
| 3 | Secondary relationship | enum | as above | Recommended |
| 4 | Secondary phone | string (E.164) | non-empty if name provided | |
| 5 | Secondary contact address | text | non-empty if name provided | |
| 6 | Medical conditions relevant to emergencies | text | free text | e.g., "Allergic to penicillin" |
| 7 | Known emergency treatment instructions | text | free text | e.g., "Carries EpiPen" |
| 8 | Blood group | enum | A+/A-/B+/B-/AB+/AB-/O+/O- | Optional; not used for employment decisions |
| 9 | Office/location specific emergency warden | ref | Facilities Lead ID | Auto-filled by HR |

## 4. Validation Rules

1. At least one emergency contact is mandatory; the primary contact block cannot be empty.
2. Primary phone must be different from the employee's own phone (rule 1 in [`../01-hr/emergency-contact-form.md`](../01-hr/emergency-contact-form.md)).
3. If a medical condition is declared, the form prompts for any known emergency treatment instructions (e.g., "Carries EpiPen").
4. Blood group is optional and recommended only; ACME does not use blood group for any employment decision.
5. Email field must be the corporate `@acme.example` email — personal emails are not accepted on this form (the form is submitted after IT provisioning completes).
6. Submission date must be on or before the employee's start date for preboarding submissions, or on the day of update for subsequent re-submissions.

## 5. Responsible Owner

- **Form owner (HR):** HRBP for the team.
  - Cloud / Workspace: Kavya Krishnan (`kavya.krishnan@acme.example`)
  - Intelligence / QE / Support: Deepika Rao (`deepika.rao@acme.example`)
  - Platform / Sales: Sanjay Patel (`sanjay.patel@acme.example`)
- **Backup:** Priya Nair, HR Onboarding Coordinator (`priya.nair@acme.example`).
- **Storage location:** ACME HR Hub (`hr.acme.example`, fictional endpoint) with `confidential` classification.
- **Access:** Restricted to HR Operations + office Facilities Lead + the office Emergency Warden. **Not** shared with the employee's manager by default; the manager is notified only in case of an actual emergency.
- **Retention:** Deleted 30 days after the employee's separation date (see [`../12-offboarding/employee-departure-checklist.md`](../12-offboarding/employee-departure-checklist.md)).

## 6. Approval Requirements (Workflow)

1. **HRBP review (mandatory).** The HRBP confirms:
   - All mandatory fields are present.
   - Primary phone differs from the employee's own phone.
   - At least one contact is reachable in the office's country (heuristic: phone country code matches office country, otherwise a note is added).
2. **No further approval required.** This form does not route to HR Director or VP HR — the HRBP's review is the final approval gate.
3. **Re-submission.** The employee may re-submit this form at any time (e.g., after marriage, after a parent's phone change). The new version supersedes the previous one; the previous version is retained in the HR Hub audit log.
4. **Annual reminder.** HR Operations sends a reminder once per year asking the employee to confirm the contacts are still current.

## 7. Sample Filled Values (Fictional)

```yaml
form_id: ACME-FORM-002
submission_id: ACME-2026-0488-EC-1
submitted_by: kavya.krishnan@acme.example
submitted_at: 2026-09-10T09:20:00+05:30
employee:
  name: Anika Rao
  employee_id: ACME-2026-0488
  corporate_email: anika.rao@acme.example
primary_contact:
  name: Sumith Rao
  relationship: Spouse
  phone: +91-9876509876
  secondary_phone: +91-80-2345-6789
  address: 14 Brigade Road, Bengaluru 560025
  language_preference: English / Kannada
secondary_contact:
  name: Lakshmi Rao
  relationship: Parent
  phone: +91-9876500001
  address: 22nd Main, Jayanagar, Bengaluru 560011
medical:
  conditions: Allergic to penicillin
  treatment_instructions: Carries EpiPen; inject intramuscular outer thigh
  blood_group: O+
approvals:
  hrbp_review:
    by: kavya.krishnan@acme.example
    decision: approved
    timestamp: 2026-09-10T10:05:00+05:30
```

## 8. Related Documents

- [`../01-hr/emergency-contact-form.md`](../01-hr/emergency-contact-form.md) — Companion HR-side form narrative.
- [`../01-hr/employee-information-form.md`](../01-hr/employee-information-form.md) — Linked via employee record.
- [`../03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md) — Privacy basis for storing emergency contact PII.
- [`../07-workflows/preboarding.md`](../07-workflows/preboarding.md) — Workflow context for this form.
- [`../07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) — Day 1 verification step.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — HRBP routing.
- [`../metadata/glossary.md`](../metadata/glossary.md) — E.164, PII definitions.
