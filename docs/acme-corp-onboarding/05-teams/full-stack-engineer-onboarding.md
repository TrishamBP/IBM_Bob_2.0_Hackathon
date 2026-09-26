---
document_id: ACME-TEAM-003
title: ACME Corp Full Stack Engineer Onboarding
category: team-onboarding
department: workspace
applicable_roles: [full-stack-engineer]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [team-onboarding, full-stack-engineer]
---

# ACME Corp Full Stack Engineer Onboarding

Welcome to the **Workspace Web** and **Workspace API** teams at ACME Corp. As a Full Stack Engineer, you will contribute to both the web frontend and the backend API for ACME Workspace, our productivity suite. This guide is your single reference for the first 90 days. It assumes you have already completed [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) and [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md).

> ACME Corp is a fictional company. All names, repositories, hosts, and systems referenced here are illustrative and use the `.example` domain. Do not attempt to reach any URL.

## 1. Team Overview

| Field | Value |
|-------|-------|
| Teams | Workspace Web (primary) + Workspace API (secondary) |
| Reports up to | Sridhar Venkatesh (VP Engineering / CTO) via EMs Thomas Buckley (Web) and Priya Menon (API) |
| Primary offices | London (Web), Hyderabad (API) — hybrid remote across all ACME offices |
| Primary product | ACME Workspace — see [`06-product/acme-workspace-overview.md`](../06-product/acme-workspace-overview.md) |
| Primary repositories | `acme-workspace-web` + `acme-workspace-api` |
| Primary channels | `#workspace-web`, `#workspace-api` (Microsoft Teams) |

**Mission.** Build and operate ACME Workspace, the productivity suite that includes document editing, real-time collaboration, video conferencing, and project tracking. Workspace competes in the enterprise productivity segment.

**Charter.** Owns the web frontend, the public API surface (Java/Spring Boot), the real-time collaboration service (WebRTC), and the document data model. Does **not** own the underlying platform infrastructure (Platform Infrastructure team), ACME Cloud's resource APIs (Cloud API), or ACME Intelligence features.

**Customers.** Knowledge workers at enterprise customers (end users); IT administrators (Workspace admin console); ACME Sales (demo tenants); ACME Support (admin tooling).

## 2. Reporting Manager

You have **two reporting lines** because of the full-stack nature of the role:

- **Primary EM (Workspace Web):** Thomas Buckley (thomas.buckley@acme.example, London office, hybrid). Owns your career, performance, and day-to-day work distribution.
- **Secondary EM (Workspace API):** Priya Menon (priya.menon@acme.example, Hyderabad office, hybrid). Co-signs API work, attend her standup when you have API-side tasks.

Both report to Sridhar Venkatesh (VP Engineering / CTO). Your standing 1:1 is weekly with Thomas; you have a biweekly 1:1 with Priya. Thomas is your HR system manager of record at `hr.acme.example`.

## 3. Onboarding Buddy

- **Buddy:** Hannah Park (hannah.park@acme.example), Tech Lead, Workspace Web.
- Hannah is your peer mentor for the first 90 days across both repos.
- For API-specific questions, Hannah will route you to Madhav Rao (Tech Lead, Workspace API — madhav.rao@acme.example), but Hannah remains your buddy of record.
- Buddy commitment: 2 hours per day for the first 2 weeks; 1 hour per day for weeks 3–6; ad-hoc thereafter.
- See [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) for the buddy program's expectations.

## 4. Required Documents (Week 1)

Read each of the following in your first week. Hannah will check progress during your week-1 1:1.

- [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md)
- [`00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- [`00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- [`00-company/communication-guidelines.md`](../00-company/communication-guidelines.md)
- [`03-security/information-security-policy.md`](../03-security/information-security-policy.md)
- [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md)
- [`03-security/customer-data-handling.md`](../03-security/customer-data-handling.md)
- [`04-engineering/developer-workstation-setup.md`](../04-engineering/developer-workstation-setup.md)
- [`04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md)
- [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md)
- [`04-engineering/repositories/acme-workspace-web.md`](../04-engineering/repositories/acme-workspace-web.md)
- [`04-engineering/repositories/acme-workspace-api.md`](../04-engineering/repositories/acme-workspace-api.md)
- [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md)
- [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md)
- [`04-engineering/practices/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md)
- [`06-product/acme-workspace-overview.md`](../06-product/acme-workspace-overview.md)

## 5. Required Software

Install only the approved tools below. Anything else requires a software access request via [`08-forms/software-access-request.md`](../08-forms/software-access-request.md). See [`02-it/approved-software-installation.md`](../02-it/approved-software-installation.md) for the binding policy.

**Workstation baseline (installed by IT before Day 1):**
- Windows 11 Enterprise or macOS 14+
- Microsoft 365 — Outlook, Teams, OneDrive
- Microsoft Authenticator, Corporate VPN client, 1Password, Microsoft Defender for Endpoint

**Developer tools — Frontend (acme-workspace-web):**
- Visual Studio Code (latest stable)
- Node.js 20 LTS (via nvm), pnpm 9
- Docker Desktop (for local collaboration service container)
- Playwright browsers (installed via `pnpm dlx playwright install`)

**Developer tools — Backend (acme-workspace-api):**
- Java 21 (Temurin), Maven 3.9 (matches the repo's `pom.xml`)
- Docker Desktop (shared with frontend)
- `psql` client for local Postgres
- GitHub CLI (`gh`) configured for `git.acme.example`

**Browsers (testing matrix):** Chrome, Microsoft Edge, Firefox ESR, Safari (for WebRTC compatibility).

## 6. Approved AI Tools

Per the role eligibility matrix in [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md), Full Stack Engineers are **default-entitled** to:

| Tool | Entitlement | Notes |
|------|-------------|-------|
| GitHub Copilot Business | **Yes (default)** | Sign in only with `@acme.example` Entra SSO. Never use a personal GitHub account. |
| Internal ACME Intelligence sandbox | Optional | Not granted by default. Request via [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md) only if a work item requires it. |

Both `acme-workspace-web` and `acme-workspace-api` are opted in to Copilot via their `copilot-instructions.md` files. Read [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) before prompting — never enter customer data, secrets, or third-party source into Copilot Chat.

## 7. Required Repositories

You will be granted read/write access to the following:

- `acme-workspace-web` — frontend (TypeScript, React, WebRTC). See [`04-engineering/repositories/acme-workspace-web.md`](../04-engineering/repositories/acme-workspace-web.md).
- `acme-workspace-api` — backend (Java, Spring Boot, PostgreSQL, Kafka). See [`04-engineering/repositories/acme-workspace-api.md`](../04-engineering/repositories/acme-workspace-api.md).

Read-only cross-repo access (auto-granted for context):

- `acme-shared-libraries` — shared libraries across Web and API (auth client, error reporting).

Repository access is requested via [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md). Thomas pre-approves Web repo; Priya pre-approves API repo.

You will **not** receive access to `acme-cloud-*`, `acme-intelligence-*`, or `acme-platform-infrastructure` unless a specific work item requires it. This is per [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).

## 8. Required Access Permissions

On Day 1, IT Onboarding (Geetha Iyer, `geetha.iyer@acme.example`) provisions the following Entra ID groups. Verify each in the My Apps portal at `myapps.acme.example`.

| Entra ID group | Purpose |
|----------------|---------|
| `ENG-Workspace-Web` | Repository write access to `acme-workspace-web`. |
| `ENG-Workspace-API` | Repository write access to `acme-workspace-api`. |
| `ENG-Shared-Libraries-Read` | Read-only access to `acme-shared-libraries`. |
| `Vault-Customer-Workspace-Web-Dev` | Personal HashiCorp Vault token scoped to `secret/workspace-web/dev/*`. |
| `Vault-Customer-Workspace-API-Dev` | Personal HashiCorp Vault token scoped to `secret/workspace-api/dev/*`. |
| `Copilot-Business-Engineering` | GitHub Copilot Business seat assignment. |
| `Observability-Reader-NonProd` | Read-only Grafana non-production dashboards. |
| `Kafka-Consumer-Workspace-API-Dev` | Dev-cluster Kafka consumer group membership. |

Additional tools (auto-provisioned):

- **Figma** — design files via SSO.
- **Storybook** (internal) — read with Entra SSO.
- **Twilio/WWebRTC test accounts** — required for local WebRTC dev; tokens in Vault.

Production access is **not** granted at onboarding.

## 9. Training Requirements

Complete the following training in your first 30 days. All training is tracked in your learning transcript at `hr.acme.example/learning`.

| Course | Link | Deadline |
|--------|------|---------|
| Company Orientation | [`10-training/company-orientation.md`](../10-training/company-orientation.md) | Week 1 |
| Security Awareness | [`10-training/security-awareness.md`](../10-training/security-awareness.md) | Week 1 |
| Privacy Awareness | [`10-training/privacy-awareness.md`](../10-training/privacy-awareness.md) | Week 2 |
| Engineering Orientation | [`10-training/engineering-orientation.md`](../10-training/engineering-orientation.md) | Week 2 |
| Git and Repository Workflows | [`10-training/git-and-repository-workflows.md`](../10-training/git-and-repository-workflows.md) | Week 2 |
| AI Coding Assistant Usage | [`10-training/ai-coding-assistant-usage.md`](../10-training/ai-coding-assistant-usage.md) | Week 3 |
| ACME Workspace Product Training | [`10-training/product-training.md`](../10-training/product-training.md) | Week 3 |
| Cloud Platform Fundamentals | [`10-training/cloud-platform-fundamentals.md`](../10-training/cloud-platform-fundamentals.md) | Week 4 |
| Workplace Conduct | [`10-training/workplace-conduct.md`](../10-training/workplace-conduct.md) | Week 4 |

## 10. First-Week Activities

- **Day 1:** IT activation (M365, Authenticator, laptop). Read [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md). Manager intro 1:1 with Thomas; meet Priya for 15 minutes.
- **Day 2:** Clone both repos. Bring up `acme-workspace-api` locally (`mvn spring-boot:run` against Docker Postgres). Bring up `acme-workspace-web` (`pnpm install && pnpm dev`). Verify the frontend talks to the local API.
- **Day 3:** Configure VS Code, sign into GitHub Copilot via Entra SSO. Read the `README.md` of each repo and the relevant per-repo doc.
- **Day 4:** Pick a `good-first-issue` from the Web repo. Create your first branch per [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md).
- **Day 5:** Open your first PR. Request review from Hannah. Read [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md) before requesting review.

## 11. First-Month Deliverables

1. **Merged PR #1 (Web)** — a `good-first-issue` in `acme-workspace-web`.
2. **Merged PR #2 (API)** — a small backend task assigned by Priya via Madhav, with unit + integration tests.
3. **End-to-end local environment** — frontend ↔ API ↔ Postgres ↔ Kafka running locally, all via Docker.
4. **Completed all Week 1–4 training** in section 9.
5. **First shadow on-call shift** — paired with the on-call engineer for one weekday evening, following [`04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md).
6. **One cross-stack PR** — a small change that touches both Web and API in the same sprint (e.g., adding a field to an API response and rendering it in the Web).

## 12. 30/60/90-Day Expectations

| Window | Expectation |
|--------|-------------|
| **30 days** | Local setup complete (both repos). First small PR merged in each repo. Pair with buddy on at least 3 PRs. Shadow one on-call shift. Complete security, privacy, engineering, and AI-assistant training. |
| **60 days** | Ship a feature-sized change that spans Web and API (e.g., a new settings page that reads and writes a new API resource) with Web + API tests. Participate in code review as a reviewer on at least 4 PRs (mix of Web and API). Complete an on-call shadow rotation (one full week of evening shifts, with a backup on call). Begin owning one component area in Web or one service area in API. |
| **90 days** | Ship a medium-sized feature end-to-end (design → PR → staging → production release, across Web and API). Lead a small design doc (RFC) for a feature in your component area, reviewed by Thomas, Priya, and Hannah. Take a primary on-call shift (with backup) for at least one weekday. Be the assigned reviewer on at least 8 PRs. |

## 13. Team Meetings

| Meeting | Cadence | Owner | Your role |
|---------|---------|-------|-----------|
| Workspace Web standup | 15 min, 10:00 GMT | Thomas Buckley | Attend daily |
| Workspace API standup | 15 min, 10:30 IST | Priya Menon | Attend on days with API tasks |
| Joint sprint planning | 60 min, every other Monday | Thomas + Priya | Estimate, sign up for cross-stack work |
| Sprint review & retro | 60 min, every other Friday | Thomas + Priya | Demo; raise retro items |
| 1:1 with Thomas | 30 min, weekly | Thomas Buckley | Career, blockers, feedback |
| 1:1 with Priya | 30 min, biweekly | Priya Menon | API-side feedback |
| 1:1 with buddy | 30 min, weekly for first 6 weeks | Hannah Park | Questions, peer feedback |
| Workspace cross-stack design review | 60 min, weekly | Hannah Park + Madhav Rao | Present your cross-stack RFCs |
| All-hands | 60 min, monthly | Sridhar Venkatesh | Attend |

## 14. Escalation Contacts

Use the following contacts in priority order. See [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for the full directory.

| Need | Contact | How |
|------|---------|-----|
| Web technical question | Buddy: Hannah Park (hannah.park@acme.example) | Teams DM or `#workspace-web` |
| API technical question | Tech Lead: Madhav Rao (madhav.rao@acme.example) | Teams DM or `#workspace-api` |
| People/career/scope | Primary manager: Thomas Buckley (thomas.buckley@acme.example) | 1:1 or Teams DM |
| API-side scope concerns | Secondary manager: Priya Menon (priya.menon@acme.example) | 1:1 or Teams DM |
| HR / leave / payroll / policy | HRBP: Kavya Krishnan (kavya.krishnan@acme.example) — covers Workspace | `hr.acme.example`, then Teams DM |
| IT (laptop, VPN, M365, software) | IT Helpdesk | `helpdesk.acme.example` or `#it-helpdesk` |
| Security incident or suspected breach | SOC + CISO Rajan Mehta | `soc@acme.example` + 24/7 hotline in [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md) |
| Production outage | On-call engineer + Thomas (Web) or Priya (API) | PagerDuty rotation `workspace-web-oncall` / `workspace-api-oncall` |
| Cross-team dependency (Platform, Cloud, Intelligence) | Receiving EM via Thomas | Thomas routes |

## Related Documents

- [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md)
- [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md)
- [`07-workflows/first-30-days.md`](../07-workflows/first-30-days.md)
- [`07-workflows/first-60-days.md`](../07-workflows/first-60-days.md)
- [`07-workflows/first-90-days.md`](../07-workflows/first-90-days.md)
- [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md)
- [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md)
- [`08-forms/software-access-request.md`](../08-forms/software-access-request.md)
- [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- [`metadata/glossary.md`](../metadata/glossary.md)
