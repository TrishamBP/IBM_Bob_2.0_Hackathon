---
document_id: ACME-OFF-005
title: Final HR and Payroll Procedures
category: offboarding
department: human-resources
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [offboarding, payroll, final-settlement, benefits, gratuity, cobra]
---

# Final HR and Payroll Procedures

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. The payroll endpoints (`hr.acme.example`, `portal.acme.example`), bank account details, statutory reference numbers, and sample settlement worksheets below are illustrative. Statutory references (e.g., Payment of Gratuity Act 1972, COBRA, UK Pensions Act) are real legislation; ACME's fictional compliance posture is described for documentation purposes only.

## 1. Purpose

This document defines the **final settlement** and **benefits continuation** procedures for a departing ACME Corp employee. It is the operational complement to [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) §Final Settlement, and it is tracked as part of the [`./employee-departure-checklist.md`](./employee-departure-checklist.md) workflow (DEP-018, DEP-019, DEP-030, DEP-031, DEP-035). It also references [`../01-hr/payroll-and-bank-information-form.md`](../01-hr/payroll-and-bank-information-form.md) for the bank-account verification step.

This document is consistent with the access policies established in [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md), [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md), and [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md). Specifically:

- The final settlement is processed **within 30–45 days of the LWD**, depending on jurisdiction.
- Final settlement is conditioned on IT certification that no corporate device or access remains outstanding (per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §3.3 and [`./employee-departure-checklist.md`](./employee-departure-checklist.md) DEP-026).
- The settlement worksheet includes: salary through LWD, PTO encashment, pending reimbursements, bonus pro-rata, statutory gratuity (India), severance per individual agreement.
- Benefits continuation differs by jurisdiction (COBRA for US, statutory continuation for India, pension continuation for UK).

## 2. Owner and SLA

- **Process owner (joint):** Payroll Lead — Sanjay Patel (`sanjay.patel@acme.example`) — and Benefits Specialist — Rohit Sharma (`rohit.sharma@acme.example`).
- **Escalation:** VP HR — Ananya Sharma (`ananya.sharma@acme.example`); for Legal/contractual questions, Legal — Hemant Joshi (`hemant.joshi@acme.example`).
- **SLA:** Final settlement is processed within **30 business days (India)**, **30–45 business days (UK and US)**, of the LWD, conditioned on IT certification of complete equipment return and access revocation.
- **Benefits continuation:** Packets are dispatched **within 5 business days of the LWD** (per [`./employee-departure-checklist.md`](./employee-departure-checklist.md) DEP-031).

## 3. Settlement Components

The final settlement includes the following components. Each component is jurisdiction-sensitive; the table below shows the general applicability and the source policy.

| # | Component | Description | Jurisdiction | Source policy |
|---|-----------|-------------|--------------|---------------|
| 1 | Salary through LWD | Salary for all days worked through the LWD, including the LWD itself, prorated if the LWD is mid-pay-cycle | All | [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) §Final Settlement |
| 2 | PTO encashment | Accrued and unused paid time off, paid out at the employee's daily rate, per applicable law and the leave policy | All | [`../01-hr/leave-and-attendance-policy.md`](../01-hr/leave-and-attendance-policy.md) |
| 3 | Pending reimbursements | Approved expense reimbursements (travel, business expenses) not yet paid | All | [`../01-hr/payroll-and-bank-information-form.md`](../01-hr/payroll-and-bank-information-form.md) |
| 4 | Bonus pro-rata | Performance bonus or signing-bonus unvested portion, prorated per the bonus plan terms; clawback applies if the individual agreement requires it | All | [`../01-hr/sample-employment-agreement.md`](../01-hr/sample-employment-agreement.md) |
| 5 | Statutory gratuity | Gratuity under the Payment of Gratuity Act 1972 (India), for employees with ≥5 years of continuous service; calculated as 15 days of last-drawn wages for every completed year of service | India only | [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) §Final Settlement |
| 6 | Severance | Per individual agreement (separation agreement) or per role-elimination policy; not standard for voluntary resignation | All (per individual agreement) | [`../01-hr/sample-employment-agreement.md`](../01-hr/sample-employment-agreement.md) |
| 7 | Leave travel allowance encashment | Unused LTA, per Indian income-tax rules | India only | [`../01-hr/leave-and-attendance-policy.md`](../01-hr/leave-and-attendance-policy.md) |
| 8 | Pension contributions (employer) | Vested employer pension contributions, per UK Pensions Act | UK only | [`../01-hr/benefits-enrollment-form.md`](../01-hr/benefits-enrollment-form.md) |
| 9 | 401(k) employer match (vested portion) | Vested employer 401(k) match; per the plan's vesting schedule | US only | [`../01-hr/benefits-enrollment-form.md`](../01-hr/benefits-enrollment-form.md) |

## 4. Settlement Worksheet (Fictional Sample)

The Payroll Lead prepares a settlement worksheet per departing employee. The worksheet is filed in HR Hub (`hr.acme.example`, fictional) under the offboarding record. The fictional sample below shows the structure for an India-based employee (Anika Rao, Cloud API engineer) with a 4-year tenure — gratuity **does not apply** because the employee has fewer than 5 years of continuous service.

```yaml
settlement_id: ACME-2026-0488-FS
employee:
  name: Anika Rao
  employee_id: ACME-2026-0488
  jurisdiction: India
  last_working_day: 2026-10-15
  tenure_years: 4
components:
  salary_through_lwd:
    days_payable: 15  # half-month (pay-cycle end on LWD)
    daily_rate: INR 8500
    amount: INR 127500
  pto_encashment:
    accrued_days: 18
    daily_rate: INR 8500
    amount: INR 153000
  pending_reimbursements:
    items:
      - travel_oct_2026: INR 12400
      - business_phone_oct_2026: INR 3200
    total: INR 15600
  bonus_pro_rata:
    plan: annual_perf_2026
    eligible: false  # leaving before bonus-eligibility date per plan terms
    amount: INR 0
  statutory_gratuity:
    eligible: false  # tenure < 5 years
    amount: INR 0
  severance:
    eligible: false  # voluntary resignation; no individual separation agreement
    amount: INR 0
  lta_encashment:
    accrued_days: 4
    daily_rate: INR 8500
    amount: INR 34000
total_settlement: INR 330100  # salary + PTO + reimbursements + LTA
statutory_deductions:
  income_tax: INR 24750  # TDS on settlement per Indian income-tax rules
  provident_fund: INR 0  # PF settled separately by EPFO
net_payable: INR 305350
bank_account:
  on_file: yes  # per ../01-hr/payroll-and-bank-information-form.md
  verified_on: 2026-10-13
  last_four: 4521
payment_date: 2026-11-10  # 30 business days post-LWD per India SLA
it_certification:
  equipment_returned: yes  # per ./employee-departure-checklist.md DEP-026
  access_revoked: yes  # per ./repository-and-system-access-revocation.md
  certified_by: Geetha Iyer
  certified_on: 2026-10-15
benefits_continuation:
  type: statutory_continuation_india  # per §5
  dispatched_on: 2026-10-19
  acknowledged_on: 2026-10-25
```

## 5. Benefits Continuation

Benefits continuation is jurisdiction-specific. The Benefits Specialist prepares the continuation packet within 5 business days of the LWD and dispatches it to the employee.

### 5.1 United States — COBRA

For US-based employees, the Consolidated Omnibus Budget Reconciliation Act (COBRA) gives the departing employee (and their covered dependents) the right to continue their employer-sponsored health coverage for a limited period (typically 18 months for voluntary separation) at the employee's own cost plus a 2% administrative fee.

| Step | Owner | Timing |
|------|-------|--------|
| Generate COBRA election notice from the health-plan administrator's portal | Benefits Specialist (Rohit Sharma) | Within 5 business days of LWD |
| Mail the COBRA election notice to the employee's home address on file | Benefits Specialist | Within 5 business days of LWD |
| Employee returns the COBRA election form within 60 days of receipt | Employee | Per COBRA statutory timeline |
| Health-plan administrator activates continuation coverage upon receipt of the election form and first premium | Health-plan administrator | Within 45 days of election |
| Benefits Specialist confirms enrolment in HR Hub | Benefits Specialist | Within 5 business days of confirmation |

COBRA continuation is independent of the final settlement. The employee pays the full premium directly to the health-plan administrator; ACME only administers the election notice.

### 5.2 India — Statutory Continuation

For India-based employees, statutory continuation covers:

| Benefit | Continuation mechanism | Owner |
|---------|-------------------------|-------|
| Provident Fund (PF) | PF balance is settled by the Employees' Provident Fund Organisation (EPFO); the employee can withdraw the full balance or transfer to a new employer's PF account | Benefits Specialist generates the EPFO withdrawal/transfer form, dispatches to the employee |
| Gratuity (if eligible, ≥5 years) | Paid as a lump sum in the final settlement (see §3 component 5) | Payroll Lead |
| Health insurance (group mediclaim) | Group coverage ends on the LWD; the employee can convert to an individual policy with the same insurer at their own cost (continuation benefit per IRDAI rules) | Benefits Specialist provides the conversion form |
| Superannuation (if any) | Vested portion settled per the superannuation trust rules | Benefits Specialist |

### 5.3 United Kingdom — Pension Continuation

For UK-based employees, pension continuation covers:

| Benefit | Continuation mechanism | Owner |
|---------|-------------------------|-------|
| Workplace pension (employer + employee contributions) | Vested employer contributions remain with the employee; the employee can leave the pension invested, transfer to a new employer's scheme, or transfer to a personal pension (per UK Pensions Act and auto-enrolment rules) | Benefits Specialist provides the pension options statement |
| Statutory sick pay, holiday pay | Holiday pay for accrued unused leave is paid out in the final settlement (see §3 component 2) | Payroll Lead |
| Private health insurance (if offered) | Group coverage ends on the LWD; the employee can convert to an individual policy with the same insurer | Benefits Specialist provides the conversion form |

## 6. Bank Account Verification

Before the settlement is disbursed, the Payroll Lead verifies the employee's bank account on file per [`../01-hr/payroll-and-bank-information-form.md`](../01-hr/payroll-and-bank-information-form.md). If the employee wants the settlement paid to a different account (e.g., they have closed the account on file), the employee must submit a new payroll-and-bank-information-form before the LWD with documentary proof of the new account.

- Verification timing: **T-2 (two business days before the LWD)**.
- If verification fails (account closed, mismatched name), the settlement is held until the employee provides a corrected form; the 30–45 day SLA starts on the date the corrected form is received.
- The Payroll Lead records the verification status in the settlement worksheet (see §4 sample `bank_account` block).

## 7. Statutory Deductions and Tax

The settlement is subject to statutory deductions:

| Jurisdiction | Deductions | Owner |
|--------------|-----------|-------|
| India | TDS (tax deducted at source) on salary, PTO encashment, gratuity (per Indian income-tax rules); PF settled separately by EPFO | Payroll Lead |
| UK | PAYE (pay as you earn) income tax and National Insurance contributions on salary and holiday pay | Payroll Lead |
| US | Federal income tax, state income tax (where applicable), FICA (Social Security and Medicare) on salary and PTO payout | Payroll Lead |

The Payroll Lead calculates the deductions per the applicable tax year's rates and provides a payslip with each component itemized. The payslip is delivered to the employee via HR Hub (`hr.acme.example`, fictional) within 5 business days of payment.

## 8. IT Certification Gate

The final settlement is **conditioned on IT certification** that:

1. All corporate equipment (laptop, monitor, peripherals, Yubikey, badge) has been returned per [`./equipment-return.md`](./equipment-return.md) and reconciled against the original equipment-handover form.
2. All corporate access (Entra ID, GitHub Enterprise, Vault, VPN, Wi-Fi, SaaS apps) has been revoked per [`./repository-and-system-access-revocation.md`](./repository-and-system-access-revocation.md).
3. The IT portion of the offboarding ticket is marked `COMPLETED` (per [`./employee-departure-checklist.md`](./employee-departure-checklist.md) DEP-026).

If IT certification is incomplete at the SLA deadline (T+30 to T+45), the Payroll Lead:

- Pays out the **non-disputed** portion (typically salary through LWD + PTO encashment) on the SLA deadline.
- Holds the **disputed** portion (typically pending reimbursements, bonus pro-rata, severance) until IT certification is complete or until the HRBP and Legal approve a write-off.
- Documents the partial payment and the hold reason in the settlement worksheet.
- Notifies the HRBP and the employee of the partial payment.

This is consistent with [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) §Access Revocation, which conditions the final settlement on the access-revocation workflow's completion.

## 9. Status Tracking

All settlement subtasks are tracked in the ITSM offboarding ticket (`OFFBD-YYYY-NNNNNN`) and mirrored to the HR Hub offboarding record. Allowed statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

| Sub-task | Mapped DEP ID | Default status |
|----------|---------------|----------------|
| Settlement worksheet prepared | DEP-018 | NOT_STARTED |
| Bank account verification | DEP-018 | NOT_STARTED |
| Benefits continuation packet prepared | DEP-019 | NOT_STARTED |
| IT certification of equipment return + access revocation | DEP-026 | NOT_STARTED |
| Final settlement disbursed | DEP-030 | NOT_STARTED |
| Benefits continuation dispatched and enrolment confirmed | DEP-031 | NOT_STARTED |
| Payslip delivered to employee | DEP-030 | NOT_STARTED |
| Offboarding ticket closed (post-settlement) | DEP-035 | NOT_STARTED |

## 10. RACI Matrix

| Activity | R | A | C | I |
|----------|---|---|---|---|
| Trigger final settlement (HRIS state change) | HRBP | HR Operations | Payroll Lead | VP HR |
| Settlement worksheet preparation | Payroll Lead | Payroll Lead (Sanjay Patel) | HRBP | VP HR |
| Bank account verification | Payroll Lead | Payroll Lead | HRBP | VP HR |
| Statutory deduction calculation | Payroll Lead | Payroll Lead | Legal / Tax | VP HR |
| Benefits continuation packet preparation | Benefits Specialist | Benefits Specialist (Rohit Sharma) | HRBP | VP HR |
| COBRA / statutory continuation / pension continuation dispatch | Benefits Specialist | Benefits Specialist | HRBP | VP HR |
| IT certification of equipment return + access revocation | IT Onboarding | IT Manager Hyderabad | GRC Analyst | CISO |
| Final settlement disbursement | Payroll Lead | Payroll Lead | HRBP + Legal | VP HR |
| Payslip delivery | Payroll Lead | Payroll Lead | HRBP | VP HR |
| Offboarding ticket closeout | HRBP | HR Operations | Payroll Lead + IT Onboarding + Benefits Specialist | VP HR |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 11. Expected Outcomes

After this document:

- The Payroll Lead knows the settlement components, jurisdiction-specific rules, bank-account verification flow, and the IT certification gate.
- The Benefits Specialist knows the COBRA / statutory-continuation / pension-continuation dispatch flows.
- The HRBP knows when the settlement can be paid in partial form and when it must wait for full IT certification.
- The departing employee knows what to expect: a settlement within 30–45 days, a payslip with each component itemized, and a benefits continuation packet within 5 business days.

## 12. Troubleshooting

| Symptom | Likely cause | Resolution |
|---------|--------------|------------|
| Bank account verification fails (account closed) | Employee closed the account on file after the LWD | Payroll Lead holds the settlement until the employee submits a new payroll-and-bank-information-form with documentary proof; the SLA clock restarts on receipt |
| IT certification not complete at the SLA deadline | Equipment not returned, or SCIM de-provision failed | Payroll Lead disburses the non-disputed portion; holds the disputed portion; notifies HRBP and Legal; resolves per [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) §Final Settlement |
| Bonus pro-rata calculation disputed by the employee | Plan terms ambiguous | Payroll Lead refers to Legal (Hemant Joshi) for plan-term interpretation; resolution within 10 business days; settlement disbursed per Legal's interpretation |
| COBRA election notice returned undelivered | Employee's home address on file is incorrect | Benefits Specialist verifies the address with the HRBP; re-dispatches via certified mail; notifies the health-plan administrator of the delay |
| PF withdrawal form returned to ACME by the employee | Employee did not submit to EPFO directly | Benefits Specialist re-routes the form to the EPFO portal on the employee's behalf (with their written authorization) |
| Pension transfer request delayed by the receiving scheme | New employer's pension scheme is slow to acknowledge | Benefits Specialist escalates to the receiving scheme; provides the employee with the transfer reference number for their own follow-up |
| Severance calculation contested by Legal | Individual separation agreement terms disputed | Legal + VP HR review; resolution within 15 business days; settlement adjusted; employee notified in writing |

## 13. Related Documents

- HR: [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md), [`../01-hr/payroll-and-bank-information-form.md`](../01-hr/payroll-and-bank-information-form.md), [`../01-hr/benefits-enrollment-form.md`](../01-hr/benefits-enrollment-form.md), [`../01-hr/leave-and-attendance-policy.md`](../01-hr/leave-and-attendance-policy.md), [`../01-hr/sample-employment-agreement.md`](../01-hr/sample-employment-agreement.md), [`../01-hr/tax-declaration-form.md`](../01-hr/tax-declaration-form.md)
- IT: [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md), [`../02-it/device-acceptance-and-responsibility.md`](../02-it/device-acceptance-and-responsibility.md)
- Security: [`../03-security/confidentiality-agreement.md`](../03-security/confidentiality-agreement.md), [`../03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md)
- Workflows: [`../07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md)
- Forms: [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md), [`../08-forms/manager-approval.md`](../08-forms/manager-approval.md)
- Contacts: [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)
