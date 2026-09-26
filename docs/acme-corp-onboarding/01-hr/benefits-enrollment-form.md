---
document_id: ACME-HR-008
title: ACME Corp Benefits Enrollment Form
category: hr
department: human-resources
applicable_roles: [all]
owner: Benefits
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, hr, benefits, enrollment, fictional]
---

# ACME Corp Benefits Enrollment Form

> **FICTIONAL EXAMPLE.** Benefits offerings, premiums, and legal eligibility vary by jurisdiction and change over time. Real-world benefit enrollment requires review by qualified benefits and legal professionals. ACME Corp is fictional.

## Purpose

This form enrolls a new hire in ACME's standard benefits program. It is part of [`07-workflows/preboarding.md`](../07-workflows/preboarding.md) and must be submitted within 30 days of the start date to avoid waiting until the next open enrollment window.

## Submission

- **Owner:** Benefits Lead — Deepika Rao (`deepika.rao@acme.example`).
- **Channel:** ACME HR Hub → Benefits.
- **Deadline:** Within 30 days of start date.

## Benefits Program (Fictional)

| Plan | Coverage | Indicative Premium Share (employee) |
|------|----------|----------------------------------------|
| Health insurance — Employee + family (India) | INR 5,00,000 sum insured | 0% (employer-paid) |
| Health insurance — Employee + family (US) | PPO plan, $2,000 deductible | 20% of premium |
| Health insurance — Employee + family (UK) | Bupa private cover | 30% of premium |
| Dental and vision (US) | Standard plan | 20% of premium |
| Life insurance | 3× annual base salary | 0% (employer-paid) |
| Accidental death and dismemberment | 5× annual base salary | 0% (employer-paid) |
| Retirement — Provident Fund (India) | 12% employee + 12% employer | Statutory |
| Retirement — 401(k) (US) | 6% employer match | Employee optional |
| Retirement — Workplace pension (UK) | 5% employer, 4% employee | Statutory |
| Parental leave — Primary caregiver | 26 weeks paid | — |
| Parental leave — Secondary caregiver | 12 weeks paid | — |
| Mental wellness program | 12 sessions per year | 0% (employer-paid) |
| Learning budget | INR 50,000 / USD 1,500 / GBP 1,000 per year | — |

## Mandatory Fields

| Field | Type | Validation |
|-------|------|------------|
| Employee name | string | non-empty |
| Employee ID | string | matches HR system |
| Country of employment | enum | India / US / UK |
| Health plan selection | enum | Yes — Employee / Yes — Family / Decline |
| Dependent names and DOBs (if family) | text | per dependent |
| Life insurance beneficiary | string | non-empty |
| AD&D beneficiary | string | non-empty |
| Retirement plan participation | enum | Yes / No |
| Retirement contribution % | numeric | 0–50 (per plan limits) |
| Acknowledgement | boolean | true |

## Validation Rules

1. If health plan is "Yes — Family," dependent records must be completed.
2. Beneficiary names must be at least one full name (first and last).
3. Retirement contribution % is capped per statutory and plan limits.

## Approval

- **Benefits Lead review:** validates form completeness.
- **Benefits Director sign-off:** Required for non-standard requests (e.g., mid-year enrollment outside the 30-day window).

## Sample Filled Form (Fictional)

```yaml
employee_name: Anika Rao
employee_id: ACME-2026-0488
country_of_employment: India
health_plan: Yes — Family
dependents:
  - name: Sumith Rao
    relationship: Spouse
    date_of_birth: 1990-08-22
  - name: Aarav Rao
    relationship: Child
    date_of_birth: 2020-04-18
life_insurance_beneficiary: Sumith Rao
ad_and_d_beneficiary: Sumith Rao
retirement_plan: Yes
retirement_contribution_percent: 12
acknowledgement: true
```

## Related Documents

- [`01-hr/employee-information-form.md`](./employee-information-form.md)
- [`01-hr/payroll-and-bank-information-form.md`](./payroll-and-bank-information-form.md)
- [`07-workflows/preboarding.md`](../07-workflows/preboarding.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
