# Agent definitions

Each agent receives the delegation packet from SKILL.md Phase 3 and returns only the output format described below. Max 8 findings. Evidence required for every finding (file:line or observed behaviour). No product-code edits.

---

## web-db-security-performance

**Focus**: secrets, RLS, SQL injection, N+1 queries, CORS misconfig, storage exposure, auth bypass, rate limiting gaps.

**Output format**:
| # | Finding | Severity | File:line | Recommendation |
|---|---|---|---|---|

Top 3 recommendations (numbered list).

---

## web-uiux-performance-designer

**Focus**: UX friction, CTA clarity, accessibility (WCAG 2.2 AA), perceived performance, responsive layout, empty/error/loading states.

**Output format**:
| # | Finding | Severity | Location | Recommendation |
|---|---|---|---|---|

Top 3 recommendations (numbered list).

**Note**: accessibility findings are first-class. Flag any WCAG 2.2 AA violation as P1 minimum.

---

## web-heuristics-guardian

**Focus**: Nielsen's 10 heuristics. Name the violated heuristic for every finding. Propose exactly two fixes per violation.

**Output format**:
| # | Heuristic violated | Observed breakage | Fix A | Fix B |
|---|---|---|---|---|

Top 3 recommendations (numbered list).

**Veto power**: may reject any UX proposal from `web-uiux-performance-designer` that introduces a new heuristic violation. Record veto in the Nielsen correction loop table.

---

## web-contrarian-auditor

**Focus**: fatal flaws, dead buttons, broken flows, no-op forms, misleading labels, contradictory states, things that will make users abandon.

**Output format**:
| # | Fatal flaw | Reproduction path | Severity | Fix |
|---|---|---|---|---|

Top 3 recommendations (numbered list).

---

## web-expansionist

**Focus**: conversion uplift, SEO/GEO improvements, onboarding gaps, pricing structure, viral/referral loops, missing CTAs, discoverability.

**Output format**:
| # | Opportunity | Estimated impact | Effort | Recommendation |
|---|---|---|---|---|

Top 3 recommendations (numbered list).

**Constraint**: no suggestions that break existing working flows. Flag any conflict with `web-contrarian-auditor` findings.

---

## web-first-principles

**Focus**: is the page solving the right problem? What assumptions are being made? What should stay exactly as-is? What is over-engineered?

**Output format**:
| # | Assumption | Valid? | Risk if wrong | Recommendation |
|---|---|---|---|---|

Top 3 recommendations (numbered list). Must include at least one "keep unchanged" recommendation.

---

## web-page-executor

**Focus**: ordered, safe implementation plan for the findings from all other agents. Produces the Implementation order table only — does not audit.

**Output format**:
| Step | File/route | Change | Risk | Acceptance criteria | Rollback |
|---|---|---|---|---|---|

Rules:
- Order P0 before P1 before P2.
- Flag any step with irreversible risk as `⚠️ irreversible`.
- Each step must have an acceptance criterion (observable, not "looks good").
- Each step must have a rollback instruction.
