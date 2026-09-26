---
document_id: ACME-COMP-009
title: ACME Corp Employee Support and Escalation Directory
category: company
department: all
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [support, escalation, contacts]
---

# ACME Corp Employee Support and Escalation Directory

This document lists the standard escalation paths for common employee situations. For the full contact directory with fictional names, roles, and `@example.com` emails, see [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md).

## General Principles

1. **Start with the closest layer.** Most issues should be resolved with your onboarding buddy or direct manager first.
2. **Use the right channel.** IT issues go to the IT Helpdesk, not your manager. HR issues go to your HRBP, not your buddy.
3. **Document the issue.** Open a ticket whenever possible — this creates the audit trail that lets the next person help you.
4. **Escalate up the chain, not sideways.** If your buddy cannot help, escalate to your manager, then to the function's leadership.

## Issue → Owner → Escalation

| Issue Type | First Contact | Escalation 1 | Escalation 2 |
|------------|---------------|---------------|---------------|
| Laptop hardware failure | IT Helpdesk | IT Manager (Arjun Kapoor) | VP IT (Ramesh Khanna) |
| Account lockout / password reset | IT Helpdesk | Identity Engineer (Faisal Ahmed) | VP IT |
| Software installation not in approved list | IT Helpdesk ticket | IT Manager (Arjun Kapoor) | CISO (Rajan Mehta) |
| Phishing or suspicious email | Report via "Report Phishing" button in Outlook | SOC Lead (Fatima Sheikh) | CISO |
| Lost or stolen device | IT Helpdesk + Security on-call | CISO on-call | CEO |
| Customer data exposure concern | Information Security on-call | CISO (Rajan Mehta) | Legal (Hemant Joshi) |
| HR / people issue | HRBP (see [`00-company/organizational-structure.md`](./organizational-structure.md)) | HR Director (office-specific) | VP HR (Ananya Sharma) |
| Payroll issue | Payroll Lead (Sanjay Patel) | HR Director (office-specific) | CFO (Ritu Khanna) |
| Benefits enrollment | Benefits Lead (Deepika Rao) | HR Director (office-specific) | VP HR |
| Workplace conduct issue | HRBP or Anti-Harassment contact | HR Director | VP HR |
| Office access / facilities | Facilities contact (per office) | HR Director (office-specific) | COO (Helena Brooks) |
| Legal / contracts | Legal and Compliance (Hemant Joshi) | CFO (Ritu Khanna) | CEO |
| Production incident (engineering) | On-call for the affected team | Engineering Manager | VP Engineering |
| Security incident | Information Security on-call | CISO | CEO |

## Service Level Targets

| Request Type | First Response | Resolution Target |
|--------------|----------------|-------------------|
| IT — account lockout | 15 minutes (business hours) | 1 business hour |
| IT — standard laptop provisioning | 2 business days | 5 business days |
| IT — approved software install | 4 business hours | 1 business day |
| IT — non-approved software install | 3 business days | 1 business week (after security review) |
| HR — payroll correction | 1 business day | 5 business days |
| HR — benefits enrollment | 2 business days | 10 business days |
| Security — phishing report | 1 business hour | 1 business day |
| Security — suspected data exposure | 30 minutes | Per incident response plan |
| Engineering — production SEV1 | 5 minutes (page on-call) | Per on-call rotation |

## After-Hours Support

- IT Helpdesk: 24×5 (Mon–Fri 24 hours, closed weekends except for SEV1 production issues routed via on-call).
- Security on-call: 24×7 — page via the PagerDuty-style rotation in [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md).
- HR emergencies (workplace safety, harassment in progress): use the 24×7 HR emergency line listed in [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md).

## When You Cannot Reach Anyone

If you have an urgent issue and the standard escalation path is not responding:

1. **For production or security incidents,** page the on-call directly. See [`04-engineering/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md).
2. **For people-safety issues,** contact your office's HR Director (see [`00-company/organizational-structure.md`](./organizational-structure.md)) and, if necessary, local emergency services.
3. **For administrative lockout,** contact the IT Manager for your office (see contact directory) and your HRBP in parallel.

## Related Documents

- [`00-company/welcome-to-acme.md`](./welcome-to-acme.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- [`00-company/organizational-structure.md`](./organizational-structure.md)
- [`01-hr/employee-grievance-procedure.md`](../01-hr/employee-grievance-procedure.md)
- [`02-it/it-support-and-troubleshooting.md`](../02-it/it-support-and-troubleshooting.md)
- [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md)
- [`04-engineering/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md)
