---
document_id: ACME-HR-006
title: ACME Corp Payroll and Bank Information Form
category: hr
department: human-resources
applicable_roles: [all]
owner: Payroll
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, hr, payroll, bank, fictional]
---

# ACME Corp Payroll and Bank Information Form

> **FICTIONAL EXAMPLE.** This form is a template for demonstration only. Do not enter real bank account details. ACME Corp is fictional. Real payroll forms require review by qualified payroll and finance professionals for the relevant jurisdiction.

## Purpose

This form collects bank account information needed to disburse salary. It is part of [`07-workflows/preboarding.md`](../07-workflows/preboarding.md) and must be submitted before the first payroll cutoff (the 20th of the month for the following month's payroll in India).

## Submission

- **Owner:** Payroll Lead — Sanjay Patel (`sanjay.patel@acme.example`).
- **Channel:** ACME HR Hub → Payroll section.
- **Deadline:** 5 business days before the first payroll cutoff following the start date.

## Mandatory Fields

| Field | Type | Validation | Sample (fictional) |
|-------|------|------------|--------------------|
| Employee name | string | non-empty | Anika Rao |
| Employee corporate email | email | @acme.example | anika.rao@acme.example |
| Employee ID | string | matches HR system | ACME-2026-0488 |
| Bank name | string | non-empty | HDFC Bank |
| Bank branch | string | non-empty | MG Road, Bengaluru |
| Account holder name | string | matches employee legal name | Anika Rao |
| Account number | string | numeric, 9–18 digits | 5010000000123456 |
| Account type | enum | Savings / Current / NRE / NRO | Savings |
| IFSC / SWIFT / BSB / Routing code | string | format per country | HDFC0000123 |
| Currency | enum | INR / USD / GBP | INR |

## Validation Rules

1. Account holder name must match the legal name in [`01-hr/employee-information-form.md`](./employee-information-form.md).
2. Account number is checked for digit length per the country's bank standard.
3. IFSC / SWIFT / Routing code format is validated per country.
4. The form is rejected if any field is empty or fails validation — the new hire must resubmit.

## Approval

- **Payroll Lead review:** Confirms bank details and account holder name match.
- **Finance Director sign-off:** Required for international wire details (GBP / USD payroll).

## Privacy and Storage

- Bank information is stored in the HR system's encrypted payroll module.
- Access is restricted to Payroll team members and the Finance Director.
- Bank details are deleted 30 days after separation.

## Sample Filled Form (Fictional)

```yaml
employee_name: Anika Rao
employee_corporate_email: anika.rao@acme.example
employee_id: ACME-2026-0488
bank_name: HDFC Bank
bank_branch: MG Road, Bengaluru
account_holder_name: Anika Rao
account_number: 5010000000123456
account_type: Savings
ifsc_code: HDFC0000123
currency: INR
```

## Related Documents

- [`01-hr/employee-information-form.md`](./employee-information-form.md)
- [`01-hr/tax-declaration-form.md`](./tax-declaration-form.md)
- [`07-workflows/preboarding.md`](../07-workflows/preboarding.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
