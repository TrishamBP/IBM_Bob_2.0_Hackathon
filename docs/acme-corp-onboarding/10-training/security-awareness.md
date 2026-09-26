---
document_id: ACME-TRN-002
title: Security Awareness Training
category: training
department: security
applicable_roles: [all]
owner: Security Operations (CISO Office)
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [training, security, awareness, mandatory]
---

# Security Awareness Training (ACME-TRN-002)

> Fictional document. All systems, links, and addresses are illustrative.

## 1. Module Overview

Security Awareness Training is the gating security module at ACME Corp. Every employee — engineer, sales, HR, finance, support — must complete this module before they can receive repository write access, GitHub Copilot Business license, customer data access, or on-call eligibility. The module consolidates the canonical security policies (information security, acceptable use, password & MFA, phishing, data classification, incident reporting, BYOD, encryption, clean desk, source code security, secrets management, OSS dependency security, AI tool acceptable use, and customer data handling) into a single learnable curriculum with realistic scenarios.

The module is owned by the CISO office (Rajan Mehta, `rajan.mehta@acme.example`) and delivered by the Security GRC team. Content lives in `wiki.acme.example`; assessments live in `hr.acme.example`. Recertification is annual.

## 2. Learning Objectives

By the end of this module, the learner will be able to:

1. Recall the four ACME data classification tiers (Public, Internal, Confidential, Restricted) and identify the correct handling, storage, and transmission controls for each.
2. Demonstrate correct password and MFA hygiene on a managed workstation, including recovery procedures for a lost Microsoft Authenticator device.
3. Identify a phishing attempt in email, chat, or SMS, and execute the correct reporting workflow within 24 hours.
4. Explain the least-privilege access model and reject access requests that violate it.
5. Identify a security incident, classify its severity, and open a report via `helpdesk.acme.example` or call `security-oncall@acme.example` for P1/P2 events.
6. Recognise the rules for source code security, secrets management, OSS dependency hygiene, and AI tool acceptable use — including what must never be typed into an AI assistant.

## 3. Target Audience

| Role | Required? | Notes |
|---|---|---|
| All employees | **Mandatory** | No role is exempt. |
| Engineers (all disciplines) | **Mandatory** | Engineer-specific scenarios emphasised; gates repo write access. |
| Contractors with internal-system access | **Mandatory** | Condensed 2-hour version; no on-call content. |
| Board members / observers | Optional | A condensed briefing is offered annually by the CISO. |

## 4. Prerequisites

- Completion of [`company-orientation.md`](./company-orientation.md) (ACME-TRN-001).
- M365 account active and Microsoft Authenticator enrolled — see [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md).
- Corporate VPN configured — see [`../02-it/corporate-vpn-configuration.md`](../02-it/corporate-vpn-configuration.md).
- Password manager configured — see [`../02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md).
- Acknowledgement of confidentiality agreement — see [`../03-security/confidentiality-agreement.md`](../03-security/confidentiality-agreement.md).

## 5. Duration

**Total: 4 hours** (3 hours self-paced + 1 hour live phishing-simulation debrief).

| Block | Duration | Modality |
|---|---|---|
| Self-paced policy modules | 120 min | Self-paced in `wiki.acme.example` |
| Scenario labs (data classification, incident reporting, secrets) | 40 min | Self-paced |
| 20-question assessment | 20 min | Self-paced in `hr.acme.example` |
| Live phishing simulation debrief | 60 min | Instructor-led, monthly cohort by GRC Analyst |

## 6. Outline of Topics Covered

### Block A — Policy Foundations (Self-paced, 70 min)

- Information security policy — see [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md).
- Acceptable use policy — see [`../03-security/acceptable-use-policy.md`](../03-security/acceptable-use-policy.md).
- Identity & access management — see [`../03-security/identity-and-access-management.md`](../03-security/identity-and-access-management.md).
- Least-privilege access — see [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).
- Password and MFA requirements — see [`../03-security/password-and-mfa-requirements.md`](../03-security/password-and-mfa-requirements.md).

### Block B — Phishing & Social Engineering (Self-paced, 40 min)

- Phishing awareness — see [`../03-security/phishing-awareness.md`](../03-security/phishing-awareness.md).
- Common lures (credential reset, vendor invoice, executive impersonation).
- How to use the "Report Phishing" button in Outlook.
- When to escalate to `security-oncall@acme.example`.

### Block C — Data & Devices (Self-paced, 40 min)

- Data classification — see [`../03-security/data-classification.md`](../03-security/data-classification.md).
- Customer data handling — see [`../03-security/customer-data-handling.md`](../03-security/customer-data-handling.md).
- BYOD policy — see [`../03-security/byod-policy.md`](../03-security/byod-policy.md).
- Device encryption — see [`../03-security/device-encryption.md`](../03-security/device-encryption.md).
- Clean desk policy — see [`../03-security/clean-desk-policy.md`](../03-security/clean-desk-policy.md).

### Block D — Engineering-specific Controls (Self-paced, 30 min)

- Source code security — see [`../03-security/source-code-security.md`](../03-security/source-code-security.md).
- Secrets management — see [`../03-security/secrets-management.md`](../03-security/secrets-management.md).
- Open-source dependency security — see [`../03-security/open-source-dependency-security.md`](../03-security/open-source-dependency-security.md).
- AI tool acceptable use — see [`../03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md).

### Block E — Incident Response (Self-paced, 20 min)

- Security incident reporting — see [`../03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md).
- Severity definitions (P1/P2/P3/P4) and on-call handoff.
- Evidence preservation and chain of custody.

### Block F — Live Phishing Simulation Debrief (Instructor-led, 60 min)

- Review of monthly simulated phishing campaign outcomes.
- Dissection of the most-clicked lure of the quarter.
- Live red-teaming demonstration (sanitised).
- Q&A with the GRC team.

## 7. Format

**Mixed.** The bulk of the content is self-paced in `wiki.acme.example`. The phishing-simulation debrief is instructor-led and scheduled monthly by the GRC team. Engineers must complete all six blocks; non-engineers may skip Block D but must complete an alternate 20-minute "AI tool acceptable use" mini-module.

## 8. Completion Criteria

- All six blocks marked `COMPLETED` in the LMS.
- 20-question final quiz score **≥ 85%** (≥ 17 correct). Retakes are unlimited but logged; after two failures the GRC Analyst assigns a 1:1 coaching session.
- Phishing simulation reported (when sent) within 24 hours of receipt.
- Acknowledgement of the information security policy, acceptable use policy, and password/MFA requirements recorded via [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md).
- [`../08-forms/training-completion.md`](../08-forms/training-completion.md) submitted and signed off by Security GRC.

**Annual recertification is mandatory.** Recertification is a 60-minute refresher plus a 15-question quiz (≥ 85%) and one phishing simulation. Recertification is scheduled automatically by `hr.acme.example` 11 months after initial completion.

## 9. Follow-up / Next Steps

- For engineers: unlocks [`ai-coding-assistant-usage.md`](./ai-coding-assistant-usage.md) (ACME-TRN-006) and repository write access requests.
- For all: unlocks [`privacy-awareness.md`](./privacy-awareness.md) (ACME-TRN-003).
- Annual refresher schedule is configured in HR Hub — see [`../07-workflows/security-training.md`](../07-workflows/security-training.md) task SEC-009.
- Security-incident-response deep-dive is offered as an elective for on-call engineers — see [`../04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md).

## 10. Trainer / Owner

| Role | Person | Responsibility |
|---|---|---|
| Module owner | Rajan Mehta, CISO (`rajan.mehta@acme.example`) | Accountability, policy alignment, annual review. |
| Delivery lead | Security GRC Analyst (under CISO office) | Cohort scheduling, quiz administration, debrief facilitation. |
| Phishing simulation operator | Security GRC team | Campaign design, send cadence, outcome reporting. |
| Acknowledgement coordinator | Anjali Iyer, Training Operations (`anjali.iyer@acme.example`) | LMS tracking, sign-off in [`../08-forms/training-completion.md`](../08-forms/training-completion.md). |

For escalation contacts, see [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md). Glossary terms are in [`../metadata/glossary.md`](../metadata/glossary.md).
