---
document_id: ACME-COMP-007
title: ACME Corp Communication Guidelines
category: company
department: all
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [communication, etiquette, async, channels]
---

# ACME Corp Communication Guidelines

These guidelines describe how ACME employees are expected to communicate internally, with each other, and with customers. The goal is not to be prescriptive — it is to make sure that a 3,500-person company can collaborate asynchronously across four time zones without information getting lost.

## Default to Asynchronous

ACME operates asynchronously by default. We work across IST, GMT/BST, and PT; expecting same-hour responses across regions is unrealistic and creates an inequitable environment for employees outside the originating time zone. The corollary: written communication matters. If a decision is not written down, it did not happen.

The acceptable response time defaults are:

| Channel | Expected Response (Same Region) | Expected Response (Cross-Region) |
|---------|-----------------------------------|----------------------------------|
| Microsoft Teams chat | 4 business hours | 1 business day |
| Microsoft Teams channel post | 1 business day | 2 business days |
| Email | 1 business day | 2 business days |
| Pull request review request | 2 business days | 3 business days |
| Production incident (SEV1/SEV2) | per [`04-engineering/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md) | per on-call |

Use synchronous meetings when the cost of the meeting is less than the cost of misalignment. We do not need a meeting for status updates.

## Channel Selection

ACME uses a fixed set of communication channels. Using the wrong channel is a real cost.

| Channel | Use For |
|---------|---------|
| Microsoft Teams chat (1:1 or small group, ≤8 people) | Quick clarifications, real-time coordination during incidents, social. |
| Microsoft Teams channel | Team and project discussions that should be discoverable by the team. |
| Email (Outlook) | External communication, formal approvals, customer-facing correspondence, anything that needs an audit trail. |
| Pull request comments | Code-specific discussion. Never use chat for code review. |
| Wiki (wiki.acme.example) | Long-form documentation, design docs, runbooks. |
| ACME Portal announcements | Company-wide announcements (executive updates, policy changes, all-hands). |
| GitHub Enterprise issue | Engineering tasks, bugs, feature work in a repo. |

When in doubt, ask: **"Where would the next person to join the team look for this?"** Write it there.

## Etiquette

- **Use clear subject lines.** "Quick question" is not a subject line. "Decision needed: staging region for ACME Intelligence EU customers" is.
- **Make asks explicit.** "Let me know what you think" is ambiguous. "Can you approve the API contract in the linked PR by Wednesday 17:00 IST?" is not.
- **Cite context.** Link the design doc, the incident, the customer record. Do not assume your reader remembers.
- **Respect time zones.** Schedule messages to send during the recipient's business hours when possible. Use Teams scheduled-send.
- **Default to public channels.** Private chats do not scale. If a discussion would benefit the team, move it to a channel.

## Customer Communication

Customer-facing communication must go through approved channels (Salesforce CRM and the Customer Support portal). Do not email customers from your personal mailbox. Always use your `@acme.example` address. Customer commitments (roadmap, dates, scope) require Sales or Product Management approval — see [`00-company/employee-support-and-escalation.md`](./employee-support-and-escalation.md).

## Confidential and Sensitive Topics

Confidential topics (customer data, security incidents, employee relations, M&A) must not be discussed in public channels. Use:

- **Email with restricted distribution** for HR or legal topics.
- **Microsoft Teams private channels** for incident bridges (created on demand by the on-call lead).
- **ACME Vault** for secrets and credentials (never email or chat). See [`03-security/secrets-management.md`](../03-security/secrets-management.md).

## Meetings

- Default meeting length is 25 minutes, not 30. Leave 5 minutes of breathing room between meetings.
- Default to no-camera meetings unless body language matters (1:1s, design reviews, customer calls).
- Every meeting must have an agenda in the invite description, at minimum a 2-bullet outline.
- Every meeting must have a notes owner. Notes are posted to the associated Wiki page within 24 hours.
- Recordings require explicit consent of all attendees and are stored in the approved SharePoint folder.

## Escalation

If you cannot reach someone through normal channels and the matter is urgent:

1. For **production incidents**, page the on-call (see [`04-engineering/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md)).
2. For **security incidents**, see [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md).
3. For **HR or people issues**, see [`01-hr/employee-grievance-procedure.md`](../01-hr/employee-grievance-procedure.md).
4. For **everything else**, see [`00-company/employee-support-and-escalation.md`](./employee-support-and-escalation.md).

## Related Documents

- [`00-company/welcome-to-acme.md`](./welcome-to-acme.md)
- [`00-company/mission-and-values.md`](./mission-and-values.md)
- [`02-it/microsoft-teams-setup.md`](../02-it/microsoft-teams-setup.md)
- [`02-it/outlook-and-company-calendar-setup.md`](../02-it/outlook-and-company-calendar-setup.md)
- [`03-security/secrets-management.md`](../03-security/secrets-management.md)
- [`01-hr/employee-grievance-procedure.md`](../01-hr/employee-grievance-procedure.md)
