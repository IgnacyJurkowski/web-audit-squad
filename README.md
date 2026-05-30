# Web Audit Squad

A token-light Claude Code skill that audits a web app page-by-page with seven specialized subagents: security/DB, UX, Nielsen heuristics, contrarian, expansionist, first-principles, and implementation planner.

It creates a durable audit workspace, maps your route structure, checks links/actions/secrets, and produces actionable P0/P1/P2 fix plans — without randomly redesigning working flows.

## Install

From your web app root:

```bash
curl -L -o web-audit-squad.zip https://github.com/IgnacyJurkowski/web-audit-squad/releases/latest/download/web-audit-squad.zip
unzip -o web-audit-squad.zip
```

Or from a local checkout of this repository:

```bash
./install.sh /path/to/your/web-app
```

**Restart Claude Code after installing.** File-based subagents load at session start.

## Quick start

> **Note**: This skill must be invoked as a slash command typed by you:
> ```
> /web-audit-squad page /pricing
> ```
> Claude cannot invoke it on your behalf via the Skill tool — you must type the command yourself. This is intentional: `disable-model-invocation: true` keeps the skill out of Claude's normal context until you explicitly call it.

In Claude Code, from your web app root:

```text
/web-audit-squad init and map this project. Then audit the landing page and auth flow in priority order. Audit-only: update audit docs, do not edit app code.
```

Common follow-up commands:

| Command | What it does |
|---|---|
| `/web-audit-squad init` | Create the audit workspace |
| `/web-audit-squad map` | Scan routes, links, and secrets; write `WEB_STRUCTURE.md` |
| `/web-audit-squad audit` | Map first, then audit priority pages one by one |
| `/web-audit-squad page /pricing` | Full seven-agent audit of one specific route |
| `/web-audit-squad backlog` | Show P0/P1/P2 queue and next execution order |
| `/web-audit-squad status` | Progress table: pages audited / in-progress / queued with P0/P1/P2 counts |
| `/web-audit-squad implement-plan A-001,A-002` | Implement specific backlog items by ID (requires explicit approval) |

See `examples/audit-session.md` for a realistic session walkthrough with expected outputs.

## The seven agents

Each page audit dispatches all seven subagents in parallel. Each is read-only and returns a compact table plus top-3 recommendations.

| Agent | Focus | Model |
|---|---|---|
| `web-db-security-performance` | Secrets, RLS, SQL injection, N+1 queries, storage exposure | Sonnet |
| `web-uiux-performance-designer` | CTA hierarchy, accessibility, perceived performance, copy trust | Sonnet |
| `web-heuristics-guardian` | Nielsen's 10 heuristics — names the violation, gives two fixes | Haiku |
| `web-contrarian-auditor` | Dead buttons, broken flows, placeholder copy, no-op forms | Sonnet |
| `web-expansionist` | Conversion, SEO/GEO, onboarding, pricing upside | Haiku |
| `web-first-principles` | Solves the right problem? What to keep unchanged? | Haiku |
| `web-page-executor` | Ordered implementation plan with acceptance criteria and rollback | Sonnet |

See `.claude/skills/web-audit-squad/references/agents.md` for each agent's full output format and conflict resolution rules.

## Severity levels

- **P0** — shipping blocker: exposed secret, auth/payment breakage, data leak, dead primary CTA, destructive bug.
- **P1** — serious issue likely to hurt users or operations: speed, trust, conversion, maintainability.
- **P2** — polish and upside: lower-risk optimizations, SEO improvements, onboarding gaps.

## Audit workspace

The skill creates and maintains these files inside your project:

```text
.claude/web-audit-squad/
  CURRENT_STATE.md      — current focus, last run, open unknowns
  WEB_STRUCTURE.md      — route graph, CTAs, suspicious links, secret hints
  BACKLOG.md            — P0/P1/P2 queue with evidence and verification steps
  DECISIONS.md          — why things were changed, kept, or removed
  SCOUT.json            — machine-readable scout output
  PAGE_AUDITS/          — one Markdown file per audited page
```

## Why this is token-light

- **Manual invocation only:** `disable-model-invocation: true` keeps the skill out of Claude's normal context unless you invoke it.
- **Scout-first workflow:** a Python scanner builds `WEB_STRUCTURE.md` before any agent reads files, so agents never scan the whole repo.
- **Small delegation packets:** agents receive only the route, relevant files, known links/actions, and known risks — not the entire codebase.
- **Read-only subagents:** all seven specialists are blocked from editing product code by tool allowlists.
- **Durable state:** audit work is written to `.claude/web-audit-squad/` so Claude does not rediscover structure across sessions.

## What it installs

```text
.claude/
  skills/web-audit-squad/SKILL.md
  skills/web-audit-squad/scripts/scout.py
  skills/web-audit-squad/scripts/state.py
  skills/web-audit-squad/references/agents.md
  skills/web-audit-squad/references/protocol.md
  skills/web-audit-squad/references/token-budget.md
  skills/web-audit-squad/references/templates/
  agents/web-db-security-performance.md
  agents/web-uiux-performance-designer.md
  agents/web-heuristics-guardian.md
  agents/web-contrarian-auditor.md
  agents/web-expansionist.md
  agents/web-first-principles.md
  agents/web-page-executor.md
```

## Supported frameworks

Scout infers routes from Next.js App Router, Next.js Pages Router, and any framework with an `app/` or `pages/` directory. It detects React, Supabase, Stripe, Prisma, Drizzle, Tailwind, and Zod from `package.json` dependencies.

## Manual commands

Run the scout directly:

```bash
python3 .claude/skills/web-audit-squad/scripts/scout.py --root . --out-dir .claude/web-audit-squad
```

Initialize state files:

```bash
python3 .claude/skills/web-audit-squad/scripts/state.py init --root .
```

Add a backlog item:

```bash
python3 .claude/skills/web-audit-squad/scripts/state.py add-backlog \
  --root . --severity P1 --page /pricing \
  --title "Pricing CTA href points to missing route" \
  --source "app/pricing/page.tsx" \
  --notes "Verify after route map update."
```

## Safety

Audit-only by default. Subagents are read-only reviewers. The main Claude session may update `.claude/web-audit-squad/*.md` audit files when asked. Product code is only touched when you explicitly invoke `implement-plan`.

## License

MIT.
