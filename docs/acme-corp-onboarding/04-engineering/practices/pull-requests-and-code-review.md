---
document_id: ACME-ENG-003
title: Pull Requests and Code Review
category: engineering
department: engineering
applicable_roles: [engineers]
owner: Engineering
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [engineering, practices, pull-requests, code-review]
---

# Pull Requests and Code Review

> All Git hosts and runners referenced here are fictional. The PR template and CODEOWNERS snippets below are samples for onboarding orientation.

Every change to an ACME repository lands through a pull request. There are no direct commits to `main`. The pull request is the unit of code review, the unit of CI verification, and the unit of audit trail.

## 1. PR Template

Every ACME repository ships a `.github/PULL_REQUEST_TEMPLATE.md` file. The template is enforced by GitHub Enterprise and applied automatically when a PR is opened.

```markdown
## Summary
<!-- One or two sentences describing what this PR does and why. -->

## Type of change
- [ ] feat — new functionality
- [ ] fix — bug fix
- [ ] docs — documentation only
- [ ] refactor — non-functional change
- [ ] test — test-only change
- [ ] chore — build, deps, config
- [ ] perf — performance improvement
- [ ] ci — CI/CD pipeline change

## Linked tickets
- CLOUD-1287
- (none)

## Test plan
<!-- What did you run to verify this change? List commands, environments, and results. -->

- [ ] Unit tests pass locally (`make test`)
- [ ] Integration tests pass locally (`make test-integration`)
- [ ] Manual smoke in dev environment
- [ ] New tests added for edge cases

## Screenshots / recordings
<!-- For UI changes, attach a screenshot or short recording. For API changes, attach a sample request/response. -->

## Risk assessment
<!-- Could this change break production? How? What is the rollback? -->
- Blast radius:
- Rollback plan:
- Feature flag required: yes / no

## Reviewer notes
<!-- Anything reviewers should pay extra attention to. -->

## Checklist
- [ ] Conventional Commit prefix on the squash commit title
- [ ] No commented-out code
- [ ] No secrets, PII, or customer data
- [ ] Public API change → `proto/` updated and `buf breaking` green
- [ ] Documentation updated
```

## 2. Required Reviewers and CODEOWNERS

Each repository ships a `.github/CODEOWNERS` file. Branch protection requires every PR to be approved by **every** owning team listed for the touched paths.

Sample `CODEOWNERS` for `acme-cloud-api`:

```text
*                                       @acme/cloud-api
/proto/                                  @acme/cloud-api-leads
/internal/quota/                         @acme/cloud-api @acme/security-grc
/internal/billing/                       @acme/cloud-api @acme/security-grc
/deploy/terraform/                       @acme/cloud-api @acme/platform
/docs/                                   @acme/cloud-api @acme/devrel
```

CODEOWNERS review is **blocking**. There is no override without a Security GRC ticket. See [`../../03-security/source-code-security.md`](../../03-security/source-code-security.md) for the policy basis.

## 3. Reviewer Minimums

| Repository tier | Minimum approving reviews | Notes |
|------------------|----------------------------|-------|
| Production-deploy repositories (all of Cloud, Intelligence, Workspace, Platform infra) | **2** | At least one must be from the home team; one may be a buddy from a sibling team. |
| Shared libraries (`acme-shared-libraries`) | **2** | One must be from Platform Infrastructure; the other from any consuming team. |
| QE / automation (`acme-quality-automation`) | **1** | QE team member required. |
| Docs-only repositories | **1** | Any CODEOWNER. |

**No new employee gets standing production access**, including the implicit "merge-button" access that production-deploy repositories grant to their maintainers. New engineers are added to a CODEOWNERS team only after the first-30-day checkpoint described in [`../../07-workflows/first-30-days.md`](../../07-workflows/first-30-days.md).

## 4. Self-Merge Policy

You may not merge a PR that you authored. This is enforced at the branch-protection layer ("Require review from someone other than the author"). If you are blocked and your reviewers are unavailable for more than one business day, escalate to your EM (see [`../../09-contacts/contact-directory.md`](../../09-contacts/contact-directory.md)) rather than self-merging.

## 5. Buddy Review vs. Blocking Review

ACME distinguishes two kinds of review:

| Kind | Triggered by | Effect | Examples |
|------|--------------|--------|----------|
| **Blocking review** | CODEOWNERS rule | PR cannot merge until that reviewer approves | `@acme/cloud-api-leads` on `/proto/`, `@acme/security-grc` on `/internal/quota/` |
| **Buddy review** | Best-practice convention | PR can merge with one home-team approval, but you should request a second opinion | Cross-team UI change; new public API surface; perf-sensitive path |

A buddy review is requested by adding the second reviewer as a reviewer in the GitHub UI and `@`-mentioning them in the PR description. The PR description should explain why the buddy review is requested (e.g., "Adding a new SLO metric — tagging @platform on the buddy review since they own the metrics schema").

## 6. Stale-Review Policy

Reviews are not eternal. The following rules apply:

- A review older than **3 business days** is automatically marked **stale** by a scheduled GitHub Action. The PR author must request a re-review.
- A stale review blocks merge until a fresh approval is recorded.
- A PR open for more than **5 business days** triggers an automatic reminder to the owning EM.
- A PR open for more than **10 business days** is automatically closed by the stale-PR bot, with a comment asking the author to reopen or rebase.
- A reviewer who has not responded in **2 business days** should be `@`-mentioned; if still no response after another business day, request an alternate reviewer from the same CODEOWNERS team.

## 7. Review Etiquette

ACME's review etiquette, distilled:

- **Comment on the code, not the person.** "This loop will O(n²) on a 10k-row tenant table" — not "you wrote an O(n²) loop here."
- **Ask questions before asserting.** "Did you consider using `context.WithTimeout` here?" beats "Use `context.WithTimeout` here."
- **Distinguish blocking from nitpick.** Prefix optional comments with `nit:` so the author knows they can skip.
- **Approve explicitly.** Approving with a request for changes cancels the approval. Use the "Request changes" button deliberately.
- **Acknowledge feedback before pushing.** Reply to each comment with "done," "fixed in <sha>," or "disagree because <reason>."
- **Don't rebase over an active review.** Wait until all reviewers have responded, then rebase and ask for a final review.
- **Time-box review.** Reviewers are expected to respond within 1 business day for normal PRs and within 2 hours for hotfix PRs during a SEV1/SEV2 incident.

## 8. Approval Gate and Required Status Checks

In addition to required reviews, the PR must be green on all required status checks before merge. The list is documented in [`./ci-cd-overview.md`](./ci-cd-overview.md). A failing check blocks merge, regardless of reviewer approval.

## 9. Force-Push and Rebase Discipline

Feature branches may be force-pushed (with `--force-with-lease`) to keep history clean and trigger a fresh CI run after a rebase. `main` and `release/*` may never be force-pushed. See [`./git-branching-strategy.md`](./git-branching-strategy.md) for details.

After a force-push, all previous reviews are marked stale and must be re-requested. This is by design: a rebase can silently change semantics.

## 10. Sample PR Lifecycle (End-to-End)

```text
Day 0, 10:00 — Author opens PR with filled-in template.
Day 0, 10:05 — GitHub assigns CODEOWNERS reviewers.
Day 0, 10:10 — CI kicks off; first review comment arrives within 2h.
Day 1, 09:00 — Author addresses comments, force-pushes (with --force-with-lease) after rebase.
Day 1, 09:05 — Stale-review bot marks previous approvals stale.
Day 1, 15:00 — Second approval recorded. CI green.
Day 1, 15:05 — Author squashes and merges. Branch deleted.
Day 1, 15:10 — Deploy pipeline promotes to dev automatically; staging waits for tag.
```

## 11. Special: Security-Sensitive PRs

PRs touching any of the following trigger an **automatic** Security GRC review:

- `/proto/` (public API surface)
- `/internal/quota/`, `/internal/billing/`, `/internal/auth/`
- `/deploy/terraform/` (production infra)
- `go.mod`, `package.json`, `requirements.txt`, `pom.xml` (dependency changes — see [`../../03-security/open-source-dependency-security.md`](../../03-security/open-source-dependency-security.md))
- Any path containing `secrets`, `keys`, `credentials`, or `tokens` (regex-based trigger)

Security GRC commits to a **2-business-day** SLA on these PRs. For SEV1/SEV2 incidents, the SLA drops to **2 hours**.

## 12. Sample Review Comment (Good vs. Bad)

**Good (specific, kind, blocking):**

> The retry loop here uses a fixed 100ms backoff. With 10k tenants re-listing at once, we'll see a thundering herd. Recommend `time.Duration = baseBackoff * math.Pow(2, attempt)` with jitter, capped at 5s.

**Bad (vague, harsh, optional masquerading as blocking):**

> This is wrong. Fix the backoff.

## Related Documents

- [`../repository-catalog.md`](../repository-catalog.md)
- [`./git-branching-strategy.md`](./git-branching-strategy.md)
- [`./coding-standards.md`](./coding-standards.md)
- [`./commit-message-conventions.md`](./commit-message-conventions.md)
- [`./ci-cd-overview.md`](./ci-cd-overview.md)
- [`./unit-and-integration-testing.md`](./unit-and-integration-testing.md)
- [`../repositories/acme-cloud-api.md`](../repositories/acme-cloud-api.md)
- [`../../03-security/source-code-security.md`](../../03-security/source-code-security.md)
- [`../../03-security/open-source-dependency-security.md`](../../03-security/open-source-dependency-security.md)
- [`../../03-security/ai-tool-acceptable-use.md`](../../03-security/ai-tool-acceptable-use.md)
- [`../../07-workflows/first-30-days.md`](../../07-workflows/first-30-days.md)
- [`../../08-forms/repository-access-request.md`](../../08-forms/repository-access-request.md)
- [`../../09-contacts/contact-directory.md`](../../09-contacts/contact-directory.md)
- [`../../metadata/glossary.md`](../../metadata/glossary.md)
