---
document_id: ACME-FORM-012
title: Quarterly Access Review Form
category: form
department: security
applicable_roles: [em, director, vp]
owner: Security
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, security, grc, access-review, quarterly, attestation, least-privilege]
---

# Quarterly Access Review Form

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. All employee names, IDs, repository lists, and approval signatures below are illustrative. Do not submit real access data against this template.

## 1. Form Purpose

This form is used quarterly by each Engineering Manager (EM) to attest that each direct report's repository and tool access is still required for their current role. It is the cornerstone of ACME's access-recertification program (see [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) and [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §review-driven revocation) and feeds the quarterly access review workflow at [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md). The form is generated automatically each quarter from the ITSM and GitHub Enterprise audit logs; the EM reviews the pre-populated list, marks each entry, and signs. Failure to complete within 7 business days triggers automatic revocation of the unattested access.

## 2. Mandatory Fields

| # | Field | Type | Validation | Sample (fictional) |
|---|-------|------|------------|--------------------|
| 1 | Review quarter | enum | Q1 / Q2 / Q3 / Q4 + year (e.g., 2026-Q3) | 2026-Q3 |
| 2 | Reviewing EM name | string | matches HR EM record | Anjali Desai |
| 3 | Reviewing EM corporate email | email | `@acme.example` | anjali.desai@acme.example |
| 4 | EM's team / BU | enum | Cloud API / Cloud Frontend / Intelligence Agents / Intelligence Inference / Intelligence ML / Workspace Web / Workspace API / Platform Infrastructure / Quality Engineering | Cloud API |
| 5 | Direct reports list | array of records | each: name, employee_id, role | [{name: Anika Rao, employee_id: ACME-2026-0488, role: Backend Engineer}, ...] |
| 6 | Current access list per report | array | each: report_id, access entries (repo, software, AI tool) | see sample |
| 7 | Attestation per access entry | enum | still-needed / no-longer-needed / change-requested | still-needed |
| 8 | EM signature | signature | captured in HR Hub | (signed) Anjali Desai, 2026-09-30 |
| 9 | Attestation date | date (YYYY-MM-DD) | within quarter + 7 business days | 2026-09-30 |
| 10 | Review form generation timestamp | timestamp | auto | 2026-09-15T00:00:00+05:30 |

## 3. Optional Fields

| # | Field | Type | Validation | Notes |
|---|-------|------|------------|-------|
| 1 | Change-request detail | text | ≥ 20 chars | Required if any entry's attestation = change-requested |
| 2 | Reason for no-longer-needed | text | ≥ 20 chars | Required if any entry's attestation = no-longer-needed |
| 3 | Notes per direct report | text | free text | For the EM's working notes |
| 4 | GRC review comments | text | ≥ 20 chars | Filled by GRC Analyst during §6 step 2 |
| 5 | Out-of-band revocations | array | matches access entry refs | Revocations triggered outside this quarter |
| 6 | Auto-revocation count | integer | ≥ 0 | Count of access entries auto-revoked due to non-attestation last quarter |

## 4. Validation Rules

1. Review quarter must match the current quarter per the GRC review calendar (Q1 = Jan–Mar, Q2 = Apr–Jun, Q3 = Jul–Sep, Q4 = Oct–Dec).
2. The reviewing EM must be a current Engineering Manager per the HR record; if the EM has changed role mid-quarter, the form is regenerated for the new EM.
3. Each direct report's access list is pre-populated from the ITSM asset register and the GitHub Enterprise team membership export. The EM cannot add entries; they can only attest, request change, or flag as no-longer-needed.
4. If `attestation = change-requested`, `change-request detail` is mandatory and must reference a sibling form (ACME-FORM-003/004/005) that requests the change.
5. If `attestation = no-longer-needed`, `reason for no-longer-needed` is mandatory. The access is queued for revocation within 1 business day of GRC review (§6 step 2).
6. Attestation date must be within the review window: quarter end date + 7 business days. Late submissions trigger automatic revocation of unattested entries (per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §review-driven revocation).
7. The EM must attest every entry in the pre-populated list — partial attestations are not accepted (the form is `incomplete` until all entries are marked).

## 5. Responsible Owner

- **Form owner (Security):** GRC Analyst — Karthik Subramanian (`karthik.subramanian@acme.example`).
- **CISO (escalation):** Rajan Mehta (`rajan.mehta@acme.example`).
- **Attesting party:** Each Engineering Manager (per [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)) attests for their direct reports.
- **Storage location:** ACME HR Hub (`hr.acme.example`, fictional) with `confidential` classification. Mirrored to the GRC archive at `vault.acme.example` (simulated).
- **Retention:** 7 years for audit evidence.

## 6. Approval Requirements (Workflow)

1. **EM attestation (mandatory).** The reviewing EM goes through each direct report's access list and marks every entry as `still-needed`, `no-longer-needed`, or `change-requested`. The EM signs the form to confirm they have reviewed the entire list.
2. **GRC review (mandatory).** Karthik Subramanian (`karthik.subramanian@acme.example`) reviews the form for:
   - Completeness (all entries attested).
   - Reasonableness of `no-longer-needed` and `change-requested` decisions.
   - Patterns (e.g., an EM marking all entries `still-needed` without review is flagged).
   - The GRC Analyst signs off and, where entries are marked `no-longer-needed`, queues the revocation request to IT (`helpdesk@acme.example`).
3. **CISO escalation (conditional).** Required when:
   - An EM has marked any `restricted`-classification access entry as `still-needed` and the GRC Analyst disagrees.
   - The form is more than 5 business days late and a partial submission has been made (escalation to confirm the partial attestation).
   - Delegate: Rajan Mehta (`rajan.mehta@acme.example`).
4. **Automatic revocation (consequence).** If the form is not completed within 7 business days of quarter end, all unattested access entries for the EM's direct reports are automatically revoked per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md). The revocation list is logged with reason `review_overdue`.
5. **Routing outcome.** Filed form triggers:
   - GRC archive record creation.
   - Revocation requests for `no-longer-needed` entries (routed to IT).
   - Change requests for `change-requested` entries (routed to IT via the sibling forms).
   - Quarterly summary report for the CISO and VP Engineering.
6. **Cross-team access.** Access entries where the employee touches a repo outside their home BU are still attested by the home-BU EM (since the home-BU EM has visibility into the employee's role); the receiving EM is notified (read-only) of the attestation outcome.

## 7. Sample Filled Values (Fictional)

```yaml
form_id: ACME-FORM-012
submission_id: ACME-AR-2026-Q3-CLOUD-API-1
generated_at: 2026-09-15T00:00:00+05:30
review_quarter: 2026-Q3
reviewing_em:
  name: Anjali Desai
  email: anjali.desai@acme.example
  team: Cloud API
direct_reports:
  - name: Anika Rao
    employee_id: ACME-2026-0488
    role: Backend Engineer
    access_entries:
      - type: repository
        name: acme-cloud-api
        access_level: write
        team_slug: cloud-api/backend
        attestation: still-needed
      - type: software
        name: Datadog
        access_level: admin
        attestation: still-needed
      - type: ai_tool
        name: GitHub Copilot Business
        attestation: still-needed
      - type: software
        name: Vault
        access_level: read
        path: secrets/cloud-api/*
        attestation: no-longer-needed
        reason: Anika no longer on-call for secrets rotation; moved to Priya.
  - name: Rohan Mehta
    employee_id: ACME-2025-1199
    role: Senior Backend Engineer
    access_entries:
      - type: repository
        name: acme-cloud-api
        access_level: maintain
        team_slug: cloud-api/backend
        attestation: still-needed
      - type: repository
        name: acme-shared-libraries
        access_level: write
        team_slug: shared/platform
        attestation: change-requested
        change_request_detail: >-
          Requesting change from write → maintain on acme-shared-libraries;
          ref ACME-2026-0488-REPO-2.
signatures:
  em:
    name: Anjali Desai
    signed_at: 2026-09-30T16:00:00+05:30
    attestation_date: 2026-09-30
  grc_review:
    by: karthik.subramanian@acme.example
    decision: approved
    comments: >-
      All entries attested; Vault revocation for Anika queued; shared-libraries
      change request for Rohan routed. No anomalies.
    timestamp: 2026-10-01T10:30:00+05:30
  ciso_escalation: not_required
routing_outcome:
  revocations_queued:
    - employee: Anika Rao
      entry: Vault (secrets/cloud-api/*)
      target_system: vault.acme.example
      queued_at: 2026-10-01T11:00:00+05:30
  change_requests_queued:
    - employee: Rohan Mehta
      entry: acme-shared-libraries (write → maintain)
      sibling_form: ACME-FORM-005
      queued_at: 2026-10-01T11:05:00+05:30
```

## 8. Related Documents

- [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) — Governing principle.
- [`../03-security/identity-and-access-management.md`](../03-security/identity-and-access-management.md) — IAM policy.
- [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) — Review-driven revocation.
- [`../02-it/software-access-requests.md`](../02-it/software-access-requests.md) — Quarterly review cadence.
- [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md) — Canonical repo list.
- [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md) — Workflow context.
- [`./repository-access-request.md`](./repository-access-request.md) — Sibling form for change requests.
- [`./software-access-request.md`](./software-access-request.md) — Sibling form for change requests.
- [`./manager-approval.md`](./manager-approval.md) — Manager sign-off record.
- [`../12-offboarding/repository-and-system-access-revocation.md`](../12-offboarding/repository-and-system-access-revocation.md) — Offboarding revocation context.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — GRC Analyst contact.
