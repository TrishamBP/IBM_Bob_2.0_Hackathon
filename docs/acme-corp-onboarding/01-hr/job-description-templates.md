---
document_id: ACME-HR-003
title: ACME Corp Job Description Templates
category: hr
department: human-resources
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [job-description, template, hr]
---

# ACME Corp Job Description Templates

This document provides reusable job-description templates for ACME Corp hiring managers. Role-specific onboarding guides for each of the listed roles live in [`05-teams/`](../05-teams/).

## Template Structure

Every ACME job description must contain the following sections, in this order:

1. **Job title** and team
2. **Reports to** — manager name and title
3. **Location** — office or "Remote — [Country]"
4. **Employment type** — full-time, part-time, or contract
5. **Mission of the role** — 1–2 sentences on the outcome this role drives
6. **Key responsibilities** — 5–10 bullet points
7. **Required qualifications** — minimum
8. **Preferred qualifications** — nice-to-haves
9. **Required tools and access** — refer to the relevant [`05-teams/`](../05-teams/) onboarding guide
10. **Values alignment** — explicit reference to [`00-company/mission-and-values.md`](../00-company/mission-and-values.md)
11. **Compensation range** — see salary band reference (separate, maintained by HR Operations)

## Template — Engineering Roles

```markdown
## [Job Title] — [Team]

Reports to: [Manager Name], [Manager Title]
Location: [Office / Remote — Country]
Employment type: Full-time

### Mission
[1–2 sentences on the outcome this role drives for ACME and its customers.]

### Key Responsibilities
- [Responsibility 1, with concrete examples]
- [Responsibility 2]
- ... (5–10 items)

### Required Qualifications
- [Degree or equivalent experience]
- [Years of experience]
- [Specific technical skill]
- [Specific technical skill]

### Preferred Qualifications
- [Optional skill]
- [Optional skill]

### Required Tools and Access
See [`05-teams/[role]-onboarding.md`](../05-teams/[role]-onboarding.md).

### Values Alignment
We expect every engineer at ACME to demonstrate the five values in
[`00-company/mission-and-values.md`](../00-company/mission-and-values.md)
in their day-to-day work. Hiring debriefs cite specific examples tied to values.

### Compensation Range
[Refer to the salary band table maintained by HR Operations.]
```

## Sample — Backend Engineer, Cloud API

```markdown
## Backend Engineer — Cloud API

Reports to: Anjali Desai, EM, Cloud API
Location: Hyderabad or Bengaluru (hybrid) / Remote (India)
Employment type: Full-time

### Mission
Build the multi-tenant control plane that powers ACME Cloud. Every customer
action — provisioning, governance, cost, observability — flows through APIs
this team owns.

### Key Responsibilities
- Design and implement new gRPC and REST endpoints in `acme-cloud-api`.
- Improve the performance and reliability of the governance engine.
- Write and maintain unit, integration, and contract tests.
- Participate in on-call rotation (1 week in 6).
- Review pull requests from peers and buddies.

### Required Qualifications
- 3+ years backend engineering experience.
- Strong Go or equivalent (Java, Rust, C++).
- Experience with PostgreSQL and Kafka (or equivalents).
- Understanding of multi-tenancy patterns.

### Required Tools and Access
See [`05-teams/backend-engineer-onboarding.md`](../05-teams/backend-engineer-onboarding.md).
```

## Sample — AI/ML Engineer, Intelligence Agents

```markdown
## AI/ML Engineer — Intelligence Agents

Reports to: Rohan Bhat, EM, Intelligence Agents
Location: Bengaluru (hybrid) / Remote (India)
Employment type: Full-time

### Mission
Build the agent runtime, tool dispatch, and RAG orchestration that powers
ACME Intelligence's customer-deployed agents.

### Key Responsibilities
- Design and implement agent runtime features in `acme-intelligence-agents`.
- Improve the guardrail library (PII redaction, prompt-injection defenses,
  output filters).
- Build eval harnesses for new agent capabilities.
- Pair with the Inference team on model serving performance.

### Required Qualifications
- 3+ years building production Python applications.
- Experience with FastAPI, Ray, or equivalent.
- Familiarity with retrieval (vector DBs, BM25, rerankers).
- Strong systems instincts (latency, throughput, failure modes).

### Required Tools and Access
See [`05-teams/ai-ml-engineer-onboarding.md`](../05-teams/ai-ml-engineer-onboarding.md).
```

## Role → Onboarding Guide Mapping

| Role | Onboarding Guide |
|------|-------------------|
| Frontend Engineer | [`05-teams/frontend-engineer-onboarding.md`](../05-teams/frontend-engineer-onboarding.md) |
| Backend Engineer | [`05-teams/backend-engineer-onboarding.md`](../05-teams/backend-engineer-onboarding.md) |
| Full Stack Engineer | [`05-teams/full-stack-engineer-onboarding.md`](../05-teams/full-stack-engineer-onboarding.md) |
| AI/ML Engineer | [`05-teams/ai-ml-engineer-onboarding.md`](../05-teams/ai-ml-engineer-onboarding.md) |
| AI Research Engineer | [`05-teams/ai-research-engineer-onboarding.md`](../05-teams/ai-research-engineer-onboarding.md) |
| Cloud Platform Engineer | [`05-teams/cloud-platform-engineer-onboarding.md`](../05-teams/cloud-platform-engineer-onboarding.md) |
| DevOps Engineer | [`05-teams/devops-engineer-onboarding.md`](../05-teams/devops-engineer-onboarding.md) |
| Quality Engineer | [`05-teams/quality-engineer-onboarding.md`](../05-teams/quality-engineer-onboarding.md) |
| Product Manager | [`05-teams/product-manager-onboarding.md`](../05-teams/product-manager-onboarding.md) |
| UX Designer | [`05-teams/ux-designer-onboarding.md`](../05-teams/ux-designer-onboarding.md) |
| Sales Representative | [`05-teams/sales-representative-onboarding.md`](../05-teams/sales-representative-onboarding.md) |
| Customer Support Engineer | [`05-teams/customer-support-engineer-onboarding.md`](../05-teams/customer-support-engineer-onboarding.md) |
| HR Specialist | [`05-teams/hr-specialist-onboarding.md`](../05-teams/hr-specialist-onboarding.md) |
| Finance Analyst | [`05-teams/finance-analyst-onboarding.md`](../05-teams/finance-analyst-onboarding.md) |

## Compensation Bands (Fictional)

Compensation bands are maintained by HR Operations and reviewed annually. Indicative ranges (fictional, India market):

| Level | Backend / Frontend | AI/ML | Sales Base | UX |
|-------|--------------------|-------|------------|-----|
| L3 | INR 18–25 LPA | INR 20–28 LPA | INR 15–22 LPA | INR 16–22 LPA |
| L4 | INR 25–38 LPA | INR 28–42 LPA | INR 22–32 LPA | INR 22–32 LPA |
| L5 | INR 38–55 LPA | INR 42–62 LPA | INR 32–48 LPA | INR 32–45 LPA |
| L6 | INR 55–80 LPA | INR 62–90 LPA | INR 48–70 LPA | INR 45–65 LPA |

Bands for London and Seattle are maintained separately in the HR system.

## Related Documents

- [`00-company/mission-and-values.md`](../00-company/mission-and-values.md)
- [`05-teams/`](../05-teams/)
- [`01-hr/performance-review-policy.md`](./performance-review-policy.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
