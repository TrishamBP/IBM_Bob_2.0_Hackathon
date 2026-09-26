---
document_id: ACME-REPO-005
title: Repository Guide — acme-intelligence-ml
category: engineering
department: engineering
applicable_roles: [ml-engineers, ml-researchers, data-engineers, platform-engineers]
owner: Lakshmi Narayan (EM, Intelligence ML)
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [repository, acme-intelligence, python-pytorch-mlflow-kubeflow]
---

# Repository Guide — `acme-intelligence-ml`

> **Fictional repository.** The host `git.acme.example` does not resolve. All commands below are **simulated** and shown for onboarding orientation only. Do not attempt to execute them against any real system.

## 1. Repository Purpose

`acme-intelligence-ml` is the **model training and evaluation** codebase for ACME Intelligence. It contains the training pipelines, fine-tuning recipes, evaluation harnesses, and the model registry glue that promotes a candidate checkpoint into `acme-intelligence-inference` for serving.

Key responsibilities:

- Supervised fine-tuning and RLHF/GRPO pipelines for the agent models.
- Offline evaluation harness (golden prompt sets, regression suites).
- MLflow tracking and model registry integration.
- Kubeflow Pipelines definitions for distributed training jobs.

## 2. Owning Team and EM

| Field | Value |
|-------|-------|
| Owning Team | Intelligence ML |
| Engineering Manager | Lakshmi Narayan (lakshmi.narayan@acme.example) |
| Product | ACME Intelligence |
| Slack channel (fictional) | `#intel-ml` |
| On-call rotation | `intel-ml-oncall` (P-grade training-registry incidents) |

## 3. Primary Technology Stack

- **Language:** Python 3.11
- **Framework:** PyTorch 2.3, TorchTitan, DeepSpeed for distributed training
- **Tracking / registry:** MLflow 2.x; model registry at `mlflow.internal.acme.example`
- **Orchestration:** Kubeflow Pipelines 2.x on `k8s-train.internal.acme.example`
- **Data:** Parquet datasets in `objects.internal.acme.example/intel-data/`; lineage in OpenLineage
- **Secrets:** Vault at `vault.acme.example` (path `secret/intel/ml/*`)

## 4. Access Requirements

- **Source access:** Read/write requires the **Engineering — Intelligence** access tier.
- **CI access:** Self-hosted GitHub Actions runners at `runners.internal.acme.example`. Multi-GPU builds run on the `gpu-build` pool.
- **Container registry:** Push to `registry.internal.acme.example/acme-intel/ml` is limited to CI plus release managers.
- **Kubeflow access:** Engineers receive a personal profile on the dev training cluster; production training pipelines run under a service account.
- **Dataset access:** Datasets are classification-tagged. Customer-derived datasets require a Data Use Agreement (DUA); see [`../../03-security/customer-data-handling.md`](../../03-security/customer-data-handling.md).
- See [`../../08-forms/repository-access-request.md`](../../08-forms/repository-access-request.md) and [`../source-code-and-repository-access.md`](../source-code-and-repository-access.md).

## 5. Manager Approval Required

**Yes.** Access requires:

1. Hiring EM (Lakshmi Narayan) approval — auto-confirmed for home repository.
2. Receiving EM (Lakshmi Narayan or delegate) for cross-team contributors.
3. Security GRC + Data Governance review — required for any change to dataset ingestion, RLHF reward models, or evaluation harness code that gates production release.

Production model promotion (writing to the model registry's `prod` stage) is restricted to the release-manager role plus on-call ML. Engineers do **not** receive standing registry-write access. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md).

## 6. Local Setup

```bash
# fictional/simulated command — clone the repository
git clone git@git.acme.example:acme-intelligence/acme-intelligence-ml.git
cd acme-intelligence-ml

# fictional/simulated command — create the virtualenv
python -m venv .venv && source .venv/bin/activate

# fictional/simulated command — install dev dependencies (CUDA build flags auto-detected)
pip install -e ".[dev]"

# fictional/simulated command — configure MLflow tracking URI
export MLFLOW_TRACKING_URI=https://mlflow.internal.acme.example

# fictional/simulated command — pull the synthetic dev dataset (NOT real customer data)
python -m acme.intel.ml.datasets pull --name=synthetic-dev --out=./data/

# fictional/simulated command — connect to dev Vault for training secrets
export VAULT_ADDR=https://vault.acme.example
# vault login -method=oidp role=intel-ml-dev  # interactive
```

> Do **not** clone real customer datasets to your laptop. Use the synthetic fixtures under `tests/fixtures/`.

## 7. Branching Conventions

Trunk-based per [`../git-branching-strategy.md`](../practices/git-branching-strategy.md):

- `main` — always re-trainable.
- `feat/<jira-id>-<slug>` — new pipeline or recipe.
- `fix/<jira-id>-<slug>` — defects.
- `exp/<your-name>-<slug>` — research branches; require a `#experiments` channel announcement before launch.
- `release/<YYYY.MM>` — cut monthly from `main`.

Experiment runs that touch reward models or eval harnesses require a peer review on the experiment plan before launch.

## 8. Build and Test Commands

```bash
# fictional/simulated command — type-check
make typecheck

# fictional/simulated command — unit tests (CPU-only)
make test

# fictional/simulated command — run the eval harness on synthetic data
make eval -- --dataset=synthetic-dev --model=baseline

# fictional/simulated command — smoke-train (a few steps, to validate pipeline)
make smoke-train

# fictional/simulated command — linters (ruff, black, bandit)
make lint

# fictional/simulated command — build the trainer container image
make docker-build IMG=registry.internal.acme.example/acme-intel/ml:dev
```

## 9. Pull-Request Requirements

- `CODEOWNERS` enforced via branch protection.
- **Two** approving reviews for `main`; at least one from the Intelligence ML team.
- Required status checks:
  - `ci/build`
  - `ci/unit-tests`
  - `ci/lint`
  - `ci/typecheck`
  - `ci/smoke-train` (validates the pipeline runs end-to-end on tiny config)
  - `ci/sast`
  - `ci/license-scan` (dataset + model license gate)
- PRs touching `pipelines/rlhf/`, `evaluation/`, or `datasets/` additionally require Security GRC + Data Governance approval.
- PRs that change model behavior must link an MLflow run ID in the description.
- See [`../pull-requests-and-code-review.md`](../practices/pull-requests-and-code-review.md) and [`../coding-standards.md`](../practices/coding-standards.md).

## 10. CODEOWNERS (Sample Structure)

```text
# Sample CODEOWNERS for acme-intelligence-ml (fictional)
*                                           @acme/intel-ml

# RLHF and reward model code — security + data governance co-review
/pipelines/rlhf/                           @acme/intel-ml @acme/security-grc @acme/data-gov
/reward_models/                            @acme/intel-ml @acme/security-grc @acme/data-gov

# Evaluation harness — gates production release; require ML lead review
/evaluation/                               @acme/intel-ml-leads

# Dataset ingestion — data governance co-review
/datasets/                                 @acme/intel-ml @acme/data-gov

# Kubeflow pipeline definitions — platform review
/kubeflow/                                 @acme/intel-ml @acme/platform
```

## 11. Deployment Environments

| Environment | Purpose | Trigger | Approver |
|-------------|---------|---------|----------|
| `dev` | Personal Kubeflow profile; smoke-train runs | Push to a feature branch | Auto (CI) |
| `staging` | Pre-prod training pipeline; staging MLflow registry | Merge to `main` | Intelligence ML EM (Lakshmi Narayan) |
| `production` | Customer-affecting model promotion (registry `prod` stage) | Tagged release + model card + change ticket | Release Manager + on-call ML |

**Sample deployment sequence (fictional):**

```bash
# fictional/simulated command — promote a candidate model to the staging MLflow registry
make model-promote -- --env=staging --run-id=abc123 --version=2026.09.3-rc1

# fictional/simulated command — render the production training pipeline definition
make kfp-render ENV=prod > deploy/manifests/prod-training.yaml

# fictional/simulated command — open a change ticket with the model card attached
# Use the ITSM portal: https://itsm.acme.example/change/new  (fictional)

# fictional/simulated command — promote model to production registry stage (release managers only)
# make model-promote -- --env=prod --version=2026.09.3
```

> Promotion to the production MLflow registry stage is **not** standing access. Release managers and on-call ML receive just-in-time elevation. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md) and [`../ci-cd-overview.md`](../practices/ci-cd-overview.md).

## 12. Documentation Links

- Internal Wiki (fictional): `https://wiki.acme.example/intelligence/ml/architecture`
- Model registry guide (fictional): `https://wiki.acme.example/intelligence/ml/registry`
- Experiment conventions (fictional): `https://wiki.acme.example/intelligence/ml/experiments`
- Runbooks (fictional): `https://wiki.acme.example/intelligence/ml/runbooks`
- Service catalog entry: `https://catalog.acme.example/services/acme-intelligence-ml`

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
- [`../../03-security/customer-data-handling.md`](../../03-security/customer-data-handling.md)
- [`../../08-forms/repository-access-request.md`](../../08-forms/repository-access-request.md)
- [`../../08-forms/it-access-request.md`](../../08-forms/it-access-request.md)
- [`../../09-contacts/contact-directory.md`](../../09-contacts/contact-directory.md)
