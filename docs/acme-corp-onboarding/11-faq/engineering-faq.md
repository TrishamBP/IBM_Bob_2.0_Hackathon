---
document_id: ACME-FAQ-003
title: Engineering Frequently Asked Questions
category: faq
department: engineering
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [faq, engineering, github, copilot, ci-cd, testing, on-call]
---

# Engineering Frequently Asked Questions

This FAQ answers the most common engineering questions at ACME Corp — GitHub Copilot, repository access, branching, code review, CI/CD, deployments, on-call, and package publishing. For anything not covered here, ask in the #eng-help channel on Microsoft Teams or escalate to your team's Director. The canonical engineering practices live in [../04-engineering/](../04-engineering/).

### Q: How do I get a GitHub Copilot license?
Copilot licenses are provisioned through the [AI coding assistant setup](../04-engineering/ai-coding-assistant-setup.md) workflow and require your manager to file a license-request form before you can activate the extension. Licenses are billed monthly, so unused seats are reclaimed after 30 days of inactivity — open VS Code or IntelliJ at least once a week to keep your seat. Read [../03-security/ai-tool-acceptable-use.md](../03-security/ai-tool-acceptable-use.md) before you start coding with Copilot; it covers what code you may and may not paste into prompts.

### Q: Which repo is mine?
Your team's repos are listed in the [repository catalog](../04-engineering/repository-catalog.md) and you can also run `gh repo list --mine` after enrolling your GitHub Enterprise token. Each repo's README documents its owning team and the CODEOWNERS file lists the maintainers who can approve changes. Your team onboarding guide (e.g. [../05-teams/backend-engineer-onboarding.md](../05-teams/backend-engineer-onboarding.md)) lists the specific repos you should clone on day one.

### Q: How do I request access to another team's repo?
File a repository access request through the form at ../08-forms/repository-access-request.md — the owning team lead receives the request and approves or rejects it within two business days. Most repos have a `Read` role for all engineers via the `acme-engineers` team, but `Write` access is team-scoped and requires business justification. The access model and the appeal path if a request is denied are documented in [../04-engineering/source-code-and-repository-access.md](../04-engineering/source-code-and-repository-access.md).

### Q: How do I get prod access?
Prod access is granted through Just-In-Time activation in Microsoft PIM, with a max session of 4 hours and a recorded business justification. You must be on the approved on-call rotation or have a Change Management ticket open to request it; standing prod access is reserved for SREs. The role definitions, break-glass procedures, and the audit trail are covered in [../03-security/least-privilege-access.md](../03-security/least-privilege-access.md) and [../04-engineering/practices/development-staging-production.md](../04-engineering/practices/development-staging-production.md).

### Q: How do I run tests?
Each repo has a `make test` or `pnpm test` target documented in its README; you can also run the full suite through the GitHub Actions workflow named `ci`. For unit tests use the framework documented in [../04-engineering/practices/unit-and-integration-testing.md](../04-engineering/practices/unit-and-integration-testing.md) — most repos use Vitest for TypeScript, JUnit5 for Java, and pytest for Python. Always run the affected tests locally before pushing; the CI gate will block your PR if tests fail.

### Q: How do I deploy?
For staging, merge to `main` and the CD pipeline auto-deploys within 10 minutes — no manual steps required. For production, open a release through the [release management](../04-engineering/practices/release-management.md) workflow, get two reviewer approvals, and the deploy runs after the change-window opens (14:00–18:00 IST weekdays). Emergency prod deploys follow the break-glass flow documented in [../04-engineering/practices/incident-response-and-on-call-introduction.md](../04-engineering/practices/incident-response-and-on-call-introduction.md).

### Q: What's the branching strategy?
ACME uses trunk-based development with `main` as the always-deployable trunk, short-lived feature branches (max 3 days), and release tags cut from `main` for production deploys. Hotfixes branch off `main` and merge back via a fast-tracked PR; the full strategy is in [../04-engineering/practices/git-branching-strategy.md](../04-engineering/practices/git-branching-strategy.md). Long-lived branches are discouraged and require an exception from your Director.

### Q: How many reviewers do I need?
Most repos require one reviewer for changes under 300 lines and two reviewers above that, with at least one CODEOWNER approval for files in protected paths. Security-sensitive changes (auth, crypto, customer data) require an additional review from the security guild; see [../04-engineering/practices/pull-requests-and-code-review.md](../04-engineering/practices/pull-requests-and-code-review.md). PRs stale for more than 5 days are auto-closed by the bot to keep the queue moving.

### Q: How do I report an incident?
Page the on-call rotation through PagerDuty (linked from status.acme.example) and post a summary in the #incidents-active channel within 5 minutes of confirming user impact. For customer-impacting incidents, also file a ticket in the Incident module so the Incident Commander can declare a severity and start the timeline. The full severity matrix, escalation paths, and the post-incident review process are in [../04-engineering/practices/incident-response-and-on-call-introduction.md](../04-engineering/practices/incident-response-and-on-call-introduction.md).

### Q: When am I on-call?
New engineers are shadow-only for their first 60 days and join the primary rotation after their manager confirms they have completed the [incident response intro](../04-engineering/practices/incident-response-and-on-call-introduction.md) training. The standard rotation is one week of primary and one week of secondary, Monday-to-Monday, with a paid on-call allowance per the [employee handbook](../00-company/employee-handbook.md). Your team's specific schedule lives in the team onboarding doc, e.g. [../05-teams/devops-engineer-onboarding.md](../05-teams/devops-engineer-onboarding.md).

### Q: How do I publish to the internal packages registry?
The internal registry is at packages.acme.example and supports npm, PyPI, and Maven artifacts; publish using the `acme-publish` CLI which signs packages with your Entra ID-bound short-lived token. Never check a long-lived token into a repo — the [secrets management](../03-security/secrets-management.md) policy covers the OIDC-based publishing flow that uses GitHub Actions trust. The full publish-and-version workflow is in [../04-engineering/practices/internal-package-management.md](../04-engineering/practices/internal-package-management.md).

### Q: What testing framework do we use?
TypeScript repos use Vitest with Playwright for end-to-end tests, Java repos use JUnit5 with Mockito and Testcontainers, Python repos use pytest with Hypothesis for property-based tests. The full matrix and the minimum coverage gates (80% unit, 60% integration) are in [../04-engineering/practices/unit-and-integration-testing.md](../04-engineering/practices/unit-and-integration-testing.md). New repos should use these defaults; switching frameworks requires an architecture review.

### Q: How do I debug a failing CI check?
Start by re-running the failed job with debug logging enabled (`gh run rerun --debug` on the run ID), and check the cache hits in the workflow summary. Common causes are flaky integration tests, expired OIDC tokens, and a missing env var — see the debugging playbook at [../04-engineering/practices/debugging.md](../04-engineering/practices/debugging.md). If the failure is infrastructural (runner offline, package registry 5xx), ping #eng-platform rather than retrying.

### Q: Where are the runbooks?
Runbooks live next to the service they cover, in the `docs/runbooks/` directory of each repo, and are also indexed on status.acme.example under "Operations". Each runbook has an owner, last-reviewed date, and links to the relevant dashboards; stale runbooks (over 6 months) are flagged red. If a runbook is missing for an incident you're handling, file a `docs/runbook` issue against the owning repo — see [../04-engineering/practices/observability-and-logging.md](../04-engineering/practices/observability-and-logging.md) for the observability layer underneath.

### Q: How do I set up Copilot in VS Code?
Install the "GitHub Copilot" and "GitHub Copilot Chat" extensions from the VS Code Marketplace (pre-installed on ACME developer images), then sign in with your Entra ID — your license activates automatically if your manager has filed the request. Configure the chat to use the `gpt-4o` model and enable `github.enterprise.uri` set to `https://git.acme.example` for repo-context suggestions. Full setup steps including JetBrains are in [../04-engineering/ai-coding-assistant-setup.md](../04-engineering/ai-coding-assistant-setup.md).

### Q: Can I use an external AI tool (ChatGPT, Claude) for work code?
No — pasting ACME source code, customer data, or secrets into external AI tools violates the [AI tool acceptable use](../03-security/ai-tool-acceptable-use.md) policy and is treated as a Confidential data leak. The only approved AI coding assistants are GitHub Copilot Business and the ACME-hosted internal LLM at llm.acme.example, which is data-resident. The [source code security](../03-security/source-code-security.md) policy covers the boundary in detail; violations are reviewed by the GRC team led by Karthik Subramanian (karthik.subramanian@acme.example).

### Q: What are CODEOWNERS?
CODEOWNERS is a file at the root of each repo (`.github/CODEOWNERS`) that maps file paths to GitHub teams or individuals who must approve changes to those paths. It enforces the [least-privilege access](../03-security/least-privilege-access.md) principle at the code-review layer — security-critical paths like `auth/`, `crypto/`, and `infra/terraform/` always require a security-guild reviewer. The format and conventions ACME follows are in [../04-engineering/practices/pull-requests-and-code-review.md](../04-engineering/practices/pull-requests-and-code-review.md).

### Q: Where do I find the design doc template?
The official design doc template lives at wiki.acme.example under "Engineering > Templates > RFC" and is also mirrored in the `acme-shared-libraries` repo at `docs/templates/rfc.md`. New RFCs are filed as PRs against the `docs/rfcs/` folder of the owning repo, with the author tagged as the owner and a 5-business-day comment window. See [../04-engineering/practices/release-management.md](../04-engineering/practices/release-management.md) for how an approved RFC feeds into the release planning process.

## Topics Covered

- **AI tooling**: GitHub Copilot Business licensing, VS Code setup, external-AI policy
- **Repositories**: finding yours, requesting access, CODEOWNERS, repository catalog
- **Environments**: prod access via PIM, dev/staging/prod boundaries
- **Testing**: framework matrix, running tests, debugging CI failures
- **CI/CD and deploys**: pipelines, release management, emergency deploys
- **Branching and review**: trunk-based strategy, reviewer counts, PR staleness
- **On-call and incidents**: paging, severity matrix, shadow period, runbooks
- **Packaging**: internal registry at packages.acme.example, signed publishing
- **Design docs**: RFC template location and approval flow

## Escalation Contacts

- VP Engineering / CTO: Sridhar Venkatesh — sridhar.venkatesh@acme.example
- Director AI/ML: Anitha Rajan — anitha.rajan@acme.example
- VP IT (infra/platform): Ramesh Khanna — ramesh.khanna@acme.example
- CISO (security review): Rajan Mehta — rajan.mehta@acme.example
- GRC Analyst: Karthik Subramanian — karthik.subramanian@acme.example
- IT Helpdesk: helpdesk@acme.example

For team-specific escalation paths, see your team onboarding guide under [../05-teams/](../05-teams/). For the full contact list, see [../09-contacts/contact-directory.md](../09-contacts/contact-directory.md).
