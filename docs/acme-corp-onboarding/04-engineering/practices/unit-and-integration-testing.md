---
document_id: ACME-ENG-007
title: Unit and Integration Testing
category: engineering
department: engineering
applicable_roles: [engineers]
owner: Engineering
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [engineering, practices, testing, coverage, flaky-tests]
---

# Unit and Integration Testing

> Sample code and commands below are **simulated** for onboarding orientation. Real test commands per repository are documented in the per-repo guides under [`../repositories/`](../repositories/).

Tests are the safety net for trunk-based development (see [`./git-branching-strategy.md`](./git-branching-strategy.md)). Without fast, deterministic tests, you cannot keep a green `main`.

## 1. Coverage Expectations

Every ACME repository enforces a **minimum line coverage of 70% per package** for unit tests. The CI `ci/unit-tests` job fails if any package drops below 70% on the diff.

- **Per package**, not repository-wide. A repository-wide average of 90% with one package at 30% is a violation.
- The threshold applies to **new and modified lines** on the PR (diff coverage), and to **the package as a whole** (aggregate coverage).
- Internal test helpers (files matching `*_test.go`, `*_test.py`, `*.test.ts`, `*Test.java`) are excluded from the denominator.
- Generated code (under `gen/`, `pb/`, etc.) is excluded from coverage.
- Coverage is reported as a comment on every PR, showing the per-file delta.

## 2. When Tests Run

| Suite | Trigger | Time budget | Where |
|-------|---------|-------------|-------|
| Unit tests | Every PR push | ≤ 5 min per package | `ci/unit-tests` |
| Unit tests | Every merge to `main` | ≤ 5 min per package | `main.yml` |
| Integration tests | Nightly 02:00 UTC | ≤ 30 min total | `nightly.yml` |
| Integration tests | Merge to `main` (touching `internal/`, `proto/`, `deploy/`) | ≤ 30 min | `main.yml` |
| End-to-end tests | Tag `v*` (release) | ≤ 60 min | `release.yml` (staging env) |
| Smoke tests | After every prod deploy | ≤ 5 min | post-deploy hook |

Unit tests **must** run on every PR. Integration tests run on merge to `main`. End-to-end tests run on staging during a release. Smoke tests run in production after every canary ramp.

## 3. Test Naming

Across all languages, the test name describes the **behavior under test, not the implementation**.

- **Go:** `TestFunctionName_Scenario_ExpectedResult` — e.g., `TestAllow_QuotaExceeded_ReturnsFailedPrecondition`.
- **Python:** `test_<unit>_<scenario>_<expected>` — e.g., `test_within_quota_over_limit_returns_false`.
- **TypeScript:** `it("describes behavior in present tense")` — e.g., `it("returns false when tenant is over quota")`.
- **Java:** `methodName_scenario_expected` — e.g., `allowUpload_overQuota_returnsFalse`.

Avoid `test1`, `test_happy`, `test_edge`. A reviewer reading the test name should know what it asserts without reading the body.

## 4. Table-Driven Tests

ACME strongly prefers **table-driven tests** for any function with more than two scenarios. Every language has a canonical pattern:

### 4.1 Go

```go
func TestAllow_QuotaExceeded(t *testing.T) {
    t.Parallel()
    cases := []struct {
        name      string
        tenantID  string
        current   map[string]int
        wantErr   string
    }{
        {
            name:     "fresh tenant under quota",
            tenantID: "t-001",
            current:  map[string]int{},
            wantErr:  "",
        },
        {
            name:     "tenant at quota returns failed precondition",
            tenantID: "t-002",
            current:  map[string]int{"agent": 50},
            wantErr:  "FAILED_PRECONDITION: quota exceeded",
        },
        {
            name:     "empty tenant id is a client error",
            tenantID: "",
            current:  nil,
            wantErr:  "INVALID_ARGUMENT: tenant_id is empty",
        },
    }
    for _, tc := range cases {
        tc := tc
        t.Run(tc.name, func(t *testing.T) {
            t.Parallel()
            // err := checker.Allow(ctx, tc.tenantID, "agent", tc.current)
            // ...assert err matches tc.wantErr...
            _ = tc
        })
    }
}
```

### 4.2 Python (pytest)

```python
@pytest.mark.parametrize(
    ("tenant_id", "current", "expected"),
    [
        ("t-001", {}, True),
        ("t-002", {"agent": 50}, False),
        ("", None, ValueError),
    ],
    ids=["under_quota", "at_quota", "empty_id"],
)
def test_within_quota(tenant_id, current, expected):
    if expected is ValueError:
        with pytest.raises(ValueError):
            within_quota(tenant_id, current or {})
        return
    assert within_quota(tenant_id, current or {}) is expected
```

### 4.3 TypeScript (Vitest)

```typescript
describe("withinQuota", () => {
  it.each([
    ["under quota", "t-001", {}, true],
    ["at quota", "t-002", { agent: 50 }, false],
  ] as const)("returns %s outcome", (_label, tenantId, current, expected) => {
    expect(withinQuota(tenantId, current)).toBe(expected);
  });
});
```

## 5. Mocks vs. Fakes

ACME's default is **fakes over mocks**. A fake is a real, in-memory implementation of an interface; a mock records calls and asserts on them.

| Property | Fake | Mock |
|----------|------|------|
| Behavior | Real, simple in-memory | Canned per test |
| Maintenance | One per interface, lives in `internal/testutil/` | Per test, brittle to refactors |
| Failure mode | Wrong value returned | "Unexpected call to mock" |
| Best for | Storage, queues, caches | Verifying "did you call X exactly once" |

Use a mock when you genuinely need to assert call counts (e.g., "the retry loop did not call the downstream twice"). Use a fake when you need real behavior (e.g., "the store returns the value I inserted").

ACME ships fakes in `acme-shared-libraries` for: `tenant.Store`, `billing.Ledger`, `kafka.Producer`, `vault.Client`. See [`../repositories/acme-shared-libraries.md`](../repositories/acme-shared-libraries.md).

## 6. Test Data Fixtures

- Fixtures live in `testdata/` at the repository root, **never** checked in alongside source.
- Golden files (expected outputs captured once and pinned) go in `testdata/golden/`. Re-recording a golden file requires a PR comment with the rationale; "I changed the output" is not enough.
- PII, customer names, real tenant IDs are **never** used as fixtures. Use the ACME fake-data generator (`acme-shared-libraries/testutil/fakedata`).
- Fixtures must be deterministic — no `time.Now()`, no `rand` without a fixed seed.

## 7. Test Isolation

- Every test sets up and tears down its own state. No `TestMain` global setup beyond logger init.
- Tests must be **order-independent**. The CI runs the suite in random order on every PR.
- Tests must be **parallel-safe** where possible. In Go, `t.Parallel()` is expected by default.
- Tests must not share mutable state across packages.

## 8. Flaky-Test Policy

A **flaky test** is one that passes and fails on the same commit. Flakiness is treated as a production-quality issue because it erodes trust in the test suite.

Policy:

1. **Detection.** The QE team's flaky-detector (`acme-quality-automation`) runs every test 10× on every PR. A test that passes and fails on the same commit is flagged.
2. **Quarantine.** After **3 failures in 7 days**, the test is **auto-quarantined** — moved to a `// QUARANTINED: <ticket>` block, skipped in CI, and a ticket is filed against the owning team.
3. **SLA to fix.** The owning team has **5 business days** to fix or delete the test. A quarantined test older than 14 days is **deleted** automatically by the QE bot, with a comment on the owning PR.
4. **Re-enable.** A re-enabled quarantined test that flakes again within 30 days is quarantined for **good**, and the team must rewrite it.
5. **Accountability.** Three or more quarantined tests on one team in a quarter triggers a review with the EM and the Director of AI/ML or VP Engineering.

See [`../repositories/acme-quality-automation.md`](../repositories/acme-quality-automation.md) for the flaky-detector implementation.

## 9. Integration Tests

Integration tests live in `test/integration/` (or `test/` in Go, where integration tests are conventionally inside the package they test, suffixed `_integration_test.go`). They:

- Require a real (ephemeral) instance of dependencies: Postgres, Kafka, Vault, the downstream service.
- Are tagged / marked / filtered so they do not run in the unit-test job.
- Are run by the `nightly.yml` workflow against a fresh ephemeral environment.
- Must use the ACME fake-data generator — no real customer data, no production fixtures.

Sample Go integration test entrypoint:

```go
//go:build integration

package quota_test

import (
    "context"
    "testing"

    "github.com/acme/internal/testutil"
)

func TestQuotaChecker_RealPostgres(t *testing.T) {
    t.Parallel()
    ctx := context.Background()
    pg := testutil.NewPostgresContainer(t) // ephemeral, per-test
    store := newStoreForTest(t, pg)
    chk := NewChecker(store)
    // ...assert against real pg...
    _ = ctx
    _ = chk
}
```

## 10. End-to-End Tests

E2E tests are owned by **Quality Engineering** and live in the [`acme-quality-automation`](../repositories/acme-quality-automation.md) repository. They:

- Run on staging during a release (`release.yml`).
- Are written in Python + Playwright (for browser flows) and pytest + httpx (for API flows).
- Are tagged by product: `@cloud`, `@intelligence`, `@workspace`.
- Are gated by the [release management](./release-management.md) cadence — a release cannot ship to production if any E2E on staging is red.

## 11. Test-First Habits

ACME does not require strict test-driven development (TDD). The required invariant is:

- New public behavior → new test.
- Bug fix → regression test that fails before the fix and passes after.
- Refactor → tests unchanged; coverage unchanged.

A PR that adds logic without a test is blocked at review. A bug-fix PR that does not include a regression test is blocked at review.

## 12. Sample Coverage Comment (Generated by CI)

```text
## Coverage report

Per-package coverage:
- internal/quota   84.2% (+1.1%)  ✓
- internal/auth    91.0% (+0.0%)  ✓
- internal/billing 68.4% (-3.2%)  ✗ below 70%

Diff coverage (changed lines only):
- internal/billing/ledger.go      55.0%  ✗

Required action: add tests for Ledger.record in internal/billing/ledger.go
to bring package coverage back to ≥ 70%.
```

## Related Documents

- [`../repository-catalog.md`](../repository-catalog.md)
- [`./git-branching-strategy.md`](./git-branching-strategy.md)
- [`./pull-requests-and-code-review.md`](./pull-requests-and-code-review.md)
- [`./coding-standards.md`](./coding-standards.md)
- [`./ci-cd-overview.md`](./ci-cd-overview.md)
- [`./debugging.md`](./debugging.md)
- [`./observability-and-logging.md`](./observability-and-logging.md)
- [`../repositories/acme-shared-libraries.md`](../repositories/acme-shared-libraries.md)
- [`../repositories/acme-quality-automation.md`](../repositories/acme-quality-automation.md)
- [`../repositories/acme-cloud-api.md`](../repositories/acme-cloud-api.md)
- [`../../03-security/source-code-security.md`](../../03-security/source-code-security.md)
- [`../../09-contacts/contact-directory.md`](../../09-contacts/contact-directory.md)
- [`../../metadata/glossary.md`](../../metadata/glossary.md)
