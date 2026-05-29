# Web Audit Squad

A token-light Claude Code skill pack for auditing a web app page-by-page with seven specialized subagents.

It creates a durable audit workspace, maps your web structure, checks links/actions, and produces backend/security/UI/UX/performance fix plans without randomly redesigning working flows.

## What it installs

```text
.claude/
  skills/web-audit-squad/SKILL.md
  skills/web-audit-squad/scripts/scout.py
  skills/web-audit-squad/scripts/state.py
  skills/web-audit-squad/references/...
  agents/web-db-security-performance.md
  agents/web-uiux-performance-designer.md
  agents/web-heuristics-guardian.md
  agents/web-contrarian-auditor.md
  agents/web-expansionist.md
  agents/web-first-principles.md
  agents/web-page-executor.md
```

## Why this version is optimized

- Manual invocation only: the skill uses `disable-model-invocation: true`, so it does not sit in Claude's normal context unless you run it.
- Scout-first workflow: a small Python scanner builds `WEB_STRUCTURE.md` and `CURRENT_STATE.md` before any agent reads files.
- Small delegation packets: agents receive the route, relevant files, and known issues, not the whole repository.
- Read-only subagents: all seven specialists are blocked from editing by tool allowlists.
- Durable state: audit work is written into `.claude/web-audit-squad/` so Claude does not need to rediscover the same structure every session.
- Page-by-page backlog: every page plan becomes P0/P1/P2 work, with evidence and verification steps.

## Install into a project

From the target project root:

```bash
curl -L -o web-audit-squad.zip https://github.com/YOUR_GITHUB_USERNAME/web-audit-squad/releases/latest/download/web-audit-squad.zip
unzip -o web-audit-squad.zip
```

Or from a local checkout of this repository:

```bash
./install.sh /path/to/your/web-app
```

Restart Claude Code after installing, because file-based subagents are loaded at session start.

## Use

In Claude Code, from your web app root:

```text
/web-audit-squad init
/web-audit-squad map
/web-audit-squad audit priority pages
/web-audit-squad page /pricing
```

Typical first run:

```text
/web-audit-squad init and map this project. Then audit the landing page first, but only create a plan, do not edit product code.
```

## Generated audit workspace

The skill creates or updates:

```text
.claude/web-audit-squad/
  CURRENT_STATE.md
  WEB_STRUCTURE.md
  BACKLOG.md
  DECISIONS.md
  SCOUT.json
  PAGE_AUDITS/
```

## Commands outside Claude Code

Run the scout manually:

```bash
python3 .claude/skills/web-audit-squad/scripts/scout.py --root . --out-dir .claude/web-audit-squad
```

Initialize state files manually:

```bash
python3 .claude/skills/web-audit-squad/scripts/state.py init --root .
```

Add a backlog item manually:

```bash
python3 .claude/skills/web-audit-squad/scripts/state.py add-backlog --root . --severity P1 --page /pricing --title "Pricing CTA href points to missing route" --source "app/pricing/page.tsx" --notes "Verify after route map update."
```

## Safety model

This pack is audit-first. It should not edit application code unless you explicitly ask Claude to implement a fix. Subagents are read-only reviewers; the main Claude session may update audit `.md` files when you ask it to persist state.

## License

MIT.
