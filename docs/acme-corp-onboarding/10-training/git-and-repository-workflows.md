---
document_id: ACME-TRN-005
title: Git and Repository Workflows
category: training
department: engineering
applicable_roles: [backend-engineer, frontend-engineer, full-stack-engineer, cloud-platform-engineer, devops-engineer, ai-ml-engineer, ai-research-engineer, quality-engineer, customer-support-engineer]
owner: Engineering Enablement
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [training, git, version-control, pull-requests, hands-on-lab]
---

# Git and Repository Workflows (ACME-TRN-005)

> Fictional document. All systems, links, and addresses are illustrative.

## 1. Module Overview

Git and Repository Workflows is the hands-on, lab-driven module that turns a new ACME engineer's conceptual understanding of trunk-based development into operational fluency. The module covers Git fundamentals, the ACME trunk-based branching strategy, commit and PR conventions, CODEOWNERS, conflict resolution, and recovery from common Git mistakes (bad commits, force-push, lost work). The culminating activity is a hands-on lab in the `acme-shared-libraries-sandbox` sandbox repository on `git.acme.example` (fictional) where the learner opens, reviews, and merges a real pull request against a non-production branch.

The module is owned by Engineering Enablement, led by Aditi Ghosh (`aditi.ghosh@acme.example`), and supported by per-business-unit Tech Leads who grade the sandbox PR.

## 2. Learning Objectives

By the end of this module, the engineer will be able to:

1. Initialise, clone, branch, commit, push, and pull a Git repository using both the CLI and the approved GUI (VS Code with GitHub Enterprise integration).
2. Apply the ACME trunk-based branching strategy: short-lived feature branches, rebase before merge, squash-merge into `main`.
3. Write a Conventional-Commits-style message that passes the ACME commit lint rules — see [`../04-engineering/practices/commit-message-conventions.md`](../04-engineering/practices/commit-message-conventions.md).
4. Open a pull request that satisfies CI, code review, and CODEOWNERS rules — see [`../04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md).
5. Resolve a merge conflict cleanly and recover from common Git mistakes (amend, reset, reflog, cherry-pick) without losing work.
6. Demonstrate the workflow end-to-end by opening, reviewing, and merging a PR in the sandbox repository.

## 3. Target Audience

| Role | Required? | Notes |
|---|---|---|
| All engineers (every discipline) | **Mandatory** | Gates first production PR. |
| Engineering Managers / Tech Leads | **Mandatory** | Plus CODEOWNERS configuration lab. |
| Customer Support Engineers (read-only repos) | **Mandatory** | Reduced lab: read-clone-fetch only. |
| Non-engineers | Optional | A 90-minute "Git for PMs" elective is offered. |

## 4. Prerequisites

- Completion of [`engineering-orientation.md`](./engineering-orientation.md) (ACME-TRN-004).
- Completion of [`security-awareness.md`](./security-awareness.md) (ACME-TRN-002).
- Source code & repository access granted — see [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md).
- Acknowledgement of source code security — see [`../03-security/source-code-security.md`](../03-security/source-code-security.md).
- Local Git installed and authenticated to `git.acme.example` via SSO.

## 5. Duration

**Total: 4 hours** (3 hours self-paced + 1 hour hands-on lab, including PR review).

| Block | Duration | Modality |
|---|---|---|
| Git fundamentals refresher | 45 min | Self-paced |
| Trunk-based development & branching | 30 min | Self-paced |
| Commits & PR conventions | 30 min | Self-paced |
| CODEOWNERS & conflict resolution | 30 min | Self-paced |
| Recovering from Git mistakes | 30 min | Self-paced |
| Hands-on lab: open, review, and merge a PR | 60 min | Hands-on + mentor review |
| Knowledge check (10 questions) | 5 min | Self-paced |

## 6. Outline of Topics Covered

### Block A — Git Fundamentals (45 min)

- Repository anatomy: working tree, staging, local repo, remote.
- Core commands: `clone`, `status`, `add`, `commit`, `push`, `pull`, `fetch`, `log`, `diff`.
- Configuring identity, signing commits, and SSH/HTTPS auth against `git.acme.example`.
- GUI usage in VS Code with the GitHub Enterprise Pull Requests extension.

### Block B — Trunk-based Development & Branching (30 min)

- Why trunk-based at ACME: small batches, fast integration, fewer long-lived branches.
- Branch naming: `feat/<slug>`, `fix/<slug>`, `chore/<slug>`, `docs/<slug>`.
- Branch strategy — see [`../04-engineering/practices/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md).
- Release tags and hotfix branches; the role of release branches in `acme-cloud-api`.

### Block C — Commits & PR Conventions (30 min)

- Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, `perf:`).
- Commit message conventions — see [`../04-engineering/practices/commit-message-conventions.md`](../04-engineering/practices/commit-message-conventions.md).
- PR template fields: summary, motivation, test plan, screenshots/telemetry, breaking changes, reviewer checklist.
- Pull requests and code review — see [`../04-engineering/practices/pull-requests-and-code-review.md`](../04-engineering/practices/pull-requests-and-code-review.md).

### Block D — CODEOWNERS & Conflict Resolution (30 min)

- How `CODEOWNERS` files work per repository — see [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md).
- Required reviewer rules and auto-assignment.
- Resolving merge conflicts: `git status`, manual edit, `git add`, complete; using `git mergetool` when needed.
- Rebasing a feature branch onto the latest `main` before merge.

### Block E — Recovering from Git Mistakes (30 min)

- Undo an uncommitted change: `git restore`, `git clean`.
- Amend the last commit (and when not to).
- Reset a branch to a previous commit: soft / mixed / hard and their trade-offs.
- `git reflog` for lost work; `git cherry-pick` for transplanting a commit.
- Force-push rules: only on feature branches you own; never on `main` or release branches.
- Reference: [`../04-engineering/practices/debugging.md`](../04-engineering/practices/debugging.md) for repository-related debugging.

### Block F — Hands-on Lab (60 min)

The learner works in the sandbox repository `git.acme.example/acme-shared-libraries-sandbox` (fictional). Tasks:

1. Clone the sandbox repository.
2. Create a feature branch named `feat/training-<employeeid>`.
3. Add a new Markdown file under `docs/training/` introducing yourself (≤ 200 words).
4. Commit with a `docs:` conventional message that passes the commit lint.
5. Push and open a PR against `main`.
6. Request review from your assigned mentor (a senior engineer from your business unit).
7. Address one round of review feedback (your mentor will request a small change).
8. Rebase onto latest `main`, resolve the planted conflict, and squash-merge.
9. Verify CI status is green and the merge commit appears on `main`.

### Block G — Knowledge Check (5 min)

- 10-question quiz on Git fundamentals and ACME conventions; threshold 80%.

## 7. Format

**Mixed.** Five self-paced blocks (3 hours) plus a hands-on lab (1 hour) with mentor review. The lab is graded pass/fail by the mentor; a failed lab can be reattempted after a coaching conversation. Mentors are senior engineers nominated per business unit by the Engineering Enablement lead.

## 8. Completion Criteria

- All five self-paced blocks marked `COMPLETED` in the LMS.
- Knowledge-check quiz score **≥ 80%** (≥ 8 of 10 correct).
- Hands-on lab: sandbox PR opened, reviewed, feedback addressed, and merged; mentor signs off in the LMS.
- Acknowledgement of source code security — see [`../03-security/source-code-security.md`](../03-security/source-code-security.md) — already on file from ACME-TRN-004.
- [`../08-forms/training-completion.md`](../08-forms/training-completion.md) submitted and signed off by Engineering Enablement.

## 9. Follow-up / Next Steps

- The learner is now eligible to open PRs in their team's production repositories.
- Proceed to [`ai-coding-assistant-usage.md`](./ai-coding-assistant-usage.md) (ACME-TRN-006) if a Copilot license is assigned.
- Proceed to [`cloud-platform-fundamentals.md`](./cloud-platform-fundamentals.md) (ACME-TRN-007) for Platform Infrastructure, Cloud API, and Workspace API engineers.
- Proceed to [`product-training.md`](./product-training.md) (ACME-TRN-008) for product-specific deep dives.
- First production PR is expected within 14 days of completion — see [`../07-workflows/first-30-days.md`](../07-workflows/first-30-days.md).

## 10. Trainer / Owner

| Role | Person | Responsibility |
|---|---|---|
| Module owner | Aditi Ghosh, Engineering Enablement lead (`aditi.ghosh@acme.example`) | Content strategy, lab design, annual review. |
| Per-business-unit mentors | Senior engineers nominated by Tech Leads | Sandbox PR review and grading. |
| Repository access coordinator | Geetha Iyer, IT Onboarding Specialist (`geetha.iyer@acme.example`) | Sandbox repository access provisioning. |
| LMS coordinator | Anjali Iyer, Training Operations (`anjali.iyer@acme.example`) | Tracking, sign-off. |

Escalation contacts are in [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md). Glossary terms are in [`../metadata/glossary.md`](../metadata/glossary.md).
