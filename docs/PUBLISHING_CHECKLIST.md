# Publishing checklist

- [ ] Review every file under `.claude/` before trusting it in a target repo.
- [ ] Run scout against this repository and confirm it does not expose secret values.
- [ ] Install into a small demo app.
- [ ] Restart Claude Code and confirm `/web-audit-squad init` appears.
- [ ] Confirm subagents appear in `/agents`.
- [ ] Create a GitHub release zip.
