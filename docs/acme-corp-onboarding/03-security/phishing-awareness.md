---
document_id: ACME-SEC-007
title: Phishing Awareness
category: security
department: information-security
applicable_roles: [all]
owner: Neha Saxena, Security Director
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [security, phishing, awareness, soc, report-phishing, fictional]
---

# Phishing Awareness

> ACME Corp fictional onboarding library. Email addresses (`security-incident@acme.example`, `security-oncall@acme.example`) and hostnames (`wiki.acme.example`, `hr.acme.example`) are fictional. No real phishing URLs are referenced; example URLs use `.example` and are not clickable infrastructure.

## 1. Purpose

This document describes how ACME Corp workforce members recognize phishing, how they report it, what the SOC does with reports, and how ACME trains the workforce to stay sharp. Phishing is the leading initial-access vector across the industry and the leading cause of incidents the ACME SOC triages. Awareness is a control, not a courtesy — and reporting a suspicious email in the first minute can be the difference between a non-event and a customer-impacting breach.

## 2. Scope

This applies to every ACME workforce member, contractor, and authorized third party using an ACME-issued identity or device. It covers phishing delivered via:

- Email (Outlook / Exchange Online).
- Teams messages and chat.
- Phone calls ("vishing") and SMS ("smishing").
- Fake login pages that mimic ACME's SSO at `login.microsoftonline.com` or fictional ACME hostnames.
- Social-engineering attempts via LinkedIn, GitHub issues, or in-person interactions.

## 3. How to Spot Phishing

Phishing messages share one or more of the following traits. Train yourself to spot them:

| Signal | What to Look For |
|--------|------------------|
| Urgency / fear | "Your account will be deactivated in 24 hours," "Invoice overdue — pay now." Phishers want you to act before you think. |
| Mismatched sender | Display name says "Rajan Mehta" but the address is `rajan.mehta@acme-support.example` — not `rajan.mehta@acme.example`. |
| Unexpected attachment | An invoice, a "secure document," or a `.html`/`.zip`/`.iso` file you did not expect. |
| Suspicious link | Hover over the link — the real URL does not match the display text. Look for typosquatted domains like `acme-login.example` or `micros0ft-login.example`. |
| MFA prompt out of nowhere | An Authenticator push you did not initiate. **Never approve it.** |
| Request for credentials, MFA codes, or payment | No legitimate ACME system, IT, or executive will ever ask for these. |
| Pressure to bypass policy | "Just share the file via your personal email," "Use this external link." |
| Too good / too bad to be true | A bonus, a job offer, a charity, a disaster relief — phishers exploit emotion. |

### 3.1 Common Phishing Patterns at ACME (Illustrative)

- A fake "ACME HR" email linking to `hr-acme.example` (the real host is `hr.acme.example`, fictional) — capturing the username and password on a look-alike page.
- A fake "GitHub Enterprise security alert" claiming a token leaked, with a link to `git-acme-security.example` (the real host is `git.acme.example`, fictional).
- A fake "Microsoft 365 storage quota exceeded" email with a sign-in button.
- A vishing call claiming to be from "ACME IT" asking the employee to read out an MFA code.

## 4. Reporting — the "Report Phishing" Button

ACME has deployed the **Microsoft Report Phishing add-in** in Outlook. Every workforce member should see the "Report Phishing" button in the Outlook ribbon (desktop, web, and mobile).

To report a suspicious email:

1. Select the email (do not click links or open attachments).
2. Click **Report Phishing** in the ribbon.
3. Choose "Phishing" (not "Junk" — Junk is for legitimate-but-annoying mail).
4. The email is sent to Microsoft for analysis **and** to the ACME SOC mailbox at `soc@acme.example` (fictional) for review.
5. You will receive an automated acknowledgement within 5 minutes.

For phishing delivered outside Outlook (Teams, SMS, phone calls):

- Forward the message to `security-incident@acme.example` (fictional).
- For a phone call, hang up and email `security-incident@acme.example` with the calling number and what was said.
- For an unexpected Authenticator push, **deny it** and email `security-incident@acme.example` immediately.

## 5. What the SOC Does with Your Report

The SOC (`Fatima Sheikh`, Lead) triages every report within 30 minutes during business hours and within 60 minutes out-of-hours. For each report, the SOC:

1. Inspects headers and URLs in a sandboxed environment.
2. Checks the URL against threat intelligence feeds.
3. If malicious, **triggers a tenant-wide sweep** — Exchange Online finds and purges every copy of the email across ACME inboxes.
4. If a workforce member clicked, the SOC resets their password, revokes sessions, and reviews sign-in logs for the past 7 days.
5. If credentials were entered on a fake page, the account is treated as compromised — see [`security-incident-reporting.md`](security-incident-reporting.md).
6. Sends a follow-up to the reporter with the outcome.

You will never be punished for reporting. You will never be punished for reporting something that turned out to be legitimate. The cost of a false alarm is minutes; the cost of a missed phish is a breach.

## 6. Phishing Simulations

The Security Director (`Neha Saxena`) runs a phishing simulation program — quarterly for the general workforce, monthly for high-risk roles (engineering, finance, customer support). Simulations are designed to mimic current attacker techniques.

- **Failure to spot a simulation is not punitive.** It triggers a 15-minute micro-learning module delivered the same day.
- Repeated failures trigger a conversation with the manager and a personalized training plan — never disciplinary action alone.
- Simulation results are reported in aggregate to executive leadership; individual results are not shared with managers except in the case of repeated failure.
- The SOC and Security Director can distinguish a real phish from a simulation; you do not need to verify with them before reporting.

## 7. What Not to Do

- **Do not click** links or open attachments in a suspicious email, even "to see what happens."
- **Do not reply** to the sender to ask if it is real — the attacker will say "yes."
- **Do not forward** the email to colleagues to warn them; that just spreads the phish. Report it and let the SOC handle the tenant-wide sweep.
- **Do not enter your credentials** on a page you reached via a link in an email. Always navigate to ACME systems by typing the known hostname or using a bookmark.
- **Do not approve** an MFA prompt you did not initiate. If one arrives, deny it and report it.
- **Do not share** an MFA code with anyone, ever. Not IT, not the CISO, not a colleague. ACME will never ask.

## 8. Multi-Factor Authentication Is Not a License to Be Reckless

MFA dramatically reduces the value of a stolen password, but attackers have adapted:

- **AiTM (Adversary-in-the-Middle) phishing** proxies the login page and steals the session token — MFA does not help if you approve the push.
- **MFA fatigue** sends dozens of pushes until you approve one to stop the noise. ACME mitigates with number-matching (see [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md)) and conditional access rate-limiting.
- **Consent phishing** asks you to grant an OAuth app permissions rather than enter a password — see the conditional access rules in [`identity-and-access-management.md`](identity-and-access-management.md).

MFA is mandatory; it is not sufficient. Vigilance is the second factor.

## 9. Responsibilities

| Role | Responsibility |
|------|----------------|
| **Security Director** (`Neha Saxena`) | Owns the awareness program, simulations, and training. |
| **SOC Lead** (`Fatima Sheikh`) | Triage of every phishing report within SLA. Tenant-wide sweeps. |
| **IAM Engineer** (`Abhishek Verma`) | Password reset, session revoke, conditional access tuning. |
| **People Managers** | Reinforce the no-blame reporting culture. Complete their own simulations. |
| **Every workforce member** | Spot, do not click, report. |

## 10. Enforcement

Reporting phishing is **expected**. Repeated failure to spot simulations triggers additional training — not discipline. Failing to report a real phish that leads to compromise may trigger an HR review under [`../01-hr/code-of-conduct.md`](../01-hr/code-of-conduct.md) but only in cases of gross negligence — the default stance is "no-blame reporting."

## 11. Related Documents

- [`information-security-policy.md`](information-security-policy.md) — Parent policy.
- [`password-and-mfa-requirements.md`](password-and-mfa-requirements.md) — Credential and MFA baseline.
- [`identity-and-access-management.md`](identity-and-access-management.md) — Conditional access, MFA enforcement.
- [`security-incident-reporting.md`](security-incident-reporting.md) — What happens if the phish succeeds.
- [`acceptable-use-policy.md`](acceptable-use-policy.md) — Prohibited behaviors.
- [`../02-it/microsoft-authenticator-and-mfa.md`](../02-it/microsoft-authenticator-and-mfa.md) — MFA enrollment and number-matching.
- [`../02-it/outlook-and-company-calendar-setup.md`](../02-it/outlook-and-company-calendar-setup.md) — Where the Report Phishing button lives.
- [`../07-workflows/security-training.md`](../07-workflows/security-training.md) — Training workflow.
- [`../08-forms/policy-acknowledgement.md`](../08-forms/policy-acknowledgement.md) — Acknowledgement form.
- [`../09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) — SOC Lead and Security Director contacts.
