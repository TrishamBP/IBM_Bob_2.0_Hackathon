---
document_id: ACME-TEAM-014
title: ACME Corp Finance Analyst Onboarding
category: team-onboarding
department: finance
applicable_roles: [finance-analyst]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [team-onboarding, finance-analyst]
---

# ACME Corp Finance Analyst Onboarding

Welcome to the **Finance** organization at ACME Corp. This guide is your single reference for the first 90 days as a Finance Analyst supporting financial planning & analysis (FP&A), accounting operations, and revenue operations across ACME's three product lines and four offices. It assumes you have already completed [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) and [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md).

> ACME Corp is a fictional company. All names, repositories, hosts, and systems referenced here are illustrative and use the `.example` domain. Do not attempt to reach any URL.

## 1. Team Overview

| Field | Value |
|-------|-------|
| Team name | Finance |
| Reports up to | Ritu Khanna (CFO), who reports to the CEO office |
| Primary offices | Hyderabad (Ritu's home office and Finance headquarters), with analysts distributed across Bengaluru, London, Seattle to support regional finance operations |
| Primary products | ACME Cloud, ACME Intelligence, ACME Workspace (revenue attribution across all three) |
| Primary tooling | Oracle ERP (financial system of record), Anaplan (FP&A), Tableau (finance dashboards), Salesforce (revenue pipeline — read-only), Workday (payroll data — read-only), Confluence (finance knowledge base) |
| Primary channel | `#finance-team` (Microsoft Teams); `#finance-help` for cross-functional questions |

**Mission.** Deliver financial planning, accounting operations, revenue and billing operations, procurement support, and financial compliance across ACME. Finance Analysts are the analytical backbone of ACME's financial decision-making.

**Charter.** Owns budgeting and forecasting, monthly close support, revenue recognition analysis, billing operations support, procurement and vendor management support, and finance analytics. Does **not** own treasury (Treasury team owns that, under CFO), tax strategy (Tax team owns that, under CFO), or audit (Audit and SOX team owns that, under CFO). All Finance functions report up through the CFO.

**Customers.** ACME leadership (CEO, CFO, Board reporting), department leaders (budget owners), Sales (revenue pipeline and orders), Engineering and IT (procurement and vendor management), Legal (contracts and revenue terms), external auditors (annual audit support).

## 2. Reporting Manager

- **CFO:** Ritu Khanna (ritu.khanna@acme.example, Hyderabad office, hybrid).
- Ritu reports to the CEO office.
- Your standing 1:1 is 30 minutes weekly.
- Reporting line is recorded at `hr.acme.example` under your profile.
- You will also be assigned to one of three Finance pods (FP&A, Accounting Operations, Revenue Operations) and to one or more product-line finance specializations.

## 3. Onboarding Buddy

- **Buddy:** Aarti Deshpande (aarti.deshpande@acme.example), Senior Finance Analyst. Aarti serves as your buddy for the first 90 days.
- Aarti is your peer mentor for the first 90 days — Oracle ERP conventions, Anaplan modeling patterns, monthly close rhythm, revenue recognition analysis, vendor management workflow.
- Buddy commitment: 2 hours per day for the first 2 weeks; 1 hour per day for weeks 3–6; ad-hoc thereafter.
- See [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) for the buddy program's expectations.

## 4. Required Documents (Week 1)

Read each of the following in your first week. Aarti will check progress during your week-1 1:1.

- [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md)
- [`00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- [`00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- [`00-company/communication-guidelines.md`](../00-company/communication-guidelines.md)
- [`00-company/products-and-business-units.md`](../00-company/products-and-business-units.md)
- [`03-security/information-security-policy.md`](../03-security/information-security-policy.md)
- [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md)
- [`03-security/confidentiality-agreement.md`](../03-security/confidentiality-agreement.md)
- [`03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md)
- [`03-security/data-classification.md`](../03-security/data-classification.md)
- [`06-product/acme-cloud-overview.md`](../06-product/acme-cloud-overview.md)
- [`06-product/acme-intelligence-overview.md`](../06-product/acme-intelligence-overview.md)
- [`06-product/acme-workspace-overview.md`](../06-product/acme-workspace-overview.md)
- [`10-training/product-training.md`](../10-training/product-training.md)
- [`10-training/workplace-conduct.md`](../10-training/workplace-conduct.md)

## 5. Required Software

Install only the approved tools below. Anything else requires a software access request via [`08-forms/software-access-request.md`](../08-forms/software-access-request.md). See [`02-it/approved-software-installation.md`](../02-it/approved-software-installation.md) for the binding policy.

**Workstation baseline (installed by IT before Day 1):**
- Windows 11 Enterprise or macOS 14+
- Microsoft 365 — Outlook, Teams, OneDrive, Word, Excel, PowerPoint
- Microsoft Authenticator, Corporate VPN, 1Password, Microsoft Defender for Endpoint

**Finance-specific tools (provisioned via Entra SSO):**
- Oracle ERP (financial system of record) — `Analyst` role at `erp.internal.acme.example`
- Anaplan (FP&A modeling) — `Analyst` seat at `fpa.internal.acme.example`
- Tableau (finance dashboards) — `Viewer/Explorer` at `bi.internal.acme.example`
- Salesforce (revenue pipeline — read-only) — `Read-Only` seat
- Workday (payroll data — read-only) — `Read-Only` role
- Confluence (finance knowledge base) — `Editor` for finance spaces
- DocuSign (finance forms) — `Sender` seat
- Coupa (procurement and vendor management) — `Requester` role

You will **not** receive access to engineering repositories or developer tooling. See section 7.

## 6. Approved AI Tools

Per the role eligibility matrix in [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md), Finance Analysts are **not entitled** to ACME engineering AI tools:

| Tool | Entitlement | Notes |
|------|-------------|-------|
| GitHub Copilot Business | **No** | Finance Analysts do not write code and do not receive a Copilot seat. Do not request one via [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md) — it will be declined. |
| Internal ACME Intelligence sandbox | **No** | Not provisioned. |

If you need AI assistance for writing (financial narratives, internal docs, board materials), use Microsoft Copilot for Microsoft 365, governed by [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md). Excel's built-in AI features and Anaplan's predictive features are governed by their respective enterprise policies and the ACME acceptable-use policy.

Do **not** enter pre-public financial results, M&A plans, employee compensation data, or customer billing data into public AI tools — see [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md), [`03-security/data-classification.md`](../03-security/data-classification.md), and [`03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md). These are Confidential or Restricted data.

## 7. Required Repositories

You will **not** receive access to any ACME engineering repositories. Finance is a non-engineering function — repository access is restricted per [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) and the access tier matrix in [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md).

If you need to reference a finance policy or process, use:

- The Finance knowledge base in Confluence (you have full editor access)
- Oracle ERP and Anaplan documentation in-app
- This onboarding library (the canonical source for cross-functional context)

If you have a documented business need for read-only access to a specific repository (e.g., to read a vendor integration contract stored in a repo), your manager may file a [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md) — these are rare exceptions and require CISO designate review.

## 8. Required Access Permissions

On Day 1, IT Onboarding (Geetha Iyer, `geetha.iyer@acme.example) provisions the following Entra ID groups. Verify each in the My Apps portal at `myapps.acme.example`.

| Entra ID group | Purpose |
|----------------|---------|
| `Finance` | Membership in the Finance org; Oracle ERP, Anaplan, Tableau, Coupa seats. |
| `Oracle-ERP-Analyst` | Oracle ERP role with GL read access, subledger read access, and report-write access for your pod's region. |
| `Anaplan-Analyst` | Anaplan analyst role for your pod's models. |
| `Tableau-Finance-Explorer` | Explorer access to finance dashboards. |
| `Salesforce-Finance-Reader` | Read-only access to Salesforce opportunities, accounts, and orders for revenue pipeline analysis. |
| `Workday-Finance-Reader` | Read-only access to Workday payroll data for compensation analysis (regional scope). |
| `Coupa-Requester` | Coupa requester role for procurement and vendor management. |
| `Confluence-Finance-Editor` | Editor access to finance spaces in Confluence. |
| `DocuSign-Finance-Sender` | Sender seat for finance forms. |
| `Confidential-Data-Access` | Marks your account as authorized for Confidential data handling per [`03-security/data-classification.md`](../03-security/data-classification.md). |
| `Restricted-Data-Access-Finance` | Limited Restricted data access for pre-public financial results, with audit logging. |

Additional tools (auto-provisioned):

- **Microsoft Excel** with Power BI add-in — already via M365.

Treasury, Tax, and Audit system access is **not** granted at onboarding — those require separate authorization from the respective team leads. Production cloud, cluster, and Vault access is **not** granted.

## 9. Training Requirements

Complete the following training in your first 30 days. All training is tracked in your learning transcript at `hr.acme.example/learning`.

| Course | Link | Deadline |
|--------|------|---------|
| Company Orientation | [`10-training/company-orientation.md`](../10-training/company-orientation.md) | Week 1 |
| Security Awareness | [`10-training/security-awareness.md`](../10-training/security-awareness.md) | Week 1 |
| Privacy Awareness | [`10-training/privacy-awareness.md`](../10-training/privacy-awareness.md) | Week 1 (high priority — you handle employee comp and pre-public financials) |
| Product Training (all three products) | [`10-training/product-training.md`](../10-training/product-training.md) | Week 2 (so you can speak credibly about ACME's products and revenue model) |
| Workplace Conduct | [`10-training/workplace-conduct.md`](../10-training/workplace-conduct.md) | Week 2 (high priority — you handle sensitive data and cross-functional negotiations) |
| Cloud Platform Fundamentals | [`10-training/cloud-platform-fundamentals.md`](../10-training/cloud-platform-fundamentals.md) | Week 4 (so you can speak credibly about ACME's cloud cost structure) |

Additional role-specific training delivered by Aarti and the Finance Enablement team in weeks 2–4:
- "Oracle ERP at ACME" workshop (4 hours — required certification).
- "Anaplan modeling conventions" workshop (4 hours — required certification).
- "Monthly close rhythm and your role" workshop (2 hours).
- "Revenue recognition basics" workshop (2 hours).
- "Procurement and vendor management workflow" workshop (1 hour).
- "Data classification and pre-public financials handling" briefing by Privacy Office + CISO designate (1 hour).

## 10. First-Week Activities

- **Day 1:** IT activation (M365, Authenticator, laptop). Read [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md). Manager intro 1:1 with Ritu. Meet your Finance pod.
- **Day 2:** Tour Oracle ERP, Anaplan, Tableau, Salesforce (read-only), Workday (read-only), Coupa, Confluence finance spaces. Read all three product overviews. Read your pod's standard operating procedures in Confluence.
- **Day 3:** Shadow at least 5 finance cases with Aarti or an experienced analyst — a budget-vs-actuals analysis, a monthly close task, a revenue pipeline review, a procurement request, a vendor invoice review. Read [`03-security/data-classification.md`](../03-security/data-classification.md) and [`03-security/privacy-acknowledgement.md`](../03-security/privacy-acknowledgement.md).
- **Day 4:** Meet the Sales Operations lead and the Procurement lead. Read the revenue recognition policy in Confluence. Read the procurement workflow end-to-end.
- **Day 5:** Process your first independent task — a small monthly close task, a budget reforecast input, or a procurement request review, with Aarti reviewing your work before submission. Draft your first Confluence knowledge-base article (or update an existing one).

## 11. First-Month Deliverables

1. **Shadowed at least 15 finance cases** — across budgeting, close, revenue analysis, procurement, vendor management. Log observations in your learning journal.
2. **Handled your first 10 cases independently** — initial analysis, work product, and review submission, all within deadline. Aarti reviewed your first 3 work products before submission.
3. **Oracle ERP and Anaplan certifications complete** — passed both certification quizzes with Ritu's sign-off.
4. **Authored or updated your first Confluence knowledge-base article** — reviewed by Aarti.
5. **Co-supported your first monthly close** — under Aarti's supervision, completed at least 3 close tasks for your pod.
6. **Completed all Week 1–4 training** in section 9 plus the role-specific workshops.

## 12. 30/60/90-Day Expectations

| Window | Expectation |
|--------|-------------|
| **30 days** | Tooling setup complete. Shadow 15 cases. Handle 10 cases independently. Oracle ERP and Anaplan certifications complete. Author first knowledge-base article. Co-support first monthly close. Complete security, privacy, workplace-conduct, product, and finance-operations training plus role-specific workshops. |
| **60 days** | Take primary on a regional or functional pod for routine finance operations cases (with Aarti as backup). Run a full monthly close cycle for your pod independently (under Ritu's review). Co-build your first Anaplan model update (e.g., a budget reforecast scenario). Begin owning one finance operations area (FP&A, accounting operations, or revenue operations). |
| **90 days** | Take primary on a regional or functional pod for all routine finance operations cases (with backup) for at least one full month-end cycle. Independently complete a monthly close for your pod (with Ritu reviewing calibration). Own one finance operations area end-to-end (curate the knowledge base, run the operational rhythm, escalate exceptions). Co-present at the monthly Finance operations review to Ritu and the broader Finance org. Be eligible to back up an FP&A lead on the next quarterly board reporting cycle (informal — FP&A lead remains the lead). |

## 13. Team Meetings

| Meeting | Cadence | Owner | Your role |
|---------|---------|-------|-----------|
| Finance org standup | 15 min, daily | Ritu Khanna | Attend; share your top open case and blockers |
| Finance pod standup (FP&A / Accounting Ops / Revenue Ops) | 15 min, daily per pod | Your pod lead | Attend; share your pod's open cases |
| Monthly close stand-up (during close week) | 15 min, daily during close | Accounting Ops lead | Attend; report close-task status |
| 1:1 with manager | 30 min, weekly | Ritu Khanna | Career, blockers, case coaching |
| 1:1 with buddy | 30 min, daily for first 2 weeks, then weekly | Aarti Deshpande | Case coaching, review of your work products |
| Finance operations area sync (FP&A / Accounting Ops / Revenue Ops) | 30 min, weekly per area | Area lead | Attend for the area(s) you cover |
| Sales-Finance sync (revenue pipeline) | 30 min, weekly | Sales Operations lead + Revenue Ops lead | Attend if in Revenue Ops pod |
| Monthly Finance operations review | 60 min, monthly | Ritu Khanna | Attend; present after 60 days |
| All-hands | 60 min, monthly | Sridhar Venkatesh | Attend |

## 14. Escalation Contacts

Use the following contacts in priority order. See [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for the full directory.

| Need | Contact | How |
|------|---------|-----|
| Case / model / process question | Buddy: Aarti Deshpande (aarti.deshpande@acme.example) | 1:1 or Teams DM |
| People/career/scope | CFO: Ritu Khanna (ritu.khanna@acme.example) | 1:1 or Teams DM |
| Treasury / cash management question | Treasury lead (via Ritu) | Email Ritu to route |
| Tax question | Tax lead (via Ritu) | Email Ritu to route |
| Audit / SOX question | Audit lead (via Ritu) | Email Ritu to route |
| HR / leave / payroll / policy | HRBP: Kavya Krishnan (kavya.krishnan@acme.example) — Finance HRBP assignment pending; route via Ananya Sharma (ananya.sharma@acme.example) | `hr.acme.example`, then Teams DM |
| IT (laptop, VPN, M365, Oracle ERP, software) | IT Helpdesk | `helpdesk.acme.example` or `#it-helpdesk` |
| Pre-public financials / data classification question | Privacy Office + CISO designate + Ritu | `privacy@acme.example`, cc Ritu |
| Security incident or suspected breach (incl. financial-data exposure) | SOC + CISO Rajan Mehta + Ritu | `soc@acme.example` + 24/7 hotline in [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md) |
| Sales / revenue / contract question | Director Sales: Christina Müller (christina.muller@acme.example) | Email or `#sales-finance-sync` |
| Vendor / contract / legal question | Director Legal: Hemant Joshi (hemant.joshi@acme.example) | Email Legal, cc Ritu |
| Cross-team dependency (Engineering, HR, Sales) | Receiving VP via Ritu | Ritu routes |

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
