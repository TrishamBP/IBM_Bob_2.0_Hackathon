---
document_id: ACME-META-004
title: ACME Corp Role to Repository Mapping
category: metadata
department: all
applicable_roles: [all]
owner: Engineering
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [metadata, repository, role-mapping]
---

# ACME Corp Role to Repository Mapping

This mapping documents, per role, which repositories the role is granted access to by default. It is consistent with [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md) and [`04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md). Standing production access is **never** granted by default — see [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).

## Repository Access by Role

| Role | Default Repositories (write) | Read-only Repositories | AI Tool Eligibility |
|------|--------------------------------|------------------------|----------------------|
| Frontend Engineer | acme-cloud-frontend, acme-workspace-web | acme-shared-libraries (read) | Copilot Business (default) |
| Backend Engineer | acme-cloud-api, acme-workspace-api, acme-intelligence-agents, acme-intelligence-inference | acme-shared-libraries (read) | Copilot Business (default) |
| Full Stack Engineer | acme-workspace-web, acme-workspace-api | acme-shared-libraries (read) | Copilot Business (default) |
| AI/ML Engineer | acme-intelligence-agents, acme-intelligence-inference, acme-intelligence-ml | acme-shared-libraries (read) | Copilot Business (default) + ACME Intelligence sandbox (default) |
| AI Research Engineer | acme-intelligence-ml | acme-shared-libraries (read) | Copilot Business (default) + ACME Intelligence sandbox (default) |
| Cloud Platform Engineer | acme-platform-infrastructure, acme-shared-libraries | acme-shared-libraries (read) | Copilot Business (default) |
| DevOps Engineer | acme-platform-infrastructure | acme-shared-libraries (read) | Copilot Business (default) |
| Quality Engineer | acme-quality-automation | acme-shared-libraries (read) | Copilot Business (optional, case-by-case) |
| Product Manager | — | (read-only on all repositories) | Copilot Business (optional, case-by-case); no sandbox |
| UX Designer | — | (read-only on acme-cloud-frontend, acme-workspace-web) | No AI tools by default |
| Sales Representative | — | (no repository access — uses Salesforce) | No AI tools by default |
| Customer Support Engineer | — | (read-only on acme-workspace-web, acme-workspace-api) | No AI tools by default |
| HR Specialist | — | (no repository access — uses HR Hub) | No AI tools by default |
| Finance Analyst | — | (no repository access — uses Oracle ERP) | No AI tools by default |

## How to Request Additional Access

Cross-team repository access requires the [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md) form, with both the hiring EM and the receiving EM approving. Production-deploy access additionally requires GRC analyst review and is granted only via Microsoft Entra ID PIM (time-bound, max 4 hours). See [`04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md) for the full workflow.

## Related Documents

- [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md)
- [`04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md)
- [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md)
- [`03-security/identity-and-access-management.md`](../03-security/identity-and-access-management.md)
- [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md)
- [`05-teams/`](../05-teams/) — per-role onboarding guides
