---
document_id: ACME-IT-007
title: Outlook and Company Calendar Setup
category: it
department: it-operations
applicable_roles: [all]
owner: Latha Krishnamurthy, IT Helpdesk Lead
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [it, outlook, calendar, m365, signature, fictional]
---

# Outlook and Company Calendar Setup

> ACME Corp fictional onboarding library. The Exchange Online tenant is hosted under `acme.onmicrosoft.com`. All room mailbox names and distribution list aliases below are simulated.

## 1. Purpose

Walks the new hire through configuring the Outlook desktop client, setting up a corporate email signature, configuring calendar permissions, booking a meeting room, setting working hours, and configuring out-of-office (OOO). Outlook is the canonical mail + calendar client at ACME; everyone is expected to read corporate mail on a daily cadence and to keep their calendar accurate.

## 2. Prerequisites

- Microsoft 365 account activated per [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md).
- Microsoft Teams set up per [`microsoft-teams-setup.md`](microsoft-teams-setup.md) (calendar is shared).
- Microsoft Outlook desktop client installed via Intune (verify under Start menu / Launchpad).

## 3. Step 1 — Configure the Outlook Desktop Profile

1. Launch **Microsoft Outlook**.
2. On first launch, the **"Let's get you set up"** dialog appears. Enter your corporate user principal name: `<firstname>.<lastname>@acme.example`.
3. Click **Connect**. Outlook auto-discovers the ACME Exchange Online endpoint (`outlook.office.com` — real Microsoft infrastructure, ACME tenant responds for the `acme.onmicrosoft.com` directory).
4. The Microsoft 365 sign-in page opens in a browser tab. Enter your permanent password and approve the MFA push.
5. Outlook returns and shows: "Your account was successfully connected."
6. The mailbox syncs. Within 5–10 minutes, your inbox will populate.

## 4. Step 2 — Set Your Corporate Email Signature

> ACME requires every external email to carry the standard corporate signature. Marketing-validated templates are pushed to your Outlook via Intune; the steps below customize the personal fields.

1. In Outlook: **File → Options → Mail → Signatures**.
2. The default ACME template is pre-populated; edit the placeholders:
   - `[Full Name]` → your full legal name as in the HRIS.
   - `[Role / Title]` → your role title (e.g., "Software Engineer II").
   - `[BU]` → your business unit (e.g., "ACME Cloud Engineering").
   - `[Phone]` → your desk / mobile extension (use the format `+91-40-0000-0000 ext. XXXX` for Hyderabad; `+1-206-555-0000 ext. XXXX` for Seattle; `+44-20-0000-0000` for London).
   - `[Office]` → your office city.
3. Set this signature as the default for **New messages** and **Replies/forwards**.
4. Save. Test by composing a new email to yourself.

> The signature block must not contain external advertising, animated GIFs, or unapproved logos. The legal disclaimer at the bottom is mandatory and tamper-proof — do not attempt to remove it.

## 5. Step 3 — Set Working Hours

1. In Outlook: **File → Options → Calendar**.
2. Under **Work time**, set:
   - **Start time:** 09:30 (or your contracted hours).
   - **End time:** 18:30.
   - **Work week:** Mon–Fri.
3. Set the **time zone**:
   - Hyderabad / Bengaluru: `(UTC+05:30) Chennai, Kolkata, Mumbai, New Delhi`.
   - London: `(UTC+00:00) Dublin, Edinburgh, Lisbon, London`.
   - Seattle: `(UTC-08:00) Pacific Time (US & Canada)`.
4. Save. The calendar grid now highlights your working hours, and Outlook will warn others when they try to schedule outside them.

## 6. Step 4 — Set Calendar Permissions

> ACME uses the "Limited Details" default for colleagues — others can see your subject lines and busy/free times, but not the body of your meetings.

1. In Outlook calendar view: right-click your calendar → **Properties → Permissions**.
2. The **Default** entry is set to **"Limited Details"** (this is the ACME baseline). Do not change this to "Full" — that would expose meeting bodies to everyone in the tenant.
3. To grant a colleague more access (e.g., "Reviewer" to see full details, or "Editor" to manage your calendar), click **Add**, select the colleague's name, choose the role, and save. Common patterns:
   - **Reviewer** to your EA / admin assistant.
   - **Editor** to your manager if they need to book on your behalf.
4. For delegation (full inbox + calendar), raise a ticket per [`software-access-requests.md`](software-access-requests.md) — the ACME baseline is "no delegates by default."

## 7. Step 5 — Book a Meeting Room

> ACME rooms are Exchange room mailboxes named by office + capacity (e.g., `HY-Conf-Aquila-12@acme.example` is a 12-seat room in Hyderabad named "Aquila").

1. In the calendar, **New Meeting**.
2. Click **Rooms** in the top ribbon. The Room Finder pane appears on the right.
3. Filter by **Building**:
   - **Hyderabad:** HY-Block-A, HY-Block-B, HY-Block-C.
   - **Bengaluru:** BL-Tower-B.
   - **London:** LN-Floor-4, LN-Floor-5.
   - **Seattle:** SE-Building-2.
4. Pick a room and add it to the meeting. Outlook shows the room's availability alongside invitees'.
5. Send the invite. The room auto-accepts if free; declines if double-booked.
6. For recurring bookings, ensure you set an **end date** within 90 days — ACME's policy forbids indefinite recurring room holds (see [`../00-company/communication-guidelines.md`](../00-company/communication-guidelines.md)).

## 8. Step 6 — Configure Out-of-Office

1. In Outlook: **File → Info → Automatic Replies**.
2. Toggle **"Send automatic replies"**.
3. Set the **start / end time** (use your last working day morning → first return morning).
4. Compose **Inside ACME** reply (template):
   > Hi, I'm out of office from `<date>` through `<date>` with limited email access. For urgent matters, contact `<onboarding-buddy>` (`<buddy-email>`) or the IT Helpdesk (`helpdesk@acme.example`). — `<firstname>`
5. Compose **Outside ACME** reply (template):
   > Hello, I'm out of the office through `<date>`. For urgent assistance, please contact `helpdesk@acme.example` or call +91-40-0000-0000. Best, `<firstname>`
6. Save. Outlook sends the reply once per sender for the duration.

## 9. Step 7 — Connect to Shared Mailboxes (If Applicable)

> If your role includes a shared mailbox (e.g., `support@acme.example`, `sales-apac@acme.example`), IT will have provisioned it. The steps below link it to your Outlook.

1. In Outlook: **File → Info → Account Settings → Account Settings**.
2. Select your account → **Change** → **More Settings → Advanced → Add**.
3. Enter the shared mailbox alias (e.g., `support@acme.example`).
4. OK → Close. The shared mailbox appears in your folder list under your primary mailbox.

If the alias is not auto-discovered, raise a P3 ticket — IT may need to grant you "Full Access" on the shared mailbox object in Exchange Online.

## 10. Expected Outcomes

After this setup:

- The new hire's Outlook is signed in, inbox synced, and signature set per ACME template.
- Working hours and time zone are correct.
- Default calendar permission is "Limited Details."
- The new hire can book a meeting room using the Room Finder.
- An out-of-office rule is configured (or ready to be toggled when they next go on leave).
- Any shared mailbox the role is entitled to appears in the folder list.

## 11. Troubleshooting

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| "Cannot connect to Exchange" on first launch | Tenant sign-in interrupted or MFA push missed | Cancel and re-launch; re-do the sign-in flow. |
| Signature template missing | Intune Office policy sync lag | Wait 30 minutes or trigger Company Portal → Sync; if still missing, raise a P3 ticket. |
| Room Finder shows no rooms | Building filter mis-applied | Clear building filter, search by room name; or use **Scheduling Assistant** instead. |
| Shared mailbox does not appear | "Full Access" not yet granted | Raise a P3 ticket — IT Helpdesk will grant and re-sync. |
| Calendar shows wrong time zone | Outlook regional settings mismatched | File → Options → Calendar → Time zone; correct manually. |
| Out-of-office replies not sent | Rule disabled or start time in past | Re-open Automatic Replies, verify times, re-enable. |
| Calendar invite from external source shows "Tentative" auto | Outlook default for external invites | This is the ACME baseline; leave as-is — do not auto-accept. |

## 12. Approval Requirements

- **Default signature template:** owned by Marketing + Legal; changes require their sign-off.
- **Shared mailbox access:** requires manager + IT Helpdesk approval; auto-provisioned for known role bundles (e.g., Support tier gets `support@acme.example`).
- **Delegate / Editor access to your calendar:** personal choice; no IT approval, but reviewers must be corporate identities (no guests).
- **Send-As permission on a shared mailbox:** requires IT Manager approval (`arjun.kapoor@acme.example`).

## 13. Related Documents

- [`microsoft-365-account-activation.md`](microsoft-365-account-activation.md) — Preceding step.
- [`microsoft-teams-setup.md`](microsoft-teams-setup.md) — Calendar is shared between Teams and Outlook.
- [`microsoft-entra-id-and-sso.md`](microsoft-entra-id-and-sso.md) — Identity context.
- [`../00-company/communication-guidelines.md`](../00-company/communication-guidelines.md) — Email etiquette.
- [`../03-security/information-security-policy.md`](../03-security/information-security-policy.md) — Mail handling policy.
- [`software-access-requests.md`](software-access-requests.md) — To request a shared mailbox.
- [`it-support-and-troubleshooting.md`](it-support-and-troubleshooting.md) — Tickets.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — IT Helpdesk contacts.
- [`../metadata/glossary.md`](../metadata/glossary.md) — Room mailbox, OOO, delegate definitions.
