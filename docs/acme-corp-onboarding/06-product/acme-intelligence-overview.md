---
document_id: ACME-PROD-003
title: ACME Intelligence Product Overview
category: product
department: intelligence-bu
applicable_roles: [all]
owner: Product Management
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [product, intelligence, ai, overview]
---

# ACME Intelligence Product Overview

ACME Intelligence is the company's enterprise AI platform. It lets customers deploy AI agents, run model inference inside their own cloud tenancy, and use retrieval-augmented generation (RAG) against their own corpora with policy guardrails. The product is aimed at regulated industries — financial services, healthcare, public sector — where customers cannot ship AI workloads to shared public SaaS endpoints without compliance review.

## Business Purpose

Customers use ACME Intelligence to put AI to work inside their own security perimeter. They connect their data sources (SharePoint, Confluence, databases, file shares), define guardrails (PII redaction, prompt-injection defenses, output filters), and deploy agents and inference endpoints that are accessible only to their own workforce. ACME's role is to provide the platform; the customer remains the data controller.

## Intended Users

- **AI platform engineers** — deploy and operate inference endpoints and agents.
- **Application developers** — build agents on top of the platform's SDKs.
- **Knowledge managers** — curate retrieval corpora, manage indexes.
- **Risk and compliance officers** — review guardrails, audit prompts and outputs.
- **Business users** — use deployed agents through ACME Workspace or a customer-built UI.

## Major Capabilities

| Capability | Description |
|------------|-------------|
| Inference endpoints | Customer-tenanted model serving for open-weight and select proprietary models. |
| Agents | Declarative agent framework with tool calling, RAG, and policy guardrails. |
| Retrieval | Vector and keyword indexes over customer corpora with refresh pipelines. |
| Guardrails | PII redaction, prompt-injection defenses, output content filters, audit logging. |
| Evaluation | Built-in eval harness for agent quality and safety. |
| Observability | Per-request tracing, token usage, latency, error rates. |
| Audit | Tamper-evident audit log of every prompt, tool call, and model response. |

## System Components

| Component | Description | Owning Repository |
|-----------|-------------|-------------------|
| Agents service | Agent execution runtime, tool dispatch, RAG orchestration | `acme-intelligence-agents` |
| Inference service | Model serving, autoscaling, routing | `acme-intelligence-inference` |
| ML platform | Training, fine-tuning, evaluation pipelines | `acme-intelligence-ml` |
| Guardrail library | PII redaction, prompt filters, output filters | `acme-intelligence-agents` (subpackages) |
| Retrieval service | Index management, ingestion pipelines | `acme-intelligence-agents` (subpackages) |
| Audit service | Tamper-evident logging | `acme-platform-infrastructure` |

## Owning Teams

- **Product:** Omar Farouk (Product Lead), reporting to Daniel Coelho (CPO).
- **Intelligence Agents:** Rohan Bhat (EM), reporting to Anitha Rajan (Director AI/ML).
- **Intelligence Inference:** Vivek Anand (EM), reporting to Anitha Rajan.
- **Intelligence ML:** Lakshmi Narayan (EM), reporting to Anitha Rajan.
- **Platform (shared):** Nikhil Joshi (Manager), reporting to Sridhar Venkatesh.
- **Design:** Sara Lindberg's UX team.

See [`00-company/organizational-structure.md`](../00-company/organizational-structure.md) and [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md).

## How Your Work Connects

- If you are joining **Intelligence Agents**, your work is in `acme-intelligence-agents`. You will likely work on the agent runtime, tool dispatch, RAG orchestration, or the guardrail library.
- If you are joining **Intelligence Inference**, your work is in `acme-intelligence-inference`. You will likely work on model serving, autoscaling, or routing.
- If you are joining **Intelligence ML**, your work is in `acme-intelligence-ml`. You will likely work on training pipelines, fine-tuning, or evaluation harnesses.
- Across all three teams, you will frequently interact with the Platform Infrastructure team for shared services (observability, audit, secrets).

## Model Lineup (Fictional, Indicative)

The following are fictional model identifiers used internally to discuss which models a customer can deploy. They are not real model names.

| Model Identifier | Class | Use Case |
|------------------|-------|----------|
| acme-mini-1 | small language model | lightweight tool calling, classification |
| acme-mid-1 | mid-size language model | general-purpose chat, summarization |
| acme-large-1 | large language model | complex reasoning, code |
| acme-embed-1 | embedding model | retrieval |
| acme-rerank-1 | reranker | retrieval quality |

## Customer-Facing URLs (Fictional)

| Surface | URL (fictional) |
|---------|-----------------|
| Intelligence console | intelligence.acme.example |
| Intelligence status | status.acme.example/intelligence |
| Intelligence docs | docs.acme.example/intelligence |
| Intelligence API | api.intelligence.acme.example |

## Related Documents

- [`06-product/product-catalog.md`](./product-catalog.md)
- [`06-product/acme-cloud-overview.md`](./acme-cloud-overview.md)
- [`06-product/acme-workspace-overview.md`](./acme-workspace-overview.md)
- [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md)
- [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md)
