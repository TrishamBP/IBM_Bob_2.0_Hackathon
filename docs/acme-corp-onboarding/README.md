---
document_id: ACME-README-000
title: ACME Corp Onboarding Library
category: index
department: all
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [index, onboarding, navigation]
---

# ACME Corp Onboarding Library

Welcome to the **ACME Corp Onboarding Library**, the canonical knowledge base for new employees, hiring managers, IT operators, security officers, and onboarding buddies. This library covers the full lifecycle of an employee's journey at ACME Corp — from preboarding through day one, week one, the first 90 days, and ultimately offboarding.

This is a **fictional demonstration knowledge base**. All company names, employee identities, contact details, systems, repositories, credentials, asset identifiers, policies, and projects are fictional and intended for illustration, training, search-and-retrieval testing, RAG evaluation, and AI assistant validation. Nothing in this library is real legal, tax, financial, or operational advice.

## About ACME Corp

- **Industry:** Enterprise software, cloud computing, AI and developer tools
- **Headquarters:** Hyderabad, India
- **Other offices:** Bengaluru, London, Seattle
- **Employees:** Approximately 3,500
- **Working model:** Hybrid and remote
- **Primary technology environment:** Microsoft-oriented enterprise
- **Products:** ACME Cloud, ACME Intelligence, ACME Workspace

See [`00-company/company-profile.md`](./00-company/company-profile.md) for the full profile.

## Library Structure

| Directory | Purpose |
|-----------|---------|
| `00-company/` | Welcome, mission, products, org structure, handbook, support |
| `01-hr/` | Employment letters, forms, policies, conduct, performance |
| `02-it/` | IT onboarding, device setup, M365, VPN, support |
| `03-security/` | Security policies, data classification, IAM, AI tool use |
| `04-engineering/` | Developer workstation, AI assistant, repositories, engineering practices |
| `05-teams/` | Role-specific onboarding guides |
| `06-product/` | Product overviews for ACME Cloud, Intelligence, Workspace |
| `07-workflows/` | Preboarding → day 90, IT provisioning, security training, etc. |
| `08-forms/` | Fillable Markdown templates for HR, IT, access, feedback |
| `09-contacts/` | HR, IT, security, engineering, facilities contacts |
| `10-training/` | Orientation, security, privacy, engineering, product training |
| `11-faq/` | Common HR, IT, engineering, security, onboarding questions |
| `12-offboarding/` | Departure, equipment return, knowledge transfer |
| `metadata/` | Document index, glossary, validation report |

## How to Use This Library

1. **If you are a new employee:** Start with [`00-company/welcome-to-acme.md`](./00-company/welcome-to-acme.md), then follow [`07-workflows/first-day-onboarding.md`](./07-workflows/first-day-onboarding.md).
2. **If you are a hiring manager:** Read [`07-workflows/manager-onboarding-responsibilities.md`](./07-workflows/manager-onboarding-responsibilities.md) and use [`08-forms/manager-approval.md`](./08-forms/manager-approval.md) for access requests.
3. **If you are an IT operator:** Start with [`02-it/new-employee-it-request.md`](./02-it/new-employee-it-request.md) and [`07-workflows/it-provisioning.md`](./07-workflows/it-provisioning.md).
4. **If you are an onboarding buddy:** Use [`05-teams/`](./05-teams/) for your buddy's role and [`07-workflows/first-week-onboarding.md`](./07-workflows/first-week-onboarding.md) for sequencing.
5. **If you are testing a RAG / AI assistant:** Use [`metadata/document-index.md`](./metadata/document-index.md) for the catalog and [`metadata/glossary.md`](./metadata/glossary.md) for term definitions.

## Document Conventions

- Every document starts with a YAML front matter block containing `document_id`, `title`, `category`, `department`, `applicable_roles`, `owner`, `version`, `last_updated`, `review_date`, `status`, `confidentiality`, and `tags`.
- Documents use **relative Markdown links** to one another.
- Task statuses follow a fixed vocabulary: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`.
- All email addresses use the reserved `@example.com` domain.
- All repository URLs use the fictional host `git.acme.example`.

## Disclaimer

This library does **not** constitute real legal, tax, employment, or security guidance. Any document marked "fictional example" must be reviewed and approved by qualified professionals before any real-world use. ACME Corp itself is fictional. The presence of a policy here does not imply legal compliance, regulatory approval, or operational accuracy.
