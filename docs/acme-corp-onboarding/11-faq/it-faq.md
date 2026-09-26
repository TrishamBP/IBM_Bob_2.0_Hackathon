---
document_id: ACME-FAQ-002
title: IT Frequently Asked Questions
category: faq
department: all
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [faq, it, laptop, vpn, mfa, software, byod]
---

# IT Frequently Asked Questions

This FAQ covers the most common IT questions at ACME Corp — laptops, software, MFA, VPN, Wi-Fi, password management, and access requests. The IT Helpdesk (helpdesk@acme.example) is staffed from 07:00 to 21:00 IST on weekdays; raise a ticket on helpdesk.acme.example for anything you cannot self-serve. For the canonical policies referenced below, see the [IT documents](../02-it/) and [security policies](../03-security/).

### Q: How do I get a laptop?
Your laptop is provisioned as part of the [new employee IT request](../02-it/new-employee-it-request.md) which your manager files at least five business days before your start date. The standard build for engineers is a 16 GB MacBook Pro or a 32 GB ThinkPad running Windows 11, depending on your role and team; non-engineering roles receive a 16 GB ThinkPad by default. See [../02-it/laptop-and-workstation-allocation.md](../02-it/laptop-and-workstation-allocation.md) for the full hardware matrix and the upgrade-request process.

### Q: How do I install software not in the catalog?
Software not available in the approved catalog on packages.acme.example requires an [approved software installation](../02-it/approved-software-installation.md) request, which routes to your manager and the IT security reviewer for sign-off. Approval typically takes two to three business days and the package is then pushed to your device through Microsoft Intune — you will not have local admin rights to install it manually. Repeated unapproved installs can flag your device for compliance review, so always check the catalog first.

### Q: My laptop was lost — what do I do?
Report the loss immediately through the [lost or stolen device reporting](../02-it/lost-or-stolen-device-reporting.md) process on helpdesk.acme.example, or by calling the IT Helpdesk at +91-40-0000-0000 if outside business hours. IT will trigger a remote lock and, if needed, a remote wipe through Microsoft Intune within 30 minutes, and the security team will review whether any data exposure occurred. Your manager will also be notified so that access tokens can be rotated; you can request a replacement via [../02-it/equipment-replacement.md](../02-it/equipment-replacement.md).

### Q: How do I reset my password?
Use the self-service password reset at aka.ms/sspr (linked from portal.acme.example) which requires both your Microsoft Authenticator app and a registered mobile number. If you have not registered SSPR yet, you can call the IT Helpdesk who will verify your identity through three security questions and reset it for you. The full password policy — including length, complexity, rotation, and the 24-hour reset cooldown — is in [../03-security/password-and-mfa-requirements.md](../03-security/password-and-mfa-requirements.md).

### Q: How do I configure VPN?
The ACME corporate VPN client is pre-installed on all corporate laptops and activated through the "ACME VPN" tray icon using your Entra ID credentials plus a push notification to Microsoft Authenticator. The VPN is required to access internal wikis, the dev/staging environments, and packages.acme.example; it is not needed for Microsoft 365, GitHub Enterprise, or hr.acme.example. Step-by-step setup, including split-tunnel rules and troubleshooting, is in [../02-it/corporate-vpn-configuration.md](../02-it/corporate-vpn-configuration.md).

### Q: How do I get access to a new tool?
File a [software access request](../02-it/software-access-requests.md) on helpdesk.acme.example, specifying the application name, business justification, and your manager — approval typically takes one to two business days. Most internal apps use Microsoft Entra ID single sign-on, so once approved, you simply sign in with your ACME credentials and complete MFA. Role-based applications (Vault, prod subscriptions, customer-data systems) require additional security review per the [least-privilege access](../03-security/least-privilege-access.md) policy.

### Q: How do I report a phishing email?
Use the "Report Phishing" button in Outlook (it ships with all ACME mailboxes) which forwards the message to the SOC and deletes it from your inbox. If you don't see the button, forward the email as an attachment to security@acme.example — do not click any links or reply to the sender. The security team will triage within four business hours; the [phishing awareness](../03-security/phishing-awareness.md) guide explains how to spot common campaigns targeting ACME employees.

### Q: How do I connect to corporate Wi-Fi?
The corporate SSID `ACME-Corp` uses WPA2-Enterprise and authenticates with your Entra ID credentials plus a Microsoft Authenticator push; the personal-device SSID `ACME-Byod` uses certificate-based auth issued through Intune. Choose `ACME-Corp` on corporate laptops and `ACME-Byod` on enrolled personal phones; the open `ACME-Guest` network is for visitors only and is throttled. See [../02-it/corporate-wifi-setup.md](../02-it/corporate-wifi-setup.md) for the full per-office SSID list and certificate enrollment steps.

### Q: My MFA stopped working — help?
First, try signing out of Microsoft Authenticator and back in; if that fails, the app may need re-registration which you can self-serve through the "Update your security info" link on portal.acme.example. If you cannot sign in at all, call the IT Helpdesk — they will issue a temporary access pass (TAP) valid for 8 hours so you can re-enroll. The recovery flow and the bypass policy are detailed in [../02-it/microsoft-authenticator-and-mfa.md](../02-it/microsoft-authenticator-and-mfa.md).

### Q: How do I get admin access on my laptop?
Local admin access is granted on a time-bound basis through a Just-In-Time request on helpdesk.acme.example, with manager approval and a 4-hour max duration. ACME uses Microsoft Privileged Identity Management (PIM) for this, and your activity is logged for security review per the [least-privilege access](../03-security/least-privilege-access.md) policy. Standing admin rights are reserved for designated IT support staff and SREs — see [../03-security/identity-and-access-management.md](../03-security/identity-and-access-management.md) for the full role matrix.

### Q: Can I install software from home?
You can install approved software from packages.acme.example at any time through the self-service Company Portal app — no VPN is required for this. Installing unapproved software, even free tools, requires the [approved software installation](../02-it/approved-software-installation.md) workflow regardless of where you are. If a tool you need is not in the catalog, raise a request rather than sideloading it; sideloaded software can disable your device's compliance and block VPN access.

### Q: My device was stolen — what do I do?
Report it within 30 minutes through [lost or stolen device reporting](../02-it/lost-or-stolen-device-reporting.md) or call the IT Helpdesk line — time matters because we need to remote-wipe before the thief bypasses disk encryption. File a police complaint and email a copy to helpdesk@acme.example so HR can update your asset record. The security team will assess whether any customer or Confidential data was exposed and rotate any tokens cached on the device; see [../03-security/security-incident-reporting.md](../03-security/security-incident-reporting.md) for the post-incident flow.

### Q: Can I use a personal laptop for work?
No — ACME requires corporate-issued laptops for all engineering and customer-data work; personal laptops cannot be enrolled in Intune and cannot access the VPN or corporate Wi-Fi. The only BYOD exception is for enrolled personal smartphones, covered in [../03-security/byod-policy.md](../03-security/byod-policy.md). If you occasionally need to read email from a personal device, use the Outlook web app at outlook.acme.example which is MFA-gated and does not download data to disk.

### Q: Where can I find approved software?
The approved software catalog is at packages.acme.example and is mirrored on the "Company Portal" app pre-installed on every corporate laptop. Each entry lists the licensing terms, owning team, and whether the install requires manager approval. The catalog and the request flow for new entries are documented in [../02-it/approved-software-installation.md](../02-it/approved-software-installation.md).

### Q: How do I get a second monitor?
Request a second monitor through the equipment-replacement module on helpdesk.acme.example — engineers and designers are eligible for one additional 27" 4K monitor by default, no manager approval needed. Other roles require manager approval and are subject to office stock availability. The full peripheral matrix, including docks, keyboards, and headsets, is in [../02-it/equipment-replacement.md](../02-it/equipment-replacement.md).

### Q: How do I update my password manager?
ACME uses 1Password Business (vault.acme.example) and the desktop app auto-updates; if it gets stuck, sign out and sign back in with your Entra ID credentials to trigger a re-sync of vaults. Do not store work credentials in personal password managers — that violates the [secrets management](../03-security/secrets-management.md) policy. The full setup, including the CLI for engineers, is in [../02-it/password-manager-configuration.md](../02-it/password-manager-configuration.md).

## Topics Covered

- **Hardware**: laptop allocation, monitors, peripherals, replacement
- **Software**: approved catalog, install requests, software from home
- **Identity and access**: password resets, MFA recovery, PIM/JIT admin access, new-tool requests
- **Network**: corporate VPN, corporate Wi-Fi and BYOD SSIDs
- **Device security and loss**: lost laptop, stolen device, BYOD limits, phishing reporting
- **Productivity tools**: password manager (1Password Business)

## Escalation Contacts

- IT Onboarding Specialist: Geetha Iyer — geetha.iyer@acme.example
- IT Manager Hyderabad: Arjun Kapoor — arjun.kapoor@acme.example
- VP IT: Ramesh Khanna — ramesh.khanna@acme.example
- IT Helpdesk: helpdesk@acme.example (or +91-40-0000-0000 after hours)
- CISO (security escalations): Rajan Mehta — rajan.mehta@acme.example
- GRC Analyst: Karthik Subramanian — karthik.subramanian@acme.example

For the full contact list, see [../09-contacts/contact-directory.md](../09-contacts/contact-directory.md). For IT support paths, see [../02-it/it-support-and-troubleshooting.md](../02-it/it-support-and-troubleshooting.md).
