---
document_id: ACME-ENG-013
title: Incident Response and On-Call Introduction
category: engineering
department: engineering
applicable_roles: [engineers]
owner: Engineering
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [engineering, practices, incident-response, on-call, sev, postmortem]
---

# Incident Response and On-Call Introduction

> All hosts referenced here are fictional. `pager.acme.example`, `status.acme.example`, `logs.internal.acme.example`, and `traces.internal.acme.example` do not resolve. Sample commands are **simulated** for onboarding orientation only.

This document is the **introduction** to incident response and on-call at ACME Corp. It defines incident severity levels, the on-call rotation, the incident commander role, communication channels, and the postmortem process. New hires are expected to read this document before their first shadow on-call shift (see §7).

For the formal policy basis, see [`../../03-security/security-incident-reporting.md`](../../03-security/security-incident-reporting.md).

## 1. Incident Severity

ACME uses a four-level severity scale:

| Severity | Definition | Examples | Response SLA | Owner |
|----------|------------|----------|---------------|-------|
| **SEV1** | Customer-facing outage or data loss; or active security incident affecting production. | Cloud API 5xx > 10% for 5 min; Workspace unavailable in a region; suspected breach | Page primary + secondary on-call; ack ≤ 5 min; mitigation ≤ 30 min | Incident Commander |
| **SEV2** | Major feature degraded with broad customer impact, no clean workaround. | Quota API returning wrong values for 5%+ of tenants; auth refresh broken intermittently | Page primary on-call; ack ≤ 15 min; mitigation ≤ 2 h | Incident Commander |
| **SEV3** | Limited customer impact or workaround available; or internal-only degradation. | A non-critical API 5xx above baseline; a slow query path on staging | Slack alert + ticket; ack ≤ 4 business hours | Owning team |
| **SEV4** | Minor, no customer impact; cosmetic or feature-request-grade. | A typo in an error message; a missed doc link | Ticket only; next business day | Owning team |

Severity can be **upgraded** or **downgraded** during an incident. Upgrades are encouraged when in doubt — better to over-respond than to miss a SEV1.

## 2. On-Call Rotation

Each team owns one or more on-call rotations. A rotation is:

- **One week long**, Monday 09:00 IST to the next Monday 09:00 IST.
- **Primary + secondary**: the primary is paged first; the secondary is paged if the primary does not ack within 5 minutes (SEV1) or 15 minutes (SEV2).
- **Frequency: 1 week in 6** on average (each rotation has ~6 engineers). The cadence is set by the team's EM.
- **Follow-the-sun**: Hyderabad and London cover EU/India business hours; Seattle covers Americas; rotations hand off at 09:00 local.

### Rotations per team

| Team | Rotation name | EM | Coverage |
|------|---------------|-----|----------|
| Cloud API | `cloud-api-oncall` | Anjali Desai | 24×7 |
| Cloud Frontend | `cloud-fe-oncall` | Manoj Pillai | Business hours + on-call SE |
| Intelligence Agents | `agents-oncall` | Rohan Bhat | 24×7 |
| Intelligence Inference | `inference-oncall` | Vivek Anand | 24×7 |
| Intelligence ML | `ml-oncall` | Lakshmi Narayan | Business hours |
| Workspace Web | `ws-web-oncall` | Thomas Buckley | Business hours + on-call SE |
| Workspace API | `ws-api-oncall` | Priya Menon | 24×7 |
| Platform Infrastructure | `platform-oncall` | Nikhil Joshi | 24×7 |
| Quality Engineering | `qe-oncall` | Asha Reddy | Business hours |

### Paging endpoint

Pages fire through the fictional pager endpoint `pager.acme.example`. The endpoint integrates with the on-call app on your phone. Pages include:

- Severity, summary, and a link to the runbook.
- Trace IDs and metric snapshot links.
- The Slack channel for the incident.
- The incident commander (if assigned) or a hint to assign one.

```bash
# fictional/simulated command — page the on-call rotation manually
acme-pager page \
  --rotation cloud-api-oncall \
  --severity SEV2 \
  --summary "Quota API returning 429 for tenants in eu-west" \
  --runbook https://wiki.acme.example/cloud/api/runbooks/quota-429
```

## 3. Incident Commander Role

Every SEV1 and SEV2 has an **Incident Commander (IC)**. The IC is **not** the person doing the technical mitigation — the IC coordinates.

### IC responsibilities

1. **Declare.** Confirm the severity, page the right rotations, open the incident channel (`#incident-<YYYY-MM-DD>-<slug>`).
2. **Coordinate.** Assign roles: scribe (writes the timeline), comms (updates status page), mitigator (does the work).
3. **Time-box.** Make a mitigation decision every 15 minutes; if the mitigation isn't working, escalate or roll back.
4. **Communicate.** Updates to the customer status page (`status.acme.example`) every 30 minutes during a SEV1, hourly during a SEV2.
5. **De-escalate.** When the system recovers, declare the incident mitigated (not resolved — resolved comes after postmortem).
6. **Handover.** If the incident spans a shift change, brief the next IC explicitly and post the briefing in the channel.

### Who can be IC

ICs are senior engineers who have completed the IC training module (`acme-quality-automation` repo ships a tabletop drill). The IC pool per rotation is reviewed annually by the EM and the Director of AI/ML (Anitha Rajan) or the VP Engineering (Sridhar Venkatesh).

## 4. Communication Channels

| Channel | Use | Audience |
|---------|-----|----------|
| `pager.acme.example` | Initial page to on-call | On-call rotation |
| Slack `#incident-<YYYY-MM-DD>-<slug>` | Real-time coordination during the incident | IC, mitigators, scribe, comms, EM |
| Slack `#incidents` | Read-only broadcast of active incidents | All engineers |
| `status.acme.example` | Customer-facing status updates | Customers, support |
| Email `customers@acme.example` | Post-incident summary | Customers (via DevRel) |
| ITSM portal `itsm.acme.example` | Change tickets, postmortem record | Internal, auditable |

### Incident channel conventions

- The channel name follows `#incident-<YYYY-MM-DD>-<short-slug>` — e.g., `#incident-2026-09-15-quota-429`.
- The first message in the channel is a pinned **status block** with: severity, summary, current mitigation owner, next update time.
- Updates are posted in-channel as replies to the status block.
- The channel is archived 30 days after the postmortem is published.

## 5. Mitigation vs. Fix

The IC's goal during an incident is **mitigation**, not fix.

- **Mitigation** = stop the bleeding. Roll back. Flip a feature flag. Shed load. Block a tenant. Mitigation is reversible and fast.
- **Fix** = address the root cause. Requires a PR, a test, a canary, a release. The fix lands after the incident is mitigated.

An IC who tries to fix during an incident typically makes things worse. Mitigate first, fix later.

## 6. Postmortem Process

Every SEV1 and SEV2 requires a **blameless postmortem** within **5 business days** of mitigation.

### Blameless

Postmortems at ACME are **blameless**. The assumption is that everyone involved acted with the information and tools they had. The postmortem asks:

- What latent conditions in our system, process, or culture allowed this incident to occur?
- What would have caught this earlier? What would have made the mitigation faster?
- What action items will we ship, by when, with which owner?

The postmortem does **not** ask "who is at fault." The postmortem document is **not** used in performance reviews.

### Document

The postmortem lives in `docs/postmortems/<YYYY-MM-DD>-<slug>.md` in the owning repository. Template:

```markdown
# Postmortem — <YYYY-MM-DD> <slug>

## Summary
<!-- 2-3 sentences. -->

## Impact
<!-- Customer-facing impact: how many tenants, for how long, what was broken. -->

## Timeline (all times UTC)
- 09:42 — First alert fires (link to alert).
- 09:43 — On-call acks; IC declared.
- 09:51 — Rollback started.
- 09:58 — Rollback complete; SLO recovering.
- 10:15 — Incident mitigated.

## Root cause
<!-- The technical root cause, e.g., "a nil-pointer deref in the
quota cache when the cache TTL expired before refresh." -->

## Contributing factors
<!-- Latent conditions: e.g., "the cache-refresh path was not
covered by the integration tests because the test harness did
not exercise the TTL expiry path." -->

## What went well
- Alert fired within 30s of impact.
- Rollback procedure was rehearsed in the quarterly drill.

## What went badly
- The cache-refresh path had no test coverage.
- The runbook for this alert did not mention the cache.

## Action items
- [ ] [CLOUD-1401] Add integration test for cache TTL expiry. Owner: A. Desai. Due: 2026-09-30.
- [ ] [CLOUD-1402] Update the quota-429 runbook with the cache-refresh step. Owner: R. Pillai. Due: 2026-09-22.
- [ ] [CLOUD-1403] Add a metric for cache-refresh latency. Owner: N. Joshi. Due: 2026-10-15.
```

### Review

The postmortem is reviewed by:

1. The owning EM.
2. The Director of AI/ML (Anitha Rajan) for Intelligence incidents; the VP Engineering (Sridhar Venkatesh) for Cloud/Workspace.
3. Security GRC for any incident with a security component.
4. The Quality Engineering team for trend analysis across postmortems.

Action items are tracked in the team's ITSM board; overdue items surface in the EM's weekly review.

## 7. New Hire Shadow On-Call

Every new engineering hire at ACME is expected to **shadow on-call** during their first **60 days**. The shadow on-call:

1. Is added as a silent observer to the team's `*-oncall` rotation.
2. Receives the same pages as the primary on-call (but is not expected to ack or mitigate).
3. Joins the incident channel for any incident during their shadow week.
4. Pairs with the primary on-call on the runbook walk-through, pre-incident.

The shadow on-call is **not** a paging target — there is no expectation of ack. The shadow's job is to learn the runbook, the IC's coordination rhythm, and the postmortem process before they take a primary rotation of their own (typically at the 6-month mark, when the rotation comes around to them).

The shadow on-call is scheduled by the EM during the [`../../07-workflows/first-30-days.md`](../../07-workflows/first-30-days.md) checkpoint and tracked through the [`../../07-workflows/first-week-onboarding.md`](../../07-workflows/first-week-onboarding.md) workflow.

## 8. Standing Production Access (Restated)

**No new employee gets standing production access.** This applies to incident response as well: even during a SEV1, the on-call SRE's production access is **PIM-elevated**, time-boxed to the incident, and expired when the incident is mitigated. The IC role itself does not carry production access — the IC coordinates; the on-call SRE mitigates with PIM-elevated credentials. See [`./development-staging-production.md`](./development-staging-production.md) and [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md).

The only exception is **break-glass** (see [`./development-staging-production.md`](./development-staging-production.md) §6), which is reserved for cases where the PIM flow itself is broken. Break-glass use always triggers a postmortem.

## 9. On-Call Hygiene

- **Swap coverage.** If you cannot take your rotation, you must arrange a swap with another rotation member **and** notify the EM at least 1 week in advance. Last-minute swaps are an exception, not the rule.
- **Laptop and phone.** On-call means your laptop is with you, charged, and connected. Your phone has the pager app installed and notifications on. Do not put yourself on a flight during your shift.
- **Acknowledge fast.** Even if you don't know the answer yet, ack within the SLA. Ack = "I am looking." Then update with findings.
- **Page early, page often.** If you're not sure whether to escalate, escalate. The cost of an unnecessary page is one annoyed engineer; the cost of a missed SEV1 is a customer-visible outage.
- **Sleep.** Do not work on the mitigation past 2 hours without handing off to the secondary. Fatigued mitigation is worse than no mitigation.

## 10. Cross-Reference Table

| Need | See |
|------|-----|
| Observability and SLO burn alerts | [`./observability-and-logging.md`](./observability-and-logging.md) |
| Debugging an incident | [`./debugging.md`](./debugging.md) |
| Rollback runbook and canary | [`./release-management.md`](./release-management.md) |
| Environments and PIM elevation | [`./development-staging-production.md`](./development-staging-production.md) |
| CI/CD deploy pipeline | [`./ci-cd-overview.md`](./ci-cd-overview.md) |
| Security incident reporting policy | [`../../03-security/security-incident-reporting.md`](../../03-security/security-incident-reporting.md) |
| Customer data handling during incidents | [`../../03-security/customer-data-handling.md`](../../03-security/customer-data-handling.md) |
| Least-privilege and PIM | [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md) |
| First 30 days (shadow on-call scheduling) | [`../../07-workflows/first-30-days.md`](../../07-workflows/first-30-days.md) |
| First week onboarding | [`../../07-workflows/first-week-onboarding.md`](../../07-workflows/first-week-onboarding.md) |
| Contact directory (EMs, IC pool) | [`../../09-contacts/contact-directory.md`](../../09-contacts/contact-directory.md) |

## Related Documents

- [`../repository-catalog.md`](../repository-catalog.md)
- [`./ci-cd-overview.md`](./ci-cd-overview.md)
- [`./observability-and-logging.md`](./observability-and-logging.md)
- [`./debugging.md`](./debugging.md)
- [`./development-staging-production.md`](./development-staging-production.md)
- [`./release-management.md`](./release-management.md)
- [`../repositories/acme-cloud-api.md`](../repositories/acme-cloud-api.md)
- [`../repositories/acme-platform-infrastructure.md`](../repositories/acme-platform-infrastructure.md)
- [`../repositories/acme-quality-automation.md`](../repositories/acme-quality-automation.md)
- [`../../03-security/security-incident-reporting.md`](../../03-security/security-incident-reporting.md)
- [`../../03-security/customer-data-handling.md`](../../03-security/customer-data-handling.md)
- [`../../03-security/least-privilege-access.md`](../../03-security/least-privilege-access.md)
- [`../../03-security/secrets-management.md`](../../03-security/secrets-management.md)
- [`../../02-it/it-support-and-troubleshooting.md`](../../02-it/it-support-and-troubleshooting.md)
- [`../../02-it/it-access-revocation.md`](../../02-it/it-access-revocation.md)
- [`../../07-workflows/first-week-onboarding.md`](../../07-workflows/first-week-onboarding.md)
- [`../../07-workflows/first-30-days.md`](../../07-workflows/first-30-days.md)
- [`../../09-contacts/contact-directory.md`](../../09-contacts/contact-directory.md)
- [`../../metadata/glossary.md`](../../metadata/glossary.md)
