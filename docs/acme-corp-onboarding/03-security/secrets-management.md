---
document_id: ACME-SEC-015
title: Secrets Management
category: security
department: information-security
applicable_roles: [all]
owner: Abhishek Verma, IAM Engineer
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, secrets, vault, rotation, kubernetes, fictional]
---

# Secrets Management

> ACME Corp fictional onboarding library. The ACME Vault at `vault.acme.example`, the package registry at `packages.acme.example`, and the mailbox `security-oncall@acme.example` are fictional. All secrets shown are placeholders and not real.

## 1. Purpose

This document defines ACME Corp's policy for managing secrets — API keys, database passwords, signing keys, certificates, OAuth client secrets, and any other credential used by code or infrastructure. Secrets are the keys to the kingdom; a leaked secret is the most common cause of a cloud breach. This policy covers where secrets live, how they are issued, how they are rotated, and how they are recovered if lost.

## 2. Scope

This applies to:

- Every secret used by ACME code, infrastructure, CI/CD pipelines, or employees.
- Every workload that authenticates to another system — cloud providers, databases, third-party APIs, internal services.
- Every environment — development, staging, production.
- Every secret lifecycle stage: issuance, storage, rotation, revocation, destruction.

This does not apply to workforce-member passwords — those are governed by [`password-and-mfa-requirements.md`](password-and-mfa-requirements.md). Service-account passwords and workload-identity secrets are governed by this document.

## 3. Where Secrets Live — ACME Vault

ACME Vault (at `vault.acme.example`, fictional) is the canonical secret store. It is a HashiCorp Vault deployment (or equivalent) operated by the IAM Engineering team. Features:

- **Secrets at rest are encrypted** with AES-256-GCM using a Hardware Security Module (HSM)-backed master key.
- **Secrets in transit are encrypted** with TLS 1.3.
- **Access is authenticated** via Entra ID workload identity federation — no static Vault tokens.
- **Authorization is policy-driven** — per-path policy; default deny.
- **Every read, write, and list is logged** — logs shipped to the SOC SIEM.
- **Dynamic secrets** supported for databases and cloud providers — short-lived credentials, automatic rotation.
- **Recovery** via Shamir's Secret Sharing — 5 keyshares held by 5 named officers (CISO, Security Director, IAM Engineer, SOC Lead, plus a backup).

### 3.1 What Does NOT Live in ACME Vault

- Workforce-member passwords — those live in the 1Password Business vault (per [`../02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md)).
- Customer data — that lives in the approved customer-data systems (see [`customer-data-handling.md`](customer-data-handling.md)).
- Source code — that lives in `git.acme.example` (fictional).
- Backup encryption keys — those live in ACME Vault, but under a separate, higher-audited path.

## 4. Workload Identity over Static Secrets

The single most important rule in this document: **prefer workload identity over static secrets, always.**

| Mechanism | Use At ACME | Static Secret Required? |
|-----------|-------------|--------------------------|
| Azure Managed Identity | Azure-hosted workloads authenticating to Azure services | No |
| AWS IAM Role for Service Account (IRSA) | EKS workloads authenticating to AWS services | No |
| GCP Workload Identity Federation | GKE workloads authenticating to GCP services | No |
| Entra ID Workload Identity Federation | Cross-cloud and SaaS-API authentication | No |
| Kubernetes service-account token with OIDC federation | Cross-cluster auth | No |
| Sealed Secrets (Bitnami) in Kubernetes | Kubernetes-native secrets that need to be in Git (encrypted) | No (the seal key is in Vault) |
| ACME Vault dynamic database credentials | Short-lived database users | No |
| **Static API key in `.env` file committed to a repo** | **Never.** | — |
| **Static secret in CI variables** | Discouraged — only when no other option exists, with documented rotation | Yes — rotate every 30 days |

If you believe you need a static secret, ask the IAM Engineer (`Abhishek Verma`) first. The answer is almost always "use workload identity."

## 5. Secrets in Code — Forbidden

Secrets must never be committed to a repository. This rule is reinforced in [`source-code-security.md`](source-code-security.md) §7 and is repeated here because it is the most-violated rule:

- No API keys, tokens, passwords, connection strings, private keys, or certificates in source code.
- No `.env` files committed to a repository. The `.gitignore` template blocks them; do not edit the ignore out.
- No secrets in commit messages, PR descriptions, comments, or test fixtures.
- Pre-commit hooks scan for high-entropy strings and known secret patterns — they will block your commit. **Do not bypass them.**
- GitHub secret scanning runs continuously. A finding triggers an automatic page to the SOC.

If a secret is committed by accident, see [`source-code-security.md`](source-code-security.md) §7 for the response — rotation first, history rewrite only if needed.

## 6. Sealed Secrets in Kubernetes

For Kubernetes-native secrets that must live alongside the deployment manifest (and may therefore be in Git), ACME uses **Bitnami Sealed Secrets** (or equivalent):

- The deployment manifest contains a `SealedSecret` resource — a ciphertext that can only be decrypted by the cluster's controller.
- The controller's private key is stored in ACME Vault, not in the cluster's etcd.
- The sealed secret can be safely committed to Git.
- On cluster recreation, the controller fetches the private key from Vault and decrypts.

This pattern is approved for low-sensitivity secrets that change rarely (e.g., an internal service's API key for a non-critical integration). For high-sensitivity secrets (production database credentials, customer-data API keys), use ACME Vault directly.

## 7. Rotation Policy

Secrets must be rotated on a defined cadence and on event. The rotation cadence:

| Secret Type | Default Rotation Cadence | Rotation Trigger |
|-------------|--------------------------|-------------------|
| Production database credentials (static) | Every 90 days | On personnel change, on suspected compromise |
| Production database credentials (dynamic, Vault-managed) | Every 1 hour (short-lived) | Automatic |
| Cloud subscription API keys (root) | Never used; emergency only | After every emergency use |
| Cloud subscription service-principal credentials (static) | Every 90 days | On personnel change |
| Cloud subscription managed identities | Not rotated — workload identity federation | — |
| CI/CD pipeline secrets (GitHub Actions secrets) | Every 30 days | On engineer turnover |
| OAuth client secrets (third-party SaaS) | Per the vendor's policy, but no longer than 180 days | On vendor breach notification |
| TLS certificates | Every 90 days (ACME-issued) or per CA | On CA compromise |
| Code-signing keys | Every 12 months | On personnel change |
| ACME Vault root key (Shamir shares) | Every 12 months | On officer change |
| Break-glass account password | After every use | After every use |

Rotation is owned by the secret's custodian (typically the IAM Engineer or the workload owner). The GRC Analyst (`Karthik Subramanian`) audits rotation compliance quarterly.

## 8. Issuance and Access

To request a new secret or access to an existing secret:

1. Open a request via the IT access request workflow — see [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md) and [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md).
2. Specify the workload, the environment, the systems being accessed, and the lifetime needed.
3. The IAM Engineer (`Abhishek Verma`) approves — for production secrets, the Security Director (`Neha Saxena`) co-approves.
4. ACME Vault provisions the secret and a Vault policy that grants the requesting workload read access to that path only.
5. The requesting workload authenticates via workload identity federation — no human sees the secret unless explicitly approved.

Human access to a production secret requires PIM activation (see [`least-privilege-access.md`](least-privilege-access.md)) and is logged at the highest severity.

## 9. Recovery

If a secret is lost (e.g., the workload cannot read Vault, or a certificate expired without rotation):

1. **Do not** write the secret in chat, email, or a ticket. The 1Password Business vault (see [`../02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md)) is the only acceptable human-readable place.
2. Page the security on-call (see [`security-incident-reporting.md`](security-incident-reporting.md)) — secret recovery is a high-severity activity.
3. The IAM Engineer (`Abhishek Verma`) provisions a new secret, updates the workload, and rotates the old secret.
4. The GRC Analyst logs the recovery in the risk register.

For ACME Vault root-key recovery (a "rekey"), Shamir's Secret Sharing requires 3 of 5 keyshares. The 5 named officers are listed in §3.

## 10. Audit

ACME Vault logs every read, write, list, and delete to the SOC SIEM. The SOC Lead (`Fatima Sheikh`) reviews:

- **Daily:** Anomalous read patterns (e.g., a workload reading 10× the typical number of secrets in an hour).
- **Weekly:** Access by humans (any human read is reviewed).
- **Monthly:** The full audit log is archived for 13 months.
- **Quarterly:** The GRC Analyst samples 50 random secret accesses and confirms each was for a legitimate business purpose.

## 11. Responsibilities

| Role | Responsibility |
|------|----------------|
| **IAM Engineer** (`Abhishek Verma`) | Operates ACME Vault. Approves secret issuance. Runs rotation automation. |
| **Security Director** (`Neha Saxena`) | Co-approves production secret requests. Approves exceptions. |
| **SOC Lead** (`Fatima Sheikh`) | Monitors Vault audit logs. Triages secret-leak findings from GitHub. |
| **GRC Analyst** (`Karthik Subramanian`) | Audits rotation compliance. Maintains the secrets inventory. |
| **Workload Owners** | Define the rotation cadence for their secrets. Trigger rotation on personnel change. |
| **Every engineer** | Never commits secrets. Uses workload identity. Reports suspected leaks. |

## 12. Enforcement

- Pre-commit hooks block commits containing secret patterns.
- GitHub secret scanning pages the SOC on every finding.
- ACME Vault audit logs are reviewed daily for anomalies.
- Workloads that fail to authenticate to Vault for >1 hour trigger a SOC alert — investigate immediately.
- The GRC Analyst's quarterly audit reports missing-rotation findings to the CISO.

## 13. Exceptions

Exceptions (e.g., a legacy system that cannot yet use workload identity) require IAM Engineer approval, a documented static secret, a 30-day rotation, and a remediation plan. Email `security-oncall@acme.example` (fictional).

## 14. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`source-code-security.md`](source-code-security.md) — No secrets in code.
- [`password-and-mfa-requirements.md`](password-and-mfa-requirements.md) — Human passwords vs service secrets.
- [`identity-and-access-management.md`](identity-and-access-management.md) — Workload identity federation.
- [`least-privilege-access.md`](least-privilege-access.md) — PIM for human access to production secrets.
- [`data-classification.md`](data-classification.md) — Secrets are Restricted.
- [`security-incident-reporting.md`](security-incident-reporting.md) — Secret-leak response.
- [`../02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md) — Where human passwords go.
- [`../04-engineering/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md) — Pipeline secret injection.
- [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md) — Pre-commit hooks.
- [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md) — Access request form.
- [`../07-workflows/access-approval.md`](../07-workflows/access-approval.md) — Approval workflow.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — IAM Engineer, Security Director, SOC Lead contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — Vault, sealed-secrets, workload-identity definitions.
