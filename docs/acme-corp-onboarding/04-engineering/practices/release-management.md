---
document_id: ACME-ENG-012
title: Release Management
category: engineering
department: engineering
applicable_roles: [engineers]
owner: Engineering
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [engineering, practices, releases, canary, rollback, release-manager]
---

# Release Management

> All hosts referenced here are fictional. `git.acme.example`, `registry.internal.acme.example`, `status.acme.example`, and `pager.acme.example` do not resolve. Sample commands are **simulated** for onboarding orientation only.

ACME Corp ships on a predictable cadence so that customers, support, and engineers can plan around releases. This document defines the cadence, the release manager role, the canary procedure, the rollback runbook, customer communication, and code-freeze windows.

## 1. Release Cadence

| Type | Frequency | Branching | Scope |
|------|-----------|-----------|-------|
| Patch | As needed, on `release/*` | Hotfix to release branch | Bug/security fix only |
| Minor | **Monthly**, first business week | Cut `release/<YYYY.MM>` from `main` | New features, backward compatible |
| Major | **Quarterly**, aligned with the minor in the first month of the quarter | Cut `release/<YYYY.Q>` from `main` | May include breaking changes (with ADR + customer comms) |

Each product (Cloud, Intelligence, Workspace) follows the same cadence, but with **staggered** weeks to avoid a "release Monday" where everything ships at once:

| Product | Minor release week |
|---------|--------------------|
| ACME Cloud | First full week of the month |
| ACME Workspace | Second full week |
| ACME Intelligence | Third full week |
| Shared libraries | Fourth full week (if a minor ships that month) |

Patch releases can ship any business day, with a 24-hour notice to support.

## 2. Release Manager Role

Each release has a **rotating release manager** drawn from the senior engineers on the owning team. The rotation:

- Cloud API — Anjali Desai maintains the rotation; the rotation has 6 senior engineers, each takes one month.
- Workspace API — Priya Menon maintains the rotation.
- Intelligence Agents/Inference/ML — Rohan Bhat, Vivek Anand, Lakshmi Narayan share the rotation.
- Platform Infrastructure — Nikhil Joshi maintains the rotation.

The release manager's responsibilities for the month:

1. Cut the `release/<YYYY.MM>` branch on the first business day of the release week.
2. Triage release-blocking bugs; approve or reject cherry-picks onto the release branch.
3. Coordinate the staging sign-off with Quality Engineering (Asha Reddy's team).
4. Drive the canary to production; make the go/no-go decisions at each ramp.
5. Author the customer release notes; coordinate with DevRel.
6. Hand the next month's release manager in a 30-minute sync.

The release manager role is **not** a permanent role. It is also not an opportunity to ship unreviewed changes — every change on a release branch still goes through PR and CODEOWNERS review (see [Pull requests and code review](./pull-requests-and-code-review.md)).

## 3. Release Branch Lifecycle

1. **Cut.** On the first business day of release week, the release manager cuts `release/<YYYY.MM>` from `main`. The cut is a fast-forward to the latest green `main`.

   ```bash
   # fictional/simulated command
   git checkout main
   git pull --ff-only origin main
   git push origin main:refs/heads/release/2026.10
   ```

2. **Stabilize.** For up to 3 business days, only bug fixes land on the release branch. Each fix is a separate PR following [commit message conventions](./commit-message-conventions.md), merged with a fast-forward.

3. **Tag.** When staging sign-off is in, the release manager tags `v<YYYY.MM>.<patch>` (e.g., `v2026.10.0` for the first release of October 2026).

   ```bash
   # fictional/simulated command
   git tag -a v2026.10.0 -m "ACME Cloud v2026.10.0"
   git push origin v2026.10.0
   ```

4. **Canary.** The tag triggers the `release.yml` workflow which promotes the image to staging, then waits for the production canary approvals (see [CI/CD overview](./ci-cd-overview.md)).

5. **Promote.** The release manager drives the canary ramps: 5% → 25% → 100%, with SLO watch between ramps (see below).

6. **Publish.** The release manager publishes the customer release notes to `https://docs.acme.example/cloud/changelog` (fictional) and the internal notes to `docs/releases/<YYYY.MM>.md` in the repository.

7. **Handoff.** A 30-minute sync with the next month's release manager covers open issues, deferred cherry-picks, and known regressions.

8. **Sunset.** A release branch is retained for **60 days** after the release ships, then deleted. Hotfixes during that window land on the branch and ship as patch releases.

## 4. Release Notes

Release notes are **auto-generated** from Conventional Commit titles on the squash commits since the last release (see [Commit message conventions](./commit-message-conventions.md)). The release manager's job is to:

1. Review the auto-generated draft for accuracy.
2. Rewrite any commit titles that don't read well to customers.
3. Add a "Breaking changes" section at the top if any `feat(scope)!: ...` commits landed.
4. Add a "Known issues" section if the release shipped with a known regression (with a ticket link and a workaround).
5. Add a "Deprecations" section for any APIs marked deprecated in this release.

The customer-facing version is published to `https://docs.acme.example/<product>/changelog`. The internal version, with additional context (SLO deltas, perf deltas, ADR links), is committed to `docs/releases/<YYYY.MM>.md` in the repository.

### Sample release notes excerpt

```markdown
# ACME Cloud v2026.10.0

Released 2026-10-07. Release manager: Anjali Desai.

## Breaking changes

- The deprecated `v1beta1` tenant endpoints are removed. Migrate to `v1`
  by following `docs/migration/v1beta1-to-v1.md`. (CLOUD-1101)

## New features

- `feat(quota)`: `POST /v1/tenants/{id}/quota` now accepts a
  `dry_run=true` parameter to validate a quota change without applying it.
  (CLOUD-1287)
- `feat(billing)`: Billing events now include a `region` field. (CLOUD-1310)

## Bug fixes

- `fix(auth)`: Token refresh now happens before expiry, not after. (CLOUD-1301)

## Deprecations

- `GET /v1beta1/tenants` is deprecated and will be removed in v2027.04.
  Migrate to `GET /v1/tenants`. (CLOUD-1350)
```

## 5. Canary Deployments

Production deploys use a **canary** strategy with three ramps. The release manager makes the go/no-go decision at each ramp using the SLO watch.

### Ramp 1: 5% canary

- Deploy to 5% of production pods in each region.
- Wait **10 minutes**.
- The SLO watch job checks: error budget burn rate < 2× baseline, p99 latency < 1.5× baseline, no new error logs.
- If pass → ramp to 25%. If fail → **rollback immediately** (see §6).

### Ramp 2: 25% canary

- Deploy to 25% of production pods.
- Wait **30 minutes**.
- Same SLO watch criteria.
- If pass → ramp to 100%. If fail → **rollback immediately**.

### Ramp 3: 100% rollout

- Deploy to the remaining 75%.
- Watch for **2 hours** post-deploy.
- If a regression appears in the watch window, follow the rollback runbook.

```bash
# fictional/simulated command — canary 5% then watch
make release-canary ENV=prod IMG=registry.internal.acme.example/acme-cloud/api:v2026.10.0 PERCENT=5
make release-watch ENV=prod WINDOW=10m

# fictional/simulated command — ramp to 25%
make release-canary ENV=prod IMG=... PERCENT=25
make release-watch ENV=prod WINDOW=30m

# fictional/simulated command — ramp to 100%
make release-canary ENV=prod IMG=... PERCENT=100
make release-watch ENV=prod WINDOW=2h
```

### Production access

**No new employee gets standing production access.** The release manager's promotion authority is itself a PIM-elevated role, granted for the release window only and expiring automatically after. The `release.yml` workflow's `production` environment requires dual approval: the PIM-elevated release manager and the PIM-elevated on-call SRE. See [`./development-staging-production.md`](./development-staging-production.md) and [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md).

## 6. Rollback Runbook

If the canary fails at any ramp, the release manager rolls back immediately. The rollback is **always** one of:

1. **Image rollback.** Redeploy the previous tagged image to 100% of pods.

   ```bash
   # fictional/simulated command
   make release-rollback ENV=prod IMG=registry.internal.acme.example/acme-cloud/api:v2026.09.3
   ```

2. **Config rollback.** If the change was config-only, revert the config map and reload.
3. **Feature flag off.** If the change was behind a feature flag, flip the flag off — no redeploy.
4. **Revert commit.** As a last resort, revert the offending squash commit on `main` and ship a patch release.

The rollback is recorded in the incident channel (see [Incident response](./incident-response-and-on-call-introduction.md)). A failed canary that triggered a rollback requires a postmortem within 5 business days if customer impact occurred.

### Rollback checklist

- [ ] Confirm the rollback target image is green on staging.
- [ ] Page the on-call SRE (if not already paged).
- [ ] Roll back in all regions, not just the canary region.
- [ ] Verify SLO recovery on the rolled-back version.
- [ ] File a rollback ticket with the trace IDs that triggered the rollback.
- [ ] Schedule a postmortem (if SEV1/SEV2).

## 7. Customer Communication

Customer communication during a release is the responsibility of the release manager, with support from DevRel.

| Event | Channel | Owner | SLA |
|-------|---------|-------|-----|
| Scheduled release ships | `status.acme.example` changelog + email to `customers@acme.example` | Release manager + DevRel | Within 1 business day of ship |
| Canary rollback (no customer impact) | Internal only, `#releases` Slack | Release manager | Within 4 business hours |
| Production incident (SEV1/SEV2) | `status.acme.example` incident post + email | Incident commander | Initial within 15 min; updates every 30 min |
| Post-incident | `status.acme.example` postmortem summary | Incident commander | Within 5 business days |

Status-page updates use the templates in `acme-shared-libraries/comms/status-page-templates.md`.

## 8. Code-Freeze Windows

ACME has two code-freeze windows:

1. **Release-week freeze.** During the release week for a product, the corresponding `main` is **soft-frozen**: only bug fixes and security fixes land. New features are deferred to the next week. The freeze is enforced by a `release-freeze` label on `main` that requires the release manager's approval on every PR.
2. **Holiday freeze.** From **December 15 to January 5** every year, all `main` branches across all products are **hard-frozen**: only P0 security fixes and SEV1 incident hotfixes land. The freeze is announced two weeks in advance by the VP Engineering (Sridhar Venkatesh).

A code freeze is **not** a deployment freeze — production can still receive hotfixes during the freeze, but the bar for landing on `main` is higher.

## 9. Hotfix Procedure

A hotfix is an urgent fix to a released version, typically for a SEV1 incident.

1. Branch from `release/<YYYY.MM>` (the latest release branch).

   ```bash
   # fictional/simulated command
   git checkout release/2026.10
   git checkout -b hotfix/CLOUD-1301-token-refresh
   ```

2. Make the fix as a small, focused PR following [commit message conventions](./commit-message-conventions.md) (`fix(...)`).
3. Get the **2-reviewer minimum** plus Security GRC if the bug is security-sensitive. The hotfix PR is allowed to skip the buddy review convention; blocking CODEOWNERS review is still required.
4. Merge to the release branch (fast-forward).
5. Tag the patch version (`v2026.10.1`).
6. **Cherry-pick** to `main` within one business day — the audit trail requires the fix to also land on `main`.

   ```bash
   # fictional/simulated command
   git checkout main
   git cherry-pick -x <hotfix-sha>
   ```

7. Drive the canary to production following §5.

## 10. Sample Release Calendar (One Quarter)

| Week | Cloud | Workspace | Intelligence | Shared libs |
|------|-------|-----------|--------------|-------------|
| Q1 W1 (Jan) | Minor v2027.01 | — | — | — |
| Q1 W2 (Jan) | — | Minor v2027.01 | — | — |
| Q1 W3 (Jan) | — | — | Minor v2027.01 | — |
| Q1 W4 (Jan) | — | — | — | Minor v2027.01 |
| Q1 W5–W8 (Feb) | Patch / hotfix | Patch / hotfix | Patch / hotfix | Patch |
| Q1 W9 (Mar) | Minor v2027.03 | Minor v2027.03 | Minor v2027.03 | Minor v2027.03 |
| Q1 W10–W12 (Mar) | Patch / hotfix | Patch / hotfix | Patch / hotfix | Patch |

Quarterly **major** releases land in W1 (Cloud), W2 (Workspace), W3 (Intelligence), W4 (shared libs) of January, April, July, October.

## 11. Cross-Reference Table

| Need | See |
|------|-----|
| CI/CD pipeline and the canary job | [`./ci-cd-overview.md`](./ci-cd-overview.md) |
| Environment gating and PIM | [`./development-staging-production.md`](./development-staging-production.md) |
| Branch model for `release/*` | [`./git-branching-strategy.md`](./git-branching-strategy.md) |
| Conventional Commit titles for changelog | [`./commit-message-conventions.md`](./commit-message-conventions.md) |
| Incident response and rollback triggers | [`./incident-response-and-on-call-introduction.md`](./incident-response-and-on-call-introduction.md) |
| Observability and SLO watch | [`./observability-and-logging.md`](./observability-and-logging.md) |
| Per-repo release runbooks | [`../repositories/acme-cloud-api.md`](../repositories/acme-cloud-api.md), [`../repositories/acme-workspace-api.md`](../repositories/acme-workspace-api.md) |
| Least-privilege policy basis | [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md) |

## Related Documents

- [`../repository-catalog.md`](../repository-catalog.md)
- [`./git-branching-strategy.md`](./git-branching-strategy.md)
- [`./pull-requests-and-code-review.md`](./pull-requests-and-code-review.md)
- [`./commit-message-conventions.md`](./commit-message-conventions.md)
- [`./ci-cd-overview.md`](./ci-cd-overview.md)
- [`./observability-and-logging.md`](./observability-and-logging.md)
- [`./development-staging-production.md`](./development-staging-production.md)
- [`./incident-response-and-on-call-introduction.md`](./incident-response-and-on-call-introduction.md)
- [`../repositories/acme-cloud-api.md`](../repositories/acme-cloud-api.md)
- [`../repositories/acme-workspace-api.md`](../repositories/acme-workspace-api.md)
- [`../repositories/acme-intelligence-inference.md`](../repositories/acme-intelligence-inference.md)
- [`../repositories/acme-shared-libraries.md`](../repositories/acme-shared-libraries.md)
- [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md)
- [`../../03-security/secrets-management.md`](../../03-security/secrets-management.md)
- [`../../03-security/security-incident-reporting.md`](../../03-security/security-incident-reporting.md)
- [`../../09-contacts/contact-directory.md`](../../09-contacts/contact-directory.md)
- [`../../metadata/glossary.md`](../../metadata/glossary.md)
