# Research notes behind v2

This package was shaped by current Claude Code documentation and public Claude skill/subagent repositories. It does not copy third-party skill code or prompts. The design borrows general engineering patterns only:

- concise skill frontmatter and manual invocation for heavy workflows;
- reference files instead of huge `SKILL.md` bodies;
- read-only subagents with explicit tool allowlists;
- max-turn limits and cheaper models for checklist-style roles;
- scout/index scripts to avoid loading the whole repository into context;
- durable Markdown state so repeated audits do not rediscover the same facts;
- page-by-page execution instead of one huge audit dump;
- issue/backlog format with severity, evidence, owner, and verification.

Public repositories/lists checked while designing the pack included: `anthropics/skills`, `travisvn/awesome-claude-skills`, `ComposioHQ/awesome-claude-skills`, `VoltAgent/awesome-claude-code-subagents`, `0xfurai/claude-code-subagents`, `lst97/claude-code-sub-agents`, `iannuttall/claude-agents`, `hesreallyhim/awesome-claude-code`, `trailofbits/skills`, `mattpocock/skills`, `alirezarezvani/claude-skills`, `Jeffallan/claude-skills`, `TerminalSkills/skills`, `fivetaku/claude-office-skills`, `FrancyJGLisboa/agent-skill-creator`, `mxyhi/ok-skills`, `agent-sh/agnix`, `mrgoonie/claudekit-skills`, `ccplugins/awesome-claude-code-plugins`, and `centminmod/my-claude-code-setup`.

Because GitHub search results shift over time, treat this as a research snapshot rather than an official ranking.
