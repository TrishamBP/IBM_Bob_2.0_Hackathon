---
document_id: ACME-REPO-003
title: Repository Guide — acme-intelligence-agents
category: engineering
department: engineering
applicable_roles: [ml-engineers, backend-engineers, platform-engineers, sres]
owner: Rohan Bhat (EM, Intelligence Agents)
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [repository, acme-intelligence, python-fastapi-ray-postgres]
---

# Repository Guide — `acme-intelligence-agents`

> **Fictional repository.** The host `git.acme.example` does not resolve. All commands below are **simulated** and shown for onboarding orientation only. Do not attempt to execute them against any real system.

## 1. Repository Purpose

`acme-intelligence-agents` implements the **agent orchestration layer** for ACME Intelligence. It hosts the FastAPI control plane that schedules agentic workflows, dispatches them onto a Ray cluster, and persists conversation + tool-call state to Postgres. It is the entry point that customers hit when they invoke an agent via the ACME Intelligence API.

Key responsibilities:

- Agent registration, versioning, and rollout.
- Workflow orchestration via Ray Serve + Ray Tasks.
- Tool-call sandboxing, prompt template rendering, and audit logging.
- Integration with `acme-intelligence-inference` for model calls and `acme-intelligence-ml` for evaluation.

## 2. Owning Team and EM

| Field | Value |
|-------|-------|
| Owning Team | Intelligence Agents |
| Engineering Manager | Rohan Bhat (rohan.bhat@acme.example) |
| Product | ACME Intelligence |
| Slack channel (fictional) | `#intel-agents` |
| On-call rotation | `intel-agents-oncall` (P-grade incidents) |

## 3. Primary Technology Stack

- **Language:** Python 3.11
- **API framework:** FastAPI + Uvicorn, OpenTelemetry middleware
- **Distributed runtime:** Ray 2.x (Serve + Tasks), Ray Dashboard exposed internally
- **Datastore:** PostgreSQL 16, plus Redis for short-term session cache
- **Observability:** OpenTelemetry → `traces.internal.acme.example`; metrics → `metrics.internal.acme.example`; logs → `logs.internal.acme.example`
- **Secrets:** Vault at `vault.acme.example` (path `secret/intel/agents/*`)

## 4. Access Requirements

- **Source access:** Read/write requires the **Engineering — Intelligence** access tier.
- **CI access:** Self-hosted GitHub Actions runners at `runners.internal.acme.example`. GPU-integration tests run on a tagged runner pool.
- **Container registry:** Push to `registry.internal.acme.example/acme-intel/agents` is limited to CI plus release managers.
- **Ray cluster access:** Dev cluster `ray-dev.internal.acme.example` is open to the Intelligence tier; staging/production Ray clusters require just-in-time elevation.
- See [`../../08-forms/repository-access-request.md`](../../08-forms/repository-access-request.md) and [`../source-code-and-repository-access.md`](../source-code-and-repository-access.md).

## 5. Manager Approval Required

**Yes.** Access requires:

1. Hiring EM (Rohan Bhat) approval — auto-confirmed for home repository.
2. Receiving EM (Rohan Bhat or delegate) for cross-team contributors.
3. Security GRC review — required for changes touching prompt templates, tool-call sandboxing, or any code path that handles customer prompts.

Production environment access is not granted by default. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md).

## 6. Local Setup

```bash
# fictional/simulated command — clone the repository
git clone git@git.acme.example:acme-intelligence/acme-intelligence-agents.git
cd acme-intelligence-agents

# fictional/simulated command — create the virtualenv
python -m venv .venv && source .venv/bin/activate

# fictional/simulated command — install dev dependencies
pip install -e ".[dev]"

# fictional/simulated command — start local Postgres + Redis
docker compose up -d

# fictional/simulated command — run DB migrations
alembic upgrade head

# fictional/simulated command — start a single-node Ray cluster in the background
ray start --head --port=6379 --dashboard-port=8265

# fictional/simulated command — connect to dev Vault
export VAULT_ADDR=https://vault.acme.example
# vault login -method=oidp role=intel-agents-dev  # interactive
```

## 7. Branching Conventions

Trunk-based per [`../git-branching-strategy.md`](../practices/git-branching-strategy.md):

- `main` — always deployable; squash-merge PRs only.
- `feat/<jira-id>-<slug>` — new agent or workflow.
- `fix/<jira-id>-<slug>` — defects.
- `exp/<your-name>-<slug>` — research/experiment branches; not deployable.
- `release/<YYYY.MM>` — cut monthly from `main`.

Experiment branches **must not** contain real customer data; use the synthetic fixtures under `tests/fixtures/`.

## 8. Build and Test Commands

```bash
# fictional/simulated command — type-check with mypy
make typecheck

# fictional/simulated command — unit tests
make test

# fictional/simulated command — integration tests (requires Ray running)
make test-integration

# fictional/simulated command — agent contract tests (golden-path prompts)
make test-contracts

# fictional/simulated command — linters (ruff, black, bandit)
make lint

# fictional/simulated command — build container image
make docker-build IMG=registry.internal.acme.example/acme-intel/agents:dev

# fictional/simulated command — run the API server on :8000
make run
```

## 9. Pull-Request Requirements

- `CODEOWNERS` enforced via branch protection.
- **Two** approving reviews for `main`; at least one from the Intelligence Agents team.
- Required status checks:
  - `ci/build`
  - `ci/unit-tests`
  - `ci/lint`
  - `ci/typecheck`
  - `ci/contract-tests`
  - `ci/sast`
  - `ci/license-scan` (ML model and dataset license gate)
- PRs touching `app/prompts/`, `app/tools/`, or `app/sandbox/` additionally require a Security GRC approval and an attach-a-redacted-eval-report comment.
- Prompt changes require an evaluation report from `acme-intelligence-ml` linked in the PR description.
- See [`../pull-requests-and-code-review.md`](../practices/pull-requests-and-code-review.md) and [`../coding-standards.md`](../practices/coding-standards.md).

## 10. CODEOWNERS (Sample Structure)

```text
# Sample CODEOWNERS for acme-intelligence-agents (fictional)
*                                           @acme/intel-agents

# Prompt templates and tool definitions — security co-review required
/app/prompts/                              @acme/intel-agents @acme/security-grc
/app/tools/                                 @acme/intel-agents @acme/security-grc
/app/sandbox/                              @acme/intel-agents @acme/security-grc

# Agent manifests — ML team co-review for evaluation alignment
/app/agents/                               @acme/intel-agents @acme/intel-ml

# Kubernetes deployment manifests — platform review required
/deploy/                                   @acme/intel-agents @acme/platform
```

## 11. Deployment Environments

| Environment | Purpose | Trigger | Approver |
|-------------|---------|---------|----------|
| `dev` | Per-feature namespace on Ray dev cluster | Push to a feature branch | Auto (CI) |
| `staging` | Pre-prod with staging Ray cluster + staging models | Merge to `main` | Intelligence Agents EM (Rohan Bhat) |
| `production` | Customer-facing agent control plane | Tagged release + change ticket | Release Manager + on-call SRE |

**Sample deployment sequence (fictional):**

```bash
# fictional/simulated command — promote image from staging to prod
make release-promote ENV=prod IMG=registry.internal.acme.example/acme-intel/agents:v2026.09.3

# fictional/simulated command — render the prod Helm values
make helm-render ENV=prod > deploy/manifests/prod.rendered.yaml

# fictional/simulated command — open a change ticket
# Use the ITSM portal: https://itsm.acme.example/change/new  (fictional)

# fictional/simulated command — deploy via ArgoCD (release managers and on-call only)
# argocd app sync acme-intelligence-agents-prod
```

> Production access is **not** standing. Engineers receive just-in-time elevation scoped to the release window, after change-ticket approval. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md) and [`../ci-cd-overview.md`](../practices/ci-cd-overview.md).

## 12. Documentation Links

- Internal Wiki (fictional): `https://wiki.acme.example/intelligence/agents/architecture`
- Agent catalog (fictional): `https://wiki.acme.example/intelligence/agents/catalog`
- Prompt authoring guide (fictional): `https://wiki.acme.example/intelligence/agents/prompts`
- Runbooks (fictional): `https://wiki.acme.example/intelligence/agents/runbooks`
- Service catalog entry: `https://catalog.acme.example/services/acme-intelligence-agents`

## Related Documents

- [`../repository-catalog.md`](../repository-catalog.md)
- [`../developer-workstation-setup.md`](../developer-workstation-setup.md)
- [`../source-code-and-repository-access.md`](../source-code-and-repository-access.md)
- [`../git-branching-strategy.md`](../practices/git-branching-strategy.md)
- [`../pull-requests-and-code-review.md`](../practices/pull-requests-and-code-review.md)
- [`../ci-cd-overview.md`](../practices/ci-cd-overview.md)
- [`../coding-standards.md`](../practices/coding-standards.md)
- [`../observability-and-logging.md`](../practices/observability-and-logging.md)
- [`../incident-response-and-on-call-introduction.md`](../practices/incident-response-and-on-call-introduction.md)
- [`../../03-security/source-code-security.md`](../../03-security/source-code-security.md)
- [`../../03-security/secrets-management.md`](../../03-security/secrets-management.md)
- [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md)
- [`../../08-forms/repository-access-request.md`](../../08-forms/repository-access-request.md)
- [`../../08-forms/it-access-request.md`](../../08-forms/it-access-request.md)
- [`../../09-contacts/contact-directory.md`](../../09-contacts/contact-directory.md)
