---
document_id: ACME-TEAM-009
title: ACME Corp Product Manager Onboarding
category: team-onboarding
department: product
applicable_roles: [product-manager]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [team-onboarding, product-manager]
---

# ACME Corp Product Manager Onboarding

Welcome to the **Product Management** organization at ACME Corp. This guide is your single reference for the first 90 days as a Product Manager (PM) driving product strategy, discovery, and delivery for one of ACME's three product lines. It assumes you have already completed [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) and [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md).

> ACME Corp is a fictional company. All names, repositories, hosts, and systems referenced here are illustrative and use the `.example` domain. Do not attempt to reach any URL.

## 1. Team Overview

| Field | Value |
|-------|-------|
| Team name | Product Management |
| Reports up to | Daniel Coelho (Director Product), who reports to the CEO/CTO office |
| Primary offices | Seattle (Daniel's home office), with PMs distributed across Hyderabad, Bengaluru, London |
| Primary products | ACME Cloud, ACME Intelligence, ACME Workspace — see product overviews |
| Primary tooling | Aha! (roadmap), Confluence (PRDs), Jira (delivery), Salesforce (customer data), Amplitude (product analytics) |
| Primary channel | `#product` (Microsoft Teams); each product line also has its own channel |

**Mission.** Drive product strategy, customer discovery, requirements definition (PRDs), roadmap, release planning, and cross-functional coordination for ACME's three product lines. PMs are the bridge between customer needs, business strategy, and engineering delivery.

**Charter.** Owns the product strategy, roadmap, PRDs, prioritization frameworks, customer discovery, and cross-functional coordination. Does **not** own engineering architecture or implementation (Engineering Managers and Tech Leads own that), design execution (UX owns that), or GTM execution (Sales and Marketing own that).

**Customers.** Enterprise buyers (via Sales), end users at customer organizations (direct research), ACME Sales and Support (internal customers who need product education), and the Engineering teams you partner with.

## 2. Reporting Manager

- **Director:** Daniel Coelho (daniel.coelho@acme.example, Seattle office, hybrid).
- Daniel reports to the CEO/CTO office.
- Your standing 1:1 is 30 minutes weekly.
- Reporting line is recorded at `hr.acme.example` under your profile.
- You will also be assigned to one of three product line sub-teams (Cloud, Intelligence, or Workspace). Your product line partner EM is your day-to-day engineering counterpart; Daniel remains your HR system manager of record.

## 3. Onboarding Buddy

- **Buddy:** Maheshwari Krishnan (maheshwari.krishnan@acme.example), Senior PM, Product.
- Maheshwari is your peer mentor for the first 90 days — Aha! conventions, PRD templates, customer discovery rituals, cross-functional coordination patterns.
- Buddy commitment: 2 hours per day for the first 2 weeks; 1 hour per day for weeks 3–6; ad-hoc thereafter.
- See [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) for the buddy program's expectations.

## 4. Required Documents (Week 1)

Read each of the following in your first week. Maheshwari will check progress during your week-1 1:1.

- [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md)
- [`00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- [`00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- [`00-company/communication-guidelines.md`](../00-company/communication-guidelines.md)
- [`00-company/products-and-business-units.md`](../00-company/products-and-business-units.md)
- [`03-security/information-security-policy.md`](../03-security/information-security-policy.md)
- [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md)
- [`06-product/acme-cloud-overview.md`](../06-product/acme-cloud-overview.md)
- [`06-product/acme-intelligence-overview.md`](../06-product/acme-intelligence-overview.md)
- [`06-product/acme-workspace-overview.md`](../06-product/acme-workspace-overview.md)
- [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md) (read-only context — you will not write code, but you will review PRs and RFCs)
- [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md)
- [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md)
- [`10-training/product-training.md`](../10-training/product-training.md)

## 5. Required Software

Install only the approved tools below. Anything else requires a software access request via [`08-forms/software-access-request.md`](../08-forms/software-access-request.md). See [`02-it/approved-software-installation.md`](../02-it/approved-software-installation.md) for the binding policy.

**Workstation baseline (installed by IT before Day 1):**
- Windows 11 Enterprise or macOS 14+
- Microsoft 365 — Outlook, Teams, OneDrive, Word, Excel, PowerPoint
- Microsoft Authenticator, Corporate VPN, 1Password, Microsoft Defender for Endpoint

**PM-specific tools (provisioned via Entra SSO):**
- Aha! (roadmap) — at `aha.internal.acme.example`
- Confluence (PRDs, strategy docs) — at `wiki.acme.example`
- Jira (delivery tracking) — at `jira.internal.acme.example`
- Salesforce (customer data, opportunities) — at `crm.internal.acme.example`
- Amplitude (product analytics) — at `analytics.internal.acme.example`
- Figma (read-only access to design files, for review)
- GitHub Enterprise (read-only access to repos, for PR/RFC review)

## 6. Approved AI Tools

Per the role eligibility matrix in [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md), Product Managers are **case-by-case optional** for AI tools:

| Tool | Entitlement | Notes |
|------|-------------|-------|
| GitHub Copilot Business | **Optional (case-by-case)** | Not granted by default. PMs do not write production code. If you regularly draft RFCs alongside engineering or maintain internal docs in repos, your manager may request a seat via [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md). |
| Internal ACME Intelligence sandbox | **No** | PMs do not have access to the sandbox. |

If you need AI assistance for writing (PRDs, customer briefs, internal docs), use Microsoft Copilot for Microsoft 365, which is governed by the same acceptable-use policy at [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) but is provisioned separately from GitHub Copilot Business.

## 7. Required Repositories

You will be granted **read-only** access to all production repositories per the access tier matrix in [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md):

- `acme-cloud-api`, `acme-cloud-frontend`
- `acme-intelligence-agents`, `acme-intelligence-inference`, `acme-intelligence-ml`
- `acme-workspace-web`, `acme-workspace-api`
- `acme-platform-infrastructure`, `acme-shared-libraries`, `acme-quality-automation`

You will **not** receive write access to any repository. Your repo access is for:

- Reading RFCs and design docs stored in `docs/` folders
- Reviewing PR descriptions (to understand what engineering is shipping)
- Filing issues (you can create issues but not PRs)

Repository access is requested via [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md). Daniel pre-approves the bulk read-only bundle.

## 8. Required Access Permissions

On Day 1, IT Onboarding (Geetha Iyer, `geetha.iyer@acme.example) provisions the following Entra ID groups. Verify each in the My Apps portal at `myapps.acme.example`.

| Entra ID group | Purpose |
|----------------|---------|
| `Product-Management` | Membership in the PM org; Aha!, Confluence, Jira PM roles. |
| `ENG-All-Read` | Read-only access to all production repos. |
| `Salesforce-PM-Role` | Read access to opportunities, customer accounts, support cases relevant to your product line. |
| `Amplitude-PM-Role` | Access to product analytics dashboards for your product line. |
| `Figma-Viewer` | Read-only Figma access to design files. |
| `Customer-Interview-Tooling` | Access to the customer interview platform at `research.internal.acme.example`. |

Additional tools (auto-provisioned):

- **Aha!** — `PM` role for your product line.
- **Confluence** — `PM-Editor` for your product line's space.
- **Jira** — `PM` role (issue creation, prioritization, sprint planning visibility).

Production cloud, cluster, and Vault access is **not** granted — PMs do not need it per [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).

## 9. Training Requirements

Complete the following training in your first 30 days. All training is tracked in your learning transcript at `hr.acme.example/learning`.

| Course | Link | Deadline |
|--------|------|---------|
| Company Orientation | [`10-training/company-orientation.md`](../10-training/company-orientation.md) | Week 1 |
| Security Awareness | [`10-training/security-awareness.md`](../10-training/security-awareness.md) | Week 1 |
| Privacy Awareness | [`10-training/privacy-awareness.md`](../10-training/privacy-awareness.md) | Week 1 (high priority — you handle customer data) |
| Product Training (all three products) | [`10-training/product-training.md`](../10-training/product-training.md) | Week 2 |
| Engineering Orientation | [`10-training/engineering-orientation.md`](../10-training/engineering-orientation.md) | Week 2 (read-only — understand how engineering works so you can partner) |
| Git and Repository Workflows | [`10-training/git-and-repository-workflows.md`](../10-training/git-and-repository-workflows.md) | Week 3 (read-only — understand PR/RFC workflows) |
| Cloud Platform Fundamentals | [`10-training/cloud-platform-fundamentals.md`](../10-training/cloud-platform-fundamentals.md) | Week 4 (so you can speak credibly about ACME's platform) |
| Workplace Conduct | [`10-training/workplace-conduct.md`](../10-training/workplace-conduct.md) | Week 4 |

Additional role-specific training delivered by Maheshwari in weeks 2–4:
- "ACME PRD template and review process" workshop (2 hours).
- "Customer discovery and interview methodology" workshop (2 hours).
- "Roadmap planning in Aha!" workshop (1 hour).
- "Pricing and packaging carve-outs for your product line" briefing by Finance (1 hour).

## 10. First-Week Activities

- **Day 1:** IT activation (M365, Authenticator, laptop). Read [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md). Manager intro 1:1 with Daniel. Meet your product line partner EM (Cloud, Intelligence, or Workspace).
- **Day 2:** Read all three product overviews and your product line's deeper docs. Tour Aha!, Confluence, Jira, Salesforce, Amplitude. Read the latest two PRDs in your product line's Confluence space.
- **Day 3:** Shadow a customer call. Maheshwari will schedule you as a silent observer on a discovery or check-in call. Read [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) for customer-data rules.
- **Day 4:** Meet the Tech Lead(s) of the engineering team(s) you will partner with. Read the latest RFCs in their `docs/` folders. Read [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md) for context.
- **Day 5:** Draft your first PRD section — a problem statement for a small feature, reviewed by Maheshwari. Read the PRD template in Confluence.

## 11. First-Month Deliverables

1. **Shadowed at least 5 customer calls** — discovery, check-in, win/loss. Log observations in Confluence.
2. **Drafted first PRD section** — a problem statement and success metrics for a small feature, reviewed by Maheshwari and your product line partner EM.
3. **Met all engineering counterparts** — at least one Tech Lead and one EM per team you will partner with.
4. **Tour of all PM tooling complete** — Aha!, Confluence, Jira, Salesforce, Amplitude, Figma, GitHub read-only.
5. **Completed all Week 1–4 training** in section 9 plus the role-specific workshops.
6. **First backlog grooming session** — co-run a backlog grooming session with your engineering partner EM.

## 12. 30/60/90-Day Expectations

| Window | Expectation |
|--------|-------------|
| **30 days** | Tooling setup complete. Shadow 5 customer calls. Draft first PRD section. Meet all engineering counterparts. Complete security, privacy, product, and partner-engineering training. |
| **60 days** | Own a small feature PRD end-to-end (problem → success metrics → solution options → engineering handoff → delivery tracking → launch). Present the PRD to the engineering team in their design review. Begin attending customer calls as a participant (not just observer). Run your first backlog grooming session independently. |
| **90 days** | Own a quarterly initiative for your product line (multiple features tied to a strategic theme). Drive a section of the next quarter's roadmap (in Aha!). Lead a customer advisory board session or a customer win/loss review. Co-present at the monthly product review to Daniel and the broader PM org. |

## 13. Team Meetings

| Meeting | Cadence | Owner | Your role |
|---------|---------|-------|-----------|
| Product org standup | 15 min, 09:00 PST | Daniel Coelho | Attend (note: late evening IST — async follow-up acceptable) |
| Product line standup (Cloud / Intelligence / Workspace) | 15 min, daily | Your product line lead PM | Attend |
| Sprint planning (with engineering) | 60 min, every other Monday | Your partner EM | Attend; co-prioritize |
| Sprint review & retro | 60 min, every other Friday | Your partner EM | Attend; demo business impact |
| 1:1 with manager | 30 min, weekly | Daniel Coelho | Career, blockers, feedback |
| 1:1 with buddy | 30 min, weekly for first 6 weeks | Maheshwari Krishnan | Questions, peer feedback |
| 1:1 with partner EM | 30 min, weekly | Your partner EM | Delivery coordination |
| Customer call shadowing | 3–5 calls per week for first 4 weeks | Customer-facing PM or Sales | Attend as observer |
| Monthly product review | 90 min, monthly | Daniel Coelho | Attend; present after 60 days |
| All-hands | 60 min, monthly | Sridhar Venkatesh | Attend |

## 14. Escalation Contacts

Use the following contacts in priority order. See [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for the full directory.

| Need | Contact | How |
|------|---------|-----|
| PRD / roadmap / customer discovery question | Buddy: Maheshwari Krishnan (maheshwari.krishnan@acme.example) | Teams DM or `#product` |
| People/career/scope | Director: Daniel Coelho (daniel.coelho@acme.example) | 1:1 or Teams DM |
| Delivery / engineering coordination | Your partner EM (Cloud / Intelligence / Workspace) | 1:1 or product line channel |
| HR / leave / payroll / policy | HRBP: Kavya Krishnan (kavya.krishnan@acme.example) — covers Product | `hr.acme.example`, then Teams DM |
| IT (laptop, VPN, M365, software) | IT Helpdesk | `helpdesk.acme.example` or `#it-helpdesk` |
| Customer data privacy question (Salesforce, interview data) | Privacy Office + CISO designate | `privacy@acme.example` |
| Security incident or suspected breach | SOC + CISO Rajan Mehta | `soc@acme.example` + 24/7 hotline in [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md) |
| Sales / GTM coordination | Director Sales: Christina Müller (christina.muller@acme.example) | Email or `#sales-product-sync` |
| Support / customer issue escalation | Director Customer Support: Bo Tan (bo.tan@acme.example) | Email or `#support-product-sync` |
| Pricing / contracts question | Director Legal: Hemant Joshi (hemant.joshi@acme.example) + Finance | Email Legal, cc Daniel |

## Related Documents

- [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md)
- [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md)
- [`07-workflows/first-30-days.md`](../07-workflows/first-30-days.md)
- [`07-workflows/first-60-days.md`](../07-workflows/first-60-days.md)
- [`07-workflows/first-90-days.md`](../07-workflows/first-90-days.md)
- [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md)
- [`08-forms/software-access-request.md`](../08-forms/software-access-request.md)
- [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- [`metadata/glossary.md`](../metadata/glossary.md)
