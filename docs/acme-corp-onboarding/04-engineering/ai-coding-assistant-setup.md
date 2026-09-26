---
document_id: ACME-ENG-015
title: ACME Corp AI Coding Assistant Setup
category: engineering
department: engineering
applicable_roles: [engineers]
owner: Engineering Enablement
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [engineering, ai, copilot, setup, policy]
---

# ACME Corp AI Coding Assistant Setup

This guide describes how to configure an approved AI coding assistant within VS Code at ACME Corp. We use **GitHub Copilot Business** as the primary illustrative tool because it is the most common approved assistant at ACME. Other approved assistants (e.g., an internal ACME Intelligence sandbox) follow a similar approval and onboarding flow.

> This is a fictional policy. The product functionality described here is illustrative of how ACME expects engineers to use an AI assistant; it does not represent official documentation for any third-party product. Always follow the vendor's official documentation for product behavior and consult [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) for the binding ACME policy.

## Eligibility — Who Is Entitled to an AI Assistant

Not every employee is entitled to every AI tool. Licenses are limited and access is governed by role and need. The matrix below shows the default entitlement; specific assignments are made by your hiring EM at offer-acceptance time and recorded in [`07-workflows/preboarding.md`](../07-workflows/preboarding.md).

| Role | GitHub Copilot Business | Internal ACME Intelligence sandbox |
|------|--------------------------|------------------------------------|
| Backend / Frontend / Full Stack Engineer | Yes (default) | Optional |
| AI/ML Engineer | Yes (default) | Yes (default) |
| AI Research Engineer | Yes (default) | Yes (default) |
| Cloud Platform / DevOps Engineer | Yes (default) | Optional |
| Quality Engineer | Optional (case-by-case) | Optional |
| Product Manager | Optional (case-by-case) | No |
| UX Designer | No | No |
| Sales / Customer Support / HR / Finance | No | No |

If you believe your role should have access and it is not listed, your manager may submit an exception request via [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md).

## Manager and IT Approval

Before you install the assistant:

1. Confirm with your hiring EM that a Copilot Business license has been assigned to you in GitHub Enterprise. The license assignment is visible to you as a seat under `https://git.acme.example/organizations/acme/settings/billing/copilot` (fictional URL).
2. If you do not see a seat, your EM must request one via the AI tool intake form ([`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md)). Approval routing is:
   - Hiring EM (auto-approved for default-entitled roles)
   - Engineering Manager of receiving team (if cross-team)
   - CISO or designate (for any AI tool request — confirms compliance with [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md))
3. After approval, IT Onboarding (Geetha Iyer, `geetha.iyer@acme.example`) adds your seat to the GitHub Enterprise organization. You will receive a confirmation email within 1 business day.

## Corporate SSO Authentication

ACME's GitHub Copilot Business deployment is enterprise-managed. Sign-in is via Microsoft Entra ID SSO:

1. In VS Code, open **Accounts** (bottom-left avatar → **Sign in with GitHub to use GitHub Copilot**).
2. Select **Sign in with GitHub Enterprise**.
3. Enter the host: `git.acme.example` (fictional).
4. Your browser opens to the GitHub sign-in page; click **Sign in with Microsoft**.
5. You are redirected to Microsoft Entra ID; sign in with your `@acme.example` credentials and approve the MFA prompt.
6. Authorize the **VS Code Copilot** app.
7. Return to VS Code — the bottom-right Copilot icon should now show as "Signed in as `anika.rao@acme.example`."

> Do **not** sign in with a personal GitHub account. Doing so would route your code suggestions through your personal account, which is forbidden by [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md).

## Installing the Approved Extension

1. Open VS Code.
2. Open the Extensions view (`Ctrl+Shift+X` Windows / `Cmd+Shift+X` macOS).
3. Search for "GitHub Copilot" (the official Microsoft extension).
4. Click **Install**.
5. Search for "GitHub Copilot Chat" and install it as well (this is the chat companion).
6. Reload VS Code if prompted.

Forbidden alternatives: do **not** install third-party AI extensions (e.g., Codeium, Tabnine, Continue) unless they are on the approved list in [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md). Installing an unapproved extension may trigger an automatic alert to the SOC and a 1:1 with your manager.

## Signing into the Enterprise Account

See the SSO section above. After signing in, the Copilot status bar icon should show a checkmark. To verify:

1. Open a source file (e.g., `hello.go`).
2. Type `// ` and start writing a comment. Copilot ghost-text suggestions should appear after a few seconds.
3. Press `Tab` to accept a suggestion.
4. Open Copilot Chat from the sidebar (`Ctrl+Alt+I` / `Cmd+Option+I`). Ask a simple question: `What does the function above do?` — the assistant should respond.

If you do not see suggestions, see the troubleshooting section below.

## Enabling Approved Assistant Features

ACME's GitHub Enterprise organization policy applies the following defaults. You do not need to opt in.

| Feature | Default at ACME | Notes |
|---------|------------------|-------|
| Code completion (ghost text) | Enabled | Inline suggestions in editor. |
| Copilot Chat | Enabled | Inline chat and chat panel. |
| Workspace context (chat) | Enabled — for files you have open | The assistant can read open files in your workspace. |
| Repository context (chat) | Disabled by default; per-repo opt-in required | See "Repository-specific instructions" below. |
| Copilot Edits (multi-file) | Enabled — for repositories marked as opted in | Requires the repo's `copilot-instructions.md` to be present. |
| Public-code matching detection | Enabled (block) | If a suggestion matches public code on GitHub, the suggestion is blocked and you are warned. |
| Telemetry to GitHub | Disabled | ACME does not share prompts or completions with GitHub for training. |

## Organization-Level Restrictions

The GitHub Enterprise organization policy at `git.acme.example/acme` (fictional) applies the following restrictions. These are non-negotiable and override any per-user setting.

- **No prompts containing Confidential or Restricted data** — see [`03-security/data-classification.md`](../03-security/data-classification.md). Customer data, secrets, and credentials must never be entered.
- **No prompts containing source code from non-ACME repositories** unless you are the author or have written permission.
- **No use of Copilot in repositories that have not opted in** — see "Repository-specific instructions" below.
- **AI-generated output must be reviewed by a human before being committed** — see [`04-engineering/practices/pull-requests-and-code-review.md`](./practices/pull-requests-and-code-review.md) and the "Human review of generated code" section below.
- **Audit logs are retained** — Copilot prompts and completions are logged to `logs.internal.acme.example` (fictional) for 90 days. See [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) for the audit policy.

## Repository-Specific Instructions

Each repository may opt in (or out) of Copilot via a `copilot-instructions.md` file at the repository root. This file is reviewed by the owning EM and the GRC analyst (Karthik Subramanian).

A sample `copilot-instructions.md`:

```markdown
# Copilot instructions for acme-cloud-api

This repository is opted in to GitHub Copilot Business.

## Allowed
- Code completion in Go files.
- Generating unit tests for new code.
- Explaining existing functions.

## Not allowed
- Generating code that handles customer data without an explicit
  human review of the generated output against
  ../../03-security/customer-data-handling.md.
- Generating SQL DDL or migrations without an explicit human review
  against the team's migration policy.

## Sensitive paths
- /secrets — do not include in prompts.
- /migrations — generate but require explicit human review.
- /vendor — third-party code; do not modify.
```

If a repository does not have a `copilot-instructions.md` file, the default is opt-out. You may still use Copilot, but you are responsible for following [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) carefully.

## Code Completion and Chat Usage

### Code completion

- Copilot suggestions are hints, not answers. Read every suggestion before accepting it. Verify against:
  - The function's actual purpose (does the suggestion match?).
  - Coding standards — see [`04-engineering/practices/coding-standards.md`](./practices/coding-standards.md).
  - Tests — does the existing test suite still pass?
- If a suggestion is wrong, do not commit it. Either fix it manually or reject it.
- Long completions (> 30 lines) are more likely to be wrong. Treat them with extra skepticism.

### Copilot Chat

- Use Chat for: explaining unfamiliar code, drafting docstrings, generating boilerplate, listing test cases.
- Do not use Chat for: making decisions on architecture, security trade-offs, or customer commitments. Those require human judgment.
- Chat context: only the files you have open and explicitly add with `@workspace` or `#file`. Do not paste Confidential/Restricted content into Chat.

## AI-Assisted Unit Test Generation

Copilot can draft unit tests. ACME's recommended workflow:

1. Open the function you want to test.
2. Open Copilot Chat. Type: `Write unit tests for the function above. Use the team's table-driven test convention. Cover happy path, edge cases, and error cases.`
3. Review the generated tests. Common gaps:
   - The generated tests often miss negative paths (what if the input is nil?).
   - The generated tests often assume the function is a pure function. If it has side effects, add assertions for those.
   - The generated tests may use APIs not in the codebase. Verify imports.
4. Add the tests to the test file. Run `make test` (or equivalent). If any test fails, the failure is a bug in your test or your function — fix it.
5. Commit the tests in the same PR as the function under test, unless the function already exists.

## AI-Assisted Code Reviews

Copilot can summarize a PR for the reviewer. ACME's recommended workflow:

1. Open the PR in GitHub Enterprise (web or via the GitHub Pull Requests extension in VS Code).
2. Click the "Copilot review" button. Copilot will generate a summary and a list of suggestions.
3. Use the summary to orient yourself. Use the suggestions as a starting point for your own review — do not blindly accept or reject them.
4. The human reviewer (you) is the binding reviewer. The CODEOWNERS approval comes from you, not from Copilot. See [`04-engineering/practices/pull-requests-and-code-review.md`](./practices/pull-requests-and-code-review.md).

## Handling Proprietary Code

ACME's source code is **Confidential** by default — see [`03-security/source-code-security.md`](../03-security/source-code-security.md). Specifically:

- Do not paste ACME source code into a non-ACME AI tool (e.g., a public chatbot).
- Do not paste ACME source code into an ACME AI tool outside the approved chat surfaces (Copilot Chat, internal ACME Intelligence sandbox).
- Do not paste customer source code into any AI tool, even approved ones, without explicit customer permission in the master service agreement.
- Do not commit AI-generated code that you have not reviewed.

## Restrictions on Sensitive Data

The following categories of data must **never** be entered into an AI assistant, even an approved one:

| Category | Example | Why forbidden |
|----------|---------|----------------|
| Customer data | Customer PII, customer logs, customer configuration | [`03-security/customer-data-handling.md`](../03-security/customer-data-handling.md) |
| Credentials and secrets | API tokens, passwords, private keys | [`03-security/secrets-management.md`](../03-security/secrets-management.md) |
| Confidential business data | M&A plans, financial results before public release, employee PII | [`03-security/data-classification.md`](../03-security/data-classification.md) |
| Regulated data | PHI, PCI data, data subject to data residency | [`03-security/customer-data-handling.md`](../03-security/customer-data-handling.md) |
| Internal legal or HR records | Investigation notes, individual performance plans | [`01-hr/employee-grievance-procedure.md`](../01-hr/employee-grievance-procedure.md), [`03-security/confidentiality-agreement.md`](../03-security/confidentiality-agreement.md) |

If you have entered any of the above into an AI assistant by mistake:

1. Stop using the chat.
2. Immediately contact the SOC (`soc@acme.example`) and your manager.
3. Open an incident using [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md).

## Human Review of Generated Code

Every AI-generated line that you commit must be reviewed by you before commit, and by a teammate before merge. Concretely:

1. **Author review (you):** Verify the generated code (a) compiles, (b) passes existing tests, (c) does not introduce security issues (e.g., `eval`, SQL string concat, weak crypto), (d) does not violate the coding standards.
2. **Add tests:** If the generated code adds behavior, add tests for it.
3. **Reviewer review (teammate):** The reviewer reads the diff and verifies the same items. The reviewer should specifically ask: "Is this generated? Did you review it?"
4. **Commit message convention:** Mark AI-assisted commits in the footer: `Co-Authored-By: Copilot <noreply@github.com>` (added automatically by GitHub) and a `Generated-By: copilot` line in the commit body for traceability in audit logs.

## Troubleshooting and Support

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| "Copilot not available for this organization" | Org policy not yet applied, or you are signed in with personal account | Sign out, sign in with `@acme.example` via SSO. |
| "Rate limit exceeded" | Too many requests in short window | Wait 60 seconds. If persistent, check `status.acme.example/copilot`. |
| No suggestions appear | File language disabled, or extension disabled | Check status bar icon. Verify the file's language is enabled in Copilot settings. |
| Suggestions are slow (> 10s) | VPN latency or proxy | Connect directly to the ACME network or report to IT Helpdesk. |
| Chat gives "I cannot help with that" | Policy block (data classification) | Verify you are not pasting Confidential/Restricted data. |
| Chat output is wrong but you cannot tell why | Model hallucination | File an issue in `#engineering-help` with the prompt (redacted). Do not commit the output. |
| License seat not visible | EM has not yet assigned the seat | Confirm with EM; if confirmed, contact IT Onboarding (Geetha Iyer). |

## What to Read Next

- [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md) — the binding ACME policy.
- [`04-engineering/practices/coding-standards.md`](./practices/coding-standards.md)
- [`04-engineering/practices/pull-requests-and-code-review.md`](./practices/pull-requests-and-code-review.md)
- [`04-engineering/practices/unit-and-integration-testing.md`](./practices/unit-and-integration-testing.md)
- Your role-specific onboarding guide in [`05-teams/`](../05-teams/).

## Related Documents

- [`04-engineering/developer-workstation-setup.md`](./developer-workstation-setup.md)
- [`04-engineering/source-code-and-repository-access.md`](./source-code-and-repository-access.md)
- [`04-engineering/repository-catalog.md`](./repository-catalog.md)
- [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- [`03-security/data-classification.md`](../03-security/data-classification.md)
- [`03-security/customer-data-handling.md`](../03-security/customer-data-handling.md)
- [`03-security/source-code-security.md`](../03-security/source-code-security.md)
- [`03-security/secrets-management.md`](../03-security/secrets-management.md)
- [`03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md)
- [`04-engineering/practices/coding-standards.md`](./practices/coding-standards.md)
- [`04-engineering/practices/pull-requests-and-code-review.md`](./practices/pull-requests-and-code-review.md)
- [`04-engineering/practices/unit-and-integration-testing.md`](./practices/unit-and-integration-testing.md)
- [`08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- [`07-workflows/first-week-onboarding.md`](../07-workflows/first-week-onboarding.md)
