---
document_id: ACME-TEAM-005
title: ACME Corp AI Research Engineer Onboarding
category: team-onboarding
department: intelligence-ml
applicable_roles: [ai-research-engineer]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [team-onboarding, ai-research-engineer]
---

# ACME Corp AI Research Engineer Onboarding

Welcome to the **Intelligence ML** team at ACME Corp. This guide is your single reference for the first 90 days as an AI Research Engineer building the model training and evaluation pipelines for ACME Intelligence. It assumes you have already completed [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) and [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md).

> ACME Corp is a fictional company. All names, repositories, hosts, and systems referenced here are illustrative and use the `.example` domain. Do not attempt to reach any URL.

## 1. Team Overview

| Field | Value |
|-------|-------|
| Team name | Intelligence ML |
| Reports up to | Anitha Rajan (Director AI/ML) via EM Lakshmi Narayan |
| Primary office | Bengaluru (with hybrid remote) |
| Primary product | ACME Intelligence — see [`06-product/acme-intelligence-overview.md`](../06-product/acme-intelligence-overview.md) |
| Primary repository | `acme-intelligence-ml` — see [`04-engineering/repositories/acme-intelligence-ml.md`](../04-engineering/repositories/acme-intelligence-ml.md) |
| Primary channel | `#intelligence-ml` (Microsoft Teams) |

**Mission.** Build and operate the model training, fine-tuning, evaluation, and release pipelines for ACME Intelligence. The team trains and ships the foundation models and task-specific adapters that the Agents and Inference teams serve to customers.

**Charter.** Owns dataset construction, training pipelines (PyTorch + MLflow + Kubeflow), evaluation harnesses, model registry, and the release process for new model versions to the Inference team. Does **not** own agent orchestration (Intelligence Agents), the inference serving engine (Intelligence Inference), or the customer-facing API surface.

**Customers.** Intelligence Agents (consumer of fine-tuned models); Intelligence Inference (consumer of released model artifacts); Anitha Rajan and the AI/ML leadership (research reviews); external research community (where ACME publishes select papers, vetted by Legal).

## 2. Reporting Manager

- **Engineering Manager:** Lakshmi Narayan (lakshmi.narayan@acme.example, Bengaluru office, hybrid).
- Lakshmi reports to Anitha Rajan (Director AI/ML).
- Your standing 1:1 is 30 minutes weekly.
- Reporting line is recorded at `hr.acme.example` under your profile.

## 3. Onboarding Buddy

- **Buddy:** Varun Iyer (varun.iyer@acme.example), Tech Lead, Intelligence ML.
- Varun is your peer mentor for the first 90 days — training pipeline conventions, dataset tooling, eval harness, model release process, GPU cluster usage.
- Buddy commitment: 2 hours per day for the first 2 weeks; 1 hour per day for weeks 3–6; ad-hoc thereafter.
- See [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) for the buddy program's expectations.

## 4. Required Documents (Week 1)

Read each of the following in your first week. Varun will check progress during your week-1 1:1.

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
- [`04-engineering/repositories/acme-intelligence-ml.md`](../04-engineering/repositories/acme-intelligence-ml.md)
- [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md)
- [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md)
- [`04-engineering/practices/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md)
- [`06-product/acme-intelligence-overview.md`](../06-product/acme-intelligence-overview.md)

## 5. Required Software

Install only the approved tools below. Anything else requires a software access request via [`08-forms/software-access-request.md`](../08-forms/software-access-request.md). See [`02-it/approved-software-installation.md`](../02-it/approved-software-installation.md) for the binding policy.

**Workstation baseline (installed by IT before Day 1):**
- Windows 11 Enterprise or macOS 14+ (your work is mostly on remote GPU clusters; the laptop is a thin client)
- Microsoft 365, Microsoft Authenticator, Corporate VPN, 1Password, Microsoft Defender for Endpoint

**Developer tools (you install via the approved package manager):**
- Visual Studio Code (latest stable) or PyCharm Professional (license via IT self-service)
- Python 3.11 (matches the repo's `pyproject.toml`)
- `uv` 0.4+ for dependency management
- Docker Desktop (for local pipeline dry-runs)
- `kubectl` and `helm` (the training cluster is Kubernetes-based; see section 8)
- `aws` / `az` / `gcloud` CLI (cross-cloud; ACME trains on multiple clouds)
- GitHub CLI (`gh`) configured for `git.acme.example`

**GPU access (provisioned via Entra ID group):** You will use the **ML training cluster** (`intel-ml-train-cluster`) — a dedicated Kubernetes namespace with multi-cloud GPU node pools. Local laptop GPU is not expected; the laptop is for editing and submitting training jobs.

## 6. Approved AI Tools

Per the role eligibility matrix in [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md), AI Research Engineers are **default-entitled** to **both** AI tools:

| Tool | Entitlement | Notes |
|------|-------------|-------|
| GitHub Copilot Business | **Yes (default)** | Sign in only with `@acme.example` Entra SSO. Useful for boilerplate (dataloaders, configs, eval harness scaffolding). |
| Internal ACME Intelligence sandbox | **Yes (default)** | Access to `intel-sandbox.internal.acme.example` for running controlled experiments against existing models, comparing against your own fine-tunes, and benchmarking. |

`acme-intelligence-ml` is opted in to Copilot via its `copilot-instructions.md`. Read [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) and [`03-security/customer-data-handling.md`](../03-security/customer-data-handling.md) carefully — training datasets may contain customer-derived content subject to consent terms, and must never be sent to public LLM tools. The sandbox is approved for de-identified and consented data only.

## 7. Required Repositories

You will be granted read/write access to the following:

- `acme-intelligence-ml` — your home repository. See [`04-engineering/repositories/acme-intelligence-ml.md`](../04-engineering/repositories/acme-intelligence-ml.md).

Read-only cross-repo access (auto-granted for context):

- `acme-shared-libraries` — shared Python libraries (training utilities, eval client).
- `acme-intelligence-inference` — read-only, to understand how your model artifacts are served.
- `acme-intelligence-agents` — read-only, to understand how agents consume your models.

Repository access is requested via [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md). Lakshmi pre-approves your home repo; cross-team read access requires the receiving EM's approval.

You will **not** receive write access to `acme-intelligence-agents` or `acme-intelligence-inference` (those are the Agents and Inference teams' domains), nor to `acme-cloud-*`, `acme-workspace-*`, or `acme-platform-infrastructure` unless a specific work item requires it. This is per [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).

## 8. Required Access Permissions

On Day 1, IT Onboarding (Geetha Iyer, `geetha.iyer@acme.example`) provisions the following Entra ID groups. Verify each in the My Apps portal at `myapps.acme.example`.

| Entra ID group | Purpose |
|----------------|---------|
| `ENG-Intelligence-ML` | Repository write access to `acme-intelligence-ml`, CI runners. |
| `ENG-Shared-Libraries-Read` | Read-only access to `acme-shared-libraries`. |
| `ENG-Intelligence-Inference-Read` | Read-only access to `acme-intelligence-inference`. |
| `ENG-Intelligence-Agents-Read` | Read-only access to `acme-intelligence-agents`. |
| `Vault-Customer-Intel-ML-Dev` | Personal HashiCorp Vault token scoped to `secret/intel-ml/dev/*` (includes cloud provider training credentials, dataset registry tokens, sandbox API key). |
| `Copilot-Business-Engineering` | GitHub Copilot Business seat assignment. |
| `Intel-Sandbox-User` | Access to the internal ACME Intelligence sandbox. |
| `Intel-ML-Train-Cluster` | Membership in the ML training Kubernetes cluster (`intel-ml-train-cluster` namespace). |
| `MLflow-Writer-NonProd` | Write access to MLflow tracking server for non-production training runs. |
| `Model-Registry-Writer-NonProd` | Write access to the model registry for non-production model versions. |
| `Observability-Reader-NonProd` | Read-only Grafana non-production dashboards. |

Additional tools (auto-provisioned):

- **Weights & Biases** — full read/write for the team's projects.
- **Hugging Face Hub Enterprise** (internal mirror at `packages.internal.acme.example/hub`) — read access to vetted model weights; push access to team's private models.

Production model registry write access is **not** granted at onboarding. Promoting a model to production requires Lakshmi's approval plus a release ticket — see [`04-engineering/practices/release-management.md`](../04-engineering/practices/release-management.md).

## 9. Training Requirements

Complete the following training in your first 30 days. All training is tracked in your learning transcript at `hr.acme.example/learning`.

| Course | Link | Deadline |
|--------|------|---------|
| Company Orientation | [`10-training/company-orientation.md`](../10-training/company-orientation.md) | Week 1 |
| Security Awareness | [`10-training/security-awareness.md`](../10-training/security-awareness.md) | Week 1 |
| Privacy Awareness | [`10-training/privacy-awareness.md`](../10-training/privacy-awareness.md) | Week 1 (high priority — training data) |
| Engineering Orientation | [`10-training/engineering-orientation.md`](../10-training/engineering-orientation.md) | Week 2 |
| Git and Repository Workflows | [`10-training/git-and-repository-workflows.md`](../10-training/git-and-repository-workflows.md) | Week 2 |
| AI Coding Assistant Usage | [`10-training/ai-coding-assistant-usage.md`](../10-training/ai-coding-assistant-usage.md) | Week 2 |
| ACME Intelligence Product Training | [`10-training/product-training.md`](../10-training/product-training.md) | Week 3 |
| Cloud Platform Fundamentals | [`10-training/cloud-platform-fundamentals.md`](../10-training/cloud-platform-fundamentals.md) | Week 3 |
| Workplace Conduct | [`10-training/workplace-conduct.md`](../10-training/workplace-conduct.md) | Week 4 |

Additional role-specific training delivered by Varun in weeks 2–4:
- "Training cluster usage and queueing" workshop (2 hours).
- "Dataset registry and consent provenance" briefing by Privacy Office (1 hour).
- "Model release to Inference" walkthrough (1 hour).
- "Eval harness and golden-set workflows" workshop (2 hours, shared with Agents team).

## 10. First-Week Activities

- **Day 1:** IT activation (M365, Authenticator, laptop). Read [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md). Manager intro 1:1 with Lakshmi.
- **Day 2:** Clone `acme-intelligence-ml`. Run `uv sync` and `make test` to verify the test suite passes. Read the repo's `README.md` and [`04-engineering/repositories/acme-intelligence-ml.md`](../04-engineering/repositories/acme-intelligence-ml.md).
- **Day 3:** Configure VS Code / PyCharm. Sign into GitHub Copilot via Entra SSO. Get your Vault token, the sandbox API key, and verify your access to the training cluster with `kubectl get pods -n intel-ml-train-cluster`.
- **Day 4:** Run a smoke training job (the repo includes `make train-smoke`) and observe it in MLflow. Pick a `good-first-issue` labeled ticket. Create your first branch per [`04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md).
- **Day 5:** Open your first PR. Request review from Varun. Read [`04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md) before requesting review.

## 11. First-Month Deliverables

1. **Merged PR #1** — a `good-first-issue` (eval case addition, dataset loader fix, config refactor).
2. **Merged PR #2** — a small training pipeline or eval change assigned by Varun, with the resulting run logged in MLflow.
3. **Local + cluster environment fully working** — including Vault, sandbox, training cluster, MLflow, model registry.
4. **Completed all Week 1–4 training** in section 9 plus the role-specific workshops.
5. **First shadow on-call shift** — paired with the on-call engineer for one weekday evening. ML on-call covers training cluster incidents and stuck jobs.
6. **First model artifact in non-production registry** — a small fine-tune or adapter, versioned in the model registry (non-production only).

## 12. 30/60/90-Day Expectations

| Window | Expectation |
|--------|-------------|
| **30 days** | Local + cluster setup complete. First small PR merged (with MLflow run). Pair with buddy on at least 3 PRs. Shadow one on-call shift. Complete security, privacy, engineering, and AI-assistant training plus role-specific workshops. |
| **60 days** | Ship a feature-sized change (a new training pipeline, a new eval suite, or a model improvement) with eval coverage showing a measurable improvement on a golden set. Participate in code review as a reviewer on at least 4 PRs. Complete an on-call shadow rotation (one full week of evening shifts, with a backup on call). Begin owning one model family or one eval suite. |
| **90 days** | Ship a medium-sized feature end-to-end (experiment design → training runs → eval → PR → non-prod model registry release → handoff to Inference). Lead a small design doc (RFC) for a feature in your area, reviewed by Lakshmi and Varun. Take a primary on-call shift (with backup) for at least one weekday. Be the assigned reviewer on at least 8 PRs. |

## 13. Team Meetings

| Meeting | Cadence | Owner | Your role |
|---------|---------|-------|-----------|
| Daily standup | 15 min, 10:00 IST | Lakshmi Narayan | Attend, share blocker |
| Sprint planning | 60 min, every other Monday | Lakshmi Narayan | Estimate, sign up |
| Sprint review & retrospective | 60 min, every other Friday | Lakshmi Narayan | Demo; raise retro items |
| 1:1 with manager | 30 min, weekly | Lakshmi Narayan | Career, blockers, feedback |
| 1:1 with buddy | 30 min, weekly for first 6 weeks | Varun Iyer | Questions, peer feedback |
| Experiment review | 60 min, weekly | Varun Iyer | Present your experiments and MLflow runs |
| Intelligence cross-team sync (Agents + Inference + ML) | 30 min, weekly | Anitha Rajan | Attend |
| Model release review | 60 min, biweekly | Lakshmi Narayan + Vivek Anand (Inference) | Attend when relevant |
| Research reading group | 60 min, weekly | Anitha Rajan | Optional but encouraged |
| All-hands | 60 min, monthly | Sridhar Venkatesh | Attend |

## 14. Escalation Contacts

Use the following contacts in priority order. See [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for the full directory.

| Need | Contact | How |
|------|---------|-----|
| Technical question, repo, build | Buddy: Varun Iyer (varun.iyer@acme.example) | Teams DM or `#intelligence-ml` |
| People/career/scope | Manager: Lakshmi Narayan (lakshmi.narayan@acme.example) | 1:1 or Teams DM |
| HR / leave / payroll / policy | HRBP: Deepika Rao (deepika.rao@acme.example) — covers Intelligence | `hr.acme.example`, then Teams DM |
| IT (laptop, VPN, M365, software) | IT Helpdesk | `helpdesk.acme.example` or `#it-helpdesk` |
| Training cluster incident (GPU pool, job stuck) | Platform Infrastructure on-call | `#platform-oncall` + PagerDuty `platform-oncall` |
| Security incident or suspected breach (incl. sandbox misuse, dataset leakage) | SOC + CISO Rajan Mehta | `soc@acme.example` + 24/7 hotline in [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md) |
| Production outage (model serving) | Inference on-call + Lakshmi | PagerDuty rotation `intel-inference-oncall` |
| Cross-team dependency (Inference, Agents, Platform) | Receiving EM via Lakshmi | Lakshmi routes |
| Customer data / consent question for training datasets | Privacy Office + CISO designate | `privacy@acme.example` |
| External publication / paper review | Legal: Hemant Joshi (hemant.joshi@acme.example) + Anitha Rajan | Email Legal, cc Lakshmi |

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
