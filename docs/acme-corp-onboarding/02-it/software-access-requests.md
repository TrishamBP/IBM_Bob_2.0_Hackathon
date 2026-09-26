---
document_id: ACME-IT-014
title: Software Access Requests
category: it
department: it-operations
applicable_roles: [all]
owner: Latha Krishnamurthy, IT Helpdesk Lead
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, access, requests, saas, scim, jira, github, fictional]
---

# Software Access Requests

> ACME Corp fictional onboarding library. All SaaS hostnames and SCIM endpoint references below are simulated for documentation. Real products (Jira, Confluence, Salesforce, Datadog, GitHub Enterprise) are referenced by their real names but the ACME integration details are fictional.

## 1. Purpose

Explains how a new hire (or any employee) requests access to ACME's portfolio of SaaS and internal business applications — Jira, Confluence, Salesforce, Datadog, GitHub Enterprise, ServiceNow-equivalent ITSM, 1Password Business vaults, and more. Covers the distinction between **auto-provisioned** and **manual** provisioning, the **approval routing** for each application, and the **review cadence** that ensures access is current.

## 2. Prerequisites

- An activated Entra ID identity (per [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md)).
- Microsoft Authenticator enrolled (per [`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md)).
- Knowledge of your role and team — used to determine which app bundles you need.
- Manager awareness — most access requests need manager approval.

## 3. The Application Portfolio

| Application | Purpose | Provisioning model | Default access |
|-------------|---------|---------------------|----------------|
| **Microsoft 365** (Exchange, SharePoint, Teams, OneDrive) | Productivity | Auto (Entra ID) | All |
| **1Password Business** | Password manager | Auto (Entra ID + SSO) | All |
| **Jira** (Atlassian Cloud, ACME tenant) | Issue tracking | SCIM from Entra ID | All engineers |
| **Confluence** (Atlassian Cloud) | Wiki | SCIM from Entra ID | All |
| **GitHub Enterprise** (`git.acme.example`) | Source control | SCIM from Entra ID | All engineers |
| **Salesforce** | CRM | Auto (role-based) | Sales, CS, Finance |
| **Datadog** | Observability | SCIM + role sync | Engineers, SREs |
| **ServiceNow-equivalent ITSM** (`helpdesk.acme.example`) | Ticketing | Auto (all employees are "requesters") | All |
| **Vault** (HashiCorp, internal `vault.acme.example`) | Secrets | Manual (PIM-gated) | Engineers with prod access |
| **Nexus / Artifactory** (`packages.acme.example`) | Package registry | Auto via Entra ID group | Engineers |
| **AWS / Azure / GCP consoles** | Cloud platforms | Manual (role-based, PIM-gated) | Engineers with prod access |
| **Figma** | Design | SCIM | Design, PM, Engineering |
| **Notion** | Knowledge management | SCIM | All |
| **Looker / Tableau** | BI | SCIM + role sync | Finance, PM, Leadership |

## 4. Auto-Provisioned vs. Manual

### 4.1 Auto-Provisioned (SCIM)

These apps receive your user object automatically when your Entra ID group membership includes the corresponding entitlement group. Examples: Jira, Confluence, GitHub Enterprise, Datadog, Figma, Notion, Nexus.

- **How you get access:** your role bundle (set at onboarding by the hiring manager per [`new-employee-it-request.md`](new-employee-it-request.md)) puts you in the right Entra ID groups.
- **Time to access:** within 60 minutes of activation.
- **How to verify:** check `https://myapps.microsoft.com` — the app tile appears.

### 4.2 Manual

These apps require a request because access is not bundled with the role. Examples: Vault (secrets), AWS / Azure / GCP prod roles, Salesforce admin, privileged ITSM roles.

- **How you get access:** file a request via [`../08-forms/software-access-request.md`](../08-forms/software-access-request.md).
- **Time to access:** 1–3 business days depending on approval chain (see §6).

## 5. Step-by-Step: Request Access

1. Complete [`../08-forms/software-access-request.md`](../08-forms/software-access-request.md) with:
   - **Application name.**
   - **Access level** (read / write / admin).
   - **Business justification** — what task you need to perform, with a link to a ticket, project, or customer.
   - **Duration** (permanent, or time-boxed for a project).
   - **Manager approval** — forward the form to your manager for an inline approval comment.
2. Submit the form via the ITSM portal at `https://helpdesk.acme.example` (simulated) or email `helpdesk@acme.example`.
3. The request routes to the **app owner** and the **Security team** for review (see §6).
4. After approval, the access is provisioned:
   - **SCIM apps:** an Entra ID group membership is added (auto-provisions within 60 minutes).
   - **Manual apps:** the app owner adds you directly.
5. You receive an email confirmation when access is granted.

## 6. Approval Routing Matrix

| Application | Approver 1 | Approver 2 (if elevated) | SLA |
|-------------|-----------|--------------------------|-----|
| Jira / Confluence (write to a project) | Project lead | — | 1 business day |
| Jira / Confluence (admin) | ITSM admin | IT Manager (`arjun.kapoor@acme.example`) | 3 business days |
| GitHub Enterprise (repo team) | Repo owner | — | 1 business day |
| GitHub Enterprise (org admin) | VP Engineering | CISO delegate | 5 business days |
| Salesforce (read) | Sales Ops | — | 1 business day |
| Salesforce (admin) | VP Sales | IT Manager | 5 business days |
| Datadog (read) | SRE lead | — | 1 business day |
| Datadog (admin) | SRE lead | IT Manager | 3 business days |
| Vault (secrets) | Team lead | Security (`rajan.mehta@acme.example`) | 2 business days |
| AWS / Azure / GCP prod roles | Team lead | Security + PIM activation required | 3 business days |
| ITSM admin | IT Manager (`arjun.kapoor@acme.example`) | VP IT (`ramesh.khanna@acme.example`) | 5 business days |

## 7. Privileged Access: Just-In-Time (PIM)

For applications with privileged roles (Vault admin, AWS prod role, ITSM admin), access is granted via **Entra ID Privileged Identity Management**:

1. You request activation in `https://myapps.microsoft.com → PIM → My roles`.
2. You specify a justification and a duration (default 4 hours, max 8).
3. If the role requires approval, the approver receives a notification.
4. On approval, your role is active for the duration; at expiry, it auto-deactivates.
5. All activations are logged for audit (see [`it-access-revocation.md`](it-access-revocation.md) §audit).

## 8. Review Cadence

| Role type | Review cadence | Reviewer |
|-----------|-----------------|----------|
| Standard SaaS access (Jira, Confluence, etc.) | Quarterly | Manager (via Access Reviews in ITSM) |
| Privileged SaaS (Vault, AWS prod) | Monthly | Security team |
| ITSM admin / Entra ID privileged | Quarterly | VP IT (`ramesh.khanna@acme.example`) |
| GitHub Enterprise org admin | Quarterly | VP Engineering + Security |
| Service accounts | Quarterly | App owner + Security |

Failure to complete an Access Review within 7 business days triggers automatic revocation of the role in question (see [`it-access-revocation.md`](it-access-revocation.md) §review-driven revocation).

## 9. Expected Outcomes

After this document:

- The new hire knows which apps are auto-provisioned vs. manual.
- The new hire can file a request via [`../08-forms/software-access-request.md`](../08-forms/software-access-request.md) with the required justification and manager approval.
- The new hire understands PIM for privileged access and the quarterly review cadence.

## 10. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| App tile missing in My Apps | Group membership sync lag | Wait 60 minutes; force-sync via Company Portal; raise P3 if persists. |
| Jira project not visible | Project-specific group missing (Jira uses project roles, not just tenant membership) | File a request for that project; project lead approves. |
| GitHub Enterprise shows "404" on `git.acme.example` | Not on VPN (`git.acme.example` is internal-only) | Connect the VPN per [`corporate-vpn-configuration.md`](corporate-vpn-configuration.md). |
| PIM activation request stuck "pending" | Approver on leave | IT Helpdesk can re-route to the approver's delegate (`helpdesk@acme.example`). |
| Access revoked after review but still needed | Review missed (manager forgot) | Re-file the request; the SLA clock restarts. |
| Salesforce login via SSO fails | User not in the correct Salesforce profile | File a request to be added to the profile; Sales Ops approves. |
| Datadog role shows "viewer" only | Default role; elevated roles need approval | File a request for the elevated role; SRE lead approves. |

## 11. Approval Requirements

- **Auto-provisioned:** no approval — driven by role bundle.
- **Manual, standard (read):** manager approval.
- **Manual, elevated (write / admin):** manager + app owner + (Security for privileged).
- **Privileged / PIM:** manager + Security + PIM activation per use.

## 12. Related Documents

- [`new-employee-it-request.md`](new-employee-it-request.md) — Role bundle that drives auto-provisioning.
- [`microsoft-entra-id-and-sso.md`](microsoft-entra-id-and-sso.md) — IdP / PIM context.
- [`approved-software-installation.md`](approved-software-installation.md) — Local software install (different from SaaS access).
- [`corporate-vpn-configuration.md`](corporate-vpn-configuration.md) — Required for `git.acme.example`.
- [`it-access-revocation.md`](it-access-revocation.md) — Review cadence and revocation.
- [`../08-forms/software-access-request.md`](../08-forms/software-access-request.md) — The request form.
- [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md) — Access control policy.
- [`../04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md) — GitHub Enterprise repo layout.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — App owners / Helpdesk contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — SCIM, PIM, SSO, IdP definitions.
