# Audit protocol standards

## Severity definitions
| Level | Meaning | Default priority |
|---|---|---|
| critical | Data loss, auth bypass, payment failure, security breach | P0 |
| high | Broken flow, inaccessible feature, significant conversion drop | P0–P1 |
| medium | UX friction, performance issue, missed opportunity | P1–P2 |
| low | Polish, minor copy, micro-optimisation | P2 |

## Evidence requirements
Every finding must cite at least one of:
- `file:line` reference
- Observed browser behaviour (describe exactly)
- Network/API response (status code + endpoint)
- `unknown` — if evidence cannot be obtained statically, define the manual check needed

## Backlog item lifecycle
`open` → `accepted` (user approves) → `done` (verified) | `wont-fix` (user rejects with reason)

`open` → `needs-verification` (finding is disputed or cannot be confirmed statically — requires a manual check before acting on it)

Items may not move from `open` to `done` without passing through `accepted`.
Items in `needs-verification` must have a defined manual check in the Evidence field before they can move to `accepted` or `wont-fix`.

## Implement-plan guard
Before any product-code edit, the orchestrator must:
1. Print the confirmation prompt defined in the Commands table.
2. Receive the exact word `CONFIRM` from the user.
3. Log the confirmation timestamp and item count in `DECISIONS.md`.

## Audit-only mode
Default mode. The orchestrator and all subagents may:
- Read any file
- Write to `.claude/web-audit-squad/` only
- Run `scout.py` and `state.py`

They must not:
- Edit product source files
- Run `npm install`, `git commit`, migrations, or deploys
- Delete files outside the audit workspace

## Loop control
After completing Phase 5 for a page:
1. Update `BACKLOG.md` and `CURRENT_STATE.md`.
2. Print a one-line summary: "Page `<route>` complete. P0: N, P1: N, P2: N. Next in queue: `<route>` — run `/web-audit-squad page <route>` to continue."
3. Stop. Do not auto-advance to the next page without a user command.
