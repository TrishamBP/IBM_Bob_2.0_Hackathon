---
document_id: ACME-FORM-001
title: New Employee Information Form
category: form
department: human-resources
applicable_roles: [all]
owner: HR
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, hr, onboarding, preboarding, employee-data]
---

# New Employee Information Form

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. This form is a template for demonstration only. Do not submit real personal information against this template. All employee names, IDs, and contact details below are illustrative.

## 1. Form Purpose

This form captures the core employment record for a new ACME Corp hire during the preboarding phase (see [`../07-workflows/preboarding.md`](../07-workflows/preboarding.md)). It is the primary input that drives HR system creation, payroll setup, IT provisioning (via [`../02-it/new-employee-it-request.md`](../02-it/new-employee-it-request.md)), and office assignment. The form is completed by the assigned HRBP from data the candidate supplied during the offer stage, and is reviewed with the new hire on day 1 for corrections.

The form supersedes the placeholder record in the HR system and is the source of truth for legal name, government ID, employment type, reporting line, and office assignment.

## 2. Mandatory Fields

| # | Field | Type | Validation | Sample (fictional) |
|---|-------|------|------------|--------------------|
| 1 | Legal full name | string | non-empty, matches passport/government ID | Anika Rao |
| 2 | Preferred name | string | non-empty, ≤ 30 chars | Anika |
| 3 | Date of birth | date (YYYY-MM-DD) | ≥ 18 years old at start date | 1994-05-12 |
| 4 | Nationality | string (ISO 3166 country) | non-empty | Indian |
| 5 | Personal email | email (RFC 5322) | non-empty, not `@acme.example` | anika.rao@example.com |
| 6 | Personal phone | string (E.164) | non-empty, unique in HR system | +91-9876543210 |
| 7 | Current address | text | non-empty | 14 Brigade Road, Bengaluru 560025 |
| 8 | Government ID type | enum | Passport / Aadhaar / PAN / NIN / BRP / SSN | PAN |
| 9 | Government ID number | string | format regex per ID type | ABCDE1234F |
| 10 | Job title | string | matches offer letter | Backend Engineer — Cloud API |
| 11 | Reports to (manager) | string (HR record match) | must match an active EM record | Anjali Desai |
| 12 | Office assignment | enum | Hyderabad / Bengaluru / London / Seattle / Remote | Bengaluru |
| 13 | Start date | date (YYYY-MM-DD) | not a public holiday in office country | 2026-09-15 |
| 14 | Employment type | enum | Full-time / Part-time / Contract | Full-time |
| 15 | Probation end date | date (YYYY-MM-DD) | start_date + 6 months (Full-time) | 2027-03-15 |

## 3. Optional Fields

| # | Field | Type | Validation | Notes |
|---|-------|------|------------|-------|
| 1 | Pronouns | string | free text | Used in directory and email signature |
| 2 | LinkedIn URL | url (https) | valid URL | For the team page |
| 3 | T-shirt size | enum (XS–XXL) | one of allowed set | For company swag kit |
| 4 | Dietary preferences | string | free text | Used for team lunches |
| 5 | Accessibility needs | text | free text | Routed to Facilities Lead |
| 6 | Photo (for badge) | image | JPEG/PNG, ≥ 200×200, ≤ 5 MB | Stored in HR system only |
| 7 | Emergency contact pointer | ref | points to ACME-FORM-002 | Linked, not duplicated |
| 8 | Payroll pointer | ref | points to payroll form | Linked, not duplicated |

## 4. Validation Rules

1. Personal email cannot be in the `acme.example` domain (corporate email is issued after this form is processed).
2. Government ID number must match the format regex for the declared ID type (e.g., PAN `^[A-Z]{5}[0-9]{4}[A-Z]{1}$`).
3. Start date cannot be a public holiday in the office assignment country — see [`../metadata/glossary.md`](../metadata/glossary.md) for region reference.
4. `reports_to` must resolve to an active Engineering Manager, Director, or VP record in the HR system.
5. Probation end date is auto-calculated as start_date + 6 months for Full-time; the field is read-only unless overridden with HR Director approval.
6. If employment type is `Contract`, probation end date is calculated as start_date + 3 months and the offer letter reference becomes mandatory.

## 5. Responsible Owner

- **Form owner (HR):** HRBP assigned to the new hire's team.
  - Cloud / Workspace BU: Kavya Krishnan (`kavya.krishnan@acme.example`)
  - Intelligence / QE / Support BU: Deepika Rao (`deepika.rao@acme.example`)
  - Platform / Sales BU: Sanjay Patel (`sanjay.patel@acme.example`)
- **Backup / escalation:** Priya Nair, HR Onboarding Coordinator (`priya.nair@acme.example`).
- **Final authority:** Ananya Sharma, VP HR (`ananya.sharma@acme.example`).
- **Submission channel:** ACME HR Hub at `hr.acme.example` (fictional endpoint) or email to the assigned HRBP.
- **Deadline:** At least 3 business days before the start date so IT provisioning can begin.

## 6. Approval Requirements (Workflow)

1. **HRBP review (mandatory).** The HRBP confirms all mandatory fields are present, validation rules pass, and the `reports_to` line is consistent with the offer letter and [`../01-hr/sample-employment-agreement.md`](../01-hr/sample-employment-agreement.md).
2. **HR Director approval (conditional).** Required only when:
   - Start date falls on a public holiday in the office country.
   - Government ID format fails validation and an exception is requested.
   - Probation end date is overridden from the default 6-month window.
   - Employment type is `Contract` and the duration exceeds 12 months.
3. **Routing.** Approved forms trigger:
   - HR system record creation (within 1 business day).
   - IT provisioning request — see [`../02-it/new-employee-it-request.md`](../02-it/new-employee-it-request.md).
   - Welcome email — see [`../01-hr/welcome-letter.md`](../01-hr/welcome-letter.md).
4. **Storage.** Form is stored in the HR Hub with `confidential` classification and access restricted to HR Operations + the assigned HRBP + the new hire's reporting manager (read-only).

## 7. Sample Filled Values (Fictional)

```yaml
form_id: ACME-FORM-001
submission_id: ACME-2026-0488
submitted_by: kavya.krishnan@acme.example
submitted_at: 2026-09-10T09:15:00+05:30
employee:
  legal_name: Anika Rao
  preferred_name: Anika
  date_of_birth: 1994-05-12
  nationality: Indian
  personal_email: anika.rao@example.com
  phone: +91-9876543210
  current_address: 14 Brigade Road, Bengaluru 560025
  government_id_type: PAN
  government_id_number: ABCDE1234F
employment:
  job_title: Backend Engineer — Cloud API
  reports_to: Anjali Desai
  office_assignment: Bengaluru
  start_date: 2026-09-15
  employment_type: Full-time
  probation_end_date: 2027-03-15
optional:
  pronouns: she/her
  t_shirt_size: M
  dietary_preferences: vegetarian
  accessibility_needs: none
approvals:
  hrbp_review:
    by: kavya.krishnan@acme.example
    decision: approved
    timestamp: 2026-09-10T10:02:00+05:30
  hr_director_approval: not_required
```

## 8. Related Documents

- [`../01-hr/employee-information-form.md`](../01-hr/employee-information-form.md) — Companion HR-side form (narrative + storage).
- [`../01-hr/welcome-letter.md`](../01-hr/welcome-letter.md) — Triggered after this form is approved.
- [`../01-hr/sample-employment-agreement.md`](../01-hr/sample-employment-agreement.md) — Offer letter source of truth for job title and start date.
- [`../02-it/new-employee-it-request.md`](../02-it/new-employee-it-request.md) — IT provisioning downstream consumer.
- [`../07-workflows/preboarding.md`](../07-workflows/preboarding.md) — Workflow context for this form.
- [`../07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) — Manager confirms `reports_to` line.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — HRBP routing.
- [`../metadata/glossary.md`](../metadata/glossary.md) — Field definitions.
