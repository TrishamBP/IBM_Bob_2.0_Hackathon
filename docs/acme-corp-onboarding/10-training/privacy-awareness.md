---
document_id: ACME-TRN-003
title: Privacy Awareness Training
category: training
department: security
applicable_roles: [all]
owner: Security Operations (CISO Office)
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [training, privacy, gdpr, dpdp, ccpa, mandatory]
---

# Privacy Awareness Training (ACME-TRN-003)

> Fictional document. All systems, links, and addresses are illustrative.

## 1. Module Overview

Privacy Awareness Training is the mandatory privacy curriculum for every ACME Corp employee. It grounds the learner in the privacy principles that govern how ACME collects, processes, stores, shares, and deletes personal data — whether that data belongs to employees, candidates, customers, or partners. The module covers the three primary regulatory regimes under which ACME operates: the EU/UK General Data Protection Regulation (GDPR), the Indian Digital Personal Data Protection Act (DPDP), and the California Consumer Privacy Act (CCPA). It also covers data subject rights, data minimisation, lawful basis, the prohibition on surveillance without cause, and the operational handling of customer data.

This module is owned by the CISO office (Rajan Mehta, `rajan.mehta@acme.example`) in partnership with VP HR Ananya Sharma (`ananya.sharma@acme.example`), and coordinated by Anjali Iyer, Training Operations (`anjali.iyer@acme.example`). It gates access to any system that stores personal data, including `hr.acme.example` and customer-data systems used by support and engineering.

## 2. Learning Objectives

By the end of this module, the learner will be able to:

1. Name the three primary regulatory regimes ACME complies with (GDPR, DPDP, CCPA) and summarise the core obligation of each in one sentence.
2. List the eight standard data subject rights (access, rectification, erasure, restriction, portability, objection, withdrawal of consent, rights related to automated decision-making) and route each correctly.
3. Apply the data minimisation principle to a sample data collection scenario and identify which fields to drop.
4. Identify the six lawful bases for processing and select the correct basis for a given ACME workflow.
5. Recognise when a "no surveillance without cause" boundary is being tested and refuse or escalate the request.
6. Demonstrate correct customer-data handling per [`../03-security/customer-data-handling.md`](../03-security/customer-data-handling.md) including redaction, retention, and cross-border transfer rules.

## 3. Target Audience

| Role | Required? | Notes |
|---|---|---|
| All employees | **Mandatory** | Gates personal-data system access. |
| Engineers handling customer telemetry or support data | **Mandatory** | Extended scenario block on customer-data redaction. |
| HR / People team | **Mandatory** | Extended scenario block on employee personal data and DSAR handling. |
| Sales / customer-facing roles | **Mandatory** | Extended scenario block on consent capture during demos and POCs. |
| Contractors | **Mandatory** | Condensed 90-minute version if personal-data access is required. |

## 4. Prerequisites

- Completion of [`company-orientation.md`](./company-orientation.md) (ACME-TRN-001).
- Completion of [`security-awareness.md`](./security-awareness.md) (ACME-TRN-002).
- Acknowledgement of the privacy acknowledgement — see [`../03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md).

## 5. Duration

**Total: 2 hours**, all self-paced in `wiki.acme.example` and `hr.acme.example`.

| Block | Duration | Modality |
|---|---|---|
| Privacy principles & regulatory overview | 40 min | Self-paced |
| Data subject rights & DSAR workflow | 25 min | Self-paced |
| Data minimisation & lawful basis labs | 25 min | Self-paced |
| No-surveillance-without-cause module | 15 min | Self-paced |
| Customer data handling scenarios | 15 min | Self-paced |
| 15-question assessment | 20 min | Self-paced |

## 6. Outline of Topics Covered

### Block A — Privacy Principles & Regulatory Landscape (40 min)

- Why privacy matters at ACME: trust, regulatory exposure, customer contracts.
- GDPR (EU/UK) — scope, key articles, ACME obligations as a data controller and processor.
- DPDP (India) — scope, lawful bases, Data Protection Board enforcement.
- CCPA / CPRA (California) — scope, consumer rights, opt-out of sale/share.
- Privacy principles: lawfulness, fairness, transparency, purpose limitation, data minimisation, accuracy, storage limitation, integrity & confidentiality, accountability.
- Cross-reference: [`../03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md).

### Block B — Data Subject Rights & DSAR Workflow (25 min)

- The eight standard data subject rights and their boundaries.
- How to recognise an inbound DSAR (email, ticket, legal letter, verbal).
- Routing: all DSARs go to `privacy@acme.example` within 24 hours; never act on a DSAR directly.
- Timelines: 30 days (GDPR), 45 days (CCPA), 30 days (DPDP). Clock starts on receipt.

### Block C — Data Minimisation & Lawful Basis Labs (25 min)

- Six lawful bases: consent, contract, legal obligation, vital interests, public task, legitimate interests.
- Hands-on lab: review a sample candidate-intake form, identify over-collection, propose minimised version.
- Hands-on lab: classify processing activities against lawful basis and document each.

### Block D — No Surveillance Without Cause (15 min)

- ACME's policy: no monitoring of employee email, chat, location, keystrokes, or web cam without (a) a documented lawful basis and (b) prior approval from HR + CISO office.
- What to do if a manager asks for "just a quick check" of a team member's chat.
- How to escalate: HRBP, CISO office, or `privacy@acme.example`.

### Block E — Customer Data Handling Scenarios (15 min)

- Customer data classification and handling — see [`../03-security/customer-data-handling.md`](../03-security/customer-data-handling.md).
- Redaction, retention, and cross-border transfer controls.
- When to refuse to accept customer data outside an approved channel.

### Block F — Assessment (20 min)

- 15-question quiz in `hr.acme.example`. Topics weighted: regulatory basics 30%, DSAR 20%, minimisation 20%, surveillance 15%, customer data 15%.

## 7. Format

**Self-paced.** All blocks are delivered through `wiki.acme.example` with the assessment in `hr.acme.example`. A live Q&A clinic is offered monthly by the privacy team and is optional; the clinic recording is posted within five business days.

## 8. Completion Criteria

- All five content blocks marked `COMPLETED` in the LMS.
- 15-question quiz score **≥ 85%** (≥ 13 correct). Retakes are unlimited but logged.
- Acknowledgement of the privacy acknowledgement — see [`../03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md) — recorded via [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md).
- [`../08-forms/training-completion.md`](../08-forms/training-completion.md) submitted by the learner and signed off by Training Operations.

**Annual recertification** is mandatory: a 30-minute refresher plus a 10-question quiz (≥ 85%) scheduled automatically 11 months after completion.

## 9. Follow-up / Next Steps

- For all: unlocks customer-data system access requests (via [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md)).
- For engineers: proceeds to [`engineering-orientation.md`](./engineering-orientation.md) (ACME-TRN-004).
- For HR / People: enables DSAR-handling permissions in `hr.acme.example`.
- For privacy champions (one per business unit): optional [`../03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md) deep-dive elective.

## 10. Trainer / Owner

| Role | Person | Responsibility |
|---|---|---|
| Module owner | Rajan Mehta, CISO (`rajan.mehta@acme.example`) | Accountability, regulatory alignment. |
| Co-owner (people data) | Ananya Sharma, VP HR (`ananya.sharma@acme.example`) | Employee/candidate data scenarios. |
| Delivery coordinator | Anjali Iyer, Training Operations (`anjali.iyer@acme.example`) | Scheduling, LMS tracking, sign-off. |
| Privacy team contact | `privacy@acme.example` | DSAR routing, escalations, monthly clinic. |

Escalation contacts are in [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md). Glossary terms are in [`../metadata/glossary.md`](../metadata/glossary.md).
