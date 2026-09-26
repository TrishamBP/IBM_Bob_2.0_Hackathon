---
document_id: ACME-ENG-005
title: Commit Message Conventions
category: engineering
department: engineering
applicable_roles: [engineers]
owner: Engineering
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [engineering, practices, commit-messages, conventional-commits]
---

# Commit Message Conventions

> All Git hosts and issue trackers referenced here are fictional. Sample commands and messages are for onboarding orientation.

ACME Corp uses **Conventional Commits 1.0.0** for all repositories. The CI `commit-lint` job enforces the format on the squash-merge commit that lands on `main` (see [`./ci-cd-overview.md`](./ci-cd-overview.md)).

## 1. Why Conventional Commits?

- **Machine-parseable history.** Auto-generated release notes, changelogs, and semantic-version bumps rely on consistent prefixes.
- **Auditable blast radius.** A `feat` in `proto/` is a public API change; `chore` in `.github/` is not. Reviewers triage accordingly.
- **Rollback target.** Reverting a single squash commit is a reliable rollback primitive (see [`./release-management.md`](./release-management.md)).
- **Cross-repo coordination.** Stacked PRs across Cloud, Intelligence, Workspace repositories can be correlated by the linked ticket in the footer.

## 2. Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

- **type** — required. One of: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`, `style`, `revert`.
- **scope** — optional but encouraged. A noun identifying the area of the change (`quota`, `auth`, `ui`, `helm`, `proto`).
- **subject** — required. Short, imperative, lowercase, no trailing period, **≤ 72 characters**.
- **body** — optional. Explain **why**, not what. Wrap at 100 characters.
- **footer** — optional. Breaking changes, ticket links, attribution, sign-off.

## 3. Allowed Types

| Type | When to use | Example |
|------|-------------|---------|
| `feat` | New user-facing or public API functionality | `feat(quota): reject create-tenant when region quota exceeded` |
| `fix` | Bug fix | `fix(auth): refresh token before expiry, not after` |
| `docs` | Documentation only | `docs(runbook): document the canary rollback procedure` |
| `refactor` | Code restructuring without behavior change | `refactor(quota): extract checker from policy engine` |
| `test` | Test-only change | `test(quota): add table-driven tests for region edge cases` |
| `chore` | Build, deps, config — not user-visible | `chore(deps): bump github.com/grpc/grpc-go to v1.66.0` |
| `perf` | Performance improvement | `perf(tenant): cache lookup reduces p99 by 18ms` |
| `ci` | CI/CD pipeline change | `ci(go): cache module downloads across jobs` |
| `build` | Build-system change (rare at ACME — `chore(deps)` is preferred) | `build(make): parallelize test targets` |
| `style` | Formatting only — usually produced by formatters, not hand-written | `style(go): gofmt after go 1.22 upgrade` |
| `revert` | Reverting a previous commit | `revert: feat(quota): reject create-tenant...` |

## 4. Subject Rules

- **Imperative mood.** "add", "fix", "reject" — not "added", "fixes", "rejected".
- **Lowercase first letter.** `feat(quota): reject...` not `feat(quota): Reject...`.
- **No trailing period.**
- **≤ 72 characters.** The CI commit-lint job will reject longer subjects. The 72-char limit is on the *subject*; the body may be wider.
- **Reference the impact, not the implementation.** "reject create-tenant when region quota exceeded" beats "add if-check before tenant insert".

## 5. Body

The body explains **why** the change is needed and what trade-offs were considered. The git diff already says *what* changed.

Sample:

```
feat(quota): reject create-tenant when region quota exceeded

Previously, create-tenant would succeed and the new tenant would
silently inherit an over-quota state, surfacing as 429s only on the
first resource call. Customers saw this as an inconsistent API.

This change makes create-tenant fail-fast with FAILED_PRECONDITION
when the region is at quota. The check uses the existing cached
quota snapshot; a new cache miss triggers a synchronous refresh.

Trade-offs considered:
- Returning QUOTA_EXHAUSTED instead: rejected because the regional
  limit is not the tenant's own quota.
- Rejecting at the billing layer: rejected because billing is
  asynchronous and would surface the error minutes later.
```

## 6. Footer — Breaking Changes and Ticket Links

### 6.1 Breaking changes

A breaking change uses `!` after the type/scope **and** a `BREAKING CHANGE:` footer.

```
feat(api)!: drop deprecated v1beta1 tenant endpoints

BREAKING CHANGE: The v1beta1 tenant endpoints were deprecated in
v2025.10 and are now removed. Migrate to v1 by following
docs/migration/v1beta1-to-v1.md. Customers still using v1beta1
will receive 404 starting in v2026.10.
```

Breaking changes additionally require:

- A Security GRC ticket reference.
- An ADR (architecture decision record) in `docs/adr/`.
- A `breaking-change` label on the PR.
- Approval from at least one EM in the affected product.

### 6.2 Ticket links

The footer is the canonical place for ticket references. Use the `Refs:`, `Closes:`, `Fixes:`, or `Resolves:` keyword depending on intent:

```
Closes: CLOUD-1287
Refs: CLOUD-1199
```

`Closes:` / `Fixes:` / `Resolves:` will auto-close the ticket on merge. `Refs:` will only link.

### 6.3 Attribution and sign-off

Co-authors (pair programming, AI assistant used as a tool — see [`../../03-security/ai-tool-acceptable-use.md`](../../03-security/ai-tool-acceptable-use.md)) use the standard trailer format:

```
Co-authored-by: Priya Menon <priya.menon@acme.example>
Co-authored-by: acme-coding-assistant <assistant@acme.example>
```

The `Signed-off-by:` trailer is added by the squash-merge action on every commit landing on `main`, providing the audit trail required by [`../../03-security/source-code-security.md`](../../03-security/source-code-security.md).

## 7. Multi-Commit Feature Branches

On a feature branch you may make as many commits as you like. They will be squashed on merge. The squash commit title is taken from your **PR title**, not from any individual commit. Therefore:

- Keep the PR title Conventional-Commits-compliant.
- Use individual commit messages to communicate progress to your reviewers (e.g., `wip: add tests for quota edge cases`).

After squash-merge, the original branch commits are no longer visible on `main` — recoverable only from the PR page.

## 8. Release Branch Bugfixes

Release branches use **fast-forward merges only** (see [`./git-branching-strategy.md`](./git-branching-strategy.md)). Each individual bugfix commit on a release branch must itself follow Conventional Commits. Example:

```
fix(auth): refresh token before expiry, not after

The refresh logic checked expiry AFTER the access call, so a token
expiring mid-request caused a 401 cascade. Move the refresh check
before the call. Add a regression test.

Closes: CLOUD-1301
Signed-off-by: Anjali Desai <anjali.desai@acme.example>
```

Cherry-picking this commit back to `main` preserves the message and audit trail.

## 9. Sample Commit (End-to-End)

```bash
# fictional/simulated command — write the squash commit message to a file
cat > /tmp/commit-msg <<'EOF'
feat(quota): reject create-tenant when region quota exceeded

Previously, create-tenant would succeed and the new tenant would
silently inherit an over-quota state, surfacing as 429s only on
the first resource call. Customers saw this as an inconsistent API.

This change makes create-tenant fail-fast with FAILED_PRECONDITION
when the region is at quota. The check uses the existing cached
quota snapshot; a new cache miss triggers a synchronous refresh.

Closes: CLOUD-1287
Refs: CLOUD-1199
Co-authored-by: Priya Menon <priya.menon@acme.example>
Signed-off-by: Anjali Desai <anjali.desai@acme.example>
EOF

# fictional/simulated command — squash and merge (typically done via GitHub UI)
git commit -F /tmp/commit-msg
```

## 10. Anti-Patterns

| Anti-pattern | Why it's wrong | Fix |
|--------------|----------------|-----|
| `Update README.md` | No type, no scope, no why | `docs(readme): clarify local setup step 7` |
| `Fixed bug` | Vague, no type | `fix(auth): refresh token before expiry, not after` |
| `feat: Added a new endpoint that returns tenant quota as a JSON object with a 200 status code when the tenant exists and a 404 when it doesn't` | Too long, mixed case, period | `feat(quota): expose GET /v1/tenants/{id}/quota` |
| `wip` on `main` | squash-merge should not produce wip | Set the PR title before merge |
| `chore: stuff` | Vague scope/subject | `chore(deps): bump github.com/grpc/grpc-go to v1.66.0` |
| Body that restates the diff | Wastes reviewer time | Explain why, alternatives considered |
| Footer missing on a breaking change | Auditors cannot trace | Use `feat(api)!: ...` + `BREAKING CHANGE:` |
| Multiple types in one subject (`feat/fix`) | Ambiguous | Split into two PRs |

## 11. Verification

The `commit-lint` CI job runs on every PR. It checks:

- Subject matches `^(feat|fix|docs|refactor|test|chore|perf|ci|build|style|revert)(\([\w-]+\))?(!)?: .{1,72}$`
- Body (if present) wraps at 100 characters.
- Footer lines (if present) match `^(BREAKING CHANGE:|[A-Za-z-]+:|Co-authored-by:|Signed-off-by:) .+`.
- No `wip`, `tmp`, `fixme`, `tbd` in the subject.

Failures block merge. See [`./pull-requests-and-code-review.md`](./pull-requests-and-code-review.md) for the approval gate.

## 12. Auto-Generated Changelog

Each release, the `release-notes` job in CI scans the squash commits since the last tag and produces a categorized changelog:

- `feat` → **New features**
- `fix` → **Bug fixes**
- `perf` → **Performance**
- `docs` → **Documentation**
- `refactor` → **Internal**
- Breaking changes are pulled to the top under **Breaking changes**.

The generated changelog is published to `docs/releases/<YYYY.MM>.md` in the repository, and the highlights are summarized in the customer release notes — see [`./release-management.md`](./release-management.md).

## Related Documents

- [`../repository-catalog.md`](../repository-catalog.md)
- [`./git-branching-strategy.md`](./git-branching-strategy.md)
- [`./pull-requests-and-code-review.md`](./pull-requests-and-code-review.md)
- [`./coding-standards.md`](./coding-standards.md)
- [`./ci-cd-overview.md`](./ci-cd-overview.md)
- [`./release-management.md`](./release-management.md)
- [`../../03-security/source-code-security.md`](../../03-security/source-code-security.md)
- [`../../03-security/ai-tool-acceptable-use.md`](../../03-security/ai-tool-acceptable-use.md)
- [`../../metadata/glossary.md`](../../metadata/glossary.md)
