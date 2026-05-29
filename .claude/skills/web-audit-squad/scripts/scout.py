#!/usr/bin/env python3
"""Token-light project scout for the Web Audit Squad Claude Code skill.

Outputs compact Markdown and JSON into `.claude/web-audit-squad/` by default.
No third-party dependencies.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

SOURCE_EXTS = {'.tsx', '.jsx', '.ts', '.js', '.mjs', '.cjs', '.html', '.md', '.mdx', '.vue', '.svelte'}
ROUTE_EXTS = {'.tsx', '.jsx', '.ts', '.js', '.mdx'}
SKIP_DIRS = {'node_modules', '.next', 'dist', 'build', '.git', '.claude', 'coverage', '.turbo', '.cache', 'vendor', '.venv'}
MAX_FILE_BYTES = 700_000

LINK_PATTERNS = [
    re.compile(r"href\s*=\s*[\"']([^\"']*)[\"']"),
    re.compile(r"to\s*=\s*[\"']([^\"']*)[\"']"),
    re.compile(r"router\.push\(\s*[\"']([^\"']*)[\"']\s*\)"),
    re.compile(r"redirect\(\s*[\"']([^\"']*)[\"']\s*\)"),
    re.compile(r"window\.location(?:\.href)?\s*=\s*[\"']([^\"']*)[\"']"),
]
BAD_TARGET_RE = re.compile(r"^(#|javascript:|void\(0\)|todo|tbd|null|undefined)?$", re.I)
TODO_RE = re.compile(r"\b(TODO|FIXME|PLACEHOLDER|COMING SOON|LOREM IPSUM)\b", re.I)
CLIENT_RE = re.compile(r"^[\s;]*['\"]use client['\"]", re.M)
FORM_RE = re.compile(r"<(form|button|input)|onSubmit\s*=|action\s*=|type\s*=\s*[\"']submit", re.I)
SECRET_PATTERNS = {
    'supabase-service-role': re.compile(r"SUPABASE_SERVICE_ROLE|service[_-]?role", re.I),
    'database-url': re.compile(r"DATABASE_URL|POSTGRES_URL|postgres(?:ql)?://", re.I),
    'aws-secret': re.compile(r"AWS_SECRET_ACCESS_KEY|AWS_ACCESS_KEY_ID", re.I),
    'private-key': re.compile(r"BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY", re.I),
    'payment-secret': re.compile(r"STRIPE_SECRET|P24|PRZELEWY24|PAYMENT_SECRET", re.I),
    'generic-secret': re.compile(r"\b(API[_-]?KEY|SECRET[_-]?KEY|ACCESS[_-]?TOKEN|AUTH[_-]?TOKEN|PASSWORD)\b\s*[:=]", re.I),
}

@dataclass
class Route:
    route: str
    source: str
    kind: str
    dynamic: bool
    priority_hint: int

@dataclass
class LinkFinding:
    severity: str
    source: str
    target: str
    kind: str
    line: int
    note: str

@dataclass
class SecretFinding:
    severity: str
    source: str
    line: int
    pattern: str
    note: str

@dataclass
class FileSignal:
    source: str
    lines: int
    bytes: int
    client_component: bool
    has_form: bool
    todos: int


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def iter_files(root: Path) -> Iterable[Path]:
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            p = Path(dirpath) / filename
            if p.suffix in SOURCE_EXTS and p.stat().st_size <= MAX_FILE_BYTES:
                yield p


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='ignore')


def route_from_app_file(app: Path, file: Path) -> str:
    parent = file.parent.relative_to(app)
    parts: list[str] = []
    for part in parent.parts:
        if part == '.':
            continue
        if part.startswith('(') and part.endswith(')'):
            continue
        if part.startswith('@'):
            continue
        if part.startswith('[[...') and part.endswith(']]'):
            parts.append('*')
        elif part.startswith('[...') and part.endswith(']'):
            parts.append('*')
        elif part.startswith('[') and part.endswith(']'):
            parts.append(':' + part[1:-1])
        else:
            parts.append(part)
    return ('/' + '/'.join(parts)).rstrip('/') or '/'


def route_from_pages_file(pages: Path, file: Path) -> str:
    no_suffix = file.relative_to(pages).with_suffix('')
    parts: list[str] = []
    for part in no_suffix.parts:
        if part == 'index':
            continue
        if part.startswith('[') and part.endswith(']'):
            parts.append(':' + part.strip('[]').lstrip('...'))
        else:
            parts.append(part)
    return ('/' + '/'.join(parts)).rstrip('/') or '/'


def infer_routes(root: Path) -> list[Route]:
    routes: list[Route] = []
    app = root / 'app'
    if app.exists():
        for p in app.rglob('*'):
            if p.name.split('.')[0] not in {'page', 'route'} or p.suffix not in ROUTE_EXTS:
                continue
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            route = route_from_app_file(app, p)
            kind = 'api' if p.name.startswith('route.') else 'page'
            priority = priority_for_route(route, p)
            routes.append(Route(route, rel(p, root), f'app-router-{kind}', ':' in route or '*' in route, priority))
    pages = root / 'pages'
    if pages.exists():
        for p in pages.rglob('*'):
            if p.is_dir() or p.suffix not in ROUTE_EXTS or p.name.startswith('_'):
                continue
            kind = 'api' if 'api' in p.relative_to(pages).parts[:1] else 'page'
            route = route_from_pages_file(pages, p)
            priority = priority_for_route(route, p)
            routes.append(Route(route, rel(p, root), f'pages-router-{kind}', ':' in route or '*' in route, priority))
    uniq = {(r.route, r.source): r for r in routes}
    return sorted(uniq.values(), key=lambda r: (-r.priority_hint, r.route, r.source))


def priority_for_route(route: str, path: Path) -> int:
    text = f'{route} {path}'.lower()
    score = 0
    if any(x in text for x in ['checkout', 'payment', 'billing', 'auth', 'login', 'signup', 'sign-up', 'register']):
        score += 3
    if any(x in text for x in ['pricing', 'landing', 'home', 'onboarding', 'booking', 'reservation', 'demo']):
        score += 2
    if any(x in text for x in ['dashboard', 'admin', 'settings', 'api', 'database']):
        score += 2
    if route == '/':
        score += 2
    return score


def line_no(text: str, index: int) -> int:
    return text.count('\n', 0, index) + 1


def scan_links(root: Path, routes: list[Route]) -> list[LinkFinding]:
    route_paths = {r.route for r in routes if 'page' in r.kind}
    has_dynamic = any(r.dynamic for r in routes)
    findings: list[LinkFinding] = []
    for p in iter_files(root):
        text = read_text(p)
        source = rel(p, root)
        for pat in LINK_PATTERNS:
            for m in pat.finditer(text):
                target = m.group(1).strip()
                ln = line_no(text, m.start())
                low = target.lower()
                if BAD_TARGET_RE.match(low):
                    findings.append(LinkFinding('P0/P1', source, target or '<empty>', 'placeholder-link', ln, 'Non-navigating or placeholder target'))
                elif target.startswith('/') and not target.startswith('//') and route_paths:
                    path = target.split('?', 1)[0].split('#', 1)[0].rstrip('/') or '/'
                    if path not in route_paths and not has_dynamic:
                        findings.append(LinkFinding('P1', source, target, 'possibly-missing-route', ln, 'Internal target not found in inferred route list'))
                elif 'localhost' in low or '127.0.0.1' in low:
                    findings.append(LinkFinding('P1/P2', source, target, 'local-dev-link', ln, 'Localhost target may break in production'))
        for m in TODO_RE.finditer(text):
            findings.append(LinkFinding('P2', source, m.group(1), 'todo-placeholder', line_no(text, m.start()), 'Production polish/trust risk'))
    return findings


def scan_secrets(root: Path) -> list[SecretFinding]:
    findings: list[SecretFinding] = []
    for p in iter_files(root):
        source = rel(p, root)
        # Avoid flagging our own scanner docs too aggressively.
        if source.startswith('.claude/skills/web-audit-squad/'):
            continue
        text = read_text(p)
        for name, pat in SECRET_PATTERNS.items():
            for m in pat.finditer(text):
                ln = line_no(text, m.start())
                severity = 'P0/P1' if name in {'supabase-service-role', 'database-url', 'aws-secret', 'private-key', 'payment-secret'} else 'P1/P2'
                findings.append(SecretFinding(severity, source, ln, name, 'Potential secret reference. Value redacted by scanner.'))
    return findings[:200]


def file_signals(root: Path) -> list[FileSignal]:
    out: list[FileSignal] = []
    for p in iter_files(root):
        text = read_text(p)
        out.append(FileSignal(
            source=rel(p, root),
            lines=text.count('\n') + 1,
            bytes=len(text.encode('utf-8', errors='ignore')),
            client_component=bool(CLIENT_RE.search(text)),
            has_form=bool(FORM_RE.search(text)),
            todos=len(TODO_RE.findall(text)),
        ))
    return sorted(out, key=lambda x: (x.client_component, x.bytes), reverse=True)[:80]


def stack_summary(root: Path) -> dict[str, object]:
    pkg = root / 'package.json'
    summary: dict[str, object] = {'packageManager': None, 'frameworkHints': [], 'scripts': {}}
    if (root / 'pnpm-lock.yaml').exists(): summary['packageManager'] = 'pnpm'
    elif (root / 'yarn.lock').exists(): summary['packageManager'] = 'yarn'
    elif (root / 'package-lock.json').exists(): summary['packageManager'] = 'npm'
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding='utf-8'))
            deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
            hints = [k for k in ['next', 'react', '@supabase/supabase-js', 'stripe', '@stripe/stripe-js', 'prisma', 'drizzle-orm', 'tailwindcss', 'zod'] if k in deps]
            summary['frameworkHints'] = hints
            summary['scripts'] = data.get('scripts', {})
        except Exception as e:
            summary['packageJsonError'] = str(e)
    return summary


def ensure_workspace(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'PAGE_AUDITS').mkdir(exist_ok=True)
    for name, content in {
        'BACKLOG.md': '# Web Audit Squad backlog\n\n## P0 — shipping blockers\n| Status | Page | Item | Evidence | Fix direction | Verify |\n|---|---|---|---|---|---|\n\n## P1 — important fixes\n| Status | Page | Item | Evidence | Fix direction | Verify |\n|---|---|---|---|---|---|\n\n## P2 — upside / polish\n| Status | Page | Item | Evidence | Fix direction | Verify |\n|---|---|---|---|---|---|\n',
        'DECISIONS.md': '# Web Audit Squad decisions\n\n| Date | Page | Decision | Reason | Risk |\n|---|---|---|---|---|\n',
    }.items():
        p = out_dir / name
        if not p.exists():
            p.write_text(content, encoding='utf-8')


def md_table(rows: list[list[object]]) -> list[str]:
    return ['| ' + ' | '.join(str(c) for c in row) + ' |' for row in rows]


def write_outputs(root: Path, out_dir: Path, max_findings: int) -> None:
    ensure_workspace(out_dir)
    routes = infer_routes(root)
    links = scan_links(root, routes)[:max_findings]
    secrets = scan_secrets(root)[:max_findings]
    signals = file_signals(root)
    stack = stack_summary(root)
    now = time.strftime('%Y-%m-%d %H:%M:%S')

    data = {
        'generatedAt': now,
        'root': str(root),
        'stack': stack,
        'routes': [asdict(r) for r in routes],
        'linkFindings': [asdict(f) for f in links],
        'secretFindings': [asdict(f) for f in secrets],
        'fileSignals': [asdict(f) for f in signals],
    }
    (out_dir / 'SCOUT.json').write_text(json.dumps(data, indent=2), encoding='utf-8')

    ws: list[str] = ['# Web structure', '', f'Last generated: {now}', '', '## Stack', '']
    ws.append(f"- Package manager: `{stack.get('packageManager') or 'unknown'}`")
    ws.append(f"- Framework/dependency hints: `{', '.join(stack.get('frameworkHints', [])) or 'unknown'}`")
    ws += ['', '## Route inventory', '', '| Priority | Route | Source | Kind | Dynamic |', '|---|---|---|---|---|']
    for r in routes:
        ws.append(f'| {r.priority_hint} | `{r.route}` | `{r.source}` | {r.kind} | {"yes" if r.dynamic else "no"} |')
    ws += ['', '## Suspicious links/actions/placeholders', '']
    if links:
        ws += ['| Severity | Source | Line | Target/action | Kind | Note |', '|---|---|---:|---|---|---|']
        for f in links:
            ws.append(f'| {f.severity} | `{f.source}` | {f.line} | `{f.target}` | {f.kind} | {f.note} |')
    else:
        ws.append('No suspicious links/actions found by scout.')
    ws += ['', '## Potential secret/security references', '']
    if secrets:
        ws += ['| Severity | Source | Line | Pattern | Note |', '|---|---|---:|---|---|']
        for f in secrets:
            ws.append(f'| {f.severity} | `{f.source}` | {f.line} | {f.pattern} | {f.note} |')
    else:
        ws.append('No potential secret references found by scout.')
    ws += ['', '## Page priority queue', '']
    for i, r in enumerate([r for r in routes if 'page' in r.kind][:20], 1):
        ws.append(f'{i}. `{r.route}` — priority hint {r.priority_hint}, source `{r.source}`')
    (out_dir / 'WEB_STRUCTURE.md').write_text('\n'.join(ws) + '\n', encoding='utf-8')

    cs: list[str] = ['# Current state', '', f'- Last updated: {now}', '- Current focus: route map / audit setup', '- Audit mode: audit-only unless implementation is explicitly requested', f"- Known stack: {', '.join(stack.get('frameworkHints', [])) or 'unknown'}", f'- Routes mapped: {len(routes)}', f'- Suspicious link/action findings: {len(links)}', f'- Potential secret/security references: {len(secrets)}', '', '## Next best action', 'Audit the highest-priority route with P0/P1 findings first. If no P0/P1 exists, start with `/`, pricing, signup/auth, booking/demo, then dashboard.', '', '## Open unknowns', '- Confirm runtime/build commands.', '- Confirm authentication, database, storage, payment provider boundaries.', '- Confirm live links with a running app if source-only scan is insufficient.', '']
    (out_dir / 'CURRENT_STATE.md').write_text('\n'.join(cs), encoding='utf-8')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.', help='Project root to scan')
    ap.add_argument('--out-dir', default='.claude/web-audit-squad', help='Audit workspace output directory')
    ap.add_argument('--max-findings', type=int, default=200)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    out_dir = (root / args.out_dir).resolve() if not Path(args.out_dir).is_absolute() else Path(args.out_dir)
    write_outputs(root, out_dir, args.max_findings)
    print(f'Wrote audit scout outputs to {out_dir}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
