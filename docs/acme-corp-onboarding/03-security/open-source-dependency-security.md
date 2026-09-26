---
document_id: ACME-SEC-016
title: Open Source Dependency Security
category: security
department: information-security
applicable_roles: [all]
owner: Neha Saxena, Security Director
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, open-source, sbom, snyk, dependencies, supply-chain, fictional]
---

# Open Source Dependency Security

> ACME Corp fictional onboarding library. The internal package registry `packages.acme.example`, the GitHub Enterprise instance `git.acme.example`, and the mailbox `security-oncall@acme.example` are fictional. Vulnerability scanning tools (Snyk, Dependabot, Trivy) are real products; the ACME deployment is simulated.

## 1. Purpose

This document defines ACME Corp's policy for using, contributing to, and securing open-source software (OSS) dependencies. Modern software is mostly composed of OSS — for ACME Cloud, ACME Intelligence, and ACME Workspace, an estimated 70-90% of the code in production is from open-source libraries. This brings enormous velocity, and a class of supply-chain risk that this policy exists to manage. The headline risk: a vulnerability in a single transitive dependency can become a remote-code-execution in production.

## 2. Scope

This applies to:

- Every ACME repository hosted on `git.acme.example` (fictional).
- Every ACME product (ACME Cloud, ACME Intelligence, ACME Workspace) and the libraries those products depend on, transitively.
- Every ACME workforce member who adds, updates, or removes a dependency.
- Every contribution ACME makes to external open-source projects.

## 3. Approved Licenses

ACME categorizes OSS licenses by permissiveness. Only the categories below are approved for use in ACME products; licenses outside the approved list require Legal review.

| Category | Licenses | Use in ACME Products? |
|----------|----------|------------------------|
| **Permissive** | MIT, ISC, BSD-2/3-Clause, Apache-2.0, Boost Software License | Approved without review. |
| **Weak Copyleft** | MPL 2.0, LGPL 2.1/3.0, EPL 2.0 | Approved with conditions — file-level copyleft is OK; do not link statically into a product that becomes a derivative work. |
| **Strong Copyleft** | GPL 2.0/3.0, AGPL 3.0 | **Not approved** for use in ACME Cloud, ACME Intelligence, or ACME Workspace. Approved only for standalone internal tooling with Legal review. |
| **Uncategorized / custom** | Any license not in the SPDX list | Requires Legal review before use. |
| **No license** | A repo with source but no LICENSE file | **Not approved.** Default copyright applies — you cannot use the code. |

The full list is maintained by Legal in the ACME Wiki at `wiki.acme.example/legal/oss-licenses` (fictional).

## 4. SBOM Generation

A Software Bill of Materials (SBOM) is generated for every ACME product release. The SBOM:

- Is in SPDX or CycloneDX format.
- Lists every direct and transitive dependency, its version, its license, and its checksum.
- Is generated automatically by the CI pipeline (see [`../04-engineering/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md)) using `syft` or equivalent.
- Is stored alongside the release artifact.
- Is published to the internal package registry at `packages.acme.example` (fictional).
- For customer-relevant releases, is provided to enterprise customers under NDA on request.

The SBOM enables rapid response to events like Log4Shell — when a new CVE drops, the SOC queries the SBOM database to find every affected release within minutes.

## 5. Vulnerability Scanning

Every ACME repository runs vulnerability scanning on every push and nightly:

| Scanner | Scope | Cadence |
|---------|-------|---------|
| **GitHub Dependabot** | Direct dependencies in `package.json`, `requirements.txt`, `go.mod`, `pom.xml`, etc. | On push + weekly |
| **Snyk** (or equivalent) | Direct + transitive dependencies, with license policy | On push + nightly |
| **Trivy** | Container images and IaC | On every image build |
| **OSV-scanner** | Cross-check against the Open Source Vulnerabilities database | On push + nightly |
| **Internal ACME Intel feed** | Cross-references ACME-internal advisories (e.g., for ACME's own disclosed CVEs) | Continuous |

A "Critical" or "High" finding blocks the CI pipeline — the merge cannot proceed without remediation or a documented exception (see §9).

## 6. Remediation SLAs by Severity

When a vulnerability is found in a dependency, the owning team is notified. The remediation SLA is:

| Severity (CVSS v3.1) | Remediation SLA | Action Required |
|----------------------|-------------------|-----------------|
| **Critical** (9.0–10.0) | 72 hours | Patch or pin to a fixed version. If no fix exists, document a compensating control or remove the dependency. |
| **High** (7.0–8.9) | 7 days | Patch or pin. |
| **Medium** (4.0–6.9) | 30 days | Patch in the next scheduled release. |
| **Low** (0.1–3.9) | 90 days | Track; patch when convenient. |
| **Unpatched (no fix available)** | Per the GRC risk register | Document risk; consider alternative library; seek Security Director approval to retain. |

The GRC Analyst (`Karthik Subramanian`) tracks SLA compliance and reports exceptions to the CISO (`Rajan Mehta`) monthly.

## 7. Adding a New Dependency

When an engineer adds a new dependency:

1. **Search the internal package registry** at `packages.acme.example` (fictional) first — an internal mirror may already have an approved, scanned copy.
2. **Check the license** is on the approved list (§3). If not, stop and request Legal review.
3. **Check the project's health** — last commit, open-issues ratio, maintainer responsiveness, stars (a weak proxy). A dormant project is a risk.
4. **Run the scanner locally** before pushing — the CI will run it again, but running locally saves a review cycle.
5. **Document the dependency** in the project's `README.md` or `NOTICES.md` — name, version, license, purpose.
6. **Request review** from a CODEOWNER (see [`source-code-security.md`](source-code-security.md)) — the reviewer confirms license, scanner pass, and necessity.

A "convenient" library that adds 500 transitive dependencies is not a good trade. Prefer fewer, well-maintained dependencies.

## 8. Contributing to External OSS

ACME workforce members may contribute to external open-source projects, subject to:

- **Manager approval** — for any contribution made on ACME time.
- **DCO sign-off** — Developer Certificate of Origin, per the project's contribution rules.
- **No Confidential information** — contributions must not include ACME Confidential code, customer data, or internal architecture details.
- **No ACME time pressure** — do not promise ACME time to a project on ACME's behalf.
- **Security-sensitive contributions** — e.g., a vulnerability fix — must be coordinated with the project's security team and with ACME's SOC. See [`security-incident-reporting.md`](security-incident-reporting.md) for the workflow if the issue affects an ACME product.
- **CLA** — if the project requires a Contributor License Agreement, route through Legal before signing.

## 9. Exceptions

An exception is required when:

- A vulnerability cannot be patched within SLA (e.g., upstream project has not released a fix).
- A license is not on the approved list.
- A dependency must be retained despite being unmaintained.

To request an exception:

1. Open a request through `security-oncall@acme.example` (fictional).
2. The GRC Analyst (`Karthik Subramanian`) logs it in the risk register.
3. The Security Director (`Neha Saxena`) approves or denies.
4. Approved exceptions include: a compensating control, an expiry date no further than 12 months out, and a review owner.

## 10. Responsibilities

| Role | Responsibility |
|------|----------------|
| **Security Director** (`Neha Saxena`) | Owns this document. Approves exceptions. |
| **GRC Analyst** (`Karthik Subramanian`) | Maintains the SBOM database. Tracks SLA compliance. Audits exceptions. |
| **SOC Lead** (`Fatima Sheikh`) | Triage of new CVEs against the SBOM database. Coordinates emergency patching. |
| **Engineering Teams** | Patch within SLA. Generate SBOMs in CI. Review new dependencies. |
| **Engineering Managers** | Ensure their teams patch within SLA. Approve new-dependency additions. |
| **Every engineer** | Search the internal registry first. Check the license. Review dependencies in PRs. |

## 11. Enforcement

- CI fails on Critical/High vulnerabilities.
- Dependabot and Snyk findings are tracked to closure; unclosed findings beyond SLA are escalated to the engineering manager.
- The GRC Analyst publishes a monthly "OSS posture" report to engineering leadership.
- Repeated failure to patch within SLA is escalated to the CISO.

## 12. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`source-code-security.md`](source-code-security.md) — Branch protection, CI requirements.
- [`secrets-management.md`](secrets-management.md) — Secrets (not) in dependencies.
- [`data-classification.md`](data-classification.md) — SBOMs are Confidential.
- [`security-incident-reporting.md`](security-incident-reporting.md) — Supply-chain incident workflow.
- [`../04-engineering/ci-cd-overview.md`](../04-engineering/practices/ci-cd-overview.md) — Where scanners run.
- [`../04-engineering/source-code-and-repository-access.md`](../04-engineering/source-code-and-repository-access.md) — Repository hygiene.
- [`../04-engineering/git-branching-strategy.md`](../04-engineering/practices/git-branching-strategy.md) — Branch model.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Security Director, GRC Analyst, SOC Lead contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — SBOM, SCA, CVE, CVSS definitions.
