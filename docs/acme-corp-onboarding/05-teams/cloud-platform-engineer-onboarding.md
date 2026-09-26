---
document_id: ACME-TEAM-006
title: ACME Corp Cloud Platform Engineer Onboarding
category: team-onboarding
department: platform-infrastructure
applicable_roles: [cloud-platform-engineer]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [team-onboarding, cloud-platform-engineer]
---

# ACME Corp Cloud Platform Engineer Onboarding

Welcome to the **Platform Infrastructure** team at ACME Corp. This guide is your single reference for the first 90 days as a Cloud Platform Engineer building the multi-cloud foundation that every other ACME product runs on. It assumes you have already completed [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) and [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md).

> ACME Corp is a fictional company. All names, repositories, hosts, and systems referenced here are illustrative and use the `.example` domain. Do not attempt to reach any URL.

## 1. Team Overview

| Field | Value |
|-------|-------|
| Team name | Platform Infrastructure |
| Reports up to | Sridhar Venkatesh (VP Engineering / CTO) via EM Nikhil Joshi |
| Primary office | Bengaluru (with hybrid remote across all ACME offices) |
| Primary product | Shared platform — used by ACME Cloud, ACME Intelligence, ACME Workspace |
| Primary repositories | `acme-platform-infrastructure` + `acme-shared-libraries` — see [`04-engineering/repositories/acme-platform-infrastructure.md`](../04-engineering/repositories/acme-platform-infrastructure.md) and [`04-engineering/repositories/acme-shared-libraries.md`](../04-engineering/repositories/acme-shared-libraries.md) |
| Primary channel | `#platform-infra` (Microsoft Teams) |

**Mission.** Build and operate the multi-cloud platform that every ACME product team builds on top of: Kubernetes clusters, infrastructure-as-code (Terraform + Crossplane), secrets management (Vault), observability backbone (OpenTelemetry collectors, Grafana), CI runners, internal package registry, and the developer platform portal at `portal.acme.example`.

**Charter.** Owns platform shared services consumed by all engineering teams. Does **not** own product-specific business logic (Cloud API, Workspace API, Intelligence Agents), product UIs (Cloud Frontend, Workspace Web), or model training pipelines (Intelligence ML).

**Customers.** Every engineering team at ACME (Cloud API, Cloud Frontend, Intelligence Agents/Inference/ML, Workspace Web/API, Quality Engineering). The Platform team is the foundational "team-of-teams" — your uptime and ergonomics directly affect every other team's velocity.

## 2. Reporting Manager

- **Engineering Manager:** Nikhil Joshi (nikhil.joshi@acme.example, Bengaluru office, hybrid).
- Nikhil reports to Sridhar Venkatesh (VP Engineering / CTO).
- Your standing 1:1 is 30 minutes weekly.
- Reporting line is recorded at `hr.acme.example` under your profile.

## 3. Onboarding Buddy

- **Buddy:** Pooja Bhatt (pooja.bhatt@acme.example), Tech Lead, Platform Infrastructure.
- Pooja is your peer mentor for the first 90 days — Terraform layout, Crossplane compositions, cluster access, Vault setup, observability stack, CI runner management.
- Buddy commitment: 2 hours per day for the first 2 weeks; 1 hour per day for weeks 3–6; ad-hoc thereafter.
- See [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) for the buddy program's expectations.

## 4. Required Documents (Week 1)

Read each of the following in your first week. Pooja will check progress during your week-1 1:1.

- [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md)
- [`00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- [`00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- [`00-company/communication-guidelines.md`](../00-company/communication-guidelines.md)
- [`03-security/information-security-policy.md`](../03-security/information-security-policy.md)
- [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md)
- [`03-security/identity-and-access-management.md`](../03-security/identity-and-access-management.md)
- [`03-security/secrets-management.md`](../03-security/secrets-management.md)
- [`04-engineering/developer-workstation-setup.md`](../04-engineering/developer-workstation-setup.md)
- [`04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md)
- [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md)
- [`04-engineering/repositories/acme-platform-infrastructure.md`](../04-engineering/repositories/acme-platform-infrastructure.md)
- [`04-engineering/repositories/acme-shared-libraries.md`](../04-engineering/repositories/acme-shared-libraries.md)
- [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md)
- [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md)
- [`04-engineering/practices/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md)
- [`04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md)
- [`10-training/cloud-platform-fundamentals.md`](../10-training/cloud-platform-fundamentals.md)

## 5. Required Software

Install only the approved tools below. Anything else requires a software access request via [`08-forms/software-access-request.md`](../08-forms/software-access-request.md). See [`02-it/approved-software-installation.md`](../02-it/approved-software-installation.md) for the binding policy.

**Workstation baseline (installed by IT before Day 1):**
- Windows 11 Enterprise or macOS 14+
- Microsoft 365, Microsoft Authenticator, Corporate VPN, 1Password, Microsoft Defender for Endpoint

**Developer tools (you install via the approved package manager):**
- Visual Studio Code (latest stable) with HashiCorp Terraform extension
- Terraform 1.7+ (matches the repo's `.terraform-version`)
- `terragrunt` (used to DRY-ify multi-environment Terraform)
- Crossplane CLI (`crossplane`), `kubectl`, `helm`, `kustomize`
- Go 1.22 (for Crossplane compositions and platform controller development)
- AWS CLI v2, Azure CLI, Google Cloud SDK (cross-cloud — ACME runs on all three)
- `vault` CLI for HashiCorp Vault at `vault.acme.example`
- Docker Desktop, `jq`, `yq`, `httpie`
- GitHub CLI (`gh`) configured for `git.acme.example`

**Cluster access (provisioned via Entra ID group):** You will get access to the platform-admin Kubernetes contexts across ACME's three clouds. This is the most privileged engineering access at ACME — review [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) carefully.

## 6. Approved AI Tools

Per the role eligibility matrix in [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md), Cloud Platform Engineers are **default-entitled** to:

| Tool | Entitlement | Notes |
|------|-------------|-------|
| GitHub Copilot Business | **Yes (default)** | Sign in only with `@acme.example` Entra SSO. Useful for Terraform boilerplate and Go scaffold. |
| Internal ACME Intelligence sandbox | Optional | Not granted by default. Request via [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md) if a specific work item (e.g., platform automation agent) requires it. |

`acme-platform-infrastructure` and `acme-shared-libraries` are opted in to Copilot via their `copilot-instructions.md` files. Read [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) before prompting — never enter customer data, secrets, cloud credentials, or Vault paths into Copilot Chat.

## 7. Required Repositories

You will be granted read/write access to the following:

- `acme-platform-infrastructure` — your primary repository (Terraform, Crossplane, Go controllers). See [`04-engineering/repositories/acme-platform-infrastructure.md`](../04-engineering/repositories/acme-platform-infrastructure.md).
- `acme-shared-libraries` — shared libraries across languages (Go, TypeScript, Python, Java). Platform Infrastructure is the acting owner of this repo. See [`04-engineering/repositories/acme-shared-libraries.md`](../04-engineering/repositories/acme-shared-libraries.md).

Repository access is requested via [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md). Nikhil pre-approves both repos for you.

You will **not** receive write access to product repos (`acme-cloud-*`, `acme-intelligence-*`, `acme-workspace-*`) — you only get read access for context, and even that is on-request. This is per [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).

## 8. Required Access Permissions

On Day 1, IT Onboarding (Geetha Iyer, `geetha.iyer@acme.example`) provisions the following Entra ID groups. Verify each in the My Apps portal at `myapps.acme.example`. **Pay particular attention to least-privilege boundaries.**

| Entra ID group | Purpose |
|----------------|---------|
| `ENG-Platform-Infrastructure` | Repository write access to `acme-platform-infrastructure` and `acme-shared-libraries`. |
| `Platform-Admin-AWS-NonProd` | AWS SSO role for non-production accounts (read-mostly; admin via break-glass). |
| `Platform-Admin-Azure-NonProd` | Azure role assignments for non-production subscriptions. |
| `Platform-Admin-GCP-NonProd` | GCP project roles for non-production projects. |
| `Platform-K8s-Admin-NonProd` | `cluster-admin` on non-production Kubernetes clusters across the three clouds. |
| `Vault-Platform-Admin-Dev` | Vault admin token scoped to `secret/platform/dev/*`. Production paths (`secret/platform/prod/*`) require break-glass. |
| `Copilot-Business-Engineering` | GitHub Copilot Business seat assignment. |
| `Observability-Admin-NonProd` | Admin on Grafana non-production (can edit dashboards, alert rules). |
| `CI-Runner-Admin-NonProd` | Admin on self-hosted GitHub Actions runners (`runners.internal.acme.example`) for non-production. |

Production cloud and cluster access is **not** granted at onboarding. Production platform changes require an approved change ticket, two-person review, and break-glass credentials — see [`04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md) and [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).

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
| Cloud Platform Fundamentals | [`10-training/cloud-platform-fundamentals.md`](../10-training/cloud-platform-fundamentals.md) | Week 2 (high priority) |
| Workplace Conduct | [`10-training/workplace-conduct.md`](../10-training/workplace-conduct.md) | Week 4 |

Additional role-specific training delivered by Pooja in weeks 2–4:
- "ACME multi-cloud topology" walkthrough (2 hours).
- "Terraform + Crossplane conventions" workshop (2 hours).
- "Vault and secret tiering" briefing (1 hour).
- "Production change management and break-glass" briefing by CISO designate (1 hour).

## 10. First-Week Activities

- **Day 1:** IT activation (M365, Authenticator, laptop). Read [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md). Manager intro 1:1 with Nikhil.
- **Day 2:** Clone both `acme-platform-infrastructure` and `acme-shared-libraries`. Run `terraform init` and `terraform plan` against the `dev` workspace. Read the per-repo docs ([`04-engineering/repositories/acme-platform-infrastructure.md`](../04-engineering/repositories/acme-platform-infrastructure.md), [`04-engineering/repositories/acme-shared-libraries.md`](../04-engineering/repositories/acme-shared-libraries.md)).
- **Day 3:** Configure VS Code, sign into GitHub Copilot via Entra SSO. Get your Vault token and verify access with `vault kv get secret/platform/dev/selftest`. Verify kubectl context to the dev cluster.
- **Day 4:** Pick a `good-first-issue` labeled ticket (e.g., a Terraform module upgrade, a Crossplane composition fix, an observability dashboard addition). Create your first branch per [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md).
- **Day 5:** Open your first PR. Request review from Pooja. Read [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md) before requesting review. **Note:** All platform PRs require two reviewers (one of which must be a Tech Lead or EM) per the platform team policy.

## 11. First-Month Deliverables

1. **Merged PR #1** — a `good-first-issue` (Terraform refactor, observability improvement, Crossplane fix).
2. **Merged PR #2** — a small platform change assigned by Pooja, with non-prod `terraform plan` and `kubectl apply --dry-run` validation in CI.
3. **Local + cloud environment fully working** — including Terraform, Crossplane, Vault, kubectl to dev clusters across the three clouds.
4. **Completed all Week 1–4 training** in section 9 plus the role-specific workshops.
5. **First shadow on-call shift** — paired with the on-call platform engineer for one weekday evening. Platform on-call covers cluster, Vault, CI runners, and observability incidents. See [`04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md).
6. **First non-prod Terraform apply you authored** — executed by your buddy with you shadowing; reviewed in the next sprint retro.

## 12. 30/60/90-Day Expectations

| Window | Expectation |
|--------|-------------|
| **30 days** | Local + cloud setup complete. First small PR merged. Pair with buddy on at least 3 PRs. Shadow one on-call shift. Complete security, privacy, engineering, and AI-assistant training plus role-specific workshops. |
| **60 days** | Ship a feature-sized change (a new Crossplane composition, a new Terraform module, or a significant observability improvement) with non-prod validation. Participate in code review as a reviewer on at least 4 PRs. Complete an on-call shadow rotation (one full week of evening shifts, with a backup on call). Begin owning one platform area (e.g., Vault, CI runners, AWS landing zone). |
| **90 days** | Ship a medium-sized change end-to-end (design → RFC → PR → non-prod apply → production change ticket → production apply with two-person review). Lead a small design doc (RFC) for a feature in your area, reviewed by Nikhil and Pooja. Take a primary on-call shift (with backup) for at least one weekday. Be the assigned reviewer on at least 8 PRs (one of the two required reviewers on platform PRs). |

## 13. Team Meetings

| Meeting | Cadence | Owner | Your role |
|---------|---------|-------|-----------|
| Daily standup | 15 min, 10:00 IST | Nikhil Joshi | Attend, share blocker |
| Sprint planning | 60 min, every other Monday | Nikhil Joshi | Estimate, sign up |
| Sprint review & retrospective | 60 min, every other Friday | Nikhil Joshi | Demo; raise retro items |
| 1:1 with manager | 30 min, weekly | Nikhil Joshi | Career, blockers, feedback |
| 1:1 with buddy | 30 min, weekly for first 6 weeks | Pooja Bhatt | Questions, peer feedback |
| Platform design review | 90 min, weekly | Pooja Bhatt | Present your RFCs |
| Change Advisory Board (production changes) | 30 min, weekly | Nikhil Joshi + CISO designate | Attend when your change is on the agenda |
| On-call handover | 15 min, daily during shift change | On-call engineer | Listen during shadow week |
| Platform user council (with consuming teams) | 60 min, monthly | Nikhil Joshi | Attend |
| All-hands | 60 min, monthly | Sridhar Venkatesh | Attend |

## 14. Escalation Contacts

Use the following contacts in priority order. See [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for the full directory.

| Need | Contact | How |
|------|---------|-----|
| Technical question, repo, build | Buddy: Pooja Bhatt (pooja.bhatt@acme.example) | Teams DM or `#platform-infra` |
| People/career/scope | Manager: Nikhil Joshi (nikhil.joshi@acme.example) | 1:1 or Teams DM |
| HR / leave / payroll / policy | HRBP: Sanjay Patel (sanjay.patel@acme.example) — covers Platform | `hr.acme.example`, then Teams DM |
| IT (laptop, VPN, M365, software) | IT Helpdesk | `helpdesk.acme.example` or `#it-helpdesk` |
| Production outage (cluster, Vault, CI runners) | On-call platform engineer + Nikhil | PagerDuty rotation `platform-oncall` |
| Production change emergency (break-glass) | On-call + Nikhil + CISO designate | See break-glass procedure in [`04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md) |
| Security incident or suspected breach | SOC + CISO Rajan Mehta | `soc@acme.example` + 24/7 hotline in [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md) |
| Cloud provider incident (AWS/Azure/GCP) | Provider status page + On-call | `status.acme.example` aggregates provider status |
| Cross-team dependency (Cloud, Intelligence, Workspace, QE) | Receiving EM via Nikhil | Nikhil routes |

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
