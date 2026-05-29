# Typical audit session

A walkthrough of a realistic audit, showing prompts and what to expect at each step.

---

## Session 1: init, map, and first audit

**Prompt:**
```text
/web-audit-squad init and map this project. Then audit the landing page and auth flow in priority order. Audit-only: update audit docs, do not edit app code.
```

**What happens:**
1. `state.py init` creates `.claude/web-audit-squad/` with empty workspace files.
2. `scout.py` scans the project and writes `SCOUT.json`, `WEB_STRUCTURE.md`, `CURRENT_STATE.md`.
3. Pages are ranked by priority (payment/auth first, then landing/pricing/onboarding, then dashboard/settings).
4. Seven agents audit the landing page in parallel, each returning a compact table.
5. Results are synthesized into `PAGE_AUDITS/home.md` and `BACKLOG.md`.
6. Auth flow is audited next.

**Expected output includes:**
- Route inventory with priority scores
- Suspicious links and placeholder targets flagged by scout
- Potential secret references (values redacted) flagged by scout
- P0/P1/P2 findings from each agent per page
- A fix plan with implementation order and regression checklist

---

## Session 2: single page deep-dive

**Prompt:**
```text
/web-audit-squad page /pricing
```

Audits only `/pricing` with all seven agents. Good for:
- Following up on a specific page before shipping a change
- Auditing a newly added page
- Re-auditing after a major change

---

## Session 3: scope-narrowed audit

For large pages (checkout, dashboard) with many components:

**Prompt:**
```text
/web-audit-squad page /checkout — focus on the payment step and form validation only
```

Narrowing scope keeps agent packets small and findings sharp.

---

## Session 4: check the backlog

**Prompt:**
```text
/web-audit-squad backlog
```

Returns the current P0/P1/P2 queue sorted by severity and page, with evidence and verification steps. Use before planning a sprint.

---

## Session 5: implement

After reviewing the backlog and explicitly approving a plan:

**Prompt:**
```text
/web-audit-squad implement-plan

Implement only the P0 items from the /pricing audit. Create a commit for each fix.
```

The skill will not touch product code unless you explicitly ask. `implement-plan` is the only mode that unlocks code edits. Normal Claude Code safeguards apply (reversibility, blast-radius checks, no force-push).

---

## Tips

**One page per session beats a full sweep.** The backlog accumulates across sessions; you do not need to audit everything at once.

**Use `backlog` before sprint planning.** It gives you a prioritized queue with evidence and verification steps — better input than loose notes.

**Trust the conflict resolution order.** Security P0 beats everything. Contrarian blockers beat expansion ideas. First-principles can freeze a working area. Override these only with a documented decision in `DECISIONS.md`.

**Restart Claude Code after installing.** File-based subagents load at session start. If agents are missing, restart and try again.

**Re-map after big structural changes.** Run `/web-audit-squad map` whenever routes, nav, or CTAs change significantly. The workspace files are the agents' source of truth.
