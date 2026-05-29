#!/usr/bin/env python3
"""Small state manager for Web Audit Squad audit Markdown files."""
from __future__ import annotations

import argparse
import re
import time
from pathlib import Path

BACKLOG_TEMPLATE = """# Web Audit Squad backlog

## P0 — shipping blockers
| Status | Page | Item | Evidence | Fix direction | Verify |
|---|---|---|---|---|---|

## P1 — important fixes
| Status | Page | Item | Evidence | Fix direction | Verify |
|---|---|---|---|---|---|

## P2 — upside / polish
| Status | Page | Item | Evidence | Fix direction | Verify |
|---|---|---|---|---|---|
"""

CURRENT_TEMPLATE = """# Current state

- Last updated: {now}
- Current focus: initialized
- Audit mode: audit-only unless implementation is explicitly requested
- Known stack: unknown
- Routes mapped: 0
- Pages audited: 0
- Open P0: unknown
- Open P1: unknown
- Open P2: unknown

## Next best action
Run scout and update WEB_STRUCTURE.md.

## Open unknowns
- Build command
- Runtime command
- Auth/database/storage/payment boundaries
"""

WEB_TEMPLATE = """# Web structure

Run scout to populate this file:

```bash
python3 .claude/skills/web-audit-squad/scripts/scout.py --root . --out-dir .claude/web-audit-squad
```
"""

DECISIONS_TEMPLATE = """# Web Audit Squad decisions

| Date | Page | Decision | Reason | Risk |
|---|---|---|---|---|
"""


def workspace(root: Path) -> Path:
    return root / '.claude' / 'web-audit-squad'


def esc(s: str) -> str:
    return s.replace('|', '\\|').replace('\n', ' ')


def init(root: Path) -> None:
    ws = workspace(root)
    (ws / 'PAGE_AUDITS').mkdir(parents=True, exist_ok=True)
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    files = {
        'CURRENT_STATE.md': CURRENT_TEMPLATE.format(now=now),
        'WEB_STRUCTURE.md': WEB_TEMPLATE,
        'BACKLOG.md': BACKLOG_TEMPLATE,
        'DECISIONS.md': DECISIONS_TEMPLATE,
    }
    for name, content in files.items():
        path = ws / name
        if not path.exists():
            path.write_text(content, encoding='utf-8')
    print(f'Initialized {ws}')


def add_backlog(root: Path, severity: str, page: str, title: str, source: str, notes: str, fix: str, verify: str) -> None:
    init(root)
    path = workspace(root) / 'BACKLOG.md'
    text = path.read_text(encoding='utf-8')
    sev = severity.upper()
    heading = {'P0': '## P0', 'P1': '## P1', 'P2': '## P2'}.get(sev[:2], '## P2')
    row = f'| open | {esc(page)} | {esc(title)} | {esc(source + (": " + notes if notes else ""))} | {esc(fix)} | {esc(verify)} |\n'
    pos = text.find(heading)
    if pos == -1:
        text += f'\n## {sev}\n| Status | Page | Item | Evidence | Fix direction | Verify |\n|---|---|---|---|---|---|\n{row}'
    else:
        next_heading = text.find('\n## ', pos + 1)
        insert_at = next_heading if next_heading != -1 else len(text)
        section = text[pos:insert_at]
        lines = section.splitlines(True)
        insert_line = len(lines)
        for i, line in enumerate(lines):
            if line.startswith('|---'):
                insert_line = i + 1
                break
        new_section = ''.join(lines[:insert_line]) + row + ''.join(lines[insert_line:])
        text = text[:pos] + new_section + text[insert_at:]
    path.write_text(text, encoding='utf-8')
    print(f'Added {sev} backlog item to {path}')


def set_focus(root: Path, focus: str) -> None:
    init(root)
    path = workspace(root) / 'CURRENT_STATE.md'
    text = path.read_text(encoding='utf-8')
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    text = re.sub(r'- Last updated:.*', f'- Last updated: {now}', text)
    text = re.sub(r'- Current focus:.*', f'- Current focus: {focus}', text)
    path.write_text(text, encoding='utf-8')
    print(f'Updated focus in {path}')


def page_path(root: Path, route: str) -> Path:
    safe = route.strip('/').replace('/', '__') or 'home'
    safe = re.sub(r'[^A-Za-z0-9_.-]+', '-', safe)
    return workspace(root) / 'PAGE_AUDITS' / f'{safe}.md'


def new_page(root: Path, route: str, title: str = '') -> None:
    init(root)
    p = page_path(root, route)
    if not p.exists():
        label = title or route
        p.write_text(f'# {label} audit\n\nRoute: `{route}`\n\n## Current job\n\n## Findings\n\n## Fix plan\n\n## Regression checklist\n', encoding='utf-8')
    print(p)


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)

    p_init = sub.add_parser('init')
    p_init.add_argument('--root', default='.')

    p_focus = sub.add_parser('set-focus')
    p_focus.add_argument('--root', default='.')
    p_focus.add_argument('--focus', required=True)

    p_page = sub.add_parser('new-page')
    p_page.add_argument('--root', default='.')
    p_page.add_argument('--route', required=True)
    p_page.add_argument('--title', default='')

    p_backlog = sub.add_parser('add-backlog')
    p_backlog.add_argument('--root', default='.')
    p_backlog.add_argument('--severity', required=True)
    p_backlog.add_argument('--page', required=True)
    p_backlog.add_argument('--title', required=True)
    p_backlog.add_argument('--source', default='')
    p_backlog.add_argument('--notes', default='')
    p_backlog.add_argument('--fix', default='')
    p_backlog.add_argument('--verify', default='')

    args = ap.parse_args()
    root = Path(args.root).resolve()
    if args.cmd == 'init':
        init(root)
    elif args.cmd == 'set-focus':
        set_focus(root, args.focus)
    elif args.cmd == 'new-page':
        new_page(root, args.route, args.title)
    elif args.cmd == 'add-backlog':
        add_backlog(root, args.severity, args.page, args.title, args.source, args.notes, args.fix, args.verify)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
