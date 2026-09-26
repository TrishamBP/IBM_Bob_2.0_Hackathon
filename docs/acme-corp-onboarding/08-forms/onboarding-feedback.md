---
document_id: ACME-FORM-011
title: Onboarding Feedback Form
category: form
department: human-resources
applicable_roles: [all]
owner: HR
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, hr, feedback, onboarding, anonymous, day-1, week-1, day-30, day-60, day-90]
---

# Onboarding Feedback Form

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. All survey responses and submission IDs below are illustrative. The form is intentionally **anonymous** to encourage candid feedback; any name fields in samples are illustrative only and would not be collected in production.

## 1. Form Purpose

This form captures the new hire's feedback on the onboarding experience at five milestones: end of day 1, end of week 1, day 30, day 60, and day 90 (see [`../07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md), [`../07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md), [`../07-workflows/first-30-days.md`](../07-workflows/first-30-days.md), [`../07-workflows/first-60-days.md`](../07-workflows/first-60-days.md), and [`../07-workflows/first-90-days.md`](../07-workflows/first-90-days.md)). The feedback is aggregated by HR Operations to identify onboarding gaps, measure onboarding health, and feed continuous improvement. Submission is **optional** and **anonymous** (employee ID is captured only for milestone tracking, not for individual identification in reports).

## 2. Mandatory Fields

| # | Field | Type | Validation | Sample (fictional) |
|---|-------|------|------------|--------------------|
| 1 | Feedback stage | enum | day-1 / week-1 / day-30 / day-60 / day-90 | day-1 |
| 2 | Submission date | date (YYYY-MM-DD) | today or earlier; matches stage window | 2026-09-15 |
| 3 | Overall rating | integer | 1–5 (1 = very poor, 5 = excellent) | 4 |
| 4 | What went well | text | ≥ 20 chars | Laptop was ready and configured; HRBP walk-through was clear; GitHub Enterprise access worked on first try. |
| 5 | What could be improved | text | ≥ 20 chars | The Microsoft Authenticator enrollment had to be done twice because the QR code expired mid-setup. |
| 6 | Anonymous submission flag | boolean | true / false (default true) | true |

## 3. Optional Fields

| # | Field | Type | Validation | Notes |
|---|-------|------|------------|-------|
| 1 | Employee ID (hashed) | string | SHA-256 hash of `ACME-YYYY-NNNN` | Used **only** for milestone deduplication; not visible in reports |
| 2 | Team / BU | enum | Cloud / Workspace / Intelligence / Platform / QE / Support / Sales | Helps segment reports; default `prefer-not-to-say` |
| 3 | Office assignment | enum | Hyderabad / Bengaluru / London / Seattle / Remote | Helps segment reports |
| 4 | Specific workflow ratings | multi-int (1–5 each) | preboarding / it-provisioning / first-day / security-training / access-approval / equipment-handover / policy-acknowledgement | Granular ratings |
| 5 | Specific contact ratings | multi-int (1–5 each) | hrbp / it-onboarding-specialist / hiring-em / buddy | Granular ratings |
| 6 | NPS-style question | integer | 0–10 ("How likely are you to recommend ACME as a place to work?") | Net Promoter Score style |
| 7 | Additional comments | text | free text | Catch-all |
| 8 | Permission to follow up (non-anonymous) | boolean | true / false | If true, employee's name is captured for HR Operations follow-up |

## 4. Validation Rules

1. `Feedback stage` must be one of the five allowed values. Any other value is auto-rejected.
2. `Submission date` must fall within the stage's reporting window:
   - `day-1`: start date through start date + 2 business days.
   - `week-1`: start date + 3 business days through start date + 10 business days.
   - `day-30`: day 28 through day 35.
   - `day-60`: day 55 through day 65.
   - `day-90`: day 85 through day 95.
3. Overall rating must be an integer 1–5; non-integer or out-of-range is auto-rejected.
4. If `Anonymous submission flag = true` (default), no name field is collected. If `false`, the form prompts for `Permission to follow up` and captures the employee's name from the HR Hub session.
5. The hashed employee ID is the only identifier stored for anonymous submissions. The hash is salted with a per-stage salt to prevent cross-stage linking in reports (cross-stage linking is done only by HR Operations for the milestone deduplication report, and the linking is one-way).
6. Free-text fields are scanned for PII (email addresses, phone numbers) before storage; detected PII is masked with `[REDACTED]` to protect the employee's anonymity.
7. Each stage can be submitted only once per employee (enforced via the hashed ID); re-submissions replace the previous submission for that stage.

## 5. Responsible Owner

- **Form owner (HR):** HR Operations (routed via Priya Nair, HR Onboarding Coordinator, `priya.nair@acme.example`).
- **Aggregate reviewer:** VP HR — Ananya Sharma (`ananya.sharma@acme.example`) reviews the quarterly aggregate report.
- **No individual approver.** This form has **no individual approval** — submissions are accepted as-is and aggregated. HR Operations produces a monthly aggregate report and a quarterly board-level summary.
- **Storage location:** ACME HR Hub (`hr.acme.example`, fictional) with `confidential` classification (because the aggregate could become identifiable in small teams).
- **Retention:** Raw submissions retained 2 years; aggregate reports retained 7 years.

## 6. Approval Requirements (Workflow)

1. **No individual approval required.** This form is **not** routed for approval — submissions are accepted as-is.
2. **HR Operations aggregate review (monthly).** Priya Nair compiles the monthly aggregate report:
   - Response rate per stage (target: ≥ 70%).
   - Average overall rating per stage (target: ≥ 4.0).
   - Top three "what went well" themes (auto-clustered).
   - Top three "what could be improved" themes (auto-clustered).
   - Office-segmented and BU-segmented views.
3. **Quarterly board summary.** Ananya Sharma (VP HR) reviews the quarterly summary and presents action items to the executive team. Themes that recur across two consecutive quarters are escalated to a process owner (e.g., IT Onboarding Specialist for IT provisioning themes).
4. **Anonymity protection.** No individual feedback is shared with the employee's manager. Only aggregate, de-identified insights leave the HR Operations team.
5. **Follow-up opt-in.** If an employee opts in to follow-up (`Permission to follow up = true`), HR Operations contacts them within 5 business days to discuss the feedback in person. The conversation notes are stored separately and are not linked back to the original submission in reports.
6. **Routing outcome.** Filed form triggers:
   - HR Hub compliance record creation (anonymous).
   - The monthly aggregate report is queued for the next cycle.
   - If a feedback comment references a critical safety, harassment, or security issue, an automated classifier flags the submission for HR Operations review (still anonymous) and Priya Nair decides whether to escalate per [`../01-hr/employee-grievance-procedure.md`](../01-hr/employee-grievance-procedure.md).

## 7. Sample Filled Values (Fictional)

```yaml
form_id: ACME-FORM-011
submission_id: ACME-FB-2026-09-15-0488  # illustrative only; not stored in reports
submitted_at: 2026-09-15T17:00:00+05:30
feedback:
  stage: day-1
  submission_date: 2026-09-15
  overall_rating: 4
  what_went_well: >-
    Laptop was ready and configured; HRBP walk-through was clear; GitHub
    Enterprise access worked on first try.
  what_could_be_improved: >-
    The Microsoft Authenticator enrollment had to be done twice because
    the QR code expired mid-setup.
  anonymous: true
optional:
  employee_id_hash: 9f2c1a8b7e6d5c4b3a2f1e0d9c8b7a6f5e4d3c2b1a0f9e8d7c6b5a4f3e2d1c0
  team: Cloud
  office: Bengaluru
  workflow_ratings:
    preboarding: 5
    it-provisioning: 4
    first-day: 4
    security-training: null  # not yet completed
    access-approval: 4
    equipment-handover: 5
    policy-acknowledgement: 4
  contact_ratings:
    hrbp: 5
    it-onboarding-specialist: 4
    hiring-em: 5
    buddy: 4
  nps: 9
  additional_comments: Buddy was great — would recommend pairing every new hire with one.
  permission_to_follow_up: false
approvals:
  individual_approval: not_required
  hr_operations_aggregate_review:
    by: priya.nair@acme.example
    cycle: 2026-09
    timestamp: 2026-10-05T11:00:00+05:30
```

## 8. Related Documents

- [`../07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) — Day 1 context.
- [`../07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md) — Week 1 context.
- [`../07-workflows/first-30-days.md`](../07-workflows/first-30-days.md) — Day 30 context.
- [`../07-workflows/first-60-days.md`](../07-workflows/first-60-days.md) — Day 60 context.
- [`../07-workflows/first-90-days.md`](../07-workflows/first-90-days.md) — Day 90 context.
- [`../07-workflows/onboarding-completion.md`](../07-workflows/onboarding-completion.md) — Completion context.
- [`../01-hr/employee-grievance-procedure.md`](../01-hr/employee-grievance-procedure.md) — Escalation path for flagged submissions.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — HR Operations routing.
- [`../metadata/glossary.md`](../metadata/glossary.md) — NPS, PII definitions.
