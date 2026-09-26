---
document_id: ACME-HR-005
title: ACME Corp Emergency Contact Form
category: hr
department: human-resources
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, hr, emergency, fictional]
---

# ACME Corp Emergency Contact Form

> **FICTIONAL EXAMPLE.** This form is for demonstration only. Do not submit real personal information against this template.

## Purpose

This form collects emergency contact information for the new hire. It is mandatory before the employee's first day on-site and is part of [`07-workflows/preboarding.md`](../07-workflows/preboarding.md). The information is used only in case of an emergency (medical, workplace incident, or natural disaster) involving the employee at an ACME office or during ACME-sponsored travel.

## Submission

- **Owner:** HRBP for the team.
- **Channel:** ACME HR Hub or HRBP email.
- **Deadline:** 3 business days before start date.

## Mandatory Fields

| Field | Type | Validation | Sample (fictional) |
|-------|------|------------|--------------------|
| Employee name | string | non-empty | Anika Rao |
| Employee corporate email | email | matches new corporate email | anika.rao@acme.example |
| Primary emergency contact name | string | non-empty | Sumith Rao |
| Relationship | enum | Parent / Spouse / Sibling / Partner / Guardian / Other | Spouse |
| Primary phone | string | E.164 | +91-9876509876 |
| Secondary phone (optional) | string | E.164 | +91-80-2345-6789 |
| Address | text | non-empty | 14 Brigade Road, Bengaluru 560025 |
| Language preference | string | non-empty | English / Kannada / Hindi |
| Medical conditions (optional, relevant to emergencies) | text | free text | Allergic to penicillin |
| Blood group (optional) | enum | A+/A-/B+/B-/AB+/AB-/O+/O- | O+ |

## Secondary Emergency Contact (Optional)

| Field | Type | Validation |
|-------|------|------------|
| Secondary contact name | string | non-empty |
| Relationship | enum | as above |
| Phone | string | E.164 |
| Address | text | non-empty |

## Validation Rules

1. At least one emergency contact is mandatory.
2. Primary phone must be a different number from the employee's own phone.
3. If the employee has declared a medical condition, the form prompts for any known emergency treatment instructions (e.g., "Carries EpiPen").
4. Blood group is optional but recommended; ACME does not require it for any employment decision.

## Privacy

- Emergency contact information is stored in the HR system with access restricted to HR Operations and the office Facilities Lead.
- It is not shared with the employee's manager by default. The manager is notified only in case of an emergency.
- The information is deleted 30 days after the employee's separation date.

## Sample Filled Form (Fictional)

```yaml
employee_name: Anika Rao
employee_corporate_email: anika.rao@acme.example
primary_contact:
  name: Sumith Rao
  relationship: Spouse
  phone: +91-9876509876
  address: 14 Brigade Road, Bengaluru 560025
  language_preference: English / Kannada
medical_conditions: Allergic to penicillin
blood_group: O+
secondary_contact:
  name: Lakshmi Rao
  relationship: Parent
  phone: +91-9876500001
  address: 22nd Main, Jayanagar, Bengaluru 560011
```

## Related Documents

- [`01-hr/employee-information-form.md`](./employee-information-form.md)
- [`07-workflows/preboarding.md`](../07-workflows/preboarding.md)
- [`08-forms/emergency-contact.md`](../08-forms/emergency-contact.md)
- [`03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md)
