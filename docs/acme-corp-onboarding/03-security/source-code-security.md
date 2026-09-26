---
document_id: ACME-SEC-014
title: Source Code Security
category: security
department: information-security
applicable_roles: [all]
owner: Neha Saxena, Security Director
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, source-code, github-enterprise, codeowners, branch-protection, fictional]
---

# Source Code Security

> ACME Corp fictional onboarding library. The GitHub Enterprise instance at `git.acme.example` is fictional. Internal package registry `packages.acme.example` and secrets store `vault.acme.example` are fictional. No real credentials, tokens, or proprietary code are shown.

## 1. Purpose

This document defines ACME Corp's policy for protecting its source code. Source code is the most valuable intellectual property ACME owns — it is the building block of ACME Cloud, ACME Intelligence, and ACME Workspace. A leak of source code can enable attackers to find vulnerabilities, expose customer-specific configurations, and damage ACME's competitive position. This policy covers classification, repository hygiene, branch protection, review, secrets handling, and external publication.

## 2. Scope

This applies to:

- Every repository hosted on the ACME GitHub Enterprise instance at `git.acme.example` (fictional).
- Every ACME workforce member who writes, reviews, merges, or deploys code.
- All code in any language, on any branch, including forks, sandboxes, and archived repositories.
- All third-party code ACME depends on — see [`open-source-dependency-security.md`](open-source-dependency-security.md) for the supply-chain rules.

## 3. Classification of Source Code

By default, **all ACME source code is classified as Confidential** per [`data-classification.md`](data-classification.md). Sub-categories:

| Sub-Category | Default Tier | Notes |
|--------------|--------------|-------|
| Public documentation site source | Public | Approved for release; only the marketing/docs repo is Public. |
| Product source (ACME Cloud, ACME Intelligence, ACME Workspace) | Confidential | Default. Never published externally. |
| Internal-tooling source | Internal | May be shared internally without restriction; not for external publication without review. |
| Customer-shared source code (e.g., a customer's repo integrated with ACME) | Customer Data (Restricted) | Treated as the customer's data — see [`customer-data-handling.md`](customer-data-handling.md). |
| Source containing secrets, customer PII, or regulated data | Restricted | Should never exist — see [`secrets-management.md`](secrets-management.md) — but if it does, immediate rotation and cleanup are required. |

If you are unsure, treat the code as Confidential until you confirm with the repository owner or the Security Director (`Neha Saxena`).

## 4. Repository Hygiene

Every ACME repository must have, at minimum:

1. **`README.md`** — purpose, ownership, classification, and a link to the design doc.
2. **`CODEOWNERS`** — at the repository root; declares which teams own which paths. See [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md) for the canonical format.
3. **`LICENSE`** — for any repo that may be published externally; absent for Confidential repos.
4. **`.github/CODEOWNERS`** or root-level `CODEOWNERS` — auto-reviewers per path.
5. **Branch protection** — see §5.
6. **Required status checks** — CI must pass before merge. See [`../04-engineering/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md).
7. **Secret scanning** — GitHub secret scanning enabled; pre-commit hooks (see [`secrets-management.md`](secrets-management.md)).
8. **A documented deployment pipeline** — for production code; see [`../04-engineering/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md).

## 5. Branch Protection

Every Confidential and Customer Data repository enforces branch protection on `main` and on release branches:

| Protection | Setting |
|------------|---------|
| **Require pull request before merging** | On. |
| **Require approval from CODEOWNERS** | On — at least one CODEOWNER approval per path. |
| **Dismiss stale approvals on new push** | On. |
| **Require status checks to pass** | On — CI must pass; security scan must pass. |
| **Require branches up to date before merging** | On. |
| **Require signed commits** | On — GPG or SSH signing. |
| **Require linear history** | On — merge commits prohibited; squash or rebase. |
| **Do not allow bypassing the above** | On — admins cannot self-merge. |
| **Force pushes** | Blocked. |
| **Deletion of `main` or release branches** | Blocked. |

The Security Director (`Neha Saxena`) reviews the branch-protection posture quarterly via the GitHub Enterprise audit log.

## 6. Code Review

- All changes flow through a pull request (see [`../04-engineering/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md)).
- The author self-reviews the diff, writes a description, and links the ticket or design doc.
- A CODEOWNER (not the author) reviews and approves.
- For changes touching security-sensitive code (auth, crypto, payment, customer-data handling), a second reviewer from the Security team is required.
- The reviewer is responsible for: correctness, tests, secrets (none in the diff), dependency changes (run [`open-source-dependency-security.md`](open-source-dependency-security.md) checks), and classification labelling.
- "Buddy reviews" (a quick non-blocking review from a peer) are encouraged but do not replace CODEOWNERS review.

## 7. Secrets in Code — Forbidden

Secrets must never be committed to a repository. Specifically:

- No API keys, tokens, passwords, connection strings, private keys, or certificates in source code.
- Secrets are stored in ACME Vault (`vault.acme.example`, fictional) — see [`secrets-management.md`](secrets-management.md).
- Use workload identity federation or managed identities wherever possible — no static secrets.
- Where a secret must be referenced in code, use a runtime-injected variable from the deployment pipeline or a sealed secret in Kubernetes.
- Pre-commit hooks scan for high-entropy strings and known secret patterns. If a pre-commit hook blocks a commit, **fix it — do not bypass the hook.**
- GitHub secret scanning runs continuously on every push. A finding triggers an automatic page to the SOC.

If a secret is committed by accident:

1. **Do not just delete the line in a follow-up commit.** The secret is in the git history forever.
2. Rotate the secret immediately in ACME Vault — see [`secrets-management.md`](secrets-management.md).
3. Contact the SOC (`soc@acme.example`, fictional) to coordinate history rewriting if the secret is high-impact (typically a customer-impacting key).
4. The SOC will run `git filter-repo` (or the equivalent) to rewrite history, force-push (allowed only by exception for this purpose), and notify anyone with a clone to re-fetch.

## 8. Public Repositories

Public repositories on `git.acme.example` (fictional) or on external Git hosts (github.com, gitlab.com) require:

- **Legal review** — confirms ACME has the rights to publish the code, including all contributions (a Developer Certificate of Origin or CLA is required).
- **Security review** — confirms no secrets, no Confidential content, no customer-specific configurations.
- **CISO approval** — for any code that touches security-critical functions.
- **A `LICENSE` file** — using an ACME-approved license (see [`open-source-dependency-security.md`](open-source-dependency-security.md)).
- **A `SECURITY.md`** — for vulnerability disclosure.
- **A `CONTRIBUTING.md`** — including the CLA requirement if external contributions are accepted.

There are no "private-then-public" flip-flops without re-review. Once public, the code is public — assume attackers have read it.

## 9. Access to Repositories

- Access is granted per-team via Entra ID SSO groups (see [`identity-and-access-management.md`](identity-and-access-management.md)).
- Repository access requests go through [`../08-forms/repository-access-request.md`](../08-forms/repository-access-request.md) and the workflow in [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md).
- Standing write access to a repository is permitted only for CODEOWNERS — see [`least-privilege-access.md`](least-privilege-access.md).
- Standing admin access to a repository requires PIM activation.
- Customer-shared repositories follow [`customer-data-handling.md`](customer-data-handling.md) — customer-named access only, logged access.

## 10. CI/CD and Pipeline Security

- Pipelines run as service accounts with workload identity federation — no static secrets in CI configuration.
- Pipeline secrets are stored in ACME Vault or as GitHub Actions secrets (encrypted at rest).
- Production deploys require approval from a CODEOWNER plus a member of the SRE team — see [`../04-engineering/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md).
- Build artifacts are signed (sigstore/cosign) and verified at deploy time.
- Dependency vulnerabilities are scanned at build time — see [`open-source-dependency-security.md`](open-source-dependency-security.md).

## 11. AI Coding Assistants and Source Code

- GitHub Copilot Business is the only approved AI coding assistant — see [`ai-tool-acceptable-use.md`](ai-tool-acceptable-use.md) and [`../04-engineering/ai-coding-assistant-setup.md`](../04-engineering/ai-coding-assistant-setup.md).
- Customer-shared source code is **never** entered into any AI tool, internal or external — see [`customer-data-handling.md`](customer-data-handling.md).
- The internal ACME Intelligence sandbox may be used on Confidential code; it must not be used on Customer Data code.
- Output from AI tools is treated as untrusted; the author is responsible for reviewing every line before merge.

## 12. Responsibilities

| Role | Responsibility |
|------|----------------|
| **Repository Owners** | Maintain CODEOWNERS, branch protection, and CI. Review access lists quarterly. |
| **Code Authors** | Write tests, run pre-commit hooks, request review, do not commit secrets. |
| **Code Reviewers (CODEOWNERS)** | Review for correctness, security, secrets, classification. Do not approve their own PRs. |
| **Security Director** (`Neha Saxena`) | Reviews branch-protection posture. Approves public-repo requests. |
| **SOC Lead** (`Fatima Sheikh`) | Triages GitHub secret-scanning findings. |
| **IAM Engineer** (`Abhishek Verma`) | Configures SSO-to-role mapping. Maintains PIM for repository admins. |
| **Engineering Managers** | Maintain CODEOWNERS list for their teams. Approve access requests. |

## 13. Enforcement

- Branch protection is enforced by GitHub Enterprise at the organization level — repository admins cannot disable it.
- Secret scanning is enabled organization-wide.
- Pre-commit hooks are installed by the developer-workstation baseline (see [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md)).
- Conditional access blocks non-compliant devices from `git.acme.example`.
- The Security Director reviews audit logs quarterly for policy violations.

## 14. Exceptions

Exceptions (e.g., legacy repos that cannot yet enforce branch protection) require Security Director (`Neha Saxena`) approval, a remediation date, and a documented compensating control. Email `security-oncall@acme.example` (fictional).

## 15. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`data-classification.md`](data-classification.md) — Source code is Confidential by default.
- [`secrets-management.md`](secrets-management.md) — Where secrets live (not in code).
- [`open-source-dependency-security.md`](open-source-dependency-security.md) — Third-party dependencies.
- [`ai-tool-acceptable-use.md`](ai-tool-acceptable-use.md) — AI coding assistant rules.
- [`least-privilege-access.md`](least-privilege-access.md) — Repository admin access via PIM.
- [`identity-and-access-management.md`](identity-and-access-management.md) — SSO-to-role mapping.
- [`customer-data-handling.md`](customer-data-handling.md) — Customer-shared source code.
- [`confidentiality-agreement.md`](confidentiality-agreement.md) — Underlying IP obligations.
- [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md) — Repository access mechanics.
- [`../04-engineering/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md) — Branching model.
- [`../04-engineering/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md) — Pipeline security.
- [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md) — Canonical repo list.
- [`../08-forms/repository-access-request.md`](../08-forms/repository-access-request.md) — Access request form.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Security Director, SOC Lead, IAM Engineer contacts.
