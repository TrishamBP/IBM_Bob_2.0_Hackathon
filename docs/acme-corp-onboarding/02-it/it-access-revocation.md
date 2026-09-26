---
document_id: ACME-IT-018
title: IT Access Revocation
category: it
department: it-operations
applicable_roles: [all]
owner: Faisal Ahmed, Identity Engineer
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, revocation, separation, off-boarding, audit, fictional]
---

# IT Access Revocation

> ACME Corp fictional onboarding library. All workflows, SCIM endpoints, and audit log references are simulated for documentation. Microsoft Entra ID is real infrastructure; the ACME tenant configuration is fictional.

## 1. Purpose

Defines the **triggers** for IT access revocation (separation, role change, security event), the **sequence of revocation steps**, the **final-settlement timing** (the relationship to the last working day), the **emergency revocation** path for security incidents, and the **audit log retention** requirements that govern the records of these actions. This document pairs with [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) and is the inverse of [`new-employee-it-request.md`](new-employee-it-request.md).

## 2. Triggers for Revocation

| Trigger | Source | Initiated by |
|---------|--------|--------------|
| **Voluntary separation** (resignation) | HRIS state change → "Pending Separation" | HRBP on receipt of resignation letter |
| **Involuntary separation** (termination) | HRIS state change → "Pending Termination" | HRBP + Manager; review by Legal |
| **Role change** (internal move) | HRIS state change → "Pending Role Change" | HRBP + new manager |
| **Leave of absence** (sabbatical, extended medical) | HRIS state change → "On Leave" | HRBP |
| **Security event** (suspected compromise, insider threat) | Security incident ticket | CISO delegate (`rajan.mehta@acme.example`) |
| **Contractor end-date** | HRIS contract record | Procurement + HRBP (automatic) |
| **Review-driven revocation** (failed Access Review) | Access Review system | IT Helpdesk (automatic) |

## 3. Sequence of Revocation

> The clock starts when the HRIS state changes. For separations, the target is "all access disabled within 24 hours of last working day, device returned on last working day, final settlement within 7 business days."

### 3.1 Pre-Last-Working-Day (T-5 to T-1 business days)

1. **HRBP triggers the workflow.** The HRIS sends a webhook to the ITSM platform; an off-boarding ticket is created (e.g., `OFFBD-2026-000123` — simulated).
2. **IT Onboarding Specialist (Geetha Iyer) reviews** the role bundle, identifies all group memberships and SaaS app entitlements, and prepares a checklist.
3. **Manager sign-off** on the off-boarding plan (specifically: which data the departing employee must hand off, which repos they must archive, which dashboards they own).
4. **Data handover.** The departing employee transfers ownership of:
   - SharePoint sites → to their manager or successor.
   - GitHub Enterprise repos → to the team lead (transfers via `git.acme.example` admin console).
   - Jira / Confluence spaces → to the team lead.
   - 1Password shared vaults → the manager becomes the new owner; the departing employee's access is removed at T-0.
   - Dashboards / Datadog monitors → ownership transferred.
5. **Out-of-office + email forwarding** is set up on T-1 (the manager chooses: forward to a colleague, or auto-reply-only, or both). The mailbox is **not** deleted — it is retained for 90 days per [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md).

### 3.2 Last Working Day (T-0)

1. **Device return.** The employee returns the laptop and peripheral kit per [`device-acceptance-and-responsibility.md`](device-acceptance-and-responsibility.md) §return-on-separation. The IT depot verifies the asset tag, signs the return section of [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md), and updates ITAM.
2. **Device wipe.** Endpoint Engineering issues an Intune **Wipe** command; the BitLocker / FileVault recovery key is rotated.
3. **Entra ID account disable.** At the end of the last working day (default: 18:00 local time), Identity Engineering (Faisal Ahmed) disables the user object:
   - `AccountEnabled = false`.
   - All refresh tokens revoked (`RevokeSignInSessions`).
   - Group memberships preserved (for audit) but ineffective because the account is disabled.
4. **SaaS app access revoked** via SCIM:
   - Jira, Confluence, GitHub Enterprise, Datadog, Figma, Notion, 1Password — all de-provision within 60 minutes.
   - Salesforce — de-provisioned; the user remains in the Salesforce "deactivated" list for 90 days.
5. **VPN / Wi-Fi** access revoked (SCEP cert revoked, profile removed).
6. **MFA methods** are preserved (do not delete — needed for audit) but the account is disabled so they cannot be used.
7. **Email** remains active (mailbox retained, OOO active) for 90 days.

### 3.3 Post-Separation (T+1 to T+90 days)

1. **Final settlement.** HR completes the final settlement per [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) within 7 business days; IT certifies that no corporate device or access remains outstanding.
2. **Mailbox archive.** At T+90, the mailbox is archived to an Exchange Online inactive mailbox (retained 7 years for compliance).
3. **OneDrive / SharePoint content** is transferred to the manager (the manager becomes the site collection administrator of any personal sites) — this happens at T+30 by default.
4. **Records retention.** Audit logs (see §6) are retained for 7 years.

## 4. Final-Settlement Timing

| Stage | Owner | Timing |
|-------|-------|--------|
| Off-boarding ticket created | ITSM | T-5 business days |
| Data handover complete | Departing employee + manager | T-1 business day |
| Device returned | Employee → IT depot | T-0 (last working day) |
| Account disabled | Identity Engineering | T-0 end of day |
| SaaS access revoked | SCIM | T-0 + 60 minutes |
| Final settlement certified | IT + HR | T+7 business days |
| Mailbox archived | Identity Engineering | T+90 days |
| Audit logs retained | Compliance | T+7 years |

## 5. Emergency Revocation

> For suspected insider threat, security incident, or termination with immediate effect.

1. The CISO delegate (`rajan.mehta@acme.example`) or VP IT (`ramesh.khanna@acme.example`) phones the IT Helpdesk and Identity Engineering on-call.
2. Within **15 minutes**, Identity Engineering performs the following **simultaneously**:
   - Disable the Entra ID account.
   - Revoke all refresh tokens.
   - Revoke all app passwords.
   - Revoke all FIDO2 keys.
   - Disable the mailbox (set OOO to "Account disabled — contact `<manager-email>`").
   - Remove from all privileged groups (PIM eligibility revoked).
   - Trigger Intune Wipe on all registered devices.
3. Within **60 minutes**, SCIM revokes access to all SaaS apps.
4. Physical security is notified if the employee is on-site and asked to escort (HR-driven per [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md)).
5. A P1 incident ticket is opened; the post-incident review is scheduled within 5 business days.

## 6. Audit Log Retention

| Log source | Retention | Owner |
|------------|-----------|-------|
| Entra ID sign-in logs | 7 years | Identity Engineering |
| Entra ID audit logs (group membership changes, role activations) | 7 years | Identity Engineering |
| Intune device actions (wipe, retire, retire) | 7 years | Endpoint Engineering |
| Microsoft Purview audit log (M365 data access) | 7 years | Compliance |
| Defender for Endpoint telemetry | 6 months hot, 7 years cold | Security |
| 1Password audit log (vault access, item access) | 7 years | Identity Engineering |
| GitHub Enterprise audit log (repo access, push events) | 7 years | Engineering IT |
| ITSM ticket history | 7 years | IT Helpdesk |
| Wi-Fi RADIUS auth logs | 1 year | Network Engineering |
| VPN session logs | 7 years | Network Engineering |

> All logs are immutable and stored in Microsoft Purview's audit-log retention pipeline with Legal Hold where applicable (e.g., during litigation).

## 7. Role-Change Revocation

When an employee moves internally:

1. The HRIS state change → "Pending Role Change" triggers an off-boarding ticket **and** an on-boarding ticket (for the new role).
2. Access that is **no longer needed** is revoked (e.g., the engineer moving from Cloud to a non-engineering role loses GitHub Enterprise + AWS prod).
3. Access that is **newly needed** is granted via the new role bundle.
4. The transition is **not** instantaneous — it occurs over 1–3 business days; the employee retains access to the old bundle during the transition.
5. The manager (both old and new) sign off on the role-change plan.

## 8. Expected Outcomes

After this document:

- The employee / manager / HRBP knows the triggers and sequence of revocation.
- Identity Engineering has the runbook for the standard and emergency paths.
- Compliance has the audit-log retention schedule.

## 9. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| Disabled user still appears in Teams chats | Teams client cache lag | Teams client refreshes the roster within 24 hours; force-refresh via Settings → Clear cache. |
| SCIM de-provision failed for one app | SCIM token expired or app-side error | Identity Engineering re-runs the SCIM cycle manually; the app's admin console can also be used as a backstop. |
| Mailbox archive fails at T+90 | Litigation hold active | The mailbox is preserved for the duration of the hold; archive resumes on hold release. |
| GitHub Enterprise repo orphaned (no owner) | Repo owner was the only owner and was off-boarded | Engineering IT reassigns ownership to the team lead; per [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md) every repo must have ≥2 owners. |
| Emergency revocation performed without VP sign-off | Process violation | Post-incident review; the action itself stands (security first), but the workflow is corrected for next time. |
| Departing employee's device cannot be wiped (offline) | Device not checking in | Rely on encryption + token revocation; the device bricks for corporate use at next sign-in attempt. |

## 10. Approval Requirements

- **Standard separation (voluntary):** HRBP initiates; IT executes; no separate IT approval needed.
- **Involuntary termination:** HRBP + HR VP + Legal sign-off; IT executes.
- **Emergency revocation:** CISO delegate or VP IT can trigger directly (no HR pre-approval needed for the technical action; HR is notified in parallel).
- **Role-change:** HRBP + both managers.
- **Failed Access Review → auto-revocation:** IT Helpdesk executes; no human approval needed (the review itself is the approval).

## 11. Related Documents

- [`new-employee-it-request.md`](new-employee-it-request.md) — The inverse (provisioning) flow.
- [`device-acceptance-and-responsibility.md`](device-acceptance-and-responsibility.md) — Device return at separation.
- [`lost-or-stolen-device-reporting.md`](lost-or-stolen-device-reporting.md) — Emergency wipe on a per-device basis.
- [`microsoft-entra-id-and-sso.md`](microsoft-entra-id-and-sso.md) — Token revocation context.
- [`software-access-requests.md`](software-access-requests.md) — SCIM apps reviewed during revocation.
- [`equipment-replacement.md`](equipment-replacement.md) — Refresh-driven device swaps.
- [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md) — HR separation policy (the authoritative source).
- [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md) — Termination grounds.
- [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md) — Access control policy.
- [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md) — GitHub Enterprise repo ownership.
- [`../08-forms/equipment-handover.md`](../08-forms/equipment-handover.md) — Return section of the handover form.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Identity / Security / HRBP contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — SCIM, PIM, inactive mailbox, legal hold definitions.
