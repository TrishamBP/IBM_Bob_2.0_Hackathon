---
document_id: ACME-FORM-009
title: Training Completion Form
category: form
department: human-resources
applicable_roles: [all]
owner: HR
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, hr, training, completion, compliance, learning]
---

# Training Completion Form

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. All employee names, IDs, scores, and assessor emails below are illustrative. Do not submit real personal information against this template.

## 1. Form Purpose

This form records completion of ACME Corp's mandatory training modules for an employee. It is the compliance record that the employee has completed the training required for their role, and is referenced during audits, access approvals (e.g., AI tool access requires AI training), and quarterly access reviews. The form is filled by the HRBP (or by L&D) once the LMS reports completion; it is also used to record in-person / live-training sessions that are not captured automatically by the LMS. See [`../07-workflows/security-training.md`](../07-workflows/security-training.md) for the training workflow context.

## 2. Mandatory Fields

| # | Field | Type | Validation | Sample (fictional) |
|---|-------|------|------------|--------------------|
| 1 | Employee name | string | non-empty | Anika Rao |
| 2 | Employee ID | string | `ACME-YYYY-NNNN` | ACME-2026-0488 |
| 3 | Employee corporate email | email | `@acme.example` | anika.rao@acme.example |
| 4 | Team / BU | enum | Cloud / Workspace / Intelligence / Platform / QE / Support / Sales | Cloud API |
| 5 | Training module | enum | company-orientation / security-awareness / privacy-awareness / engineering-orientation / git-and-repository-workflows / ai-coding-assistant-usage / cloud-platform-fundamentals / product-training / workplace-conduct | security-awareness |
| 6 | Completion date | date (YYYY-MM-DD) | today or earlier; ≥ start date | 2026-09-16 |
| 7 | Delivery mode | enum | online-self-paced / online-instructor-led / in-person | online-self-paced |
| 8 | Score (if assessed) | number | 0–100 (pass ≥ 80) | 92 |
| 9 | Pass/fail | enum | pass / fail | pass |
| 10 | Assessor name | string | non-empty (L&D, HRBP, or instructor) | Kavya Krishnan |
| 11 | Assessor corporate email | email | `@acme.example` | kavya.krishnan@acme.example |
| 12 | LMS record URL | url | https://hr.acme.example/lms/... | https://hr.acme.example/lms/records/ACME-LMS-2026-09-16-488 |

## 3. Optional Fields

| # | Field | Type | Validation | Notes |
|---|-------|------|------------|-------|
| 1 | Time spent (minutes) | integer | > 0 | For LMS reporting |
| 2 | Module version | string | matches LMS version | For audit trail |
| 3 | Re-training trigger | enum | annual-refresh / policy-change / failed-audit / role-change / other | If this is a re-training |
| 4 | Prior training record ID | string | matches HR Hub record | For audit trail continuity |
| 5 | Linked policy acknowledgement | string | ACME-FORM-008 ref | For policies that require paired training |
| 6 | Manager notification | boolean | true / false | If manager should be notified (default true for fail) |
| 7 | Comments | text | free text | Notes from assessor or employee |

## 4. Validation Rules

1. Training module must match the role's required-training list (per [`../10-training/security-awareness.md`](../10-training/security-awareness.md), [`../10-training/privacy-awareness.md`](../10-training/privacy-awareness.md), [`../10-training/git-and-repository-workflows.md`](../10-training/git-and-repository-workflows.md), [`../10-training/ai-coding-assistant-usage.md`](../10-training/ai-coding-assistant-usage.md), [`../10-training/workplace-conduct.md`](../10-training/workplace-conduct.md)).
2. If `score` is provided, `pass` is auto-calculated (`score ≥ 80 → pass`, else `fail`).
3. If `pass = fail`, the form routes to L&D for re-training scheduling within 5 business days.
4. Completion date cannot be earlier than the employee's start date.
5. `ai-coding-assistant-usage` module completion is a prerequisite for ACME-FORM-006 ([`./ai-coding-assistant-license-request.md`](./ai-coding-assistant-license-request.md)) — the AI tool seat request cannot be approved without this record on file.
6. `security-awareness` and `privacy-awareness` must be completed within 7 calendar days of the employee's start date (per [`../07-workflows/security-training.md`](../07-workflows/security-training.md)).
7. Annual refresh: every employee re-completes `security-awareness`, `privacy-awareness`, and `workplace-conduct` once per year; the form is re-filed with `re-training trigger = annual-refresh`.

## 5. Responsible Owner

- **Form owner (HR):** HRBP for the team.
  - Cloud / Workspace: Kavya Krishnan (`kavya.krishnan@acme.example`)
  - Intelligence / QE / Support: Deepika Rao (`deepika.rao@acme.example`)
  - Platform / Sales: Sanjay Patel (`sanjay.patel@acme.example`)
- **L&D owner (for LMS-sourced records):** Priya Nair, HR Onboarding Coordinator (`priya.nair@acme.example`).
- **Compliance owners (per module):**
  - `security-awareness` → CISO delegate Rajan Mehta (`rajan.mehta@acme.example`)
  - `privacy-awareness` → DPO (routed via HRBP)
  - `ai-coding-assistant-usage` → Director AI/ML Anitha Rajan (`anitha.rajan@acme.example`)
- **Storage location:** ACME HR Hub (`hr.acme.example`, fictional) with `confidential` classification.

## 6. Approval Requirements (Workflow)

1. **HRBP review (mandatory).** The HRBP confirms the LMS record matches the form (URL is valid, score matches, completion date is plausible). The HRBP counter-signs the form.
2. **L&D confirmation (for live-training modules).** For modules delivered in-person or instructor-led (e.g., `engineering-orientation`), the L&D owner (Priya Nair) confirms attendance and the score (if any).
3. **Compliance owner co-sign (conditional).** Required when:
   - Module is `security-awareness` and `pass = fail` — CISO delegate co-signs the re-training plan.
   - Module is `ai-coding-assistant-usage` and `pass = pass` — Director AI/ML (Anitha Rajan) co-signs to unlock ACME-FORM-006 eligibility.
4. **No manager approval required.** This form does not route to the engineering manager; the manager is notified (read-only) when the form is filed so they can plan the rest of the onboarding week.
5. **Routing outcome.** Filed form triggers:
   - HR Hub compliance record creation.
   - Downstream: the linked access form (e.g., ACME-FORM-006 for AI tools) becomes eligible.
   - Annual refresh reminder is queued for next year.
6. **Re-training on fail.** If `pass = fail`, L&D schedules a re-take within 5 business days; the original form is retained with `fail` and a new form is filed after the re-take.

## 7. Sample Filled Values (Fictional)

```yaml
form_id: ACME-FORM-009
submission_id: ACME-2026-0488-TR-1
submitted_at: 2026-09-16T17:30:00+05:30
employee:
  name: Anika Rao
  employee_id: ACME-2026-0488
  corporate_email: anika.rao@acme.example
  team: Cloud API
training:
  module: security-awareness
  completion_date: 2026-09-16
  delivery_mode: online-self-paced
  score: 92
  pass_fail: pass
  time_spent_minutes: 65
  module_version: sec-aware-v4.1
  lms_record_url: https://hr.acme.example/lms/records/ACME-LMS-2026-09-16-488
assessor:
  name: Kavya Krishnan
  email: kavya.krishnan@acme.example
approvals:
  hrbp_review:
    by: kavya.krishnan@acme.example
    decision: approved
    timestamp: 2026-09-16T17:35:00+05:30
  l_and_d_confirmation: not_required (online-self-paced module)
  compliance_co_sign: not_required (pass; not the AI module)
manager_notification:
  to: anjali.desai@acme.example
  sent_at: 2026-09-16T17:36:00+05:30
```

## 8. Related Documents

- [`../10-training/security-awareness.md`](../10-training/security-awareness.md) — Module reference.
- [`../10-training/privacy-awareness.md`](../10-training/privacy-awareness.md) — Module reference.
- [`../10-training/git-and-repository-workflows.md`](../10-training/git-and-repository-workflows.md) — Module reference.
- [`../10-training/ai-coding-assistant-usage.md`](../10-training/ai-coding-assistant-usage.md) — Module reference.
- [`../10-training/workplace-conduct.md`](../10-training/workplace-conduct.md) — Module reference.
- [`../07-workflows/security-training.md`](../07-workflows/security-training.md) — Workflow context.
- [`../07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md) — Week 1 training schedule.
- [`./policy-acknowledgement.md`](./policy-acknowledgement.md) — Companion acknowledgement form.
- [`./ai-coding-assistant-license-request.md`](./ai-coding-assistant-license-request.md) — Downstream access form (gated by AI training).
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — HRBP / L&D / compliance contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — LMS, PII definitions.
