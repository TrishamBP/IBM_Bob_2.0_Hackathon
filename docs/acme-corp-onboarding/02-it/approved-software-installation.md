---
document_id: ACME-IT-013
title: Approved Software Installation
category: it
department: it-operations
applicable_roles: [all]
owner: Arjun Kapoor, IT Manager Hyderabad
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, software, installation, catalog, intune, fictional]
---

# Approved Software Installation

> ACME Corp fictional onboarding library. The endpoints `packages.acme.example` and the catalogs listed are simulated. The Microsoft Software Center / Company Portal are real Microsoft products.

## 1. Purpose

Explains how new hires install approved software on their corporate device using the **Company Portal** (Windows 11) and **Self Service** app (macOS) — both front-ends for the Intune software catalog — the process for requesting additional software via [`../08-forms/software-access-request.md`](../08-forms/software-access-request.md), the SLA for catalog additions, and what is **not** approved. No software may be installed from arbitrary sources (downloads, USB, email attachments) — the Intune catalog is the only sanctioned channel.

## 2. Prerequisites

- A corporate-managed, Intune-compliant device (per [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md)).
- An activated Entra ID identity (per [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md)).
- Network connectivity (office Wi-Fi per [`corporate-wifi-setup.md`](corporate-wifi-setup.md) or VPN per [`corporate-vpn-configuration.md`](corporate-vpn-configuration.md) for off-catalog packages).

## 3. The Approved Catalog

The ACME approved catalog is maintained by the Endpoint Engineering team and refreshed weekly. Categories include:

| Category | Examples |
|----------|----------|
| **Browsers** | Microsoft Edge for Business (default), Google Chrome, Mozilla Firefox ESR |
| **Productivity** | Microsoft 365 Apps, Microsoft Teams, Microsoft OneDrive, Notion (managed), Obsidian |
| **Developer tools** | Visual Studio Code, Git, GitHub Desktop, Docker Desktop, Node.js LTS, Python 3.x, .NET 8 SDK, JDK 21 |
| **AI / ML tooling** | PyTorch, Jupyter, Ollama (managed), Cursor (managed), GitHub Copilot client |
| **Design** | Figma desktop, Sketch, Adobe Creative Cloud (Design tier only) |
| **Communication** | Slack (limited), Zoom (limited), Webex (limited) — Microsoft Teams is primary |
| **Security tooling** | 1Password, YubiKey Authenticator, Wireshark (engineers only) |
| **Ops tooling** | k9s, kubectl, Terraform, Ansible, AWS CLI, Azure CLI, gcloud |
| **Data tooling** | DBeaver, Tableau Desktop, Power BI Desktop |
| **Remote access** | ACME VPN client, Royal TSX |

> Each catalog item has a pinned version. The catalog auto-updates within 14 days of the upstream release; you cannot pin to an older version yourself.

## 4. Step 1 — Install Software on Windows 11 (Company Portal)

1. Open **Company Portal** (Start menu → "Company Portal").
2. Sign in with `<firstname>.<lastname>@acme.example` if prompted.
3. Click **Apps** in the left rail.
4. Browse or search for the application (e.g., "Visual Studio Code").
5. Click the app → **Install**.
6. The Company Portal downloads the package from `packages.acme.example` (simulated) and installs silently.
7. When installation completes, the status changes to **"Installed"** and the app appears in your Start menu.
8. On first launch, sign in (for SSO-enabled apps like Figma, Notion, Copilot) using your corporate identity.

## 5. Step 2 — Install Software on macOS (Self Service)

1. Open **Self Service** from Launchpad (the app icon looks like a yellow briefcase).
2. Sign in with `<firstname>.<lastname>@acme.example` if prompted.
3. Browse or search for the application.
4. Click the app → **Install**.
5. Self Service downloads the package (PKG) from `packages.acme.example` (simulated) and installs with admin privileges (granted via the MDM framework — no password prompt).
6. When complete, the app appears in Launchpad.

## 6. Step 3 — Request Software Not in the Catalog

> If you need a tool that is not in the catalog, do **not** install it from a download. Use the request form.

1. Complete [`../08-forms/software-access-request.md`](../08-forms/software-access-request.md) with:
   - Application name + version + publisher + official download URL.
   - Business justification (what task it enables, why existing tools cannot do it).
   - Approval from your manager (forwarded with the form).
2. Submit the form to `helpdesk@acme.example` or via the ITSM portal at `helpdesk.acme.example`.
3. The request is reviewed by:
   - **Endpoint Engineering** for technical feasibility and packaging.
   - **Security** for malware / supply-chain risk (run against Microsoft Defender for Endpoint + Defend configuration).
   - **Procurement** for licensing (if paid).
   - **Legal** for license terms (for non-OSS).
4. If approved, the package is added to the catalog within **5 business days** (standard) or **2 business days** (expedited with VP IT approval).

## 7. What's NOT Approved (Ever)

The following are blocked at the network egress, the Defender for Endpoint level, and the AppLocker / Gatekeeper level:

- **Consumer cloud sync tools** that bypass ACME controls: Dropbox, personal Google Drive desktop client, iCloud Drive desktop client (the OS-level iCloud for photos is permitted; the Drive sync is not).
- **Unsanctioned remote-access tools:** TeamViewer, AnyDesk, Chrome Remote Desktop, ngrok, Tailscale (unmanaged). ACME provides the corporate VPN; do not tunnel around it.
- **Cracked / pirated software** of any kind — instantly a termination-level violation (see [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md)).
- **Cryptocurrency mining software.**
- **Steganography / cloaking tools** (Tor Browser, I2P, unapproved VPNs).
- **Personal password managers** (you must use 1Password Business, see [`password-manager-configuration.md`](password-manager-configuration.md)).
- **Software downloaded from non-publisher sources** (e.g., a Python wheel from a random PyPI mirror that is not the corporate proxy).
- **Browser extensions** not approved through the managed Edge / Chrome extension allow-list.

## 8. Updates

- Catalog software auto-updates within 14 days of upstream release.
- Critical security patches (e.g., a high-severity CVE in a browser or runtime) are pushed within 48 hours via Intune expedited rings.
- You cannot defer a security update beyond 7 days — after that, the device is marked non-compliant and conditional access begins blocking M365 access.

## 9. Expected Outcomes

After this document:

- The new hire can install approved software from the Company Portal / Self Service catalog.
- The new hire knows how to request additions to the catalog and the 5-business-day SLA.
- The new hire understands what is **not** approved and the consequences of installing it.

## 10. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| App in Company Portal shows "Failed" | Insufficient disk space or another install in progress | Free up disk space; wait for any in-flight installs; retry from **Settings → Sync → Retry**. |
| Self Service on macOS shows blank catalog | MDM profile stale | System Settings → Profiles → ACME Corp Management → "Sync"; reboot. |
| Requested software denied with "Supply-chain risk" | Security review flagged a vulnerable dependency | Open a dialogue with Security (`security@acme.example`) on a fork or pinned-version mitigation. |
| Install fails with "Error 1603" (Windows) | User context issue (software requires a device reboot) | Reboot the device; retry install; if persists, raise a P2 ticket. |
| App installed but cannot launch (macOS Gatekeeper block) | Notarization chain broken | Do not bypass Gatekeeper; raise P3 — Endpoint Engineering will re-sign the package. |
| Edge extension auto-disabled | Extension not on managed allow-list | File a request via [`../08-forms/software-access-request.md`](../08-forms/software-access-request.md) for the extension to be added to the allow-list. |

## 11. Approval Requirements

- **Standard catalog install:** no approval — the user can self-serve.
- **New catalog addition (standard):** Endpoint Engineering + Security + (Procurement if paid). 5-business-day SLA.
- **New catalog addition (expedited):** + VP IT (`ramesh.khanna@acme.example`). 2-business-day SLA.
- **Privileged tooling (e.g., Nessus, Burp Suite, kubectl with prod context):** + Security approval + PIM activation for the duration of use.
- **Personal / unmanaged software:** not permitted; consider a BYOD exception (see [`../03-security/byod-policy.md`](../03-security/byod-policy.md)).

## 12. Related Documents

- [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md) — Device prerequisite.
- [`software-access-requests.md`](software-access-requests.md) — SaaS access (different from local software install).
- [`password-manager-configuration.md`](password-manager-configuration.md) — Password manager as the canonical catalog tool.
- [`../08-forms/software-access-request.md`](../08-forms/software-access-request.md) — The request form.
- [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md) — Approved-use policy.
- [`../03-security/byod-policy.md`](../03-security/byod-policy.md) — Personal-device installs.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — Endpoint / Security contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — MDM, allow-list, notarization definitions.
