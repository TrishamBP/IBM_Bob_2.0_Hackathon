---
document_id: ACME-FORM-006
title: AI Coding Assistant License Request Form
category: form
department: it-operations
applicable_roles: [engineer, ai-ml-engineer, ai-research-engineer, cloud-platform-engineer, devops-engineer, qe, full-stack-engineer, backend-engineer, frontend-engineer, em, product-manager]
owner: IT
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, it, ai, github-copilot, license, ai-tool-acceptable-use, compliance]
---

# AI Coding Assistant License Request Form

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. The GitHub Copilot Business tenant, the internal sandbox "ACME Intelligence Sandbox," and the ITSM endpoint `helpdesk.acme.example` are simulated for documentation. Real product names (GitHub Copilot) are referenced by their real names; ACME-specific configuration details are fictional.

## 1. Form Purpose

This form is used by a hiring Engineering Manager (EM) to request a GitHub Copilot Business seat for a new hire, or by an engineer to request an AI coding assistant seat for themselves. It also handles requests for access to the internal "ACME Intelligence Sandbox" — a fictional internal LLM playground used for prompt experimentation. The form enforces the AI tool acceptable use policy at [`../03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) and is the prerequisite for the AI coding assistant setup documented at [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md). CISO sign-off is **always** required — even for default-entitled roles — to confirm the AI tool compliance check has passed.

## 2. Mandatory Fields

| # | Field | Type | Validation | Sample (fictional) |
|---|-------|------|------------|--------------------|
| 1 | Employee name | string | non-empty | Anika Rao |
| 2 | Employee ID | string | `ACME-YYYY-NNNN` | ACME-2026-0488 |
| 3 | Employee corporate email | email | `@acme.example` | anika.rao@acme.example |
| 4 | Role / job title | string | matches HR record | Backend Engineer — Cloud API |
| 5 | Team / BU | enum | Cloud / Workspace / Intelligence / Platform / QE | Cloud API |
| 6 | Hiring manager / requester | string | matches HR EM record | Anjali Desai |
| 7 | Manager corporate email | email | `@acme.example` | anjali.desai@acme.example |
| 8 | Requested AI tool | enum | GitHub Copilot Business / ACME Intelligence Sandbox / Both | GitHub Copilot Business |
| 9 | Justification | text | ≥ 30 chars | Engineer on cloud-api backend; Copilot Business is default-entitled for role per [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md) |
| 10 | Duration | enum | standing (until revoked) / time-bound (date range) | standing |
| 11 | AI tool acceptable use acknowledgement | boolean | true | true |
| 12 | Requested by | string | corporate email | anjali.desai@acme.example |

## 3. Optional Fields

| # | Field | Type | Validation | Notes |
|---|-------|------|------------|-------|
| 1 | Time-bound start date | date (YYYY-MM-DD) | today or future | Required if Duration = time-bound |
| 2 | Time-bound end date | date (YYYY-MM-DD) | > start | Required if Duration = time-bound |
| 3 | Use case category | enum | code-completion / test-generation / doc-generation / refactoring / prompt-prototyping / other | Helps the AI/ML team track usage patterns |
| 4 | Sandbox project name | string | matches sandbox registry | Required if tool = ACME Intelligence Sandbox |
| 5 | Data classification touched | enum | public / internal / confidential / restricted | See [`../03-security/data-classification.md`](../03-security/data-classification.md). Restricted requires CISO escalation. |
| 6 | Cost center | string | finance record | For license charge-back |
| 7 | Prior seat ID (for renewal / changes) | string | matches seat registry | If updating an existing seat |

## 4. Validation Rules

1. Requested AI tool must be one of: `GitHub Copilot Business`, `ACME Intelligence Sandbox`, or `Both`. Any other value is auto-rejected.
2. The employee must have acknowledged the AI tool acceptable use policy (`acknowledgement = true`). The acknowledgement is also recorded separately on ACME-FORM-008 ([`./policy-acknowledgement.md`](./policy-acknowledgement.md)) — see [`../07-workflows/policy-acknowledgement.md`](../07-workflows/policy-acknowledgement.md)).
3. If the role is in the default-entitled list (per [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md)), the hiring EM approval is automatic — the submission itself is the approval. Default-entitled roles include: Backend Engineer, Frontend Engineer, Full-Stack Engineer, Cloud Platform Engineer, DevOps Engineer, AI/ML Engineer, AI Research Engineer, Quality Engineer, Engineering Manager, Director AI/ML.
4. If the role is **not** in the default-entitled list (e.g., Product Manager, Sales Engineer), the form requires an additional Director AI/ML approval — Anitha Rajan (`anitha.rajan@acme.example`).
5. If `data_classification_touched = restricted`, the form is auto-escalated to the CISO delegate (Rajan Mehta, `rajan.mehta@acme.example`) and the request is held until reviewed.
6. If `tool = ACME Intelligence Sandbox`, a `sandbox_project_name` is mandatory and must match the project registry maintained by the AI/ML team.
7. `Duration = time-bound` requires both start and end dates; the seat is auto-revoked on the end date.

## 5. Responsible Owner

- **Form owner (IT):** IT Onboarding Specialist — Geetha Iyer (`geetha.iyer@acme.example`).
- **Director AI/ML (non-default-entitled roles):** Anitha Rajan (`anitha.rajan@acme.example`).
- **CISO (always required):** Rajan Mehta (`rajan.mehta@acme.example`).
- **GRC Analyst (supporting):** Karthik Subramanian (`karthik.subramanian@acme.example`) — assists with the compliance check record.
- **Submission channel:** ITSM portal `https://helpdesk.acme.example` (simulated) or email `helpdesk@acme.example`.
- **SLA:** 2 business days for default-entitled roles; 4 business days for non-default-entitled roles (Director AI/ML review).

## 6. Approval Requirements (Workflow)

1. **Hiring EM (auto for default-entitled roles).** When the form is submitted by the hiring EM for a default-entitled role (per [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md)), approval is **automatic** — the hiring EM's submission is itself the approval. For non-default-entitled roles, the hiring EM approval is still required but a separate Director AI/ML approval is added.
2. **Director AI/ML (conditional).** Required when the role is **not** in the default-entitled list. Anitha Rajan (`anitha.rajan@acme.example`) confirms the business case for the AI seat.
3. **CISO (always required).** Rajan Mehta (`rajan.mehta@acme.example`) confirms the AI tool compliance check has passed — per [`../03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md). This check is mandatory for **every** seat grant, including default-entitled roles, to ensure:
   - The employee has completed the AI tool acceptable use training ([`../10-training/ai-coding-assistant-usage.md`](../10-training/ai-coding-assistant-usage.md)).
   - The acknowledgement on ACME-FORM-008 is on file.
   - The data classification the employee will touch is compatible with AI tool usage.
4. **GRC Analyst (supporting record).** Karthik Subramanian (`karthik.subramanian@acme.example`) appends the compliance check record to the form. Not a blocking approval, but a record-keeping step.
5. **Routing outcome.** Approved form triggers:
   - **GitHub Copilot Business:** seat assignment via the ACME GitHub Enterprise org at `git.acme.example` (simulated) within 1 business day.
   - **ACME Intelligence Sandbox:** project role assignment via the sandbox admin console within 2 business days.
   - Welcome email to the employee with the setup guide at [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md).
6. **Quarterly review.** All AI tool seats are added to the next quarterly access review (ACME-FORM-012, [`./access-review.md`](./access-review.md)).

## 7. Sample Filled Values (Fictional)

```yaml
form_id: ACME-FORM-006
submission_id: ACME-2026-0488-AI-1
submitted_at: 2026-09-11T09:30:00+05:30
employee:
  name: Anika Rao
  employee_id: ACME-2026-0488
  corporate_email: anika.rao@acme.example
  role: Backend Engineer — Cloud API
  team: Cloud API
requester:
  name: Anjali Desai
  email: anjali.desai@acme.example
request:
  ai_tool: GitHub Copilot Business
  duration: standing
  justification: >-
    Engineer on cloud-api backend; Copilot Business is default-entitled
    for the Backend Engineer role per ai-coding-assistant-setup.md.
  use_case_category: code-completion
  data_classification_touched: internal
  ai_tool_acceptable_use_acknowledgement: true
requested_by: anjali.desai@acme.example
approvals:
  hiring_em:
    by: anjali.desai@acme.example
    decision: approved (auto — default-entitled role)
    timestamp: 2026-09-11T09:30:00+05:30
  director_ai_ml: not_required (default-entitled role)
  ciso:
    by: rajan.mehta@acme.example
    decision: approved
    timestamp: 2026-09-11T15:45:00+05:30
    notes: >-
      Employee completed AI tool acceptable use training on 2026-09-11;
      acknowledgement on file (ACME-FORM-008 ref ACME-2026-0488-ACK-1);
      data classification internal compatible.
  grc_record:
    by: karthik.subramanian@acme.example
    timestamp: 2026-09-11T16:00:00+05:30
provisioning:
  method: GitHub Enterprise org seat assignment
  completed_at: 2026-09-14T10:15:00+05:30
```

## 8. Related Documents

- [`../03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) — Governing policy.
- [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md) — Setup guide and default-entitlement list.
- [`../10-training/ai-coding-assistant-usage.md`](../10-training/ai-coding-assistant-usage.md) — Required training.
- [`../03-security/data-classification.md`](../03-security/data-classification.md) — Data classification touchpoints.
- [`../07-workflows/it-provisioning.md`](../07-workflows/it-provisioning.md) — Workflow context.
- [`./it-access-request.md`](./it-access-request.md) — Sibling form (general IT kit).
- [`./policy-acknowledgement.md`](./policy-acknowledgement.md) — Acknowledgement record (ACME-FORM-008).
- [`./manager-approval.md`](./manager-approval.md) — Manager sign-off record.
- [`./access-review.md`](./access-review.md) — Quarterly attestation.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Routing contacts.
