# Contributing

Good contributions make the skill more precise without making it heavier.

## Rules

1. Keep `SKILL.md` short. Put reference material in `references/`.
2. Prefer scripts that output compact Markdown/JSON over asking Claude to read the whole repo.
3. Keep subagents read-only unless there is a strong reason.
4. Add exact output contracts to every agent prompt.
5. Do not paste long copied prompts from other repositories. Adapt patterns, cite inspiration in docs, and keep our wording original.
6. Test on a small demo app before release.

## Local validation

```bash
python3 .claude/skills/web-audit-squad/scripts/scout.py --root . --out-dir /tmp/web-audit-squad-test
python3 .claude/skills/web-audit-squad/scripts/state.py init --root /tmp/web-audit-squad-test-root
```
