# Web Audit Squad protocol

## Severity

- P0: exposed secret, auth/payment breakage, data leak, public sensitive storage, unusable core route, dead primary CTA, destructive bug.
- P1: serious conversion/speed/trust/maintainability issue likely to hurt users or operations.
- P2: polish, optional upside, lower-risk optimization.

## Evidence standard

Every finding should include at least one of:
- file path and line;
- route and link/action target;
- command output from scout;
- visible UI behavior;
- missing file/route proof;
- unknown that requires verification.

Do not paste long code. Quote only the exact identifier or 1-3 line fragment required to prove the point.

## Page priority formula

Score each page 0-10:
- +3 revenue/payment/auth/core product;
- +2 landing/pricing/onboarding/public booking;
- +2 data-heavy/admin/security-sensitive;
- +1 high traffic or main navigation;
- +1 known broken links/actions;
- +1 high business uncertainty.

## Agent conflict resolution

1. Security/database P0 overrides all.
2. Contrarian blockers override expansion ideas.
3. First-principles can freeze a working area.
4. Heuristics guardian can veto UX ideas with a named heuristic violation.
5. Executor decides implementation order, not product value.
