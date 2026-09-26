---
document_id: ACME-IT-006
title: Microsoft Teams Setup
category: it
department: it-operations
applicable_roles: [all]
owner: Latha Krishnamurthy, IT Helpdesk Lead
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, teams, communication, m365, fictional]
---

# Microsoft Teams Setup

> ACME Corp fictional onboarding library. The Teams tenant is `acme.onmicrosoft.com`. All channel names, team IDs, and call-routing endpoints below are simulated.

## 1. Purpose

Walks the new hire through installing the Microsoft Teams desktop client, signing in with the corporate identity, joining the onboarding team channels, configuring status and notifications, and performing a first-call test to validate audio and video. Teams is ACME's primary collaboration tool; everyone is expected to be reachable on it during working hours.

## 2. Prerequisites

- Microsoft 365 account activated per [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md).
- Microsoft Authenticator enrolled per [`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md).
- Audio output device (headset or built-in speakers) and a camera (built-in webcam or USB camera).
- A quiet environment for the first-call test.

## 3. Step 1 — Download and Install the Desktop Client

> On managed corporate devices, Teams is pre-installed via Intune; you can skip to step 2 if the app is already in your Start menu / Launchpad.

1. Navigate to `https://teams.microsoft.com/download` (real Microsoft URL; ACME tenant will accept the corporate sign-in).
2. Download the appropriate client:
   - **Windows:** `Teams_x64.msi` (new Teams client).
   - **macOS:** `Microsoft Teams.dmg`.
   - **Mobile (optional):** iOS App Store or Google Play — "Microsoft Teams".
3. Install with default options. On managed devices, no admin prompt appears because the install runs under the Intune Software Ring policy.
4. Launch the client.

## 4. Step 2 — Sign In with `@acme.example`

1. On launch, the sign-in window appears.
2. Enter your corporate user principal name: `<firstname>.<lastname>@acme.example`.
3. Enter your permanent password (set during [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md)).
4. Approve the MFA push in Microsoft Authenticator.
5. When prompted **"Stay signed in?"**, click **Yes** — this is fine on a managed corporate device. On shared/public machines, click **No**.
6. The Teams client loads. The top-right shows your avatar and the ACME logo. The left rail shows the default layout: **Activity, Chat, Teams, Calendar, Calls, Files**.

## 5. Step 3 — Join the Onboarding Team Channels

You are auto-added to the following on activation:

| Team | Channel | Purpose |
|------|---------|---------|
| ACME-New-Hires | General | Cohort-wide announcements from HR and IT. |
| ACME-New-Hires | Ask-IT | IT questions during the first 30 days. |
| ACME-New-Hires | Introduce-Yourself | Post a short intro by end of day 1. |
| ACME-All-Staff | General | Company-wide announcements. |
| `<Your-BU>` (e.g., ACME-Cloud-Engineering) | General | BU announcements. |
| `<Your-BU>` | Engineering / `<your-team>` | Your immediate team's daily channel. |

If you do not see your BU team within 60 minutes of activation, raise a P3 ticket (see [`it-support-and-troubleshooting.md`](it-support-and-troubleshooting.md)) — the group membership sync has lagged.

## 6. Step 4 — Configure Status and Working Hours

1. Click your avatar → **Settings → General**.
2. Under **Coexistence mode**, confirm "Teams Only" (this is enforced by the tenant policy).
3. Under **Working hours**, set your contracted hours (e.g., 09:30–18:30 IST) and timezone (Asia/Kolkata for Hyderabad, Asia/Kolkata for Bengaluru, Europe/London for London, America/Los_Angeles for Seattle). This drives quiet-hours suppression of notifications outside working hours.
4. Click **Save**.

## 7. Step 5 — Configure Notifications

1. **Settings → Notifications**.
2. Set the following baseline (recommended by IT and HR for new hires):
   - **Messages:** Banner + feed.
   - **Mentions:** Banner + feed.
   - **Replies:** Feed only (this avoids banner fatigue).
   - **Calls:** Banner.
   - **Meetings start:** Notification 5 minutes before.
   - **Quiet hours:** Enable, set to outside your working hours.
3. Do **not** enable the "Always on top" floating window — it interferes with screen-share during calls.
4. Save.

## 8. Step 6 — Set Your Status Message

1. Click your avatar (top-right) → **Set status message**.
2. Use the template: "Hi, I'm `<firstname>` from `<BU>` — happy to be here! Reach me via this channel or email."
3. Set **Clear status message after** to **"End of day today"** so it does not persist indefinitely.
4. Save.

## 9. Step 7 — First Call Test

> This validates audio, video, and network connectivity. Do this with your onboarding buddy.

1. Click the **Calls** icon in the left rail.
2. Click **Make a call** and enter your onboarding buddy's name (your hiring manager will have provided this on day one; if not, ask in the ACME-New-Hires / Ask-IT channel).
3. Before the call connects, click **Settings (gear) → Device settings** in the pre-call screen.
4. Make a **test call** ("Make a test call"). The bot will play back a recorded message — confirm you can hear it and that your mic picks up your voice (the bot will play it back).
5. If the test passes, proceed with the call to your buddy. If it fails, see §11 Troubleshooting.

## 10. Step 8 — Configure Calendar

1. Click **Calendar** in the left rail.
2. Confirm it shows your time zone correctly at the top.
3. The calendar mirrors your Outlook calendar (see [`outlook-and-company-calendar-setup.md`](outlook-and-company-calendar-setup.md)). You can join any meeting directly from here.
4. To schedule a Teams meeting: **New meeting → Add required attendees → Send**. A Teams join link is auto-inserted.

## 11. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| "You're not on Teams" message on launch | Account not yet Teams-enabled | Verify in M365 portal → Settings → Apps; if missing, contact `faisal.ahmed@acme.example`. |
| Test call plays back silence | Mic permissions denied / wrong mic selected | System Settings → Privacy → Microphone → enable Microsoft Teams. In Teams → Device settings, select correct mic. |
| Audio is garbled / cuts out | Network bandwidth or VPN split-tunnel mis-config | See [`corporate-vpn-configuration.md`](corporate-vpn-configuration.md) §split-tunnel — Teams media should bypass the VPN. |
| Camera shows black square | Camera in use by another app or privacy shutter closed | Close Zoom / Webex / other apps; open the shutter. |
| Channel "Introduce-Yourself" not visible | Auto-add group membership lag | Wait 30 min or sign out and back in. |
| Cannot join a meeting from the Calendar | Calendar sync lag | Use the meeting invite's "Join Microsoft Teams Meeting" link directly. |

## 12. Expected Outcomes

After this setup:

- The new hire can place and receive Teams calls with audio + video working.
- The new hire is a member of the onboarding team and their BU / team channels.
- Quiet hours are set; out-of-hours notifications are suppressed.
- The new hire has posted a brief introduction in the Introduce-Yourself channel.

## 13. Approval Requirements

- **None for the standard flow.**
- **Creating a new Team (anyone can request):** requires BU leadership approval and an expiry review date set within 12 months. See [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md).
- **External (guest) access in a Team:** requires the team owner + IT Manager approval; guests must be sponsored and expire after 90 days.

## 14. Related Documents

- [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md) — Preceding step.
- [`outlook-and-company-calendar-setup.md`](outlook-and-company-calendar-setup.md) — Calendar integration.
- [`microsoft-entra-id-and-sso.md`](microsoft-entra-id-and-sso.md) — Identity context.
- [`microsoft-authenticator-and-mfa.md`](microsoft-authenticator-and-mfa.md) — MFA for the sign-in.
- [`corporate-vpn-configuration.md`](corporate-vpn-configuration.md) — VPN split-tunnel and media bypass.
- [`it-support-and-troubleshooting.md`](it-support-and-troubleshooting.md) — How to raise a ticket.
- [`../00-company/communication-guidelines.md`](../00-company/communication-guidelines.md) — ACME communication etiquette.
- [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md) — Guest-access policy.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — IT Helpdesk contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — Teams, channel, split-tunnel definitions.
