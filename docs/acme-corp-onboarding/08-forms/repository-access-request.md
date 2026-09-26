---
document_id: ACME-FORM-005
title: Repository Access Request Form
category: form
department: it-operations
applicable_roles: [engineer, em, sre, qe, ai-research-engineer, devops-engineer, cloud-platform-engineer, ai-ml-engineer]
owner: IT
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, it, engineering, repository, github-enterprise, access, least-privilege]
---

# Repository Access Request Form

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. The GitHub Enterprise endpoint `git.acme.example` and all repository names below are illustrative. Real product names (GitHub Enterprise, GitHub Copilot) are referenced by their real names but the ACME integration details are fictional.

## 1. Form Purpose

This form is used by an ACME Corp engineer to request access to a specific repository hosted on ACME's GitHub Enterprise at `git.acme.example` (simulated). It complements ACME-FORM-003 ([`./it-access-request.md`](./it-access-request.md)) which grants organization-level SSO; this form grants **repository-level team membership** with a specific access level (read / write / maintain / admin). The form is the standard mechanism for both new-hire onboarding (the home repository is requested by the hiring EM) and for ongoing access changes (an engineer joining a new project). The form enforces the least-privilege principle documented in [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) and the source-code security policy at [`../03-security/source-code-security.md`](../03-security/source-code-security.md).

## 2. Mandatory Fields

| # | Field | Type | Validation | Sample (fictional) |
|---|-------|------|------------|--------------------|
| 1 | Employee name | string | non-empty | Anika Rao |
| 2 | Employee ID | string | `ACME-YYYY-NNNN` | ACME-2026-0488 |
| 3 | Employee corporate email | email | `@acme.example` | anika.rao@acme.example |
| 4 | Team / BU | enum | Cloud / Workspace / Intelligence / Platform / QE | Cloud API |
| 5 | Hiring manager / requester | string | matches HR EM record | Anjali Desai |
| 6 | Manager corporate email | email | `@acme.example` | anjali.desai@acme.example |
| 7 | Repository name | enum | one of: acme-cloud-api / acme-cloud-frontend / acme-intelligence-agents / acme-intelligence-inference / acme-intelligence-ml / acme-workspace-web / acme-workspace-api / acme-platform-infrastructure / acme-shared-libraries / acme-quality-automation | acme-cloud-api |
| 8 | Access level | enum | read / write / maintain / admin | write |
| 9 | GitHub Enterprise team slug | string | matches `git.acme.example` team | cloud-api/backend |
| 10 | Business justification | text | ≥ 30 chars; reference a ticket, project, or epic | Joining cloud-api backend team; needs write access for sprint CLOUD-1423 deliverables |
| 11 | Requested by | string | corporate email | anjali.desai@acme.example |

## 3. Optional Fields

| # | Field | Type | Validation | Notes |
|---|-------|------|------------|-------|
| 1 | Cross-team recipient EM | string | matches HR EM record | Required if repo is outside the employee's home BU |
| 2 | Expiration date | date (YYYY-MM-DD) | > today | For time-bound access (e.g., rotation) |
| 3 | CODEOWNERS path scope | string | matches `CODEOWNERS` file path | Restrict write to specific subtree |
| 4 | Branch protection scope | enum | all branches / main only / release/* | For granular write |
| 5 | Production deploy flag | boolean | true / false | If true → GRC approval mandatory |
| 6 | Reference PR / ticket URL | url | https://git.acme.example/... or https://helpdesk.acme.example/... | Recommended |
| 7 | Sister-repo access | enum (multi) | from canonical repo list | If work spans multiple repos |

## 4. Validation Rules

1. Repository name must match the canonical list in [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md). If `Other`, the form is auto-rejected and routed to IT Helpdesk.
2. Access level must respect the CODEOWNERS policy for the repository (see each repo doc, e.g., [`../04-engineering/repositories/acme-cloud-api.md`](../04-engineering/repositories/acme-cloud-api.md)). `admin` level is gated to the repository's owning-team EM only.
3. GitHub Enterprise team slug must exist in the `git.acme.example` org (validated via SCIM).
4. If the repository is outside the employee's home BU (e.g., Cloud API engineer requesting access to `acme-intelligence-agents`), the cross-team recipient EM field is mandatory.
5. `production_deploy_flag = true` triggers GRC Analyst approval (see §6) and a mandatory reference ticket URL.
6. `Expiration date` is enforced via GitHub Enterprise team membership expiry; expired memberships are auto-removed by SCIM.
7. The requester must be the hiring EM, the engineer themselves (for additional repo access), or the IT Onboarding Specialist acting on their behalf.

## 5. Responsible Owner

- **Form owner (IT):** IT Onboarding Specialist — Geetha Iyer (`geetha.iyer@acme.example`).
- **Repo owners (per repository):**
  - acme-cloud-api → Anjali Desai (`anjali.desai@acme.example`)
  - acme-cloud-frontend → Manoj Pillai (`manoj.pillai@acme.example`)
  - acme-intelligence-agents → Rohan Bhat (`rohan.bhat@acme.example`)
  - acme-intelligence-inference → Vivek Anand (`vivek.anand@acme.example`)
  - acme-intelligence-ml → Lakshmi Narayan (`lakshmi.narayan@acme.example`)
  - acme-workspace-web → Thomas Buckley (`thomas.buckley@acme.example`)
  - acme-workspace-api → Priya Menon (`priya.menon@acme.example`)
  - acme-platform-infrastructure → Nikhil Joshi (`nikhil.joshi@acme.example`)
  - acme-shared-libraries → Nikhil Joshi (`nikhil.joshi@acme.example`)
  - acme-quality-automation → Asha Reddy (`asha.reddy@acme.example`)
- **GRC Analyst (prod-deploy only):** Karthik Subramanian (`karthik.subramanian@acme.example`).
- **Submission channel:** ITSM portal `https://helpdesk.acme.example` (simulated) or email `helpdesk@acme.example`.

## 6. Approval Requirements (Workflow)

1. **Hiring EM (auto for home repo).** When the form is submitted by the hiring EM and the repository matches the engineer's home BU repository (per [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md)), approval is **automatic** — the hiring EM's submission is itself the approval.
2. **Receiving EM (cross-team).** Required when the repository is outside the employee's home BU. For example, a Cloud API engineer requesting access to `acme-intelligence-agents` requires Rohan Bhat's approval.
3. **GRC Analyst (prod-deploy only).** Required when `production_deploy_flag = true`. Karthik Subramanian (`karthik.subramanian@acme.example`) confirms the engineer has completed production-deploy training and the access aligns with least-privilege (see [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md)).
4. **CISO (escalation).** Required only when the GRC Analyst escalates (e.g., the repo handles `restricted` customer data per [`../03-security/data-classification.md`](../03-security/data-classification.md)). Delegate: Rajan Mehta (`rajan.mehta@acme.example`).
5. **Routing outcome.** Approved form triggers GitHub Enterprise team membership add via SCIM (auto-provisions within 60 minutes). The engineer receives an email confirmation at their `@acme.example` address.
6. **Quarterly review.** Approved access is added to the next quarterly access review (ACME-FORM-012, [`./access-review.md`](./access-review.md)).

## 7. Sample Filled Values (Fictional)

```yaml
form_id: ACME-FORM-005
submission_id: ACME-2026-0488-REPO-1
submitted_at: 2026-09-11T09:00:00+05:30
employee:
  name: Anika Rao
  employee_id: ACME-2026-0488
  corporate_email: anika.rao@acme.example
  team: Cloud API
requester:
  name: Anjali Desai
  email: anjali.desai@acme.example
request:
  repository: acme-cloud-api
  access_level: write
  github_team_slug: cloud-api/backend
  justification: >-
    Joining cloud-api backend team; needs write access for sprint
    CLOUD-1423 deliverables on /services/payments.
  reference_ticket_url: https://helpdesk.acme.example/ticket/CLOUD-1423
  production_deploy_flag: false
approvals:
  hiring_em:
    by: anjali.desai@acme.example
    decision: approved (auto — home repo)
    timestamp: 2026-09-11T09:00:00+05:30
  cross_team_em: not_required (repo is in home BU)
  grc_analyst: not_required (no prod-deploy flag)
  ciso: not_required
provisioning:
  method: SCIM (GitHub Enterprise team add)
  completed_at: 2026-09-11T10:02:00+05:30
```

## 8. Related Documents

- [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md) — Canonical repo list and owning teams.
- [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md) — Repo access narrative.
- [`../04-engineering/repositories/acme-cloud-api.md`](../04-engineering/repositories/acme-cloud-api.md) — Per-repo doc example.
- [`../03-security/source-code-security.md`](../03-security/source-code-security.md) — Source code security policy.
- [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) — Least-privilege principle.
- [`../02-it/software-access-requests.md`](../02-it/software-access-requests.md) — GitHub Enterprise routing matrix.
- [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md) — Workflow context.
- [`./it-access-request.md`](./it-access-request.md) — Sibling form (org-level SSO).
- [`./manager-approval.md`](./manager-approval.md) — Manager sign-off record.
- [`./access-review.md`](./access-review.md) — Quarterly attestation.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Repo owners.
