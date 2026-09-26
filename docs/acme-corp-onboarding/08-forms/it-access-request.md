---
document_id: ACME-FORM-003
title: IT Access Request Form
category: form
department: it-operations
applicable_roles: [all]
owner: IT
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: confidential
tags: [form, it, access, provisioning, laptop, entra-id, intune]
---

# IT Access Request Form

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. All hostnames (`portal.acme.example`, `hr.acme.example`, `helpdesk.acme.example`, `vault.acme.example`, `packages.acme.example`, `git.acme.example`) and IDs below are illustrative. Real product names (Microsoft 365, Microsoft Entra ID, Microsoft Intune, Microsoft Authenticator, Jira, Salesforce, Datadog) are referenced by their real names but the ACME integration details are fictional.

## 1. Form Purpose

This form is used by a hiring Engineering Manager (EM) to request the standard IT kit for a new hire — laptop, Microsoft 365 account, Microsoft Entra ID identity, Microsoft Intune enrollment, Microsoft Authenticator enrollment, and the role's default SaaS bundle. It can also be used by an existing employee to request additional access (e.g., a new SaaS app, a second laptop, an extra Intune-enrolled device). The form drives the IT provisioning workflow at [`../07-workflows/it-provisioning.md`](../07-workflows/it-provisioning.md) and feeds the access-approval workflow at [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md).

## 2. Mandatory Fields

| # | Field | Type | Validation | Sample (fictional) |
|---|-------|------|------------|--------------------|
| 1 | Employee name | string | non-empty | Anika Rao |
| 2 | Employee ID | string | matches `ACME-YYYY-NNNN` | ACME-2026-0488 |
| 3 | Employee corporate email | email | `@acme.example` | anika.rao@acme.example |
| 4 | Hiring manager / requester | string | matches HR EM record | Anjali Desai |
| 5 | Manager corporate email | email | `@acme.example` | anjali.desai@acme.example |
| 6 | Role / job title | string | matches offer / HR record | Backend Engineer — Cloud API |
| 7 | Team / BU | enum | Cloud / Workspace / Intelligence / Platform / QE / Support / Sales | Cloud API |
| 8 | Office assignment | enum | Hyderabad / Bengaluru / London / Seattle / Remote | Bengaluru |
| 9 | Start date (new hire) OR request date (existing employee) | date | YYYY-MM-DD | 2026-09-15 |
| 10 | Requested access type | enum (multi-select) | laptop / M365 / Entra ID / Intune / Authenticator / SSO-Jira / SSO-Confluence / SSO-GitHub-Enterprise / SSO-Salesforce / SSO-Datadog / SSO-Figma / VPN / Wi-Fi / 1Password | laptop, M365, Entra ID, Intune, Authenticator, SSO-Jira, SSO-GitHub-Enterprise, 1Password |
| 11 | Laptop model (if laptop requested) | enum | MacBook Pro 14 / MacBook Pro 16 / Dell Latitude 7440 / Microsoft Surface Laptop 5 | MacBook Pro 14 |
| 12 | Operating system | enum | macOS Sonoma / Windows 11 Pro / Ubuntu 22.04 LTS (Cloud Platform Engineers only) | macOS Sonoma |
| 13 | Business justification | text | ≥ 30 chars | New hire Cloud API engineer; standard Cloud API team kit |
| 14 | Urgency | enum | standard (3 business days) / expedited (1 business day) / emergency (same day, requires VP IT approval) | standard |
| 15 | Requested by | string | corporate email | anjali.desai@acme.example |

## 3. Optional Fields

| # | Field | Type | Validation | Notes |
|---|-------|------|------------|-------|
| 1 | Special accessories | text | free text | e.g., "external monitor 27 inch", "ergonomic keyboard" |
| 2 | Pre-installed software list | text | free text | Beyond standard image — see [`../02-it/approved-software-installation.md`](../02-it/approved-software-installation.md) |
| 3 | Additional Entra ID group memberships | text | must match group CN | Used for non-default bundles |
| 4 | GitHub Enterprise team membership | string | matches `git.acme.example` team slug | e.g., `cloud-api/backend` |
| 5 | Datadog role | enum | viewer / standard / admin | Only if `SSO-Datadog` requested |
| 6 | Vault access path | string | matches `vault.acme.example` path | Engineering-only; gated by GRC |
| 7 | Cross-team recipient EM (if applicable) | string | matches HR EM record | Only if the new hire will work across teams |
| 8 | Cost center | string | matches finance record | Used for charge-back |

## 4. Validation Rules

1. Employee ID must match a record in the HR system (or, for new hires, the preboarding record created via [`../08-forms/new-employee-information.md`](../08-forms/new-employee-information.md)).
2. If `laptop` is requested, `laptop_model` and `operating_system` are mandatory.
3. `Ubuntu 22.04 LTS` is only permitted when team is `Platform Infrastructure` (see [`../04-engineering/repositories/acme-platform-infrastructure.md`](../04-engineering/repositories/acme-platform-infrastructure.md)).
4. `SSO-GitHub-Enterprise` triggers a sub-form ACME-FORM-005 ([`repository-access-request.md`](./repository-access-request.md)) for at least the engineer's home repository.
5. `Vault` access is only available to engineers with prod-deploy roles and requires GRC Analyst approval.
6. `Urgency = emergency` requires a P1/P2 ticket reference; without it the form is auto-downgraded to `expedited`.
7. The requester must be the hiring EM, the employee themselves (for additional access), or an HRBP/IT Onboarding Specialist acting on their behalf.

## 5. Responsible Owner

- **Form owner (IT):** IT Onboarding Specialist — Geetha Iyer (`geetha.iyer@acme.example`).
- **IT Manager Hyderabad (escalation):** Arjun Kapoor (`arjun.kapoor@acme.example`).
- **VP IT (emergency escalation):** Ramesh Khanna (`ramesh.khanna@acme.example`).
- **Submission channel:** ITSM portal at `https://helpdesk.acme.example` (simulated endpoint) or email `helpdesk@acme.example`.
- **SLA:** standard 3 business days, expedited 1 business day, emergency same day (see [`../02-it/new-employee-it-request.md`](../02-it/new-employee-it-request.md)).

## 6. Approval Requirements (Workflow)

1. **Hiring EM approval (auto for new-hire standard kit).** When the form is submitted by the hiring EM for a new hire and the requested access matches the role bundle in [`../02-it/new-employee-it-request.md`](../02-it/new-employee-it-request.md), approval is **automatic** — the hiring EM's submission is itself the approval.
2. **Receiving team EM (cross-team).** If the form indicates cross-team access (e.g., the new hire will also touch `acme-intelligence-agents`), the receiving EM (e.g., Rohan Bhat for Intelligence Agents) must approve.
3. **CISO (elevated / prod-deploy).** Required when any of:
   - The form requests Vault access.
   - The form requests prod-deploy roles on AWS / Azure / GCP.
   - The form requests `SSO-GitHub-Enterprise` admin (org-level).
   - The new hire will hold a role with access to customer data classified `restricted` (see [`../03-security/data-classification.md`](../03-security/data-classification.md)).
   - CISO delegate: Rajan Mehta (`rajan.mehta@acme.example`).
4. **VP IT (emergency only).** Required for `Urgency = emergency` to confirm the request cannot wait for the standard SLA.
5. **Routing.** Approved form triggers Intune enrollment email, M365 activation email (see [`../02-it/microsoft-365-account-activation.md`](../02-it/microsoft-365-account-activation.md)), and Entra ID group memberships per the role bundle.

## 7. Sample Filled Values (Fictional)

```yaml
form_id: ACME-FORM-003
submission_id: ACME-2026-0488-IT-1
submitted_at: 2026-09-11T08:30:00+05:30
employee:
  name: Anika Rao
  employee_id: ACME-2026-0488
  corporate_email: anika.rao@acme.example
  role: Backend Engineer — Cloud API
  team: Cloud API
  office_assignment: Bengaluru
  start_date: 2026-09-15
requester:
  name: Anjali Desai
  email: anjali.desai@acme.example
requested_access:
  - laptop
  - M365
  - Entra ID
  - Intune
  - Authenticator
  - SSO-Jira
  - SSO-Confluence
  - SSO-GitHub-Enterprise
  - 1Password
  - VPN
  - Wi-Fi
laptop:
  model: MacBook Pro 14
  operating_system: macOS Sonoma
justification: New hire Cloud API engineer; standard Cloud API team kit per role bundle.
urgency: standard
github_enterprise_team: cloud-api/backend
approvals:
  hiring_em:
    by: anjali.desai@acme.example
    decision: approved (auto — role bundle match)
    timestamp: 2026-09-11T08:30:00+05:30
  cross_team_em: not_required
  ciso: not_required (no vault, no prod-deploy, no customer-data-restricted role)
  vp_it: not_required (standard urgency)
```

## 8. Related Documents

- [`../02-it/new-employee-it-request.md`](../02-it/new-employee-it-request.md) — Role bundle reference.
- [`../02-it/laptop-and-workstation-allocation.md`](../02-it/laptop-and-workstation-allocation.md) — Laptop allocation policy.
- [`../02-it/software-access-requests.md`](../02-it/software-access-requests.md) — SaaS access reference.
- [`../02-it/microsoft-365-account-activation.md`](../02-it/microsoft-365-account-activation.md) — M365 activation.
- [`../02-it/microsoft-entra-id-and-sso.md`](../02-it/microsoft-entra-id-and-sso.md) — Entra ID / SSO context.
- [`../03-security/identity-and-access-management.md`](../03-security/identity-and-access-management.md) — IAM policy.
- [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) — Least-privilege principle.
- [`../07-workflows/it-provisioning.md`](../07-workflows/it-provisioning.md) — Workflow context.
- [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md) — Approval workflow.
- [`./software-access-request.md`](./software-access-request.md) — Sibling form for SaaS.
- [`./repository-access-request.md`](./repository-access-request.md) — Sibling form for repos.
- [`./equipment-handover.md`](./equipment-handover.md) — Handover record after this form is fulfilled.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Routing contacts.
