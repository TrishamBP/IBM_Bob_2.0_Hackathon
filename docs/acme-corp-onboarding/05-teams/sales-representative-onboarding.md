---
document_id: ACME-TEAM-011
title: ACME Corp Sales Representative Onboarding
category: team-onboarding
department: sales
applicable_roles: [sales-representative]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [team-onboarding, sales-representative]
---

# ACME Corp Sales Representative Onboarding

Welcome to the **Sales** organization at ACME Corp. This guide is your single reference for the first 90 days as a Sales Representative driving revenue for one of ACME's three product lines. It assumes you have already completed [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) and [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md).

> ACME Corp is a fictional company. All names, repositories, hosts, and systems referenced here are illustrative and use the `.example` domain. Do not attempt to reach any URL.

## 1. Team Overview

| Field | Value |
|-------|-------|
| Team name | Sales |
| Reports up to | Christina Müller (Director Sales), who reports to the CEO/CFO office |
| Primary offices | London (Christina's home office), with reps distributed across Seattle, Hyderabad, Bengaluru to cover regional territories |
| Primary products | ACME Cloud, ACME Intelligence, ACME Workspace — see product overviews |
| Primary tooling | Salesforce (CRM), Outreach (sales engagement), Gong (call recording & coaching), LinkedIn Sales Navigator, Highspot (sales content) |
| Primary channel | `#sales` (Microsoft Teams); each region also has its own channel |

**Mission.** Drive new-logo acquisition, expansion within existing accounts, and renewal protection for ACME's three product lines. Reps are the primary revenue owners and the primary customer-facing voice of ACME.

**Charter.** Owns the customer relationship through the sales cycle — prospecting, qualification, solution pitching, negotiation, closing. Does **not** own product strategy (PM owns that), customer success post-close (Customer Support owns that), or contract drafting (Legal owns that).

**Customers.** Enterprise buyers (CIOs, CTOs, CISOs, CFOs, Heads of Platform/Engineering/AI), IT administrators, FinOps leads, and procurement teams at enterprise customers.

## 2. Reporting Manager

- **Director:** Christina Müller (christina.muller@acme.example, London office, hybrid).
- Christina reports to the CEO/CFO office.
- Your standing 1:1 is 30 minutes weekly.
- Reporting line is recorded at `hr.acme.example` under your profile.
- You will also be assigned to a regional pod (EMEA, Americas, or APAC) and to one or more product line specializations (Cloud, Intelligence, Workspace).

## 3. Onboarding Buddy

- **Buddy:** Christina Müller (christina.muller@acme.example, Director Sales) serves as your buddy for the first 90 days. For a Sales team of ACME's size, the Director personally buddies new reps to set the tone for customer engagement standards.
- Christina is your peer mentor for the first 90 days — territory strategy, deal qualification, customer engagement standards, cross-functional coordination patterns.
- Buddy commitment: 1 hour per week for the first 12 weeks (split between 1:1 and ride-along shadowing on customer calls).
- See [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) for the buddy program's expectations.

## 4. Required Documents (Week 1)

Read each of the following in your first week. Christina will check progress during your week-1 1:1.

- [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md)
- [`00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- [`00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- [`00-company/communication-guidelines.md`](../00-company/communication-guidelines.md)
- [`00-company/products-and-business-units.md`](../00-company/products-and-business-units.md)
- [`03-security/information-security-policy.md`](../03-security/information-security-policy.md)
- [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md)
- [`03-security/customer-data-handling.md`](../03-security/customer-data-handling.md)
- [`03-security/confidentiality-agreement.md`](../03-security/confidentiality-agreement.md)
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

**Sales-specific tools (provisioned via Entra SSO):**
- Salesforce (CRM) — `Sales Rep` seat at `crm.internal.acme.example`
- Outreach (sales engagement) — `Sender` seat
- Gong (call recording, coaching) — `Contributor` seat
- Highspot (sales content) — `Viewer/Editor`
- LinkedIn Sales Navigator — `Enterprise Seat`
- DocuSign (signature) — `Sender` seat
- Zoom or Microsoft Teams (customer meetings) — already provisioned via M365

You will **not** receive access to engineering repositories or developer tooling. See section 7.

## 6. Approved AI Tools

Per the role eligibility matrix in [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md), Sales Representatives are **not entitled** to ACME engineering AI tools:

| Tool | Entitlement | Notes |
|------|-------------|-------|
| GitHub Copilot Business | **No** | Sales reps do not write code and do not receive a Copilot seat. Do not request one via [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md) — it will be declined. |
| Internal ACME Intelligence sandbox | **No** | Not provisioned. |

If you need AI assistance for writing (account plans, emails, account research), use Microsoft Copilot for Microsoft 365, governed by [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md). Salesforce Einstein (Salesforce's built-in AI) is governed by Salesforce enterprise policy and the ACME acceptable-use policy.

Do **not** enter customer confidential information or ACME confidential pricing into public AI tools — see [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) and [`03-security/customer-data-handling.md`](../03-security/customer-data-handling.md).

## 7. Required Repositories

You will **not** receive access to any ACME engineering repositories. Sales is a non-engineering function — repository access is restricted per [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) and the access tier matrix in [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md).

If you need to understand what a product feature does (for a customer demo), use:

- Product overviews in [`06-product/`](../06-product/) (no special access required)
- Highspot sales content (battle cards, demo scripts, customer decks)
- Confluence sales spaces (read-only — `Sales-Cloud`, `Sales-Intelligence`, `Sales-Workspace`)
- Your partner PM and Solutions Engineer (request a demo walkthrough)

If you have a documented business need for read-only access to a specific repository (e.g., to read an integration guide for a customer), your manager may file a [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md) — these are rare exceptions and require CISO designate review.

## 8. Required Access Permissions

On Day 1, IT Onboarding (Geetha Iyer, `geetha.iyer@acme.example) provisions the following Entra ID groups. Verify each in the My Apps portal at `myapps.acme.example`.

| Entra ID group | Purpose |
|----------------|---------|
| `Sales` | Membership in the Sales org; Salesforce, Outreach, Gong, Highspot seats. |
| `Salesforce-Sales-Rep` | Salesforce role with lead, opportunity, account, contact CRUD for assigned territory. |
| `Outreach-Sender` | Outreach sender seat for sales engagement sequences. |
| `Highspot-Editor` | Editor access to your product line's Highspot sales content. |
| `Confluence-Sales-Reader` | Read-only access to sales spaces in Confluence. |
| `DocuSign-Sender` | Sender seat for NDA and order-form routing. |
| `Customer-Data-Processor-Sales` | Access to customer data in Salesforce within your territory scope. |

Additional tools (auto-provisioned):

- **LinkedIn Sales Navigator** — `Enterprise` seat.
- **Gong** — `Contributor` seat.

Cloud production, cluster, and Vault access is **not** granted. Sales does not need it per [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).

## 9. Training Requirements

Complete the following training in your first 30 days. All training is tracked in your learning transcript at `hr.acme.example/learning`.

| Course | Link | Deadline |
|--------|------|---------|
| Company Orientation | [`10-training/company-orientation.md`](../10-training/company-orientation.md) | Week 1 |
| Security Awareness | [`10-training/security-awareness.md`](../10-training/security-awareness.md) | Week 1 |
| Privacy Awareness | [`10-training/privacy-awareness.md`](../10-training/privacy-awareness.md) | Week 1 (high priority — you handle customer data) |
| Product Training (all three products) | [`10-training/product-training.md`](../10-training/product-training.md) | Week 2 (high priority — customer-facing) |
| Workplace Conduct | [`10-training/workplace-conduct.md`](../10-training/workplace-conduct.md) | Week 2 (high priority — customer-facing) |
| Cloud Platform Fundamentals | [`10-training/cloud-platform-fundamentals.md`](../10-training/cloud-platform-fundamentals.md) | Week 4 (so you can speak credibly about ACME's platform) |

Additional role-specific training delivered by Christina and the Sales Enablement team in weeks 2–4:
- "Salesforce at ACME" workshop (2 hours).
- "MEDDPICC qualification methodology" workshop (4 hours — required certification).
- "Demo environment and Solutions Engineer handoff" workshop (2 hours).
- "Pricing, discounting, and Legal handoff" briefing by Finance and Legal (2 hours).
- "Competitive battle cards" briefing by Product Marketing (2 hours).

## 10. First-Week Activities

- **Day 1:** IT activation (M365, Authenticator, laptop). Read [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md). Manager intro 1:1 with Christina. Meet your regional pod.
- **Day 2:** Tour Salesforce, Outreach, Gong, Highspot. Read all three product overviews. Read your territory assignment and account list (in Salesforce).
- **Day 3:** Shadow at least 2 customer calls with an experienced rep. Christina will schedule you as a silent observer. Read [`03-security/customer-data-handling.md`](../03-security/customer-data-handling.md) for customer-data rules.
- **Day 4:** Meet your partner PM and Solutions Engineer. Read your product line's battle card in Highspot. Read the demo script in Confluence.
- **Day 5:** Complete the MEDDPICC certification pre-work. Schedule your first prospecting block (50 outbound activities — emails, LinkedIn messages, calls).

## 11. First-Month Deliverables

1. **Shadowed at least 10 customer calls** — discovery, demo, negotiation, close. Log observations in your learning journal.
2. **MEDDPICC certification complete** — passed the certification quiz with Christina's sign-off.
3. **Territory plan v1 drafted** — top 25 accounts, hypothesis per account, sequencing. Reviewed by Christina.
4. **First 200 outbound activities logged** in Outreach (emails, calls, LinkedIn touches). Review conversion metrics with Christina in your week-4 1:1.
5. **First qualified meeting booked** — a discovery call with a target account, with a Solutions Engineer on standby. Gong recording logged.
6. **Completed all Week 1–4 training** in section 9 plus the role-specific workshops.

## 12. 30/60/90-Day Expectations

| Window | Expectation |
|--------|-------------|
| **30 days** | Tooling setup complete. Shadow 10 customer calls. MEDDPICC certification complete. Territory plan v1 drafted. 200 outbound activities logged. First qualified meeting booked. Complete security, privacy, product, and workplace-conduct training. |
| **60 days** | First demo delivered independently (with a Solutions Engineer as backup). Run a full discovery cycle on at least 5 active opportunities. Co-build the first order form with Legal. Begin to forecast your pipeline in the weekly forecast call. Run your first negotiation call with Christina observing. |
| **90 days** | Close your first deal (with Christina's coaching on the final negotiation). Independently forecast your pipeline. Mentor the next new rep informally (shadow them on their first calls). Co-present your territory plan to Christina and the regional pod at the quarterly business review. |

## 13. Team Meetings

| Meeting | Cadence | Owner | Your role |
|---------|---------|-------|-----------|
| Regional pod standup | 15 min, daily | Your regional lead | Attend; share your top opportunity of the day |
| Forecast call | 30 min, weekly | Christina Müller | Attend; forecast your commit, best-case, and pipeline |
| 1:1 with manager | 30 min, weekly | Christina Müller | Career, blockers, deal coaching |
| 1:1 with buddy (also Christina) | 1 hour, weekly for first 12 weeks | Christina Müller | Coaching on live deals and customer engagement |
| Product Marketing update | 30 min, biweekly | Product Marketing | Attend for new-feature battle cards |
| Solutions Engineer sync | 30 min, weekly | Your partner SE | Pre-demo prep, post-demo debrief |
| Quarterly business review (regional pod) | 90 min, quarterly | Christina Müller | Present your territory plan and results |
| All-hands | 60 min, monthly | Sridhar Venkatesh | Attend |

## 14. Escalation Contacts

Use the following contacts in priority order. See [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for the full directory.

| Need | Contact | How |
|------|---------|-----|
| Deal coaching, qualification, customer engagement | Buddy & Director: Christina Müller (christina.muller@acme.example) | 1:1 or Teams DM |
| Pricing / discounting approval | Director Sales (Christina) + CFO Ritu Khanna | Email Christina, cc Finance |
| Order form / contract drafting | Director Legal: Hemant Joshi (hemant.joshi@acme.example) | Email Legal (route via Christina) |
| Demo environment / Solutions Engineer | Your partner SE | Teams DM or `#sales-se-sync` |
| Product / feature question | Your partner PM (via `#sales-product-sync`) | Teams channel |
| HR / leave / payroll / policy | HRBP: Sanjay Patel (sanjay.patel@acme.example) — covers Sales | `hr.acme.example`, then Teams DM |
| IT (laptop, VPN, M365, Salesforce, software) | IT Helpdesk | `helpdesk.acme.example` or `#it-helpdesk` |
| Customer data privacy question (Salesforce, Gong) | Privacy Office + CISO designate | `privacy@acme.example` |
| Security incident or suspected breach | SOC + CISO Rajan Mehta | `soc@acme.example` + 24/7 hotline in [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md) |
| Customer success / post-close escalation | Director Customer Support: Bo Tan (bo.tan@acme.example) | Email or `#support-sales-handoff` |

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
