---
document_id: ACME-FAQ-005
title: Onboarding Frequently Asked Questions
category: faq
department: all
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [faq, onboarding, preboarding, first-day, 30-60-90, buddy]
---

# Onboarding Frequently Asked Questions

This FAQ answers the most common questions from new ACME Corp hires about preboarding, day one, the first week, and the 30/60/90 plan. Your onboarding coordinator is Priya Nair (priya.nair@acme.example); your IT onboarding specialist is Geetha Iyer (geetha.iyer@acme.example). The full onboarding workflows are documented in [../07-workflows/](../07-workflows/).

### Q: What do I do before day 1?
Complete the preboarding checklist at [../07-workflows/preboarding.md](../07-workflows/preboarding.md) which includes signing the [employment agreement](../01-hr/sample-employment-agreement.md), submitting the [employee information form](../01-hr/employee-information-form.md), and uploading your bank and tax details. You will receive the checklist by email from Priya Nair seven days before your start date. Most steps can be done from your phone; the laptop is handed over on day one.

### Q: Where do I get my laptop?
Laptops are handed out at the IT desk on the ground floor of your assigned office (Hyderabad, Bengaluru, London, or Seattle) between 09:00 and 11:00 IST on day one — bring a government photo ID. Remote employees receive a courier shipment two business days before start date; the tracking number is shared by Geetha Iyer (geetha.iyer@acme.example). The allocation policy and the upgrade-request path are in [../02-it/laptop-and-workstation-allocation.md](../02-it/laptop-and-workstation-allocation.md).

### Q: Who is my onboarding buddy?
Your onboarding buddy is a peer on your team assigned by your manager before day one — you'll get their name and Teams handle in the welcome email from your HRBP. The buddy is your go-to for "how do I…" questions during the first 30 days and is expected to schedule a 30-minute check-in daily in week one. Manager responsibilities for assigning and supporting buddies are documented in [../07-workflows/manager-onboarding-responsibilities.md](../07-workflows/manager-onboarding-responsibilities.md).

### Q: When do I get my corporate email?
Your Microsoft 365 account is activated at 09:00 IST on your start date and you'll receive a welcome email at your personal address with first-time sign-in instructions. You must set up Microsoft Authenticator on your phone during the first sign-in — IT support is on standby in the office to help. The full activation flow, including the temporary access pass for users without a phone, is in [../02-it/microsoft-365-account-activation.md](../02-it/microsoft-365-account-activation.md).

### Q: What's the schedule for day 1?
Day one runs from 09:30 to 16:00 IST and includes office tour, IT setup, HR welcome with your HRBP, a welcome lunch with your buddy, and a 30-minute intro with your manager. The full agenda is in [../07-workflows/first-day-onboarding.md](../07-workflows/first-day-onboarding.md); remote employees follow the same schedule on Teams. You'll receive the calendar invite the Friday before your start date.

### Q: When do I do security training?
The mandatory [security awareness](../10-training/security-awareness.md) and [privacy awareness](../10-training/privacy-awareness.md) modules must be completed by end of your first week, before repo or prod access is granted. The course takes about 3 hours total and is hosted on hr.acme.example under Learning; you can split it across multiple sittings. The completion record feeds the access-approval workflow documented in [../07-workflows/security-training.md](../07-workflows/security-training.md).

### Q: When will I have repo access?
Repository access is provisioned within two business days of your Microsoft 365 activation, provided you've completed security training and your manager has filed the access request. You'll see your repos in the [repository catalog](../04-engineering/repository-catalog.md) once your team membership syncs to GitHub Enterprise. The end-to-end access-approval flow, including the SLA per access tier, is in [../07-workflows/access-approval.md](../07-workflows/access-approval.md).

### Q: What if I don't have access I need?
Email your manager and your HRBP (cc helpdesk@acme.example) with the specific tool, repo, or system you're missing — most gaps are provisioning delays and resolve within 24 hours. If the access requires a security review (e.g. Vault, prod), expect up to 5 business days; your HRBP can expedite if it blocks your first-week goals. The escalation matrix for access issues is in [../00-company/employee-support-and-escalation.md](../00-company/employee-support-and-escalation.md).

### Q: Who is my HRBP?
HRBP assignment is by business unit: Kavya Krishnan (kavya.krishnan@acme.example) covers Cloud and Workspace; Deepika Rao (deepika.rao@acme.example) covers Intelligence, QE, and Support; Sanjay Patel (sanjay.patel@acme.example) covers Platform and Sales. Your HRBP is named in the welcome email from Priya Nair and is your first stop for benefits, leaves, and people issues. The full HRBP-to-team mapping is in [../09-contacts/contact-directory.md](../09-contacts/contact-directory.md).

### Q: When is my first 1:1 with my manager?
Your first 1:1 is scheduled on day one — typically a 30-minute intro — and then becomes a recurring weekly 45-minute slot starting week one. Your manager is expected to share the 30/60/90 expectations in writing by end of week one; the manager checklist is in [../07-workflows/manager-onboarding-responsibilities.md](../07-workflows/manager-onboarding-responsibilities.md). If your 1:1 keeps getting rescheduled, escalate to your HRBP.

### Q: What are the 30/60/90 expectations?
By day 30 you should be shipping small PRs, by day 60 leading a small feature, and by day 90 owning a project end-to-end — the full rubric is in [../07-workflows/first-30-days.md](../07-workflows/first-30-days.md), [../07-workflows/first-60-days.md](../07-workflows/first-60-days.md), and [../07-workflows/first-90-days.md](../07-workflows/first-90-days.md). Your manager tailors these to your role using the [team onboarding guide](../05-teams/). At day 90 you and your manager complete a written check-in that feeds into your probation confirmation.

### Q: How do I find my team's repos?
Open the [repository catalog](../04-engineering/repository-catalog.md) and filter by your team name, or run `gh repo list --mine` after your GitHub Enterprise access is active. Your team onboarding guide (e.g. [../05-teams/backend-engineer-onboarding.md](../05-teams/backend-engineer-onboarding.md)) lists the specific repos to clone on day one. If a repo you expected is missing, file a repository access request through the form at ../08-forms/repository-access-request.md.

### Q: When do I shadow on-call?
Engineers shadow the on-call rotation starting week three (after completing the [incident response intro](../04-engineering/practices/incident-response-and-on-call-introduction.md) training) and join as primary after their manager signs off at day 60. Shadowing means you receive pages alongside the primary and join the incident bridge but are not the lead responder. Your team onboarding doc lists the exact rotation length and the on-call allowance per the [employee handbook](../00-company/employee-handbook.md).

### Q: How do I get a Copilot seat?
Your manager files the [AI coding assistant license request](../08-forms/ai-coding-assistant-license-request.md) form during week one — the license activates within two business days of approval. You'll see "GitHub Copilot" in your GitHub Enterprise settings once provisioned; the VS Code and IntelliJ extensions auto-detect the seat. Setup steps and the acceptable-use rules are in [../04-engineering/ai-coding-assistant-setup.md](../04-engineering/ai-coding-assistant-setup.md) and [../03-security/ai-tool-acceptable-use.md](../03-security/ai-tool-acceptable-use.md).

### Q: How do I give onboarding feedback?
Submit the [onboarding feedback](../08-forms/onboarding-feedback.md) form at day 30, day 60, and day 90 — anonymous submission is supported. Feedback goes to Priya Nair and the VP of the business unit you joined, and is reviewed monthly to improve the program. You can also share urgent feedback any time by emailing your HRBP directly; see [../09-contacts/contact-directory.md](../09-contacts/contact-directory.md).

### Q: Where do I find my team's training plan?
Each team's training plan is in [../10-training/](../10-training/) and is also linked from your team onboarding guide under the "Training" section. The plan lists required modules, target completion dates, and elective courses; completion is tracked in the Learning module on hr.acme.example. Engineering roles share a common [engineering orientation](../10-training/engineering-orientation.md) baseline plus team-specific additions.

### Q: How do I book a meeting room?
Use the "Book a Room" feature in Outlook (linked from portal.acme.example) — rooms are listed by office and capacity, with TVs and Zoom-equipment rooms marked. Bookings auto-release after 10 minutes if no one checks in via the room tablet, so release early if your meeting is cancelled. The full list of rooms per office and the standing-booking rules are in [../00-company/office-locations-and-working-arrangements.md](../00-company/office-locations-and-working-arrangements.md).

### Q: What's the dress code in the office?
ACME is business-casual across all four offices — collared shirts, blouses, kurtas, chinos, and smart jeans are all fine; closed-toe footwear is required in lab and data-center areas. Client-facing meetings may warrant a blazer but suits are not required. The full dress expectation, including exceptions for events, is in [../01-hr/code-of-conduct.md](../01-hr/code-of-conduct.md).

### Q: Can I work from another city for a week?
Yes — a "work from anywhere" week is allowed up to four times per calendar year, with manager approval and a security attestation that your remote setup meets ACME standards (corporate laptop, MFA, no public Wi-Fi for work). Submit the request through the Leave-and-Working-Arrangement module on hr.acme.example at least five business days in advance. The full policy, including tax-implications for international work, is in [../01-hr/remote-and-hybrid-working-policy.md](../01-hr/remote-and-hybrid-working-policy.md) and [../00-company/office-locations-and-working-arrangements.md](../00-company/office-locations-and-working-arrangements.md).

## Topics Covered

- **Preboarding**: forms, agreements, ID verification, bank/tax setup
- **Day one**: schedule, laptop handover, corporate email activation, first 1:1
- **First week**: security training, repo access, Copilot seat, missing-access escalation
- **First 30/60/90**: expectations, on-call shadowing, training plans, feedback
- **HRBP and buddies**: who your HRBP is, onboarding buddy assignments
- **Office logistics**: meeting-room booking, dress code, work-from-anywhere weeks

## Escalation Contacts

- HR Onboarding Coordinator: Priya Nair — priya.nair@acme.example
- IT Onboarding Specialist: Geetha Iyer — geetha.iyer@acme.example
- VP HR: Ananya Sharma — ananya.sharma@acme.example
- VP IT: Ramesh Khanna — ramesh.khanna@acme.example
- IT Helpdesk: helpdesk@acme.example
- Your HRBP (assigned by team) — see [../09-contacts/contact-directory.md](../09-contacts/contact-directory.md)

For the support-and-escalation paths, see [../00-company/employee-support-and-escalation.md](../00-company/employee-support-and-escalation.md). To give onboarding feedback, use the [onboarding feedback form](../08-forms/onboarding-feedback.md).
