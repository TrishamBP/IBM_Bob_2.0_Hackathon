---
document_id: ACME-TEAM-002
title: ACME Corp Backend Engineer Onboarding
category: team-onboarding
department: cloud-api
applicable_roles: [backend-engineer]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [team-onboarding, backend-engineer]
---

# ACME Corp Backend Engineer Onboarding

Welcome to the **Cloud API** team at ACME Corp. This guide is your single reference for the first 90 days as a Backend Engineer building the core API service for ACME Cloud. It assumes you have already completed [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) and [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md).

> ACME Corp is a fictional company. All names, repositories, hosts, and systems referenced here are illustrative and use the `.example` domain. Do not attempt to reach any URL.

## 1. Team Overview

| Field | Value |
|-------|-------|
| Team name | Cloud API |
| Reports up to | Sridhar Venkatesh (VP Engineering / CTO) via EM Anjali Desai |
| Primary office | Hyderabad (with hybrid remote across Bengaluru, London, Seattle) |
| Primary product | ACME Cloud — see [`06-product/acme-cloud-overview.md`](../06-product/acme-cloud-overview.md) |
| Primary repository | `acme-cloud-api` — see [`04-engineering/repositories/acme-cloud-api.md`](../04-engineering/repositories/acme-cloud-api.md) |
| Primary channel | `#cloud-api` (Microsoft Teams) |

**Mission.** Build and operate the public gRPC and REST API surface that customers and internal products use to provision cloud resources, manage tenants, and stream telemetry. The API is the system of record for tenant metadata, billing events, and quota state.

**Charter.** Owns tenant onboarding, identity federation, resource provisioning abstractions, quota enforcement, and metering event publication to Kafka. Does **not** own the console UI (Cloud Frontend), the inference engine (Intelligence Inference), or shared platform libraries (Platform Infrastructure).

**Customers.** Cloud architects and DevOps engineers at enterprise customers (direct API users); Cloud Frontend team (internal consumer); ACME Intelligence (consumes metering events and quota state); ACME Support (uses admin APIs).

## 2. Reporting Manager

- **Engineering Manager:** Anjali Desai (anjali.desai@acme.example, Hyderabad office, hybrid).
- Anjali reports to Sridhar Venkatesh (VP Engineering / CTO).
- Your standing 1:1 is 30 minutes weekly, scheduled by Anjali's assistant after your first week.
- Reporting line is recorded at `hr.acme.example` under your profile.

## 3. Onboarding Buddy

- **Buddy:** Aditi Ghosh (aditi.ghosh@acme.example), Tech Lead, Cloud API.
- Aditi will be your peer mentor for the first 90 days — IDE setup, repo layout, build commands, protobuf conventions, PR etiquette.
- Buddy commitment: 2 hours per day for the first 2 weeks; 1 hour per day for weeks 3–6; ad-hoc thereafter.
- See [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) for the buddy program's expectations.

## 4. Required Documents (Week 1)

Read each of the following in your first week. Aditi will check progress during your week-1 1:1.

- [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md)
- [`00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- [`00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- [`00-company/communication-guidelines.md`](../00-company/communication-guidelines.md)
- [`03-security/information-security-policy.md`](../03-security/information-security-policy.md)
- [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md)
- [`03-security/secrets-management.md`](../03-security/secrets-management.md)
- [`03-security/customer-data-handling.md`](../03-security/customer-data-handling.md)
- [`04-engineering/developer-workstation-setup.md`](../04-engineering/developer-workstation-setup.md)
- [`04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md)
- [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md)
- [`04-engineering/repositories/acme-cloud-api.md`](../04-engineering/repositories/acme-cloud-api.md)
- [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md)
- [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md)
- [`04-engineering/practices/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md)
- [`04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md)
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

**Developer tools (you install via the approved package manager):**
- Visual Studio Code (latest stable) or GoLand (license via IT self-service)
- Go 1.22 (matches the repo's `go.mod`)
- `protoc` 25+ and `protoc-gen-go`, `protoc-gen-go-grpc`, `protoc-gen-grpc-gateway`
- `buf` CLI (the repo enforces buf for protobuf linting and breaking-change detection)
- Docker Desktop (for local Postgres + Kafka stack)
- `psql` client, `kcat`/`kafka-console-consumer` for Kafka debugging
- GitHub CLI (`gh`) configured for `git.acme.example`

## 6. Approved AI Tools

Per the role eligibility matrix in [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md), Backend Engineers are **default-entitled** to:

| Tool | Entitlement | Notes |
|------|-------------|-------|
| GitHub Copilot Business | **Yes (default)** | Sign in only with `@acme.example` Entra SSO. Never use a personal GitHub account. |
| Internal ACME Intelligence sandbox | Optional | Not granted by default. Request via [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md) only if a work item requires it. |

`acme-cloud-api` is opted in to Copilot via its `copilot-instructions.md` file. Read [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) before prompting — never enter customer data, secrets, or third-party source into Copilot Chat.

## 7. Required Repositories

You will be granted read/write access to the following:

- `acme-cloud-api` — your home repository. See [`04-engineering/repositories/acme-cloud-api.md`](../04-engineering/repositories/acme-cloud-api.md).

Read-only cross-repo access (auto-granted for context):

- `acme-shared-libraries` — shared Go libraries (error reporting, tracing, auth middleware).
- `acme-cloud-frontend` — read-only, to understand the consumer of the API you build.

Repository access is requested via [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md). Your manager pre-approves your home repo; cross-team read access requires the receiving EM's approval.

You will **not** receive access to `acme-intelligence-*`, `acme-workspace-*`, `acme-platform-infrastructure`, or `acme-quality-automation` (beyond read) unless a specific work item requires it. This is per [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).

## 8. Required Access Permissions

On Day 1, IT Onboarding (Geetha Iyer, `geetha.iyer@acme.example`) provisions the following Entra ID groups. Verify each in the My Apps portal at `myapps.acme.example`.

| Entra ID group | Purpose |
|----------------|---------|
| `ENG-Cloud-API` | Repository write access to `acme-cloud-api`, CI runners, staging deployment visibility. |
| `ENG-Shared-Libraries-Read` | Read-only access to `acme-shared-libraries`. |
| `ENG-Cloud-Frontend-Read` | Read-only access to `acme-cloud-frontend` for API consumer context. |
| `Vault-Customer-CloudAPI-Dev` | Personal HashiCorp Vault token scoped to `secret/cloud-api/dev/*`. |
| `Copilot-Business-Engineering` | GitHub Copilot Business seat assignment. |
| `Observability-Reader-NonProd` | Read-only Grafana non-production dashboards. |
| `Kafka-Consumer-CloudAPI-Dev` | Dev-cluster Kafka consumer group membership. |

Additional tools (auto-provisioned):

- **PagerDuty** — added to the `cloud-api-oncall` rotation as a shadow for the first 6 weeks.
- **Datadog / OpenTelemetry collector** viewer for the `cloud-api` service.

Production access is **not** granted at onboarding. Production deployment is restricted to release managers and on-call engineers per [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md). Time-boxed production Vault access for incident response is granted via break-glass — see [`04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md).

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
| ACME Cloud Product Training | [`10-training/product-training.md`](../10-training/product-training.md) | Week 3 |
| Cloud Platform Fundamentals | [`10-training/cloud-platform-fundamentals.md`](../10-training/cloud-platform-fundamentals.md) | Week 4 |
| Workplace Conduct | [`10-training/workplace-conduct.md`](../10-training/workplace-conduct.md) | Week 4 |

## 10. First-Week Activities

- **Day 1:** IT activation (M365, Authenticator, laptop handover). Read [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md). Manager intro 1:1 with Anjali.
- **Day 2:** Clone `acme-cloud-api`. Run `make local-up` to bring up Postgres + Kafka via Docker. Run `make test` to verify the suite passes. Read the repo's `README.md` and [`04-engineering/repositories/acme-cloud-api.md`](../04-engineering/repositories/acme-cloud-api.md).
- **Day 3:** Configure VS Code / GoLand. Sign into GitHub Copilot via Entra SSO. Read [`03-security/secrets-management.md`](../03-security/secrets-management.md) and request your dev Vault token.
- **Day 4:** Pick a `good-first-issue` labeled ticket from `git.acme.example/acme/acme-cloud-api/issues`. Create your first branch per [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md).
- **Day 5:** Open your first PR. Request review from Aditi. Read [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md) before requesting review.

## 11. First-Month Deliverables

1. **Merged PR #1** — a `good-first-issue` (small bug, missing test, refactoring).
2. **Merged PR #2** — a small feature or refactor assigned by Aditi, typically a single gRPC method or REST endpoint with unit + integration tests.
3. **Local environment fully working** — including Docker, Postgres, Kafka, Vault dev token, VPN.
4. **Completed all Week 1–4 training** in section 9.
5. **First shadow on-call shift** — paired with the on-call engineer for one weekday evening, following [`04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md).
6. **First protobuf change reviewed** — at least one PR that adds or modifies a `.proto` file, with `buf breaking` passing.

## 12. 30/60/90-Day Expectations

| Window | Expectation |
|--------|-------------|
| **30 days** | Local setup complete and reproducible. First small PR merged. Pair with buddy on at least 3 PRs. Shadow one on-call shift. Complete security, privacy, engineering, and AI-assistant training. |
| **60 days** | Ship a feature-sized change (a new gRPC method + REST projection + Kafka metering event + tests) end-to-end. Participate in code review as a reviewer on at least 4 PRs. Complete an on-call shadow rotation (one full week of evening shifts, with a backup on call). Begin owning one service area (e.g., quota, metering, tenant onboarding). |
| **90 days** | Ship a medium-sized feature end-to-end (design → PR → staging → production release). Lead a small design doc (RFC) for a feature in your service area, reviewed by Anjali and Aditi. Take a primary on-call shift (with backup) for at least one weekday. Be the assigned reviewer on at least 8 PRs. |

## 13. Team Meetings

| Meeting | Cadence | Owner | Your role |
|---------|---------|-------|-----------|
| Daily standup | 15 min, 10:00 IST | Anjali Desai | Attend, share blocker |
| Sprint planning | 60 min, every other Monday | Anjali Desai | Estimate, sign up for tickets |
| Sprint review & retrospective | 60 min, every other Friday | Anjali Desai | Demo; raise retro items |
| 1:1 with manager | 30 min, weekly | Anjali Desai | Career, blockers, feedback |
| 1:1 with buddy | 30 min, weekly for first 6 weeks | Aditi Ghosh | Questions, peer feedback |
| API design review | 60 min, weekly | Aditi Ghosh | Attend, present your RFCs |
| On-call handover | 15 min, daily during shift change | On-call engineer | Listen during shadow week |
| All-hands | 60 min, monthly | Sridhar Venkatesh | Attend |

## 14. Escalation Contacts

Use the following contacts in priority order. See [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for the full directory.

| Need | Contact | How |
|------|---------|-----|
| Technical question, repo, build | Buddy: Aditi Ghosh | Teams DM or `#cloud-api` |
| People/career/scope | Manager: Anjali Desai (anjali.desai@acme.example) | 1:1 or Teams DM |
| HR / leave / payroll / policy | HRBP: Kavya Krishnan (kavya.krishnan@acme.example) — covers Cloud API | `hr.acme.example`, then Teams DM |
| IT (laptop, VPN, M365, software) | IT Helpdesk | `helpdesk.acme.example` or `#it-helpdesk` |
| Security incident or suspected breach | SOC + CISO Rajan Mehta | `soc@acme.example` + 24/7 hotline in [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md) |
| Production outage | On-call engineer + Anjali | PagerDuty rotation `cloud-api-oncall` |
| Cross-team dependency (Cloud Frontend, Platform, Intelligence) | Receiving EM via Anjali | Anjali routes |
| Vault / secret issue | Platform Infrastructure on-call + Anjali | `#platform-oncall` |

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
