---
document_id: ACME-TEAM-012
title: ACME Corp Customer Support Engineer Onboarding
category: team-onboarding
department: customer-support
applicable_roles: [customer-support-engineer]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [team-onboarding, customer-support-engineer]
---

# ACME Corp Customer Support Engineer Onboarding

Welcome to the **Customer Support** organization at ACME Corp. This guide is your single reference for the first 90 days as a Customer Support Engineer helping enterprise customers succeed with ACME Cloud, ACME Intelligence, and ACME Workspace. It assumes you have already completed [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) and [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md).

> ACME Corp is a fictional company. All names, repositories, hosts, and systems referenced here are illustrative and use the `.example` domain. Do not attempt to reach any URL.

## 1. Team Overview

| Field | Value |
|-------|-------|
| Team name | Customer Support |
| Reports up to | Bo Tan (Director Customer Support), who reports to the CEO office |
| Primary offices | Seattle (Bo's home office), with support engineers distributed across Hyderabad, Bengaluru, London to provide follow-the-sun coverage |
| Primary products | ACME Cloud, ACME Intelligence, ACME Workspace — see product overviews |
| Primary tooling | Zendesk (ticketing), StatusPage (customer-facing status), Looker (support analytics), GitHub Enterprise (read-only for code context), internal Runbook portal at `runbooks.internal.acme.example` |
| Primary channel | `#customer-support` (Microsoft Teams); each product line also has its own support channel |

**Mission.** Provide tier-2 and tier-3 technical support to enterprise customers across ACME's three product lines, including incident triage, root-cause analysis, customer-facing communications, and runbook authorship. The team also drives known-issue feedback loops into Engineering and Product.

**Charter.** Owns the support incident lifecycle, customer-facing status communications, runbook library, and the engineering-to-support feedback loop. Does **not** own customer success/account management (post-close success is shared with Sales), product strategy (PM owns that), or engineering fixes (Engineering owns that — Support escalates and tracks).

**Customers.** Technical contacts at enterprise customers (cloud architects, DevOps engineers, IT administrators), ACME Sales (for post-sale escalations), ACME Engineering (for bug escalations and RCA collaboration).

## 2. Reporting Manager

- **Director:** Bo Tan (bo.tan@acme.example, Seattle office, hybrid).
- Bo reports to the CEO office.
- Your standing 1:1 is 30 minutes weekly.
- Reporting line is recorded at `hr.acme.example` under your profile.
- You will also be assigned to one of three product-line support pods (Cloud, Intelligence, or Workspace) and to a follow-the-sun shift.

## 3. Onboarding Buddy

- **Buddy:** Bo Tan (bo.tan@acme.example, Director Customer Support) serves as your buddy for the first 90 days. For a Support team of ACME's size, the Director personally buddies new support engineers to set the tone for customer engagement standards.
- Bo is your peer mentor for the first 90 days — incident triage workflow, RCA conventions, customer-facing communication standards, escalation patterns to Engineering.
- Buddy commitment: 2 hours per day for the first 2 weeks (shift overlap), then 1 hour per day for weeks 3–6, then ad-hoc.
- See [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) for the buddy program's expectations.

## 4. Required Documents (Week 1)

Read each of the following in your first week. Bo will check progress during your week-1 1:1.

- [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md)
- [`00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- [`00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- [`00-company/communication-guidelines.md`](../00-company/communication-guidelines.md)
- [`00-company/products-and-business-units.md`](../00-company/products-and-business-units.md)
- [`03-security/information-security-policy.md`](../03-security/information-security-policy.md)
- [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md)
- [`03-security/customer-data-handling.md`](../03-security/customer-data-handling.md)
- [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md)
- [`04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md)
- [`06-product/acme-cloud-overview.md`](../06-product/acme-cloud-overview.md)
- [`06-product/acme-intelligence-overview.md`](../06-product/acme-intelligence-overview.md)
- [`06-product/acme-workspace-overview.md`](../06-product/acme-workspace-overview.md)
- [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md)
- [`10-training/product-training.md`](../10-training/product-training.md)
- [`10-training/workplace-conduct.md`](../10-training/workplace-conduct.md)

## 5. Required Software

Install only the approved tools below. Anything else requires a software access request via [`08-forms/software-access-request.md`](../08-forms/software-access-request.md). See [`02-it/approved-software-installation.md`](../02-it/approved-software-installation.md) for the binding policy.

**Workstation baseline (installed by IT before Day 1):**
- Windows 11 Enterprise or macOS 14+
- Microsoft 365 — Outlook, Teams, OneDrive, Word, Excel
- Microsoft Authenticator, Corporate VPN, 1Password, Microsoft Defender for Endpoint

**Support-specific tools (provisioned via Entra SSO):**
- Zendesk (ticketing) — `Agent` seat at `tickets.internal.acme.example`
- StatusPage (customer-facing status) — `Manager` seat
- Looker (support analytics) — `Viewer` seat
- GitHub Enterprise (read-only — see section 7)
- Internal Runbook portal — `Editor` at `runbooks.internal.acme.example`
- Slack Connect (for shared channels with key customers) — `Admin` (limited)
- Zoom or Microsoft Teams (customer calls) — already provisioned via M365

**Developer tools (read-only context — you will read code but not write it):**
- Visual Studio Code (latest stable) with read-only GitHub auth
- GitHub CLI (`gh`) configured for `git.acme.example` (read-only)
- `jq`, `yq`, `httpie`, `curl` for debugging customer API calls

## 6. Approved AI Tools

Per the role eligibility matrix in [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md), Customer Support Engineers are **not entitled** to ACME engineering AI tools:

| Tool | Entitlement | Notes |
|------|-------------|-------|
| GitHub Copilot Business | **No** | Support engineers do not write production code and do not receive a Copilot seat. Do not request one via [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md) — it will be declined. |
| Internal ACME Intelligence sandbox | **No** | Not provisioned. |

If you need AI assistance for writing (runbooks, customer comms, internal docs), use Microsoft Copilot for Microsoft 365, governed by [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md). Zendesk AI features (e.g., answer bot, macro suggestions) are governed by Zendesk enterprise policy and the ACME acceptable-use policy.

Do **not** enter customer-identifying information or customer logs into public AI tools — see [`03-security/customer-data-handling.md`](../03-security/customer-data-handling.md) and [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md).

## 7. Required Repositories

You will be granted **read-only** access to ACME's Workspace repositories per the access tier matrix in [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md), with broader read access for context:

- `acme-workspace-web` — Workspace web frontend (read-only)
- `acme-workspace-api` — Workspace backend (read-only)
- `acme-shared-libraries` — read-only (shared libraries)

Read-only cross-repo access for context (auto-granted):

- `acme-cloud-api`, `acme-cloud-frontend` — read-only
- `acme-intelligence-agents`, `acme-intelligence-inference`, `acme-intelligence-ml` — read-only
- `acme-platform-infrastructure`, `acme-quality-automation` — read-only

The repo access is for:

- Reading runbooks and known-issue notes in `docs/` folders
- Reviewing PR descriptions and release notes (to understand recent changes that may have caused a customer incident)
- Filing bug-escalation issues (you can create issues but not PRs)

You will **not** receive write access to any repository — that would violate [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md). Code changes are made by the owning engineering team.

Repository access is requested via [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md). Bo pre-approves the bulk read-only bundle.

## 8. Required Access Permissions

On Day 1, IT Onboarding (Geetha Iyer, `geetha.iyer@acme.example) provisions the following Entra ID groups. Verify each in the My Apps portal at `myapps.acme.example`.

| Entra ID group | Purpose |
|----------------|---------|
| `Customer-Support` | Membership in the Support org; Zendesk, StatusPage, Looker seats. |
| `ENG-Workspace-Web-Read` | Read-only access to `acme-workspace-web`. |
| `ENG-Workspace-API-Read` | Read-only access to `acme-workspace-api`. |
| `ENG-Shared-Libraries-Read` | Read-only access to `acme-shared-libraries`. |
| `ENG-All-Read` (limited) | Read-only access to remaining production repos for RCA context. |
| `Vault-Customer-Support-Reader-Staging` | Vault read-only token scoped to `secret/customer-support/staging/*` (used to verify customer-config issues without exposing production secrets). |
| `Observability-Reader-Staging` | Read-only Grafana staging dashboards (for customer-incident triage in staging). |
| `Observability-Reader-Production-Limited` | Limited read-only access to production Grafana dashboards for the products you support (filters restrict to your product line). |
| `Runbooks-Editor` | Editor access to the internal Runbook portal. |
| `Slack-Connect-Admin` | Admin on shared Slack Connect channels with key customers (limited scope). |

Additional tools (auto-provisioned):

- **Zendesk** — `Agent` seat.
- **StatusPage** — `Manager` seat (can post customer-facing status updates during incidents, with Bo's sign-off).

Production Vault write, cluster admin, and CI runner access is **not** granted.

## 9. Training Requirements

Complete the following training in your first 30 days. All training is tracked in your learning transcript at `hr.acme.example/learning`.

| Course | Link | Deadline |
|--------|------|---------|
| Company Orientation | [`10-training/company-orientation.md`](../10-training/company-orientation.md) | Week 1 |
| Security Awareness | [`10-training/security-awareness.md`](../10-training/security-awareness.md) | Week 1 |
| Privacy Awareness | [`10-training/privacy-awareness.md`](../10-training/privacy-awareness.md) | Week 1 (high priority — you handle customer data) |
| Product Training (all three products) | [`10-training/product-training.md`](../10-training/product-training.md) | Week 2 (high priority — customer-facing) |
| Workplace Conduct | [`10-training/workplace-conduct.md`](../10-training/workplace-conduct.md) | Week 2 (high priority — customer-facing) |
| Engineering Orientation | [`10-training/engineering-orientation.md`](../10-training/engineering-orientation.md) | Week 2 (read-only — understand engineering workflow so you can escalate effectively) |
| Git and Repository Workflows | [`10-training/git-and-repository-workflows.md`](../10-training/git-and-repository-workflows.md) | Week 3 (read-only — understand how to file bug-escalation issues) |
| Cloud Platform Fundamentals | [`10-training/cloud-platform-fundamentals.md`](../10-training/cloud-platform-fundamentals.md) | Week 3 (so you can speak credibly about ACME's platform) |

Additional role-specific training delivered by Bo in weeks 2–4:
- "Zendesk at ACME" workshop (2 hours).
- "Incident triage workflow and severity" workshop (2 hours).
- "RCA conventions and the engineering escalation loop" workshop (2 hours).
- "Customer-facing status communications" briefing by Bo (1 hour).
- "Runbook authoring" workshop (1 hour).

## 10. First-Week Activities

- **Day 1:** IT activation (M365, Authenticator, laptop). Read [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md). Manager intro 1:1 with Bo. Meet your product line support pod.
- **Day 2:** Tour Zendesk, StatusPage, Looker, Runbook portal, GitHub read-only. Read all three product overviews and your product line's runbook index.
- **Day 3:** Shadow at least 3 customer tickets with an experienced support engineer. Bo will assign you as a watcher on P2 and P3 tickets (P1 tickets are reserved for tenured engineers during your first 2 weeks). Read [`03-security/customer-data-handling.md`](../03-security/customer-data-handling.md).
- **Day 4:** Meet the EM and Tech Lead of the engineering team(s) you will partner with. Read their runbook and known-issue notes. Read [`04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md).
- **Day 5:** Handle your first P3 ticket independently (with Bo reviewing your reply before send). Draft your first runbook addition for the next known issue.

## 11. First-Month Deliverables

1. **Shadowed at least 15 customer tickets** — across severities P1 (observe only), P2, P3. Log observations in your learning journal.
2. **Handled your first 10 P3 tickets independently** — initial reply, root-cause investigation, resolution or escalation, all within SLA.
3. **Authored your first runbook** — a new or updated runbook for a known issue, reviewed by Bo and the partner engineering Tech Lead.
4. **Escalated your first P2 to Engineering** — with a properly triaged escalation document (repro steps, customer impact, suspect area), tracked in GitHub issues.
5. **Tour of all support tooling complete** — Zendesk, StatusPage, Looker, GitHub read-only, Runbook portal.
6. **Completed all Week 1–4 training** in section 9 plus the role-specific workshops.

## 12. 30/60/90-Day Expectations

| Window | Expectation |
|--------|-------------|
| **30 days** | Tooling setup complete. Shadow 15 tickets. Handle 10 P3 tickets independently. Author first runbook. Escalate first P2. Complete security, privacy, product, workplace-conduct, and partner-engineering training. |
| **60 days** | Take primary on a follow-the-sun shift for P2 tickets (with backup). Run a full incident triage independently (gather customer impact, declare severity, route to engineering, post StatusPage update with Bo's sign-off). Co-author an RCA with engineering for a P2 incident. Begin owning one product area's runbook library. |
| **90 days** | Take primary on a follow-the-sun shift for P1 tickets (with backup and Bo on standby). Independently author an RCA for a P2 incident and present it to engineering. Own one product area's runbook library end-to-end (curate, update, deprecate). Co-present at the monthly support review to Bo and the broader Support org. Be eligible for the next P1 on-call rotation as a primary (with backup). |

## 13. Team Meetings

| Meeting | Cadence | Owner | Your role |
|---------|---------|-------|-----------|
| Support pod standup | 15 min, daily (per shift) | Your pod lead | Attend; share your top open ticket and blockers |
| Product line sync (with engineering) | 30 min, weekly | Your partner EM + pod lead | Attend; surface known issues, get roadmap context |
| 1:1 with manager | 30 min, weekly | Bo Tan | Career, blockers, ticket coaching |
| 1:1 with buddy (also Bo) | 30 min, daily for first 2 weeks, then weekly | Bo Tan | Ticket coaching, escalation review |
| Severity-1 incident bridge (when active) | Ad-hoc, on-call | Incident commander + Bo | Attend if on shift; observe if not |
| RCA review (post-incident) | 60 min, weekly | Bo Tan | Attend; present your RCAs after 60 days |
| Runbook review | 60 min, biweekly | Pod lead | Attend; present your runbook additions |
| All-hands | 60 min, monthly | Sridhar Venkatesh | Attend |

## 14. Escalation Contacts

Use the following contacts in priority order. See [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for the full directory.

| Need | Contact | How |
|------|---------|-----|
| Ticket / triage / customer comms question | Buddy & Director: Bo Tan (bo.tan@acme.example) | 1:1 or Teams DM |
| Engineering escalation (suspected bug) | Your partner EM + Tech Lead (via the escalation workflow in your runbook) | GitHub issue + Teams DM |
| Severity-1 incident (customer down) | On-call engineer (PagerDuty) + Bo + relevant product EM | See runbook: declare Sev-1, page on-call, ping Bo |
| People/career/scope | Director: Bo Tan (bo.tan@acme.example) | 1:1 or Teams DM |
| HR / leave / payroll / policy | HRBP: Deepika Rao (deepika.rao@acme.example) — covers Support | `hr.acme.example`, then Teams DM |
| IT (laptop, VPN, M365, Zendesk, software) | IT Helpdesk | `helpdesk.acme.example` or `#it-helpdesk` |
| Customer data privacy question (Zendesk, support logs) | Privacy Office + CISO designate | `privacy@acme.example` |
| Security incident or suspected breach (incl. customer-data exposure) | SOC + CISO Rajan Mehta | `soc@acme.example` + 24/7 hotline in [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md) |
| Sales / account handoff for at-risk customers | Director Sales: Christina Müller (christina.muller@acme.example) | Email or `#support-sales-handoff` |

## Related Documents

- [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md)
- [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md)
- [`07-workflows/first-30-days.md`](../07-workflows/first-30-days.md)
- [`07-workflows/first-60-days.md`](../07-workflows/first-60-days.md)
- [`07-workflows/first-90-days.md`](../07-workflows/first-90-days.md)
- [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md)
- [`08-forms/software-access-request.md`](../08-forms/software-access-request.md)
- [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- [`metadata/glossary.md`](../metadata/glossary.md)
