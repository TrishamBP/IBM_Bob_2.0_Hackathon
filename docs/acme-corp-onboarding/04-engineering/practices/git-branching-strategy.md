---
document_id: ACME-ENG-002
title: Git Branching Strategy
category: engineering
department: engineering
applicable_roles: [engineers]
owner: Engineering
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [engineering, practices, git, branching, trunk-based]
---

# Git Branching Strategy

> All Git hosts and runners referenced here are fictional. `git.acme.example` does not resolve and the commands shown are **simulated** for onboarding orientation only.

## 1. Why Trunk-Based?

ACME Corp uses a **trunk-based development** model. Trunk-based development keeps the entire engineering organization working from a single, always-deployable `main` branch and short-lived feature branches. Compared with long-lived Git-flow style branches, trunk-based development:

- Reduces merge conflicts and integration risk.
- Shortens the time between "code written" and "code running in production."
- Forces small, reviewable changes.
- Makes the deployment pipeline the canonical source of truth for what is in production.

For background on which repository uses which stack, see the [repository catalog](../repository-catalog.md).

## 2. Branch Model

| Branch type | Naming pattern | Lifetime | Purpose | Merge strategy |
|-------------|----------------|----------|---------|----------------|
| Trunk | `main` | Permanent | Always-green, always-deployable | n/a (target) |
| Feature | `feat/<jira-id>-<slug>` | ≤ 3 days | New functionality | Squash merge |
| Bugfix | `fix/<jira-id>-<slug>` | ≤ 3 days | Non-urgent defect fix | Squash merge |
| Hotfix | `hotfix/<jira-id>-<slug>` | ≤ 1 day | Urgent production fix | Squash merge |
| Release | `release/<YYYY.MM>` | 30–60 days | Stabilize a monthly minor release | Fast-forward only |
| Chore | `chore/<slug>` | ≤ 1 day | Refactor, dependency bump, build glue | Squash merge |

**No long-lived `develop` branch.** A `develop` branch is treated as a bug and removed on sight.

## 3. Trunk Protection Rules

`main` is protected by GitHub Enterprise branch protection. The following rules are enforced on every ACME repository:

- **No direct commits.** All changes land via pull request. The only exception is a security patch applied by Security GRC during an active incident, and that patch is reverted or replaced within 24 hours by a normal PR.
- **Force-push forbidden.** History rewrite on `main` or any `release/*` branch is blocked at the host level. Even administrators cannot bypass this.
- **Required status checks.** See [CI/CD overview](./ci-cd-overview.md) for the full list. Trunk requires a green build before any merge.
- **Required reviewers.** See [Pull requests and code review](./pull-requests-and-code-review.md).
- **Linear history.** Merge commits are disallowed on `main`; only squash-merge or fast-forward is permitted.

## 4. Feature Branch Lifecycle

A feature branch is expected to live **no more than 3 working days**. If a branch is older than 5 days, the CODEOWNERS team is notified automatically by a scheduled action and the branch is candidate for closure.

1. Branch from latest `main`:

   ```bash
   # fictional/simulated command
   git checkout main
   git pull --ff-only origin main
   git checkout -b feat/CLOUD-1287-tenant-quota-check
   ```

2. Make small, logically grouped commits following [commit message conventions](./commit-message-conventions.md).

3. Rebase onto latest `main` before opening the PR and again before merge:

   ```bash
   # fictional/simulated command
   git fetch origin
   git rebase origin/main
   # resolve conflicts, run tests
   make test  # fictional/simulated
   ```

4. Open the PR using the template in [Pull requests and code review](./pull-requests-and-code-review.md).
5. After all checks pass and reviewers approve, **squash-merge** the PR. The squash commit message follows Conventional Commits.
6. Delete the feature branch from the remote after merge (GitHub does this automatically).

## 5. Release Branches

A release branch is cut from `main` on the **first business day of each month** for each product, following the [release management](./release-management.md) cadence.

- Naming: `release/<YYYY.MM>` — for example, `release/2026.10`.
- The release manager for that month is the only person permitted to push commits to a release branch (bugfixes only — no new features).
- Release branches accept **fast-forward merges only**. No squash, no merge commit. This preserves a clean history for cherry-picks.
- Hotfixes applied to a release branch must be cherry-picked back to `main` within one business day.
- A release branch is deleted 60 days after the release ships, after the postmortem window for any regression has closed.

## 6. Rebase Before Merge

**Always rebase your feature branch onto the latest `main` before merging.** This ensures:

- Linear history on `main`.
- The CI run that approved your change reflects the latest trunk state, not a stale snapshot.
- Reviewers see the actual diff that will land.

If your branch has been open long enough that rebasing produces conflicts, prefer splitting the PR into smaller ones rather than producing a giant conflict-resolution commit.

## 7. Merge Strategy Summary

| Source → Target | Strategy | Why |
|------------------|----------|-----|
| `feat/*` → `main` | Squash merge | Collapses noisy WIP commits into one reviewable change |
| `fix/*` → `main` | Squash merge | Same as features |
| `hotfix/*` → `release/*` | Squash merge | Same as features; cherry-pick to `main` after |
| `release/*` → `release/*` (bugfix) | Fast-forward only | Clean history for cherry-picks |
| `main` → `release/*` (backmerge) | Fast-forward only | Rare; only for picking up shared infra fixes |
| Any → `main` | Merge commit | **Forbidden** — keep history linear |

## 8. Forbidden Practices

The following are blocked by branch protection, by CI policy, or by review:

- **Force-push** to `main` or any `release/*`.
- **Direct push** to `main`.
- **Long-lived `develop` / `integration` branches.**
- **Merging without all required status checks green.**
- **Bypassing CODEOWNERS review.**
- **Reverting a security patch** without Security GRC acknowledgment.
- **Merging a PR you authored** (no self-merges — see [Pull requests and code review](./pull-requests-and-code-review.md)).
- **Commented-out code in merged changes** (see [Coding standards](./coding-standards.md)).

## 9. Cross-Repository Considerations

ACME has three products (Cloud, Intelligence, Workspace) and shared platform/QE libraries. A change that touches more than one repository is rare and should be coordinated via:

1. A tracking ticket in the ITSM portal (fictional: `https://itsm.acme.example`).
2. Stacked PRs across the involved repositories, merged in dependency order.
3. A clear note in each PR linking to the others and listing the merge order.

The repository catalog at [`../repository-catalog.md`](../repository-catalog.md) is the source of truth for which repository owns which surface area.

## 10. Sample Workflow (End-to-End)

```bash
# fictional/simulated commands — end-to-end feature flow

# 1. Branch
git checkout main && git pull --ff-only
git checkout -b feat/CLOUD-1287-tenant-quota-check

# 2. Code, commit (Conventional Commits — see commit-message-conventions.md)
git add internal/quota/check.go
git commit -m "feat(quota): reject create-tenant when region quota exceeded"

# 3. Push and open PR (PR template applied automatically by GitHub)
git push -u origin feat/CLOUD-1287-tenant-quota-check
# Open PR at https://git.acme.example/acme-cloud/acme-cloud-api/pull/... (fictional)

# 4. Rebase before merge
git fetch origin
git rebase origin/main
make test  # fictional/simulated
git push --force-with-lease  # allowed on feature branches only

# 5. Squash-merge via GitHub UI; delete branch on merge
```

## 11. Common Mistakes to Avoid

- **Rebasing a shared feature branch** that someone else has pulled. Coordinate with your co-authors first.
- **Forgetting to pull `main` before branching.** You will end up rebasing anyway; save a step.
- **Naming branches `feature/foo` instead of `feat/foo`.** The CI commit-lint job rejects non-Conventional prefixes.
- **Leaving a feature branch open for a week.** Schedule a rebase reminder; split the PR if scope grew.
- **Squashing a release branch bugfix into one commit.** Release branches are fast-forward only — push individual commits.

## Related Documents

- [`../repository-catalog.md`](../repository-catalog.md)
- [`../developer-workstation-setup.md`](../developer-workstation-setup.md)
- [`../source-code-and-repository-access.md`](../source-code-and-repository-access.md)
- [`./pull-requests-and-code-review.md`](./pull-requests-and-code-review.md)
- [`./coding-standards.md`](./coding-standards.md)
- [`./commit-message-conventions.md`](./commit-message-conventions.md)
- [`./ci-cd-overview.md`](./ci-cd-overview.md)
- [`./release-management.md`](./release-management.md)
- [`../repositories/acme-cloud-api.md`](../repositories/acme-cloud-api.md)
- [`../repositories/acme-shared-libraries.md`](../repositories/acme-shared-libraries.md)
- [`../../03-security/source-code-security.md`](../../03-security/source-code-security.md)
- [`../../08-forms/repository-access-request.md`](../../08-forms/repository-access-request.md)
- [`../../09-contacts/contact-directory.md`](../../09-contacts/contact-directory.md)
- [`../../metadata/glossary.md`](../../metadata/glossary.md)
