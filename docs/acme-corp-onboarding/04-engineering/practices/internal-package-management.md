---
document_id: ACME-ENG-009
title: Internal Package Management
category: engineering
department: engineering
applicable_roles: [engineers]
owner: Engineering
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [engineering, practices, packages, semver, provenance]
---

# Internal Package Management

> All hosts referenced here are fictional. `packages.acme.example`, `git.acme.example`, and `registry.internal.acme.example` do not resolve. Sample commands are **simulated** for onboarding orientation only.

ACME Corp's internal package registry lives at `packages.acme.example`. It serves Go modules, npm packages, Python wheels, and Maven artifacts. This document defines how packages are published, versioned, consumed, and deprecated.

## 1. Registry Overview

`packages.acme.example` is a fictional multi-format registry:

| Format | Path prefix | Auth |
|--------|-------------|------|
| Go modules | `packages.acme.example/go` | OIDC token from GitHub Actions, mapped to a per-repo write token |
| npm | `packages.acme.example/npm` | `.npmrc` with `//packages.acme.example/npm/:_authToken` from Vault |
| PyPI | `packages.acme.example/pypi` | `pip` with keyring backed by Vault |
| Maven | `packages.acme.example/maven` | `~/.m2/settings.xml` with a per-team server entry |

Engineers have **read** access to all packages scoped to their team and to the shared libraries. **Write** access is granted only to the CI service account (`ci-bot@acme.example`) — there are **no manual publishes**, period.

## 2. Versioning: Semantic Versioning

All internal packages follow **Semantic Versioning 2.0.0**:

- `MAJOR` — breaking change (an API removal or behavior change that would break a known consumer).
- `MINOR` — new functionality, backward compatible.
- `PATCH` — bug or security fix, backward compatible.

Pre-release identifiers follow the SemVer spec:

- `1.4.0-rc.1` — release candidate.
- `1.4.0-beta.2` — beta.
- `1.4.0-dev.3+<short-sha>` — development snapshot, never published to consumers directly.

The version is **derived** from a single source of truth per package:

| Language | Source of truth |
|----------|-----------------|
| Go | git tag `v<MAJOR>.<MINOR>.<PATCH>` on `main`, or on a release branch |
| npm | `package.json` `version` field |
| Python | `pyproject.toml` `[project].version` |
| Maven | `pom.xml` `<version>` |

CI refuses to publish if the version is already present in the registry — there are no overwrites, ever.

## 3. Publishing: CI Only, Provenance Required

Publishing happens only from the `release.yml` workflow (see [CI/CD overview](./ci-cd-overview.md)) when a `v*` tag is pushed. The publish job:

1. Verifies the version is not already in the registry.
2. Builds the artifact.
3. Generates an SBOM (CycloneDX) for the artifact.
4. Generates an in-toto SLSA build attestation, signed with the ACME OIDC key.
5. Publishes the artifact **and** the SBOM **and** the attestation as OCI artifacts alongside the package.
6. Posts a notification to the owning team's Slack channel (fictional: `#cloud-api-releases`).

A manual `npm publish`, `twine upload`, `mvn deploy`, or `GOPROXY` push is **forbidden**. If a release is broken mid-publish, the fix is to publish the **next** patch version, never to overwrite the broken one.

### Sample publish workflow (npm)

```yaml
# Sample GitHub Actions workflow — fictional, illustrative only.
name: release

on:
  push:
    tags: ['acme-ui-utils-v*']

permissions:
  contents: read
  id-token: write
  packages: write

jobs:
  publish-npm:
    runs-on: self-hosted:linux-amd64-medium
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          registry-url: 'https://packages.acme.example/npm'
      - name: Build
        run: pnpm install --frozen-lockfile && pnpm build
      - name: Generate SBOM
        run: pnpm sbom --out bom.json
      - name: Publish
        run: npm publish --provenance --access restricted
        env:
          NODE_AUTH_TOKEN: ${{ secrets.VAULT_ISSUED_NPM_TOKEN }}
```

## 4. Consumption Rules

### 4.1 Go modules

```bash
# fictional/simulated command — pull an internal Go module
GOPROXY=https://packages.acme.example/go,https://proxy.golang.org,direct \
  go get acme.internal/shared/quota@v1.4.0
```

- The `GOPROXY` env var must list `packages.acme.example` first; the standard proxy as fallback.
- Pin a specific minor version (`@v1.4.0` or `@v1.4.2`), not a moving tag.
- The `go.sum` is the source of truth; CI fails if a checksum mismatches.
- Internal Go modules live under the `acme.internal/` path; the public `github.com/acme` path is reserved for OSS we publish externally.

### 4.2 npm

```ini
; .npmrc — fictional sample
@acme:registry=https://packages.acme.example/npm
//packages.acme.example/npm/:_authToken=${VAULT_ISSUED_NPM_TOKEN}
always-auth=true
```

- All internal npm packages are scoped `@acme/*`.
- Pin exact versions in `package.json` — no `^` or `~` for internal packages. Use `renovate` for bumps (see [Open-source dependency security](../../03-security/open-source-dependency-security.md)).

### 4.3 PyPI

```ini
; pip.conf — fictional sample
[global]
extra-index-url = https://packages.acme.example/pypi/simple
trusted-host = packages.acme.example
```

- Internal PyPI packages live under the `acme_*` namespace (e.g., `acme_shared_logging`).
- Pin exact versions in `requirements.txt` or `pyproject.toml`. The `acme-quality-automation` repository owns the `pip-tools` compile step.

### 4.4 Maven

```xml
<!-- pom.xml — fictional sample -->
<repositories>
  <repository>
    <id>acme-internal</id>
    <url>https://packages.acme.example/maven</url>
    <releases><enabled>true</enabled></releases>
    <snapshots><enabled>false</enabled></snapshots>
  </repository>
</repositories>
```

- Snapshots are **disabled**. ACME publishes release-only; consumers depend on real versions.
- The `~/.m2/settings.xml` server entry for `acme-internal` is populated from Vault.

## 5. Provenance and Supply-Chain Integrity

Every published artifact carries:

1. **An SBOM** in CycloneDX 1.5 format, attached as an OCI artifact.
2. **A SLSA Level 3 build attestation** in in-toto statement format, signed with the ACME OIDC signing key (sigstore).
3. **A signed provenance** linking the package to the source commit and the build workflow run.

Consumers can verify a package before use:

```bash
# fictional/simulated command — verify an npm package's provenance
npm view @acme/quota-utils --provenance --json | acme-verify-provenance

# fictional/simulated command — verify a Go module's checksum against the registry
acme-verify-module acme.internal/shared/quota@v1.4.0
```

A package that fails provenance verification is rejected by CI on the consumer side. See [`../../03-security/open-source-dependency-security.md`](../../03-security/open-source-dependency-security.md) for the policy basis.

## 6. Deprecation Policy

Internal packages are deprecated, not deleted. The lifecycle is:

1. **Active** — published and recommended for new use.
2. **Deprecated** — still published, but a `npm deprecate` / Go ` retract` directive is set; consumers see a deprecation message. A deprecation ticket is filed against the owning team.
3. **Maintenance** — only security fixes land. The owning team commits to a 6-month maintenance window.
4. **End-of-life** — no new fixes; the package is marked `end-of-life` in the registry. Consumers receive a hard error on install.
5. **Removed** — after 12 months in EOL state, the package is removed. A migration runbook is published before removal.

The deprecation clock starts when the owning team publishes the first successor version. A successor is required; packages cannot be deprecated without a documented migration path.

## 7. Shared Libraries Catalog

The [`acme-shared-libraries`](../repositories/acme-shared-libraries.md) repository is the canonical home for cross-team libraries. New packages proposed for inclusion must:

- Have at least two consuming teams (otherwise, the package belongs in the consuming team's repo).
- Pass the [coding standards](./coding-standards.md) gate.
- Have 80%+ unit coverage (higher than the 70% floor).
- Be sponsored by a senior engineer on the Platform Infrastructure team (Nikhil Joshi) or a delegate.

## 8. Version Bump Discipline

When a consuming team bumps an internal dependency, the rules are:

| Bump type | When | PR requires |
|-----------|------|-------------|
| Patch | Bug fix or security fix | 1 reviewer + CI green |
| Minor | New backward-compatible feature | 1 reviewer + CI green + consuming team sign-off |
| Major | Breaking change | 2 reviewers + an ADR + consuming-team EM sign-off |

A breaking change in a shared library is rare. The preferred path is:

1. Add the new API.
2. Mark the old API as deprecated in the same release.
3. Migrate consumers per-team over a quarter.
4. Remove the deprecated API in a major bump **after** all consumers are migrated.

## 9. Audit and Compliance

The registry is audited weekly by Security GRC. The audit reports:

- All packages published in the last week, with their publish workflow URL and provenance status.
- All packages consumed in the last week, with the consuming repository and version pin.
- Any package whose provenance failed verification.
- Any package in EOL state still actively consumed (migration ticket required).

Audit reports are published to the fictional Wiki at `https://wiki.acme.example/platform/registry-audit`.

## 10. Anti-Patterns

| Anti-pattern | Why it's wrong | Fix |
|---------------|-----------------|------|
| Manual `npm publish` | Bypasses provenance | Use the release workflow |
| Overwriting a published version | Breaks consumers | Publish the next patch |
| `^` / `~` for internal deps | Silent breaking change | Pin exact version |
| Publishing from a feature branch | Untested artifact | Tag from `main` or `release/*` |
| Skipping the SBOM | Blocks audit | Use the `release.yml` template |
| Deprecating without a successor | Migration impossible | Ship successor first |
| Removing without notice | Consumer breakage | Follow the EOL → removed 12-month path |

## 11. Cross-Reference Table

| Need | See |
|------|-----|
| How releases are tagged | [`./release-management.md`](./release-management.md) |
| CI/CD pipeline and the publish job | [`./ci-cd-overview.md`](./ci-cd-overview.md) |
| Coding standards for libraries | [`./coding-standards.md`](./coding-standards.md) |
| OSS dependency policy | [`../../03-security/open-source-dependency-security.md`](../../03-security/open-source-dependency-security.md) |
| Secrets / publish tokens | [`../../03-security/secrets-management.md`](../../03-security/secrets-management.md) |
| Shared libraries repo | [`../repositories/acme-shared-libraries.md`](../repositories/acme-shared-libraries.md) |
| Platform infrastructure repo | [`../repositories/acme-platform-infrastructure.md`](../repositories/acme-platform-infrastructure.md) |

## Related Documents

- [`../repository-catalog.md`](../repository-catalog.md)
- [`./git-branching-strategy.md`](./git-branching-strategy.md)
- [`./pull-requests-and-code-review.md`](./pull-requests-and-code-review.md)
- [`./coding-standards.md`](./coding-standards.md)
- [`./commit-message-conventions.md`](./commit-message-conventions.md)
- [`./ci-cd-overview.md`](./ci-cd-overview.md)
- [`./release-management.md`](./release-management.md)
- [`../repositories/acme-shared-libraries.md`](../repositories/acme-shared-libraries.md)
- [`../repositories/acme-platform-infrastructure.md`](../repositories/acme-platform-infrastructure.md)
- [`../../03-security/secrets-management.md`](../../03-security/secrets-management.md)
- [`../../03-security/open-source-dependency-security.md`](../../03-security/open-source-dependency-security.md)
- [`../../03-security/source-code-security.md`](../../03-security/source-code-security.md)
- [`../../metadata/glossary.md`](../../metadata/glossary.md)
