# Web Audit Squad — UI Dashboard

> **Status: Visual demo only.** All data is hardcoded. The progress bars, phase highlights, P0/P1/P2 counts, and agent cards do not reflect a live audit run.
> To connect it to real data, see "Connecting to real audit output" below.

## Open it

```bash
open .claude/skills/web-audit-squad/ui/dashboard.html
```

Or serve it locally:
```bash
python3 -m http.server 8099 --directory .claude/skills/web-audit-squad/ui
# then open http://localhost:8099/dashboard.html
```

## What the demo shows

| Element | Description |
|---|---|
| Phase track | Six phases from setup → synthesis (hardcoded highlight) |
| Agent grid | Seven agent cards with simulated progress bars and status badges |
| Stats row | Hardcoded P0 / P1 / P2 / repair counts |
| Inspector panel | Click any agent or finding to see detail (static data) |
| Repair log | Simulated fault-injection and self-repair log |

## Self-repair demo

1. Click **▶ Run audit** to start the simulation
2. Click **⚡ Inject fault** at any time to stage a failure on an upcoming agent
3. Watch the simulated agent hit the error, log it, then recover
4. The repair count increments and the badge turns gold (repaired)

## Connecting to real audit output

To connect the dashboard to a live audit, edit the `FINDINGS` object in `dashboard.html` to read from `../PAGE_AUDITS/*.md` via a local fetch, or run a small Python server that reads BACKLOG.md and pipes P0/P1/P2 counts into that object:

```python
# minimal example — serve BACKLOG.md counts as JSON
import json, re, http.server, pathlib

def count_priorities(path):
    text = pathlib.Path(path).read_text()
    return {p: text.count(f"**Priority**: {p}") for p in ("P0", "P1", "P2")}

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        data = count_priorities(".claude/web-audit-squad/BACKLOG.md")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

http.server.HTTPServer(("", 8100), Handler).serve_forever()
```

Then in `dashboard.html`, replace the hardcoded `FINDINGS` object with a `fetch("http://localhost:8100")` call.
