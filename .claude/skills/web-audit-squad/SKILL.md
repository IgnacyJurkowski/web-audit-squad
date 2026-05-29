---
name: web-audit-squad
description: Use when auditing a web app for security holes, broken flows, UX problems, performance issues, or revenue opportunities. Dispatches seven specialized subagents in parallel. Works with Next.js, React, Vue, Svelte, and similar frameworks.
disable-model-invocation: true
argument-hint: "init | map | audit [scope] | page [route] | backlog | implement-plan"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Agent(web-db-security-performance,web-uiux-performance-designer,web-heuristics-guardian,web-contrarian-auditor,web-expansionist,web-first-principles,web-page-executor)
  - Bash(python3 .claude/skills/web-audit-squad/scripts/scout.py *)
  - Bash(python3 .claude/skills/web-audit-squad/scripts/state.py *)
---

# Web Audit Squad

Run the workflow requested in `$ARGUMENTS`.

Default: **audit, document, and plan only**. Do not edit product code unless the user explicitly asks for implementation. Updating `.claude/web-audit-squad/*.md` audit files is allowed when the user asks for state/backlog/doc updates.

## Quick start

Typical first session:
```text
/web-audit-squad init and map this project. Then audit the landing page and auth flow in priority order. Audit-only: update audit docs, do not edit app code.
```

Common follow-ups:
```text
/web-audit-squad page /pricing
/web-audit-squad backlog
/web-audit-squad implement-plan
```

## Commands

| Command | What it does |
|---|---|
| `init` | Create `.claude/web-audit-squad/` state files |
| `map` | Run scout, refresh `WEB_STRUCTURE.md` and `CURRENT_STATE.md` |
| `audit [scope]` | Map if needed, rank pages, audit priority pages one by one |
| `page <route>` | Full seven-agent audit of one route/page |
| `backlog` | Summarize P0/P1/P2 queue and next execution order |
| `implement-plan` | Implement an accepted plan (requires explicit user approval) |

## Token-light protocol

1. Never read the whole repository. Start with:
   ```bash
   python3 .claude/skills/web-audit-squad/scripts/state.py init --root .
   python3 .claude/skills/web-audit-squad/scripts/scout.py --root . --out-dir .claude/web-audit-squad
   ```
2. Read `SCOUT.json`, `WEB_STRUCTURE.md`, `CURRENT_STATE.md`, and only the files for the current page.
3. Keep each subagent packet under 400 words. Include only route, goal, relevant files, known links/actions, and known risks.
4. Ask each subagent for max 8 findings. No long code excerpts. Use paths/line numbers instead.
5. Audit one page/flow at a time. Do not run all pages through all agents in one giant pass.
6. Persist durable facts in `.claude/web-audit-squad/`; do not rely on chat memory.

## Persistent audit workspace

Maintain:

```text
.claude/web-audit-squad/
  CURRENT_STATE.md      # What we know now, current focus, last run
  WEB_STRUCTURE.md      # route graph, nav, CTAs, links/actions
  BACKLOG.md            # P0/P1/P2 work queue with evidence + verification
  DECISIONS.md          # why we changed/kept/removed things
  SCOUT.json            # machine-readable scout output
  PAGE_AUDITS/          # one file per audited page
```

Update `WEB_STRUCTURE.md` before page-level opinions. Update `BACKLOG.md` after every page synthesis.

## Workflow

### Phase 0 — setup

Run `state.py init` if the audit workspace does not exist. Then run `scout.py`.

### Phase 1 — current state and web structure

Build or refresh:
- stack summary;
- route inventory;
- global nav/footer/sidebar links;
- CTA targets and form actions;
- broken/suspicious links/actions;
- data/API/storage/payment dependencies;
- page priority queue.

### Phase 2 — choose pages

Prioritize pages by business/risk impact:
1. Revenue/payment/auth/core product routes.
2. Landing, pricing, signup, onboarding, public booking/demo pages.
3. Dashboard/admin/settings/data-heavy pages.
4. Support/legal/static pages.

### Phase 3 — seven-agent review

For each selected page, dispatch all seven subagents in parallel when Claude Code supports it. If the runtime serializes calls, still keep each agent in its own context.

Agent names and focus — see `references/agents.md` for full output formats:
- `web-db-security-performance` — secrets, RLS, SQL injection, N+1 queries, storage exposure
- `web-uiux-performance-designer` — UX, CTAs, accessibility, perceived performance
- `web-heuristics-guardian` — Nielsen's 10 heuristics, names violations, two fixes each
- `web-contrarian-auditor` — fatal flaws, dead buttons, broken flows, no-op forms
- `web-expansionist` — conversion, SEO/GEO, onboarding, pricing upside
- `web-first-principles` — solves the right problem? what to keep unchanged?
- `web-page-executor` — ordered implementation plan with acceptance criteria and rollback

Delegation packet:

```text
Scope: <route/page/flow>
Business goal: <one sentence>
User job: <one sentence>
Source files to inspect: <short list>
Known routes/links/actions: <short list from WEB_STRUCTURE.md>
Known stack/data dependencies: <short list>
Constraints: audit-only, max 8 findings, evidence required, no product-code edits.
Return: only your role-specific table plus top 3 recommendations.
```

### Phase 4 — UI/UX correction loop

1. UI/UX Expert 1 proposes improvements.
2. Heuristics Guardian checks those proposals against Nielsen's 10 heuristics.
3. If a violation exists, record heuristic, breakage, two fixes, and chosen option.
4. UI/UX Expert 1's final recommendation must use the chosen option.

### Phase 5 — synthesis and backlog

Merge the agent results into:
- P0 shipping blockers/security risks;
- P1 speed, trust, conversion, maintainability issues;
- P2 polish/upside;
- exact implementation order;
- regression checks;
- rollback notes.

Persist page output to `PAGE_AUDITS/<safe-route-name>.md` when asked to update docs. Add accepted items to `BACKLOG.md`.

## Output contract

For each page:

```md
# <Page/route> audit

## Current job
- User:
- Business:
- Keep stable:

## Route/link/action status
| Item | Source | Target | Status | Severity | Evidence |
|---|---|---|---|---|---|

## Seven-agent synthesis
| Agent | Highest-risk finding | Best opportunity | Evidence | Recommendation |
|---|---|---|---|---|

## Nielsen correction loop
| UX proposal | Heuristic issue | Fix A | Fix B | Chosen |
|---|---|---|---|---|

## Fix plan
### P0
### P1
### P2

## Implementation order
| Step | File/route | Change | Risk | Verification |
|---|---|---|---|---|

## Regression checklist
- [ ] desktop/mobile
- [ ] links/routes
- [ ] forms/buttons
- [ ] loading/empty/error states
- [ ] auth/user states
- [ ] data/API/storage/payment boundaries
- [ ] performance smoke check
```

## Decision rules

- Do not redesign because of taste. Fix user friction, risk, speed, broken flows, or business clarity.
- Protect working flows. Prefer reversible changes.
- If evidence is missing, say `unknown` and define the check.
- Fatal flaws beat upside. First principles beat expansion. Heuristics guardian can veto UX ideas that break usability.
- Backlog items require severity, page, evidence, fix direction, and verification.

See `references/protocol.md` for the complete standards.
