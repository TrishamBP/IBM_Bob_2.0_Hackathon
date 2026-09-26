---
document_id: ACME-HR-010
title: ACME Corp Remote and Hybrid Working Policy
category: hr
department: human-resources
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [policy, hr, remote, hybrid, workplace]
---

# ACME Corp Remote and Hybrid Working Policy

This policy defines who can work remotely, who is expected in-office, what equipment and security obligations apply to remote work, and the process for changing working model.

## Working Models

| Model | Definition | In-office expectation |
|-------|------------|------------------------|
| Hybrid (office-assigned) | Employee lives within commuting distance of an ACME office. | ≥ 2 days/week in office. |
| Remote (domestic) | Employee lives in the same country as their hiring office, but outside commuting distance. | No in-office requirement. Annual in-person gathering optional. |
| Remote (international) | Employee lives in a country without an ACME office. | No in-office requirement. Annual in-person gathering mandatory. |

## Eligibility

- Hybrid is the default for employees living within commuting distance of an ACME office.
- Remote (domestic) requires hiring manager and HR Director approval. Eligibility is determined at the time of hire; subsequent changes require re-approval.
- Remote (international) requires hiring manager, HR Director, and Legal approval due to tax and employment-law implications. Approval lead time is typically 4–6 weeks.

## Equipment and Setup

All employees, regardless of model, receive:

- A corporate laptop, encrypted and managed by Intune. See [`02-it/laptop-and-workstation-allocation.md`](../02-it/laptop-and-workstation-allocation.md).
- An external monitor (1 for hybrid, 2 for remote).
- Keyboard and mouse.
- A headset for video meetings.

Additional peripherals (ergonomic chair, standing desk, second monitor for hybrid) can be requested via [`08-forms/it-access-request.md`](../08-forms/it-access-request.md) and are approved on a case-by-case basis.

Remote employees are not reimbursed for home office furniture beyond the standard kit. A one-time setup allowance (INR 15,000 / USD 300 / GBP 200) is provided for employees transitioning from hybrid to remote status.

## Security Obligations

Remote and hybrid employees must:

1. Use the corporate VPN (see [`02-it/corporate-vpn-configuration.md`](../02-it/corporate-vpn-configuration.md)) whenever accessing ACME internal services.
2. Store no customer data on local storage beyond what is required for active work.
3. Encrypt their device (default for all ACME laptops — see [`03-security/device-encryption.md`](../03-security/device-encryption.md)).
4. Not work from public Wi-Fi networks without the VPN active.
5. Follow the [`03-security/clean-desk-policy.md`](../03-security/clean-desk-policy.md) when working from a shared or public space.

## Tax and Legal Considerations

- Employees must work from the country declared in their employment agreement. Working from another country for more than 30 cumulative days in a calendar year may trigger tax and immigration obligations; it must be approved in advance by Legal and Finance.
- Cross-border work (more than 90 cumulative days per year outside the employment country) is generally not permitted without a written exception approved by the CFO and Legal.

## Changing Working Model

- **Hybrid → Remote (domestic):** Apply via ACME HR Hub. Requires manager and HR Director approval. Lead time: 2 weeks.
- **Remote (domestic) → Hybrid:** Apply via ACME HR Hub. Requires manager approval. Lead time: 2 weeks.
- **Office change (Hyderabad → Bengaluru, etc.):** Apply via ACME HR Hub. Requires old and new HR Director approval. Lead time: 4 weeks.

## In-Person Gatherings

- ACME hosts an annual company-wide gathering (typically in Hyderabad or Bengaluru) in Q1.
- Each BU hosts a 2-day off-site annually.
- Each team is encouraged to host an in-person quarterly review when budget permits.

## Related Documents

- [`00-company/office-locations-and-working-arrangements.md`](../00-company/office-locations-and-working-arrangements.md)
- [`01-hr/leave-and-attendance-policy.md`](./leave-and-attendance-policy.md)
- [`02-it/laptop-and-workstation-allocation.md`](../02-it/laptop-and-workstation-allocation.md)
- [`02-it/corporate-vpn-configuration.md`](../02-it/corporate-vpn-configuration.md)
- [`03-security/byod-policy.md`](../03-security/byod-policy.md)
- [`03-security/device-encryption.md`](../03-security/device-encryption.md)
- [`03-security/clean-desk-policy.md`](../03-security/clean-desk-policy.md)
