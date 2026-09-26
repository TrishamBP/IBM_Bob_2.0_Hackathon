---
document_id: ACME-META-001
title: ACME Corp Glossary
category: metadata
department: all
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [glossary, terms, acronyms, canonical]
---

# ACME Corp Glossary

This glossary defines company-specific terms, systems, and acronyms used across the ACME Corp onboarding library. New employees should skim it on day one; refer back as needed.

## Company-Specific Terms

| Term | Definition |
|------|------------|
| ACME Cloud | Multi-cloud management platform. See [`06-product/acme-cloud-overview.md`](../06-product/acme-cloud-overview.md). |
| ACME Intelligence | Enterprise AI platform. See [`06-product/acme-intelligence-overview.md`](../06-product/acme-intelligence-overview.md). |
| ACME Workspace | Productivity and collaboration suite. See [`06-product/acme-workspace-overview.md`](../06-product/acme-workspace-overview.md). |
| ACME Portal | Employee intranet at `portal.acme.example` (fictional). |
| ACME Hub | HR self-service at `hr.acme.example` (fictional). |
| ACME Vault | Internal secrets and credential store at `vault.acme.example` (fictional). |
| ACME Package | Internal package registry at `packages.acme.example` (fictional). |
| ACME Wiki | Knowledge base at `wiki.acme.example` (fictional). |
| ACME Status | Status pages at `status.acme.example` (fictional). |
| ACME Helpdesk | IT ticketing at `helpdesk.acme.example` (fictional). |
| HRBP | HR Business Partner — an HR specialist paired with each engineering team. |
| EM | Engineering Manager — owns a team and its repositories. |
| Buddy | Onboarding buddy — a peer assigned to support a new hire's first 90 days. |
| OKR | Objectives and Key Results — ACME's quarterly goal framework. |
| SEV1 / SEV2 / SEV3 | Incident severity levels (1 = highest). See [`04-engineering/incident-response-and-on-call-introduction.md`](../04-engineering/practices/incident-response-and-on-call-introduction.md). |
| On-call | The engineer currently responsible for responding to incidents for a team. |
| GRC | Governance, Risk, and Compliance — a function within Information Security. |
| SOC | Security Operations Center — the team that monitors and responds to security events. |
| IAM | Identity and Access Management. |
| RBAC | Role-Based Access Control. |
| ABAC | Attribute-Based Access Control. |
| JIT | Just-In-Time access — temporary elevated access for a specific task. |
| PR | Pull Request — the unit of code review at ACME. |
| CODEOWNERS | File in a repo declaring which teams own which paths. |
| IaC | Infrastructure as Code — typically Terraform or Bicep at ACME. |
| FinOps | Cloud financial operations practice — managing cloud spend. |
| RAG | Retrieval-Augmented Generation — combining a language model with retrieval over a corpus. |
| Guardrails | PII redaction, prompt-injection defenses, output content filters used in ACME Intelligence. |
| BYOD | Bring Your Own Device. See [`03-security/byod-policy.md`](../03-security/byod-policy.md). |
| MDM | Mobile Device Management — at ACME, Microsoft Intune. |
| EDR | Endpoint Detection and Response — at ACME, Microsoft Defender for Endpoint. |
| DLP | Data Loss Prevention — at ACME, Microsoft Purview. |
| SSO | Single Sign-On — at ACME, Microsoft Entra ID. |
| MFA | Multi-Factor Authentication — at ACME, Microsoft Authenticator. |
| L1 / L2 / L3 | Support tiers (1 = first line, 3 = deepest engineering). |
| TDD | Test-Driven Development. |
| CI / CD | Continuous Integration / Continuous Delivery. |
| SLO / SLI / SLA | Service-Level Objective / Indicator / Agreement. |
| Runbook | A documented procedure for operating a service, especially during incidents. |
| Design Doc | A pre-implementation document describing a non-trivial change. |
| RFC | Request for Comments — a circulated design document for feedback. |
| Code freeze | A period during which deploys to production are restricted (e.g., during a holiday). |
| Hotfix | An urgent fix applied outside the normal release cadence. |
| Buddy review | A non-blocking review from a peer, distinct from a formal CODEOWNERS review. |
| Onboarding plan | The 30/60/90-day plan a manager creates for a new hire. |
| Preboarding | Activities that happen between offer acceptance and start date. |
| Offboarding | Activities that happen between resignation and final day. |

## Acronyms — Common (Non-ACME-Specific)

The following acronyms appear in the library and are included here for completeness. They are industry-standard terms, not ACME-specific.

| Acronym | Definition |
|---------|------------|
| API | Application Programming Interface |
| AWS | Amazon Web Services |
| Azure | Microsoft Azure |
| GCP | Google Cloud Platform |
| CPU / GPU | Central Processing Unit / Graphics Processing Unit |
| CSV / JSON / YAML | Common data/serialization formats |
| DNS | Domain Name System |
| HTTP / HTTPS | HyperText Transfer Protocol (Secure) |
| IDE | Integrated Development Environment |
| JSON | JavaScript Object Notation |
| KPI | Key Performance Indicator |
| MCP | Model Context Protocol (used by AI tooling integrations) |
| OS | Operating System |
| PDF / DOCX / XLSX | Document formats |
| PII | Personally Identifiable Information |
| REST | Representational State Transfer |
| SDK | Software Development Kit |
| SSH | Secure Shell |
| SSL / TLS | Secure Sockets Layer / Transport Layer Security |
| UI / UX | User Interface / User Experience |
| URL | Uniform Resource Locator |
| VPN | Virtual Private Network |
| WSL2 | Windows Subsystem for Linux, version 2 |
| XML | Extensible Markup Language |

## Related Documents

- [`metadata/document-index.md`](./document-index.md)
- [`README.md`](../README.md)
- [`00-company/company-profile.md`](../00-company/company-profile.md)
