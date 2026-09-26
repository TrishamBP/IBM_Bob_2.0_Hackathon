---
document_id: ACME-TRN-006
title: AI Coding Assistant Usage
category: training
department: engineering
applicable_roles: [backend-engineer, frontend-engineer, full-stack-engineer, cloud-platform-engineer, devops-engineer, ai-ml-engineer, ai-research-engineer, quality-engineer, customer-support-engineer, engineering-managers]
owner: Engineering Enablement
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [training, ai, copilot, github-copilot, acceptable-use]
---

# AI Coding Assistant Usage (ACME-TRN-006)

> Fictional document. All systems, links, and addresses are illustrative.

## 1. Module Overview

The AI Coding Assistant Usage module governs how ACME engineers use the company's approved AI tool, GitHub Copilot Business, and any future AI coding assistants that pass the ACME security review. The module covers eligibility and approval flow, SSO installation, the features that are enabled in the ACME tenancy, the organisation-level restrictions, repository-specific instructions, completion and chat usage, unit test generation, AI-assisted code review, the handling of proprietary code and sensitive data, and the human-in-the-loop review obligations.

The module is owned by Engineering Enablement in partnership with the Director AI/ML (Anitha Rajan, `anitha.rajan@acme.example`) and the CISO office (Rajan Mehta, `rajan.mehta@acme.example`). It is mandatory for any engineer with an assigned Copilot Business license and recommended for all engineers regardless of license status.

## 2. Learning Objectives

By the end of this module, the learner will be able to:

1. Determine whether they are eligible for a Copilot Business license and complete the approval flow via [`../08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md).
2. Install and authenticate GitHub Copilot Business via SSO against `git.acme.example` and configure the IDE extension per [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md).
3. List the ACME tenancy-level restrictions (block list, allow list, prompt filter, telemetry scope) and explain why each exists.
4. Use Copilot Chat, inline completion, and PR-summary features safely, including applying repository-specific instructions files (`.github/copilot-instructions.md`).
5. Identify proprietary code, secrets, customer data, and other content that must never be pasted into an AI assistant, and demonstrate the safe alternative.
6. Apply the human-in-the-loop review obligation: every AI-suggested change is reviewed by a human before merge, with a focus on correctness, security, license, and attribution.

## 3. Target Audience

| Role | Required? | Notes |
|---|---|---|
| Engineers with an assigned Copilot Business license | **Mandatory** | Gates license activation; revokes the license if not completed within 14 days. |
| Engineers without a Copilot license | Recommended | A 45-minute condensed version covers acceptable-use rules without hands-on installation. |
| Engineering Managers / Tech Leads | **Mandatory** | Plus the manager supplement on seat allocation and cost review. |
| Customer Support Engineers (Copilot for PRs only) | **Mandatory** | Reduced scope: PR-summary and chat only; no inline completion. |
| Non-engineers (PM, HR, Sales) | Optional | A 30-minute "AI tools awareness" briefing covers acceptable use for non-code work. |

## 4. Prerequisites

- Completion of [`security-awareness.md`](./security-awareness.md) (ACME-TRN-002) — gating.
- Acknowledgement of the AI tool acceptable use policy — see [`../03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) — recorded via [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md).
- Developer workstation setup complete — see [`../04-engineering/developer-workstation-setup.md`](../04-engineering/developer-workstation-setup.md).
- AI coding assistant setup completed — see [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md).
- For hands-on completion: Copilot Business license assigned via [`../08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md).

## 5. Duration

**Total: 2 hours**, all self-paced in `wiki.acme.example`.

| Block | Duration | Modality |
|---|---|---|
| Eligibility, approval flow, SSO install | 20 min | Self-paced |
| Enabled features & organisation restrictions | 25 min | Self-paced |
| Repository-specific instructions & Copilot Chat | 25 min | Self-paced |
| Unit test generation & PR summaries | 20 min | Self-paced |
| Proprietary code, sensitive data, secrets | 15 min | Self-paced |
| Human-in-the-loop review & attribution | 5 min | Self-paced |
| Acknowledgement + 10-question quiz | 10 min | Self-paced |

## 6. Outline of Topics Covered

### Block A — Eligibility, Approval Flow, SSO Install (20 min)

- Who is eligible: engineers with manager approval, on a product engineering team, with security training complete.
- Approval flow: engineer submits [`../08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md); manager approves; Director AI/ML (Anitha Rajan) countersigns for seats exceeding 100 per quarter; IT Onboarding (Geetha Iyer) provisions the seat in `git.acme.example`.
- SSO installation: install the IDE extension, sign in with your `@acme.example` Entra ID, accept the organisation prompt; never use a personal GitHub account.
- Reference: [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md).

### Block B — Enabled Features & Organisation Restrictions (25 min)

- Enabled: inline completions, Copilot Chat, PR summaries, code explanations, test scaffolding, docstring generation.
- Restricted: Copilot Workspace (autonomous agent mode) is disabled pending security review.
- Block list: prompts containing secrets, customer data, or restricted-classified content are blocked by the prompt filter and logged.
- Allow list: only `git.acme.example` repositories under approved organisations.
- Telemetry scope: prompt content is not retained beyond 30 days; suggestions telemetry is retained for product improvement; see [`../03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md).

### Block C — Repository-Specific Instructions & Copilot Chat (25 min)

- Per-repo `.github/copilot-instructions.md` files: how ACME seeds them, how to maintain them, and how they shape suggestions.
- Copilot Chat usage: scope to the current workspace, use `@workspace` and `#file` references, never paste entire files from other repos.
- Chat etiquette: do not use chat to bypass review; chat outputs are suggestions, not decisions.
- Examples drawn from `acme-shared-libraries` and `acme-cloud-api`.

### Block D — Unit Test Generation & PR Summaries (20 min)

- Generating unit tests: request tests for a single function, review the output against ACME testing philosophy — see [`../04-engineering/practices/unit-and-integration-testing.md`](../04-engineering/practices/unit-and-integration-testing.md).
- Generating PR summaries: use the PR-summary feature to draft the description, then edit; never auto-submit.
- Quality engineering collaboration with `acme-quality-automation` fixtures.

### Block E — Proprietary Code, Sensitive Data, Secrets (15 min)

- Never paste into Copilot Chat: secrets (see [`../03-security/secrets-management.md`](../03-security/secrets-management.md)), customer data (see [`../03-security/customer-data-handling.md`](../03-security/customer-data-handling.md)), source code from third parties without license clearance (see [`../03-security/open-source-dependency-security.md`](../03-security/open-source-dependency-security.md)).
- Repository boundaries: do not paste code from one ACME repo into a chat scoped to a different repo if the repos are in different business units.
- Screenshot/PDFs of internal architecture diagrams: prohibited.

### Block F — Human-in-the-Loop Review & Attribution (5 min)

- Every AI-suggested change is reviewed by a human author before commit.
- Authorship: the engineer who merges the PR is the author of record; AI is a tool, not an author.
- Attribution: if an AI suggestion contributed substantially, note it in the PR description.
- Reference: [`../04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md).

### Block G — Acknowledgement + Quiz (10 min)

- Acknowledge the AI tool acceptable use policy.
- 10-question quiz on eligibility, restrictions, sensitive data, and review obligations.

## 7. Format

**Self-paced.** All content is in `wiki.acme.example`; the acknowledgement and quiz are in `hr.acme.example`. A monthly live Q&A clinic is hosted by the Engineering Enablement lead and the AI/ML Director's office.

## 8. Completion Criteria

- All six content blocks marked `COMPLETED` in the LMS.
- Acknowledgement of the AI tool acceptable use policy — see [`../03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) — recorded via [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md).
- 10-question quiz score **≥ 80%** (≥ 8 of 10 correct). Retakes are unlimited but logged.
- [`../08-forms/training-completion.md`](../08-forms/training-completion.md) submitted and signed off by Engineering Enablement.
- If the learner fails to complete within 14 days of license assignment, the Copilot seat is revoked and re-assigned only after completion.

## 9. Follow-up / Next Steps

- The Copilot Business license is now fully active; the engineer may use Copilot in any repository in the allow list.
- Annual recertification: a 30-minute refresher plus a 5-question quiz, scheduled 11 months after completion.
- The CISO office runs a quarterly AI-tool audit; engineers may be sampled for a usage review.
- Engineers may submit `.github/copilot-instructions.md` improvements via PR to their repo's `CODEOWNERS`.

## 10. Trainer / Owner

| Role | Person | Responsibility |
|---|---|---|
| Module owner | Aditi Ghosh, Engineering Enablement lead (`aditi.ghosh@acme.example`) | Content strategy, clinic hosting, annual review. |
| AI/ML content co-owner | Anitha Rajan, Director AI/ML (`anitha.rajan@acme.example`) | Feature review, restriction list sign-off, seat allocation oversight. |
| Security content co-owner | Rajan Mehta, CISO (`rajan.mehta@acme.example`) | Restriction list, telemetry scope, audit oversight. |
| License provisioning | Geetha Iyer, IT Onboarding Specialist (`geetha.iyer@acme.example`) | Seat assignment, revocation. |
| LMS coordinator | Anjali Iyer, Training Operations (`anjali.iyer@acme.example`) | Tracking, sign-off. |

Escalation contacts are in [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md). Glossary terms are in [`../metadata/glossary.md`](../metadata/glossary.md).
