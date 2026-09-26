---
document_id: ACME-SEC-008
title: Security Incident Reporting
category: security
department: information-security
applicable_roles: [all]
owner: Fatima Sheikh, SOC Lead
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, incident, reporting, soc, postmortem, fictional]
---

# Security Incident Reporting

> ACME Corp fictional onboarding library. Hostnames (`helpdesk.acme.example`, `status.acme.example`) and mailboxes (`security-incident@acme.example`, `security-oncall@acme.example`, `soc@acme.example`) are fictional. The pager / on-call contact details are illustrative.

## 1. Purpose

This document defines what counts as a security incident at ACME Corp, how to report one, the timelines that apply, and the roles everyone plays in handling one. Speed matters: a report made in the first hour is often the difference between a non-event and a customer-impacting breach. When in doubt, report — the SOC would rather triage a false alarm than miss a real one.

## 2. Scope

This applies to every ACME workforce member, contractor, and authorized third party. It covers any suspected or confirmed incident affecting ACME data, systems, accounts, devices, or facilities. It also covers incidents affecting customer data, even when the incident originates outside ACME (e.g., a customer's compromised account accessing ACME Cloud).

## 3. What Counts as an Incident

If any of the following is true, treat it as an incident and report it. This list is non-exhaustive — when in doubt, report.

| Category | Examples |
|----------|----------|
| **Account compromise** | An unexpected MFA push you didn't initiate. A sign-in from a country you're not in. An account lockout you didn't cause. A colleague's account behaving oddly. |
| **Phishing click** | You (or a colleague) clicked a link or opened an attachment in a suspicious email — even if nothing visible happened. |
| **Credential leak** | You realize you used an ACME password on a non-ACME site that has since been breached. You spot a credential in a GitHub commit. |
| **Lost or stolen device** | A corporate laptop, phone, or YubiKey is lost or stolen. See [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md). |
| **Data exposure** | Confidential or Restricted data is in a location it shouldn't be (public SharePoint, external email, unencrypted USB). Customer data is in a non-production environment without masking. |
| **Malware** | Defender for Endpoint flags something. Your laptop is behaving oddly. Cryptominer or ransomware indicators. |
| **Unauthorized access** | You see something you shouldn't be able to see. A colleague is using someone else's account. A service account is being used interactively. |
| **Misconfiguration** | A production S3 bucket / Blob container is set to public. A firewall rule is allowing 0.0.0.0/0 inbound. A conditional access policy was disabled. |
| **Social engineering** | Someone (call, chat, in person) tried to get you to reveal credentials, MFA codes, or to bypass a policy. |
| **AI tool misuse** | Customer data was entered into an external AI tool. See [`ai-tool-acceptable-use.md`](ai-tool-acceptable-use.md). |
| **Third-party incident** | A vendor or sub-processor notifies ACME of a breach affecting ACME data they held. |
| **Suspected — anything** | "I'm not sure, but…" — report it. |

If you are unsure whether something is an incident, **report it and let the SOC decide.** The cost of a false alarm is minutes; the cost of a missed report can be a breach.

## 4. How to Report

There are three reporting paths at ACME, ordered by urgency:

### 4.1 Suspected Incident — Routine (within 1 hour)

- Email `security-incident@acme.example` (fictional).
- Include: what you observed, when, what systems/accounts/data are involved, what you have done so far.
- The SOC triages within 1 business hour.

### 4.2 Confirmed or High-Impact Incident (immediately — page the on-call)

- **Page the security on-call** via the pager system (contact details in [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) and in `status.acme.example/oncall`, fictional URL).
- The pager is monitored 24×7; the on-call SOC engineer acknowledges within 5 minutes.
- Also email `security-oncall@acme.example` (fictional) for the record.

### 4.3 Urgent — Someone's Safety at Risk

- If the incident involves a threat to a person's physical safety, contact local emergency services first (Hyderabad: 100; London: 999; Seattle: 911), then the ACME pager.
- If the incident involves illegal content (e.g., child sexual abuse material), do not investigate further — preserve the device state, report to the SOC, and the SOC will coordinate with law enforcement.

### 4.4 What to Include in the Report

| Field | Example |
|-------|---------|
| Reporter name | `<your-name>` |
| Time observed | 2026-09-15 14:32 IST |
| What happened | "I clicked a link in an email claiming to be from ACME HR; my browser redirected to `hr-acme.example/login` and I entered my ACME password" |
| Accounts involved | `<your-corporate-email>` |
| Systems involved | "My corporate laptop, Outlook" |
| Data potentially involved | "My ACME password, possibly an MFA push" |
| Actions taken so far | "Disconnected laptop from Wi-Fi, denied the MFA push" |

## 5. Timelines

| Event | Timeline |
|-------|----------|
| Reporter reports a suspected incident | Within 1 hour of becoming aware |
| SOC acknowledges the report | Within 1 business hour (routine) / 5 minutes (paged) |
| SOC initial triage complete | Within 2 hours of acknowledgement |
| Incident Commander assigned | For confirmed SEV1/SEV2 incidents, within 30 minutes of triage |
| Customer notification (if customer data involved) | Within 72 hours of confirmation, per [`customer-data-handling.md`](customer-data-handling.md) |
| Containment target | Within 24 hours for SEV1; within 72 hours for SEV2 |
| Postmortem published | Within 10 business days of incident closure |

## 6. Roles

| Role | Who | Responsibility |
|------|-----|----------------|
| **Reporter** | The person who observed the incident | Reports promptly. Cooperates with the investigation. Does not attempt vigilante remediation. |
| **SOC On-Call** | SOC Engineer on rotation (rotates weekly) | Acknowledges the page. Triages. Activates the Incident Commander if SEV1/SEV2. |
| **Incident Commander (IC)** | Designated senior SOC or Security team member | Owns the incident response. Coordinates containment, eradication, recovery. Communicates to stakeholders. Authorizes emergency actions (break-glass, etc.). |
| **SOC Lead** | `Fatima Sheikh` | Owns the SOC rotation. Reviews postmortems. Coordinates with external responders. |
| **IAM Engineer** | `Abhishek Verma` | Executes identity actions (password reset, session revoke, conditional access changes, account disable). |
| **GRC Analyst** | `Karthik Subramanian` | Maintains the incident register. Tracks regulatory notification obligations. Coordinates customer notification language. |
| **CISO** | `Rajan Mehta` | Final accountable owner. Approves customer notification. Approves external regulator engagement. |
| **Communications Lead** | Designee from Corporate Comms | Owns external statements (per ACME incident communications protocol). |
| **Customer-facing Lead** | Customer Success Manager | Notifies affected customers per the contract terms. |

## 7. Response Process

ACME follows the standard NIST 800-61 lifecycle:

1. **Preparation** — Detection tools (Defender for Endpoint, Entra ID Identity Protection, Purview DLP, cloud CSPM) continuously monitor. Workforce is trained (see [`phishing-awareness.md`](phishing-awareness.md)).
2. **Detection & Analysis** — A signal from the SOC tools or a report from a workforce member triggers triage. The SOC validates and assigns a severity.
3. **Containment** — Short-term: isolate the affected device (Defender network isolation), revoke the session, disable the account. Long-term: rotate affected credentials, apply conditional access blocks, purge phishing emails tenant-wide.
4. **Eradication** — Remove malware, patch the underlying vulnerability, remove unauthorized access.
5. **Recovery** — Restore services from known-good backups. Monitor for re-infection.
6. **Post-Incident Activity** — Postmortem (§8). Update detections. Track remediation to closure.

## 8. Postmortem Requirement

Every confirmed SEV1 or SEV2 incident produces a **blameless postmortem** within 10 business days of closure. The postmortem:

- Is owned by the Incident Commander.
- Is reviewed by the SOC Lead (`Fatima Sheikh`) and the CISO (`Rajan Mehta`).
- Documents the timeline, root cause, contributing factors, impact, and action items.
- Is published to the ACME Wiki at `wiki.acme.example/security/postmortems` (fictional) at the **Confidential** classification.
- Has action items tracked to closure by the GRC Analyst.

Postmortems are blameless: the goal is to fix the system, not to find a person to blame. People are never named as root causes — failures of process, tooling, or design are.

## 9. What Not to Do

- **Do not investigate alone.** Report and let the SOC drive.
- **Do not delete evidence.** Do not "clean up" the suspicious email or uninstall the suspicious app. The SOC needs the evidence.
- **Do not communicate externally.** No tweets, no LinkedIn posts, no customer emails. Communications are coordinated by the Comms Lead.
- **Do not name customers in chat.** Customer-impacting incidents are coordinated through the GRC Analyst to ensure contractual and regulatory wording.
- **Do not reboot a potentially-compromised device** unless instructed by the SOC — you may destroy volatile evidence in memory.

## 10. Responsibilities

| Role | Responsibility |
|------|----------------|
| **Reporter** | Reports within 1 hour. Cooperates. Does not interfere. |
| **SOC On-Call** | Acknowledges within SLA. Triages. Activates IC. |
| **Incident Commander** | Owns the response. Authorizes emergency actions. |
| **SOC Lead** (`Fatima Sheikh`) | Owns the SOC rotation. Reviews postmortems. |
| **IAM Engineer** (`Abhishek Verma`) | Executes identity actions. |
| **GRC Analyst** (`Karthik Subramanian`) | Maintains the incident register. Coordinates notifications. |
| **CISO** (`Rajan Mehta`) | Final accountable owner. Approves customer notifications. |
| **Every workforce member** | Knows how to report. Reports promptly. Cooperates with investigations. |

## 11. Enforcement

- Failure to report a known incident within the SLA is a violation of [`acceptable-use-policy.md`](acceptable-use-policy.md) and [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md) and may result in disciplinary action up to termination.
- Tampering with evidence is treated as gross misconduct.
- The SOC's no-blame stance covers reporters and even those who caused an incident by mistake — the goal is to learn, not to punish. Gross negligence or malicious action is a separate matter handled by HR.

## 12. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`acceptable-use-policy.md`](acceptable-use-policy.md) — What counts as a violation.
- [`phishing-awareness.md`](phishing-awareness.md) — The most common incident type.
- [`password-and-mfa-requirements.md`](password-and-mfa-requirements.md) — What the IAM Engineer will do during an incident.
- [`identity-and-access-management.md`](identity-and-access-management.md) — Identity actions during containment.
- [`data-classification.md`](data-classification.md) — Drives notification obligations.
- [`customer-data-handling.md`](customer-data-handling.md) — Customer notification obligations and timelines.
- [`secrets-management.md`](secrets-management.md) — Secret rotation during containment.
- [`../02-it/lost-or-stolen-device-reporting.md`](../02-it/lost-or-stolen-device-reporting.md) — Lost device workflow.
- [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) — If the incident involves an employee departure.
- [`../00-company/employee-support-and-escalation.md`](../00-company/employee-support-and-escalation.md) — Escalation path.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — SOC on-call pager details.
- [`../metadata/glossary.md`](../metadata/glossary.md) — SEV1/SEV2, SOC, IC definitions.
