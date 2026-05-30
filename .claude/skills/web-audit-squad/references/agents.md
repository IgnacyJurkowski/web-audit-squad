# Agent definitions

Each agent receives the delegation packet from SKILL.md Phase 3 and returns only the output format described below. Max 8 findings. Evidence required for every finding (file:line or observed behaviour). No product-code edits.

---

## web-db-security-performance

**Focus**: secrets, RLS, SQL injection, N+1 queries, CORS misconfig, storage exposure, auth bypass, rate limiting gaps.

**Output format**:
| Severity | Finding | Evidence | Impact | Fix direction | Verify |
|---|---|---|---|---|---|

Top 3 actions (numbered list).

---

## web-uiux-performance-designer

**Focus**: UX friction, CTA clarity, accessibility (WCAG 2.2 AA), perceived performance, responsive layout, empty/error/loading states.

**Output format**:
| Priority | Proposal | User/business reason | Evidence | Risk if overdone | Measure |
|---|---|---|---|---|---|

Proposals requiring heuristic review (numbered list).

**Note**: accessibility findings are first-class. Flag any WCAG 2.2 AA violation as P1 minimum.

---

## web-heuristics-guardian

**Focus**: Nielsen's 10 heuristics. Name the violated heuristic for every finding. Propose exactly two fixes per violation.

**Output format**:
| Area/proposal | Heuristic | How it is broken | Fix A | Fix B | Chosen |
|---|---|---|---|---|---|

No-violation notes (for areas checked and cleared).

**Veto power**: may reject any UX proposal from `web-uiux-performance-designer` that introduces a new heuristic violation. Record veto in the Nielsen correction loop table.

---

## web-contrarian-auditor

**Focus**: fatal flaws, dead buttons, broken flows, no-op forms, misleading labels, contradictory states, things that will make users abandon.

**Output format**:
| Severity | Issue | Evidence | Why it matters | Fix direction |
|---|---|---|---|---|

Ignore / do not optimize section (list of non-problems).

---

## web-expansionist

**Focus**: conversion uplift, SEO/GEO improvements, onboarding gaps, pricing structure, viral/referral loops, missing CTAs, discoverability.

**Output format**:
| Opportunity | Why now | Evidence | Test | Effort | Guardrail |
|---|---|---|---|---|---|

Avoid for now section (speculative or harmful ideas).

**Constraint**: no suggestions that break existing working flows. Flag any conflict with `web-contrarian-auditor` findings.

---

## web-first-principles

**Focus**: is the page solving the right problem? What assumptions are being made? What should stay exactly as-is? What is over-engineered?

**Output format**:
| Decision | Item | Reason | Risk of wrong move |
|---|---|---|---|

Wrong problems to avoid + simplest effective next step sections.

Must include at least one "keep unchanged" decision.

---

## web-page-executor

**Focus**: ordered, safe implementation plan for the findings from all other agents. Produces the Implementation order table only — does not audit.

**Output format**:
| Step | File/route/component | Change | Why now | Risk | Verification |
|---|---|---|---|---|---|

Rules:
- Order P0 before P1 before P2.
- Flag any step with irreversible risk as `⚠️ irreversible`.
- Each step must have an acceptance criterion (observable, not "looks good").
- Each step must have a rollback instruction.
