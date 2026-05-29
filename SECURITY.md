# Security Policy

This repository contains instructions and local helper scripts for Claude Code. Treat every skill, agent, hook, and script as executable project tooling.

## Security principles

- Do not grant broad `allowed-tools` permissions unless you have reviewed the skill.
- Do not put real secrets in examples, screenshots, issues, or test fixtures.
- The included secret scanner redacts values and reports only path/line/pattern.
- Subagents are read-only by default and should not receive Write/Edit tools.
- Keep generated audit outputs private if they include sensitive route names, environment variable names, or security findings.

## Reporting

Open a private advisory or contact the repository owner if you find a dangerous prompt, unsafe command, or secret-exposing behavior.
