---
document_id: ACME-COMP-005
title: ACME Corp Organizational Structure
category: company
department: all
applicable_roles: [all]
owner: HR Operations
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [org-chart, leadership, structure, canonical]
---

# ACME Corp Organizational Structure

This document is the **canonical reference** for ACME's leadership structure. Every other document in this library that references a leader, manager, or reporting relationship must agree with what is listed here. If you are writing a new document, link here rather than inventing a new chain of command.

## Executive Leadership

| Role | Name (fictional) | Reports To |
|------|------------------|------------|
| Chief Executive Officer | Karthikeyan Subramanian | Board of Directors |
| Chief Operating Officer | Helena Brooks | CEO |
| Chief Technology Officer | Sridhar Venkatesh | CEO |
| Chief Financial Officer | Ritu Khanna | CEO |
| Chief Information Security Officer | Colonel Rajan Mehta (Retd.) | CEO |
| Chief Product Officer | Daniel Coelho | CEO |
| VP Human Resources | Ananya Sharma | COO |
| VP IT Operations | Ramesh Khanna | COO |
| Director, Sales | Christina Müller | COO |
| Director, Customer Support | Bo Tan | COO |
| Director, Legal and Compliance | Hemant Joshi | CFO |

## Department Leadership

| Department | Leader | Title | Office |
|-----------|--------|-------|--------|
| Human Resources | Ananya Sharma | VP HR | Hyderabad |
| IT Operations | Ramesh Khanna | VP IT | Hyderabad |
| Information Security | Rajan Mehta | CISO | Hyderabad |
| Software Engineering (Cloud + Workspace) | Sridhar Venkatesh | CTO | Hyderabad |
| AI and Machine Learning | Anitha Rajan | Director AI/ML | Bengaluru |
| Cloud Platform and DevOps | Nikhil Joshi | Manager, Platform | Bengaluru |
| Product Management | Daniel Coelho | CPO | Seattle |
| UX and Design | Sara Lindberg | Director UX | London |
| Quality Engineering | Asha Reddy | Manager, QE | Bengaluru |
| Sales | Christina Müller | Director, Sales | London |
| Customer Support | Bo Tan | Director, Support | Seattle |
| Finance | Ritu Khanna | CFO | Hyderabad |
| Legal and Compliance | Hemant Joshi | Director, Legal | Hyderabad |

## Engineering Manager Roster

Engineering managers own the repositories listed in [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md). New engineers must know their EM and their team's repos.

| Team | EM | Reports To | Repositories Owned |
|------|----|-----------|---------------------|
| Cloud API | Anjali Desai | Sridhar Venkatesh | `acme-cloud-api` |
| Cloud Frontend | Manoj Pillai | Sridhar Venkatesh | `acme-cloud-frontend` |
| Intelligence Agents | Rohan Bhat | Anitha Rajan | `acme-intelligence-agents` |
| Intelligence Inference | Vivek Anand | Anitha Rajan | `acme-intelligence-inference` |
| Intelligence ML | Lakshmi Narayan | Anitha Rajan | `acme-intelligence-ml` |
| Workspace Web | Thomas Buckley | Sridhar Venkatesh | `acme-workspace-web` |
| Workspace API | Priya Menon | Sridhar Venkatesh | `acme-workspace-api` |
| Platform Infrastructure | Nikhil Joshi | Sridhar Venkatesh | `acme-platform-infrastructure` |
| Shared Libraries | Nikhil Joshi (acting) | Sridhar Venkatesh | `acme-shared-libraries` |
| Quality Engineering | Asha Reddy | Sridhar Venkatesh | `acme-quality-automation` |

## HR and Operations Leadership by Office

| Office | HR Lead | IT Lead |
|--------|---------|---------|
| Hyderabad | Vikram Reddy (HR Director) | Arjun Kapoor (IT Manager) |
| Bengaluru | Priya Iyer (HR Director) | Latha Krishnamurthy (IT Helpdesk Lead, acting) |
| London | Meera Nair (HR Director) | Faisal Ahmed (Identity Engineer, acting) |
| Seattle | James Whitfield (HR Director) | Suresh Babu (Endpoint Engineer, acting) |

## Reporting Lines

The simplest way to think about reporting at ACME:

- All engineers report into a **team** owned by an **Engineering Manager** (EM).
- EMs report into either Sridhar Venkatesh (Cloud, Workspace, Platform, QE) or Anitha Rajan (Intelligence).
- EMs are responsible for their engineers' onboarding plans, access requests, performance reviews, and promotion packets.
- HR Business Partners (HRBPs) are paired with each engineering team. Your HRBP is your escalation point for HR issues.

## HR Business Partner Assignments

| Team | HRBP |
|------|------|
| Cloud API / Cloud Frontend | Kavya Krishnan |
| Intelligence (Agents / Inference / ML) | Deepika Rao |
| Workspace (Web / API) | Kavya Krishnan |
| Platform Infrastructure / Shared Libraries | Sanjay Patel |
| Quality Engineering | Deepika Rao |
| Sales | Sanjay Patel |
| Customer Support | Deepika Rao |

## Onboarding Buddies

Every new employee is assigned an onboarding buddy from their team. Buddies are typically a peer (same level, same team) who has been at ACME for at least 6 months. Buddy assignments are made by the hiring EM one week before the start date and recorded in [`07-workflows/preboarding.md`](../07-workflows/preboarding.md).

See [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md) for full contact details.

## Related Documents

- [`00-company/company-profile.md`](./company-profile.md)
- [`00-company/products-and-business-units.md`](./products-and-business-units.md)
- [`09-contacts/contact-directory.md`](../09-contacts/contact-directory.md)
- [`04-engineering/repository-catalog.md`](../04-engineering/repository-catalog.md)
- [`07-workflows/manager-onboarding-responsibilities.md`](../07-workflows/manager-onboarding-responsibilities.md)
