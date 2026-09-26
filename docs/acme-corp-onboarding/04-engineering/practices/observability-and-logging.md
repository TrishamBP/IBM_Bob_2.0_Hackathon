---
document_id: ACME-ENG-010
title: Observability and Logging
category: engineering
department: engineering
applicable_roles: [engineers]
owner: Engineering
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [engineering, practices, observability, logging, metrics, traces, slo]
---

# Observability and Logging

> All hosts referenced here are fictional. `metrics.internal.acme.example`, `logs.internal.acme.example`, `traces.internal.acme.example`, and `status.acme.example` do not resolve. Sample code and queries are **simulated** for onboarding orientation only.

Observability is the contract between a service and the people who run it. At ACME Corp, every service that runs in production is required to emit structured logs, metrics, and traces — and to have a dashboard, an SLO, and an on-call rotation. This document defines how.

## 1. The Three Pillars

| Pillar | Endpoint (fictional) | Format | Retention | Tool (analogy) |
|--------|----------------------|--------|-----------|----------------|
| Metrics | `metrics.internal.acme.example` | Prometheus-style | 13 months | Prometheus-style |
| Logs | `logs.internal.acme.example` | JSON, structured | 30 days hot, 1 year cold | Loki-style |
| Traces | `traces.internal.acme.example` | OpenTelemetry OTLP | 7 days sampled, 30 days 1% head-based | Tempo-style |

The status page lives at `https://status.acme.example`. Incidents visible to customers are posted there.

## 2. Structured Logging

All logs are **JSON objects, one per line**. Every ACME service uses the shared logger from `acme-shared-libraries`:

| Language | Import path |
|----------|-------------|
| Go | `acme.internal/shared/logging` |
| Python | `acme.shared.logging` |
| TypeScript | `@acme/shared-logging` |
| Java | `com.acme.shared.logging` |

### Required fields on every log line

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `ts` | RFC3339 with nanoseconds | `2026-09-15T09:42:11.123456789Z` | UTC, always |
| `level` | enum | `debug`, `info`, `warn`, `error`, `fatal` | No `panic`-level — let the runtime panic |
| `service` | string | `acme-cloud-api` | Matches the service-catalog name |
| `version` | semver | `v2026.09.3` | The deployed version |
| `trace_id` | string | `7e3f9a1c8b4d4d7e9c1f2b3a4d5e6f70` | From the OTel context |
| `span_id` | string | `b3a4d5e6f70a1` | From the OTel context |
| `msg` | string | `quota.Allow returned unexpected nil` | One-line human description |

### Optional, common fields

| Field | When to set |
|-------|-------------|
| `tenant_id` | Whenever a tenant context exists |
| `user_id` | Whenever an end-user context exists (use the ACME opaque ID, never email) |
| `request_id` | When the upstream gateway propagates one |
| `component` | File:line of the log call site |
| `latency_ms` | For timed operations |
| `error` | The error type name (no stack trace in the log — use traces for that) |

### Sample log line

```json
{
  "ts": "2026-09-15T09:42:11.123456789Z",
  "level": "warn",
  "service": "acme-cloud-api",
  "version": "v2026.09.3",
  "trace_id": "7e3f9a1c8b4d4d7e9c1f2b3a4d5e6f70",
  "span_id": "b3a4d5e6f70a1",
  "tenant_id": "t-bug",
  "user_id": "u-anonymous",
  "msg": "quota.Allow returned unexpected nil",
  "remaining": -1,
  "component": "internal/quota/checker.go:84",
  "latency_ms": 3
}
```

## 3. No PII in Logs

PII is **never** logged. This includes:

- Email addresses.
- Phone numbers.
- Government identifiers (PAN, Aadhaar, SSN, passport).
- Payment instrument numbers (use the last-4 with a hash).
- IP addresses (truncate to /24, or hash).
- Customer-provided names (use the opaque tenant / user ID).
- Free-text fields that may contain PII.

The CI `ci/secret-scan` and a separate `ci/pii-scan` job both check diffs and runtime log samples. A PII leak is treated as a SEV2 security incident — see [`../../03-security/security-incident-reporting.md`](../../03-security/security-incident-reporting.md) and [`../../03-security/customer-data-handling.md`](../../03-security/customer-data-handling.md).

## 4. Metrics — RED for Services, GOLDEN Signals for Systems

ACME adopts two complementary frameworks:

| Framework | Scope | Signals |
|-----------|-------|---------|
| **RED** | Request-driven services (APIs, RPCs) | Rate, Errors, Duration |
| **USE** | Resource utilization (CPU, disk, network) | Utilization, Saturation, Errors |
| **Golden Signals** | Combined dashboard for any system | Latency, Traffic, Errors, Saturation |

### RED metrics (required for every service endpoint)

| Metric name | Type | Labels |
|-------------|------|--------|
| `acme_http_requests_total` | counter | `service`, `route`, `method`, `status` |
| `acme_http_request_duration_seconds` | histogram | `service`, `route`, `method` |
| `acme_http_in_flight_requests` | gauge | `service`, `route` |

### Golden Signals dashboard (per service)

A pre-built dashboard exists for every service at `https://metrics.internal.acme.example/d/<service-slug>`. It includes:

- Latency p50, p95, p99 over the last hour and last 7 days.
- Request rate by route and status code.
- Error rate (4xx vs 5xx).
- Saturation (CPU, memory, file descriptors, connection pool).
- SLO burn rate (see below).

## 5. SLOs Per Service

Every service publishes **at least one SLO** in the service catalog (`https://catalog.acme.example`). The default ACME SLO template:

| Tier | SLI | Target | Window |
|------|-----|--------|--------|
| **Tier 1 — customer-facing** | Availability (non-5xx) | 99.95% | 28 days rolling |
| **Tier 1 — customer-facing** | Latency p95 | ≤ 500 ms | 7 days rolling |
| **Tier 2 — internal API** | Availability (non-5xx) | 99.9% | 28 days rolling |
| **Tier 2 — internal API** | Latency p99 | ≤ 2 s | 7 days rolling |
| **Tier 3 — batch / async** | Job success rate | 99% | 7 days rolling |

A service may have additional SLOs (e.g., freshness for streaming pipelines). All SLOs are defined in the service's `deploy/slo/*.yaml` and rendered into Prometheus recording rules by the platform team. See [`../repositories/acme-platform-infrastructure.md`](../repositories/acme-platform-infrastructure.md).

### Burn-rate alerting

Alerts fire when the SLO burn rate exceeds thresholds in **both** a short and long window:

- **Page** (SEV2): 2% budget burn in 1h **and** 1% burn in 6h.
- **Page** (SEV1): 5% budget burn in 5m **and** 2% burn in 1h.
- **Ticket** (SEV3): 10% budget burn in 3d **and** 5% burn in 14d.

The multi-window/multi-burn-rate pattern avoids both over-paging and missing slow-burn regressions.

## 6. Tracing

Every service emits OpenTelemetry traces via OTLP to `traces.internal.acme.example`. The tracing client is initialized by the shared logger bootstrap. Required spans:

- Inbound HTTP/gRPC: server span with `http.method`, `http.route`, `http.status_code`.
- Outbound HTTP/gRPC: client span with the same set.
- Database calls: span with `db.system`, `db.statement` (without parameters), `db.operation`.
- Long-running operations: span named for the operation, with `component` and a `latency_ms` attribute.

Sampling: head-based 1% always-on; tail-based additional 10% for erroring traces. All traces that contain an error span are kept 100%.

A trace ID is propagated through every log line, every internal call, and every Kafka message header (`traceparent`). This is what makes a cross-service debugging session tractable — see [Debugging](./debugging.md).

## 7. Dashboards Per Service

Every service has:

1. **An overview dashboard** — the Golden Signals. Linked from the service-catalog entry.
2. **A dependencies dashboard** — downstream calls, with their latency and error rate, by route.
3. **A saturation dashboard** — CPU, memory, disk, connection pools, queue depths.
4. **An SLO dashboard** — burn rate, error budget, current trajectory.

Dashboards are defined as code in `deploy/dashboards/*.json` and rendered into the metrics platform by the platform team's `dashboards-as-code` pipeline.

## 8. Alert Routing

Alerts route to the on-call rotation via the fictional pager endpoint `pager.acme.example`. The routing rules:

| Severity | Channel | Response SLA |
|----------|---------|--------------|
| SEV1 | Page primary + secondary on-call | Ack ≤ 5 min; mitigation ≤ 30 min |
| SEV2 | Page primary on-call | Ack ≤ 15 min; mitigation ≤ 2 h |
| SEV3 | Slack + ticket | Ack ≤ 4 business hours |
| SEV4 | Ticket only | Next business day |

See [Incident response](./incident-response-and-on-call-introduction.md) for the incident commander role and the postmortem process.

## 9. Logging Anti-Patterns

| Anti-pattern | Why it's wrong | Fix |
|--------------|----------------|------|
| Free-text `fmt.Sprintf` logs | Not parseable, loses fields | Structured logger with fields |
| Logging full request bodies | PII, size, cost | Hash sensitive fields; truncate bodies |
| `level=info` for everything | Noise; alerting impossible | Use `debug`, `info`, `warn`, `error` deliberately |
| Missing `trace_id` | Breaks cross-service debugging | Use the shared logger bootstrap |
| Logging in a hot loop | Cost, cardinality | Sample, or move to debug |
| Stack traces in log lines | Bloats Loki; available in trace | Log the error type, link the trace |
| Logging the same line on every retry | Cardinality explosion | Log at the end of the retry loop, with `attempts` |

## 10. Cardinality Budget

Every service has a **cardinality budget** — the maximum number of unique label combinations its metrics can produce. The platform team's `metrics-cardinality-bot` alerts when a service exceeds 80% of its budget. Common causes:

- A label that includes a tenant ID, user ID, or request ID.
- A label that includes a free-text error message.
- A label that includes a high-cardinality version string per-build.

Cardinality violations are a P2 ticket against the owning team. See [`../repositories/acme-platform-infrastructure.md`](../repositories/acme-platform-infrastructure.md).

## 11. Sample Instrumentation (Go)

```go
package quota

import (
    "context"

    "github.com/acme/internal/shared/logging"
    "github.com/acme/internal/shared/metrics"
    "go.opentelemetry.io/otel"
)

var (
    allowCounter = metrics.NewCounterVec(
        "acme_quota_allow_total",
        []string{"tenant_id", "result"},
    )
)

// Allow returns nil if the tenant may create a new resource.
func (c *Checker) Allow(ctx context.Context, tenantID, kind string) error {
    ctx, span := otel.Tracer("quota").Start(ctx, "Allow")
    defer span.End()
    span.SetAttributes(attribute.String("tenant.id", tenantID))

    log := logging.FromContext(ctx).With("tenant_id", tenantID)
    // ...
    if err := c.store.Check(ctx, tenantID); err != nil {
        log.Warn("quota check failed", "error", err.Error())
        allowCounter.Inc(tenantID, "error")
        return err
    }
    allowCounter.Inc(tenantID, "ok")
    return nil
}
```

## 12. Cross-Reference Table

| Need | See |
|------|-----|
| How logs/traces are used for debugging | [`./debugging.md`](./debugging.md) |
| Environments where logs are emitted | [`./development-staging-production.md`](./development-staging-production.md) |
| Incident severity and routing | [`./incident-response-and-on-call-introduction.md`](./incident-response-and-on-call-introduction.md) |
| Release canary and SLO watch | [`./release-management.md`](./release-management.md) |
| Customer data handling | [`../../03-security/customer-data-handling.md`](../../03-security/customer-data-handling.md) |
| Security incident reporting | [`../../03-security/security-incident-reporting.md`](../../03-security/security-incident-reporting.md) |
| Shared libraries (logger) | [`../repositories/acme-shared-libraries.md`](../repositories/acme-shared-libraries.md) |
| Platform infrastructure (metrics) | [`../repositories/acme-platform-infrastructure.md`](../repositories/acme-platform-infrastructure.md) |

## Related Documents

- [`../repository-catalog.md`](../repository-catalog.md)
- [`./coding-standards.md`](./coding-standards.md)
- [`./ci-cd-overview.md`](./ci-cd-overview.md)
- [`./debugging.md`](./debugging.md)
- [`./development-staging-production.md`](./development-staging-production.md)
- [`./release-management.md`](./release-management.md)
- [`./incident-response-and-on-call-introduction.md`](./incident-response-and-on-call-introduction.md)
- [`./internal-package-management.md`](./internal-package-management.md)
- [`../repositories/acme-shared-libraries.md`](../repositories/acme-shared-libraries.md)
- [`../repositories/acme-platform-infrastructure.md`](../repositories/acme-platform-infrastructure.md)
- [`../repositories/acme-cloud-api.md`](../repositories/acme-cloud-api.md)
- [`../../03-security/customer-data-handling.md`](../../03-security/customer-data-handling.md)
- [`../../03-security/security-incident-reporting.md`](../../03-security/security-incident-reporting.md)
- [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md)
- [`../../09-contacts/contact-directory.md`](../../09-contacts/contact-directory.md)
- [`../../metadata/glossary.md`](../../metadata/glossary.md)
