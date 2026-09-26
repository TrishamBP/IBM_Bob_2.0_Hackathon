---
document_id: ACME-ENG-001
title: ACME Corp Repository Catalog
category: engineering
department: engineering
applicable_roles: [all-engineers]
owner: Engineering
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [repositories, catalog, canonical]
---

# ACME Corp Repository Catalog

This is the **canonical catalog** of fictional ACME repositories. Every other document that mentions a repository must agree with what is listed here. All repository URLs use the fictional host `git.acme.example`.

> Repositories below are fictional. The host `git.acme.example` does not resolve and the listed repository names exist only for internal consistency of this knowledge base.

## Catalog

| Repository | Owning Team | EM | Product | Primary Stack | Access Tier |
|------------|-------------|----|---------|---------------|-------------|
| `acme-cloud-api` | Cloud API | Anjali Desai | ACME Cloud | Go, gRPC, PostgreSQL, Kafka | Engineering — Cloud |
| `acme-cloud-frontend` | Cloud Frontend | Manoj Pillai | ACME Cloud | TypeScript, React, Vite, Playwright | Engineering — Cloud |
| `acme-intelligence-agents` | Intelligence Agents | Rohan Bhat | ACME Intelligence | Python, FastAPI, Ray, Postgres | Engineering — Intelligence |
| `acme-intelligence-inference` | Intelligence Inference | Vivek Anand | ACME Intelligence | Python, CUDA, Triton, Kubernetes | Engineering — Intelligence |
| `acme-intelligence-ml` | Intelligence ML | Lakshmi Narayan | ACME Intelligence | Python, PyTorch, MLflow, Kubeflow | Engineering — Intelligence |
| `acme-workspace-web` | Workspace Web | Thomas Buckley | ACME Workspace | TypeScript, React, WebRTC | Engineering — Workspace |
| `acme-workspace-api` | Workspace API | Priya Menon | ACME Workspace | Java, Spring Boot, PostgreSQL, Kafka | Engineering — Workspace |
| `acme-platform-infrastructure` | Platform Infrastructure | Nikhil Joshi | Shared | Terraform, Go, Kubernetes, Crossplane | Engineering — Platform |
| `acme-shared-libraries` | Platform Infrastructure (acting) | Nikhil Joshi | Shared | Multi-language (Go, TypeScript, Python, Java) | Engineering — Platform |
| `acme-quality-automation` | Quality Engineering | Asha Reddy | Shared | Python, Playwright, JMeter | Engineering — QE |

## Access Tiers

Access to ACME repositories is gated by tier. The same employee does not automatically get every repository in their tier — they get the repositories required for their role, approved by their EM.

| Tier | Description | Examples |
|------|-------------|----------|
| **All Engineers** | Read access to shared libraries and quality automation. | `acme-shared-libraries`, `acme-quality-automation` (read) |
| **Engineering — Cloud** | Read/write to Cloud repositories, plus platform shared libs. | `acme-cloud-api`, `acme-cloud-frontend` |
| **Engineering — Intelligence** | Read/write to Intelligence repositories. | `acme-intelligence-agents`, `acme-intelligence-inference`, `acme-intelligence-ml` |
| **Engineering — Workspace** | Read/write to Workspace repositories. | `acme-workspace-web`, `acme-workspace-api` |
| **Engineering — Platform** | Read/write to platform and shared libraries. | `acme-platform-infrastructure`, `acme-shared-libraries` |
| **Production deploy** | Restricted to on-call and release managers. | Production environment credentials |

For the full per-repository details — purpose, primary technology stack, access requirements, branching conventions, build/test commands, PR requirements, CODEOWNERS, deployment environments — see the per-repository documents in [`04-engineering/repositories/`](./repositories/).

## Per-Repository Documents

- [`04-engineering/repositories/acme-cloud-api.md`](./repositories/acme-cloud-api.md)
- [`04-engineering/repositories/acme-cloud-frontend.md`](./repositories/acme-cloud-frontend.md)
- [`04-engineering/repositories/acme-intelligence-agents.md`](./repositories/acme-intelligence-agents.md)
- [`04-engineering/repositories/acme-intelligence-inference.md`](./repositories/acme-intelligence-inference.md)
- [`04-engineering/repositories/acme-intelligence-ml.md`](./repositories/acme-intelligence-ml.md)
- [`04-engineering/repositories/acme-workspace-web.md`](./repositories/acme-workspace-web.md)
- [`04-engineering/repositories/acme-workspace-api.md`](./repositories/acme-workspace-api.md)
- [`04-engineering/repositories/acme-platform-infrastructure.md`](./repositories/acme-platform-infrastructure.md)
- [`04-engineering/repositories/acme-shared-libraries.md`](./repositories/acme-shared-libraries.md)
- [`04-engineering/repositories/acme-quality-automation.md`](./repositories/acme-quality-automation.md)

## Requesting Repository Access

Repository access is requested via [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md). The request requires:

1. **Hiring EM approval** (auto-confirmed for the new hire's home repository).
2. **Receiving EM approval** (for cross-team repositories).
3. **Security GRC review** for production-deploy or sensitive repositories.

See [`03-security/identity-and-access-management.md`](../03-security/identity-and-access-management.md) and [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) for the policy basis.

## Related Documents

- [`04-engineering/developer-workstation-setup.md`](./developer-workstation-setup.md)
- [`04-engineering/source-code-and-repository-access.md`](./source-code-and-repository-access.md)
- [`04-engineering/git-branching-strategy.md`](./practices/git-branching-strategy.md)
- [`04-engineering/pull-requests-and-code-review.md`](./practices/pull-requests-and-code-review.md)
- [`00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md)
