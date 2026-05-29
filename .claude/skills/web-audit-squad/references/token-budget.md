# Token budget rules

## Read order

1. `SCOUT.json`
2. `WEB_STRUCTURE.md`
3. `CURRENT_STATE.md`
4. Current page files only
5. Shared components used by current page
6. API/data files called by current page

## Do not load

- `node_modules/`, `.next/`, `dist/`, `build/`, coverage, lockfiles unless needed for package manager.
- Large generated files.
- Entire documents when route map already has the relevant lines.

## Subagent packet budget

Aim for:
- 1 route or flow;
- 3-8 files max;
- 10 links/actions max;
- 10 known facts max;
- explicit output cap.

## Subagent answer budget

Ask agents for:
- max 8 findings;
- top 3 recommendations;
- tables over paragraphs;
- no full code blocks unless asked to implement.
