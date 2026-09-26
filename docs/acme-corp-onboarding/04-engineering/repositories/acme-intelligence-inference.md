---
document_id: ACME-REPO-004
title: Repository Guide — acme-intelligence-inference
category: engineering
department: engineering
applicable_roles: [ml-engineers, inference-engineers, sres, platform-engineers]
owner: Vivek Anand (EM, Intelligence Inference)
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [repository, acme-intelligence, python-cuda-triton-kubernetes]
---

# Repository Guide — `acme-intelligence-inference`

> **Fictional repository.** The host `git.acme.example` does not resolve. All commands below are **simulated** and shown for onboarding orientation only. Do not attempt to execute them against any real system.

## 1. Repository Purpose

`acme-intelligence-inference` is the **model serving layer** for ACME Intelligence. It packages foundation + fine-tuned models onto NVIDIA Triton Inference Server, exposes them through a thin FastAPI router, and runs on GPU-enabled Kubernetes node pools. It is the system that turns raw weights into callable endpoints.

Key responsibilities:

- Triton model repository management and warm-up.
- Request routing, batching, and KV-cache-aware scheduling.
- GPU autoscaling via Kubernetes + NVIDIA GPU operator.
- Latency and token-throughput SLO enforcement per model.

## 2. Owning Team and EM

| Field | Value |
|-------|-------|
| Owning Team | Intelligence Inference |
| Engineering Manager | Vivek Anand (vivek.anand@acme.example) |
| Product | ACME Intelligence |
| Slack channel (fictional) | `#intel-inference` |
| On-call rotation | `intel-inference-oncall` (P-grade GPU/SLO incidents) |

## 3. Primary Technology Stack

- **Language:** Python 3.11 (control plane), CUDA 12.x kernels in `kernels/`
- **Serving runtime:** NVIDIA Triton Inference Server 24.x
- **Orchestration:** Kubernetes 1.29, NVIDIA GPU operator, KAI Scheduler for batch jobs
- **Observability:** OpenTelemetry → `traces.internal.acme.example`; DCGM-exporter metrics → `metrics.internal.acme.example`
- **Secrets:** Vault at `vault.acme.example` (path `secret/intel/inference/*`); model weight access keys rotated weekly.

## 4. Access Requirements

- **Source access:** Read/write requires the **Engineering — Intelligence** access tier.
- **CI access:** Self-hosted GitHub Actions runners at `runners.internal.acme.example`. Builds that produce GPU images run on the `gpu-build` runner pool.
- **Container registry:** Push to `registry.internal.acme.example/acme-intel/inference` is limited to CI plus release managers. GPU images carry license-scoped labels.
- **Kubernetes access:** Engineers get a personal namespace on the dev cluster `k8s-dev.internal.acme.example`. Production cluster access is restricted.
- **Model weights:** Stored in encrypted object storage at `objects.internal.acme.example/intel-models/`; access keys issued per-PR via OIDC.
- See [`../../08-forms/repository-access-request.md`](../../08-forms/repository-access-request.md) and [`../source-code-and-repository-access.md`](../source-code-and-repository-access.md).

## 5. Manager Approval Required

**Yes.** Access requires:

1. Hiring EM (Vivek Anand) approval — auto-confirmed for home repository.
2. Receiving EM (Vivek Anand or delegate) for cross-team contributors.
3. Security GRC review — required for any change to model weight loading, encryption-at-rest configuration, or GPU kernel code.

> **Production deploy repository.** Engineers do **not** receive standing production access by default. GPU production clusters are gated behind just-in-time elevation and break-glass procedures. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md).

## 6. Local Setup

```bash
# fictional/simulated command — clone the repository
git clone git@git.acme.example:acme-intelligence/acme-intelligence-inference.git
cd acme-intelligence-inference

# fictional/simulated command — create the virtualenv
python -m venv .venv && source .venv/bin/activate

# fictional/simulated command — install dev dependencies (note: CUDA wheels are heavy)
pip install -e ".[dev,cuda]"

# fictional/simulated command — start a local Triton container with the dev model repo
docker run --gpus all -p8000:8000 -p8001:8001 -p8002:8002 \
  -v $(pwd)/model_repository:/models \
  registry.internal.acme.example/tritonserver:24.x py-tritonserver \
  --model-repository=/models --strict-model-config=false

# fictional/simulated command — connect to dev Vault for model weight credentials
export VAULT_ADDR=https://vault.acme.example
# vault login -method=oidp role=intel-inference-dev  # interactive
```

> Without a GPU on your laptop, use the `--mode=cpu-mock` dev profile; it routes calls to a stub kernel so the rest of the stack still boots.

## 7. Branching Conventions

Trunk-based per [`../git-branching-strategy.md`](../practices/git-branching-strategy.md):

- `main` — always deployable.
- `feat/<jira-id>-<slug>` — new model adapter, router feature, or kernel.
- `fix/<jira-id>-<slug>` — defects.
- `kernel/<slug>` — CUDA kernel experiments (not deployable without review).
- `release/<YYYY.MM>` — cut monthly from `main`.

## 8. Build and Test Commands

```bash
# fictional/simulated command — type-check
make typecheck

# fictional/simulated command — unit tests (CPU-only)
make test

# fictional/simulated command — GPU integration tests (requires GPU runner)
make test-gpu

# fictional/simulated command — latency benchmark on a fixed prompt set
make bench

# fictional/simulated command — linters (ruff, black, bandit, nvtx-check)
make lint

# fictional/simulated command — build the GPU container image
make docker-build-gpu IMG=registry.internal.acme.example/acme-intel/inference:dev-gpu
```

## 9. Pull-Request Requirements

- `CODEOWNERS` enforced via branch protection.
- **Two** approving reviews for `main`; at least one from the Intelligence Inference team.
- Required status checks:
  - `ci/build`
  - `ci/unit-tests`
  - `ci/lint`
  - `ci/typecheck`
  - `ci/gpu-integration` (runs on `gpu-build` pool)
  - `ci/sast`
  - `ci/license-scan` (model + dataset license gate)
- PRs touching `kernels/`, `model_repository/`, or `deploy/` additionally require Security GRC approval and an SRE review.
- Benchmark regression: if `make bench` regresses p99 latency by >5% vs. baseline, the PR is blocked pending an SRE sign-off.
- See [`../pull-requests-and-code-review.md`](../practices/pull-requests-and-code-review.md) and [`../coding-standards.md`](../practices/coding-standards.md).

## 10. CODEOWNERS (Sample Structure)

```text
# Sample CODEOWNERS for acme-intelligence-inference (fictional)
*                                           @acme/intel-inference

# CUDA kernels — SRE + security co-review
/kernels/                                   @acme/intel-inference @acme/sre @acme/security-grc

# Model repository config — ML team co-review for adapter alignment
/model_repository/                          @acme/intel-inference @acme/intel-ml

# Kubernetes deployment — platform review required
/deploy/                                    @acme/intel-inference @acme/platform

# Router logic — SRE co-review for batching/scheduling changes
/app/router/                                @acme/intel-inference @acme/sre
```

## 11. Deployment Environments

| Environment | Purpose | Trigger | Approver |
|-------------|---------|---------|----------|
| `dev` | Per-feature GPU namespace on dev cluster | Push to feature branch | Auto (CI) |
| `staging` | Pre-prod GPU pool with staging models | Merge to `main` | Intelligence Inference EM (Vivek Anand) |
| `production` | Customer-facing GPU inference clusters | Tagged release + change ticket | Release Manager + on-call SRE |

**Sample deployment sequence (fictional):**

```bash
# fictional/simulated command — promote GPU image from staging to prod
make release-promote ENV=prod IMG=registry.internal.acme.example/acme-intel/inference:v2026.09.3-gpu

# fictional/simulated command — render the prod Helm values (GPU pool config)
make helm-render ENV=prod > deploy/manifests/prod.rendered.yaml

# fictional/simulated command — open a change ticket
# Use the ITSM portal: https://itsm.acme.example/change/new  (fictional)

# fictional/simulated command — deploy via ArgoCD (release managers and on-call only)
# argocd app sync acme-intelligence-inference-prod

# fictional/simulated command — canary a single model adapter to 5% traffic
# argocd app sync acme-intelligence-inference-prod --strategy=canary --weight=5
```

> Production GPU clusters are **not** accessible to engineers by default. Just-in-time elevation is granted for a release window after change-ticket approval. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md) and [`../ci-cd-overview.md`](../practices/ci-cd-overview.md).

## 12. Documentation Links

- Internal Wiki (fictional): `https://wiki.acme.example/intelligence/inference/architecture`
- Model catalog (fictional): `https://wiki.acme.example/intelligence/inference/models`
- SLO definitions (fictional): `https://wiki.acme.example/intelligence/inference/slos`
- Runbooks (fictional): `https://wiki.acme.example/intelligence/inference/runbooks`
- Service catalog entry: `https://catalog.acme.example/services/acme-intelligence-inference`

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
