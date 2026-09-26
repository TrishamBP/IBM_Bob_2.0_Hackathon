---
document_id: ACME-TEAM-013
title: ACME Corp HR Specialist Onboarding
category: team-onboarding
department: human-resources
applicable_roles: [hr-specialist]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [team-onboarding, hr-specialist]
---

# ACME Corp HR Specialist Onboarding

Welcome to the **Human Resources** organization at ACME Corp. This guide is your single reference for the first 90 days as an HR Specialist supporting ACME employees across our four offices and remote workforce. It assumes you have already completed [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) and [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md).

> ACME Corp is a fictional company. All names, repositories, hosts, and systems referenced here are illustrative and use the `.example` domain. Do not attempt to reach any URL.

## 1. Team Overview

| Field | Value |
|-------|-------|
| Team name | Human Resources |
| Reports up to | Ananya Sharma (VP HR), who reports to the CEO office |
| Primary offices | Hyderabad (Ananya's home office and HR headquarters), with HR specialists distributed across Bengaluru, London, Seattle to support regional employees |
| Primary tooling | Workday (HRIS), HR Hub at `hr.acme.example` (internal HR portal), Microsoft 365, DocuSign (HR forms), Leena.ai (HR chatbot for employee self-service) |
| Primary channel | `#hr-team` (Microsoft Teams); `#hr-help` for employee questions |

**Mission.** Deliver HR operations excellence across the employee lifecycle — onboarding, leave and time-off, payroll and benefits coordination, employee relations, performance management administration, and policy stewardship. HR Specialists are the human face of ACME's people operations.

**Charter.** Owns employee lifecycle operations, policy administration, employee records, leave coordination, benefits enrollment support, performance-review administration, and the HR knowledge base. Does **not** own recruiting (Talent Acquisition owns that, also under VP HR), compensation strategy (Total Rewards owns that), or workplace investigations (HRBP team owns that — HR Specialists support but do not lead).

**Customers.** All ACME employees (primary), managers and leaders (for performance and people-management operations), Talent Acquisition (handoff from recruiting), Payroll (data handoff), Legal (employment-law questions).

## 2. Reporting Manager

- **VP:** Ananya Sharma (ananya.sharma@acme.example, Hyderabad office, hybrid).
- Ananya reports to the CEO office.
- Your standing 1:1 is 30 minutes weekly.
- Reporting line is recorded at `hr.acme.example` under your profile.
- You will also be assigned to one of three HR pods (India, EMEA, Americas) and to one or more HR operations areas (onboarding, leave, benefits, performance, employee relations support).

## 3. Onboarding Buddy

- **Buddy:** Kavya Krishnan (kavya.krishnan@acme.example), HRBP, Cloud/Workspace HRBP. Kavya serves as your buddy for the first 90 days.
- Kavya is your peer mentor for the first 90 days — Workday conventions, HR Hub portal workflow, leave coordination patterns, employee-relations escalation patterns.
- Buddy commitment: 2 hours per day for the first 2 weeks; 1 hour per day for weeks 3–6; ad-hoc thereafter.
- See [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) for the buddy program's expectations.

## 4. Required Documents (Week 1)

Read each of the following in your first week. Kavya will check progress during your week-1 1:1.

- [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md)
- [`00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- [`00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- [`00-company/communication-guidelines.md`](../00-company/communication-guidelines.md)
- [`00-company/office-locations-and-working-arrangements.md`](../00-company/office-locations-and-working-arrangements.md)
- [`01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md)
- [`01-hr/anti-harassment-policy.md`](../01-hr/anti-harassment-policy.md)
- [`01-hr/employee-grievance-procedure.md`](../01-hr/employee-grievance-procedure.md)
- [`01-hr/leave-and-attendance-policy.md`](../01-hr/leave-and-attendance-policy.md)
- [`01-hr/probation-and-confirmation-process.md`](../01-hr/probation-and-confirmation-process.md)
- [`01-hr/performance-review-policy.md`](../01-hr/performance-review-policy.md)
- [`01-hr/remote-and-hybrid-working-policy.md`](../01-hr/remote-and-hybrid-working-policy.md)
- [`01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md)
- [`03-security/information-security-policy.md`](../03-security/information-security-policy.md)
- [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md)
- [`03-security/confidentiality-agreement.md`](../03-security/confidentiality-agreement.md)
- [`03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md)
- [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md)
- [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md)
- [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md)

## 5. Required Software

Install only the approved tools below. Anything else requires a software access request via [`08-forms/software-access-request.md`](../08-forms/software-access-request.md). See [`02-it/approved-software-installation.md`](../02-it/approved-software-installation.md) for the binding policy.

**Workstation baseline (installed by IT before Day 1):**
- Windows 11 Enterprise or macOS 14+
- Microsoft 365 — Outlook, Teams, OneDrive, Word, Excel, PowerPoint
- Microsoft Authenticator, Corporate VPN, 1Password, Microsoft Defender for Endpoint

**HR-specific tools (provisioned via Entra SSO):**
- Workday (HRIS) — `HR Specialist` role at `workday.internal.acme.example`
- HR Hub (internal HR portal) — `Editor` at `hr.acme.example`
- Leena.ai (HR chatbot admin) — `Editor` for content authoring
- DocuSign (HR forms) — `Sender` seat
- Microsoft Forms (pulse surveys) — already provisioned via M365
- Power BI (HR dashboards) — `Viewer` for org-wide dashboards, `Contributor` for your pod

You will **not** receive access to engineering repositories or developer tooling. See section 7.

## 6. Approved AI Tools

Per the role eligibility matrix in [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md), HR Specialists are **not entitled** to ACME engineering AI tools:

| Tool | Entitlement | Notes |
|------|-------------|-------|
| GitHub Copilot Business | **No** | HR Specialists do not write code and do not receive a Copilot seat. Do not request one via [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md) — it will be declined. |
| Internal ACME Intelligence sandbox | **No** | Not provisioned. |

If you need AI assistance for writing (HR communications, knowledge-base articles, internal docs), use Microsoft Copilot for Microsoft 365, governed by [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md). Workday's built-in AI features are governed by Workday enterprise policy and the ACME acceptable-use policy.

Do **not** enter employee-identifying information, salary data, performance review content, or investigation notes into public AI tools — see [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) and [`03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md). These are Confidential or Restricted per [`03-security/data-classification.md`](../03-security/data-classification.md).

## 7. Required Repositories

You will **not** receive access to any ACME engineering repositories. HR is a non-engineering function — repository access is restricted per [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) and the access tier matrix in [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md).

If you need to reference an HR policy or form, use:

- The HR knowledge base at `hr.acme.example` (you have full editor access)
- The HR Hub document library
- This onboarding library (the canonical source)

If you have a documented business need for read-only access to a specific repository (e.g., to update HR documentation that lives in a repo), your manager may file a [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md) — these are rare exceptions and require CISO designate review.

## 8. Required Access Permissions

On Day 1, IT Onboarding (Geetha Iyer, `geetha.iyer@acme.example) provisions the following Entra ID groups. Verify each in the My Apps portal at `myapps.acme.example`.

| Entra ID group | Purpose |
|----------------|---------|
| `HR-Operations` | Membership in the HR org; Workday, Leena.ai, Power BI HR seats. |
| `Workday-HR-Specialist` | Workday role with employee records CRUD for your pod's region. |
| `HR-Hub-Editor` | Editor access to the HR Hub portal at `hr.acme.example`. |
| `Leena-AI-Editor` | Editor access to the HR chatbot content for self-service. |
| `DocuSign-HR-Sender` | Sender seat for HR forms (offer letters, separation docs, acknowledgements). |
| `PowerBI-HR-Contributor` | Contributor access to your pod's HR dashboards. |
| `Employee-Data-Processor-HR` | Access to employee PII in Workday within your pod's regional scope. |
| `Confidential-Data-Access` | Marks your account as authorized for Confidential data handling per [`03-security/data-classification.md`](../03-security/data-classification.md). |

Additional tools (auto-provisioned):

- **Microsoft Forms** — already via M365.
- **Power BI** — `Contributor` for pod dashboards.

Investigation-related access (employee grievance, performance improvement plan documents) is **not** granted at onboarding — those require an active investigation case and Ananya's sign-off. See [`01-hr/employee-grievance-procedure.md`](../01-hr/employee-grievance-procedure.md).

Cloud production, cluster, and Vault access is **not** granted.

## 9. Training Requirements

Complete the following training in your first 30 days. All training is tracked in your learning transcript at `hr.acme.example/learning`.

| Course | Link | Deadline |
|--------|------|---------|
| Company Orientation | [`10-training/company-orientation.md`](../10-training/company-orientation.md) | Week 1 |
| Security Awareness | [`10-training/security-awareness.md`](../10-training/security-awareness.md) | Week 1 |
| Privacy Awareness | [`10-training/privacy-awareness.md`](../10-training/privacy-awareness.md) | Week 1 (high priority — you handle employee PII) |
| Workplace Conduct | [`10-training/workplace-conduct.md`](../10-training/workplace-conduct.md) | Week 1 (high priority — you model and enforce conduct) |
| Product Training (all three products) | [`10-training/product-training.md`](../10-training/product-training.md) | Week 4 (so you can speak credibly about ACME's products to candidates and employees) |

Additional role-specific training delivered by Kavya and the HR Enablement team in weeks 2–4:
- "Workday at ACME" workshop (4 hours — required certification).
- "HR Hub portal and knowledge-base authoring" workshop (2 hours).
- "Leave and time-off coordination" workshop (2 hours).
- "Benefits enrollment support" briefing by Total Rewards (2 hours).
- "Performance review administration" workshop (2 hours).
- "Employee-relations escalation and HRBP handoff" briefing by Kavya (1 hour).
- "Data classification and employee PII handling" briefing by Privacy Office (1 hour).

## 10. First-Week Activities

- **Day 1:** IT activation (M365, Authenticator, laptop). Read [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md). Manager intro 1:1 with Ananya. Meet your HR pod.
- **Day 2:** Tour Workday, HR Hub, Leena.ai, DocuSign, Power BI. Read all HR policies (section 4 list). Read your pod's regional specific HR procedures in the HR Hub.
- **Day 3:** Shadow at least 5 employee cases with Kavya or an experienced HR Specialist — leave requests, onboarding handoffs, benefits questions, performance administration tasks. Read [`03-security/customer-data-handling.md`](../03-security/customer-data-handling.md) and [`03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md).
- **Day 4:** Meet the IT Onboarding lead (Geetha Iyer) and Payroll lead. Read the onboarding handoff workflow in [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) end-to-end from the HR perspective.
- **Day 5:** Process your first independent case — a leave request or benefits question, with Kavya reviewing your response before send. Draft your first HR Hub knowledge-base article (or update an existing one).

## 11. First-Month Deliverables

1. **Shadowed at least 15 employee cases** — across leave, benefits, performance administration, employee relations support, onboarding handoffs. Log observations in your learning journal.
2. **Handled your first 10 cases independently** — initial response, case resolution or escalation, all within SLA. Kavya reviewed your first 3 responses before send.
3. **Workday certification complete** — passed the Workday certification quiz with Ananya's sign-off.
4. **Authored or updated your first HR Hub knowledge-base article** — reviewed by Kavya.
5. **Coordinated your first onboarding handoff** — received a candidate-accepted offer from Talent Acquisition and handed off to IT Onboarding for laptop and M365 provisioning, following [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md).
6. **Completed all Week 1–4 training** in section 9 plus the role-specific workshops.

## 12. 30/60/90-Day Expectations

| Window | Expectation |
|--------|-------------|
| **30 days** | Tooling setup complete. Shadow 15 cases. Handle 10 cases independently. Workday certification complete. Author first knowledge-base article. Coordinate first onboarding handoff. Complete security, privacy, workplace-conduct, and HR-operations training plus role-specific workshops. |
| **60 days** | Take primary on a regional pod for routine HR operations cases (with Kavya as backup). Run a full onboarding cycle end-to-end independently (offer-acceptance handoff from TA → IT provisioning coordination → Day-1 welcome → first-week check-in → first-30-day check-in). Co-administer a performance review cycle for your pod (under Ananya's review). Begin owning one HR operations area (onboarding, leave, benefits, performance, or employee relations support). |
| **90 days** | Take primary on a regional pod for all routine HR operations cases (with backup) for at least one full week. Independently administer a performance review cycle for your pod (with Ananya reviewing calibration). Own one HR operations area end-to-end (curate the knowledge base, run the operational rhythm, escalate exceptions). Co-present at the monthly HR operations review to Ananya and the broader HR org. Be eligible to back up an HRBP on employee-relations escalations (informal — HRBP remains the lead). |

## 13. Team Meetings

| Meeting | Cadence | Owner | Your role |
|---------|---------|-------|-----------|
| HR org standup | 15 min, daily | Ananya Sharma | Attend; share your top open case and blockers |
| HR pod standup (India / EMEA / Americas) | 15 min, daily per pod | Your pod lead | Attend; share your pod's open cases |
| 1:1 with manager | 30 min, weekly | Ananya Sharma | Career, blockers, case coaching |
| 1:1 with buddy | 30 min, daily for first 2 weeks, then weekly | Kavya Krishnan | Case coaching, escalation review |
| HR operations area sync (onboarding / leave / benefits / performance) | 30 min, weekly per area | Area lead | Attend for the area(s) you cover |
| Onboarding handoff sync (with IT Onboarding + TA) | 30 min, weekly | IT Onboarding lead | Attend; surface handoff issues |
| Monthly HR operations review | 60 min, monthly | Ananya Sharma | Attend; present after 60 days |
| All-hands | 60 min, monthly | Sridhar Venkatesh | Attend |

## 14. Escalation Contacts

Use the following contacts in priority order. See [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for the full directory.

| Need | Contact | How |
|------|---------|-----|
| Case / policy / procedure question | Buddy: Kavya Krishnan (kavya.krishnan@acme.example) | 1:1 or Teams DM |
| People/career/scope | VP: Ananya Sharma (ananya.sharma@acme.example) | 1:1 or Teams DM |
| Employee relations / grievance escalation | HRBP for the employee's team — see [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for the full HRBP map. Kavya covers Cloud/Workspace; Deepika Rao covers Intelligence/QE/Support; Sanjay Patel covers Platform/Sales. | Teams DM to the relevant HRBP; copy Ananya |
| IT (laptop, VPN, M365, Workday, software) | IT Helpdesk | `helpdesk.acme.example` or `#it-helpdesk` |
| Employee data privacy question (Workday, PII) | Privacy Office + CISO designate | `privacy@acme.example` |
| Security incident or suspected breach (incl. employee-data exposure) | SOC + CISO Rajan Mehta | `soc@acme.example` + 24/7 hotline in [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md) |
| Payroll / tax / bank detail question | Payroll lead (via Ananya) | Email Ananya to route |
| Employment-law question | Director Legal: Hemant Joshi (hemant.joshi@acme.example) | Email Legal, cc Ananya |
| Cross-team dependency (Engineering, Sales, Finance) | Receiving VP via Ananya | Ananya routes |

## Related Documents

- [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md)
- [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md)
- [`07-workflows/first-30-days.md`](../07-workflows/first-30-days.md)
- [`07-workflows/first-60-days.md`](../07-workflows/first-60-days.md)
- [`07-workflows/first-90-days.md`](../07-workflows/first-90-days.md)
- [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md)
- [`08-forms/software-access-request.md`](../08-forms/software-access-request.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- [`metadata/glossary.md`](../metadata/glossary.md)
