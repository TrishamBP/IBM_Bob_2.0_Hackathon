---
document_id: ACME-PROD-004
title: ACME Workspace Product Overview
category: product
department: workspace-bu
applicable_roles: [all]
owner: Product Management
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [product, workspace, overview]
---

# ACME Workspace Product Overview

ACME Workspace is the company's enterprise productivity and collaboration suite. It combines documents, spreadsheets, video meetings, and project tracking in a single application. The product is sold per-seat to enterprises and is the broadest of ACME's three products in terms of user base.

## Business Purpose

Customers use ACME Workspace to replace the patchwork of separate productivity tools that most enterprises accumulate. The promise to customers: a single application where employees can draft documents, model data in spreadsheets, run meetings, and track projects — without exporting their data to multiple vendors.

## Intended Users

- **Knowledge workers** — documents, spreadsheets, project tracking.
- **Meeting organizers** — video meetings, agendas, notes, action items.
- **Project managers** — cross-functional planning, status, reporting.
- **IT administrators** — user lifecycle, data governance, audit.
- **End-user support** — helpdesk staff supporting the broader Workspace user base.

## Major Capabilities

| Capability | Description |
|------------|-------------|
| Documents | Rich-text collaborative documents with comments and revision history. |
| Spreadsheets | Multi-sheet workbooks with formulas, charts, and scripts. |
| Video meetings | Scheduled and ad-hoc meetings with recording, transcription, and captions. |
| Calendar | Personal and team calendars, room booking. |
| Project tracking | Kanban, list, timeline, and dashboard views. |
| Workflow automation | Trigger-based automations across documents, spreadsheets, and project items. |
| Admin console | User lifecycle, data classification, audit, eDiscovery. |
| Integration APIs | REST and webhook APIs for customer-side integrations. |

## System Components

| Component | Description | Owning Repository |
|-----------|-------------|-------------------|
| Workspace Web | Customer-facing single-page application | `acme-workspace-web` |
| Workspace API | Multi-tenant backend API for documents, sheets, projects, meetings | `acme-workspace-api` |
| Real-time collaboration | Operational transform service for live co-editing | `acme-workspace-api` (subpackages) |
| Media service | Video, audio, recording, transcription | `acme-workspace-api` (subpackages) |
| Admin service | User lifecycle, audit, eDiscovery | `acme-workspace-api` (subpackages) |
| Workflow engine | Trigger evaluation and execution | `acme-workspace-api` (subpackages) |
| Observability collector | Shared telemetry ingestion | `acme-platform-infrastructure` |

## Owning Teams

- **Product:** Elena Petrova (Product Lead), reporting to Daniel Coelho (CPO).
- **Workspace Web:** Thomas Buckley (EM), reporting to Sridhar Venkatesh (CTO).
- **Workspace API:** Priya Menon (EM), reporting to Sridhar Venkatesh.
- **Platform (shared):** Nikhil Joshi (Manager), reporting to Sridhar Venkatesh.
- **Design:** Sara Lindberg's UX team.

See [`00-company/organizational-structure.md`](../00-company/organizational-structure.md) and [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md).

## How Your Work Connects

- If you are joining **Workspace Web**, your work is in `acme-workspace-web`. You will likely work on the customer-facing single-page application — documents, spreadsheets, project tracking, video meeting UI.
- If you are joining **Workspace API**, your work is in `acme-workspace-api`. You will likely work on the multi-tenant backend — REST API, real-time collaboration, media service, admin and workflow engine.
- If you are joining **Platform Infrastructure**, your work crosses all products — see [`06-product/acme-cloud-overview.md`](./acme-cloud-overview.md) for context on the shared platform.

## Customer-Facing URLs (Fictional)

| Surface | URL (fictional) |
|---------|-----------------|
| Workspace app | workspace.acme.example |
| Workspace status | status.acme.example/workspace |
| Workspace docs | docs.acme.example/workspace |
| Workspace API | api.workspace.acme.example |

## Related Documents

- [`06-product/product-catalog.md`](./product-catalog.md)
- [`06-product/acme-cloud-overview.md`](./acme-cloud-overview.md)
- [`06-product/acme-intelligence-overview.md`](./acme-intelligence-overview.md)
- [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md)
- [`00-company/products-and-business-units.md`](../00-company/products-and-business-units.md)
