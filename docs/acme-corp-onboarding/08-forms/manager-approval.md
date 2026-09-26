---
document_id: ACME-FORM-010
title: Manager Approval Form
category: form
department: human-resources
applicable_roles: [all]
owner: HR
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, hr, manager, approval, sign-off, generic]
---

# Manager Approval Form

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. All employee names, IDs, manager emails, and reference IDs below are illustrative.

## 1. Form Purpose

This is a **generic** manager approval form used to capture a hiring Engineering Manager's (EM's) sign-off on any access, equipment, training, or role-change request that requires manager approval. It is the lightweight companion to ACME-FORM-003 through ACME-FORM-009 — those forms carry the request-specific data; this form carries the manager's decision (approve / reject / escalate), comments, signature, and date. The form exists because some requests arrive via email, chat, or external systems that don't carry a structured approval, and a uniform approval record is needed for audit. See [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md) and [`../07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) for workflow context.

## 2. Mandatory Fields

| # | Field | Type | Validation | Sample (fictional) |
|---|-------|------|------------|--------------------|
| 1 | Employee name | string | non-empty | Anika Rao |
| 2 | Employee ID | string | `ACME-YYYY-NNNN` | ACME-2026-0488 |
| 3 | Employee corporate email | email | `@acme.example` | anika.rao@acme.example |
| 4 | Manager name | string | matches HR EM record | Anjali Desai |
| 5 | Manager corporate email | email | `@acme.example` | anjali.desai@acme.example |
| 6 | Request type | enum | it-access / software-access / repository-access / ai-tool-license / equipment-handover / training / role-change / other | ai-tool-license |
| 7 | Request reference | string | matches sibling form's `submission_id` | ACME-2026-0488-AI-1 |
| 8 | Approval decision | enum | approve / reject / escalate | approve |
| 9 | Manager comments | text | ≥ 10 chars (decision rationale) | Approving AI tool seat for Anika; she's on the cloud-api backend team, default-entitled role. |
| 10 | Manager signature | signature | captured in HR Hub | (signed) Anjali Desai, 2026-09-11 |
| 11 | Approval date | date (YYYY-MM-DD) | today or earlier | 2026-09-11 |

## 3. Optional Fields

| # | Field | Type | Validation | Notes |
|---|-------|------|------------|-------|
| 1 | Escalation target | string | matches HR record | Required if decision = escalate |
| 2 | Escalation reason | text | ≥ 10 chars | Required if decision = escalate |
| 3 | Time-bound approval duration | integer (days) | 1–365 | If approval is time-bound (auto-expires) |
| 4 | Conditions | text | free text | e.g., "approved conditional on completing AI training within 7 days" |
| 5 | Counter-signer (escalated only) | string | matches HR record | Required if decision = escalate and the escalation requires counter-sign |
| 6 | Linked policy reference | string | ACME-FORM-008 ref | If the request touches a policy area |
| 7 | Cost center | string | finance record | For charge-back |

## 4. Validation Rules

1. `Request reference` must match an existing sibling form's `submission_id` (e.g., `ACME-2026-0488-AI-1` for an AI tool license request). If the reference does not resolve, the form is auto-rejected.
2. `Manager corporate email` must match the `reports_to` field on the employee's HR record. A manager who is not the employee's reporting line cannot approve on this form (they would need to escalate).
3. `Approval decision` must be one of `approve`, `reject`, `escalate`. Any other value is auto-rejected.
4. If `decision = escalate`, both `escalation_target` and `escalation_reason` are mandatory.
5. If `decision = reject`, `manager_comments` must be ≥ 30 chars (so the employee has actionable feedback).
6. If `time_bound_approval_duration` is provided, the approval auto-expires on `approval_date + duration`; downstream systems are notified to revoke access at that point.
7. The form cannot be self-approved — the manager and the employee must be different individuals.

## 5. Responsible Owner

- **Form owner (HR):** HRBP for the team (acts as the routing owner, not the approver).
  - Cloud / Workspace: Kavya Krishnan (`kavya.krishnan@acme.example`)
  - Intelligence / QE / Support: Deepika Rao (`deepika.rao@acme.example`)
  - Platform / Sales: Sanjay Patel (`sanjay.patel@acme.example`)
- **Approval owner (the EM):** The employee's direct manager (per [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)).
- **Storage location:** ACME HR Hub (`hr.acme.example`, fictional) with `confidential` classification.
- **Retention:** 7 years after the employee's separation date, per ACME records retention policy.

## 6. Approval Requirements (Workflow)

1. **Manager signature (mandatory).** This form **is** the manager's approval record — there is no further manager approval beyond this form.
2. **HRBP review (mandatory, record-keeping only).** The HRBP confirms the form is correctly linked to a sibling request (`request_reference` resolves) and routes the outcome back to the originating system. The HRBP does **not** approve or reject — they only confirm routing integrity.
3. **Escalation (conditional).** If `decision = escalate`, the form routes to the named `escalation_target` (e.g., Director AI/ML, CISO, VP IT). The escalation target completes a new ACME-FORM-010 with their own decision; that becomes the controlling approval.
4. **Counter-signer (conditional).** Required only when the original request's policy mandates a counter-sign (e.g., `ai-tool-license` for non-default-entitled roles requires Director AI/ML counter-sign per [`./ai-coding-assistant-license-request.md`](./ai-coding-assistant-license-request.md)).
5. **Time-bound auto-expiry.** If `time_bound_approval_duration` is set, the originating system (ITSM, LMS, GitHub Enterprise, etc.) is notified to revoke access at `approval_date + duration`. Revocation is logged per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md).
6. **Routing outcome.** Filed form triggers:
   - HR Hub record creation (audit trail).
   - Originating sibling form's `manager_approval` field is updated with the decision and timestamp.
   - If `decision = approve` and the sibling form's other approvals are complete, the sibling form moves to `provisioning`.

## 7. Sample Filled Values (Fictional)

```yaml
form_id: ACME-FORM-010
submission_id: ACME-2026-0488-APPROVAL-1
submitted_at: 2026-09-11T09:35:00+05:30
employee:
  name: Anika Rao
  employee_id: ACME-2026-0488
  corporate_email: anika.rao@acme.example
manager:
  name: Anjali Desai
  email: anjali.desai@acme.example
approval:
  request_type: ai-tool-license
  request_reference: ACME-2026-0488-AI-1
  decision: approve
  comments: >-
    Approving AI tool seat for Anika; she's on the cloud-api backend
    team, default-entitled role. CISO compliance check still required
    per AI tool acceptable use policy.
  conditions: Conditional on AI tool acceptable use training completion within 7 days.
  time_bound_approval_duration: null
signatures:
  manager:
    name: Anjali Desai
    signed_at: 2026-09-11T09:40:00+05:30
  approval_date: 2026-09-11
hrbp_review:
  by: kavya.krishnan@acme.example
  routing_confirmed: true
  timestamp: 2026-09-11T10:00:00+05:30
originating_form_update:
  sibling_form: ACME-FORM-006
  sibling_submission_id: ACME-2026-0488-AI-1
  field_updated: manager_approval
  updated_to: approved
  updated_at: 2026-09-11T10:00:00+05:30
```

## 8. Related Documents

- [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md) — Approval workflow.
- [`../07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) — Manager responsibilities.
- [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) — Auto-expiry / revocation.
- [`./it-access-request.md`](./it-access-request.md) — Sibling form (IT access).
- [`./software-access-request.md`](./software-access-request.md) — Sibling form (SaaS).
- [`./repository-access-request.md`](./repository-access-request.md) — Sibling form (repos).
- [`./ai-coding-assistant-license-request.md`](./ai-coding-assistant-license-request.md) — Sibling form (AI tool).
- [`./equipment-handover.md`](./equipment-handover.md) — Sibling form (equipment).
- [`./training-completion.md`](./training-completion.md) — Sibling form (training).
- [`./access-review.md`](./access-review.md) — Quarterly attestation.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Manager routing.
