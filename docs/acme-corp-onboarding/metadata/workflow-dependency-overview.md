---
document_id: ACME-META-005
title: ACME Corp Onboarding Workflow Dependency Overview
category: metadata
department: all
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [metadata, workflow, dependencies]
---

# ACME Corp Onboarding Workflow Dependency Overview

This document summarizes the cross-workflow dependencies in the ACME onboarding program. Each row lists a prerequisite task and the dependent task, with a note on why the dependency exists. All workflow files live in [`07-workflows/`](../07-workflows/) and use the four-status vocabulary: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.

## Cross-Workflow Dependencies

| Prerequisite Task | Dependent Task | Why the Dependency Exists |
|-------------------|----------------|---------------------------|
| MGR-001 (Manager approval) | IT-001 (IT provisioning) | IT cannot begin provisioning until manager approval is recorded. |
| PRE-001 (HRBP info collection) | PRE-004 (Bank info form) | Bank info cannot be collected without employee identity verification. |
| IT-002 (M365 account activation) | DAY1-003 (MFA enrollment) | MFA enrollment requires an activated M365 identity. |
| DAY1-003 (MFA enrollment) | DAY1-004 (VPN configuration) | VPN cert issuance requires MFA enrollment. |
| EQP-001 (Equipment pre-stage) | EQP-002 (Equipment handover) | Equipment cannot be handed over before it is pre-staged. |
| EQP-002 (Equipment handover) | EQP-003 (Device acceptance) | Acceptance form requires handover to be complete. |
| POL-001 (Code of conduct ack) | ACC-002 (Standard tool access) | Tool access beyond read-only requires policy acknowledgement. |
| SEC-001 (Security training) | ACC-003 (Repository access) | Repository access requires security training completion. |
| ACC-003 (Repository access) | WK1-008 (First commit) | Engineers cannot push code without repository access. |
| MGR-002 (Buddy assignment) | DAY1-002 (Buddy introduction) | Buddy introduction requires buddy to be assigned. |
| PRE-008 (Day-1 calendar invite) | DAY1-001 (HR welcome) | HR welcome requires the calendar invite to be sent. |
| SEC-002 (Privacy ack) | ACC-004 (Customer data access) | Customer data access requires privacy acknowledgement. |
| ACC-004 (Customer data access) | ACC-005 (Production-deploy access) | Production-deploy access requires customer data handling training. |
| MGR-003 (EM access requests) | ACC-001 (Entra ID group membership) | Access provisioning begins only after EM submits requests. |
| WK1-001 (Company orientation) | WK1-002 (Security training) | Security training is taken after company orientation. |
| WK1-002 (Security training) | WK1-003 (Privacy training) | Privacy training is taken after security training. |
| D30-001 (30-day review) | D60-001 (60-day review) | 60-day review requires 30-day review to be complete. |
| D60-001 (60-day review) | D90-001 (90-day review) | 90-day review requires 60-day review to be complete. |
| D90-001 (90-day review) | CMP-001 (Onboarding completion) | Completion requires the 90-day review. |
| CMP-001 (Onboarding completion) | — | Terminal step — no further dependencies. |

## Workflow Files

- [`07-workflows/preboarding.md`](../07-workflows/preboarding.md) — `PRE-*` tasks
- [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) — `DAY1-*` tasks
- [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md) — `WK1-*` tasks
- [`07-workflows/first-30-days.md`](../07-workflows/first-30-days.md) — `D30-*` tasks
- [`07-workflows/first-60-days.md`](../07-workflows/first-60-days.md) — `D60-*` tasks
- [`07-workflows/first-90-days.md`](../07-workflows/first-90-days.md) — `D90-*` tasks
- [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) — `MGR-*` tasks
- [`07-workflows/it-provisioning.md`](../07-workflows/it-provisioning.md) — `IT-*` tasks
- [`07-workflows/security-training.md`](../07-workflows/security-training.md) — `SEC-*` tasks
- [`07-workflows/access-approval.md`](../07-workflows/access-approval.md) — `ACC-*` tasks
- [`07-workflows/equipment-handover.md`](../07-workflows/equipment-handover.md) — `EQP-*` tasks
- [`07-workflows/policy-acknowledgement.md`](../07-workflows/policy-acknowledgement.md) — `POL-*` tasks
- [`07-workflows/onboarding-completion.md`](../07-workflows/onboarding-completion.md) — `CMP-*` tasks

## Related Documents

- [`metadata/document-index.md`](./document-index.md)
- [`metadata/role-to-document-mapping.md`](./role-to-document-mapping.md)
- [`metadata/glossary.md`](./glossary.md)
