---
document_id: ACME-TEAM-008
title: ACME Corp Quality Engineer Onboarding
category: team-onboarding
department: quality-engineering
applicable_roles: [quality-engineer]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [team-onboarding, quality-engineer]
---

# ACME Corp Quality Engineer Onboarding

Welcome to the **Quality Engineering** team at ACME Corp. This guide is your single reference for the first 90 days as a Quality Engineer building the cross-product test automation, performance, and reliability tooling that every product team depends on. It assumes you have already completed [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) and [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md).

> ACME Corp is a fictional company. All names, repositories, hosts, and systems referenced here are illustrative and use the `.example` domain. Do not attempt to reach any URL.

## 1. Team Overview

| Field | Value |
|-------|-------|
| Team name | Quality Engineering |
| Reports up to | Sridhar Venkatesh (VP Engineering / CTO) via EM Asha Reddy |
| Primary office | Bengaluru (with hybrid remote) |
| Primary product | Shared quality tooling — used by ACME Cloud, ACME Intelligence, ACME Workspace |
| Primary repository | `acme-quality-automation` — see [`04-engineering/repositories/acme-quality-automation.md`](../04-engineering/repositories/acme-quality-automation.md) |
| Primary channel | `#quality-engineering` (Microsoft Teams), `#qe-help` (cross-team) |

**Mission.** Build and operate the shared quality automation platform: end-to-end test suites, performance and load testing (JMeter), visual regression (Chromatic), accessibility scanning, reliability chaos experiments, and the quality analytics dashboard.

**Charter.** Owns the shared quality tooling, the cross-product test plan templates, the release-gate quality checks, and the quality analytics. Does **not** own product-specific unit tests (those are owned by the product teams), and does **not** own production infrastructure (Platform Infrastructure).

**Customers.** Every engineering team at ACME — QE provides the automation framework, the runners, and the dashboards; product teams write and maintain their own tests on top. Secondary customer: ACME Support (relies on QE dashboards for known-issue triage).

## 2. Reporting Manager

- **Engineering Manager:** Asha Reddy (asha.reddy@acme.example, Bengaluru office, hybrid).
- Asha reports to Sridhar Venkatesh (VP Engineering / CTO).
- Your standing 1:1 is 30 minutes weekly.
- Reporting line is recorded at `hr.acme.example` under your profile.

## 3. Onboarding Buddy

- **Buddy:** Sandeep Kulkarni (sandeep.kulkarni@acme.example), Tech Lead, Quality Engineering.
- Sandeep is your peer mentor for the first 90 days — Playwright patterns, JMeter scenarios, the quality analytics dashboard, the release-gate pipeline.
- Buddy commitment: 2 hours per day for the first 2 weeks; 1 hour per day for weeks 3–6; ad-hoc thereafter.
- See [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) for the buddy program's expectations.

## 4. Required Documents (Week 1)

Read each of the following in your first week. Sandeep will check progress during your week-1 1:1.

- [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md)
- [`00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- [`00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- [`00-company/communication-guidelines.md`](../00-company/communication-guidelines.md)
- [`03-security/information-security-policy.md`](../03-security/information-security-policy.md)
- [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md)
- [`04-engineering/developer-workstation-setup.md`](../04-engineering/developer-workstation-setup.md)
- [`04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md)
- [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md)
- [`04-engineering/repositories/acme-quality-automation.md`](../04-engineering/repositories/acme-quality-automation.md)
- [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md)
- [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md)
- [`04-engineering/practices/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md)
- [`04-engineering/practices/unit-and-integration-testing.md`](../04-engineering/practices/unit-and-integration-testing.md)
- [`06-product/acme-cloud-overview.md`](../06-product/acme-cloud-overview.md)
- [`06-product/acme-intelligence-overview.md`](../06-product/acme-intelligence-overview.md)
- [`06-product/acme-workspace-overview.md`](../06-product/acme-workspace-overview.md)

## 5. Required Software

Install only the approved tools below. Anything else requires a software access request via [`08-forms/software-access-request.md`](../08-forms/software-access-request.md). See [`02-it/approved-software-installation.md`](../02-it/approved-software-installation.md) for the binding policy.

**Workstation baseline (installed by IT before Day 1):**
- Windows 11 Enterprise or macOS 14+
- Microsoft 365, Microsoft Authenticator, Corporate VPN, 1Password, Microsoft Defender for Endpoint

**Developer tools (you install via the approved package manager):**
- Visual Studio Code (latest stable)
- Python 3.11 (matches the repo's `pyproject.toml`)
- `uv` 0.4+ for dependency management
- Node.js 20 LTS and pnpm 9 (Playwright requires Node)
- Playwright browsers (`pnpm dlx playwright install --with-deps`)
- Docker Desktop (for JMeter, Chromatic, and ChaosMesh containers)
- `kubectl` (for chaos experiments against the staging cluster)
- GitHub CLI (`gh`) configured for `git.acme.example`
- `jq`, `yq`, `httpie`

**Browsers (test matrix):** Chrome, Microsoft Edge, Firefox ESR (Playwright-managed).

## 6. Approved AI Tools

Per the role eligibility matrix in [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md), Quality Engineers are **case-by-case optional** for AI tools:

| Tool | Entitlement | Notes |
|------|-------------|-------|
| GitHub Copilot Business | **Optional (case-by-case)** | Not granted by default. If your work involves heavy test scaffolding or test refactoring, your manager may request a seat via [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md). Default expectation: you will not have Copilot at onboarding. |
| Internal ACME Intelligence sandbox | Optional (case-by-case) | Same as above — request-based. |

If you do not receive a Copilot seat, do not use a personal AI tool to substitute — that violates [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md). Use the team's existing test templates and pair-programming with your buddy instead.

## 7. Required Repositories

You will be granted read/write access to the following:

- `acme-quality-automation` — your home repository. See [`04-engineering/repositories/acme-quality-automation.md`](../04-engineering/repositories/acme-quality-automation.md).

Read-only access to **all production repositories** (per the access tier matrix in [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md)):

- `acme-cloud-api`, `acme-cloud-frontend`
- `acme-intelligence-agents`, `acme-intelligence-inference`, `acme-intelligence-ml`
- `acme-workspace-web`, `acme-workspace-api`
- `acme-platform-infrastructure`, `acme-shared-libraries`

This read access is **not** for editing product code — it is so you can read tests, debug failures, and propose improvements to test structure via PRs to the product teams. Any code change to a product repo requires that team's review and approval.

Repository access is requested via [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md). Asha pre-approves your home repo. The bulk read-only bundle for production repos is approved by the receiving EMs as part of standard QE onboarding.

## 8. Required Access Permissions

On Day 1, IT Onboarding (Geetha Iyer, `geetha.iyer@acme.example) provisions the following Entra ID groups. Verify each in the My Apps portal at `myapps.acme.example`.

| Entra ID group | Purpose |
|----------------|---------|
| `ENG-QE` | Repository write access to `acme-quality-automation`. |
| `ENG-All-Read` | Read-only access to all production repos (for test debugging and proposals). |
| `Vault-Customer-QE-Dev` | Personal HashiCorp Vault token scoped to `secret/qe/dev/*` (test data, synthetic user credentials). |
| `Test-Environments-Reader-Staging` | Read-only access to staging environments across the three product lines (for E2E test execution). |
| `Observability-Reader-Staging` | Read-only Grafana staging dashboards (for performance and reliability analysis). |
| `Chaos-Mesh-Operator-Staging` | Operator role on the staging ChaosMesh namespace (for chaos experiments). |
| `Quality-Analytics-Editor` | Editor access to the quality analytics dashboard at `quality.internal.acme.example`. |
| `Copilot-Business-Engineering` | GitHub Copilot Business seat assignment — **only if your manager approved a seat.** See section 6. |

Production access is **not** granted at onboarding. QE does not deploy to production; QE runs release-gate checks against staging, and the release manager (DevOps) promotes to production.

## 9. Training Requirements

Complete the following training in your first 30 days. All training is tracked in your learning transcript at `hr.acme.example/learning`.

| Course | Link | Deadline |
|--------|------|---------|
| Company Orientation | [`10-training/company-orientation.md`](../10-training/company-orientation.md) | Week 1 |
| Security Awareness | [`10-training/security-awareness.md`](../10-training/security-awareness.md) | Week 1 |
| Privacy Awareness | [`10-training/privacy-awareness.md`](../10-training/privacy-awareness.md) | Week 2 |
| Engineering Orientation | [`10-training/engineering-orientation.md`](../10-training/engineering-orientation.md) | Week 2 |
| Git and Repository Workflows | [`10-training/git-and-repository-workflows.md`](../10-training/git-and-repository-workflows.md) | Week 2 |
| AI Coding Assistant Usage | [`10-training/ai-coding-assistant-usage.md`](../10-training/ai-coding-assistant-usage.md) | Week 3 — only if you received a Copilot seat |
| ACME Cloud / Intelligence / Workspace product training | [`10-training/product-training.md`](../10-training/product-training.md) | Week 3 (covers all three products — QE is cross-product) |
| Cloud Platform Fundamentals | [`10-training/cloud-platform-fundamentals.md`](../10-training/cloud-platform-fundamentals.md) | Week 4 |
| Workplace Conduct | [`10-training/workplace-conduct.md`](../10-training/workplace-conduct.md) | Week 4 |

Additional role-specific training delivered by Sandeep in weeks 2–4:
- "QE automation framework" workshop (2 hours).
- "Playwright patterns and conventions" workshop (2 hours).
- "Performance and load testing with JMeter" workshop (2 hours).
- "Chaos experiments with ChaosMesh" workshop (1 hour).
- "Release-gate pipeline" walkthrough (1 hour).

## 10. First-Week Activities

- **Day 1:** IT activation (M365, Authenticator, laptop). Read [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md). Manager intro 1:1 with Asha.
- **Day 2:** Clone `acme-quality-automation`. Run `uv sync` and `make test` to verify the framework tests pass. Read the repo's `README.md` and [`04-engineering/repositories/acme-quality-automation.md`](../04-engineering/repositories/acme-quality-automation.md).
- **Day 3:** Configure VS Code. If you have a Copilot seat, sign in via Entra SSO. Get your Vault token, verify staging test-environment access by running a single Playwright smoke test against staging.
- **Day 4:** Pick a `good-first-issue` labeled ticket (e.g., a flaky test fix, a Playwright helper improvement, a JMeter scenario tweak). Create your first branch per [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md).
- **Day 5:** Open your first PR. Request review from Sandeep. Read [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md) before requesting review.

## 11. First-Month Deliverables

1. **Merged PR #1** — a `good-first-issue` (flaky test fix, helper improvement, scenario tweak).
2. **Merged PR #2** — a small automation change assigned by Sandeep, with a new test or scenario that runs cleanly against staging.
3. **Local + staging environment fully working** — including Playwright, JMeter, Docker, ChaosMesh staging access, quality analytics dashboard.
4. **Completed all Week 1–4 training** in section 9 plus the role-specific workshops.
5. **First shadow on-call shift** — paired with the on-call QE engineer for one weekday evening. QE on-call covers release-gate failures and test-environment incidents. See [`04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md).
6. **One cross-product test addition** — added at least one test to a product team's suite via a PR to that team's repo (with their review).

## 12. 30/60/90-Day Expectations

| Window | Expectation |
|--------|-------------|
| **30 days** | Local + staging setup complete. First small PR merged. Pair with buddy on at least 3 PRs. Shadow one on-call shift. Complete security, privacy, engineering, and AI-assistant training plus role-specific workshops. |
| **60 days** | Ship a feature-sized change (a new test suite, a JMeter scenario, a chaos experiment, or a quality dashboard improvement) with non-prod validation. Participate in code review as a reviewer on at least 4 PRs. Complete an on-call shadow rotation (one full week of evening shifts, with a backup on call). Begin owning one product line's quality automation coverage. |
| **90 days** | Ship a medium-sized change end-to-end (test plan → automation → staging validation → release-gate integration → analytics dashboard). Lead a small design doc (RFC) for a quality improvement in your area, reviewed by Asha and Sandeep. Take a primary on-call shift (with backup) for at least one weekday. Be the assigned reviewer on at least 8 PRs. Be eligible to run release-gate sign-off for non-critical releases (with a backup). |

## 13. Team Meetings

| Meeting | Cadence | Owner | Your role |
|---------|---------|-------|-----------|
| Daily standup | 15 min, 10:00 IST | Asha Reddy | Attend, share blocker |
| Sprint planning | 60 min, every other Monday | Asha Reddy | Estimate, sign up |
| Sprint review & retrospective | 60 min, every other Friday | Asha Reddy | Demo; raise retro items |
| 1:1 with manager | 30 min, weekly | Asha Reddy | Career, blockers, feedback |
| 1:1 with buddy | 30 min, weekly for first 6 weeks | Sandeep Kulkarni | Questions, peer feedback |
| QE design review | 60 min, weekly | Sandeep Kulkarni | Present your RFCs |
| Cross-product QE sync (with each product team's QE liaison) | 30 min, weekly per product line | Asha Reddy + liaison | Attend the lines you cover |
| Release-gate review (release week) | 30 min, weekly during release weeks | Release manager + QE on-call | Attend when your product is releasing |
| All-hands | 60 min, monthly | Sridhar Venkatesh | Attend |

## 14. Escalation Contacts

Use the following contacts in priority order. See [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for the full directory.

| Need | Contact | How |
|------|---------|-----|
| Technical question, repo, build | Buddy: Sandeep Kulkarni (sandeep.kulkarni@acme.example) | Teams DM or `#quality-engineering` |
| Cross-team test question | Product team's QE liaison (via `#qe-help`) | Teams channel |
| People/career/scope | Manager: Asha Reddy (asha.reddy@acme.example) | 1:1 or Teams DM |
| HR / leave / payroll / policy | HRBP: Deepika Rao (deepika.rao@acme.example) — covers QE | `hr.acme.example`, then Teams DM |
| IT (laptop, VPN, M365, software) | IT Helpdesk | `helpdesk.acme.example` or `#it-helpdesk` |
| Test environment outage (staging) | Platform Infrastructure on-call | `#platform-oncall` + PagerDuty `platform-oncall` |
| Release-gate failure (production release blocked) | On-call QE + DevOps release manager + product team on-call | PagerDuty rotation `qe-oncall` |
| Security incident or suspected breach | SOC + CISO Rajan Mehta | `soc@acme.example` + 24/7 hotline in [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md) |
| Cross-team dependency (Cloud, Intelligence, Workspace, Platform) | Receiving EM via Asha | Asha routes |

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
