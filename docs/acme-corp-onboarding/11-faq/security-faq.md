---
document_id: ACME-FAQ-004
title: Security Frequently Asked Questions
category: faq
department: all
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [faq, security, data-classification, phishing, mfa, encryption, byod]
---

# Security Frequently Asked Questions

This FAQ answers the most common security questions at ACME Corp — data classification, phishing, password policy, secrets management, BYOD, encryption, customer data, and incident reporting. When in doubt, email the security team at security@acme.example or page the on-call Security Engineer through PagerDuty. The canonical policies are in [../03-security/](../03-security/); CISO Rajan Mehta (rajan.mehta@acme.example) owns them.

### Q: What counts as Confidential?
Confidential is the second-highest data classification tier at ACME and includes source code, internal financials, customer PII, contracts, and any data whose unauthorized disclosure would cause material harm. The next tier up is Restricted (encryption keys, prod credentials, customer data covered by contractual SLAs), and below Confidential are Internal and Public. The full definitions and examples per category are in [../03-security/data-classification.md](../03-security/data-classification.md).

### Q: How do I report a phishing email?
Click the "Report Phishing" button in Outlook — it forwards the message to the SOC and removes it from your mailbox in one step. If you don't see the button, forward the email as an attachment (not inline) to security@acme.example and delete the original. The SOC triages within 4 business hours; see [../03-security/phishing-awareness.md](../03-security/phishing-awareness.md) for the patterns ACME has seen in past campaigns.

### Q: I clicked a suspicious link — what now?
Disconnect from the network (turn off Wi-Fi or unplug the cable) and call the IT Helpdesk at +91-40-0000-0000 immediately — do not shut down the laptop, just disconnect. The security team will remotely capture memory and start the incident workflow per [../03-security/security-incident-reporting.md](../03-security/security-incident-reporting.md). You will not be penalized for self-reporting; ACME's [acceptable use policy](../03-security/acceptable-use-policy.md) explicitly protects employees who promptly report clicks.

### Q: What's the password policy?
Passwords must be at least 14 characters, contain three of four character classes, and not appear in the breached-passwords list; rotation is risk-based (only on suspected compromise) rather than time-based. All credentials must be stored in 1Password Business (vault.acme.example), never in browser autofill or text files. The full requirements, including service-account and API-key rules, are in [../03-security/password-and-mfa-requirements.md](../03-security/password-and-mfa-requirements.md).

### Q: Can I store a customer API key locally?
No — customer API keys, tokens, and credentials are Restricted data and must live in ACME Vault (vault.acme.example) or a managed secret store, never on disk or in env files. Local `.env` files used during development must contain only non-sensitive values; real credentials are injected at runtime from the Vault agent. Violations are flagged by the secrets-scanning bot and reviewed per [../03-security/secrets-management.md](../03-security/secrets-management.md); see also [../03-security/customer-data-handling.md](../03-security/customer-data-handling.md).

### Q: How do I report a security incident?
Open a ticket on the Incident module at helpdesk.acme.example, selecting "Security" — the on-call Security Engineer is paged automatically. For active breaches or customer-data exposure, also page the SOC through the number on the back of your badge and notify Rajan Mehta (rajan.mehta@acme.example) within 30 minutes. The severity matrix, escalation paths, and the post-incident review template are in [../03-security/security-incident-reporting.md](../03-security/security-incident-reporting.md).

### Q: Is BYOD allowed?
BYOD is allowed for personal smartphones only, enrolled through Microsoft Intune which creates a separate work profile that ACME cannot view your personal data through. Personal laptops and tablets are not permitted to access ACME internal systems, VPN, or corporate Wi-Fi. The full policy, including the mandatory encryption, screen-lock, and remote-wipe conditions, is in [../03-security/byod-policy.md](../03-security/byod-policy.md).

### Q: What's the data classification for source code?
Source code is classified as Confidential by default; customer-specific code or code containing proprietary algorithms may be bumped to Restricted at the Director's discretion. Public-facing docs and marketing code samples are Internal unless explicitly marked Public on the repo README. The classification, handling, and disclosure rules for source are in [../03-security/source-code-security.md](../03-security/source-code-security.md).

### Q: Can I use ChatGPT or other public AI tools with company code?
No — pasting ACME source code, internal documents, customer data, or credentials into external AI tools (ChatGPT, Claude, Gemini, etc.) is treated as a Confidential data leak and is a policy violation. The only approved AI tools are GitHub Copilot Business and the ACME-hosted internal LLM at llm.acme.example which is data-resident and audited. The full rules, including the exception process for research use, are in [../03-security/ai-tool-acceptable-use.md](../03-security/ai-tool-acceptable-use.md).

### Q: How do I get a hardware security key?
Hardware security keys (YubiKey 5 NFC) are issued to all engineers, IT staff, and anyone with prod or admin access; file a request on helpdesk.acme.example and IT will hand it over at your nearest office. Enrollment takes 5 minutes through the Microsoft Entra portal's security-info page and you should register two keys for redundancy. The key is required for privileged-role activation per [../03-security/identity-and-access-management.md](../03-security/identity-and-access-management.md); see [../02-it/microsoft-authenticator-and-mfa.md](../02-it/microsoft-authenticator-and-mfa.md) for the full MFA flow.

### Q: How is encryption enforced?
All corporate laptops have BitLocker (Windows) or FileVault (macOS) enabled by Intune policy and escrowed to Microsoft Entra; you cannot disable it. Data at rest in our cloud subscriptions is encrypted with customer-managed keys held in ACME Vault, and data in transit uses TLS 1.2+. The encryption standards, key-rotation cadence, and the break-glass recovery flow are in [../03-security/device-encryption.md](../03-security/device-encryption.md).

### Q: How do I handle customer data?
Customer data is classified as Restricted or Confidential depending on the contract; you may access it only from corporate devices on the VPN or in approved cloud tenants, and only with a documented business need. Never download customer data to local disk, email it to personal accounts, or paste it into AI tools; use the customer-data workbench at portal.acme.example for analysis. The full handling matrix, including retention and deletion rules, is in [../03-security/customer-data-handling.md](../03-security/customer-data-handling.md).

### Q: What's the clean desk policy?
The clean desk policy requires that all Confidential and Restricted documents are locked away when you leave your desk — including whiteboard notes, printed code reviews, and sticky notes with passwords. At end of day, lock your laptop (Win+L or Ctrl+Cmd+Q) and stow any removable media in your desk drawer with the lock engaged. The full policy, including the random-desk-check cadence run by GRC, is in [../03-security/clean-desk-policy.md](../03-security/clean-desk-policy.md).

### Q: How do I access ACME Vault?
Vault is at vault.acme.example and uses Entra ID SSO with hardware-key MFA — your default vaults (Personal, Team-Shared, Engineering-Shared) are provisioned on your start date. Additional vaults require a vault-access request through the form at ../08-forms/software-access-request.md with the owning team's approval. The full setup, including CLI for engineers and the emergency-recovery flow, is in [../02-it/password-manager-configuration.md](../02-it/password-manager-configuration.md) and [../03-security/secrets-management.md](../03-security/secrets-management.md).

### Q: How often do I need to do security training?
All employees must complete the [security awareness](../10-training/security-awareness.md) module annually and the [privacy awareness](../10-training/privacy-awareness.md) module annually, both due by your hire-anniversary date. Engineers additionally complete a quarterly phishing simulation; click-throughs above 20% trigger a refresher assignment. Completion is tracked in the Learning module on hr.acme.example and gates access to customer-data systems per [../03-security/information-security-policy.md](../03-security/information-security-policy.md).

### Q: What is PIM?
PIM (Microsoft Entra Privileged Identity Management) is the Just-In-Time access system ACME uses for admin, prod-deploy, and elevated roles — you activate a role for a bounded window (typically 4 hours) with a recorded justification. PIM approvals route to your manager and the security on-call; all activations are logged and reviewed monthly by GRC. The role catalog, eligibility rules, and the audit dashboard are in [../03-security/identity-and-access-management.md](../03-security/identity-and-access-management.md) and [../03-security/least-privilege-access.md](../03-security/least-privilege-access.md).

### Q: How do I get a prod-deploy credential?
Prod-deploy credentials are issued only through PIM activation paired with an open Change Management ticket — there is no standing credential. The credential is OIDC-issued, short-lived (15 minutes), and bound to the deployment workflow ID; you cannot copy it to your local terminal. The full break-glass process, in case PIM is unavailable, is documented in [../03-security/secrets-management.md](../03-security/secrets-management.md) and [../04-engineering/practices/development-staging-production.md](../04-engineering/practices/development-staging-production.md).

### Q: Where are security policies published?
All ACME security policies are published on wiki.acme.example under "Security > Policies" and are also mirrored in this repo at [../03-security/](../03-security/). Each policy has an owner (CISO Rajan Mehta or a delegate), a version, and a review date printed in the front matter. If you find a contradiction between the wiki and this repo, the repo copy is canonical — please file an issue at git.acme.example/acme/internal-docs.

## Topics Covered

- **Data classification**: Confidential vs Restricted vs Internal vs Public; source-code classification
- **Phishing and clicks**: reporting phishing, what to do after clicking a link
- **Credentials**: password policy, customer API keys, prod-deploy credentials via PIM
- **Incidents**: how to report, severity, break-glass, customer-data exposure
- **Devices and access**: BYOD policy, hardware security keys (YubiKey), encryption enforcement
- **Secrets and Vault**: ACME Vault access, local `.env` rules, secrets-scanning
- **Customer data**: handling rules, retention, deletion
- **Clean desk**: physical security, removable media, end-of-day checklist
- **Training**: annual security + privacy modules, quarterly phishing simulations
- **PIM**: Just-In-Time activation, audit trail, monthly GRC review

## Escalation Contacts

- CISO: Rajan Mehta — rajan.mehta@acme.example
- GRC Analyst: Karthik Subramanian — karthik.subramanian@acme.example
- VP IT (incident response): Ramesh Khanna — ramesh.khanna@acme.example
- IT Helpdesk: helpdesk@acme.example (24/7 security paging through PagerDuty)
- Security on-call (active incidents): page through PagerDuty, link on status.acme.example

For the full contact list, see [../09-contacts/contact-directory.md](../09-contacts/contact-directory.md). For incident-response paths, see [../03-security/security-incident-reporting.md](../03-security/security-incident-reporting.md).
