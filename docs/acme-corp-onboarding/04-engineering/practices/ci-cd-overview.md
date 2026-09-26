---
document_id: ACME-ENG-006
title: CI/CD Overview
category: engineering
department: engineering
applicable_roles: [engineers]
owner: Engineering
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [engineering, practices, ci-cd, github-actions]
---

# CI/CD Overview

> All hosts and runners referenced here are fictional. `runners.internal.acme.example`, `git.acme.example`, and `registry.internal.acme.example` do not resolve. Sample YAML is for onboarding orientation only and is not expected to be executed against a real GitHub Actions deployment.

ACME Corp's CI/CD platform is **GitHub Actions** running on self-hosted runners at `runners.internal.acme.example`. Build artifacts are pushed to the internal container registry at `registry.internal.acme.example`. Internal libraries are published to `packages.acme.example` (see [Internal package management](./internal-package-management.md)).

## 1. Pipeline Shape

Every ACME repository ships a `.github/workflows/` directory with at least four workflows:

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `pr.yml` | Pull request opened / updated | Lint, unit tests, license scan, secret scan, SAST |
| `main.yml` | Push to `main` | Build artifacts, publish, deploy to `dev` |
| `release.yml` | Tag `v*` on `main` | Deploy to staging, hold for prod approval |
| `nightly.yml` | Schedule 02:00 UTC | Integration tests, dependency vuln scan, drift detection |

## 2. Required Checks on Every PR

The following checks must pass before a PR can be merged into `main`. Branch protection enforces this; see [`./pull-requests-and-code-review.md`](./pull-requests-and-code-review.md).

| Check | Job | Purpose |
|-------|-----|---------|
| `ci/build` | compile all packages | Catches obvious breakage early |
| `ci/lint` | run formatter + linters | Enforces [Coding standards](./coding-standards.md) |
| `ci/unit-tests` | per-package unit tests with coverage | See [Unit and integration testing](./unit-and-integration-testing.md) |
| `ci/integration-tests` | against ephemeral dev stack | Run on PRs touching `internal/`, `proto/`, or `deploy/` |
| `ci/license-scan` | identifies GPL/AGPL/etc. in deps | Enforces [`../../03-security/open-source-dependency-security.md`](../../03-security/open-source-dependency-security.md) |
| `ci/secret-scan` | grep + gitleaks on diff | Enforces [`../../03-security/secrets-management.md`](../../03-security/secrets-management.md) |
| `ci/sast` | static analysis (Semgrep + language-native) | Enforces [`../../03-security/source-code-security.md`](../../03-security/source-code-security.md) |
| `ci/commit-lint` | validate Conventional Commits on PR title | Enforces [Commit message conventions](./commit-message-conventions.md) |
| `ci/buf-breaking` | proto backward-compat (Cloud API, Workspace API) | Prevents accidental public API breakage |

A failing check blocks merge, even if all reviewers have approved. Security GRC may bypass for an active incident only, and the bypass is logged and reviewed weekly.

## 3. Sample PR Workflow (`pr.yml`)

```yaml
# Sample GitHub Actions workflow — fictional, illustrative only.
name: pr

on:
  pull_request:
    branches: [main]

permissions:
  contents: read
  checks: write
  pull-requests: write

jobs:
  build:
    runs-on: self-hosted:linux-amd64-medium
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      - name: Build
        run: make build
      - name: Lint
        run: make lint
      - name: Unit tests
        run: make test
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage-${{ github.sha }}
          path: coverage.out
          retention-days: 14

  license-scan:
    runs-on: self-hosted:linux-amd64-small
    steps:
      - uses: actions/checkout@v4
      - name: Scan dependencies for license policy violations
        run: make license-scan  # fictional; uses acme-license-scanner

  secret-scan:
    runs-on: self-hosted:linux-amd64-small
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Scan diff for secrets
        run: make secret-scan  # fictional; uses gitleaks

  sast:
    runs-on: self-hosted:linux-amd64-small
    steps:
      - uses: actions/checkout@v4
      - name: Static analysis (Semgrep + gosec)
        run: make sast  # fictional

  commit-lint:
    runs-on: self-hosted:linux-amd64-small
    steps:
      - uses: actions/checkout@v4
      - name: Validate PR title (Conventional Commits)
        run: make commit-lint  # fictional; uses acme-commit-lint
```

## 4. Build Artifacts and the Internal Registry

On merge to `main`, the `main.yml` workflow builds the container image and pushes it to the internal registry:

```bash
# fictional/simulated command — tag and push the image
docker build \
  --label org.opencontainers.image.source=https://git.acme.example/acme-cloud/acme-cloud-api \
  --label org.opencontainers.image.revision=${GITHUB_SHA} \
  -t registry.internal.acme.example/acme-cloud/api:${GITHUB_SHA::7} \
  -t registry.internal.acme.example/acme-cloud/api:dev \
  .
docker push registry.internal.acme.example/acme-cloud/api:${GITHUB_SHA::7}
docker push registry.internal.acme.example/acme-cloud/api:dev
```

The image carries:

- **Provenance:** an in-toto SLSA build attestation, signed with the ACME OIDC-issued signing key.
- **SBOM:** a CycloneDX manifest attached to the image as an OCI artifact.
- **Labels:** source URL, git revision, build timestamp, build workflow URL.

Pull access to `registry.internal.acme.example` is restricted:

| Identity | Pull | Push |
|----------|------|------|
| All engineers (read) | All repos | None |
| CI service account (`ci-bot@acme.example`) | All repos | Own team's repos |
| Release manager role | All repos | Own team's release tags |
| On-call SRE | All repos | Hotfix tags only, time-boxed 4h |

**Push access to the registry is never granted to individual engineers.** Only the CI service account, the rotating release manager role, and time-boxed SRE hotfix access can push.

## 5. Deploy Pipeline and Environment Gating

The deploy pipeline is **gated by environment**. GitHub Actions environments are used to enforce approval:

| Environment | Trigger | Approval | Notes |
|-------------|---------|----------|-------|
| `dev` | Merge to `main` | Auto | Ephemeral namespace per PR or per engineer |
| `staging` | Tag `v*` on `main` | Auto (tag implies approval) | Shared, integration with partner systems |
| `production` | Tagged release + change ticket | **Manual approval** by release manager + on-call SRE | Canary 5% → 25% → 100% |

### Sample deploy job (`release.yml`)

```yaml
# Sample GitHub Actions workflow — fictional, illustrative only.
name: release

on:
  push:
    tags: ['v*']

permissions:
      contents: read
      id-token: write
      packages: write

jobs:
  deploy-staging:
    runs-on: self-hosted:linux-amd64-medium
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - name: Promote image staging
        run: make release-promote ENV=staging IMG=registry.internal.acme.example/acme-cloud/api:${GITHUB_REF_NAME}

  deploy-production:
    needs: deploy-staging
    runs-on: self-hosted:linux-amd64-medium
    environment:
      name: production
      url: https://status.acme.example
    steps:
      - uses: actions/checkout@v4
      - name: Canary 5%
        run: make release-canary ENV=prod IMG=... PERCENT=5
      - name: Wait 10m, check SLO burn
        run: make release-watch ENV=prod WINDOW=10m
      - name: Ramp to 25%
        run: make release-canary ENV=prod IMG=... PERCENT=25
      - name: Wait 30m, check SLO burn
        run: make release-watch ENV=prod WINDOW=30m
      - name: Ramp to 100%
        run: make release-canalty ENV=prod IMG=... PERCENT=100
```

### Standing production access

**No new employee gets standing production access.** Production deploy rights are granted **just-in-time** through the Privileged Identity Management (PIM) flow described in [`./development-staging-production.md`](./development-staging-production.md) and [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md). The GitHub Actions `production` environment requires manual approval from a member of the `release-managers` team and an on-call SRE; that approval is itself a PIM-elevated role, not a standing one. Production environment credentials live in [`vault.acme.example`](https://vault.acme.example) and are issued on a 4-hour, single-approval basis.

## 6. Self-Hosted Runners

Self-hosted runners live at `runners.internal.acme.example` and are organized by capability:

| Runner label | Hardware | Use case |
|--------------|----------|----------|
| `self-hosted:linux-amd64-small` | 2 vCPU, 4 GB | Lint, scan, commit-lint |
| `self-hosted:linux-amd64-medium` | 8 vCPU, 16 GB | Build, unit tests, deploy |
| `self-hosted:linux-amd64-large` | 32 vCPU, 64 GB | Integration tests, ML model packaging |
| `self-hosted:linux-amd64-gpu` | 8 vCPU + 1× A100 | Inference image build, model benchmark |
| `self-hosted:windows-amd64-medium` | 8 vCPU, 16 GB | Windows-specific build and tests |

Runners are ephemeral: a fresh runner is provisioned per job and destroyed after. Runner logs are forwarded to `logs.internal.acme.example` and are restricted to the owning team plus Security GRC.

## 7. Caching Strategy

CI performance relies on three caches:

1. **Module / package caches** (Go module cache, npm cache, pip cache, Maven `.m2`) — keyed on the lockfile hash, restored by `actions/cache`.
2. **Build caches** (Go build cache, TypeScript incremental build info, Maven target) — keyed on the source tree hash.
3. **Layer caches** (Docker BuildKit) — pushed to a private cache endpoint at `cache.internal.acme.example`.

A cold-cache PR build is expected to take ≤ 15 minutes for an average repository. If it routinely exceeds that, file an issue against `acme-platform-infrastructure` (see [`../repositories/acme-platform-infrastructure.md`](../repositories/acme-platform-infrastructure.md)).

## 8. Secrets in CI

Secrets are never stored in GitHub Actions secrets at the repository level — except for short-lived, low-privilege tokens that grant access to Vault. The pattern is:

1. The workflow uses `id-token: write` to mint a GitHub OIDC token.
2. The OIDC token is exchanged at `vault.acme.example` for a Vault token scoped to the secrets the job needs.
3. The Vault token expires when the job ends.

See [`../../03-security/secrets-management.md`](../../03-security/secrets-management.md) for the policy basis.

## 9. Required vs. Non-Required Checks

Some checks run on every PR but are **non-required** (advisory). They are visible in the PR UI but do not block merge:

- `ci/coverage-delta` — comments on whether coverage went up or down.
- `ci/bundle-size` (frontend only) — comments on JS bundle size delta.
- `ci/codeclimate` — Code Climate maintainability trend.

Required checks are configured in the GitHub branch-protection rule for each repository. The list above (`ci/build`, `ci/lint`, `ci/unit-tests`, `ci/license-scan`, `ci/secret-scan`, `ci/sast`, `ci/commit-lint`, `ci/buf-breaking`) is the floor; individual repositories may add more.

## 10. Failure Handling

- A red `ci/build` or `ci/lint` is almost always the author's responsibility.
- A red `ci/secret-scan` blocks merge until the secret is removed **and** rotated. The secret-scan job posts a comment with the file:line and the rotation runbook link.
- A red `ci/license-scan` blocks merge until either the offending dependency is replaced or a Legal-exception ticket is filed.
- A red `ci/sast` blocks merge until the finding is triaged: fix, suppress with a justification + ticket link, or escalate to Security GRC.
- A flaky `ci/unit-tests` job (the same test failing intermittently) is auto-quarantined after 3 failures in 7 days — see [Unit and integration testing](./unit-and-integration-testing.md).

## 11. Cross-Reference Table

| Need | See |
|------|-----|
| Branch protection rules | [`./git-branching-strategy.md`](./git-branching-strategy.md) |
| Reviewer requirements | [`./pull-requests-and-code-review.md`](./pull-requests-and-code-review.md) |
| Coding standards enforced by lint | [`./coding-standards.md`](./coding-standards.md) |
| Commit message format | [`./commit-message-conventions.md`](./commit-message-conventions.md) |
| Test expectations | [`./unit-and-integration-testing.md`](./unit-and-integration-testing.md) |
| Environment gating, PIM | [`./development-staging-production.md`](./development-staging-production.md) |
| Release cadence and rollback | [`./release-management.md`](./release-management.md) |
| Observability for deployed services | [`./observability-and-logging.md`](./observability-and-logging.md) |
| Secrets in CI | [`../../03-security/secrets-management.md`](../../03-security/secrets-management.md) |
| Source code security baseline | [`../../03-security/source-code-security.md`](../../03-security/source-code-security.md) |
| Least-privilege rationale | [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md) |

## Related Documents

- [`../repository-catalog.md`](../repository-catalog.md)
- [`./git-branching-strategy.md`](./git-branching-strategy.md)
- [`./pull-requests-and-code-review.md`](./pull-requests-and-code-review.md)
- [`./coding-standards.md`](./coding-standards.md)
- [`./commit-message-conventions.md`](./commit-message-conventions.md)
- [`./unit-and-integration-testing.md`](./unit-and-integration-testing.md)
- [`./internal-package-management.md`](./internal-package-management.md)
- [`./observability-and-logging.md`](./observability-and-logging.md)
- [`./development-staging-production.md`](./development-staging-production.md)
- [`./release-management.md`](./release-management.md)
- [`../repositories/acme-cloud-api.md`](../repositories/acme-cloud-api.md)
- [`../repositories/acme-platform-infrastructure.md`](../repositories/acme-platform-infrastructure.md)
- [`../../03-security/source-code-security.md`](../../03-security/source-code-security.md)
- [`../../03-security/secrets-management.md`](../../03-security/secrets-management.md)
- [`../../03-security/open-source-dependency-security.md`](../../03-security/open-source-dependency-security.md)
- [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md)
- [`../../metadata/glossary.md`](../../metadata/glossary.md)
