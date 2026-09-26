---
document_id: ACME-IT-011
title: Corporate Wi-Fi Setup
category: it
department: it-operations
applicable_roles: [all]
owner: Arjun Kapoor, IT Manager Hyderabad
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, wifi, 802.1x, networking, intune, fictional]
---

# Corporate Wi-Fi Setup

> ACME Corp fictional onboarding library. The SSIDs `ACME-Corporate` and `ACME-Guest` are simulated for documentation. No live credentials or certificates are demonstrated.

## 1. Purpose

Walks the new hire through connecting to the corporate Wi-Fi (`ACME-Corporate`, WPA2-Enterprise with 802.1X EAP-TLS using a per-device certificate issued by Intune), configuring the guest SSID (`ACME-Guest`) for visitors, and understanding the eduroam-style off-boarding flow for devices leaving the fleet. From any ACME office, `ACME-Corporate` is the primary network; the VPN (see [`corporate-vpn-configuration.md`](corporate-vpn-configuration.md)) is only needed for remote work.

## 2. Prerequisites

- A corporate-managed, Intune-compliant device (per [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md)).
- An activated Entra ID identity (per [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md)).
- An SCEP-issued client certificate (pushed automatically via Intune Wi-Fi profile — see §4).
- Physical presence in an ACME office (Hyderabad, Bengaluru, London, or Seattle).

## 3. Step 1 — Confirm the Wi-Fi Profile is Pushed

1. On your corporate device, open the **Company Portal** app.
2. Navigate to **Settings → Account → Sync**. Click **Sync**.
3. Wait 5–10 minutes. The Intune Wi-Fi profile `ACME-Corporate-EAP-TLS` installs silently.
4. Verify:
   - **Windows 11:** Settings → Network & internet → Wi-Fi → "Manage known networks". You should see **`ACME-Corporate`** listed, marked as **"Managed by your organization"**.
   - **macOS:** System Settings → Wi-Fi. The `ACME-Corporate` network appears in the list with a small "managed" badge.
5. The SCEP client certificate is installed in the device's certificate store (Windows: `Certmgr` → Personal; macOS: Keychain → "Certificates").

## 4. Step 2 — Connect to `ACME-Corporate`

1. Click the Wi-Fi icon in the system tray / menu bar.
2. Select **`ACME-Corporate`** from the list.
3. On the connection dialog:
   - **Authentication method:** EAP-TLS (auto-selected by the managed profile).
   - **Client certificate:** the SCEP-issued `ACME-Device-Cert` (auto-selected).
   - **Trust the server certificate:** verify the server cert fingerprint matches the one published on `https://wiki.acme.example/it/wifi` (simulated). This is a defense against rogue-AP attacks.
4. Click **Connect**.
5. The device authenticates via 802.1X (EAP-TLS) and is granted a `10.40.x.x` IP via DHCP.

> You do **not** enter a username or password — the per-device certificate is your credential. There is no shared Wi-Fi password; do not attempt to share one.

## 5. Step 3 — Verify Connectivity

1. **Internal resources:** open a browser to `https://wiki.acme.example/` (simulated internal). Should load without VPN.
2. **Internet egress:** open `https://ifconfig.me` — should show an ACME office public IP (Hyderabad: `203.0.113.10`–`203.0.113.20` [simulated]; Bengaluru: `203.0.113.30`–`203.0.113.40`; London: `203.0.113.50`–`203.0.113.60`; Seattle: `203.0.113.70`–`203.0.113.80`).
3. **DNS resolution:** `nslookup vault.acme.example` should resolve to `10.64.x.x`.

## 6. Step 4 — The Guest SSID (`ACME-Guest`)

> For visitors, contractors without a managed device, and personal phones. Internet-only; no internal access.

1. Select `ACME-Guest` from the Wi-Fi list.
2. A captive portal opens: enter your name + a sponsor email (an `@acme.example` address). The sponsor receives a one-time approval link.
3. The sponsor clicks "Approve" — the guest is granted 24 hours of internet access (rate-limited to 50 Mbps).
4. Guests must be re-sponsored every 24 hours. Do not approve a guest you do not personally know.

## 7. Step 5 — Off-Boarding / Device Leaving the Fleet

> ACME operates an eduroam-style flow: when a device leaves the fleet (separation, return-to-IT, or transfer), the certificate on the device is revoked and the device is dropped from the Wi-Fi RADIUS allow-list.

1. When a device is off-boarded (see [`it-access-revocation.md`](it-access-revocation.md)):
   - The Intune Wi-Fi profile is removed at the next check-in.
   - The SCEP client certificate is revoked in the CA's CRL.
   - The RADIUS reject-list is updated.
2. The device will no longer authenticate to `ACME-Corporate`, even if the profile is still cached locally — the cert is invalid.
3. For a clean off-boarding, IT performs an `Intune sync` then `Retire` action, which forces an immediate profile + cert removal.

## 8. Expected Outcomes

After this document:

- The new hire's corporate device connects to `ACME-Corporate` via EAP-TLS, no shared password.
- The device gets an IP in the office subnet and can reach internal resources without VPN.
- The new hire can sponsor a guest on `ACME-Guest`.
- The new hire understands devices leaving the fleet lose Wi-Fi access automatically.

## 9. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| `ACME-Corporate` does not appear in Wi-Fi list | Intune Wi-Fi profile not yet synced | Open Company Portal → Sync; wait 10 minutes; if persists, raise a P3 ticket. |
| "Cannot connect" / "Authentication failed" | SCEP cert not issued or expired | Check Certificates store; if missing, force-sync via Company Portal. If expired, raise P3. |
| Server cert fingerprint mismatch | Rogue AP / spoofing attempt | **Disconnect immediately**; report to `security@acme.example` and the IT Helpdesk. |
| Slowness / packet loss on Wi-Fi | Channel congestion or wrong AP model | Check signal strength; if RSSI < -70 dBm, move to a closer AP; report dead zones via [`it-support-and-troubleshooting.md`](it-support-and-troubleshooting.md). |
| Guest captive portal does not appear | DNS hijack or captive-portal detection off | Open `http://captive.acme.example/` manually; if that fails, the guest VLAN may be down — contact IT. |
| macOS prompts to "always allow" the cert | Keychain access prompt — normal | Click "Always Allow" with admin (the device admin is the MDM framework). |
| After off-boarding, device still shows the profile | Sync lag | The profile is removed at next check-in; force a check-in or power-cycle. |

## 10. Approval Requirements

- **Standard `ACME-Corporate` access:** no extra approval — granted by the Intune Wi-Fi profile to every managed device.
- **Guest sponsorship on `ACME-Guest`:** open to every employee, but each guest must be re-sponsored every 24 hours.
- **Privileged network access (e.g., lab VLAN):** requires IT Manager approval (`arjun.kapoor@acme.example`) and a separate SCEP profile.
- **Adding a non-managed device to `ACME-Corporate`:** not permitted. BYOD uses BYOD Wi-Fi profile + MDM enrollment (see [`../03-security/byod-policy.md`](../03-security/byod-policy.md)).

## 11. Related Documents

- [`windows-11-and-macos-workstation-setup.md`](windows-11-and-macos-workstation-setup.md) — Device prerequisite.
- [`corporate-vpn-configuration.md`](corporate-vpn-configuration.md) — Remote alternative.
- [`it-access-revocation.md`](it-access-revocation.md) — Off-boarding flow.
- [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md) — Network access policy.
- [`../03-security/byod-policy.md`](../03-security/byod-policy.md) — Personal device Wi-Fi.
- [`../00-company/office-locations-and-working-arrangements.md`](../00-company/office-locations-and-working-arrangements.md) — Office locations.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — IT Manager / Endpoint contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — 802.1X, EAP-TLS, SCEP, RADIUS definitions.
