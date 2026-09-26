---
document_id: ACME-TEAM-010
title: ACME Corp UX Designer Onboarding
category: team-onboarding
department: ux-design
applicable_roles: [ux-designer]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [team-onboarding, ux-designer]
---

# ACME Corp UX Designer Onboarding

Welcome to the **UX and Design** organization at ACME Corp. This guide is your single reference for the first 90 days as a UX Designer building the customer experience for ACME's three product lines. It assumes you have already completed [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md) and [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md).

> ACME Corp is a fictional company. All names, repositories, hosts, and systems referenced here are illustrative and use the `.example` domain. Do not attempt to reach any URL.

## 1. Team Overview

| Field | Value |
|-------|-------|
| Team name | UX and Design |
| Reports up to | Sara Lindberg (Director UX), who reports to the CEO/CTO office |
| Primary offices | London (Sara's home office), with designers distributed across Seattle, Bengaluru, Hyderabad |
| Primary products | ACME Cloud, ACME Intelligence, ACME Workspace — see product overviews |
| Primary tooling | Figma (design files), Maze (usability testing), Dovetail (research repository), Storybook (design system reference), Confluence (design specs) |
| Primary channel | `#ux-design` (Microsoft Teams) |

**Mission.** Drive user research, interaction design, visual design, and design-system stewardship for ACME's three product lines. Designers partner with PMs and engineering to ship customer experiences that are usable, accessible, on-brand, and consistent across products.

**Charter.** Owns user research, design specs, prototypes, the ACME design system, accessibility standards, and usability testing. Does **not** own product strategy (PM owns that), engineering implementation (engineering owns that), or brand marketing (Marketing owns that).

**Customers.** End users at customer organizations (direct research), PMs and engineering (internal partners), ACME Sales (demo design partners), ACME Support (self-service UX for support flows).

## 2. Reporting Manager

- **Director:** Sara Lindberg (sara.lindberg@acme.example, London office, hybrid).
- Sara reports to the CEO/CTO office.
- Your standing 1:1 is 30 minutes weekly.
- Reporting line is recorded at `hr.acme.example` under your profile.
- You will also be assigned to one of three product line sub-teams (Cloud, Intelligence, or Workspace) and will work day-to-day with that product line's PM and engineering teams.

## 3. Onboarding Buddy

- **Buddy:** Sara Lindberg (sara.lindberg@acme.example, Director UX), serves as your buddy for the first 90 days as the UX team is small and Sara partners directly with all new designers.
- Sara is your peer mentor for the first 90 days — Figma conventions, design-system contribution patterns, research workflow, cross-functional collaboration patterns.
- Buddy commitment: 2 hours per week (two 1-hour sessions) for the first 6 weeks; one 1-hour session per week for weeks 7–12; ad-hoc thereafter.
- See [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md) for the buddy program's expectations.

## 4. Required Documents (Week 1)

Read each of the following in your first week. Sara will check progress during your week-1 1:1.

- [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md)
- [`00-company/employee-handbook.md`](../00-company/employee-handbook.md)
- [`00-company/organizational-structure.md`](../00-company/organizational-structure.md)
- [`00-company/communication-guidelines.md`](../00-company/communication-guidelines.md)
- [`00-company/products-and-business-units.md`](../00-company/products-and-business-units.md)
- [`03-security/information-security-policy.md`](../03-security/information-security-policy.md)
- [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md)
- [`03-security/customer-data-handling.md`](../03-security/customer-data-handling.md)
- [`06-product/acme-cloud-overview.md`](../06-product/acme-cloud-overview.md)
- [`06-product/acme-intelligence-overview.md`](../06-product/acme-intelligence-overview.md)
- [`06-product/acme-workspace-overview.md`](../06-product/acme-workspace-overview.md)
- [`04-engineering/repositories/acme-cloud-frontend.md`](../04-engineering/repositories/acme-cloud-frontend.md) (read-only — design implementation context)
- [`04-engineering/repositories/acme-workspace-web.md`](../04-engineering/repositories/acme-workspace-web.md)
- [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md)
- [`10-training/product-training.md`](../10-training/product-training.md)

## 5. Required Software

Install only the approved tools below. Anything else requires a software access request via [`08-forms/software-access-request.md`](../08-forms/software-access-request.md). See [`02-it/approved-software-installation.md`](../02-it/approved-software-installation.md) for the binding policy.

**Workstation baseline (installed by IT before Day 1):**
- macOS 14+ preferred (design work); Windows 11 Enterprise acceptable
- Microsoft 365 — Outlook, Teams, OneDrive, Word, PowerPoint
- Microsoft Authenticator, Corporate VPN, 1Password, Microsoft Defender for Endpoint

**Designer-specific tools (provisioned via Entra SSO):**
- Figma (design files) — `Editor` seat at `figma.internal.acme.example`
- Figma Make / variables plugin (auto-installed)
- Maze (usability testing) — `Researcher` seat at `maze.internal.acme.example`
- Dovetail (research repository) — `Researcher` seat at `dovetail.internal.acme.example`
- Storybook (internal) — read with Entra SSO at `storybook.internal.acme.example`
- Confluence (design specs) — `Editor` for the design space
- GitHub Enterprise (read-only — see sections 6 and 7)

## 6. Approved AI Tools

Per the role eligibility matrix in [`04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md), UX Designers are **not entitled** to AI coding tools:

| Tool | Entitlement | Notes |
|------|-------------|-------|
| GitHub Copilot Business | **No** | Designers do not write production code and do not receive a Copilot seat. Do not request one via [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md) — it will be declined. |
| Internal ACME Intelligence sandbox | **No** | Not provisioned. |

If you need AI assistance for writing (research summaries, design specs, internal docs), use Microsoft Copilot for Microsoft 365, governed by [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md). Figma's built-in AI features are governed by Figma enterprise policy and the ACME acceptable-use policy.

## 7. Required Repositories

You will be granted **read-only** access to ACME's frontend repositories per the access tier matrix in [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md):

- `acme-cloud-frontend` — Cloud Console (TypeScript, React)
- `acme-workspace-web` — Workspace web frontend (TypeScript, React, WebRTC)

Read-only cross-repo access (auto-granted for design implementation context):

- `acme-shared-libraries` — read-only access to the design-tokens package.

You will **not** receive access to backend repositories (`acme-cloud-api`, `acme-workspace-api`, `acme-intelligence-*`, `acme-platform-infrastructure`, `acme-quality-automation`) — those have no design-relevant content and are restricted per [`03-security/least-privilege-access.md`](../03-security/least-privilege-access.md).

Repository access is requested via [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md). Sara pre-approves the bulk read-only bundle.

Your repo access is for:

- Reading Storybook stories and component docs in `docs/` folders
- Reviewing PR descriptions and screenshots (to verify design implementation)
- Filing design-bug issues (you can create issues but not PRs)

## 8. Required Access Permissions

On Day 1, IT Onboarding (Geetha Iyer, `geetha.iyer@acme.example) provisions the following Entra ID groups. Verify each in the My Apps portal at `myapps.acme.example`.

| Entra ID group | Purpose |
|----------------|---------|
| `UX-Design` | Membership in the UX org; Figma, Maze, Dovetail seats. |
| `ENG-Cloud-Frontend-Read` | Read-only access to `acme-cloud-frontend`. |
| `ENG-Workspace-Web-Read` | Read-only access to `acme-workspace-web`. |
| `ENG-Shared-Libraries-Read` | Read-only access to `acme-shared-libraries` (design tokens). |
| `Storybook-Editor` | Editor access to the internal Storybook for design-system updates. |
| `Customer-Interview-Tooling` | Access to the customer interview platform at `research.internal.acme.example`. |

Additional tools (auto-provisioned):

- **Figma** — `Editor` seat for the ACME enterprise org.
- **Confluence** — `Editor` for the `UX` and `Design-System` spaces.

Production cloud, cluster, and Vault access is **not** granted.

## 9. Training Requirements

Complete the following training in your first 30 days. All training is tracked in your learning transcript at `hr.acme.example/learning`.

| Course | Link | Deadline |
|--------|------|---------|
| Company Orientation | [`10-training/company-orientation.md`](../10-training/company-orientation.md) | Week 1 |
| Security Awareness | [`10-training/security-awareness.md`](../10-training/security-awareness.md) | Week 1 |
| Privacy Awareness | [`10-training/privacy-awareness.md`](../10-training/privacy-awareness.md) | Week 1 (high priority — you handle research data) |
| Product Training (all three products) | [`10-training/product-training.md`](../10-training/product-training.md) | Week 2 |
| Engineering Orientation | [`10-training/engineering-orientation.md`](../10-training/engineering-orientation.md) | Week 2 (read-only — understand engineering workflow) |
| Git and Repository Workflows | [`10-training/git-and-repository-workflows.md`](../10-training/git-and-repository-workflows.md) | Week 3 (read-only — understand how to file design-bug issues) |
| Cloud Platform Fundamentals | [`10-training/cloud-platform-fundamentals.md`](../10-training/cloud-platform-fundamentals.md) | Week 4 (so you can speak credibly about ACME's platform) |
| Workplace Conduct | [`10-training/workplace-conduct.md`](../10-training/workplace-conduct.md) | Week 4 |

Additional role-specific training delivered by Sara in weeks 2–4:
- "ACME design system" walkthrough (2 hours).
- "Research repository (Dovetail) conventions" workshop (1 hour).
- "Usability testing with Maze" workshop (1 hour).
- "Accessibility standards at ACME" briefing by accessibility lead (1 hour).

## 10. First-Week Activities

- **Day 1:** IT activation (M365, Authenticator, laptop). Read [`00-company/welcome-to-acme.md`](../00-company/welcome-to-acme.md). Manager intro 1:1 with Sara. Meet your product line partner PM.
- **Day 2:** Tour Figma, Maze, Dovetail, Storybook. Read the ACME design system in Figma. Read the latest two design specs in your product line's Confluence space.
- **Day 3:** Shadow a user research session. Sara will schedule you as a silent observer on a usability test or interview. Read [`03-security/customer-data-handling.md`](../03-security/customer-data-handling.md) for research-data rules.
- **Day 4:** Meet the frontend Tech Lead(s) of the team(s) you will partner with. Read their Storybook stories and the latest component docs. Read [`04-engineering/repositories/acme-cloud-frontend.md`](../04-engineering/repositories/acme-cloud-frontend.md) or the Workspace equivalent.
- **Day 5:** Pick a small design-system contribution (e.g., a missing token, an accessibility improvement to a component) and prototype it in Figma. Review with Sara.

## 11. First-Month Deliverables

1. **Shadowed at least 3 user research sessions** — usability tests, interviews, or contextual inquiries. Log observations in Dovetail.
2. **Authored first design spec** — a small feature spec (problem, flows, wireframes, accessibility notes) reviewed by Sara and the partner PM.
3. **Met all engineering counterparts** — at least one frontend Tech Lead and one EM per team you will partner with.
4. **Tour of all designer tooling complete** — Figma, Maze, Dovetail, Storybook, Confluence, GitHub read-only.
5. **Completed all Week 1–4 training** in section 9 plus the role-specific workshops.
6. **First design-system contribution** — a token, variant, or component improvement, reviewed by Sara and merged by the frontend team.

## 12. 30/60/90-Day Expectations

| Window | Expectation |
|--------|-------------|
| **30 days** | Tooling setup complete. Shadow 3 research sessions. Draft first design spec. Meet all engineering counterparts. Complete security, privacy, product, and design-system training plus role-specific workshops. |
| **60 days** | Own a small feature design end-to-end (problem framing with PM → flows → wireframes → hi-fi → usability test → handoff to engineering). Present the design in engineering's design review. Begin attending customer research sessions as a participant (not just observer). Run your first usability test independently (with Sara reviewing the script and results). |
| **90 days** | Own a feature-cluster (multiple screens or a feature area with multiple components) end-to-end. Lead a design-system contribution (a new component, a token rework, or an accessibility improvement to a high-traffic area). Co-present at the monthly UX review to Sara and the broader design org. Begin mentoring the next new hire (informal). |

## 13. Team Meetings

| Meeting | Cadence | Owner | Your role |
|---------|---------|-------|-----------|
| UX org standup | 15 min, 10:00 GMT | Sara Lindberg | Attend |
| Product line design sync (Cloud / Intelligence / Workspace) | 30 min, weekly | Your product line PM | Attend |
| Sprint review & retro (with engineering) | 60 min, every other Friday | Your partner EM | Attend; demo design impact |
| 1:1 with manager | 30 min, weekly | Sara Lindberg | Career, blockers, feedback |
| 1:1 with buddy (also Sara) | 1 hour, twice weekly for first 6 weeks | Sara Lindberg | Questions, peer feedback |
| 1:1 with partner PM | 30 min, weekly | Your partner PM | Discovery and prioritization |
| Design review | 60 min, weekly | Sara Lindberg | Present your specs |
| Research review (cross-product) | 60 min, biweekly | Sara Lindberg | Present your research findings |
| All-hands | 60 min, monthly | Sridhar Venkatesh | Attend |

## 14. Escalation Contacts

Use the following contacts in priority order. See [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for the full directory.

| Need | Contact | How |
|------|---------|-----|
| Design / design-system / research question | Buddy & Director: Sara Lindberg (sara.lindberg@acme.example) | 1:1 or Teams DM |
| Product / discovery question | Your partner PM | 1:1 or product line channel |
| Engineering handoff / implementation question | Your partner frontend Tech Lead (Cloud: Rahul Menon; Workspace: Hannah Park) | Teams DM or product line channel |
| HR / leave / payroll / policy | HRBP: Kavya Krishnan (kavya.krishnan@acme.example) — covers Workspace and Cloud (UX is bundled with Cloud/Workspace HRBP) | `hr.acme.example`, then Teams DM |
| IT (laptop, VPN, M365, software) | IT Helpdesk | `helpdesk.acme.example` or `#it-helpdesk` |
| Customer / research data privacy question | Privacy Office + CISO designate | `privacy@acme.example` |
| Security incident or suspected breach | SOC + CISO Rajan Mehta | `soc@acme.example` + 24/7 hotline in [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md) |
| Accessibility escalation | Accessibility lead (via Sara) | `#ux-design` or email Sara |
| Brand / marketing alignment | Marketing Director (via Sara) | Email Sara to route |

## Related Documents

- [`07-workflows/first-day-onboarding.md`](../07-workflows/first-day-onboarding.md)
- [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md)
- [`07-workflows/first-30-days.md`](../07-workflows/first-30-days.md)
- [`07-workflows/first-60-days.md`](../07-workflows/first-60-days.md)
- [`07-workflows/first-90-days.md`](../07-workflows/first-90-days.md)
- [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md)
- [`08-forms/software-access-request.md`](../08-forms/software-access-request.md)
- [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- [`metadata/glossary.md`](../metadata/glossary.md)
