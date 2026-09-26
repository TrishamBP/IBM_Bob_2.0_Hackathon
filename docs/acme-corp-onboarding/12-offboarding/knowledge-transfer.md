---
document_id: ACME-OFF-004
title: Knowledge Transfer Plan
category: offboarding
department: engineering
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [offboarding, knowledge-transfer, handover, runbooks, on-call]
---

# Knowledge Transfer Plan

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. The systems (`git.acme.example`, `wiki.acme.example`, `helpdesk.acme.example`), repositories, and customer names below are illustrative.

## 1. Purpose

This document is the **mandatory Knowledge Transfer (KT) plan template** that a departing employee and their hiring engineering manager (EM) complete together in the final weeks of employment. It is consistent with [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) §Knowledge Transfer and is tracked as part of the [`./employee-departure-checklist.md`](./employee-departure-checklist.md) workflow (DEP-006 through DEP-013 and DEP-017).

Knowledge transfer at ACME is not optional. It is the single most important activity of the final week: it protects the team from losing tacit knowledge of systems, customers, and on-call playbooks, and it gives the successor a fair start. The hiring EM owns the KT plan, the departing employee executes it, and the successor signs off on it before the LWD.

## 2. Owner and SLA

- **Process owner:** Hiring EM (engineering manager per team — see [`../00-company/organizational-structure.md`](../00-company/organizational-structure.md)).
- **SLA (KT plan):** The KT plan is **delivered to the hiring EM 1 week before the LWD (T-7)**.
- **SLA (KT execution):** KT is **executed over the final week (T-7 to T-1)**, with successor sign-off recorded in HR Hub by T-1.
- **Escalation:** If KT plan or sign-off is incomplete at T-1, escalate to the HRBP and the VP Engineering / CTO — Sridhar Venkatesh (`sridhar.venkatesh@acme.example`).

## 3. Scope

The KT plan covers every dimension of the departing employee's work that the team needs to continue without them:

| # | Dimension | What it includes |
|---|-----------|------------------|
| 1 | In-flight work | Pull requests, design docs, customer commitments, scheduled releases |
| 2 | Owned runbooks | Operational runbooks the employee owns in `wiki.acme.example` (fictional); on-call playbooks; incident-response runbooks |
| 3 | Customer / stakeholder introductions | Direct customer contacts, partner relationships, internal stakeholder dependencies |
| 4 | Design doc finalization | Outstanding design docs the employee authored — finalize, mark final, and hand off ownership |
| 5 | On-call rotation removal | Removal from PagerDuty / Opsgenie rotation(s) with a backup-coverage plan that does not create an unstaffed gap |
| 6 | Code ownership transfer | CODEOWNERS file updates; GitHub Enterprise repo ownership transfer to the team lead |
| 7 | Standing meetings | Recurring meetings the employee chairs — reassign chair, or cancel with notice |
| 8 | Outstanding access requests | Pending access-request tickets the employee filed — close or transfer to the successor |

## 4. KT Plan Template (Mandatory Sections)

The KT plan is filed in HR Hub and linked to the offboarding ticket (`OFFBD-YYYY-NNNNNN`). The plan is structured as below; each section must be filled. Status of each section: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

### 4.1 In-flight work handover

| Field | Description | Sample (fictional) |
|-------|-------------|---------------------|
| Employee name | Departing employee | Anika Rao |
| Employee ID | `ACME-YYYY-NNNN` | ACME-2026-0488 |
| Hiring EM | Engineering manager | Anjali Desai |
| Successor / coverage owner | Person taking over | Rahul Verma |
| Last working day | LWD | 2026-10-15 |
| KT plan delivery date | T-7 | 2026-10-08 |
| KT execution window | T-7 to T-1 | 2026-10-08 to 2026-10-14 |
| In-flight PRs | Open PRs authored by the employee, with status | PR #1234 (open, awaiting review), PR #1238 (draft, WIP), PR #1240 (blocked on design) |
| In-flight design docs | Outstanding design docs the employee authored | ADR-2026-091 (Cloud API rate limiting) — draft; ADR-2026-097 (Cloud API observability) — review |
| Customer commitments | Customer-facing commitments with dates | Customer X — feature Y by 2026-10-20; Customer Z — bug fix by 2026-10-22 |
| Scheduled releases | Releases the employee was driving | Cloud API v3.4 — release manager; was due 2026-10-18 |

For each item, the plan records: (a) current status, (b) the successor's next action, (c) any blockers, (d) the target close date.

### 4.2 Owned runbooks update

The employee lists every runbook they own in `wiki.acme.example` (fictional Confluence space). For each:

| Runbook | Last updated | Update needed? | Successor action | Status |
|---------|--------------|----------------|------------------|--------|
| RB-ENG-014 Cloud API incident triage | 2026-08-15 | Yes — add Datadog monitor link | Rahul Verma to merge updates | NOT_STARTED |
| RB-ENG-019 Cloud API deployment rollback | 2026-07-22 | Yes — add new Helm chart path | Rahul Verma to merge updates | NOT_STARTED |
| RB-ENG-022 Cloud API on-call onboarding | 2026-09-01 | No | n/a | COMPLETED |

Each runbook is reviewed by the employee and the successor together; updates are merged before T-1; the successor is added as a watcher.

### 4.3 Customer / stakeholder introductions

The employee introduces the successor to every direct customer and stakeholder relationship. For each:

| Customer / stakeholder | Relationship | Introduction mechanism | Status |
|------------------------|-------------|-------------------------|--------|
| Customer X (Cloud API enterprise) | TAM (technical account manager) | Email intro + 30-min Zoom | NOT_STARTED |
| Customer Z (Cloud API mid-market) | Primary eng contact | Email intro + Slack channel invite | NOT_STARTED |
| Internal stakeholder: QE lead (Asha Reddy) | Cross-team dependency on release sign-off | Slack intro + 15-min sync | NOT_STARTED |
| Internal stakeholder: Workspace API team (Priya Menon) | Shared library consumer | Slack intro + design-doc review meeting | NOT_STARTED |
| Partner: Datadog integration owner | Third-party integration | Email intro (cc'd) | NOT_STARTED |

Introduction emails are sent at T-7 and T-6; transition meetings are scheduled at T-3 and T-2.

### 4.4 Design doc finalization

The employee finalizes every outstanding design doc:

| ADR / design doc | Status at KT start | Target status at T-1 | Owner after handover |
|-------------------|---------------------|----------------------|----------------------|
| ADR-2026-091 (Cloud API rate limiting) | Draft | Final (or moved to a successor as draft) | Rahul Verma |
| ADR-2026-097 (Cloud API observability) | In review | Final | Rahul Verma |

If a design doc cannot be finalized before T-1, the hiring EM explicitly accepts the draft state and assigns a new owner; the successor inherits the draft and the open questions.

### 4.5 On-call rotation removal (with backup coverage plan)

This is the most operationally sensitive section. Removing a person from an on-call rotation can leave the team with an unstaffed gap — that must not happen. For each rotation the employee is on:

| Rotation | Role in rotation | Removal timing | Backup coverage plan | Status |
|----------|-------------------|----------------|----------------------|--------|
| Cloud API primary on-call | Primary (weeks 3, 7) | Remove from PagerDuty schedule at T-2 | Reassign weeks 3, 7 to Rahul Verma + Manoj Pillai (Cloud Frontend EM who has been cross-trained) | NOT_STARTED |
| Cloud API secondary on-call | Secondary (weeks 1, 5) | Remove at T-2 | Reassign weeks 1, 5 to alternate engineers per Cloud API staffing plan | NOT_STARTED |
| Cloud API incident commander (sev1) | IC rotation (week 9) | Remove at T-2 | Anjali Desai (hiring EM) takes week 9 IC rotation; backup IC: Sridhar Venkatesh (VP Eng) | NOT_STARTED |

Backup coverage plan must include:

- The replacement name(s) for every rotation slot the departing employee held.
- Confirmation that the replacement(s) are trained (have completed the on-call onboarding runbook).
- Confirmation that PagerDuty / Opsgenie schedules are updated by T-2 (not later, to avoid a T-0 on-call emergency).
- A contingency for a sev1 incident in the gap: who is the named backup IC if the replacement is also unavailable.

The hiring EM signs the backup coverage plan at T-2 and notifies the GRC Analyst (Karthik Subramanian) so the on-call audit reflects the change.

### 4.6 Code ownership transfer

For every GitHub Enterprise repository the employee has ownership or CODEOWNERS entry in:

| Repo | Role | New owner | CODEOWNERS update | Status |
|------|------|-----------|---------------------|--------|
| `acme-cloud-api` (Cloud API) | Maintainer + CODEOWNERS entry on `/services/` | Rahul Verma | PR removes `@anika.rao`, adds `@rahul.verma` | NOT_STARTED |
| `acme-shared-libraries` (Shared Libraries) | Maintainer | Nikhil Joshi (Platform Infra EM) | PR removes `@anika.rao` | NOT_STARTED |
| `acme-quality-automation` (QE) | Read-only (no ownership transfer needed) | n/a | n/a | COMPLETED |

Per [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md) every repo must have **≥2 owners**. The hiring EM verifies this after the transfer; if a repo falls below 2 owners, Engineering IT reassigns ownership to the team lead as a fallback (per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §9).

### 4.7 Standing meetings

| Meeting | Role | Reassignment | Status |
|--------|------|--------------|--------|
| Cloud API weekly eng review | Chair | Reassign to Rahul Verma; cancel if no successor | NOT_STARTED |
| Cloud API quarterly roadmap | Co-chair | Reassign to Anjali Desai | NOT_STARTED |
| Cross-team sync with Workspace API | Attendee | Reassign to Rahul Verma | NOT_STARTED |

For meetings the employee chairs, the calendar invite is updated with the new chair at T-3, with a note to attendees.

### 4.8 Outstanding access requests

| Pending ticket | Filed by | Action | Status |
|----------------|----------|--------|--------|
| `ACC-2026-09123` — additional Datadog dashboard access | Anika Rao (departing) | Close as "not needed"; the successor files a new request if required | NOT_STARTED |
| `ACC-2026-09145` — Vault secret request for new Cloud API service | Anika Rao (departing) | Transfer to Rahul Verma — re-approval required | NOT_STARTED |

Per [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) §3 default-deny, the successor does **not** inherit the access automatically — they must file their own request and obtain their own approval.

## 5. KT Sign-Off

The hiring EM signs off on the KT plan in HR Hub at T-1. Sign-off attests that:

1. The in-flight work handover is complete and the successor has acknowledged their next actions.
2. The owned runbooks are updated and merged; the successor is the new watcher.
3. The customer / stakeholder introductions are sent and transition meetings are scheduled.
4. The design docs are finalized (or the EM accepts the draft state and assigns a new owner).
5. The on-call rotation is updated and the backup coverage plan is signed; no unstaffed gap exists.
6. The CODEOWNERS files are updated; every repo still has ≥2 owners.
7. The standing meetings are reassigned.
8. The outstanding access requests are closed or transferred.

Sign-off triggers DEP-017 (KT sign-off in HR Hub) → `COMPLETED`. Without KT sign-off, the offboarding ticket cannot be closed at T+45 by the HRBP (per [`./employee-departure-checklist.md`](./employee-departure-checklist.md) DEP-035).

## 6. On-Call Removal and Backup Coverage Plan — Detail

Because on-call is the area where a poorly-managed KT can directly cause a sev1 incident (an unstaffed gap during a production outage), this section gets extra detail:

- **Removal timing:** On-call removals execute at **T-2** (two business days before the LWD), not at T-0. This gives a 2-day buffer to confirm the rotation is correctly staffed.
- **Backup coverage plan structure:** For every rotation slot the departing employee held, the plan must name (a) a primary replacement and (b) a named backup. Both must have completed the on-call onboarding runbook (per [`../04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md)).
- **Cross-training evidence:** If the replacement is being cross-trained (e.g., Manoj Pillai from Cloud Frontend taking a Cloud API secondary slot), the hiring EM attests that the cross-training is at a level sufficient for the rotation. This is a judgment call — but it must be documented, not assumed.
- **PagerDuty / Opsgenie update:** IT Onboarding (Geetha Iyer) updates the PagerDuty / Opsgenie schedule at T-2, after the hiring EM signs the backup coverage plan.
- **Sev1 contingency:** If a sev1 incident occurs in the final week with the departing employee still in the rotation, they are expected to respond as normal (they are still employed). If a sev1 occurs in the gap between T-2 and T-0, the backup coverage plan activates.
- **Audit:** The GRC Analyst (Karthik Subramanian) reviews on-call changes during quarterly access reviews (per [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) §7).

## 7. Status Tracking

All KT subtasks are tracked in the ITSM offboarding ticket (`OFFBD-YYYY-NNNNNN`) and mirrored to the HR Hub offboarding record. Allowed statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

| Sub-task | Mapped DEP ID | Default status |
|----------|---------------|----------------|
| Draft KT plan | DEP-006 | NOT_STARTED |
| Ownership transfer (SharePoint, Jira, Confluence, vaults) | DEP-007 | NOT_STARTED |
| Design doc finalization + runbook updates | DEP-008 | NOT_STARTED |
| Customer / stakeholder introductions | DEP-009 | NOT_STARTED |
| KT execution over the final week | DEP-013 | NOT_STARTED |
| On-call rotation removal + backup coverage | DEP-014 | NOT_STARTED |
| KT sign-off in HR Hub | DEP-017 | NOT_STARTED |

## 8. RACI Matrix

| Activity | R | A | C | I |
|----------|---|---|---|---|
| Draft KT plan | Departing employee + Hiring EM | Hiring EM | HRBP | VP Eng |
| Execute in-flight work handover | Departing employee + Successor | Hiring EM | HRBP | VP Eng |
| Update owned runbooks | Departing employee + Successor | Hiring EM | HRBP | VP Eng |
| Customer / stakeholder introductions | Departing employee | Hiring EM | HRBP | VP Eng |
| Finalize design docs | Departing employee + Successor | Hiring EM | HRBP | VP Eng |
| On-call rotation removal + backup coverage | Departing employee + Hiring EM + IT Onboarding | Hiring EM | GRC Analyst | VP Eng + CISO |
| CODEOWNERS / repo ownership transfer | Departing employee + Engineering IT | Hiring EM | Engineering IT | VP Eng |
| KT sign-off | Hiring EM | Hiring EM | HRBP + Successor | VP Eng |
| Close offboarding ticket (post-T+45) | HRBP | HR Operations | IT Onboarding | VP HR |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 9. Expected Outcomes

After this document:

- The hiring EM has a template to draft and execute the KT plan.
- The departing employee knows what is expected of them in their final week.
- The successor knows what they are receiving and signs off on it.
- The GRC Analyst and the CISO have the audit trail for on-call coverage continuity.
- The HRBP can refuse to close the offboarding ticket at T+45 if the KT sign-off is missing.

## 10. Troubleshooting

| Symptom | Likely cause | Resolution |
|---------|--------------|------------|
| Successor is not yet hired at KT start | Backfill delayed | Hiring EM identifies an interim coverage owner (typically a senior engineer on the team); KT proceeds with the interim owner; the eventual successor inherits a clean handover doc |
| CODEOWNERS update PR is blocked on review | CODEOWNERS review is slow | Hiring EM pings the team lead directly; Engineering IT can override in the admin console as a fallback per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §9 |
| Backup coverage plan cannot identify a trained replacement | Team is understaffed / cross-training incomplete | Hiring EM escalates to VP Eng (Sridhar Venkatesh); on-call slot is reassigned to the hiring EM as a fallback; HRBP notified; rotation gap documented in risk register |
| Customer introduction declined | Customer unavailable before LWD | Departing employee records the customer relationship in a CRM handoff note; hiring EM (or sales rep for sales-led relationships) picks up post-LWD |
| KT plan blocked on missing design-doc sign-off from a stakeholder | Stakeholder unavailable | Hiring EM accepts the draft state; the open question is recorded in the design doc and assigned to the successor; KT plan proceeds |

## 11. Related Documents

- HR: [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md), [`../01-hr/probation-and-confirmation-process.md`](../01-hr/probation-and-confirmation-process.md)
- IT: [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md)
- Security: [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md), [`../03-security/source-code-security.md`](../03-security/source-code-security.md), [`../03-security/confidentiality-agreement.md`](../03-security/confidentiality-agreement.md)
- Engineering: [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md), [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md), [`../04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md)
- Workflows: [`../07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md), [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md)
- Forms: [`../08-forms/manager-approval.md`](../08-forms/manager-approval.md)
- Contacts: [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)
