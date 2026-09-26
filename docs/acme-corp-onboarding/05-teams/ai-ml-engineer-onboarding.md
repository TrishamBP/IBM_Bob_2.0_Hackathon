---
document_id: ACME-TEAM-004
title: ACME Corp AI/ML Engineer Onboarding
category: team-onboarding
department: intelligence-agents
applicable_roles: [ai-ml-engineer]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [team-onboarding, ai-ml-engineer]
---

# ACME Corp AI/ML Engineer Onboarding

Welcome to the **Intelligence Agents** team at ACME Corp. This guide is your single reference for the first 90 days as an AI/ML Engineer building agent orchestration for ACME Intelligence. It assumes you have already completed [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) and [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md).

> ACME Corp is a fictional company. All names, repositories, hosts, and systems referenced here are illustrative and use the `.example` domain. Do not attempt to reach any URL.

## 1. Team Overview

| Field | Value |
|-------|-------|
| Team name | Intelligence Agents |
| Reports up to | Anitha Rajan (Director AI/ML) via EM Rohan Bhat |
| Primary office | Bengaluru (with hybrid remote across Hyderabad, London, Seattle) |
| Primary product | ACME Intelligence — see [`06-product/acme-intelligence-overview.md`](../06-product/acme-intelligence-overview.md) |
| Primary repository | `acme-intelligence-agents` — see [`04-engineering/repositories/acme-intelligence-agents.md`](../04-engineering/repositories/acme-intelligence-agents.md) |
| Primary channel | `#intelligence-agents` (Microsoft Teams) |

**Mission.** Build and operate the agent orchestration layer for ACME Intelligence — tool-using LLM agents, planner/executor loops, retrieval-augmented generation pipelines, and the API surface that other ACME products call to invoke agents.

**Charter.** Owns agent definition, tool calling, RAG retrieval, conversation memory, and the public agent invocation API. Does **not** own the underlying inference engine (Intelligence Inference), model training pipelines (Intelligence ML), or the customer-facing admin console (Workspace Web).

**Customers.** Enterprise customers using ACME Intelligence agents (direct API users); ACME Workspace (consumer of agents for in-document assistance); ACME Cloud (consumer of agents for cloud-cost optimization assistants); ACME Support (consumer of agents for ticket triage).

## 2. Reporting Manager

- **Engineering Manager:** Rohan Bhat (rohan.bhat@acme.example, Bengaluru office, hybrid).
- Rohan reports to Anitha Rajan (Director AI/ML).
- Your standing 1:1 is 30 minutes weekly.
- Reporting line is recorded at `hr.acme.example` under your profile.

## 3. Onboarding Buddy

- **Buddy:** Imran Khan (imran.khan@acme.example), Tech Lead, Intelligence Agents.
- Imran is your peer mentor for the first 90 days — Python tooling, repo layout, agent framework conventions, prompt engineering standards, eval harness usage.
- Buddy commitment: 2 hours per day for the first 2 weeks; 1 hour per day for weeks 3–6; ad-hoc thereafter.
- See [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) for the buddy program's expectations.

## 4. Required Documents (Week 1)

Read each of the following in your first week. Imran will check progress during your week-1 1:1.

- [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md)
- [`00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- [`00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- [`00-company/communication-guidelines.md`](../00-company/communication-guidelines.md)
- [`03-security/information-security-policy.md`](../03-security/information-security-policy.md)
- [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md)
- [`03-security/customer-data-handling.md`](../03-security/customer-data-handling.md)
- [`03-security/data-classification.md`](../03-security/data-classification.md)
- [`04-engineering/developer-workstation-setup.md`](../04-engineering/developer-workstation-setup.md)
- [`04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md)
- [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md)
- [`04-engineering/repositories/acme-intelligence-agents.md`](../04-engineering/repositories/acme-intelligence-agents.md)
- [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md)
- [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md)
- [`04-engineering/practices/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md)
- [`06-product/acme-intelligence-overview.md`](../06-product/acme-intelligence-overview.md)

## 5. Required Software

Install only the approved tools below. Anything else requires a software access request via [`08-forms/software-access-request.md`](../08-forms/software-access-request.md). See [`02-it/approved-software-installation.md`](../02-it/approved-software-installation.md) for the binding policy.

**Workstation baseline (installed by IT before Day 1):**
- Windows 11 Enterprise or macOS 14+ (per [`02-it/laptop-and-workstation-allocation.md`](../02-it/laptop-and-workstation-allocation.md))
- Microsoft 365, Microsoft Authenticator, Corporate VPN, 1Password, Microsoft Defender for Endpoint

**Developer tools (you install via the approved package manager):**
- Visual Studio Code (latest stable) or PyCharm Professional (license via IT self-service)
- Python 3.11 (matches the repo's `pyproject.toml`)
- `uv` 0.4+ for fast dependency resolution (the repo enforces uv; do not use plain pip)
- Docker Desktop (for local Ray cluster, Postgres, Redis)
- `psql` and `redis-cli` for local dev
- GitHub CLI (`gh`) configured for `git.acme.example`
- Optional: `jq`, `httpie` for API debugging

**GPU access (provisioned via Entra ID group):** Shared development GPU pool (`intel-gpu-dev-pool`) for local model prototyping via Ray. For training runs, use the ACME Intelligence sandbox — see section 6.

## 6. Approved AI Tools

Per the role eligibility matrix in [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md), AI/ML Engineers are **default-entitled** to **both** AI tools — the only role with both entitlements as defaults:

| Tool | Entitlement | Notes |
|------|-------------|-------|
| GitHub Copilot Business | **Yes (default)** | Sign in only with `@acme.example` Entra SSO. |
| Internal ACME Intelligence sandbox | **Yes (default)** | Access to the sandbox LLM endpoints at `intel-sandbox.internal.acme.example` for prompt iteration, eval runs, and model comparison. Use this **instead of** public LLM tools for any ACME-internal prompts. |

`acme-intelligence-agents` is opted in to Copilot via its `copilot-instructions.md`. Read [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) before prompting — you handle customer prompts as part of your job, so review the **customer-data-handling carve-outs** carefully. Customer data must never be sent to public LLM tools; the sandbox is approved for de-identified and consented data only.

## 7. Required Repositories

You will be granted read/write access to the following:

- `acme-intelligence-agents` — your home repository. See [`04-engineering/repositories/acme-intelligence-agents.md`](../04-engineering/repositories/acme-intelligence-agents.md).

Read-only cross-repo access (auto-granted for context):

- `acme-shared-libraries` — shared Python libraries (auth, tracing, eval harness client).
- `acme-intelligence-inference` — read-only, to understand the inference API surface your agents call.

Repository access is requested via [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md). Rohan pre-approves your home repo; cross-team read access requires the receiving EM's approval.

You will **not** receive access to `acme-intelligence-ml` (training pipelines — that's the AI Research Engineer's domain), `acme-cloud-*`, `acme-workspace-*`, or `acme-platform-infrastructure` unless a specific work item requires it. This is per [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).

## 8. Required Access Permissions

On Day 1, IT Onboarding (Geetha Iyer, `geetha.iyer@acme.example`) provisions the following Entra ID groups. Verify each in the My Apps portal at `myapps.acme.example`.

| Entra ID group | Purpose |
|----------------|---------|
| `ENG-Intelligence-Agents` | Repository write access to `acme-intelligence-agents`, CI runners. |
| `ENG-Shared-Libraries-Read` | Read-only access to `acme-shared-libraries`. |
| `ENG-Intelligence-Inference-Read` | Read-only access to `acme-intelligence-inference` for API context. |
| `Vault-Customer-Intel-Agents-Dev` | Personal HashiCorp Vault token scoped to `secret/intel-agents/dev/*` (includes sandbox API key). |
| `Copilot-Business-Engineering` | GitHub Copilot Business seat assignment. |
| `Intel-Sandbox-User` | Access to the internal ACME Intelligence sandbox at `intel-sandbox.internal.acme.example`. |
| `Intel-GPU-Dev-Pool` | Membership in the shared dev GPU pool for local prototyping. |
| `Observability-Reader-NonProd` | Read-only Grafana non-production dashboards. |
| `MLflow-Reader-NonProd` | Read-only access to MLflow tracking server for eval runs. |

Additional tools (auto-provisioned):

- **LangSmith / prompt eval tooling** (internal mirror) — seat assigned by Rohan.
- **Weights & Biases** — read access to the team's existing eval runs.

Production access is **not** granted at onboarding. Production model serving and deployment is restricted to the Intelligence Inference on-call rotation.

## 9. Training Requirements

Complete the following training in your first 30 days. All training is tracked in your learning transcript at `hr.acme.example/learning`.

| Course | Link | Deadline |
|--------|------|---------|
| Company Orientation | [`10-training/company-orientation.md`](../10-training/company-orientation.md) | Week 1 |
| Security Awareness | [`10-training/security-awareness.md`](../10-training/security-awareness.md) | Week 1 |
| Privacy Awareness | [`10-training/privacy-awareness.md`](../10-training/privacy-awareness.md) | Week 1 (high priority — you handle customer prompts) |
| Engineering Orientation | [`10-training/engineering-orientation.md`](../10-training/engineering-orientation.md) | Week 2 |
| Git and Repository Workflows | [`10-training/git-and-repository-workflows.md`](../10-training/git-and-repository-workflows.md) | Week 2 |
| AI Coding Assistant Usage | [`10-training/ai-coding-assistant-usage.md`](../10-training/ai-coding-assistant-usage.md) | Week 2 |
| ACME Intelligence Product Training | [`10-training/product-training.md`](../10-training/product-training.md) | Week 3 |
| Cloud Platform Fundamentals | [`10-training/cloud-platform-fundamentals.md`](../10-training/cloud-platform-fundamentals.md) | Week 4 |
| Workplace Conduct | [`10-training/workplace-conduct.md`](../10-training/workplace-conduct.md) | Week 4 |

Additional role-specific training delivered by Imran in weeks 2–4:
- Internal "Agent framework patterns" workshop (2 hours).
- "Eval harness and golden-set workflows" workshop (2 hours).
- "Customer data and the sandbox carve-out" briefing by CISO designate (1 hour).

## 10. First-Week Activities

- **Day 1:** IT activation (M365, Authenticator, laptop). Read [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md). Manager intro 1:1 with Rohan.
- **Day 2:** Clone `acme-intelligence-agents`. Run `uv sync` and `make local-up` to bring up Ray + Postgres + Redis. Run `make test` and `make eval-smoke` to verify the test and eval suites pass.
- **Day 3:** Configure VS Code / PyCharm. Sign into GitHub Copilot via Entra SSO. Get your sandbox API key from Vault and verify the sandbox endpoint at `intel-sandbox.internal.acme.example/health`.
- **Day 4:** Pick a `good-first-issue` labeled ticket (e.g., adding a tool, fixing a prompt, extending an eval case). Create your first branch per [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md).
- **Day 5:** Open your first PR. Request review from Imran. Read [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md) before requesting review.

## 11. First-Month Deliverables

1. **Merged PR #1** — a `good-first-issue` (small tool, prompt fix, eval case addition).
2. **Merged PR #2** — a small feature assigned by Imran, typically a new agent tool or a retrieval pipeline change, with eval cases in the same PR.
3. **Local environment fully working** — including Ray, Postgres, Redis, sandbox API key, GPU pool access.
4. **Completed all Week 1–4 training** in section 9 plus the role-specific workshops.
5. **First shadow on-call shift** — paired with the on-call engineer for one weekday evening, following [`04-engineering/practices/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md).
6. **First eval-run authored** — at least one prompt or agent change accompanied by a new eval case and a passing eval run logged in MLflow.

## 12. 30/60/90-Day Expectations

| Window | Expectation |
|--------|-------------|
| **30 days** | Local setup complete. First small PR merged (with eval cases). Pair with buddy on at least 3 PRs. Shadow one on-call shift. Complete security, privacy, engineering, and AI-assistant training. |
| **60 days** | Ship a feature-sized change (a new agent or a significant tool/RAG enhancement) with eval coverage showing a measurable improvement on a golden set. Participate in code review as a reviewer on at least 4 PRs. Complete an on-call shadow rotation (one full week of evening shifts, with a backup on call). Begin owning one agent or one tool category. |
| **90 days** | Ship a medium-sized feature end-to-end (agent design → eval → PR → staging → production release). Lead a small design doc (RFC) for a feature in your area, reviewed by Rohan and Imran. Take a primary on-call shift (with backup) for at least one weekday. Be the assigned reviewer on at least 8 PRs. |

## 13. Team Meetings

| Meeting | Cadence | Owner | Your role |
|---------|---------|-------|-----------|
| Daily standup | 15 min, 10:00 IST | Rohan Bhat | Attend, share blocker |
| Sprint planning | 60 min, every other Monday | Rohan Bhat | Estimate, sign up |
| Sprint review & retrospective | 60 min, every other Friday | Rohan Bhat | Demo; raise retro items |
| 1:1 with manager | 30 min, weekly | Rohan Bhat | Career, blockers, feedback |
| 1:1 with buddy | 30 min, weekly for first 6 weeks | Imran Khan | Questions, peer feedback |
| Agent design review | 60 min, weekly | Imran Khan | Present your RFCs |
| Intelligence cross-team sync (Agents + Inference + ML) | 30 min, weekly | Anitha Rajan | Attend |
| Eval review | 60 min, biweekly | Imran Khan | Present your eval runs |
| All-hands | 60 min, monthly | Sridhar Venkatesh | Attend |

## 14. Escalation Contacts

Use the following contacts in priority order. See [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for the full directory.

| Need | Contact | How |
|------|---------|-----|
| Technical question, repo, build | Buddy: Imran Khan (imran.khan@acme.example) | Teams DM or `#intelligence-agents` |
| People/career/scope | Manager: Rohan Bhat (rohan.bhat@acme.example) | 1:1 or Teams DM |
| HR / leave / payroll / policy | HRBP: Deepika Rao (deepika.rao@acme.example) — covers Intelligence | `hr.acme.example`, then Teams DM |
| IT (laptop, VPN, M365, software) | IT Helpdesk | `helpdesk.acme.example` or `#it-helpdesk` |
| Security incident or suspected breach (incl. sandbox misuse) | SOC + CISO Rajan Mehta | `soc@acme.example` + 24/7 hotline in [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md) |
| Production outage (agent serving) | On-call engineer + Rohan | PagerDuty rotation `intel-agents-oncall` |
| Sandbox or GPU pool issue | Platform Infrastructure on-call + Rohan | `#platform-oncall` |
| Cross-team dependency (Inference, ML, Workspace) | Receiving EM via Rohan | Rohan routes |
| Customer data question (sandbox carve-out) | Privacy Office + CISO designate | `privacy@acme.example` |

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
