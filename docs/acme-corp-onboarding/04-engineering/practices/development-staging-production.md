---
document_id: ACME-ENG-011
title: Development, Staging, and Production Environments
category: engineering
department: engineering
applicable_roles: [engineers]
owner: Engineering
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [engineering, practices, environments, production, pim, least-privilege]
---

# Development, Staging, and Production Environments

> All hosts referenced here are fictional. `vault.acme.example`, `runners.internal.acme.example`, and `registry.internal.acme.example` do not resolve. Sample commands are **simulated** for onboarding orientation only.

ACME Corp operates three environment tiers: **dev**, **staging**, and **production**. The rules below are non-negotiable; they are enforced by CI, by Vault, by network policy, and by review.

## 1. Environment Definitions

| Environment | Purpose | Data | Access | Trigger |
|-------------|---------|------|--------|---------|
| `dev` | Per-developer or ephemeral sandbox. | Synthetic data only. | Standing, per engineer. | Merge to `main`. |
| `staging` | Shared, pre-prod integration with partner systems and downstream services. | Synthetic, plus production-shaped fixtures. | Standing read; standing limited write for tests. | Tag `v*`. |
| `production` | Customer-facing. | Real customer data, regulated. | **No standing access.** PIM-elevated, time-boxed. | Tagged release + change ticket + dual approval. |

### Sub-environments

Within each tier there may be sub-environments:

- `dev-eu-west`, `dev-ap-south` — regional dev sandboxes.
- `staging-partner-a` — a sandboxed staging slice for a partner integration.
- `prod-eu-west`, `prod-ap-south`, `prod-us-east`, `prod-us-west` — regional production deployments.

The full list is published in the service catalog at `https://catalog.acme.example/environments`.

## 2. What Is Allowed Where

| Activity | dev | staging | production |
|----------|-----|---------|------------|
| Deploy a build | Auto on merge to `main` | Auto on tag `v*` | Manual, dual approval (release manager + on-call SRE) |
| Run integration tests | Yes, ephemeral | Yes, scheduled nightly + on tag | No |
| Read logs | Yes, your sandbox | Yes | Yes, read-only via `logs.internal.acme.example` |
| Read customer data | No — synthetic only | No — synthetic only | No. Customer data is accessed via the customer-support tooling only, with audit. |
| SSH into a pod | Yes | Yes, with EM approval | **No** standing SSH. PIM-elevated break-glass for SEV1, recorded. |
| Run a manual SQL query | Yes, against dev RDS | Yes, against staging RDS, with EM approval | **No**. Production queries run via the read-replica service only, PIM-elevated, time-boxed. |
| Run a debug build | Yes | Yes, with EM approval | **No** |
| Push a hotfix | n/a | n/a | Yes, via the hotfix procedure (see [Release management](./release-management.md)) |

## 3. Data Rules

The data rules are simple and absolute:

- **No production data in dev.** Ever. Not a sample. Not a row. Not a column.
- **No production data in staging.** Staging uses production-shaped synthetic data produced by the ACME fake-data generator (see [`../repositories/acme-shared-libraries.md`](../repositories/acme-shared-libraries.md)).
- **No customer PII in any non-production log.** The `ci/pii-scan` job in CI rejects diffs that introduce literal PII; runtime log sampling in dev and staging rejects log lines that look like PII.
- **Anonymized, aggregated data may be replicated to staging** for performance testing, with the data residency and retention rules below applied.
- **Production data exports** require a Security GRC ticket, an EM sign-off, and an expiry date — see [`../../03-security/customer-data-handling.md`](../../03-security/customer-data-handling.md).

### Data residency

ACME operates in multiple regions. Customer data residency is enforced per tenant:

- EU tenants' data stays in `prod-eu-west`.
- India tenants' data stays in `prod-ap-south`.
- US tenants' data stays in `prod-us-east` or `prod-us-west`.

Cross-region replication is restricted to derived, aggregated, anonymized metrics only. The Vault-backed per-tenant region lock prevents accidental cross-region reads. See [`../../03-security/customer-data-handling.md`](../../03-security/customer-data-handling.md) for the residency matrix.

## 4. Access Rules

The access rules are based on least privilege — see [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md).

### 4.1 Standing access

| Identity | dev | staging | production |
|----------|-----|---------|------------|
| Engineer (own team) | Read/write | Read-only | Read-only logs |
| Engineer (other team) | Read-only | Read-only | Read-only logs |
| EM | Read-only | Read-only | Read-only logs |
| On-call SRE (during shift) | Read/write | Read/write | PIM-elevated, time-boxed |
| Release manager (current rotation) | Read | Read | PIM-elevated for release window |
| Security GRC | Read | Read | Read, plus break-glass |

### 4.2 Standing production access — none

**No new employee gets standing production access.** This is true for:

- New hires in their first 30 days (see [`../../07-workflows/first-30-days.md`](../../07-workflows/first-30-days.md)).
- New hires in their first 90 days.
- Senior engineers.
- EMs.
- The CTO (Sridhar Venkatesh) and the Director of AI/ML (Anitha Rajan).

Production access is **always** PIM-elevated, time-boxed, single-purpose, and audited. The only standing production identity is the CI service account (`ci-bot@acme.example`), and it can only promote a tagged image — it cannot SSH, cannot query the database, cannot read secrets.

## 5. PIM Flow for Production Access

Production access is requested through the Privileged Identity Management (PIM) flow:

1. **Request.** Engineer files a PIM request from the IT self-service portal at `https://itsm.acme.example/pim/request`. The request specifies:
   - Target role (e.g., `prod-cloud-api-ssh`, `prod-cloud-api-db-read`).
   - Justification (a ticket, an incident ID, a release window).
   - Duration (default 1h; max 4h; max 24h for an active SEV1 with IC sign-off).
2. **Approve.** Two approvals are required:
   - The on-call SRE on the matching rotation.
   - The current release manager (for release-window requests) or the incident commander (for SEV1/SEV2 requests).
3. **Activate.** On approval, Vault issues a short-lived token scoped to the requested role, with the requested duration. The token is fetched automatically by the requester's authenticated session; it is never emailed or pasted.
4. **Use.** The engineer uses the token within the activation window. Every action is logged with the requester's identity, the role, the justification, and the timestamp.
5. **Expire.** The token expires automatically. There is **no renewal** — a new request is required for further access.
6. **Audit.** Every PIM elevation is reviewed weekly by Security GRC. Anomalous patterns (same person, same role, daily) trigger a follow-up.

### Sample PIM request

```bash
# fictional/simulated command — file a PIM request for prod DB read access
acme-pim request \
  --role prod-cloud-api-db-read \
  --duration 1h \
  --ticket CLOUD-1301 \
  --justification "investigate SEV2 quota regression; IC is on-call SRE"

# fictional/simulated command — Vault issues the token after approval
export VAULT_TOKEN=$(acme-pim collect --request-id pim-2026-09-15-001)
vault kv get -mount=prod/cloud-api secret/db-ro-credentials
```

## 6. Break-Glass

For a SEV1 where the PIM flow itself is impaired (e.g., Vault is the system that is broken), there is an emergency break-glass procedure:

1. Page the Platform Infrastructure on-call (`pager.acme.example/platform`).
2. The on-call SRE retrieves the sealed break-glass credentials from a physical safe in the Hyderabad and London offices — see [`../../09-contacts/contact-directory.md`](../../09-contacts/contact-directory.md) for the safe custodian.
3. The on-call SRE uses the credentials **only** to restore the PIM flow, not to fix the underlying incident.
4. Every use of break-glass requires a postmortem within 5 business days (see [Incident response](./incident-response-and-on-call-introduction.md)).

Break-glass is exercised quarterly in a tabletop drill led by Asha Reddy's Quality Engineering team.

## 7. CI/CD and Environments

The CI/CD pipeline (see [CI/CD overview](./ci-cd-overview.md)) maps onto the environment tiers as follows:

| Environment | Deploy trigger | Approval | Notes |
|-------------|----------------|----------|-------|
| `dev` | Merge to `main` | Auto (CI) | Ephemeral namespace per PR or per engineer |
| `staging` | Tag `v*` on `main` | Auto (tag implies approval) | Shared; integrated with partner systems |
| `production` | Tagged release + change ticket | Manual: release manager + on-call SRE | Canary 5% → 25% → 100%; SLO watch between ramps |

The `production` GitHub Actions environment requires a member of the `release-managers` team and an on-call SRE to approve — and both of those are themselves PIM-elevated roles.

## 8. Cost and Capacity

Each environment has a cost ceiling:

| Environment | Monthly ceiling (fictional) | Owner |
|-------------|------------------------------|-------|
| `dev` (aggregate, all engineers) | $40,000 | Platform Infrastructure |
| `staging` | $80,000 | Platform Infrastructure |
| `production` | cost-of-goods, tracked against revenue | Per-product finance |

The platform team's `cost-bot` alerts when an environment exceeds 80% of its ceiling. Dev sandboxes idle for > 7 days are auto-suspended.

## 9. Anti-Patterns

| Anti-pattern | Why it's wrong | Fix |
|--------------|-----------------|------|
| Copying a production DB snapshot to staging | Violates data residency, customer data | Use the ACME fake-data generator |
| Using a real customer email as a test user | PII leak | Use the fake-data generator |
| Sharing a prod credential across engineers | Breaks audit | Use PIM, per request |
| Asking for "just one prod SSH, 10 minutes" | Foot in the door | Use the PIM flow — it really is fast |
| Leaving a PIM session open longer than needed | Window of risk | Close the session when done |
| Running ad-hoc prod queries during a deploy | Contamination risk | Use the read-replica service, PIM-elevated |
| Bypassing PIM "just this once" | Pattern of bypasses | Never. Escalate if PIM is broken. |

## 10. Cross-Reference Table

| Need | See |
|------|-----|
| CI/CD pipeline and environment gates | [`./ci-cd-overview.md`](./ci-cd-overview.md) |
| Release cadence and canary procedure | [`./release-management.md`](./release-management.md) |
| Incident response and PIM during SEV1 | [`./incident-response-and-on-call-introduction.md`](./incident-response-and-on-call-introduction.md) |
| Least-privilege policy basis | [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md) |
| Secrets and Vault | [`../../03-security/secrets-management.md`](../../03-security/secrets-management.md) |
| Customer data residency | [`../../03-security/customer-data-handling.md`](../../03-security/customer-data-handling.md) |
| IT access revocation (offboarding) | [`../../02-it/it-access-revocation.md`](../../02-it/it-access-revocation.md) |
| IT access request form | [`../../08-forms/it-access-request.md`](../../08-forms/it-access-request.md) |

## Related Documents

- [`../repository-catalog.md`](../repository-catalog.md)
- [`./git-branching-strategy.md`](./git-branching-strategy.md)
- [`./pull-requests-and-code-review.md`](./pull-requests-and-code-review.md)
- [`./ci-cd-overview.md`](./ci-cd-overview.md)
- [`./observability-and-logging.md`](./observability-and-logging.md)
- [`./debugging.md`](./debugging.md)
- [`./release-management.md`](./release-management.md)
- [`./incident-response-and-on-call-introduction.md`](./incident-response-and-on-call-introduction.md)
- [`../repositories/acme-cloud-api.md`](../repositories/acme-cloud-api.md)
- [`../repositories/acme-platform-infrastructure.md`](../repositories/acme-platform-infrastructure.md)
- [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md)
- [`../../03-security/secrets-management.md`](../../03-security/secrets-management.md)
- [`../../03-security/customer-data-handling.md`](../../03-security/customer-data-handling.md)
- [`../../03-security/data-classification.md`](../../03-security/data-classification.md)
- [`../../02-it/it-access-revocation.md`](../../02-it/it-access-revocation.md)
- [`../../08-forms/it-access-request.md`](../../08-forms/it-access-request.md)
- [`../../07-workflows/first-30-days.md`](../../07-workflows/first-30-days.md)
- [`../../09-contacts/contact-directory.md`](../../09-contacts/contact-directory.md)
- [`../../metadata/glossary.md`](../../metadata/glossary.md)
