---
document_id: ACME-IT-010
title: Corporate VPN Configuration
category: it
department: it-operations
applicable_roles: [all]
owner: Arjun Kapoor, IT Manager Hyderabad
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, vpn, remote-access, security, split-tunnel, fictional]
---

# Corporate VPN Configuration

> ACME Corp fictional onboarding library. The VPN host `vpn.acme.example` is simulated for documentation. The VPN client is a fictional ACME-branded build of OpenVPN Connect. No live credentials or certificates are demonstrated.

## 1. Purpose

Walks the new hire through downloading and installing the ACME VPN client, configuring the corporate profile, connecting, verifying connectivity, understanding split-tunnel routing rules, and troubleshooting. The corporate VPN is required for access to internal-only resources (`vault.acme.example`, `packages.acme.example`, the ITSM admin console, internal databases, and certain administrative consoles that conditional-access policies gate by source IP).

## 2. Prerequisites

- A corporate-managed, Intune-compliant device (per [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md)).
- An activated Entra ID identity and registered MFA (per [`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md)).
- Network egress (home Wi-Fi, mobile hotspot, or office Wi-Fi).
- The temporary / permanent corporate password.

## 3. Step 1 — Download the ACME VPN Client

> The client is a fictional ACME-branded build of OpenVPN Connect, packaged and signed by ACME's Endpoint Engineering team. On managed devices, it is pre-installed via Intune.

1. On a managed corporate device, verify the **"ACME VPN"** app is already in your Start menu (Windows) or Launchpad (macOS). If yes, skip to §4.
2. If the app is missing (or for reinstall), navigate to `https://packages.acme.example/vpn/` (simulated) and download the latest installer for your platform:
   - `acme-vpn-client-win-x64-2.3.0.msi`
   - `acme-vpn-client-macos-2.3.0.pkg`
3. Install with default options. On managed devices, no admin prompt appears because the Intune Software Ring policy authorizes the install.

## 4. Step 2 — Import the ACME VPN Profile

1. Launch **ACME VPN** from the Start menu / Launchpad.
2. On first launch, the client opens to the "No profile configured" screen.
3. Click **Import Profile**. The client auto-fetches the corporate profile from `https://packages.acme.example/vpn/acme-corporate.ovpn` (simulated).
4. The import dialog displays:
   - **Profile name:** ACME Corporate
   - **Remote host:** `vpn.acme.example`
   - **Port:** `1194/UDP` (primary), `443/TCP` (fallback)
   - **Auth method:** SSO via Entra ID (open the browser)
5. Click **Save**.

> The profile contains a CA certificate and client-config-directives signed by ACME's PKI. The private client certificate is **issued at sign-in time** — it is never stored on disk in a portable form. Do not attempt to export it.

## 5. Step 3 — Connect for the First Time

1. In the ACME VPN client, click **Connect**.
2. The client opens your default browser to the ACME Entra ID sign-in page.
3. Sign in with `<firstname>.<lastname>@acme.example` and complete MFA.
4. A conditional-access evaluation runs (device must be Intune-compliant — see [`microsoft-entra-id-and-sso.md`](microsoft-entra-id-and-sso.md)).
5. On success, the browser shows: "You can close this window. The ACME VPN client is connecting."
6. The client's tray icon turns **green** and displays:
   - **Assigned IP:** `10.64.<random>.<random>` (simulated RFC1918 in the `10.64.0.0/11` pool).
   - **Tunnel time:** elapsed.
   - **Bytes in/out:** counters.
7. The connection holds for 12 hours; you will be prompted to re-authenticate at expiry.

## 6. Step 4 — Verify Connectivity

Run the following checks. All hostnames are simulated.

1. **DNS resolution:**
   ```bash
   # macOS / Linux
   nslookup vault.acme.example
   # Windows
   Resolve-DnsName vault.acme.example
   ```
   Expected: resolves to a `10.64.x.x` address (the internal IP of the Vault cluster).
2. **Vault reachability:**
   ```bash
   curl -sS https://vault.acme.example/v1/sys/health
   ```
   Expected: HTTP `200` (or `429` if standby; both are fine — proves routing works).
3. **Packages registry reachability:**
   ```bash
   curl -sS -I https://packages.acme.example/
   ```
   Expected: HTTP `200` from the internal Nexus proxy.
4. **Internet egress (split-tunnel — should reach via the local network, not the VPN):**
   ```bash
   curl -sS https://ifconfig.me
   ```
   Expected: your **home / mobile public IP**, not the ACME VPN public IP. This proves split-tunnel is working.

## 7. Split-Tunnel Rules

ACME operates a split-tunnel VPN: only traffic destined for ACME-internal CIDRs and ACME-internal domains is routed over the tunnel. General internet traffic continues to use your local network egress. The benefits are faster media (Teams video, YouTube), lower ACME egress cost, and better privacy.

| Traffic class | Routed via | Example |
|---------------|------------|---------|
| ACME-internal CIDRs (`10.0.0.0/8`, `172.16.0.0/12`) | VPN | `vault.acme.example`, databases |
| ACME-internal domains (`*.acme.example`, `*.internal.acme.example`) | VPN | `wiki.acme.example` |
| Microsoft 365 (Exchange, SharePoint, Teams media) | Local egress | `outlook.office.com`, `*.sharepoint.com` |
| Public internet | Local egress | Browser traffic |
| GitHub Enterprise (`git.acme.example`) | VPN | Required (internal-only) |
| Software catalogs (`packages.acme.example`) | VPN | Internal Nexus / Artifactory |

> Microsoft 365 traffic is intentionally **excluded** from the VPN to keep media quality high. Teams media bypass is enabled at the tenant level; do not attempt to route Teams through the VPN.

## 8. Step 5 — Disconnect

1. Click the ACME VPN tray icon → **Disconnect**.
2. The tray icon turns grey.
3. Internal hostnames stop resolving within 30 seconds (DNS cache flush).

## 9. Expected Outcomes

After this document:

- The new hire can connect to the ACME VPN with MFA, get an IP from the `10.64.0.0/11` pool, and reach internal-only resources.
- The new hire understands split-tunnel and can verify it with `ifconfig.me`.
- The new hire knows the 12-hour re-auth cadence and how to renew.

## 10. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| "Profile fetch failed" during import | Corporate packages host not reachable (need VPN to fetch profile — chicken-and-egg) | Download the profile `acme-corporate.ovpn` manually from `https://packages.acme.example/vpn/` (it is publicly reachable for bootstrap) and import from disk. |
| MFA browser tab spins, never completes | Pop-up blocker or default browser mis-set | Set Edge for Business / Chrome as default; allow pop-ups from `vpn.acme.example`. |
| Connected but `vault.acme.example` does not resolve | DNS server pushed by VPN not honored | macOS: System Settings → Network → VPN → ACME → DNS; verify it shows `10.64.0.10`. Windows: `ipconfig /all` shows DNS servers. |
| `ifconfig.me` shows ACME public IP | Split-tunnel disabled / mis-route | Disconnect and reconnect; if persists, raise P3 — split-tunnel config drift. |
| Connection drops every 5 minutes | UDP blocked on local network | Switch the profile to `443/TCP` fallback (Profile → Advanced → Protocol = TCP). |
| "Device is not compliant" error at sign-in | Intune compliance stale | Open Company Portal → Sync; reboot if needed. |
| Cannot reach GitHub Enterprise (`git.acme.example`) | Not on VPN | Connect the VPN first; `git.acme.example` is not publicly routable. |

## 11. Approval Requirements

- **Standard VPN access:** included in the standard role bundle; no extra approval.
- **Privileged VPN profile (admin-level network access):** requires VP IT approval (`ramesh.khanna@acme.example`) and Just-In-Time PIM activation. See [`microsoft-entra-id-and-sso.md`](microsoft-entra-id-and-sso.md).
- **VPN from a BYOD device:** requires BYOD exception approval (see [`../03-security/byod-policy.md`](../03-security/byod-policy.md)) and full-device MDM enrollment.

## 12. Related Documents

- [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md) — Device prerequisite.
- [`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md) — MFA for VPN sign-in.
- [`microsoft-entra-id-and-sso.md`](microsoft-entra-id-and-sso.md) — Conditional access on VPN sign-in.
- [`corporate-wifi-setup.md`](corporate-wifi-setup.md) — Office network (an alternative to VPN from office).
- [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md) — Remote access policy.
- [`../03-security/byod-policy.md`](../03-security/byod-policy.md) — Personal device VPN.
- [`../08-forms/it-access-request.md`](../08-forms/it-access-request.md) — VPN request form (only for privileged profiles).
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — IT Manager / Endpoint Engineering contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — VPN, split-tunnel, MDM definitions.
