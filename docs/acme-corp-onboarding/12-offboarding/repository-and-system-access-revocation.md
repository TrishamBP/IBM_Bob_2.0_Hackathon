---
document_id: ACME-OFF-003
title: Repository and System Access Revocation
category: offboarding
department: information-technology
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [offboarding, access-revocation, entra-id, github, vault, vpn, scim, audit]
---

# Repository and System Access Revocation

> **FICTIONAL EXAMPLE.** ACME Corp is a fictional company. The endpoints `git.acme.example`, `vault.acme.example`, `packages.acme.example`, `wiki.acme.example`, `helpdesk.acme.example`, and `portal.acme.example` are illustrative. Microsoft Entra ID, GitHub Enterprise, Microsoft Intune, and Microsoft Purview are real infrastructure; the ACME tenant configuration and SCIM integrations are fictional.

## 1. Purpose

This document specifies the **detailed technical sequence** for revoking a departing employee's access to ACME's source-control, identity, secrets-management, network, and SaaS systems. It is the operational complement to [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) (which governs the **policy and triggers**) and to [`./employee-departure-checklist.md`](./employee-departure-checklist.md) (which tracks the workflow). It is also the operational complement to [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) (which establishes the principle that "no standing production access" is the correct starting state — and therefore no standing production access needs to be revoked at offboarding).

This document is consistent with the access policies established in [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md), [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md), and [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md). Specifically:

- All corporate identity access (Entra ID, GitHub Enterprise, ACME Vault, VPN, SaaS apps) is revoked at **end-of-business on the LWD** (T-0 EOB, 18:00 local time).
- Standing production access was **never granted** during employment (only time-bound PIM); therefore, there is no production RBAC role to revoke — PIM eligibility is preserved for audit (2 years) but rendered moot by the Entra ID account disable (§3).
- SCIM is the primary mechanism for SaaS app de-provisioning (Jira, Confluence, GitHub Enterprise, Datadog, Figma, Notion, 1Password, Salesforce).
- Audit log retention is enforced per §8 — 1 year for Entra ID group-membership changes, 2 years for PIM activations, 7 years for sign-in logs and GitHub Enterprise audit logs.

## 2. Owner and SLA

- **Process owner (joint):** IT Onboarding Specialist — Geetha Iyer (`geetha.iyer@acme.example`) — and GRC Analyst — Karthik Subramanian (`karthik.subramanian@acme.example`).
- **Escalation:** IT Manager Hyderabad — Arjun Kapoor (`arjun.kapoor@acme.example`); for compliance-related concerns, CISO — Rajan Mehta (`rajan.mehta@acme.example`).
- **SLA:** End-of-business on the LWD (T-0 EOB). SCIM de-provisioning completes within 60 minutes of the Entra ID account disable.
- **Emergency path:** For suspected insider threat or for-cause termination, the CISO delegate can trigger the emergency revocation path in [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §5 — all revocation steps execute **simultaneously within 15 minutes**.

## 3. Microsoft Entra ID Revocation (Identity Layer)

The Entra ID account disable is the keystone: every downstream system (GitHub Enterprise, Vault, SaaS apps, VPN) trusts Entra ID via SSO, so disabling the account and revoking refresh tokens cascades through the integrations. The technical steps are run by Identity Engineering per the runbook in [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §3.2.

| # | Step | Owner | Evidence |
|---|------|-------|----------|
| 1 | Set `AccountEnabled = false` on the user object | Identity Engineering | Entra ID audit log entry |
| 2 | Call `RevokeSignInSessions` — revokes all refresh tokens, app cookies, and browser SSO sessions | Identity Engineering | Entra ID audit log entry |
| 3 | Revoke all app passwords (per-app passwords generated via the user's security info) | Identity Engineering | Entra ID audit log entry |
| 4 | Revoke all FIDO2 security keys (Yubikey) registered to the user | Identity Engineering | Entra ID audit log entry |
| 5 | Remove the user from all **privileged** group memberships — Global Administrator, Security Administrator, Exchange/SharePoint Administrator, GitHub Enterprise Org Owner, Vault Administrator | Identity Engineering + IT Onboarding | Entra ID audit log entry (group-membership change) |
| 6 | **Preserve** all non-privileged group memberships for audit (do **not** delete — they are needed for audit traceability; they are ineffective because the account is disabled) | Identity Engineering | Entra ID audit log entry (group membership retained) |
| 7 | **Preserve** the user's PIM eligibility records (do not delete — needed for 2-year retention per §8) | Identity Engineering | Entra ID audit log entry (PIM eligibility retained) |
| 8 | Set the mailbox Out-of-Office message per the manager's choice (forward to a colleague, auto-reply-only, or both) — mailbox **retained** for 90 days | IT Onboarding | Exchange admin log entry |
| 9 | Set MFA methods (Authenticator, FIDO2, SMS) to **preserved** state (do not delete — needed for audit) — but they are unusable because the account is disabled | Identity Engineering | Entra ID audit log entry |

## 4. Entra ID Group Membership Removal

Group membership is the **primary access-control primitive** in Entra ID. Engineers are granted access to repositories, Vault secrets, and SaaS apps via dynamic and assigned security groups. The full list of groups a departing employee belongs to is captured in the role bundle IT Onboarding prepares at T-5 ([`./employee-departure-checklist.md`](./employee-departure-checklist.md) DEP-011).

For each group, IT Onboarding:

1. Identifies the group's owning team (per [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md) and the IT role bundle).
2. Removes the user from **privileged** groups (the §3 step 5 list) immediately at T-0 EOB.
3. **Preserves** membership in non-privileged groups for audit per §8 (retention: 1 year for group-membership-change events, 7 years for sign-in logs).
4. Logs the removal in the ITSM offboarding ticket.
5. Triggers downstream SCIM cycles (§5) — SCIM reads the group memberships and propagates the de-provisioning to SaaS apps.

Common ACME Entra ID groups (non-privileged, preserved for audit; privileged, removed):

| Group | Privileged? | Action at T-0 EOB |
|-------|-------------|-------------------|
| `acme-eng-cloud-api-ro` (read on Cloud API repos) | No | Preserved (account disabled renders ineffective) |
| `acme-eng-cloud-api-rw` (write on Cloud API repos) | No | Preserved (account disabled renders ineffective) |
| `acme-vault-secrets-cloud-prod-request` (per-secret Vault request group) | No | Preserved (account disabled renders Vault tokens moot; see §5) |
| `acme-pim-github-org-owner` (PIM-eligible GitHub Org Owner) | Yes — eligibility removed | PIM eligibility retained for 2-year audit per §8 (preserved but moot) |
| `acme-pim-vault-admin` (PIM-eligible Vault Administrator) | Yes — eligibility removed | PIM eligibility retained for 2-year audit per §8 (preserved but moot) |
| `acme-pim-global-admin` (PIM-eligible Entra ID Global Administrator) | Yes — eligibility removed | PIM eligibility retained for 2-year audit per §8 (preserved but moot) |
| `acme-salesforce-standard` (Salesforce standard user) | No | Preserved (account disabled; SCIM de-provisions Salesforce) |
| `acme-distribution-eng-cloud` (mailing list) | No | Removed at T+1 by IT Helpdesk per §7 |

## 5. GitHub Enterprise Seat Removal (via SCIM)

GitHub Enterprise seat removal happens via SCIM, the same integration that provisions seats on day 1. The flow:

1. Identity Engineering disables the Entra ID account at T-0 EOB (§3 step 1).
2. The GitHub Enterprise SCIM integration reads the Entra ID user object on its next cycle (default: every 30 minutes, or manually triggered).
3. SCIM de-provisions the user's org membership and SSO mapping in GitHub Enterprise at `git.acme.example` (fictional).
4. The user appears in the GitHub Enterprise admin console as `suspended`, not `active` — this is the equivalent of "deactivated" (per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §3.2 step 4 the user remains in the Salesforce "deactivated" list for 90 days; for GitHub Enterprise the same 90-day retention applies before hard delete).
5. **Repository ownership transfer** should already be complete by T-1 (per [`./employee-departure-checklist.md`](./employee-departure-checklist.md) DEP-007). If not, Engineering IT reassigns ownership to the team lead — every repo must have ≥2 owners per [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md).
6. **CODEOWNERS files** are reviewed by the hiring manager during KT (per [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md)) — the departing employee's handle is removed from CODEOWNERS files in any repo where they appear.

GitHub Enterprise audit log entries (push events, repo access, role changes) are retained for **7 years** per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §6.

## 6. ACME Vault Token Revocation

ACME Vault (at `vault.acme.example`, fictional) holds production and pre-production secrets. Per [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) §3 and §6, engineers never received standing access to Vault secrets — they had per-secret request access, granted on a per-need basis. At offboarding:

| # | Step | Owner | Evidence |
|---|------|-------|----------|
| 1 | Identity Engineering lists all per-secret Vault tokens issued to the user (via the Vault audit log) | Identity Engineering + GRC Analyst | Vault audit log export |
| 2 | Identity Engineering revokes every issued token — Vault tokens are immediately invalidated | Identity Engineering | Vault audit log entry (token revocation) |
| 3 | Identity Engineering removes the user from the `acme-vault-secrets-*` Entra ID groups (per-secret request groups) | Identity Engineering | Entra ID group-membership audit log entry |
| 4 | Identity Engineering removes the user from the PIM-eligible `acme-pim-vault-admin` role (per §3 step 5) | Identity Engineering | Entra ID audit log entry |
| 5 | The Vault root token is not affected (root token is held by the CISO + IAM Engineer per [`../03-security/secrets-management.md`](../03-security/secrets-management.md)) | n/a | n/a |
| 6 | The Vault audit log (vault access, token issuance, token revocation) is retained for **7 years** per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §6 | Compliance | Microsoft Purview audit pipeline |

If the departing employee held **break-glass** Vault credentials (extremely rare — only issued during incident response per [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) §8), the CISO reviews the issuance log and rotates the break-glass credential.

## 7. VPN, Wi-Fi, and SaaS App Deactivation

### 7.1 VPN client certificate revocation

The ACME corporate VPN uses SCEP-issued client certificates tied to the Entra ID device. At T-0 EOB:

1. Identity Engineering revokes the SCEP certificate for every device registered to the user (visible in Intune).
2. The VPN profile is removed from the device (via Intune, simultaneous with the §6 device wipe in [`./equipment-return.md`](./equipment-return.md)).
3. VPN session logs are retained for **7 years** per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §6.

### 7.2 Wi-Fi RADIUS auth revocation

Corporate Wi-Fi (802.1X) uses RADIUS auth backed by the same Entra ID device certificate:

1. Identity Engineering removes the device from the Wi-Fi RADIUS allow-list.
2. The Wi-Fi profile is removed from the device (via Intune).
3. Wi-Fi RADIUS auth logs are retained for **1 year** per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §6.

### 7.3 SaaS app deactivation via SCIM

SCIM is the primary mechanism for SaaS app de-provisioning. Within 60 minutes of the Entra ID account disable, the SCIM cycle de-provisions the user in:

| App | Endpoint (fictional) | Action | Retention |
|-----|----------------------|--------|-----------|
| Jira | `jira.acme.example` (via Atlassian Access) | Deactivate user; preserve issue history | 7 years (Atlassian audit log) |
| Confluence | `wiki.acme.example` (via Atlassian Access) | Deactivate user; preserve page edits | 7 years (Atlassian audit log) |
| GitHub Enterprise | `git.acme.example` | Suspend user; preserve commit history | 7 years (GitHub audit log) |
| Datadog | `app.datadoghq.com` (via SCIM) | Deactivate user; preserve dashboard ownership (transferred in DEP-007) | Per Datadog retention |
| Figma | `figma.com` (via SCIM) | Deactivate user; preserve design files (transferred in DEP-007) | Per Figma retention |
| Notion | `notion.so` (via SCIM) | Deactivate user; preserve page edits (transferred in DEP-007) | Per Notion retention |
| 1Password | `1password.com` (via SCIM) | Deactivate user; vault access removed; vault ownership already transferred in DEP-007 | 7 years (1Password audit log) |
| Salesforce | `acme.salesforce.com` (via SCIM) | Deactivate user; user remains in Salesforce "deactivated" list for 90 days | Per Salesforce retention |

If a SCIM de-provision fails for any app (token expired, app-side error), Identity Engineering re-runs the SCIM cycle manually and uses the app's admin console as a backstop — see [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §9 (Troubleshooting).

### 7.4 Distribution lists and Teams chats

At T+1 business day, IT Helpdesk removes the user from:

- All mailing lists and distribution groups (DLs) in Exchange Online.
- All Teams chats and channel memberships (the Teams client roster refreshes within 24 hours; see [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §9 (Troubleshooting)).
- All Microsoft 365 Group memberships (SharePoint site members, Teams team members, Planner plan members).

## 8. Audit Log Retention

Audit log retention is the closing control of the access-revocation process. It establishes that even after access is revoked, the records of what the user did during employment and what was revoked at separation are preserved for compliance and investigations.

| Log source | Retention | Owner | Trigger |
|------------|-----------|-------|---------|
| Entra ID sign-in logs | **7 years** | Identity Engineering | Per-user sign-in events |
| Entra ID audit logs — group membership changes | **1 year** | Identity Engineering | §3 step 5 + §4 group removals |
| Entra ID audit logs — PIM activations | **2 years** | Identity Engineering | §3 step 7 PIM eligibility retention; per-user PIM activation history |
| Entra ID audit logs — role activations (privileged) | 7 years | Identity Engineering | Per-role activation events |
| Intune device actions (wipe, retire) | 7 years | Endpoint Engineering | [`./equipment-return.md`](./equipment-return.md) §6.3 wipe verification |
| Microsoft Purview audit log (M365 data access) | 7 years | Compliance | Per-user M365 data access events |
| Defender for Endpoint telemetry | 6 months hot, 7 years cold | Security | Per-device telemetry |
| 1Password audit log (vault access, item access) | 7 years | Identity Engineering | §6 Vault token revocation |
| GitHub Enterprise audit log (repo access, push events) | 7 years | Engineering IT | §5 GitHub seat removal |
| ITSM ticket history | 7 years | IT Helpdesk | Offboarding ticket `OFFBD-YYYY-NNNNNN` |
| Wi-Fi RADIUS auth logs | **1 year** | Network Engineering | §7.2 Wi-Fi revocation |
| VPN session logs | 7 years | Network Engineering | §7.1 VPN revocation |
| Vault audit log (vault access, token issuance/revocation) | 7 years | Compliance | §6 Vault token revocation |

All logs are immutable and stored in the Microsoft Purview audit-log retention pipeline with **Legal Hold** where applicable (e.g., during litigation or a security incident investigation).

The 1-year retention for Entra ID group-membership-change events and the 2-year retention for PIM activations are **shorter** than the 7-year retention for sign-in logs because they are operational logs (used by GRC for quarterly access reviews and incident triage), not compliance logs. The 7-year retention is reserved for logs that are likely to be subpoenaed or audited by external regulators.

## 9. Production Access Note (No Standing Access to Revoke)

Per [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md) §6, ACME engineers never received standing production access. Therefore, at offboarding:

- **No** standing `Contributor` or `Owner` Azure role assignments exist to revoke (the user never had them).
- **No** standing AWS IAM role assignments exist to revoke (the user never had them).
- **No** standing GCP project role bindings exist to revoke (the user never had them).
- **No** standing database-administrator grants exist to revoke (the user never had them).
- **No** standing Kubernetes cluster-admin bindings exist to revoke (the user never had them).
- **No** standing production Vault secret access exists to revoke (per-secret tokens were already time-bound; §6 revokes any in-flight tokens).
- PIM eligibility (if any) is **preserved** for 2-year audit retention per §8 but is rendered moot by the §3 Entra ID account disable.

This is the operational inverse of the onboarding default-deny principle (§3 of [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md)): "no access" is the correct starting state, and "no standing access to revoke" is the correct ending state.

## 10. Status Tracking

All revocation subtasks are tracked in the ITSM offboarding ticket (`OFFBD-YYYY-NNNNNN`) and mirrored to the HR Hub offboarding record. Allowed statuses: `NOT_STARTED`, `IN_PROGRESS`, `BLOCKED`, `COMPLETED`. The subtasks (mapped to [`./employee-departure-checklist.md`](./employee-departure-checklist.md) DEP-* task IDs):

| Sub-task | Mapped DEP ID | Default status |
|----------|---------------|----------------|
| Entra ID account disable + token revocation | DEP-022 | NOT_STARTED |
| Entra ID privileged group removal | DEP-022 | NOT_STARTED |
| GitHub Enterprise SCIM de-provision | DEP-023 / DEP-025 | NOT_STARTED |
| ACME Vault token revocation | DEP-024 | NOT_STARTED |
| VPN cert revocation | DEP-024 | NOT_STARTED |
| Wi-Fi RADIUS auth revocation | DEP-024 | NOT_STARTED |
| SaaS app SCIM de-provision (Jira, Confluence, Datadog, Figma, Notion, 1Password, Salesforce) | DEP-023 | NOT_STARTED |
| Mailing lists / DLs / Teams chats removal | DEP-028 | NOT_STARTED |
| Audit logs preserved per §8 | DEP-034 | NOT_STARTED |
| IT certifies no corporate access remains | DEP-026 | NOT_STARTED |

## 11. RACI Matrix

| Activity | R | A | C | I |
|----------|---|---|---|---|
| Trigger revocation (HRIS state change) | HRBP | HR Operations | IT Onboarding | VP HR |
| Entra ID account disable + token revocation | Identity Engineering | IT Manager Hyderabad | GRC Analyst | CISO |
| Privileged group removal | Identity Engineering | IT Manager Hyderabad | GRC Analyst | CISO |
| GitHub Enterprise SCIM de-provision | Engineering IT | IT Manager Hyderabad | GRC Analyst | VP Engineering |
| Vault token revocation | Identity Engineering | IT Manager Hyderabad | GRC Analyst | CISO |
| VPN cert revocation | Identity Engineering + Network Engineering | IT Manager Hyderabad | GRC Analyst | CISO |
| Wi-Fi RADIUS revocation | Network Engineering | IT Manager Hyderabad | GRC Analyst | CISO |
| SaaS app SCIM de-provision | Identity Engineering | IT Manager Hyderabad | IT Onboarding | CISO |
| Mailing list / DL / Teams removal | IT Helpdesk | IT Manager Hyderabad | HRBP | VP IT |
| Audit log retention verification | GRC Analyst | Compliance | Identity Engineering | CISO |
| IT certification of revocation complete | IT Onboarding | IT Manager Hyderabad | GRC Analyst + HRBP | VP IT |

Legend: R = Responsible, A = Accountable, C = Consulted, I = Informed.

## 12. Troubleshooting

| Symptom | Likely cause | Resolution |
|---------|--------------|------------|
| SCIM de-provision failed for one SaaS app | SCIM token expired or app-side error | Identity Engineering re-runs SCIM cycle; admin console of the app used as backstop per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §9 |
| Disabled user still appears in Teams chats | Teams client cache lag | Teams client refreshes within 24 hours; force-refresh via Settings → Clear cache per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §9 |
| Vault token still active after §6 revocation | Vault audit log replication delay | Identity Engineering re-runs the revocation command; if persists, the Vault root token holder (IAM Engineer) forcefully invalidates the user's identity binding |
| GitHub Enterprise seat still active after SCIM cycle | SSO mapping cached on GitHub side | Engineering IT manually suspends the user in the GitHub Enterprise admin console; SSO session cookies expire within 1 hour |
| User's PIM eligibility still appears as "active" after T-0 | PIM eligibility is intentionally retained for audit per §8 | No action needed — the Entra ID account is disabled, so the PIM eligibility is moot; the audit log entry for §3 step 7 records the retention |
| User's MFA methods still listed under their security info | MFA methods are intentionally preserved per §3 step 9 | No action needed — they are unusable because the account is disabled; preservation is for audit |
| Departing employee's repo is orphaned (no owner) | Repo owner was the only owner and was off-boarded | Engineering IT reassigns ownership to the team lead per [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md); every repo must have ≥2 owners |
| Emergency revocation performed without VP sign-off | Process violation | Post-incident review; the action itself stands (security first), but the workflow is corrected for next time per [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md) §10 |

## 13. Expected Outcomes

After this document:

- IT Onboarding and Identity Engineering have the runbook for the standard and emergency revocation paths.
- The GRC Analyst knows which audit logs to retain and for how long.
- Engineering IT knows the GitHub Enterprise SCIM de-provisioning flow and the repo-ownership reassignment fallback.
- The CISO office has the audit trail of what was revoked, when, and by whom.

## 14. Related Documents

- HR: [`../01-hr/employee-separation-policy.md`](../01-hr/employee-separation-policy.md)
- IT: [`../02-it/it-access-revocation.md`](../02-it/it-access-revocation.md), [`../02-it/microsoft-entra-id-and-sso.md`](../02-it/microsoft-entra-id-and-sso.md), [`../02-it/corporate-vpn-configuration.md`](../02-it/corporate-vpn-configuration.md), [`../02-it/corporate-wifi-setup.md`](../02-it/corporate-wifi-setup.md), [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md)
- Security: [`../03-security/least-privilege-access.md`](../03-security/least-privilege-access.md), [`../03-security/identity-and-access-management.md`](../03-security/identity-and-access-management.md), [`../03-security/secrets-management.md`](../03-security/secrets-management.md), [`../03-security/source-code-security.md`](../03-security/source-code-security.md), [`../03-security/security-incident-reporting.md`](../03-security/security-incident-reporting.md)
- Engineering: [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md), [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md)
- Workflows: [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md)
- Forms: [`../08-forms/access-review.md`](../08-forms/access-review.md)
- Contacts: [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- Glossary: [`../metadata/glossary.md`](../metadata/glossary.md)
