---
document_id: ACME-FORM-004
title: Software Access Request Form
category: form
department: it-operations
applicable_roles: [all]
owner: IT
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, it, software, saas, access, least-privilege]
---

# Software Access Request Form

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. Hostnames like `vault.acme.example`, `packages.acme.example`, `git.acme.example`, `helpdesk.acme.example` are simulated for documentation. Real product names (Datadog, Jira, Confluence, Salesforce, GitHub Enterprise, Figma, Notion, Looker) are referenced by their real names but ACME-specific integration details are fictional.

## 1. Form Purpose

This form is used by an ACME Corp employee to request access to **non-default** software that is not auto-provisioned by their role bundle. Typical examples: Datadog admin, Jira admin, GitHub Enterprise org admin, Salesforce admin, Vault (secrets), AWS / Azure / GCP prod roles, Looker, Figma editor. It complements ACME-FORM-003 ([`./it-access-request.md`](./it-access-request.md)) which is used for the standard new-hire kit. The form enforces the least-privilege principle documented in [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) and feeds the access-approval workflow at [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md).

## 2. Mandatory Fields

| # | Field | Type | Validation | Sample (fictional) |
|---|-------|------|------------|--------------------|
| 1 | Employee name | string | non-empty | Anika Rao |
| 2 | Employee ID | string | `ACME-YYYY-NNNN` | ACME-2026-0488 |
| 3 | Employee corporate email | email | `@acme.example` | anika.rao@acme.example |
| 4 | Team / BU | enum | Cloud / Workspace / Intelligence / Platform / QE / Support / Sales | Cloud API |
| 5 | Manager name | string | matches HR EM record | Anjali Desai |
| 6 | Manager corporate email | email | `@acme.example` | anjali.desai@acme.example |
| 7 | Software / application name | enum | Jira / Confluence / GitHub Enterprise / Salesforce / Datadog / Vault / AWS Console / Azure Console / GCP Console / Figma / Notion / Looker / Nexus / ServiceNow-equivalent ITSM / Other | Datadog |
| 8 | Access level | enum | read / write / admin / prod-deploy | admin |
| 9 | Business justification | text | ≥ 30 chars; reference a ticket, project, or customer | Need Datadog admin to manage monitors for cloud-api dashboards; ticket CLOUD-1423 |
| 10 | Duration | enum | one-time (≤ 24h, PIM) / time-bound (date range) / standing (until revoked) | standing |
| 11 | Manager approval | enum | approved / pending / rejected | approved |
| 12 | Requested by | string | corporate email | anika.rao@acme.example |

## 3. Optional Fields

| # | Field | Type | Validation | Notes |
|---|-------|------|------------|-------|
| 1 | Time-bound start date | date | YYYY-MM-DD | Required if Duration = time-bound |
| 2 | Time-bound end date | date | YYYY-MM-DD, > start | Required if Duration = time-bound |
| 3 | PIM activation max hours | integer | 1–8, default 4 | Required if Duration = one-time |
| 4 | Reference ticket URL | url | https://helpdesk.acme.example/... | Recommended |
| 5 | Project / customer context | text | free text | Helps approver decide |
| 6 | Cross-recipient team | string | matches HR EM record | If access is shared cross-team |
| 7 | Data classification touched | enum | public / internal / confidential / restricted | See [`../03-security/data-classification.md`](../03-security/data-classification.md) |
| 8 | Cost center | string | finance record | For charge-back |

## 4. Validation Rules

1. Software name must match a name in the application portfolio table in [`../02-it/software-access-requests.md`](../02-it/software-access-requests.md). If `Other`, the form is auto-rejected and routed to IT Helpdesk (`helpdesk@acme.example`) for triage.
2. If `access_level = admin` or `prod-deploy`, a reference ticket URL is mandatory.
3. If `Duration = time-bound`, both `time_bound_start` and `time_bound_end` must be present and end must be after start.
4. If `Duration = one-time`, `pim_activation_max_hours` must be 1–8 (default 4).
5. If the application touches `restricted` customer data, CISO approval is mandatory — the form cannot be submitted without the CISO routing flagged.
6. `Vault` access requires an existing ACME-FORM-003 IT access record showing the engineer has a laptop with the corporate password manager configured (see [`../02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md)).
7. `Access_level = admin` on GitHub Enterprise org-level requires VP Engineering co-approval (see [`../02-it/software-access-requests.md`](../02-it/software-access-requests.md) §6).

## 5. Responsible Owner

- **Form owner (IT):** IT Onboarding Specialist — Geetha Iyer (`geetha.iyer@acme.example`).
- **Software owner (varies by app):** See [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md). Defaults:
  - Jira / Confluence admin → IT Manager Hyderabad (Arjun Kapoor, `arjun.kapoor@acme.example`)
  - GitHub Enterprise org admin → VP Engineering (Sridhar Venkatesh, `sridhar.venkatesh@acme.example`)
  - Salesforce admin → VP Sales (via HRBP)
  - Datadog admin → SRE Lead under Platform Infrastructure (Nikhil Joshi, `nikhil.joshi@acme.example`)
  - Vault → CISO delegate (Rajan Mehta, `rajan.mehta@acme.example`)
  - AWS / Azure / GCP prod roles → Team lead + Security
- **Submission channel:** ITSM portal `https://helpdesk.acme.example` (simulated) or email `helpdesk@acme.example`.
- **SLA:** 1 business day (read), 3 business days (write/admin), 5 business days (org admin / prod-deploy).

## 6. Approval Requirements (Workflow)

1. **Hiring EM / Direct manager (mandatory).** The employee's direct manager approves the business justification. Without manager approval the form is auto-rejected.
2. **Software owner (mandatory for elevated).** Required when `access_level ∈ {write, admin, prod-deploy}`. The application owner (per §5) confirms the request fits the app's usage policy.
3. **CISO (mandatory for elevated / privileged).** Required when any of:
   - `access_level = admin` or `prod-deploy`.
   - Application is Vault, AWS / Azure / GCP prod, or GitHub Enterprise org admin.
   - Data classification touched is `restricted`.
   - CISO delegate: Rajan Mehta (`rajan.mehta@acme.example`).
4. **VP Engineering (co-approval).** Required only for GitHub Enterprise org admin.
5. **VP IT (co-approval).** Required only for ITSM admin roles.
6. **Routing outcome.** Approved form triggers:
   - **SCIM apps:** Entra ID group membership add (auto-provisions within 60 minutes).
   - **Manual apps:** Direct add by the app owner.
   - **Privileged / PIM:** Entra ID PIM eligibility (the employee activates per use, see [`../02-it/software-access-requests.md`](../02-it/software-access-requests.md) §7).
7. **Quarterly review.** All approved access is added to the next quarterly access review (ACME-FORM-012, [`./access-review.md`](./access-review.md)).

## 7. Sample Filled Values (Fictional)

```yaml
form_id: ACME-FORM-004
submission_id: ACME-2026-0488-SOFT-1
submitted_at: 2026-10-04T11:00:00+05:30
employee:
  name: Anika Rao
  employee_id: ACME-2026-0488
  corporate_email: anika.rao@acme.example
  team: Cloud API
manager:
  name: Anjali Desai
  email: anjali.desai@acme.example
request:
  software: Datadog
  access_level: admin
  duration: standing
  justification: >-
    Need Datadog admin to manage monitors and dashboards for cloud-api
    services; ticket CLOUD-1423 for on-call rotation setup.
  reference_ticket_url: https://helpdesk.acme.example/ticket/CLOUD-1423
  data_classification_touched: internal
  cost_center: CC-CLOUD-2026
requested_by: anika.rao@acme.example
approvals:
  manager:
    by: anjali.desai@acme.example
    decision: approved
    timestamp: 2026-10-04T13:15:00+05:30
  software_owner:
    by: nikhil.joshi@acme.example
    decision: approved
    timestamp: 2026-10-05T10:00:00+05:30
  ciso:
    by: rajan.mehta@acme.example
    decision: approved
    timestamp: 2026-10-05T16:30:00+05:30
provisioning:
  method: SCIM (Entra ID group add)
  completed_at: 2026-10-05T17:35:00+05:30
```

## 8. Related Documents

- [`../02-it/software-access-requests.md`](../02-it/software-access-requests.md) — Application portfolio and approval routing matrix.
- [`../02-it/new-employee-it-request.md`](../02-it/new-employee-it-request.md) — Role bundle (default access).
- [`../02-it/microsoft-entra-id-and-sso.md`](../02-it/microsoft-entra-id-and-sso.md) — PIM and SSO context.
- [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) — Least-privilege principle.
- [`../03-security/identity-and-access-management.md`](../03-security/identity-and-access-management.md) — IAM policy.
- [`../03-security/data-classification.md`](../03-security/data-classification.md) — Data classification touchpoints.
- [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md) — Workflow context.
- [`./it-access-request.md`](./it-access-request.md) — Sibling form (new-hire kit).
- [`./repository-access-request.md`](./repository-access-request.md) — Sibling form (repos).
- [`./manager-approval.md`](./manager-approval.md) — Manager sign-off record.
- [`./access-review.md`](./access-review.md) — Quarterly attestation.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — App owners.
