---
document_id: ACME-TEAM-007
title: ACME Corp DevOps Engineer Onboarding
category: team-onboarding
department: platform-infrastructure
applicable_roles: [devops-engineer]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [team-onboarding, devops-engineer]
---

# ACME Corp DevOps Engineer Onboarding

Welcome to the **Platform Infrastructure** team at ACME Corp. This guide is your single reference for the first 90 days as a DevOps Engineer focused on CI/CD pipelines, deployment automation, release tooling, and developer experience. It assumes you have already completed [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) and [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md).

> ACME Corp is a fictional company. All names, repositories, hosts, and systems referenced here are illustrative and use the `.example` domain. Do not attempt to reach any URL.

## 1. Team Overview

| Field | Value |
|-------|-------|
| Team name | Platform Infrastructure (DevOps sub-track) |
| Reports up to | Sridhar Venkatesh (VP Engineering / CTO) via EM Nikhil Joshi |
| Primary office | Bengaluru (with hybrid remote across all ACME offices) |
| Primary product | Shared platform — used by ACME Cloud, ACME Intelligence, ACME Workspace |
| Primary repository | `acme-platform-infrastructure` — see [`04-engineering/repositories/acme-platform-infrastructure.md`](../04-engineering/repositories/acme-platform-infrastructure.md) |
| Primary channel | `#platform-infra` (Microsoft Teams), `#devops-help` (cross-team) |

**Mission.** Build and operate the CI/CD pipelines, deployment automation, release tooling, internal package registry (`packages.acme.example`), self-hosted GitHub Actions runners, and developer experience tooling (the developer portal at `portal.acme.example`) that every product engineering team relies on.

**Charter.** Owns the CI/CD reference pipelines, deployment automation, release management tooling, internal package publishing, runner fleet management, and the developer experience portal. Does **not** own cloud landing-zone infrastructure (that's the Cloud Platform Engineer sub-track within the same team), or product-specific application code.

**Customers.** Every engineering team at ACME. The DevOps sub-track is the most cross-cutting role at ACME — when CI is slow or a release tool is broken, every product team is blocked simultaneously.

## 2. Reporting Manager

- **Engineering Manager:** Nikhil Joshi (nikhil.joshi@acme.example, Bengaluru office, hybrid).
- Nikhil reports to Sridhar Venkatesh (VP Engineering / CTO).
- Your standing 1:1 is 30 minutes weekly.
- Reporting line is recorded at `hr.acme.example` under your profile.

## 3. Onboarding Buddy

- **Buddy:** Pooja Bhatt (pooja.bhatt@acme.example), Tech Lead, Platform Infrastructure.
- Pooja is your peer mentor for the first 90 days — CI/CD pipeline patterns, release tooling, runner fleet, package registry, developer portal.
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
- [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md)
- [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md)
- [`04-engineering/practices/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md)
- [`04-engineering/practices/release-management.md`](../04-engineering/practices/release-management.md)
- [`04-engineering/practices/internal-package-management.md`](../04-engineering/practices/internal-package-management.md)
- [`04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md)

## 5. Required Software

Install only the approved tools below. Anything else requires a software access request via [`08-forms/software-access-request.md`](../08-forms/software-access-request.md). See [`02-it/approved-software-installation.md`](../02-it/approved-software-installation.md) for the binding policy.

**Workstation baseline (installed by IT before Day 1):**
- Windows 11 Enterprise or macOS 14+
- Microsoft 365, Microsoft Authenticator, Corporate VPN, 1Password, Microsoft Defender for Endpoint

**Developer tools (you install via the approved package manager):**
- Visual Studio Code (latest stable)
- GitHub CLI (`gh`) configured for `git.acme.example`
- Docker Desktop (essential — you will build container images daily)
- `kubectl`, `helm`, `kustomize`
- `terraform` (read-only context for platform repo)
- Go 1.22 (some internal tooling is Go)
- Python 3.11 (some release scripts are Python)
- `jq`, `yq`, `httpie`, `curl`
- `cosign` (sigstore; required for image signing)

**Runner fleet management:** You will be granted access to the self-hosted GitHub Actions runner fleet at `runners.internal.acme.example` (via Entra ID group — see section 8).

## 6. Approved AI Tools

Per the role eligibility matrix in [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md), DevOps Engineers are **default-entitled** to:

| Tool | Entitlement | Notes |
|------|-------------|-------|
| GitHub Copilot Business | **Yes (default)** | Sign in only with `@acme.example` Entra SSO. Useful for YAML pipelines, Dockerfiles, Helm charts. |
| Internal ACME Intelligence sandbox | Optional | Not granted by default. Request via [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md) if a specific work item requires it. |

`acme-platform-infrastructure` is opted in to Copilot via its `copilot-instructions.md` file. Read [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) before prompting — never enter secrets, runner tokens, signing keys, or customer data into Copilot Chat.

## 7. Required Repositories

You will be granted read/write access to the following:

- `acme-platform-infrastructure` — your home repository, specifically the `ci-cd/`, `release-tooling/`, `runners/`, and `package-registry/` subdirectories. See [`04-engineering/repositories/acme-platform-infrastructure.md`](../04-engineering/repositories/acme-platform-infrastructure.md).

Read-only cross-repo access (auto-granted for context — you need to see how product teams use the pipelines you build):

- `acme-shared-libraries` — shared libraries and CI reusable workflows.
- All production repos (`acme-cloud-api`, `acme-cloud-frontend`, `acme-intelligence-agents`, `acme-intelligence-inference`, `acme-intelligence-ml`, `acme-workspace-web`, `acme-workspace-api`, `acme-quality-automation`) — **read-only** so you can debug pipeline failures and propose improvements.

Repository access is requested via [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md). Nikhil pre-approves your home repo. Read access to product repos is bulk-approved by the receiving EMs as part of the standard DevOps onboarding bundle.

You will **not** receive write access to product repos — that would violate [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).

## 8. Required Access Permissions

On Day 1, IT Onboarding (Geetha Iyer, `geetha.iyer@acme.example) provisions the following Entra ID groups. Verify each in the My Apps portal at `myapps.acme.example`.

| Entra ID group | Purpose |
|----------------|---------|
| `ENG-Platform-Infrastructure` | Repository write access to `acme-platform-infrastructure`. |
| `ENG-All-Read` | Read-only access to all production repos (for pipeline debugging). |
| `ENG-Shared-Libraries-Read` | Read-only access to `acme-shared-libraries`. |
| `CI-Runner-Admin-NonProd` | Admin on self-hosted GitHub Actions runners for non-production. |
| `CI-Runner-Deploy-Production` | Limited production runner fleet admin (apply changes only — not credential rotation). |
| `Package-Registry-Admin-NonProd` | Admin on `packages.internal.acme.example` non-production. |
| `Container-Registry-Pusher-CI` | Push access to `registry.internal.acme.example/acme/*` for the CI service account (used for signed images only). |
| `Vault-Platform-DevOps-Dev` | Vault token scoped to `secret/platform/devops/dev/*` (CI runner tokens, signing key references). |
| `Copilot-Business-Engineering` | GitHub Copilot Business seat assignment. |
| `Observability-Reader-NonProd` | Read-only Grafana non-production dashboards. |
| `Portal-Editor-NonProd` | Editor access to the developer portal at `portal.acme.example` for non-prod. |

Production container-registry push (production-signed images), production package-registry admin, and production runner fleet credential rotation are **not** granted at onboarding — those require break-glass and two-person review per [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).

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
- "ACME CI/CD reference pipeline" walkthrough (2 hours).
- "Image signing with cosign" workshop (1 hour).
- "Release tooling and the release-manager role" workshop (2 hours).
- "Production change management and break-glass" briefing by CISO designate (1 hour, shared with Cloud Platform Engineer track).

## 10. First-Week Activities

- **Day 1:** IT activation (M365, Authenticator, laptop). Read [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md). Manager intro 1:1 with Nikhil.
- **Day 2:** Clone `acme-platform-infrastructure`. Read the `ci-cd/README.md` and `release-tooling/README.md`. Trigger a smoke pipeline run in the `dev` environment.
- **Day 3:** Configure VS Code, sign into GitHub Copilot via Entra SSO. Get your Vault token, verify runner fleet access, verify package-registry access by `helm pull` against an internal chart.
- **Day 4:** Pick a `good-first-issue` labeled ticket (e.g., a reusable workflow improvement, a Dockerfile optimization, a release script bug). Create your first branch per [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md).
- **Day 5:** Open your first PR. Request review from Pooja. Read [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md) before requesting review. All platform PRs require two reviewers.

## 11. First-Month Deliverables

1. **Merged PR #1** — a `good-first-issue` (reusable workflow improvement, Dockerfile fix, release script bug).
2. **Merged PR #2** — a small pipeline or release-tooling change assigned by Pooja, with non-prod validation passing in CI.
3. **Local + fleet environment fully working** — including Docker, kubectl, GitHub CLI, runner fleet admin (non-prod), package-registry admin (non-prod), Vault token.
4. **Completed all Week 1–4 training** in section 9 plus the role-specific workshops.
5. **First shadow on-call shift** — paired with the on-call DevOps engineer for one weekday evening. DevOps on-call covers CI/CD, runner fleet, package registry, and release tooling incidents.
6. **One release you shadowed** — observed a release-manager running a production release end-to-end (release ticket approval → signed image build → registry push → deploy → post-release verification).

## 12. 30/60/90-Day Expectations

| Window | Expectation |
|--------|-------------|
| **30 days** | Local + fleet setup complete. First small PR merged. Pair with buddy on at least 3 PRs. Shadow one on-call shift. Complete security, privacy, engineering, and AI-assistant training plus role-specific workshops. |
| **60 days** | Ship a feature-sized change (a new reusable workflow, a release tooling improvement, or a runner fleet enhancement) with non-prod validation. Participate in code review as a reviewer on at least 4 PRs. Complete an on-call shadow rotation (one full week of evening shifts, with a backup on call). Begin owning one CI/CD pipeline family or one release tool. |
| **90 days** | Ship a medium-sized change end-to-end (design → RFC → PR → non-prod validation → production change ticket → production rollout with two-person review). Lead a small design doc (RFC) for a feature in your area, reviewed by Nikhil and Pooja. Take a primary on-call shift (with backup) for at least one weekday. Be the assigned reviewer on at least 8 PRs. Be eligible to take release-manager shifts for non-critical releases (with a backup release manager). |

## 13. Team Meetings

| Meeting | Cadence | Owner | Your role |
|---------|---------|-------|-----------|
| Daily standup | 15 min, 10:00 IST | Nikhil Joshi | Attend, share blocker |
| Sprint planning | 60 min, every other Monday | Nikhil Joshi | Estimate, sign up |
| Sprint review & retrospective | 60 min, every other Friday | Nikhil Joshi | Demo; raise retro items |
| 1:1 with manager | 30 min, weekly | Nikhil Joshi | Career, blockers, feedback |
| 1:1 with buddy | 30 min, weekly for first 6 weeks | Pooja Bhatt | Questions, peer feedback |
| Platform design review | 90 min, weekly | Pooja Bhatt | Present your RFCs |
| CI/CD office hours (open to all engineers) | 60 min, weekly | DevOps sub-track | Attend; co-host after 60 days |
| Change Advisory Board (production changes) | 30 min, weekly | Nikhil Joshi + CISO designate | Attend when your change is on the agenda |
| On-call handover | 15 min, daily during shift change | On-call engineer | Listen during shadow week |
| All-hands | 60 min, monthly | Sridhar Venkatesh | Attend |

## 14. Escalation Contacts

Use the following contacts in priority order. See [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for the full directory.

| Need | Contact | How |
|------|---------|-----|
| Technical question, repo, build | Buddy: Pooja Bhatt (pooja.bhatt@acme.example) | Teams DM or `#platform-infra` |
| CI/CD question (cross-team) | DevOps sub-track on-call or `#devops-help` | Teams channel |
| People/career/scope | Manager: Nikhil Joshi (nikhil.joshi@acme.example) | 1:1 or Teams DM |
| HR / leave / payroll / policy | HRBP: Sanjay Patel (sanjay.patel@acme.example) — covers Platform | `hr.acme.example`, then Teams DM |
| IT (laptop, VPN, M365, software) | IT Helpdesk | `helpdesk.acme.example` or `#it-helpdesk` |
| Production outage (CI/CD, runner fleet, package registry, release tooling) | On-call DevOps engineer + Nikhil | PagerDuty rotation `platform-oncall` (DevOps sub-rotation) |
| Production change emergency (break-glass) | On-call + Nikhil + CISO designate | See break-glass procedure in [`04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md) |
| Security incident or suspected breach | SOC + CISO Rajan Mehta | `soc@acme.example` + 24/7 hotline in [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md) |
| Cross-team dependency (any product team) | Receiving EM via Nikhil | Nikhil routes |
| Status / outage comms | Engineering leadership + IT comms | `status.acme.example` |

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
