---
document_id: ACME-ENG-014
title: ACME Corp Developer Workstation Setup
category: engineering
department: engineering
applicable_roles: [engineers]
owner: Engineering
version: 1.0.0
last_updated: 2026-09-15
review_date: 2027-09-15
status: published
confidentiality: internal
tags: [engineering, developer-workstation, setup, onboarding]
---

# ACME Corp Developer Workstation Setup

This guide walks a new engineer through setting up a working development environment on their ACME-issued laptop. It assumes the laptop has been enrolled in Intune, BitLocker or FileVault is enabled, and Microsoft 365 + Microsoft Authenticator are configured — see [`02-it/windows-11-and-macos-workstation-setup.md`](../02-it/windows-11-and-macos-workstation-setup.md) and [`02-it/microsoft-365-account-activation.md`](../02-it/microsoft-365-account-activation.md) for those prerequisites.

This is a fictional guide. Commands and snippets are illustrative; some endpoints (`packages.acme.example`, `vault.acme.example`, `git.acme.example`) are fictional and not reachable.

## Prerequisites

- ACME laptop enrolled in Intune, encrypted, with corporate identity signed in.
- Microsoft 365 active and Microsoft Authenticator enrolled.
- Corporate VPN installed and tested — see [`02-it/corporate-vpn-configuration.md`](../02-it/corporate-vpn-configuration.md).
- 1Password Business installed and signed in — see [`02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md).
- Repository access approved by your EM — see [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md).
- For Windows users: WSL2 installed and Ubuntu 24.04 LTS configured.

> Before running any of the commands below, connect to the ACME VPN. Internal hosts (`packages.acme.example`, `vault.acme.example`, `git.acme.example`, `runners.internal.acme.example`) are not resolvable off-VPN.

## 1. VS Code Installation

ACME standardizes on **Visual Studio Code** (not VS Code Insiders and not Cursor for default work). The approved distribution is the standard installer from Microsoft, installed via Software Center (Windows) or Self Service (macOS).

### Windows

1. Open **Software Center** from the Start menu.
2. Search for "Visual Studio Code" and click **Install**.
3. After install, sign in with your `@acme.example` account under **Settings Sync** to sync approved extensions across devices.

### macOS

1. Open **Self Service** from Applications.
2. Search for "Visual Studio Code" and click **Install**.
3. After install, sign in with your `@acme.example` account under **Settings Sync**.

### Approved Extensions

Install the following approved extensions via the VS Code Marketplace. The list is governed by [`03-security/source-code-security.md`](../03-security/source-code-security.md) and [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md).

| Extension | Purpose | Required? |
|-----------|---------|-----------|
| GitHub Copilot | AI coding assistant — see [`ai-coding-assistant-setup.md`](./ai-coding-assistant-setup.md) | Required for engineers with a Copilot license |
| GitHub Pull Requests | PR review in-editor | Required |
| Remote – WSL | Run VS Code server inside WSL2 | Required for Windows |
| Remote – SSH | Develop against remote dev-containers | Optional |
| Docker | Manage Docker Desktop from VS Code | Required |
| Python (Microsoft) | Python language server, debugging | Required for Python work |
| Go | Go language server, debugging | Required for Go work |
| ESLint | Lint TypeScript / JavaScript | Required for TS work |
| Prettier | Format TypeScript / JavaScript | Required for TS work |
| SonarLint | Static analysis on save | Optional, recommended |
| 1Password | Inline secrets UI | Optional, recommended |
| GitLens | Inline Git blame, log | Optional |

Forbidden extensions: any extension that exfiltrates source code to an external endpoint not on the approved AI tool list (see [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)). When in doubt, ask in `#engineering-help` on Microsoft Teams.

## 2. Git Installation and Configuration

### Windows

Git for Windows is pre-installed via Intune. Verify:

```bash
# fictional/simulated
git --version
# git version 2.46.0.windows.1
```

### macOS

```bash
# fictional/simulated
xcode-select --install  # if not already installed
git --version
# git version 2.46.0 (Apple Git-143)
```

### Global Configuration

Set your identity and the ACME-standard defaults:

```bash
# fictional/simulated
git config --global user.name "Anika Rao"
git config --global user.email "anika.rao@acme.example"
git config --global init.defaultBranch main
git config --global pull.rebase true
git config --global push.autoSetupRemote true
git config --global core.autocrlf input   # macOS / Linux
# git config --global core.autocrlf true  # Windows
git config --global commit.gpgsign true
git config --global gpg.format ssh
```

> Use your `@acme.example` email — not your personal email. Commits with personal emails are blocked by the commit-author check on GitHub Enterprise.

## 3. GitHub Enterprise Authentication

ACME uses GitHub Enterprise Cloud at the fictional host `git.acme.example`. Authentication is via Microsoft Entra ID SSO.

### Sign In

1. Open `https://git.acme.example` in your browser.
2. Sign in with your `@acme.example` email.
3. You will be redirected to Microsoft Entra ID; sign in with your corporate credentials and approve the MFA prompt.
4. On first sign-in, you will be added to the `acme` organization automatically via SCIM provisioning.

### Configure the GitHub CLI

Install the GitHub CLI (`gh`) from Software Center (Windows) or Self Service (macOS). Then:

```bash
# fictional/simulated
gh auth login --hostname git.acme.example --web
# Follow the prompt; select "Login with a web browser".
# Authorize the GitHub CLI app.
gh auth status
```

### Verify Repository Access

After your manager approves your repository access request (see [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md)), verify by cloning the canonical "hello world" test repository:

```bash
# fictional/simulated
git clone git@git.acme.example:acme/hello-acme.git
cd hello-acme
cat README.md
```

If you receive "Permission denied", your repository access request has not been processed yet. Contact your EM or open a ticket with IT Helpdesk.

## 4. SSH Key Generation and Registration

ACME requires SSH key authentication for Git operations on GitHub Enterprise. The supported key types are `ed25519` (default) and `rsa` 4096-bit (legacy).

### Generate a Key

```bash
# fictional/simulated
ssh-keygen -t ed25519 -C "anika.rao@acme.example" -f ~/.ssh/id_ed25519_acme
```

Use a strong passphrase (≥ 14 characters). Store the passphrase in 1Password.

### Register the Public Key

```bash
# fictional/simulated
gh ssh-key add ~/.ssh/id_ed25519_acme.pub --title "Anika's ACME laptop" --type authentication
```

Alternatively, paste the public key into `https://git.acme.example/settings/ssh` under "SSH and GPG keys".

### Verify

```bash
# fictional/simulated
ssh -T git@git.acme.example
# Hi anika-rao! You've successfully authenticated, but GitHub does not provide shell access.
```

### Configure the SSH Agent

To avoid typing your passphrase on every operation:

```bash
# fictional/simulated
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_acme
```

On macOS, configure the keychain:

```bash
# fictional/simulated
# ~/.ssh/config
Host git.acme.example
  HostName git.acme.example
  User git
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519_acme
```

## 5. Python Installation and Virtual Environments

ACME uses Python 3.12 by default. Intelligence teams may use 3.11 for compatibility with specific ML libraries — check with your team.

### Install via pyenv (recommended)

```bash
# fictional/simulated
# Install pyenv (macOS)
brew install pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc

# Install Python 3.12
pyenv install 3.12.7
pyenv global 3.12.7
python --version
# Python 3.12.7
```

### Configure pip to Use the ACME Internal Registry

```ini
# ~/.pip/pip.conf  (macOS/Linux)
# %APPDATA%\pip\pip.ini  (Windows)

[global]
index-url = https://packages.acme.example/pypi/simple/
extra-index-url = https://pypi.org/simple/
trusted-host = packages.acme.example

[install]
no-build-isolation = false
```

> The internal registry is required for ACME-internal packages. Public packages are pulled from PyPI via the proxy. The internal registry is signed; verification is enforced by `pip` ≥ 23.

### Virtual Environments

ACME uses `uv` for fast virtual environment management. Install via:

```bash
# fictional/simulated
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then, per project:

```bash
# fictional/simulated
cd acme-intelligence-agents
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt -r requirements-dev.txt
```

## 6. Node.js and Package Managers

ACME uses Node.js 22 LTS by default. Frontend teams additionally use 20 LTS for legacy compatibility.

### Install via fnm (recommended)

```bash
# fictional/simulated
curl -fsSL https://fnm.vercel.app/install | bash
exec $SHELL
fnm install 22
fnm use 22
node --version
# v22.10.0
npm --version
# 10.9.0
```

### Configure npm to Use the ACME Internal Registry

```bash
# fictional/simulated
npm config set registry https://packages.acme.example/npm/
npm login --scope=@acme --registry=https://packages.acme.example/npm/
# Authenticate via browser-based SSO.
```

### pnpm (preferred for monorepos)

```bash
# fictional/simulated
npm install -g pnpm
pnpm config set registry https://packages.acme.example/npm/
```

## 7. Docker Desktop or Docker Engine

ACME provides Docker Desktop (with a Business license) to all engineers on Windows and macOS. Linux users install Docker Engine directly.

### Windows / macOS

Install Docker Desktop from Software Center (Windows) or Self Service (macOS). Sign in with your `@acme.example` email under **Sign In** → **GitHub** (Docker Desktop uses GitHub for auth).

Configure Docker Desktop:

- **Resources → WSL Integration:** Enable for your WSL distro (Windows only).
- **Settings → Docker Engine:** Add the ACME registry mirror.

```json
{
  "registry-mirrors": ["https://registry.internal.acme.example"],
  "insecure-registries": [],
  "experimental": false
}
```

### Verify

```bash
# fictional/simulated
docker version
docker run --rm hello-world
docker login registry.internal.acme.example
# Sign in with your @acme.example SSO.
```

## 8. WSL2 for Windows Developers

Windows engineers do native development inside WSL2 (Ubuntu 24.04 LTS), not on Windows directly. The corporate Windows image ships with WSL2 enabled; the Ubuntu distribution is installed via Software Center.

### Install Ubuntu

1. Open **Software Center**, search for "Ubuntu 24.04 LTS", and click **Install**.
2. Launch **Ubuntu 24.04 LTS** from the Start menu.
3. Set a UNIX username and password. Use a strong passphrase (≥ 14 characters); store in 1Password.

### Configure WSL

In PowerShell (admin):

```powershell
# fictional/simulated
wsl --set-default Ubuntu-24.04
wsl --shutdown
```

Inside Ubuntu:

```bash
# fictional/simulated
sudo apt update && sudo apt install -y build-essential curl git
```

### VS Code Remote-WSL

Install the **Remote – WSL** extension in VS Code. Open a WSL terminal in VS Code via **View → Command Palette → WSL: New Window**. All subsequent VS Code windows from WSL will run the VS Code server inside Ubuntu.

## 9. Corporate Package Registries

ACME operates internal package registries for Go, npm, PyPI, and Maven. They are all reachable at `packages.acme.example` (fictional) over the VPN.

| Ecosystem | Registry URL (fictional) | Scope |
|-----------|-------------------------|-------|
| Go | `https://packages.acme.example/go/` | `acme.example/*` modules |
| npm | `https://packages.acme.example/npm/` | `@acme/*` packages |
| PyPI | `https://packages.acme.example/pypi/simple/` | `acme-*` packages |
| Maven | `https://packages.acme.example/maven/` | `com.acme.*` artifacts |

For Go, configure `GOPRIVATE`:

```bash
# fictional/simulated
go env -w GOPRIVATE=git.acme.example/*
go env -w GONOSUMCHECK=git.acme.example/*
echo 'export GOPRIVATE=git.acme.example/*' >> ~/.bashrc
```

For Maven, configure `~/.m2/settings.xml`:

```xml
<!-- fictional/simulated -->
<settings>
  <servers>
    <server>
      <id>acme-internal</id>
      <username>${env.ARTIFACTORY_USER}</username>
      <password>${env.ARTIFACTORY_TOKEN}</password>
    </server>
  </servers>
  <profiles>
    <profile>
      <id>acme</id>
      <repositories>
        <repository>
          <id>acme-internal</id>
          <url>https://packages.acme.example/maven/</url>
        </repository>
      </repositories>
    </profile>
  </profiles>
  <activeProfiles>
    <activeProfile>acme</activeProfile>
  </activeProfiles>
</settings>
```

> The `ARTIFACTORY_USER` and `ARTIFACTORY_TOKEN` values are stored in ACME Vault under `secret/acme/dev/artifactory`. Fetch them via the Vault CLI after enrolling in Vault — see [`03-security/secrets-management.md`](../03-security/secrets-management.md).

## 10. Local Environment Configuration

Most repositories provide a `Makefile` (or `taskfile`) with common targets. The standard convention:

```bash
# fictional/simulated
make help      # list available targets
make setup     # install dependencies, configure toolchain
make build     # build all artifacts
make test      # run unit + integration tests
make lint      # run linters
make fmt       # format code in place
make run       # run the service locally
make clean     # remove build artifacts
```

A canonical `setup` script will:

1. Create or activate the virtual environment (Python) or install npm packages (Node).
2. Fetch secrets from ACME Vault for local development credentials.
3. Run database migrations against a local containerized DB.
4. Print next steps.

If `make setup` fails, check the troubleshooting section below.

## 11. Running Unit Tests

The ACME convention for unit tests is to mirror the source layout. Tests are placed under `*_test.go` (Go), `tests/` directory with `test_*.py` files (Python), or `*.spec.ts` (TypeScript).

```bash
# fictional/simulated — Go
cd acme-cloud-api
go test ./... -race -cover

# fictional/simulated — Python
cd acme-intelligence-agents
pytest -n auto --cov=src --cov-report=term

# fictional/simulated — TypeScript
cd acme-cloud-frontend
pnpm test
```

Coverage thresholds are enforced in CI; see [`practices/unit-and-integration-testing.md`](./practices/unit-and-integration-testing.md) for the policy.

## 12. Troubleshooting Development Environments

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `git clone` fails with "Could not resolve host" | VPN not connected | Connect ACME VPN — see [`02-it/corporate-vpn-configuration.md`](../02-it/corporate-vpn-configuration.md). |
| `gh auth login` says "device flow timed out" | Corporate proxy blocking GitHub | Set `HTTPS_PROXY=http://proxy.acme.example:3128` (fictional). |
| `Permission denied (publickey)` from `git@git.acme.example` | SSH key not registered, or wrong key offered | Re-run `gh ssh-key add` and verify `ssh -T git@git.acme.example`. |
| `pip install` fails with "Could not fetch" | Internal registry URL not configured | Check `~/.pip/pip.conf` per section 5 above. |
| `npm install` installs from public npm instead of internal registry | npm scope misconfigured | Run `npm config set registry https://packages.acme.example/npm/`. |
| Docker Desktop: "no space left on device" | WSL2 disk image full | Run `wsl --shutdown` then `wsl --manage Ubuntu-24.04 --set-sparse` (Windows). |
| `make setup` fails fetching a secret | ACME Vault token expired | Re-run `vault login -method=oidc -path=oidc` (fictional). |
| VS Code Remote-WSL cannot connect | VS Code Server install failed in WSL | Open the WSL terminal in VS Code, run `rm -rf ~/.vscode-server`, retry. |
| `go test` fails with `module ... not found` | GOPRIVATE not set | `go env -w GOPRIVATE=git.acme.example/*`. |
| macOS: `zsh: command not found: gh` | Not in PATH | `echo 'export PATH="$PATH:/opt/homebrew/bin"' >> ~/.zshrc`. |

If none of the above resolves the issue:

1. Search the `#engineering-help` Teams channel.
2. Ask your onboarding buddy.
3. Open an IT Helpdesk ticket — see [`02-it/it-support-and-troubleshooting.md`](../02-it/it-support-and-troubleshooting.md).

## Related Documents

- [`04-engineering/ai-coding-assistant-setup.md`](./ai-coding-assistant-setup.md)
- [`04-engineering/source-code-and-repository-access.md`](./source-code-and-repository-access.md)
- [`04-engineering/repository-catalog.md`](./repository-catalog.md)
- [`04-engineering/practices/git-branching-strategy.md`](./practices/git-branching-strategy.md)
- [`04-engineering/practices/coding-standards.md`](./practices/coding-standards.md)
- [`04-engineering/practices/ci-cd-overview.md`](./practices/ci-cd-overview.md)
- [`04-engineering/practices/internal-package-management.md`](./practices/internal-package-management.md)
- [`04-engineering/practices/unit-and-integration-testing.md`](./practices/unit-and-integration-testing.md)
- [`02-it/windows-11-and-macos-workstation-setup.md`](../02-it/windows-11-and-macos-workstation-setup.md)
- [`02-it/microsoft-365-account-activation.md`](../02-it/microsoft-365-account-activation.md)
- [`02-it/corporate-vpn-configuration.md`](../02-it/corporate-vpn-configuration.md)
- [`02-it/password-manager-configuration.md`](../02-it/password-manager-configuration.md)
- [`02-it/approved-software-installation.md`](../02-it/approved-software-installation.md)
- [`03-security/source-code-security.md`](../03-security/source-code-security.md)
- [`03-security/secrets-management.md`](../03-security/secrets-management.md)
- [`03-security/ai-tool-acceptable-use.md`](../03-security/ai-tool-acceptable-use.md)
- [`08-forms/repository-access-request.md`](../08-forms/repository-access-request.md)
- [`05-teams/`](../05-teams/) (find your role-specific onboarding guide)
