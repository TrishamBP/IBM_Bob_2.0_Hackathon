---
document_id: ACME-ENG-004
title: Coding Standards
category: engineering
department: engineering
applicable_roles: [engineers]
owner: Engineering
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [engineering, practices, coding-standards, linting]
---

# Coding Standards

> All tools referenced here (formatters, linters, package managers) are configured at the repository level. Commands shown are **simulated** examples for onboarding orientation only.

This document defines the minimum, non-negotiable coding standards across all ACME repositories. Individual repositories may add stricter rules in their `README.md` or `CONTRIBUTING.md`, but they may not relax what is defined here.

## 1. Universal Standards

The following apply to **every** language and repository at ACME:

- **No commented-out code.** Use git history to recover dead code. If you must keep a snippet for context, link to the ticket or ADR.
- **No `console.log`, `fmt.Println`, `print()` in committed code.** Use the structured logger (see [Observability and logging](./observability-and-logging.md)). A debug print statement in `main` is a CI failure.
- **No secrets, no PII, no customer data** in source. See [`../../03-security/secrets-management.md`](../../03-security/secrets-management.md).
- **No AI-generated code submitted without review.** AI assistants may draft, but the author is the sole accountable party. See [`../../03-security/ai-tool-acceptable-use.md`](../../03-security/ai-tool-acceptable-use.md).
- **No magic numbers.** Named constants only.
- **Functions ≤ 80 lines.** Files ≤ 500 lines unless a justified ADR is referenced in the file header.
- **Public symbols documented.** Every exported type, function, method, and constant carries a doc comment in the language's idiomatic format.
- **Error handling explicit.** No swallowed errors. No empty `catch`/`except`. No `panic(err)` in libraries.
- **Tests required for new logic.** See [Unit and integration testing](./unit-and-integration-testing.md).

## 2. `.editorconfig` (Universal)

Every repository ships an `.editorconfig` at the root:

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 4

[*.{go,rs}]
indent_style = tab

[*.{ts,tsx,js,jsx,json,yml,yaml,css,scss,html,md}]
indent_size = 2

[Makefile]
indent_style = tab
```

Editors with the EditorConfig plugin (VS Code, JetBrains, Neovim, Sublime) auto-apply these settings. See [`../developer-workstation-setup.md`](../developer-workstation-setup.md) for the supported editor list.

## 3. Language-Specific Standards

### 3.1 Go (`acme-cloud-api`, `acme-platform-infrastructure`)

- **Formatter:** `gofmt` (enforced; `gofumpt` is permitted with strict equivalent rules).
- **Linter:** `golangci-lint` with the ACME-shared config in `acme-shared-libraries/golangci/.golangci.yml`.
- **Import order:** stdlib, blank line, third-party, blank line, `acme.internal/...`.
- **Error wrapping:** `fmt.Errorf("do thing: %w", err)` — never `fmt.Errorf("do thing: %v", err)`.
- **Context propagation:** Every function that does I/O takes a `ctx context.Context` as its first argument.
- **No `init()` side effects.** Use explicit registration in `cmd/`.
- **No `interface{}` in new code.** Use `any` (Go 1.18+) or a typed constraint.
- **Sample:**

    ```go
    // Package quota enforces per-tenant resource limits.
    package quota

    import (
        "context"
        "fmt"

        "github.com/acme/internal/tenant"
    )

    // Checker decides whether a tenant may create a new resource.
    type Checker struct {
        store tenant.Store
    }

    // NewChecker returns a Checker backed by the supplied tenant store.
    func NewChecker(s tenant.Store) *Checker {
        return &Checker{store: s}
    }

    // Allow returns nil if the tenant is within quota; an error otherwise.
    func (c *Checker) Allow(ctx context.Context, tenantID string, kind string) error {
        // ...
        return nil
    }
    ```

### 3.2 Python (`acme-intelligence-agents`, `acme-intelligence-inference`, `acme-intelligence-ml`, `acme-quality-automation`)

- **Formatter:** `black` (line length 100, enforced).
- **Sorter:** `isort` (ACME profile).
- **Linter:** `ruff` (replaces flake8 + pylint for new code).
- **Type checker:** `mypy --strict` on `src/`; tests may relax to `--disallow-untyped-defs`.
- **Docstring style:** Google-style on every public function.
- **No mutable default arguments.** Use `None` + sentinel.
- **No `print()` in committed code.** Use the structured logger from `acme.shared.logging`.
- **Sample:**

    ```python
    """Tenant quota checker for ACME Intelligence agents."""

    from __future__ import annotations

    from collections.abc import Mapping
    from typing import Final

    from acme.shared.logging import get_logger

    log = get_logger(__name__)

    #: Maximum number of agents a tenant may run concurrently.
    MAX_AGENTS: Final[int] = 50


    def within_quota(tenant_id: str, current: Mapping[str, int]) -> bool:
        """Return True if tenant may start another agent.

        Args:
            tenant_id: The tenant identifier (must be non-empty).
            current: A mapping of agent kind → count for this tenant.

        Returns:
            True if the tenant is below the per-tenant agent quota.

        Raises:
            ValueError: If tenant_id is empty.
        """
        if not tenant_id:
            raise ValueError("tenant_id must be non-empty")
        return current.get(tenant_id, 0) < MAX_AGENTS
    ```

### 3.3 TypeScript (`acme-cloud-frontend`, `acme-workspace-web`)

- **Formatter:** `prettier` (ACME config: single quote, trailing comma `all`, print width 100).
- **Linter:** `eslint` with `@typescript-eslint/recommended` + ACME ruleset (no `any`, no `console.*`, exhaustive `switch`).
- **Type system:** `strict: true`. New code must use `unknown` over `any`.
- **Module system:** ESM, `NodeNext`. No CommonJS `require` in new code.
- **Imports:** absolute via `tsconfig` `paths` rooted at `@/`. No deep relative imports across feature directories.
- **React:** function components only. Hooks must start with `use`. No `default` exports for components unless the file is the entry.
- **Sample:**

    ```typescript
    import { type FC, useMemo } from 'react';

    import { useTenantQuota } from '@/hooks/use-tenant-quota';

    interface TenantQuotaBadgeProps {
      readonly tenantId: string;
    }

    export const TenantQuotaBadge: FC<TenantQuotaBadgeProps> = ({ tenantId }) => {
      const { used, limit } = useTenantQuota(tenantId);
      const pct = useMemo(() => (limit > 0 ? Math.round((used / limit) * 100) : 0), [used, limit]);
      return (
        <span className="badge" aria-label="tenant quota usage">
          {pct}%
        </span>
      );
    };
    ```

### 3.4 Java (`acme-workspace-api`)

- **Formatter:** `google-java-format` (AOSP profile permitted for legacy files, must not be mixed in one file).
- **Linter:** `spotbugs` + `checkstyle` with the ACME config in `acme-shared-libraries/checkstyle/acme-checkstyle.xml`.
- **JDK:** 21 LTS. New code uses records, sealed types, pattern matching for `instanceof`.
- **No public mutable fields.** Use records or accessor methods.
- **No checked exceptions in new APIs.** Use unchecked `RuntimeException` subclasses with a typed `ErrorCode`.
- **Logging:** SLF4J → Logback; structured JSON appender (see [Observability and logging](./observability-and-logging.md)).
- **Sample:**

    ```java
    package com.acme.workspace.quota;

    /** Enforces per-tenant document count limits. */
    public final class TenantQuotaChecker {
        private static final int DEFAULT_LIMIT = 500;
        private final TenantStore store;

        public TenantQuotaChecker(TenantStore store) {
            this.store = store;
        }

        /**
         * Returns {@code true} if the tenant may upload one more document.
         *
         * @param tenantId the tenant identifier, must be non-null and non-empty
         * @return true if the tenant is below quota
         */
        public boolean allowUpload(String tenantId) {
            // ...
            return true;
        }
    }
    ```

## 4. Lint Configuration as Code

Lint configs are version-controlled. They live in `acme-shared-libraries` and are pulled into each repository via a symlink or a small `Makefile` `bootstrap` target:

```bash
# fictional/simulated command — pull the canonical lint config into your repo
make bootstrap-lint
# Creates .golangci.yml, .eslintrc.cjs, .prettierrc, acme-checkstyle.xml, etc.
```

Updates to the canonical config roll out via a PR to each consuming repository. Each consuming repository has 10 business days to address new violations; the violation policy is "warn → error" with one minor release of lead time.

## 5. Documentation Requirements

Every public API — gRPC service, REST endpoint, npm export, PyPI module, Maven artifact, Go package — must have:

- A doc comment in the language's idiomatic format.
- A usage example in the repository's `docs/examples/` directory.
- An entry in the service or library catalog (fictional: `https://catalog.acme.example`).
- For public API changes (`proto/`, `/api/`), an ADR entry in `docs/adr/`.

A PR that adds a new public symbol without documentation fails the `docs-coverage` check. Documentation that lies (e.g., a function name says `Delete` but the doc says `Create`) is treated as a P1 bug.

## 6. Commenting Standards

- **Why, not what.** Comments explain intent, not restate code.
- **No commented-out code.** (Restated because this is the most common violation.)
- **TODO format:** `// TODO(CLOUD-1287, @github-handle): describe what and why, with a deadline if relevant.`
- **FIXME format:** `// FIXME: <description>. Tracking in <ticket>.`
- **No "HACK", "WORKAROUND", "TEMP" comments** without an accompanying ticket. They rot.

## 7. File and Directory Layout

Across all repositories:

```
repo-root/
├── .github/                     # PR template, CODEOWNERS, workflows
├── .editorconfig
├── Makefile                     # canonical entry: build, test, lint, run
├── README.md
├── CONTRIBUTING.md
├── docs/                        # architecture, adr, examples
├── internal/ or src/            # implementation
├── proto/ or api/               # public API surface
├── deploy/                      # terraform, helm, kustomize
└── test/                        # integration tests, fixtures
```

Variations are documented in the per-repo README. See [`../repository-catalog.md`](../repository-catalog.md).

## 8. Forbidden Patterns

| Pattern | Why forbidden | What to do instead |
|---------|----------------|---------------------|
| `any` in TypeScript | Erases type safety | `unknown` + narrowing |
| `interface{}` in Go 1.18+ | Legacy alias | `any` or a typed constraint |
| Mutable default args in Python | Classic bug | `None` sentinel + assignment |
| Checked exceptions in new Java APIs | Couples caller to impl | Unchecked with `ErrorCode` |
| `console.log` / `print()` / `fmt.Println` in committed code | Unstructured noise | Structured logger |
| Commented-out code | Rot | Delete; recover from git |
| Magic numbers | Hard to grep | Named constant |
| Functions > 80 lines | Hard to review | Split |
| Files > 500 lines | Hard to navigate | Split or extract module |
| `TODO` without ticket | Will never be done | Ticket + deadline |

## 9. Enforcement

All standards in this document are **machine-enforced** by CI. A PR that fails the lint job is blocked from merge. Branch protection prevents override; only the Security GRC team may bypass, and only for a documented incident. See [`./ci-cd-overview.md`](./ci-cd-overview.md).

## Related Documents

- [`../repository-catalog.md`](../repository-catalog.md)
- [`../developer-workstation-setup.md`](../developer-workstation-setup.md)
- [`../ai-coding-assistant-setup.md`](../ai-coding-assistant-setup.md)
- [`./git-branching-strategy.md`](./git-branching-strategy.md)
- [`./pull-requests-and-code-review.md`](./pull-requests-and-code-review.md)
- [`./commit-message-conventions.md`](./commit-message-conventions.md)
- [`./ci-cd-overview.md`](./ci-cd-overview.md)
- [`./unit-and-integration-testing.md`](./unit-and-integration-testing.md)
- [`./observability-and-logging.md`](./observability-and-logging.md)
- [`./internal-package-management.md`](./internal-package-management.md)
- [`../repositories/acme-shared-libraries.md`](../repositories/acme-shared-libraries.md)
- [`../../03-security/source-code-security.md`](../../03-security/source-code-security.md)
- [`../../03-security/open-source-dependency-security.md`](../../03-security/open-source-dependency-security.md)
- [`../../03-security/ai-tool-acceptable-use.md`](../../03-security/ai-tool-acceptable-use.md)
- [`../../metadata/glossary.md`](../../metadata/glossary.md)
