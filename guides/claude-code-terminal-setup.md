# Claude Code Terminal Setup Guide

## Goal

This guide is for someone who needs Claude Code working in a terminal and may need help from IT to get there.

## What the User Needs

At minimum:

1. A supported terminal on macOS, Linux, or Windows with WSL
2. Git installed and usable from the command line
3. Node.js and `npm` available in the terminal
4. Access to the company GitHub org and the target repositories
5. Access to Claude Code under the company's approved licensing model
6. Network access that allows the CLI to authenticate and reach required services

## Basic Setup Flow

1. Confirm terminal access works.
2. Confirm `git --version` works.
3. Confirm `node --version` and `npm --version` work.
4. Install Claude Code using the approved internal method.
5. Authenticate with the required account.
6. Clone the target repo.
7. Launch Claude Code from inside the repo.

## Quick Verification Commands

```bash
git --version
node --version
npm --version
```

If any of these fail, stop and resolve that dependency first.

## Git Setup

### Verify

Run:

```bash
git --version
```

If that returns a version number, Git is available in terminal.

### What Good Looks Like

These commands should work:

```bash
git --version
git config --global user.name
git config --global user.email
```

### Configure Identity

If needed:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"
```

Check it:

```bash
git config --global --list
```

### Common Git Problems

#### `git: command not found`

Cause:

- Git is not installed or not on `PATH`

Action:

- Ask IT to install Git and ensure it is available from terminal

#### Git works in one terminal but not another

Cause:

- Shell profile or `PATH` is inconsistent

Action:

- Compare shell startup config and fix `PATH`

#### Git works for public repos but not company repos

Cause:

- Missing GitHub org access, SSO authorization, VPN, or credential setup

Action:

- Ask the GitHub admin or IT to confirm org membership and SSO access

## Node.js and npm Setup

### Verify

Run:

```bash
node --version
npm --version
```

If both return version numbers, Node.js and `npm` are available in terminal.

### What Good Looks Like

These commands should work:

```bash
node --version
npm --version
npm config get registry
```

### Common Node/npm Problems

#### `node: command not found`

Cause:

- Node.js is not installed or not on `PATH`

Action:

- Ask IT to install an approved Node.js version and expose it in terminal

#### `npm: command not found`

Cause:

- Broken or partial Node.js install

Action:

- Ask IT to repair the Node.js installation

#### `npm install` fails behind corporate network

Cause:

- Proxy, certificate, or registry restrictions

Action:

- Ask IT for the approved npm registry/proxy configuration and any required certificates

#### Wrong Node.js version

Cause:

- System version is too old or differs from team standard

Action:

- Ask IT what version is supported for development and install that version

## What to Ask IT For

If the user cannot get Claude Code working, ask IT or the endpoint/platform team for:

1. Permission to use a developer terminal on the machine
2. Installation or approval for Git
3. Installation or approval for Node.js and `npm`
4. Approval for the Claude Code CLI under company policy
5. Access to the correct GitHub organisation and repositories
6. Access to the secret manager or credential store used by engineering
7. VPN or SSO access if repo/authentication is blocked behind corporate access controls
8. Network allowlisting if the CLI cannot authenticate or download required packages

For Git and Node/npm specifically, ask IT for:

- Git installed and available on `PATH`
- Node.js installed and available on `PATH`
- `npm` installed and available on `PATH`
- Access to the approved npm/package registry
- Any proxy, certificate, SSO, or VPN setup needed for package installation and repo access

## Useful Details to Include in the IT Request

Provide:

- Operating system and version
- Terminal being used
- Whether `git`, `node`, and `npm` are already installed
- Exact error message
- Whether the failure is install-time, login-time, or repo-access-time
- Whether GitHub access works in the browser
- Whether VPN is connected

## Common Failure Modes

### `git` not found

Cause:

- Git is not installed or not on `PATH`

Action:

- Ask IT to install Git or fix the shell path

### `node` or `npm` not found

Cause:

- Node.js is missing or blocked

Action:

- Ask IT to install an approved Node.js version and ensure it is available in the shell

### Install blocked

Cause:

- Package installation is restricted by endpoint policy or proxy settings

Action:

- Ask IT for the approved install path or for package/network allowlisting

### Login/authentication fails

Cause:

- Missing license/access, blocked browser auth flow, or network restrictions

Action:

- Confirm the user has been provisioned for Claude Code and that browser/device-code login is allowed

### Repo access fails

Cause:

- Missing GitHub org membership, missing repo permissions, or SSO/VPN issue

Action:

- Ask IT or the GitHub org admin to verify org membership, team membership, and SSO authorization

## Suggested IT Request Template

```text
I need Claude Code working in terminal for product development.

Please help me with:
- Git installed and available on PATH
- Node.js and npm installed and available on PATH
- Approval/access for Claude Code
- Access to the required GitHub org/repositories
- Any VPN, SSO, proxy, or network allowlisting needed for CLI authentication and package download

Current machine:
- OS:
- Terminal:

Current issue:
- Exact error:
- What I have already tested:
```

## Team-Level Recommendation

If multiple people need this, do not solve it one laptop at a time. Ask IT/platform to publish:

1. A standard install method
2. A supported Node.js version
3. A one-page access checklist
4. A named support contact for licensing and network issues
