---
document_id: ACME-TEAM-001
title: ACME Corp Frontend Engineer Onboarding
category: team-onboarding
department: cloud-frontend
applicable_roles: [frontend-engineer]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [team-onboarding, frontend-engineer]
---

# ACME Corp Frontend Engineer Onboarding

Welcome to the **Cloud Frontend** team at ACME Corp. This guide is your single reference for the first 90 days as a Frontend Engineer building the ACME Cloud Console. It assumes you have already completed the company-wide onboarding in [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) and [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md). If you have not, please stop and complete those first — your manager and buddy will check.

> ACME Corp is a fictional company. All names, repositories, hosts, and systems referenced here are illustrative and use the `.example` domain. Do not attempt to reach any URL.

## 1. Team Overview

| Field | Value |
|-------|-------|
| Team name | Cloud Frontend |
| Reports up to | Sridhar Venkatesh (VP Engineering / CTO) via EM Manoj Pillai |
| Primary office | Bengaluru (with hybrid remote across Hyderabad, London, Seattle) |
| Primary product | ACME Cloud Console — see [`06-product/acme-cloud-overview.md`](../06-product/acme-cloud-overview.md) |
| Primary repository | `acme-cloud-frontend` — see [`04-engineering/repositories/acme-cloud-frontend.md`](../04-engineering/repositories/acme-cloud-frontend.md) |
| Primary channel | `#cloud-frontend` (Microsoft Teams) |

**Mission.** Build the web console that customers use to provision, monitor, and govern cloud resources across multiple clouds. The console is the front door to ACME Cloud; every other ACME product surfaces data that originates here.

**Charter.** Owns the customer-facing web experience for ACME Cloud — including tenant onboarding flows, resource provisioning UIs, cost dashboards, IAM console, and the design system. Does **not** own backend APIs (Cloud API team), mobile apps, or the ACME Workspace product.

**Customers.** Cloud architects, DevOps engineers, FinOps teams, and IT administrators at enterprise customers. Secondary internal customers: ACME Support and ACME Sales (who use the console for tenant demos).

## 2. Reporting Manager

- **Engineering Manager:** Manoj Pillai (manoj.pillai@acme.example, Bengaluru office, hybrid).
- Manoj reports to Sridhar Venkatesh (VP Engineering / CTO).
- Your standing 1:1 is 30 minutes weekly — Manoj's assistant will schedule it after your first week.
- Direct report line is recorded in the HR Hub at `hr.acme.example` and visible to you in your profile under `hr.acme.example/me`.

## 3. Onboarding Buddy

- **Buddy:** Rahul Menon (rahul.menon@acme.example), Tech Lead, Cloud Frontend.
- Rahul is your go-to peer for the first 90 days for questions that do not need your manager — IDE setup, repo layout, build commands, PR etiquette, who-to-ask for what.
- Buddy commitment: Rahul will block 2 hours per day on your calendar for the first 2 weeks, then 1 hour per day for weeks 3–6, then ad-hoc.
- See [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) for the buddy program's full expectations.

## 4. Required Documents (Week 1)

Read each of the following in your first week. Your buddy will check on progress during your week-1 1:1.

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
- [`04-engineering/repositories/acme-cloud-frontend.md`](../04-engineering/repositories/acme-cloud-frontend.md)
- [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md)
- [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md)
- [`04-engineering/practices/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md)
- [`06-product/acme-cloud-overview.md`](../06-product/acme-cloud-overview.md)

## 5. Required Software

Install only the approved tools below. Anything else requires a software access request via [`08-forms/software-access-request.md`](../08-forms/software-access-request.md). See [`02-it/approved-software-installation.md`](../02-it/approved-software-installation.md) for the binding policy.

**Workstation baseline (installed by IT before Day 1):**
- Windows 11 Enterprise or macOS 14+ (per [`02-it/laptop-and-workstation-allocation.md`](../02-it/laptop-and-workstation-allocation.md))
- Microsoft 365 — Outlook, Teams, OneDrive (per [`02-it/microsoft-365-account-activation.md`](../02-it/microsoft-365-account-activation.md))
- Microsoft Authenticator (per [`02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md))
- Corporate VPN client (per [`02-it/corporate-vpn-configuration.md`](../02-it/corporate-vpn-configuration.md))
- 1Password (per [`02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md))
- Microsoft Defender for Endpoint

**Developer tools (you install via the approved package manager / IT self-service):**
- Visual Studio Code (latest stable)
- Node.js 20 LTS (via nvm-windows or nvm) — matches `acme-cloud-frontend` build toolchain
- pnpm 9 (the repo enforces pnpm; do not use npm or yarn)
- Git 2.40+ and the GitHub CLI (`gh`) configured for `git.acme.example`
- Docker Desktop (for local design-system storybook + a11y regression container)
- Playwright browsers (installed via `pnpm dlx playwright install`)

**Browsers (testing matrix):** Chrome (stable), Microsoft Edge (stable), Firefox ESR.

## 6. Approved AI Tools

Per the role eligibility matrix in [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md), Frontend Engineers are **default-entitled** to:

| Tool | Entitlement | Notes |
|------|-------------|-------|
| GitHub Copilot Business | **Yes (default)** | Sign in only with your `@acme.example` Entra SSO. Never use a personal GitHub account. |
| Internal ACME Intelligence sandbox | Optional | Not granted by default; request via [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md) if a specific work item requires it. |

Copilot is opted-in at the repository level via a `copilot-instructions.md` file in `acme-cloud-frontend`. Before prompting Copilot, read [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) — the policy forbids entering customer data, secrets, or source code from other companies into any AI tool.

If your seat is not visible in VS Code by Day 3, file [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md).

## 7. Required Repositories

You will be granted read/write access to the following:

- `acme-cloud-frontend` — your home repository. See [`04-engineering/repositories/acme-cloud-frontend.md`](../04-engineering/repositories/acme-cloud-frontend.md).

Read-only cross-repo access (auto-granted for context):

- `acme-shared-libraries` — design tokens, shared React hooks, error reporting client. Read-only for frontend engineers.
- `acme-cloud-api` — read-only, to read the gRPC/REST contracts the frontend calls.

Repository access is requested via [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md). Your manager pre-approves your home repo; cross-team read access requires the receiving EM's approval and is processed within 2 business days.

You will **not** receive access to `acme-intelligence-*`, `acme-workspace-*`, or `acme-platform-infrastructure` unless a specific work item requires it. This is per [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).

## 8. Required Access Permissions

On Day 1, IT Onboarding (Geetha Iyer, `geetha.iyer@acme.example`) provisions the following Entra ID groups. Verify each in the My Apps portal at `myapps.acme.example`.

| Entra ID group | Purpose |
|----------------|---------|
| `ENG-Cloud-Frontend` | Repository write access to `acme-cloud-frontend`, CI runners, staging deployment visibility. |
| `ENG-Shared-Libraries-Read` | Read-only access to `acme-shared-libraries`. |
| `ENG-Cloud-API-Read` | Read-only access to `acme-cloud-api` for contract reading. |
| `Vault-Customer-CloudFrontend-Dev` | Personal HashiCorp Vault token scoped to `secret/cloud-frontend/dev/*`. |
| `Copilot-Business-Engineering` | GitHub Copilot Business seat assignment. |
| `Observability-Reader-NonProd` | Read-only access to Grafana non-production dashboards. |

Additional tools (provisioned automatically with the above groups):

- **Figma** — design files, via SSO. Request seat via [`08-forms/software-access-request.md`](../08-forms/software-access-request.md) if not auto-assigned.
- **Storybook** (internal, `storybook.internal.acme.example`) — read with Entra SSO.
- **Chromatic** (visual regression) — seat assigned by your buddy.

Production access is **not** granted at onboarding. Production deployment is restricted to release managers and on-call engineers per [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).

## 9. Training Requirements

Complete the following training in your first 30 days. All training is hosted in the ACME Learning portal and tracked in your learning transcript at `hr.acme.example/learning`.

| Course | Link | Deadline |
|--------|------|---------|
| Company Orientation | [`10-training/company-orientation.md`](../10-training/company-orientation.md) | Week 1 |
| Security Awareness | [`10-training/security-awareness.md`](../10-training/security-awareness.md) | Week 1 |
| Privacy Awareness | [`10-training/privacy-awareness.md`](../10-training/privacy-awareness.md) | Week 2 |
| Engineering Orientation | [`10-training/engineering-orientation.md`](../10-training/engineering-orientation.md) | Week 2 |
| Git and Repository Workflows | [`10-training/git-and-repository-workflows.md`](../10-training/git-and-repository-workflows.md) | Week 2 |
| AI Coding Assistant Usage | [`10-training/ai-coding-assistant-usage.md`](../10-training/ai-coding-assistant-usage.md) | Week 3 |
| ACME Cloud Product Training | [`10-training/product-training.md`](../10-training/product-training.md) | Week 4 |
| Workplace Conduct | [`10-training/workplace-conduct.md`](../10-training/workplace-conduct.md) | Week 4 |

Cloud-platform training is optional for this role but recommended before taking primary on-call. See [`10-training/cloud-platform-fundamentals.md`](../10-training/cloud-platform-fundamentals.md).

## 10. First-Week Activities

Day-by-day plan. Your buddy will walk through Day 1–2 with you.

- **Day 1:** IT activation (M365, Authenticator, laptop handover). Read [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md). Manager intro 1:1 with Manoj. Team lunch (in office) or virtual coffee (remote).
- **Day 2:** Clone `acme-cloud-frontend`. Run `pnpm install` and `pnpm dev`. Open the local Storybook. Read the repo's `README.md` and [`04-engineering/repositories/acme-cloud-frontend.md`](../04-engineering/repositories/acme-cloud-frontend.md).
- **Day 3:** Configure VS Code, sign into GitHub Copilot via Entra SSO. Complete [`10-training/security-awareness.md`](../10-training/security-awareness.md).
- **Day 4:** Pick a "good first issue" labeled `good-first-issue` from `git.acme.example/acme/acme-cloud-frontend/issues`. Create your first branch `feat/<issue-id>-<short-slug>` per [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md).
- **Day 5:** Open your first PR. Ask Rahul to review. Read [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md) before requesting review.

## 11. First-Month Deliverables

Concrete deliverables for the first 30 days:

1. **Merged PR #1** — a `good-first-issue` (typo, a11y fix, missing test, design-token alignment).
2. **Merged PR #2** — a small feature or refactor assigned by Rahul, typically 1–3 components, with Playwright tests added.
3. **Local environment fully working** — including Docker, Storybook, Playwright, VPN, and Figma access.
4. **Completed all Week 1–4 training** in section 9.
5. **First shadow on-call shift** — paired with the on-call engineer for one weekday evening. See [`04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md).
6. **Design-system contribution** — at least one token or component update reviewed by the UX team.

## 12. 30/60/90-Day Expectations

| Window | Expectation |
|--------|-------------|
| **30 days** | Local setup complete and reproducible. First small PR merged. Pair with buddy on at least 3 PRs. Shadow one on-call shift. Complete security, privacy, engineering, and AI-assistant training. |
| **60 days** | Ship a feature-sized change (a new console page, or a significant enhancement to an existing page) with Playwright coverage. Participate in code review as a reviewer (not just author) on at least 4 PRs. Complete an on-call shadow rotation (a full week, evening shifts, with a backup on call). Begin owning one component area in the design system. |
| **90 days** | Ship a medium-sized feature end-to-end (design → PR → staging → production release). Lead a small design doc (RFC) for a feature in your component area, reviewed by Manoj and Rahul. Take a primary on-call shift (with backup) for at least one weekday. Be the assigned reviewer on at least 8 PRs. |

## 13. Team Meetings

| Meeting | Cadence | Owner | Your role |
|---------|---------|-------|-----------|
| Daily standup | 15 min, 10:00 IST | Manoj Pillai | Attend, share blocker, request help |
| Sprint planning | 60 min, every other Monday | Manoj Pillai | Estimate, sign up for tickets |
| Sprint review & retrospective | 60 min, every other Friday | Manoj Pillai | Demo your work; raise retro items |
| 1:1 with manager | 30 min, weekly | Manoj Pillai | Career, blockers, feedback |
| 1:1 with buddy | 30 min, weekly for first 6 weeks | Rahul Menon | Questions, peer feedback |
| Frontend guild | 60 min, biweekly | Sara Lindberg (UX director) cross-team | Optional but encouraged |
| On-call handover | 15 min, daily during shift change | On-call engineer | Listen during shadow week |
| All-hands | 60 min, monthly | Sridhar Venkatesh | Attend |

## 14. Escalation Contacts

Use the following contacts in priority order. See [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for the full directory.

| Need | Contact | How |
|------|---------|-----|
| Technical question, repo, build | Buddy: Rahul Menon | Teams DM or `#cloud-frontend` |
| People/career/scope | Manager: Manoj Pillai (manoj.pillai@acme.example) | 1:1 or Teams DM |
| HR / leave / payroll / policy | HRBP: Kavya Krishnan (kavya.krishnan@acme.example) — covers Cloud Frontend | `hr.acme.example`, then Teams DM |
| IT (laptop, VPN, M365, software) | IT Helpdesk | `helpdesk.acme.example` or `#it-helpdesk` |
| Security incident or suspected breach | SOC + CISO Rajan Mehta | `soc@acme.example` + 24/7 hotline in [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md) |
| Production outage | On-call engineer + Manoj | PagerDuty rotation `cloud-frontend-oncall` |
| Cross-team dependency (Cloud API, Platform) | Receiving EM via Manoj | Manoj routes |

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
