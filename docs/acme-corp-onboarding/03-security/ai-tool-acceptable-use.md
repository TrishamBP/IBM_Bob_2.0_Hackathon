---
document_id: ACME-SEC-017
title: AI Tool Acceptable Use
category: security
department: information-security
applicable_roles: [all]
owner: Neha Saxena, Security Director
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, ai, copilot, llm, acceptable-use, fictional]
---

# AI Tool Acceptable Use

> ACME Corp fictional onboarding library. Hostnames (`git.acme.example`, `portal.acme.example`), the internal LLM platform, the sandbox, and mailboxes are fictional. GitHub Copilot Business is a real Microsoft product; the ACME deployment is simulated for illustration. No real prompts, completions, or credentials are shown.

## 1. Purpose

This document defines ACME Corp's policy for using AI tools — code-completion assistants, conversational LLMs, internal models, and embedded AI features. AI tools can accelerate engineering, support, and operational work, but they also create two classes of risk that this policy exists to manage: (1) leakage of Confidential, Restricted, or Customer Data into external AI services, and (2) low-quality, insecure, or non-compliant AI-generated output being shipped without human review. This policy applies on top of [`acceptable-use-policy.md`](acceptable-use-policy.md) and is the canonical reference for any AI-tool-related decision at ACME.

## 2. Scope

This applies to:

- All ACME workforce members, contractors, and authorized third parties.
- All AI tools — whether integrated into an IDE, accessed via a web chat, called via API, or embedded in another product.
- All ACME data — Public, Internal, Confidential, Restricted, and Customer Data per [`data-classification.md`](data-classification.md).
- All devices used to access AI tools — corporate-issued laptops, BYOD phones (per [`byod-policy.md`](byod-policy.md)), and personal devices used for ACME work in violation of this policy.

## 3. Approved AI Tools

ACME maintains a small allowlist of approved AI tools. Use of any AI tool outside this list is a violation of [`acceptable-use-policy.md`](acceptable-use-policy.md).

| Tool | Use Case | Approval Path |
|------|----------|----------------|
| **GitHub Copilot Business** | Code completion and chat inside the IDE, for ACME Confidential source code | Provisioned via the ACME GitHub Enterprise org — see [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md). Request a license via [`../08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md). |
| **ACME Intelligence internal sandbox** | Internal LLM platform for ACME Confidential data, hosted inside ACME's environment. Suitable for confidential documents, internal RAG over ACME Wiki. | Provisioned via SSO at `portal.acme.example/ai-sandbox` (fictional URL). |
| **Microsoft 365 Copilot** (where licensed) | Document summarization, email drafting inside Microsoft 365 apps, on ACME Confidential data | Provisioned per-seat by IT. |
| **Embedded AI features in approved ACME products** | E.g., features shipped inside ACME Workspace | Owned by the product teams; reviewed at design-doc stage. |

### 3.1 Prohibited AI Tools

The following are **prohibited** for any ACME work:

- ChatGPT, Claude.ai, Google Gemini (consumer), Perplexity, and any consumer AI chat accessed via a personal account.
- Any AI coding assistant other than GitHub Copilot Business — including Copilot Free, Tabnine, Codeium (consumer), and any AI assistant integrated into a personal IDE account.
- Any external AI tool that does not have a signed Data Processing Agreement (DPA) with ACME.
- Any "free" or community-hosted AI tool, even for a quick test.
- Any AI tool accessed via a personal API key, even briefly.

This list is non-exhaustive — when in doubt, the rule is: assume the tool is prohibited unless it is on the approved list above.

## 4. Data Classification Rules for AI Tools

This is the most important rule in this document. The matrix below maps data classification to where it may be entered.

| Data Tier | May be entered into external AI tools? | May be entered into the ACME Intelligence internal sandbox? |
|------------|----------------------------------------|--------------------------------------------------------------|
| **Public** | Yes (e.g., "summarize this public ACME blog post") | Yes |
| **Internal** | No | Yes |
| **Confidential** | No | Yes, with redaction where possible |
| **Restricted** | No | **No** (the sandbox is not approved for Restricted data) |
| **Customer Data** | **No — never, ever** | **No — never, ever** |

**Any customer data brought into ACME systems is Restricted by default** and is never to be entered into any AI tool, internal or external. This includes: customer configurations, customer-uploaded documents, customer source code, customer support tickets, customer telemetry, and any field that could identify or be combined to identify a customer's end-user.

If you are about to paste something into an AI tool and you are unsure of its classification — **stop**. Treat it as Restricted until you confirm with the GRC Analyst (`Karthik Subramanian`) or the data owner.

## 5. Using GitHub Copilot Business

GitHub Copilot Business is the only approved AI coding assistant at ACME. Use rules:

- **Eligible code:** Confidential ACME source code (per the repository's classification in `README.md` / `CODEOWNERS`). Copilot's prompts and completions flow within the ACME GitHub Enterprise tenant and are governed by the Microsoft/Copilot Business DPA.
- **Ineligible code:** Customer-shared source code (Customer Data tier). If you are working in a repository that contains customer-shared code, **disable Copilot** for that workspace — see [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md) for how.
- **Ineligible content:** Secrets, API keys, customer PII, regulated data. Copilot may suggest completions that look like these — never accept them. Never paste a real secret into Copilot chat.
- **License:** Requested via [`../08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md). Each license is reviewed quarterly; unused licenses are reclaimed.
- **Output review:** You are responsible for every line you commit, whether you wrote it or Copilot suggested it. Review the diff. Check the license of suggested snippets. Run CI checks. Do not skip review because "Copilot wrote it."

## 6. Using the ACME Intelligence Internal Sandbox

The internal sandbox at `portal.acme.example/ai-sandbox` (fictional) is approved for:

- ACME Confidential documents — with redaction of any Restricted fields (PII, secrets, customer-specific data).
- Internal RAG over the ACME Wiki (`wiki.acme.example`, fictional).
- Drafting internal communications, design docs, and runbooks.

It is **not** approved for:

- Restricted data (production credentials, customer PII, source code containing secrets).
- Customer Data (any data about or belonging to an ACME customer).
- Personal data of employees beyond what is necessary for the task (data minimization — see [`privacy-acknowledgement.md`](privacy-acknowledgement.md)).

The sandbox logs every prompt and completion to the SOC SIEM, retained for 13 months. Anomalous usage (e.g., a user pasting 100MB of Confidential text in an hour) triggers a SOC alert.

## 7. Human Review of AI Output

AI tools produce confident-sounding output that can be wrong. Rules for using AI output:

1. **Review every line.** Whether it is a code suggestion, a paragraph of marketing copy, or a SQL query — review it before it is used.
2. **Verify facts.** LLMs hallucinate citations, API names, and library signatures. Cross-check against the canonical documentation.
3. **Verify code.** Run the tests. AI-suggested code that "looks right" can have off-by-one errors, security flaws, or wrong imports. CI checks (see [`../04-engineering/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md)) and security scanners (see [`open-source-dependency-security.md`](open-source-dependency-security.md)) still apply.
4. **Verify licenses.** AI tools can suggest snippets verbatim from licensed code (e.g., GPL). Run a license scan; do not commit code without verifying its provenance.
5. **Disclose AI assistance.** In design docs and postmortems, note where AI assistance was materially used. This is not a punishment; it is for audit traceability.
6. **No autonomous decisions.** AI tools must not make decisions about customers (e.g., deny support, escalate billing, block access) without a human in the loop.
7. **No customer communication without review.** AI-drafted customer emails must be reviewed by a human and by the Comms team for material statements.

## 8. Audit Expectations

The SOC audits AI tool usage:

- **GitHub Copilot:** quarterly review of license allocation (reclaim unused licenses); quarterly review of any prompt-history exports available in the GitHub Enterprise audit log.
- **ACME Intelligence sandbox:** continuous review of prompt volumes; daily review of anomalous usage.
- **Microsoft 365 Copilot:** quarterly review of license allocation.
- **External AI tools:** the SOC reviews outbound network traffic for signs of unsanctioned AI-tool use. Connecting to an unsanctioned AI service from a corporate device triggers a SOC alert.

## 9. What Counts as a Violation

Violations of this policy include — non-exhaustively:

- Entering Customer Data into any AI tool (external or internal).
- Entering Restricted data into the internal sandbox.
- Using an external AI tool (ChatGPT, Claude.ai, Gemini consumer) for ACME work.
- Using Copilot in a repository containing Customer Data.
- Committing AI-generated code without review.
- Using a personal API key to access an external AI tool for ACME work.
- Sharing an ACME-issued AI tool license with another person.

Violations are handled under [`acceptable-use-policy.md`](acceptable-use-policy.md) §9 and [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md). Customer Data exposure via AI tools is a SEV1 incident — see [`security-incident-reporting.md`](security-incident-reporting.md) and triggers customer notification per [`customer-data-handling.md`](customer-data-handling.md).

## 10. Responsibilities

| Role | Responsibility |
|------|----------------|
| **Security Director** (`Neha Saxena`) | Owns this document. Approves additions to the allowlist. |
| **IAM Engineer** (`Abhishek Verma`) | Provisions Copilot licenses and sandbox access via SSO. |
| **SOC Lead** (`Fatima Sheikh`) | Monitors AI tool usage. Triage alerts for unsanctioned use. |
| **GRC Analyst** (`Karthik Subramanian`) | Maintains the AI-tool risk register. Reviews DPAs for new tools. |
| **Engineering Managers** | Ensure their teams use approved tools. Review new-tool requests. |
| **Every workforce member** | Use only approved tools. Never enter Customer/Restricted data. Review AI output before use. |

## 11. Enforcement

- The internal sandbox is gated by SSO; the conditional access policy restricts access to compliant devices.
- GitHub Copilot licenses are allocated via the ACME GitHub Enterprise org; only licensed seats can use Copilot.
- The SOC reviews outbound network traffic from corporate devices; unsanctioned AI tool use triggers an alert.
- DLP prevents copy-paste of Customer Data into external AI tools (where supported).
- Violations are handled per §9.

## 12. Exceptions

To request an addition to the approved AI tools list:

1. Email `security-oncall@acme.example` (fictional) with the tool name, the use case, and the vendor's DPA.
2. The GRC Analyst (`Karthik Subramanian`) reviews the DPA for data-handling terms.
3. The Security Director (`Neha Saxena`) approves or denies.
4. Approved tools are added to the list in §3.

Personal-use AI tools, on personal devices, on personal time, with personal data, are outside the scope of this policy. They become in-scope the moment any ACME data is involved.

## 13. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`acceptable-use-policy.md`](acceptable-use-policy.md) — Underlying AUP.
- [`data-classification.md`](data-classification.md) — Drives which data may go where.
- [`customer-data-handling.md`](customer-data-handling.md) — Customer data is never in any AI tool.
- [`source-code-security.md`](source-code-security.md) — Copilot in repositories.
- [`security-incident-reporting.md`](security-incident-reporting.md) — AI-tool-related incident workflow.
- [`privacy-acknowledgement.md`](privacy-acknowledgement.md) — Data minimization.
- [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md) — Copilot setup.
- [`../08-forms/ai-coding-assistant-license-request.md`](../08-forms/ai-coding-assistant-license-request.md) — License request form.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Security Director, IAM Engineer, GRC Analyst contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — LLM, RAG, prompt, completion definitions.
