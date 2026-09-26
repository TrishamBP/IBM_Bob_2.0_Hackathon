---
document_id: ACME-WF-010
title: Access Approval Workflow
category: workflow
department: security
applicable_roles: [all]
owner: Security Operations (CISO Office)
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [workflow, onboarding, access-approval]
---

# Access Approval Workflow

> Fictional document. All systems (vault.acme.example, packages.acme.example, git.acme.example, portal.acme.example) are illustrative.

## 1. Overview

ACME Corp applies a strict **least-privilege, time-boxed, just-in-time** access model. New hires progress through three tiers: **read-only** (day 1), **write** (week 1, gated by security training), and **production / elevated** (after day 60, gated by manager + skip-level + CISO approvals). All access is logged in the GRC system, reviewed quarterly, and revoked on separation per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md).

The canonical sequencing rule:

> Manager approval (MGR-001) → IT provisioning starts (IT-001). Policy acknowledgement (POL-001 / SEC-004) → access approvals beyond read-only (ACC-002). Security training (SEC-001) → repository write access (ACC-003).

## 2. Scope

- **Starts:** MGR-001 (manager checklist with access request list).
- **Ends:** Quarterly access review loop (ACC-008, ongoing).
- **Roles involved:** Hiring Manager, IT Onboarding, Security (GRC), CISO, New Hire, repo CODEOWNERS, team owners for vault / package / cloud resources.
- **Office-agnostic.**

## 3. Cross-References

- Security: [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md), [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md), [`../03-security/identity-and-access-management.md`](../03-security/identity-and-access-management.md), [`../03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- IT: [`../02-it/new-employee-it-request.md`](../02-it/new-employee-it-request.md), [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md), [`../02-it/software-access-requests.md`](../02-it/software-access-requests.md), [`../02-it/microsoft-entra-id-and-sso.md`](../02-it/microsoft-entra-id-and-sso.md)
- Engineering: [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md)
- Forms: [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md), [`../08-forms/repository-access-request.md`](../08-forms/repository-access-request.md), [`../08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md), [`../08-forms/manager-approval.md`](../08-forms/manager-approval.md), [`../08-forms/access-review.md`](../08-forms/access-review.md)
- Contacts: [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)

## 4. Access Approval Task List

| Task ID | Description | Responsible | Prerequisites | Due | Approval | Completion Criteria | Default Status |
|---|---|---|---|---|---|---|---|
| ACC-001 | Define access request list (repos, vault paths, package feeds, cloud subscriptions, app roles) | Hiring Manager | MGR-001 | 3 business days before start date | Skip-level director | List submitted in HR Hub; routed to IT and Security | NOT_STARTED |
| ACC-002 | Grant read-only repository access (clone, pull) across the listed repos | IT Onboarding + repo CODEOWNERS | IT-004 (active identity) | Day 2 | Manager | New hire can clone/pull listed repos; verified on `git.acme.example` | NOT_STARTED |
| ACC-003 | Grant write repository access (push, branch creation, PR authorship) | IT Onboarding + repo CODEOWNERS | SEC-001 (security training), [`policy-acknowledgement.md`](./policy-acknowledgement.md) POL-001, ACC-002 | End of day 5 | CODEOWNERS + Manager | New hire can push to a feature branch; first PR opened (WK1-010) | NOT_STARTED |
| ACC-004 | Grant AI coding assistant (GitHub Copilot Business) seat | IT Onboarding | SEC-005 (AI tool acknowledgement), [`first-week-onboarding.md`](./first-week-onboarding.md) WK1-007 | End of day 5 | Manager + Director AI/ML (Anitha Rajan) | Seat assigned in GitHub Enterprise; IDE plugin authenticated | NOT_STARTED |
| ACC-005 | Grant vault (`vault.acme.example`) read access to non-prod secrets | IT Onboarding + Security (GRC) | SEC-001, ACC-002 | End of day 5 | Security (GRC) | Vault policy attached; read verified for non-prod path | NOT_STARTED |
| ACC-006 | Grant package feed (`packages.acme.example`) read access (internal NuGet/npm/PyPI feeds) | IT Onboarding | ACC-002 | End of day 3 | IT Manager Hyderabad | Feed tokens issued; stored in password manager | NOT_STARTED |
| ACC-007 | Grant production / elevated access (production cloud subscriptions, prod vault paths, prod DBs) — *time-boxed, JIT, with break-glass review* | IT Onboarding + Security (GRC) | D60-008 (60-day HRBP sign-off), SEC-007, SEC-010, Manager + CISO approvals | After day 60 | Manager + skip-level director + CISO (Rajan Mehta) | Elevated access granted with expiry (max 90 days; renewal requires re-approval); logged in GRC | NOT_STARTED |
| ACC-008 | Quarterly access review — confirm least-privilege; retire unused grants; document exceptions | Hiring Manager + Security (GRC) + IT Onboarding | D30-003 (first 30-day review) | Quarterly (recurring) | Manager + IT Manager Hyderabad | Access review form submitted; retirements actioned in HR Hub | NOT_STARTED |
| ACC-009 | Audit log review — verify all access grants (ACC-002 through ACC-007) were properly approved; sample 10% of new hires per quarter | Security (GRC) | ACC-007 (last grant complete) | Quarterly | CISO office | Audit report filed; exceptions routed for remediation | NOT_STARTED |
| ACC-010 | Access revocation (separation trigger) — see [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) | IT Onboarding + Security | Separation event in HR Hub | Same business day as separation | IT Manager Hyderabad + CISO | All access revoked; revocation log closed; equipment recovered | NOT_STARTED |

## 5. Dependencies

- **MGR-001 blocks ACC-001** — Manager approval precedes access provisioning (canonical dependency).
- **ACC-001 blocks ACC-002 through ACC-007** — All grants require the manager-approved list.
- **IT-004 (active identity) blocks ACC-002** — Cannot grant repository access without an active Entra ID identity.
- **POL-001 (policy acknowledgement) blocks ACC-002** — Wait, the canonical rule says policy acknowledgement is required for access **beyond read-only**. So ACC-002 (read-only) does *not* require POL-001; but ACC-003 (write) does.
- **SEC-001 blocks ACC-003** — Repository write access requires security training completion (canonical dependency).
- **POL-001 blocks ACC-003** — Write repository access requires the policy acknowledgement (canonical dependency).
- **SEC-005 blocks ACC-004** — AI tool seat requires the AI tool acceptable use acknowledgement.
- **D60-008 blocks ACC-007** — Production / elevated access requires the 60-day HRBP sign-off — i.e., the new hire has demonstrated first-contribution + on-call shadow maturity.
- **SEC-007 blocks ACC-007** — Incident-reporting walkthrough must be complete before elevated access.
- **ACC-007 → D90-003** — Elevated access is a soft prerequisite for primary on-call (some on-call actions require elevated access; otherwise the new hire is paired with a senior on-call).
- **ACC-008 (quarterly review) → ACC-010** — The quarterly review cadence ensures revocation happens promptly on separation; the separation trigger (ACC-010) follows the same playbook for emergency revocation.
- **D30-003 → ACC-008** — The first 30-day access review (D30-003) establishes the quarterly cadence.

## 6. Status Tracking

All ACC-* tasks are tracked in the GRC system (`vault.acme.example` audit log) and mirrored to HR Hub under **Onboarding → Access**. Allowed statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

For ACC-007 (elevated access), the GRC Analyst records: grant date, expiry date (max 90 days), approver names, scope, and break-glass reviewer. Renewal requires a fresh ACC-007 entry; a lapsed grant is auto-revoked by the GRC system at expiry.

If ACC-008 (quarterly review) finds an unused grant, IT retires it within 5 business days and notifies the manager. Repeated unused grants for the same team trigger a CISO office review of that team's access patterns.

## 7. RACI Matrix

| Activity | R | A | C | I |
|---|---|---|---|---|
| Define access request list | Hiring Manager | Skip-level director | IT Onboarding, Security | VP HR |
| Read-only repo access | IT Onboarding + repo CODEOWNERS | Manager | New Hire | Security |
| Write repo access | IT Onboarding + repo CODEOWNERS | CODEOWNERS + Manager | Security | VP Engineering |
| AI coding assistant seat | IT Onboarding | Manager + Director AI/ML | Security | VP Engineering |
| Vault (non-prod) read | IT Onboarding + Security (GRC) | Security (GRC) | Manager | CISO office |
| Package feed tokens | IT Onboarding | IT Manager Hyderabad | New Hire | Engineering onboarding lead |
| Production / elevated access (JIT) | IT Onboarding + Security (GRC) | Manager + skip-level + CISO | New Hire | VP Engineering |
| Quarterly access review | Hiring Manager + Security (GRC) + IT Onboarding | Manager + IT Manager Hyderabad | HRBP | CISO office |
| Audit log review | Security (GRC) | CISO office | IT Onboarding | VP HR |
| Access revocation (separation) | IT Onboarding + Security | IT Manager Hyderabad + CISO | HRBP | VP HR |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 8. Key Terms

- **Least-privilege** — access principle: grant the minimum access required for the task. See [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).
- **JIT** — Just-In-Time access; temporary elevated access for a specific task. See [`../metadata/glossary.md`](../metadata/glossary.md).
- **IAM** — Identity and Access Management.
- **RBAC / ABAC** — Role-Based / Attribute-Based Access Control.
- **GRC** — Governance, Risk, and Compliance.
- **Break-glass** — emergency access path used when normal access procedures cannot be followed.

## 9. Hand-off

Access approval is ongoing: ACC-001 through ACC-007 complete during onboarding; ACC-008 and ACC-009 are recurring forever; ACC-010 fires only on separation. The onboarding-specific portion (ACC-001 through ACC-007) hands off to the standard IT/Security operations once D90-008 closes the 90-day file.
