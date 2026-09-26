---
document_id: ACME-TRN-001
title: Company Orientation
category: training
department: hr
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [training, orientation, company, onboarding]
---

# Company Orientation (ACME-TRN-001)

> Fictional document. All systems, links, and addresses are illustrative.

## 1. Module Overview

The Company Orientation module is the foundational, mandatory course for every new ACME Corp employee regardless of role, level, or office location. It introduces the company's mission, history, values, product portfolio, office footprint, and hybrid working model. The module also orients new hires to the internal systems they will use daily — `portal.acme.example`, `hr.acme.example`, `helpdesk.acme.example`, `wiki.acme.example`, `vault.acme.example`, `packages.acme.example`, and `status.acme.example` (all fictional) — and to the canonical ACME people they will interact with during their first 90 days.

This module is the on-ramp for every other curriculum path. It is owned by HR Operations and coordinated by Anjali Iyer (Training Operations, `anjali.iyer@acme.example`) under VP HR Ananya Sharma (`ananya.sharma@acme.example`). Delivery is a mix of instructor-led sessions on day 1 and self-paced modules completed during week 1.

## 2. Learning Objectives

By the end of this module, the learner will be able to:

1. Articulate ACME Corp's mission, three-year strategy, and five operating values in their own words.
2. Recognise the company's history timeline from founding to present and identify the three product lines (ACME Cloud, ACME Intelligence, ACME Workspace) and their primary buyers.
3. Locate all canonical internal systems and complete single sign-on access to each from a managed workstation.
4. Describe the hybrid working model, office footprint (Hyderabad, Bengaluru, London, Seattle), and the expectations for office days versus remote days.
5. Identify the senior leadership team (CTO, VP HR, VP IT, CISO, Director AI/ML) and the HRBP assigned to their business unit.

## 3. Target Audience

| Role | Required? | Notes |
|---|---|---|
| All new hires (every department) | **Mandatory** | Must be completed during week 1, no exceptions. |
| Existing employees re-onboarding after ≥ 12 months leave | **Mandatory** | Refresh module within 5 business days of return. |
| Long-tenured employees (refresh) | Optional | Offered annually; recommended for those moving business units. |
| Contractors / vendors | Optional | A condensed 1-hour version is assigned if access to internal systems is granted. |

## 4. Prerequisites

- Microsoft 365 account activation — see [`../02-it/microsoft-365-account-activation.md`](../02-it/microsoft-365-account-activation.md).
- Microsoft Authenticator + MFA enrollment — see [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md).
- Corporate laptop / workstation issued and enrolled in Intune — see [`../02-it/laptop-and-workstation-allocation.md`](../02-it/laptop-and-workstation-allocation.md).
- Welcome letter acknowledgement — see [`../01-hr/welcome-letter.md`](../01-hr/welcome-letter.md).

## 5. Duration

**Total: 4 hours**, split as follows:

| Block | Duration | Modality |
|---|---|---|
| Live orientation session (day 1, hosted by Anjali Iyer) | 90 min | Instructor-led |
| Self-paced modules in `wiki.acme.example` (mission, values, products, offices) | 90 min | Self-paced |
| Hybrid working model walkthrough + office tour (or virtual tour for remote hires) | 30 min | Instructor-led |
| Quiz (5 questions) + Q&A | 30 min | Self-paced |

## 6. Outline of Topics Covered

### Hour 1 — Welcome & Company Story (Instructor-led)

- Welcome from VP HR Ananya Sharma and VP Engineering / CTO Sridhar Venkatesh.
- ACME Corp history: founding in Hyderabad, expansion to Bengaluru, London, Seattle.
- Mission, vision, and three-year strategy — see [`../00-company/mission-and-values.md`](../00-company/mission-and-values.md).
- Five operating values and what "living the values" looks like in daily work.
- Organisational structure overview — see [`../00-company/organizational-structure.md`](../00-company/organizational-structure.md).

### Hour 2 — Products, Customers, Markets (Self-paced)

- The three products: ACME Cloud (multi-cloud management), ACME Intelligence (agents, inference, ML), ACME Workspace (productivity & collaboration).
- Product deep dives are in [`../06-product/acme-cloud-overview.md`](../06-product/acme-cloud-overview.md), [`../06-product/acme-intelligence-overview.md`](../06-product/acme-intelligence-overview.md), [`../06-product/acme-workspace-overview.md`](../06-product/acme-workspace-overview.md).
- Customer segments: enterprise IT, regulated industries, large engineering organisations.
- How each business unit contributes and the canonical VP / Director / HRBP for each.

### Hour 3 — Internal Systems & Hybrid Working (Mixed)

- The seven canonical internal systems and their purposes (`portal`, `hr`, `helpdesk`, `wiki`, `vault`, `packages`, `status` — all `.acme.example`).
- Hybrid working model, office locations, and attendance expectations — see [`../00-company/office-locations-and-working-arrangements.md`](../00-company/office-locations-and-working-arrangements.md).
- Communication guidelines and channels — see [`../00-company/communication-guidelines.md`](../00-company/communication-guidelines.md).
- Employee support and escalation paths — see [`../00-company/employee-support-and-escalation.md`](../00-company/employee-support-and-escalation.md).

### Hour 4 — Assessment & Q&A (Self-paced)

- 5-question quiz covering mission, values, products, offices, and internal systems.
- Recorded Q&A from the live session, plus office-tour video for remote hires.
- Submission of the [`../08-forms/training-completion.md`](../08-forms/training-completion.md) form (TRN-001 row).

## 7. Format

**Mixed format.** Day-1 instructor-led session (90 min + 30 min walkthrough) plus self-paced wiki modules and quiz. Instructor-led sessions are held twice a month on the first and third Monday, with capacity for 25 participants each. Cohort assignments are made by the HR Onboarding Coordinator, Priya Nair (`priya.nair@acme.example`).

## 8. Completion Criteria

- Attendance recorded for the instructor-led blocks (in `hr.acme.example` training hub).
- Quiz score **≥ 80%** (4 of 5 correct). Retakes are unlimited but logged.
- Acknowledgement of the [`../00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md) and [`../00-company/mission-and-values.md`](../00-company/mission-and-values.md) recorded in the [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md) form.
- [`../08-forms/training-completion.md`](../08-forms/training-completion.md) submitted by the learner; sign-off recorded by Training Operations.

## 9. Follow-up / Next Steps

After ACME-TRN-001 is `COMPLETED`, the learner is unlocked into the next set of mandatory modules:

1. [`security-awareness.md`](./security-awareness.md) (ACME-TRN-002) — gating for repository access and AI tool license.
2. [`privacy-awareness.md`](./privacy-awareness.md) (ACME-TRN-003) — gating for any customer data access.
3. [`workplace-conduct.md`](./workplace-conduct.md) (ACME-TRN-009) — gating for full HR sign-off.

Engineers additionally proceed to [`engineering-orientation.md`](./engineering-orientation.md) (ACME-TRN-004). Role-specific paths are documented in [`../05-teams/`](../05-teams/).

## 10. Trainer / Owner

| Role | Person | Responsibility |
|---|---|---|
| Module owner | HR Operations (Ananya Sharma, VP HR) | Accountability, content strategy, annual review. |
| Training Operations coordinator | Anjali Iyer (`anjali.iyer@acme.example`) | Scheduling, delivery, attendance, quiz administration, sign-off. |
| HR Onboarding Coordinator | Priya Nair (`priya.nair@acme.example`) | Cohort assignment, day-1 logistics. |
| Executive sponsors | Sridhar Venkatesh (CTO), Ananya Sharma (VP HR) | Welcome remarks. |

For questions, escalation contacts are in [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md). Glossary terms are in [`../metadata/glossary.md`](../metadata/glossary.md).
