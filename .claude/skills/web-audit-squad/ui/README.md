# Web Audit Squad — UI Dashboard

A standalone HTML dashboard that visualises the seven-agent audit workflow in real time.

## Open it

```bash
open .claude/skills/web-audit-squad/ui/dashboard.html
```

Or serve it locally:
```bash
python3 -m http.server 8099 --directory .claude/skills/web-audit-squad/ui
# then open http://localhost:8099/dashboard.html
```

## What it shows

| Element | Description |
|---|---|
| Phase track | Six phases from setup → synthesis, live-highlighted |
| Agent grid | Seven agent cards with live progress bars, status badges, and findings |
| Stats row | Live P0 / P1 / P2 / repair counts |
| Inspector panel | Click any agent or finding to see detail |
| Repair log | Timestamped log of every event, error, and self-repair |

## Self-repair demo

1. Click **▶ Run audit** to start
2. Click **⚡ Inject fault** at any time to stage a failure on an upcoming agent
3. Watch the agent hit the error, log it, then recover automatically
4. The repair count increments and the badge turns gold (repaired)

## Connecting to real audit output

The dashboard is currently a visual demo. To connect it to live audit runs, edit the `FINDINGS` object in `dashboard.html` to read from `../PAGE_AUDITS/*.md` via a local fetch, or pipe `BACKLOG.md` items into it via a small Python server.
