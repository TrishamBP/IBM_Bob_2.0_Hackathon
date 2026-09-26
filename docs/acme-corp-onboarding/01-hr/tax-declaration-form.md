---
document_id: ACME-HR-007
title: ACME Corp Tax Declaration Form
category: hr
department: human-resources
applicable_roles: [all]
owner: Payroll
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, hr, tax, fictional]
---

# ACME Corp Tax Declaration Form

> **FICTIONAL EXAMPLE.** This form is a template for demonstration only. Tax rules vary by jurisdiction and change frequently. Any real tax filing requires review by a qualified tax professional and the relevant tax authority. ACME Corp is fictional.

## Purpose

This form captures the employee's tax declarations and deductions for payroll withholding purposes. It is part of [`07-workflows/preboarding.md`](../07-workflows/preboarding.md) and is updated annually or whenever the employee's tax situation changes.

## Submission

- **Owner:** Payroll Lead — Sanjay Patel (`sanjay.patel@acme.example`).
- **Channel:** ACME HR Hub → Payroll → Tax Declaration.
- **Deadline:** Before the first payroll cutoff (20th of the month for the following month's payroll in India).

## Mandatory Fields

| Field | Type | Validation | Sample (fictional) |
|-------|------|------------|--------------------|
| Employee name | string | non-empty | Anika Rao |
| Employee ID | string | matches HR system | ACME-2026-0488 |
| Tax year | string | YYYY–YYYY | 2026–2027 |
| Country of tax residency | string | ISO 3166 | India |
| Tax registration ID (PAN / SSN / NIN) | string | format per country | ABCDE1234F |
| Tax regime (India only) | enum | Old / New | New |
| Investment declarations (Section 80C, etc.) | numeric | ≥ 0 | 150000 |
| HRA exemption claimed (if applicable) | numeric | ≥ 0 | 60000 |
| Other deductions | numeric | ≥ 0 | 0 |
| Total deductions claimed | numeric | sum of above | 210000 |

## Validation Rules

1. Tax registration ID format is checked per country.
2. Total deductions cannot exceed statutory limits for the declared regime.
3. Supporting documents (investment receipts, rent receipts, etc.) must be uploaded as separate PDF attachments before the end of the financial year.
4. If the employee fails to submit investment proof by the deadline (typically January 31 for the Indian financial year), the provisional tax benefit is reversed in the February payroll.

## Approval

- **Payroll Lead:** validates form completeness.
- **Finance Director:** signs off on annual payroll tax filings.

## Sample Filled Form (Fictional, India)

```yaml
employee_name: Anika Rao
employee_id: ACME-2026-0488
tax_year: 2026-2027
country_of_tax_residency: India
tax_registration_id: ABCDE1234F
tax_regime: New
investment_declarations:
  section_80C: 150000
  section_80D: 25000
  section_80CCD1B: 50000
hra_exemption_claimed: 60000
other_deductions: 0
total_deductions_claimed: 285000
supporting_documents: [80c_proof.pdf, 80d_proof.pdf, rent_receipts.pdf]
```

## Disclaimer

Tax rules change. Employees should consult a qualified tax advisor for their specific situation. ACME does not provide tax advice.

## Related Documents

- [`01-hr/payroll-and-bank-information-form.md`](./payroll-and-bank-information-form.md)
- [`07-workflows/preboarding.md`](../07-workflows/preboarding.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
