#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-.}"
mkdir -p "$TARGET/.claude"
cp -R .claude/skills "$TARGET/.claude/"
cp -R .claude/agents "$TARGET/.claude/"
echo "Installed Web Audit Squad into $TARGET/.claude"
echo "Restart Claude Code, then run: /web-audit-squad init"
