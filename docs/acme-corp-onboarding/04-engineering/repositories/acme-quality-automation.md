---
document_id: ACME-REPO-010
title: Repository Guide — acme-quality-automation
category: engineering
department: engineering
applicable_roles: [qe-engineers, sres, backend-engineers, frontend-engineers]
owner: Asha Reddy (EM, Quality Engineering)
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [repository, shared, python-playwright-jmeter]
---

# Repository Guide — `acme-quality-automation`

> **Fictional repository.** The host `git.acme.example` does not resolve. All commands below are **simulated** and shown for onboarding orientation only. Do not attempt to execute them against any real system.

## 1. Repository Purpose

`acme-quality-automation` is the **central test automation + load-testing** repository for ACME Corp. It hosts the cross-product Playwright end-to-end suites, JMeter load + soak tests, synthetic monitoring scripts, and the shared fixtures + assertion library consumed by every product team's CI.

Key responsibilities:

- Cross-product E2E suites (Cloud, Intelligence, Workspace).
- Load and soak tests (JMeter) for platform SLO validation.
- Synthetic monitoring probes wired to the on-call alerting path.
- Shared fixture generators, faker bindings, and the ACME assertion DSL.

## 2. Owning Team and EM

| Field | Value |
|-------|-------|
| Owning Team | Quality Engineering |
| Engineering Manager | Asha Reddy (asha.reddy@acme.example) |
| Product | Shared |
| Slack channel (fictional) | `#qe-automation` |
| On-call rotation | `qe-oncall` (synthetic-monitoring failures only) |

## 3. Primary Technology Stack

- **Language:** Python 3.11
- **E2E framework:** Playwright 1.x (sync + async APIs)
- **Load testing:** JMeter 5.6, Taurus for orchestration
- **Reporting:** Allure reports published to `reports.internal.acme.example`
- **Observability:** Test results → `metrics.internal.acme.example`; failure alerts via the QE PagerDuty-style rotation
- **Secrets:** Vault at `vault.acme.example` (path `secret/qe/*`); staging test accounts are short-lived OIDC-federated identities.

## 4. Access Requirements

- **Source access:** Read access is granted to **all engineers**. Write access requires the **Engineering — QE** tier plus a QE EM approval.
- **CI access:** Self-hosted GitHub Actions runners at `runners.internal.acme.example`. E2E runs use the Playwright grid at `playwright.internal.acme.example`.
- **Test environment access:** Engineers receive staging test accounts via OIDC; production synthetic-monitor credentials are CI-scoped only.
- See [`../../08-forms/repository-access-request.md`](../../08-forms/repository-access-request.md) and [`../source-code-and-repository-access.md`](../source-code-and-repository-access.md).

## 5. Manager Approval Required

**Yes — for write access.** Read access is granted to all engineers by default.

1. Read access — auto-granted at onboarding via the SSO group `acme-all-engineers`.
2. Write access — requires the **Engineering — QE** tier and approval from Asha Reddy (EM).
3. Security GRC review — required for any change to the synthetic-monitor credentials path, the prod-monitor probes, or the data-redaction assertions in `lib/redaction/`.

Production synthetic-monitor credentials are **not** standing access. The production monitor probes run from a CI-scoped service account with break-glass reserved for on-call SRE. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md).

## 6. Local Setup

```bash
# fictional/simulated command — clone the repository
git clone git@git.acme.example:acme-quality/acme-quality-automation.git
cd acme-quality-automation

# fictional/simulated command — create the virtualenv
python -m venv .venv && source .venv/bin/activate

# fictional/simulated command — install dev dependencies + Playwright browsers
pip install -e ".[dev]"
playwright install --with-deps chromium

# fictional/simulated command — connect to dev Vault for staging test accounts
export VAULT_ADDR=https://vault.acme.example
# vault login -method=oidp role=qe-dev  # interactive, read-only

# fictional/simulated command — point the suite at the staging environment
export ACME_TARGET=https://api.staging.acme.example
```

## 7. Branching Conventions

Trunk-based per [`../git-branching-strategy.md`](../practices/git-branching-strategy.md):

- `main` — always runnable; squash-merge PRs only.
- `feat/<jira-id>-<slug>` — new E2E suite, load profile, or fixture generator.
- `fix/<jira-id>-<slug>` — flaky-test fixes, selector updates.
- `perf/<slug>` — load-profile tuning (regression-gated).
- `release/<YYYY.MM>` — cut monthly from `main`.

Flaky-test fixes should reference the failing run URL in the PR description; the CI auto-tags re-runs.

## 8. Build and Test Commands

```bash
# fictional/simulated command — type-check
make typecheck

# fictional/simulated command — run a single E2E suite against staging
make e2e -- --suite=cloud --env=staging

# fictional/simulated command — run the full E2E matrix (all products, all browsers)
make e2e-full

# fictional/simulated command — run a JMeter load profile against staging
make load -- --profile=cloud-api-baseline --env=staging

# fictional/simulated command — run a soak test (60 min)
make soak -- --profile=workspace-soak --env=staging --minutes=60

# fictional/simulated command — linters (ruff, black, bandit)
make lint

# fictional/simulated command — generate Allure report
make report
```

## 9. Pull-Request Requirements

- `CODEOWNERS` enforced via branch protection.
- **Two** approving reviews for `main`; at least one from the QE team.
- Required status checks:
  - `ci/build`
  - `ci/typecheck`
  - `ci/lint`
  - `ci/e2e-smoke` (a representative subset, fast)
  - `ci/sast`
- PRs that add or modify a load profile must include a baseline-vs-after report from the staging run.
- PRs touching `monitors/prod/` or `lib/redaction/` additionally require Security GRC approval.
- Flaky-test detection: a test that flakes on >2% of runs in the trailing 7 days is auto-quarantined; a PR that removes the quarantine requires a fix linked.
- See [`../pull-requests-and-code-review.md`](../practices/pull-requests-and-code-review.md) and [`../coding-standards.md`](../practices/coding-standards.md).

## 10. CODEOWNERS (Sample Structure)

```text
# Sample CODEOWNERS for acme-quality-automation (fictional)
# Read access is open to all engineers; write access is QE-gated.

*                                           @acme/qe

# Per-product E2E suites — product team co-review
/suites/cloud/                             @acme/qe @acme/cloud-api @acme/cloud-frontend
/suites/intelligence/                      @acme/qe @acme/intel-agents @acme/intel-inference
/suites/workspace/                         @acme/qe @acme/workspace-api @acme/workspace-web

# Load + soak profiles — SRE co-review for SLO alignment
/load/                                      @acme/qe @acme/sre
/soak/                                      @acme/qe @acme/sre

# Production monitors + redaction — security co-review
/monitors/prod/                            @acme/qe @acme/security-grc
/lib/redaction/                            @acme/qe @acme/security-grc

# CI pipeline — platform co-review
/.github/workflows/                        @acme/qe @acme/platform
```

## 11. Deployment Environments

This repository has **no long-lived runtime environments**. "Deploy" means publishing the suite to the test runner grids and the synthetic monitor controllers.

| Stage | Purpose | Trigger | Approver |
|-------|---------|---------|----------|
| `dev` | Per-branch suite run on the dev grid | Push to a feature branch | Auto (CI) |
| `staging` | Suite + load profiles against staging envs | Merge to `main` | QE EM (Asha Reddy) |
| `production` | Synthetic monitor probes against prod endpoints | Tagged release + change ticket | Release Manager + on-call SRE |

**Sample deployment sequence (fictional):**

```bash
# fictional/simulated command — cut a release tag (QE EM approval)
git tag -a v2026.09.3 -m "qe-automation v2026.09.3"
git push origin v2026.09.3

# fictional/simulated command — publish suite package to internal registry
make publish -- --version=v2026.09.3

# fictional/simulated command — open a change ticket for prod monitor rollout
# Use the ITSM portal: https://itsm.acme.example/change/new  (fictional)

# fictional/simulated command — deploy prod synthetic monitors (on-call SRE only)
# acme-monitorctl deploy --env=prod --version=v2026.09.3
```

> Production synthetic-monitor rollout is **not** standing access. Just-in-time elevation is granted for a release window after change-ticket approval. See [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md) and [`../ci-cd-overview.md`](../practices/ci-cd-overview.md).

## 12. Documentation Links

- Internal Wiki (fictional): `https://wiki.acme.example/qe/automation/overview`
- E2E suite catalog (fictional): `https://wiki.acme.example/qe/automation/suites`
- Load profile reference (fictional): `https://wiki.acme.example/qe/automation/load-profiles`
- Synthetic monitor runbook (fictional): `https://wiki.acme.example/qe/automation/monitors`
- Service catalog entry: `https://catalog.acme.example/services/acme-quality-automation`

## Related Documents

- [`../repository-catalog.md`](../repository-catalog.md)
- [`../developer-workstation-setup.md`](../developer-workstation-setup.md)
- [`../source-code-and-repository-access.md`](../source-code-and-repository-access.md)
- [`../git-branching-strategy.md`](../practices/git-branching-strategy.md)
- [`../pull-requests-and-code-review.md`](../practices/pull-requests-and-code-review.md)
- [`../ci-cd-overview.md`](../practices/ci-cd-overview.md)
- [`../coding-standards.md`](../practices/coding-standards.md)
- [`../observability-and-logging.md`](../practices/observability-and-logging.md)
- [`../incident-response-and-on-call-introduction.md`](../practices/incident-response-and-on-call-introduction.md)
- [`../../03-security/source-code-security.md`](../../03-security/source-code-security.md)
- [`../../03-security/secrets-management.md`](../../03-security/secrets-management.md)
- [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md)
- [`../../08-forms/repository-access-request.md`](../../08-forms/repository-access-request.md)
- [`../../08-forms/it-access-request.md`](../../08-forms/it-access-request.md)
- [`../../09-contacts/contact-directory.md`](../../09-contacts/contact-directory.md)
