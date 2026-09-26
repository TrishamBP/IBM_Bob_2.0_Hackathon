---
document_id: ACME-HR-004
title: ACME Corp Employee Information Form
category: hr
department: human-resources
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, hr, employee-data, fictional]
---

# ACME Corp Employee Information Form

> **FICTIONAL EXAMPLE.** This form is a template for demonstration. It does not constitute real-world tax, immigration, or employment advice. ACME Corp itself is fictional. Do not submit real personal information against this template.

## Purpose

This form collects basic employment information from a new hire before day one. It is completed as part of [`07-workflows/preboarding.md`](../07-workflows/preboarding.md) and submitted to the HRBP at least 3 business days before the start date.

## Submission

- **Owner:** HRBP for the team (see [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)).
- **Channel:** Submit through ACME HR Hub (`hr.acme.example`) or via email to your HRBP at `@acme.example`.
- **Deadline:** 3 business days before start date.

## Mandatory Fields

| Field | Type | Validation | Sample (fictional) |
|-------|------|------------|--------------------|
| Full legal name | string | non-empty, matches passport | Anika Rao |
| Preferred name | string | non-empty | Anika |
| Date of birth | date | YYYY-MM-DD, > 18 years old | 1994-05-12 |
| Gender (optional, self-identified) | enum | F / M / NB / prefer-not-to-say / other | F |
| Nationality | string | ISO 3166 country | Indian |
| Personal email | email | RFC 5322 | anika.rao@example.com |
| Phone | string | E.164 | +91-9876543210 |
| Current address | text | non-empty | 14 Brigade Road, Bengaluru 560025 |
| Permanent address | text | non-empty | (same as above) |
| Government ID type | enum | Passport / Aadhaar / PAN / SSN / NIN / BRP | PAN |
| Government ID number | string | format depends on ID type | ABCDE1234F |
| Job title | string | matches offer letter | Backend Engineer — Cloud API |
| Reports to | string | matches [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) | Anjali Desai |
| Office assignment | enum | Hyderabad / Bengaluru / London / Seattle / Remote | Bengaluru |
| Start date | date | YYYY-MM-DD | 2026-09-15 |
| Employment type | enum | Full-time / Part-time / Contract | Full-time |
| Probation end date | date | start date + 6 months | 2027-03-15 |

## Optional Fields

| Field | Type | Validation | Notes |
|-------|------|------------|-------|
| Pronouns | string | free text | Used in directory |
| LinkedIn URL | url | https | Optional |
| T-shirt size | enum | XS–XXL | For company swag |
| Dietary preferences | string | free text | For team lunches |
| Wheelchair / accessibility needs | text | free text | For office setup |
| Photo (for badge) | image | JPEG, ≥ 200×200 | Used only for corporate badge |

## Validation Rules

1. Personal email cannot be the same as the corporate email domain (the corporate email is issued after this form is submitted).
2. Government ID number is validated against the format for the declared ID type (this validation is fictional; real validation depends on jurisdiction).
3. Start date cannot be a public holiday in the office's country.
4. Reports-to field must match an active manager record in the HR system.

## Approval

- **HRBP review:** Confirms all mandatory fields are present and valid.
- **HR Director approval:** Required only if any field triggers a flag (e.g., start date on a public holiday, government ID format mismatch).

## What Happens Next

1. The HRBP enters the data into the HR system within 1 business day.
2. The HR system triggers an automated IT provisioning request — see [`02-it/new-employee-it-request.md`](../02-it/new-employee-it-request.md).
3. The new hire receives a confirmation email with the [`01-hr/welcome-letter.md`](./welcome-letter.md).

## Sample Filled Form (Fictional)

```yaml
full_legal_name: Anika Rao
preferred_name: Anika
date_of_birth: 1994-05-12
gender: F
nationality: Indian
personal_email: anika.rao@example.com
phone: +91-9876543210
current_address: 14 Brigade Road, Bengaluru 560025
permanent_address: 14 Brigade Road, Bengaluru 560025
government_id_type: PAN
government_id_number: ABCDE1234F
job_title: Backend Engineer — Cloud API
reports_to: Anjali Desai
office_assignment: Bengaluru
start_date: 2026-09-15
employment_type: Full-time
probation_end_date: 2027-03-15
pronouns: she/her
t_shirt_size: M
dietary_preferences: vegetarian
```

## Related Documents

- [`01-hr/welcome-letter.md`](./welcome-letter.md)
- [`01-hr/emergency-contact-form.md`](./emergency-contact-form.md)
- [`01-hr/payroll-and-bank-information-form.md`](./payroll-and-bank-information-form.md)
- [`07-workflows/preboarding.md`](../07-workflows/preboarding.md)
- [`08-forms/new-employee-information.md`](../08-forms/new-employee-information.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
