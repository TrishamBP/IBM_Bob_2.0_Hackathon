---
document_id: ACME-FORM-008
title: Policy Acknowledgement Form
category: form
department: human-resources
applicable_roles: [all]
owner: HR
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, hr, security, policy, acknowledgement, signature, compliance]
---

# Policy Acknowledgement Form

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. All employee names, IDs, and signatures below are illustrative. Do not submit real personal information against this template.

## 1. Form Purpose

This form records the employee's signed acknowledgement of ACME Corp's core policies. It is completed on the employee's first day on-site (see [`../07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) and [`../07-workflows/policy-acknowledgement.md`](../07-workflows/policy-acknowledgement.md)) and re-acknowledged annually or when a policy materially changes. The form is the compliance record for the policies listed in §2 and is referenced during audits (see [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md)).

## 2. Mandatory Fields

| # | Field | Type | Validation | Sample (fictional) |
|---|-------|------|------------|--------------------|
| 1 | Employee name | string | non-empty | Anika Rao |
| 2 | Employee ID | string | `ACME-YYYY-NNNN` | ACME-2026-0488 |
| 3 | Employee corporate email | email | `@acme.example` | anika.rao@acme.example |
| 4 | Office assignment | enum | Hyderabad / Bengaluru / London / Seattle / Remote | Bengaluru |
| 5 | Acknowledgement date | date (YYYY-MM-DD) | today or earlier | 2026-09-15 |
| 6 | Policy list (multi-select) | enum (multi) | code-of-conduct / anti-harassment / information-security / acceptable-use / confidentiality / privacy / ai-tool-acceptable-use | code-of-conduct, anti-harassment, information-security, acceptable-use, confidentiality, privacy, ai-tool-acceptable-use |
| 7 | Acknowledgement statement | text | non-empty (pre-filled) | "I acknowledge that I have read, understood, and agree to comply with the policies listed above." |
| 8 | Employee signature | signature | captured in HR Hub | (signed) Anika Rao, 2026-09-15 |
| 9 | Witness (HRBP) name | string | matches HR record | Kavya Krishnan |
| 10 | Witness signature | signature | captured in HR Hub | (signed) Kavya Krishnan, 2026-09-15 |

## 3. Optional Fields

| # | Field | Type | Validation | Notes |
|---|-------|------|------------|-------|
| 1 | Policy version per policy | text | matches version field of each policy doc | Used to track which version was acknowledged |
| 2 | Re-acknowledgement trigger | enum | annual-review / policy-change / role-change / other | If this is a re-acknowledgement |
| 3 | Prior acknowledgement ID | string | matches HR Hub record | For audit trail continuity |
| 4 | Manager co-sign (role-change only) | signature | captured in HR Hub | Only if trigger = role-change |
| 5 | Comments | text | free text | Employee may note questions or concerns |
| 6 | Linked training records | text | ACME-FORM-009 refs | For policies that require paired training (e.g., AI tool acceptable use) |

## 4. Validation Rules

1. All seven policies in §2 must be acknowledged on the day-1 form. Partial acknowledgements are not accepted for the initial day-1 form; subsequent re-acknowledgements can be policy-specific (e.g., a single policy update).
2. Acknowledgement date must be on or after the employee's start date (for the initial form) and on or before the start date + 5 business days (grace window).
3. Both signatures (employee + HRBP witness) are mandatory. The form is `pending` until both are captured.
4. The `ai-tool-acceptable-use` policy acknowledgement must be paired with a completed AI tool acceptable use training record (see [`../10-training/ai-coding-assistant-usage.md`](../10-training/ai-coding-assistant-usage.md)) and the training-completion form ACME-FORM-009 ([`./training-completion.md`](./training-completion.md)).
5. The `confidentiality` policy acknowledgement triggers a separate signed NDA filed in the HR Hub (see [`../03-security/confidentiality-agreement.md`](../03-security/confidentiality-agreement.md)).
6. The acknowledgement statement text is pre-filled and cannot be edited by the employee. Edits are not allowed — the statement is the standard compliance text reviewed by Legal.

## 5. Responsible Owner

- **Form owner (HR):** HRBP for the team.
  - Cloud / Workspace: Kavya Krishnan (`kavya.krishnan@acme.example`)
  - Intelligence / QE / Support: Deepika Rao (`deepika.rao@acme.example`)
  - Platform / Sales: Sanjay Patel (`sanjay.patel@acme.example`)
- **Backup:** Priya Nair, HR Onboarding Coordinator (`priya.nair@acme.example`).
- **Compliance owner (for AI tool policy):** CISO delegate Rajan Mehta (`rajan.mehta@acme.example`).
- **Storage location:** ACME HR Hub (`hr.acme.example`, fictional) with `confidential` classification.
- **Retention:** 7 years after the employee's separation date, per ACME records retention policy.

## 6. Approval Requirements (Workflow)

1. **Employee signature (mandatory).** The employee signs the form in the HR Hub on day 1 after the HRBP has walked them through each policy. By signing, the employee confirms they have read, understood, and agree to comply with the policies listed.
2. **HRBP witness signature (mandatory).** The HRBP counter-signs the form to confirm they presented each policy and answered the employee's questions. The HRBP also confirms:
   - The employee has been given the policy documents (links in HR Hub).
   - The employee knows where to find the policies on the wiki at `wiki.acme.example` (simulated).
3. **No further approvals required** for the standard day-1 form.
4. **Manager co-sign (conditional).** Required only when the trigger is `role-change` (the employee is moving to a role with different policy applicability, e.g., moving into a role with prod-deploy access triggers re-acknowledgement of `least-privilege-access` and `source-code-security`).
5. **CISO co-sign (conditional).** Required only when the `ai-tool-acceptable-use` policy is being acknowledged for the first time and the employee's role is **not** in the default-entitled AI tool list (per [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md)). Rajan Mehta (`rajan.mehta@acme.example`) co-signs.
6. **Routing outcome.** Signed form triggers:
   - HR Hub record creation (compliance file).
   - Triggers downstream: access forms (ACME-FORM-003, -004, -005, -006) become eligible — most access forms require this acknowledgement on file.
   - The signed NDA filed separately (for the confidentiality policy).
7. **Annual re-acknowledgement.** HR Operations sends a reminder once per year asking the employee to re-acknowledge the full policy set. Re-acknowledgement uses the same form with `Re-acknowledgement trigger = annual-review`.

## 7. Sample Filled Values (Fictional)

```yaml
form_id: ACME-FORM-008
submission_id: ACME-2026-0488-ACK-1
submitted_at: 2026-09-15T15:00:00+05:30
employee:
  name: Anika Rao
  employee_id: ACME-2026-0488
  corporate_email: anika.rao@acme.example
  office_assignment: Bengaluru
acknowledgement:
  date: 2026-09-15
  policy_list:
    - code-of-conduct (v1.4)
    - anti-harassment (v2.1)
    - information-security (v3.0)
    - acceptable-use (v2.5)
    - confidentiality (v1.2)
    - privacy (v2.0)
    - ai-tool-acceptable-use (v1.1)
  statement: >-
    I acknowledge that I have read, understood, and agree to comply with
    the policies listed above.
  re_acknowledgement_trigger: initial-day-1
  linked_training_records:
    - ACME-FORM-009 ref ACME-2026-0488-TR-1 (security-awareness)
    - ACME-FORM-009 ref ACME-2026-0488-TR-2 (ai-coding-assistant-usage)
  comments: No questions; policies clear.
signatures:
  employee:
    name: Anika Rao
    signed_at: 2026-09-15T15:10:00+05:30
  hrbp_witness:
    name: Kavya Krishnan
    email: kavya.krishnan@acme.example
    signed_at: 2026-09-15T15:15:00+05:30
  ciso_co_sign: not_required (role is in default-entitled AI list)
```

## 8. Related Documents

- [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md) — Code of conduct.
- [`../01-hr/anti-harassment-policy.md`](../01-hr/anti-harassment-policy.md) — Anti-harassment.
- [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md) — Info security.
- [`../03-security/acceptable-use-policy.md`](../03-security/acceptable-use-policy.md) — Acceptable use.
- [`../03-security/confidentiality-agreement.md`](../03-security/confidentiality-agreement.md) — Confidentiality / NDA.
- [`../03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md) — Privacy.
- [`../03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) — AI tool use.
- [`../07-workflows/policy-acknowledgement.md`](../07-workflows/policy-acknowledgement.md) — Workflow context.
- [`../07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) — Day 1 context.
- [`./training-completion.md`](./training-completion.md) — Paired training record.
- [`./equipment-handover.md`](./equipment-handover.md) — Device acceptance record.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — HRBP routing.
