---
document_id: ACME-ENG-008
title: Debugging Practices
category: engineering
department: engineering
applicable_roles: [engineers]
owner: Engineering
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [engineering, practices, debugging, observability]
---

# Debugging Practices

> All hosts referenced here are fictional. `logs.internal.acme.example`, `traces.internal.acme.example`, and `metrics.internal.acme.example` do not resolve. Sample commands are **simulated** for onboarding orientation only.

This document defines how ACME engineers approach debugging. It is not exhaustive — your team may have a richer per-service runbook — but the principles below apply everywhere.

## 1. The Iron Rule: Reproduce First

**Do not begin fixing until you can reproduce the bug.**

If you cannot reproduce the failure, you cannot verify the fix. A "fix" you cannot verify is not a fix — it is a guess that lands on `main`. Reproduction is the foundation of every debugging session at ACME.

Reproduction means:

1. A clear list of inputs and preconditions.
2. A reproducible set of steps (or a failing test) that triggers the failure.
3. A captured log line, trace ID, or metric anomaly from the failing run.

If the bug is intermittent, capture as many runs as possible and look for the **common precondition**. Intermittent bugs are almost always time-, order-, or state-dependent.

## 2. The Five-Step Debugging Process

ACME engineers use a five-step process for any non-trivial bug:

1. **Reproduce.** Build the smallest failing case you can.
2. **Isolate.** Reduce the failing case until changing any single input makes the bug disappear.
3. **Hypothesize.** Form a falsifiable hypothesis: "I believe X is null because Y was skipped."
4. **Verify.** Add a log line, a breakpoint, or a one-line test that proves (or refutes) the hypothesis.
5. **Fix.** The smallest change that resolves the verified hypothesis, plus a regression test (see [Unit and integration testing](./unit-and-integration-testing.md)).

Skip a step and you will spend the next morning reverting a "fix" that broke something else.

## 3. The MVE — Minimal Verifiable Example

When you ask for help — from a teammate, from #engineering Slack, from an internal LLM assistant — you are expected to bring an **MVE** (Minimal Verifiable Example). An MVE is:

- A self-contained reproduction: a single file, a single test, or a curl command.
- Reduced to the smallest size that still reproduces the failure.
- Committed to a gist or to a `debug/` branch in your fork.
- Accompanied by the captured log line or trace ID.

An MVE is the equivalent of a good bug report. Without it, your reviewer, your buddy, or your AI assistant is guessing.

### Sample MVE structure

```text
Title: quota.Allow returns nil for tenant with negative remaining

Repro (Python):
    $ python -m acme.quota.demo --tenant t-bug --remaining -1
    Result: allow=True (expected: allow=False)

Log line from the failing run (logs.internal.acme.example):
    {"ts":"2026-09-15T09:42:11Z","level":"warn","msg":"quota.Allow","tenant":"t-bug","remaining":-1,"allow":true}

Trace ID: 7e3f9a1c8b4d4d7e9c1f2b3a4d5e6f70

Hypothesis: signed-int underflow when computing remaining;
            the check `if remaining > 0` skips negative values.
```

## 4. Where to Look First: Logs, Traces, Metrics

ACME's observability stack (see [Observability and logging](./observability-and-logging.md)) has three pillars. Each pillar answers a different question; choose the right one for the job.

| Pillar | Endpoint (fictional) | Best for | When to use |
|--------|----------------------|----------|-------------|
| Logs | `https://logs.internal.acme.example` | Discrete events, error messages, structured fields | "What happened at this instant?" |
| Traces | `https://traces.internal.acme.example` | Distributed causality, latency, fan-out | "Why was this request slow?" |
| Metrics | `https://metrics.internal.acme.example` | Aggregate behavior, SLO burn, alerting | "How is the system behaving overall?" |

### Workflow

1. **Start with the trace.** Every request has a trace ID. Look up the trace in Tempo; identify the span with anomalous latency or an error status.
2. **Pull the logs for the trace.** Search logs by the trace ID. Every ACME service emits a `trace_id` field on every log line — filtering by it gives you the exact path through the system.
3. **Cross-check metrics.** If the trace shows a downstream slowness, check the metrics dashboard for the downstream service: is the SLO burning? Are there error-rate spikes?

### Sample structured log line

```json
{
  "ts": "2026-09-15T09:42:11.123456789Z",
  "level": "error",
  "service": "acme-cloud-api",
  "version": "v2026.09.3",
  "trace_id": "7e3f9a1c8b4d4d7e9c1f2b3a4d5e6f70",
  "span_id": "b3a4d5e6f70a1",
  "tenant_id": "t-bug",
  "user_id": "u-anonymous",
  "msg": "quota.Allow returned unexpected nil",
  "remaining": -1,
  "component": "internal/quota/checker.go:84"
}
```

Note the `trace_id`, `span_id`, `tenant_id`, `component`, and the absence of any PII. See [Observability and logging](./observability-and-logging.md) for the schema rules.

## 5. Language-Specific Debugging Tools

### 5.1 Go — `dlv` (Delve)

```bash
# fictional/simulated command — attach to a running server
dlv attach $(pidof acme-cloud-api)
# (dlv) break internal/quota.Allow
# (dlv) continue
# (dlv) print remaining
# (dlv) goroutines
# (dlv) traces
```

For a panic in production: load the core dump from `vault.acme.example` (gated by PIM — see [Environments](./development-staging-production.md)) into `dlv core <binary> <core>`.

### 5.2 Python — `pdb` / `ipdb` / `pdb++`

```bash
# fictional/simulated command — drop into pdb on the next exception
python -m pdb -m acme.intelligence.agents.run --tenant t-bug
# (Pdb) b acme/intelligence/quota.py:42
# (Pdb) c
# (Pdb) p remaining
# (Pdb) w   # show stack trace
```

For long-running inference servers, prefer `ipdb` post-mortem with `PYTHONBREAKPOINT=ipdb.set_trace`.

### 5.3 TypeScript / Browser — browser devtools

- **Network tab** — capture the failing fetch, check request/response bodies and timing.
- **Sources tab** — set a breakpoint; use `debugger;` to drop in from code (do not commit `debugger;`).
- **Performance tab** — record a flame chart for slow UI paths.
- **Memory tab** — capture a heap snapshot for memory leaks.

For Node.js services, use `--inspect` and connect Chrome devtools to it.

### 5.4 Java — `jdb` / `jstack` / `async-profiler`

```bash
# fictional/simulated command — capture a thread dump from a running JVM
jstack $(pidof java) > thread-dump.txt

# fictional/simulated command — start an interactive debugger
jdb -attach 8000
# > stop in com.acme.workspace.quota.TenantQuotaChecker.allowUpload
# > run
```

For CPU profiling, use `async-profiler` to render a flamegraph; the profile is uploaded to `traces.internal.acme.example` for retention.

## 6. Do Not Push to Production Without a Fix

The second iron rule: **do not push to production without a fix.**

This sounds obvious but is consistently violated under pressure. Specifically:

- A "diagnostic log line" committed to `main` and deployed to prod is a fix in disguise — it changes behavior in production. Either it is part of the fix (and ships with the regression test), or it is debug instrumentation that should be on a feature branch and removed before merge.
- A "quick configuration tweak" pushed to prod to "see if it helps" is a fix without a hypothesis. It will fail and you will not know why.
- A hotfix to a release branch must follow the [release management](./release-management.md) hotfix procedure: PR, CI, two approvers, change ticket.

If you find yourself in production without a fix, you are debugging in production. That is permitted only during an active SEV1/SEV2 incident, with the incident commander's approval, and with the change recorded in the incident channel (see [Incident response](./incident-response-and-on-call-introduction.md)).

## 7. Common Anti-Patterns

| Anti-pattern | Why it wastes time | What to do instead |
|--------------|-------------------|--------------------|
| Adding print statements until "it works" | You don't know what fixed it | Form a hypothesis first |
| Fixing without a regression test | The bug will come back | Write the failing test first |
| Debugging in production | Noisy, risky, slow | Reproduce locally; see [Environments](./development-staging-production.md) |
| Asking for help without an MVE | Reviewers guess | Build an MVE first |
| Reading code top-to-bottom | Linear reading misses causality | Follow the trace |
| Blaming the framework | Premature narrowing | Verify with a minimal repro |
| Cherry-picking a "fix" to a release branch | Untested change in prod | Follow the hotfix procedure |

## 8. Asking for Help

After you have an MVE and a falsifiable hypothesis, escalation is welcome and expected:

- **Team channel** (e.g., `#cloud-api`) — first stop. Include the MVE.
- **Buddy reviewer** — your assigned onboarding buddy (see [`../../07-workflows/first-30-days.md`](../../07-workflows/first-30-days.md)).
- **Engineering Manager** — for non-blocking, opinion questions.
- **Platform Infrastructure** — for cluster, runner, or infra bugs (`#platform`).
- **Quality Engineering** — for test-harness issues (`#qe`).
- **On-call SRE** — only for production issues that match an on-call rotation's scope; see [Incident response](./incident-response-and-on-call-introduction.md).

## 9. Debugging Across Services

When the trace crosses service boundaries (e.g., Cloud API → Intelligence Inference → Workspace API), the trace ID is the only reliable thread. The Temporal query that joins them is:

```text
# fictional/simulated — query the trace in traces.internal.acme.example
service = "acme-cloud-api" AND
  trace_id = "7e3f9a1c8b4d4d7e9c1f2b3a4d5e6f70" AND
  status = "ERROR"
```

Cross-service bugs are ownership-boundary bugs. File a ticket against the service whose span has the error status. If the error span is in your own service, fix it; if it is in another team's service, hand off with the trace ID and the MVE.

## 10. Post-Fix: Verify and Document

After the fix is merged:

1. Verify the regression test fails on the prior commit (revert your fix locally, run the test, observe failure).
2. Verify the regression test passes on the fix commit.
3. Update the per-service runbook with the new failure mode and the new span/log signature.
4. If the bug was a SEV1/SEV2, the postmortem is required (see [Incident response](./incident-response-and-on-call-introduction.md)).

## Related Documents

- [`../repository-catalog.md`](../repository-catalog.md)
- [`./ci-cd-overview.md`](./ci-cd-overview.md)
- [`./unit-and-integration-testing.md`](./unit-and-integration-testing.md)
- [`./observability-and-logging.md`](./observability-and-logging.md)
- [`./development-staging-production.md`](./development-staging-production.md)
- [`./release-management.md`](./release-management.md)
- [`./incident-response-and-on-call-introduction.md`](./incident-response-and-on-call-introduction.md)
- [`../repositories/acme-cloud-api.md`](../repositories/acme-cloud-api.md)
- [`../repositories/acme-intelligence-inference.md`](../repositories/acme-intelligence-inference.md)
- [`../../02-it/it-support-and-troubleshooting.md`](../../02-it/it-support-and-troubleshooting.md)
- [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md)
- [`../../03-security/security-incident-reporting.md`](../../03-security/security-incident-reporting.md)
- [`../../07-workflows/first-30-days.md`](../../07-workflows/first-30-days.md)
- [`../../09-contacts/contact-directory.md`](../../09-contacts/contact-directory.md)
- [`../../metadata/glossary.md`](../../metadata/glossary.md)
