/**
 * Mock assistant service.
 *
 * This module provides clearly fictional demo responses for the onboarding
 * chatbot. It is a drop-in replacement for a real FastAPI RAG client and will
 * be swapped out in a future phase.
 *
 * IMPORTANT: These responses are illustrative placeholders only.
 * They do not represent real ACME Corp policies or documentation.
 */

import type { AssistantRequest, AssistantResponse } from '@/types/chat';
import { generateId } from './chatUtils';

// ---------------------------------------------------------------------------
// Simulated response delay (ms) — makes the demo feel realistic
// ---------------------------------------------------------------------------

const MOCK_DELAY_MS = 900;

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// ---------------------------------------------------------------------------
// Keyword → canned response map
// ---------------------------------------------------------------------------

interface MockEntry {
  keywords: string[];
  response: string;
  sources?: AssistantResponse['sources'];
}

const MOCK_ENTRIES: MockEntry[] = [
  {
    keywords: ['development environment', 'dev environment', 'dev setup', 'set up', 'setup'],
    response: `## Setting Up Your Development Environment

Welcome to ACME Engineering! Here's the standard setup process:

### 1. Install Required Tools
\`\`\`bash
# Install Homebrew (macOS) or use your package manager
brew install git node python@3.12 docker
\`\`\`

### 2. Clone the Onboarding Repository
\`\`\`bash
git clone https://github.acmecorp.internal/eng/onboarding-kit.git
cd onboarding-kit && ./setup.sh
\`\`\`

### 3. Configure Your IDE
ACME recommends **VS Code** with the ACME extensions pack. You can install it by opening VS Code and running:
> Extensions → Search "ACME Corp Pack" → Install

### 4. Access Internal Services
Your IT buddy will send you credentials for:
- **Jira** — project tracking
- **Confluence** — internal wiki
- **Vault** — secrets management

> ⚠️ **Demo response** — This is illustrative content. Refer to the actual IT Setup Guide in Confluence for authoritative instructions.`,
    sources: [
      {
        id: generateId('src'),
        title: 'Engineering Onboarding Handbook',
        department: 'Software Engineering',
        reference: 'Section 2: Environment Setup',
      },
      {
        id: generateId('src'),
        title: 'IT Setup Checklist',
        department: 'IT Operations',
        reference: 'Appendix A',
      },
    ],
  },
  {
    keywords: ['documents', 'paperwork', 'onboarding documents', 'what documents', 'need for onboarding'],
    response: `## Onboarding Documents

To complete your onboarding at ACME Corp, you'll typically need to submit the following:

### Identity & Legal
- Government-issued photo ID (passport or driving licence)
- Right-to-work documentation
- Bank account details for payroll

### HR Forms
- Emergency contact form
- Benefits enrollment form (deadline: first 30 days)
- Tax declaration (W-4 or P46 depending on jurisdiction)

### IT & Security
- Acceptable Use Policy — sign and return to IT
- NDA acknowledgement — provided by Legal

All forms are available in **Workday** under *My Profile → Onboarding Tasks*.

> ⚠️ **Demo response** — Document requirements may vary by location. Contact HR directly for jurisdiction-specific guidance.`,
    sources: [
      {
        id: generateId('src'),
        title: 'New Employee Onboarding Guide',
        department: 'Human Resources',
        reference: 'Chapter 1: Your First Week',
      },
    ],
  },
  {
    keywords: ['vpn', 'corporate vpn', 'configure vpn', 'connect vpn'],
    response: `## Corporate VPN Setup

ACME Corp uses **Cisco AnyConnect** for secure remote access.

### Installation
1. Download AnyConnect from the IT Self-Service Portal: \`https://selfservice.acmecorp.internal\`
2. Run the installer and accept the ACME certificate
3. Enter the gateway: \`vpn.acmecorp.internal\`

### First Connection
\`\`\`
Host:     vpn.acmecorp.internal
Username: your ACME email (e.g. you@acmecorp.com)
Password: your SSO password
MFA:      Approve the push notification in Microsoft Authenticator
\`\`\`

### Troubleshooting
If the connection fails, open a ticket with IT Support at \`#it-help\` in Slack or email \`itsupport@acmecorp.com\`.

> ⚠️ **Demo response** — VPN gateway addresses are fictional. Confirm details with your IT buddy.`,
    sources: [
      {
        id: generateId('src'),
        title: 'Remote Access & VPN Policy',
        department: 'Information Security',
        reference: 'Policy IS-204, v3.1',
      },
    ],
  },
  {
    keywords: ['leave policy', 'holiday', 'annual leave', 'time off', 'pto', 'vacation'],
    response: `## Leave Policy

ACME Corp offers a **flexible leave** policy. Key details:

| Leave Type         | Allowance              |
|--------------------|------------------------|
| Annual Leave       | 25 days (pro-rated)    |
| Sick Leave         | Unlimited (with notice) |
| Parental Leave     | 26 weeks primary carer |
| Bereavement        | 5 days paid            |
| Volunteering Days  | 3 days per year        |

### How to Request Leave
1. Open **Workday** → *Time & Absence*
2. Select *Request Absence*
3. Your manager receives an approval notification

For planned absence of more than 2 weeks, notify your manager at least 4 weeks in advance.

> ⚠️ **Demo response** — Leave entitlements depend on your contract and jurisdiction. Review your offer letter or contact HR.`,
    sources: [
      {
        id: generateId('src'),
        title: 'Employee Leave Policy',
        department: 'Human Resources',
        reference: 'HR-POL-012, Section 4',
      },
    ],
  },
  {
    keywords: ['repository', 'repo', 'access', 'request access', 'github access'],
    response: `## Requesting Repository Access

### Standard Access
Most repositories are accessible automatically once your GitHub account is linked to the ACME organisation. To link your account:

1. Go to **IT Self-Service** → *GitHub Access Request*
2. Enter your GitHub username
3. Accept the organisation invitation (check your email)

### Elevated Access
For private or restricted repositories:
1. Ask your tech lead to raise an **access request ticket** in Jira (project: \`ITREQ\`)
2. The repo owner reviews and approves within 2 business days
3. IT provisions access and notifies you via Slack

> 💡 Always use your ACME GitHub account (\`@acmecorp\`), not personal accounts, for work code.

> ⚠️ **Demo response** — Process may vary by team. Check with your tech lead first.`,
    sources: [
      {
        id: generateId('src'),
        title: 'Source Code Access Policy',
        department: 'Information Security',
        reference: 'Policy IS-108',
      },
    ],
  },
  {
    keywords: ['github copilot', 'copilot', 'ai coding', 'code completion'],
    response: `## Setting Up GitHub Copilot at ACME

ACME Corp provides GitHub Copilot licences to all engineers. Setup takes about 5 minutes.

### 1. Verify Your Licence
Check your ACME GitHub profile at \`github.acmecorp.internal\` — Copilot should show as **Active**. If not, contact IT.

### 2. Install the VS Code Extension
\`\`\`
Extensions → Search "GitHub Copilot" → Install
\`\`\`
Also install **GitHub Copilot Chat** for inline chat.

### 3. Sign In
When prompted, sign in with your **ACME GitHub account** (SSO). Do not use a personal GitHub account.

### 4. Usage Guidelines
- ✅ Use Copilot for boilerplate, tests and documentation
- ✅ Always review generated code before committing
- ❌ Do not paste confidential data, credentials or customer PII into prompts
- ❌ Do not use Copilot on repositories marked \`[RESTRICTED]\`

Full guidelines are in the **AI Tools Acceptable Use Policy** on Confluence.

> ⚠️ **Demo response** — Licence availability subject to team allocation. Contact your manager.`,
    sources: [
      {
        id: generateId('src'),
        title: 'AI Tools Acceptable Use Policy',
        department: 'Information Security',
        reference: 'Policy IS-312, v1.0',
      },
      {
        id: generateId('src'),
        title: 'Engineering Tooling Guide',
        department: 'Software Engineering',
        reference: 'Section 7: AI Assistance',
      },
    ],
  },
];

// ---------------------------------------------------------------------------
// Generic fallback
// ---------------------------------------------------------------------------

const GENERIC_RESPONSE = `I'm your ACME onboarding assistant, but I'm not yet connected to the company knowledge base.

The AI knowledge service (**RAG pipeline**) will be integrated in a future phase. Once connected, I'll be able to answer questions using actual ACME Corp documentation, policies and internal resources.

In the meantime, here are some ways to find what you need:

- **Confluence** — Internal wiki and documentation
- **Workday** — HR forms and policies
- **#it-help** on Slack — IT support
- **#people-ops** on Slack — HR queries
- Your **onboarding buddy** — assigned in your welcome email

> ⚠️ **Demo mode** — This assistant is currently returning placeholder responses only.`;

// ---------------------------------------------------------------------------
// Service function
// ---------------------------------------------------------------------------

/**
 * Returns a mock assistant response.
 *
 * Matches the last user message against known onboarding keywords.
 * Falls back to a generic "not yet connected" message.
 *
 * Replace this entire function with a real FastAPI API client in the next phase.
 */
export async function getMockAssistantResponse(
  request: AssistantRequest
): Promise<AssistantResponse> {
  await delay(MOCK_DELAY_MS);

  const lastUserMessage = [...request.messages]
    .reverse()
    .find((m) => m.role === 'user');

  if (!lastUserMessage) {
    return { content: GENERIC_RESPONSE, isMock: true };
  }

  const query = lastUserMessage.content.toLowerCase();

  for (const entry of MOCK_ENTRIES) {
    if (entry.keywords.some((kw) => query.includes(kw))) {
      return {
        content: entry.response,
        sources: entry.sources,
        isMock: true,
      };
    }
  }

  return { content: GENERIC_RESPONSE, isMock: true };
}
