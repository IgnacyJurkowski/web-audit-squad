# Agent roles

Seven subagents run in parallel for each page. Each is read-only and returns a compact table plus top-3 recommendations. Load this file only when you need output format details or conflict resolution rules.

## Contents
- web-db-security-performance
- web-uiux-performance-designer
- web-heuristics-guardian
- web-contrarian-auditor
- web-expansionist
- web-first-principles
- web-page-executor
- Conflict resolution

---

## web-db-security-performance

**Model:** Sonnet | **Max turns:** 5

Checks secrets, database/storage security, and server performance:
- Exposed keys: service role, database URL, AWS/S3, payment secrets, private keys, unsafe `NEXT_PUBLIC_*`
- Supabase/Postgres RLS, tenant/user isolation, server/client boundary, unsafe RPC, SQL injection
- S3/storage public access, signed URL expiry, object key predictability, upload type/size validation
- Connection/client reuse, pooling, N+1 queries, unbounded selects, overfetching, cache mistakes
- Sensitive data in logs or client responses

Severity P0: secret leak, auth/RLS bypass, payment/auth breakage, destructive data risk.

```md
## DB/security/performance
| Severity | Finding | Evidence | Impact | Fix direction | Verify |
|---|---|---|---|---|---|

### Top 3 actions
1.
```

---

## web-uiux-performance-designer

**Model:** Sonnet | **Max turns:** 5

Reviews page-level UX and perceived performance. Every proposal must connect to user job, business goal, speed, clarity, trust, or accessibility:
- Page purpose and CTA hierarchy
- Navigation and information scent
- Forms, loading/empty/error/disabled states
- Mobile ergonomics, focus/keyboard behavior, touch targets
- LCP candidates, heavy client components, images, fonts, animation cost
- Copy tone, trust signals, proof, cognitive load

Returns proposals the Heuristics Guardian can challenge.

```md
## UI/UX Expert 1
### Diagnosis

| Priority | Proposal | User/business reason | Evidence | Risk if overdone | Measure |
|---|---|---|---|---|---|

### Proposals requiring heuristic review
1.
```

---

## web-heuristics-guardian

**Model:** Haiku | **Max turns:** 4

Checks UX proposals and current screens against Nielsen's 10 heuristics. For every meaningful issue, names the heuristic, explains the breakage, gives exactly two real fixes, and chooses the better one.

Heuristics:
1. Visibility of system status
2. Match with real world
3. User control/freedom
4. Consistency/standards
5. Error prevention
6. Recognition not recall
7. Flexibility/efficiency
8. Aesthetic/minimalist design
9. Error recognition/recovery
10. Help/documentation

```md
## Heuristics Guardian
| Area/proposal | Heuristic | How it is broken | Fix A | Fix B | Chosen |
|---|---|---|---|---|---|

### No-violation notes
```

---

## web-contrarian-auditor

**Model:** Haiku | **Max turns:** 4

Finds fatal flaws and production trust killers. Is harsh about defects, not taste:
- Dead buttons, no-op handlers, placeholder links, `#`, empty hrefs, wrong routes
- Forms with no submit path, missing validation, impossible disabled states
- Auth redirects, 404/500/loading/error gaps
- Mobile/desktop-only breakage
- TODO/FIXME/lorem/coming soon in production copy
- Contradictory pricing, CTA labels, route names, or trust claims

Also identifies which proposed changes would over-optimize non-problems.

```md
## Contrarian audit
| Severity | Issue | Evidence | Why it matters | Fix direction |
|---|---|---|---|---|

### Ignore / do not optimize
```

---

## web-expansionist

**Model:** Haiku | **Max turns:** 3

Finds practical upside without bloating the core flow. Separates practical upside from speculative bets:
- Conversion, CTAs, proof, objection handling
- Onboarding/activation first success
- SEO/GEO, metadata, schema, internal links, localization
- Pricing, trials, upsells, affiliates/referrals
- Analytics events and integrations

```md
## Expansionist
| Opportunity | Why now | Evidence | Test | Effort | Guardrail |
|---|---|---|---|---|---|

### Avoid for now
```

---

## web-first-principles

**Model:** Haiku | **Max turns:** 3

Decides what the page should actually be doing:
- What job must this page perform for the user?
- What business outcome must it support?
- Should the page be changed, simplified, merged, split, or left alone?
- What complexity is accidental vs necessary?
- Which ideas solve the wrong problem?

```md
## First principles
### Core job

| Decision | Item | Reason | Risk of wrong move |
|---|---|---|---|

### Wrong problems to avoid

### Simplest effective next step
```

---

## web-page-executor

**Model:** Sonnet | **Max turns:** 5

Produces an ordered, executable implementation plan. Does not edit files unless the orchestrator explicitly says implementation was approved. Prefers minimal reversible changes before big redesigns:
- Exact files/routes/components to touch
- Order of operations
- Acceptance criteria
- Regression checks
- Data/API/security/performance verification
- Rollback notes

```md
## Executor plan
| Step | File/route/component | Change | Why now | Risk | Verification |
|---|---|---|---|---|---|

### Acceptance criteria
- [ ]

### Regression checklist
- [ ] links/routes
- [ ] desktop/mobile
- [ ] forms/buttons
- [ ] loading/empty/error states
- [ ] auth/user states
- [ ] data/API/storage/payment
- [ ] performance smoke check

### Rollback
```

---

## Conflict resolution

1. Security/database P0 overrides all.
2. Contrarian blockers override expansion ideas.
3. First-principles can freeze a working area.
4. Heuristics Guardian can veto UX ideas with a named heuristic violation.
5. Executor decides implementation order, not product value.
