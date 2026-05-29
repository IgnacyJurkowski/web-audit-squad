# Changelog

## 2.1.0

- Fixed SKILL.md description: was a workflow summary (CSO anti-pattern); now uses "Use when..." triggering conditions so Claude reads the skill body instead of short-circuiting on the description.
- Added Commands table to SKILL.md for at-a-glance reference.
- Added Quick start block to SKILL.md.
- Added `references/agents.md`: progressive-disclosure file with each agent's focus, output format, and conflict resolution rules — loaded on demand rather than polluting the main skill context.
- Added `examples/audit-session.md`: realistic session walkthrough covering init/map, single-page deep-dive, scope narrowing, backlog review, and implement-plan.
- Rewrote README.md: added agent roles table, severity legend, supported frameworks section, "Why token-light" explanation, and links to new reference files.

## 2.0.0

- Added manual-only invocation to reduce ambient context usage.
- Added durable audit workspace: `CURRENT_STATE.md`, `WEB_STRUCTURE.md`, `BACKLOG.md`, `DECISIONS.md`, and `PAGE_AUDITS/`.
- Added `scout.py` for token-light route/link/security discovery.
- Added `state.py` for audit state initialization and backlog maintenance.
- Tightened subagent prompts, models, turn limits, and tool access.
- Added GitHub-ready README, install script, contribution notes, and setup docs.
