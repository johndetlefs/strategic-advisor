# Fix

## Summary

- Fix: FIX-004
- Title: Prevent Owner-Led Recommendation Drift
- Status: Review
- Created: 2026-08-24
- Intent contract: compact

## Intent

Strategic Advisor must keep its diagnosis and recommendation tied to the owner's confirmed outcome and qualifying evidence across messy, forceful, owner-led turns. Agreement and disagreement are incidental: an owner proposal, confidence, frustration, or later accusation must neither upgrade the proposal nor be required to trigger the advisor's strongest rival or failure reset.

## Report

- Observed or requested: Owner-authorised review found recurrence after FIX-002: in consequential multi-turn discussions, the advisor can endorse a plausible owner-proposed mechanism before testing the strongest smaller or opposing rival, use unscoped agreement, and recover only after the owner explicitly challenges the drift.
- Expected: Materially identical evidence produces a stable diagnosis and readiness regardless of owner preference, confidence, forcefulness, or anger; the advisor confirms or labels material intent uncertainty before consequential advice, treats mechanisms as hypotheses, and suspends a success claim when the real outcome contradicts it.
- Affected users or systems: Strategic Advisor users making consequential decisions through iterative conversation, especially owners who provide valid failure evidence together with candidate remedies.
- Delivered baseline: FIX-002 added explicit preference-conservation rules and DRIFT-007. EPIC-006 then added proportionate decision-baseline and technical-architecture controls, and exact-runtime run-005 passed twelve synthetic scenario groups. Those controls do not yet require turn-local adjudication of the first unsupported proposal or distinguish outcome correction from the owner's proposed mechanism strongly enough.
- Report evidence: Owner-authorised review of live Strategic Advisor tasks, the current task's self-audit, FIX-002, EPIC-006, canonical runtime source, and retained run-005. No private task content will be committed; regression cases will be public-synthetic abstractions.

## Routing

- Decision: Fix
- Rationale: This is one bounded recurrence against the delivered anti-preference-drift behaviour and its regression proof. It restores the existing outcome rather than adding a lens, domain, workflow, or independent product outcome.
- Related work state: FIX-002 and EPIC-006 Complete; EPIC-001 remains In Progress with comparative evaluation and real-pilot proof still pending.
- Bounded correction: Add a stable material-turn decision state, recommendation-delta invariant, scoped agreement, and delivery-failure reset to the canonical conversational runtime; add uncued, public-synthetic multi-turn drift scenarios whose first unsupported proposal turn is explicitly reviewed; retain fresh exact-runtime smoke evidence.
- New outcome or material decisions: No
- Independent work items: One

## Classification

- Type: Defect
- Mode: Normal
- Severity: High
- Impact: The advisor may sound evidence-disciplined while allowing owner framing to change the recommended mechanism or readiness before qualifying evidence changes, causing wasted work and failure against the requested outcome.
- Urgency: Before relying on Strategic Advisor for another consequential owner-led solution or delivery decision.
- Owner: John Detlefs

## Related Work

- Originating work: FIX-002 Prevent Preference Drift In Candidate Ranking; EPIC-006 Technical Architecture And Evidence Grounded Invocation; EPIC-001 remains the broader source-implementation, comparative-evaluation, and real-pilot proof boundary through its existing children.
- External links: None

## Risk

- Risk level: Medium
- Risks: Overcorrecting into automatic disagreement, making routine advice bureaucratic, treating emotion as evidence, forcing repetitive confirmation, encoding private task facts in public tests, weakening newer technical-architecture controls, or expanding a bounded regression into host-specific orchestration.
- Rollback or containment: Revert the bounded runtime clauses and new synthetic drift cases together; keep the product capability unvalidated and retain the live failure report as unresolved evidence. Do not add an independent critic architecture unless prompt-level controls fail the new uncued cases.

## Fix Plan

- Scope: First freeze uncued live-derived synthetic failures; then implement the smallest canonical rules that preserve a material decision state, classify owner proposals separately from evidence, require an evidence/constraint/value/outcome delta before recommendation change, scope agreement to the supported proposition, and suspend prior success/readiness on a material outcome contradiction.
- Non-goals: Guarantee perfect objectivity or correct outcomes, suppress legitimate agreement, require disagreement, make the owner use a special prompt template, commit private task content, create another Epic or lens, complete EPIC-001's comparative evaluation or real pilots, publish or install a release, or make cross-host independent-critic support a current capability.
- Affected target: Canonical Strategic Advisor conversational runtime, bounded actual-turn drift-smoke specification/verifier/tests, and fresh exact-runtime drift evidence.
- Primary repo: .
- Repos touched: .
- Branch, PR, and evidence links: Local `codex/fix-004-owner-led-recommendation-drift` based on `9dbc7d744dc10bd5053daacf6054e978c67c3a5c`; no commit, push, PR, release, installation, or deployment authorised; retained evidence under `evidence/evaluations/drift-smoke/run-006/`.
- Verification plan: Add new public-synthetic cases and deterministic turn-review enforcement before runtime edits; confirm the exact current runtime fails at least one newly frozen criterion or record honestly if it does not; implement the bounded runtime correction; run focused drift-smoke/runtime tests, full deterministic validation and unit tests; build the exact runtime package; execute every frozen scenario in isolated fresh/resumed Codex CLI sessions; review every precommitted criterion, including first-proposal turns; verify the retained result and run Project Workflow Doctor.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | `codex/fix-004-owner-led-recommendation-drift` | None | `evidence/evaluations/drift-smoke/run-006/` (retained) |

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | Local `codex/fix-004-owner-led-recommendation-drift`; no PR yet | Behavioural, release-state, claims, aggregate, 149-test, seven-scope validator, run-006, Doctor, compilation, and diff gates pass | Alpha.5 prepared locally; no commit, push, merge, publication, finalization, or installation yet | `run-006-baseline`, exact-runtime `run-006`, `distribution.json`, FIX-005 review |

## Verification

- Delivered scope: Upgraded this branch's Project Workflow installation from 0.1.1 to 0.6.0; added explicit material-decision-state, outcome-ambiguity, owner-proposal, recommendation-delta, scoped-agreement, and delivered-journey reset rules to the canonical runtime; expanded the frozen drift authority from 12 to 15 groups; required exact per-turn reviews for the three new groups; retained the failing previous-runtime baseline and passing corrected-runtime run-006.
- Verification result: Behavioural and bounded deterministic implementation proof passes. `build_evals.py --check` reports 56 cases; the 15-group run-006 verifier and all seven validator scopes pass; the complete unit suite passes 149 tests; compilation, diff check, and Workflow Doctor pass. FIX-005 immutably retained unpublished alpha.4 at runtime `0dd72075...` and prepared alpha.5 against corrected runtime `85398afb...`; the prior release-state, claims, and aggregate failures are resolved.
- Adjacent behavior checked: DRIFT-001 through DRIFT-012 all passed on the corrected exact runtime, including three implicit-positive architecture sessions with proven technical-lens reads and one direct-assistance session with no Strategic Advisor read. The latter used `--ignore-user-config` after discarded host-memory lookups violated the synthetic visibility boundary. Existing evaluation inventory, privacy, lenses, pilots, links, runtime packaging, and installation-artifact unit coverage showed no independent regression.
- Original acceptance criteria result: Not applicable
- Regression evidence: The retained `run-006-baseline` binds the exact prior runtime `0dd72075...` to a DRIFT-013 failure: neutral T2 refused implementation pending a trace, neutral T3 upgraded to building a minimal orchestration layer after only repeated preference, while the matched angry final did not. Corrected runtime `85398afb...` passed all 15 groups, 17 source-bound sessions, 48 actual turns, every frozen criterion, and every new turn-local review.
- Residual risk: This proves bounded behaviour only for the retained synthetic cases, Codex CLI version, model, source, and date. It does not establish universal objectivity, skilled-versus-unskilled improvement, independent human validation, cross-host parity, real-task effectiveness, adoption, or support. Protected-main integration, GitHub publication, fresh-download verification, finalization, and current personal installation remain unproven and are required before closeout.

## QA & Code Review

- Date: 2026-08-24
- Reviewed areas: Fix classification and scope; Project Workflow upgrade provenance; canonical runtime decision-state rules; technical-architecture and evidence-baseline preservation; new case authority; per-turn verifier enforcement; baseline and run-006 source binding; public status derivation; privacy; release-state sequencing; diff hygiene; workflow state; and exact delivery boundaries.
- Validation evidence: `git diff --check`; `build_evals.py --check` (56 current cases); frozen 15-group exact-runtime run-006 verifier; all seven validator scopes; `python3 -m unittest discover -s tests` (149 pass); compilation; Workflow Doctor; exact alpha.4/alpha.5 release-state and live absence evidence recorded in FIX-005.
- Findings:
  - **Resolved — release/distribution sequence:** FIX-005 added and exercised the authorised pre-publication supersession transition. Alpha.4 remains immutably recorded with its original version, runtime identity, source, reason, timestamp, and alpha.5 replacement; it was not published or reused. Alpha.5 is prepared against the corrected runtime and every previously affected release/claims/aggregate gate passes.
  - **Proof boundary — delivery pending:** Run-006 remains source-bound by exact frozen-spec and runtime identities, but the local authority is not yet commit-backed, merged, publicly published, freshly downloaded, finalized, or installed. Those named stages remain the only closeout work.
  - No independent runtime-logic, regression-authority, per-turn-verifier, privacy, lens, pilot, link, or workflow finding remains in the bounded correction.
- Verdict: **Pass for local implementation and prepared alpha.5 state.** No code or behavioural finding remains; completion is withheld only until the named integration, public verification, finalization, and installed-runtime delivery stages pass.

## Outcome

- Disposition: Pending
- Decision: ____
- Closed by: ____
- Closed date: ____
- Promoted to: None
