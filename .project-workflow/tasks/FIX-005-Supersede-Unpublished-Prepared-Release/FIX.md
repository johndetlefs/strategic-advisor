# Fix

## Summary

- Fix: FIX-005
- Title: Supersede Unpublished Prepared Release
- Status: Review
- Created: 2026-08-24
- Intent contract: compact

## Intent

Permit an immutable prepared release candidate that has not been published to be superseded without rewriting or reusing its version. Preserve an auditable record of the superseded candidate and atomically prepare the next version from the current canonical runtime.

## Report

- Observed or requested: `v0.2.0-alpha.4` is prepared against runtime identity `0dd72075...`, but FIX-004 changes the canonical runtime to `85398afb...`. The release state refuses both a mismatched alpha.4 and preparation of alpha.5 while alpha.4 remains prepared.
- Expected: An unpublished prepared candidate can be immutably recorded as superseded, its version can never be reused, and the next advancing version can be prepared in the same transaction against the current runtime.
- Affected users or systems: Strategic Advisor maintainers, release automation, release provenance, and consumers who must not receive a knowingly superseded candidate merely to advance the release state.
- Delivered baseline: The release lifecycle supports only `published -> prepared -> published`; it deliberately prevents overwriting prepared bytes but has no pre-publication supersession transition.
- Report evidence: Live `release_state.py check` reports the alpha.4/runtime mismatch; `prepare --version 0.2.0-alpha.5` refuses while alpha.4 is prepared; `distribution.json` retains alpha.3 as current public and alpha.4 as prepared.

## Routing

- Decision: Fix
- Rationale: This is one bounded defect in the delivered immutable release lifecycle. It restores an honest pre-publication path and does not add a product capability or change Strategic Advisor reasoning.
- Related work state: FIX-004 is Blocked only at its release/distribution gate; EPIC-006 prepared alpha.4 without publishing it.
- Bounded correction: Add a validated, transactional `supersede` transition and immutable superseded-candidate history, then use it to supersede alpha.4 and prepare alpha.5.
- New outcome or material decisions: No
- Independent work items: One

## Classification

- Type: Defect
- Mode: Normal
- Severity: High
- Impact: Without correction, maintainers must either corrupt version provenance or publish a knowingly superseded candidate before releasing corrected runtime bytes.
- Urgency: Before FIX-004 publication.
- Owner: John Detlefs

## Related Work

- Originating work: EPIC-006 prepared `v0.2.0-alpha.4`; FIX-004 exposed the missing supersession path before publication.
- External links: None

## Risk

- Risk level: High
- Risks: Accidentally superseding a published candidate, losing the original prepared identity, permitting version reuse, accepting fabricated source provenance, partially writing release state/documents, or allowing a non-advancing replacement version.
- Rollback or containment: Keep the existing fail-closed lifecycle unless every supersession precondition passes. The transition must be transactional; reverting the implementation before applying it leaves alpha.4 prepared and unpublished.

## Fix Plan

- Scope: Extend the canonical distribution authority with validated superseded-candidate history; require a prepared state, exact committed source proof, an advancing unused next version, a non-empty reason, and an explicit timestamp; atomically retain alpha.4 and prepare alpha.5; synchronize release-facing documents and validators.
- Non-goals: Rewrite alpha.4, publish alpha.4, reuse its tag/version, weaken runtime/package binding, change Strategic Advisor product behaviour beyond FIX-004, claim stable release or universal behavioural effectiveness, or alter unrelated workflow state.
- Affected target: `scripts/release_state.py`, distribution authority/schema, release-state and aggregate validation tests, release documentation, and the alpha.5 preparation/publication sequence.
- Primary repo: .
- Repos touched: .
- Branch, PR, and evidence links: `codex/fix-004-owner-led-recommendation-drift`; candidate commit `1cc2826eda9c2270a88f1cec35e5a167bc1ab6fa`; [PR #18](https://github.com/johndetlefs/strategic-advisor/pull/18); release pending; retained FIX-004 drift evidence under `evidence/evaluations/drift-smoke/run-006/`.
- Verification plan: Freeze transition tests first; prove refusal for non-prepared, reused/non-advancing versions, invalid source/reason/time, mismatched committed intent, and transactional failure; prove exact superseded record plus alpha.5 preparation; run release/package/claims tests, complete unit and validator suites, clean deterministic builds, Workflow Doctor, protected-main publication, fresh-download verification, finalization, and installed-runtime identity verification.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | `codex/fix-004-owner-led-recommendation-drift` | [#18](https://github.com/johndetlefs/strategic-advisor/pull/18) | Unit/validator/run-006/two-build evidence pass; release pending |

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | Pushed `codex/fix-004-owner-led-recommendation-drift`; PR #18 | Focused release-state/publication suites and complete 149-test suite pass; seven validator scopes, 56-case rebuild, run-006 verifier, Doctor, compilation, diff check, and two clean byte-identical candidate builds pass | Alpha.4 retained as superseded and alpha.5 prepared; merge, publication, finalization, and installation pending | `distribution.json`; FIX-004 `run-006`; clean build from `1cc2826...`; commands recorded below |

## Verification

- Delivered scope: Added schema-v2 immutable superseded-candidate history and an atomic `release_state.py supersede` transition; froze success, refusal, source-proof, invalid-input, tagged-candidate, version-reuse, history-preservation, and transactional-rollback coverage; documented the maintainer route; live-verified alpha.4 had no local tag, remote tag, or GitHub release; recorded exact alpha.4 intent from `9dbc7d7...`; superseded alpha.4 and prepared alpha.5 against runtime `85398afb...`.
- Verification result: `release_state.py check` passes with alpha.5 prepared and alpha.4 retained; `build_evals.py --check` reports 56 current cases; the 15-group run-006 verifier and all seven `validate.py` scopes pass; focused release-state/publication suites pass (12 tests); the complete unit suite passes (149 tests); compilation, `git diff --check`, and Workflow Doctor pass.
- Adjacent behavior checked: Existing prepare/finalize, public-release verification, deterministic install packaging, runtime-binding, documentation synchronization, claims derivation, and superseded-history preservation remain covered. FIX-004's corrected runtime identity remains exactly `85398afb...`.
- Original acceptance criteria result: Not applicable
- Regression evidence: Prior code refused alpha.5 with `current distribution is already prepared; publish and finalize it first`. New tests prove an exact committed prepared candidate can be retained and replaced atomically, while published, tagged, unproven, invalid, reused, non-advancing, and partially written transitions fail closed.
- Residual risk: Local evidence does not prove protected-main merge, GitHub publication, fresh public download, finalization, or personal installation. Those delivery stages remain mandatory before either Fix is closed.

## QA & Code Review

- Date: 2026-08-24
- Reviewed areas: Release authority schema compatibility; immutable history invariants; exact committed-source verification; ancestor/source constraints; unpublished/tag/evidence refusal; version advancement and reuse; atomic writes and rollback; document synchronization; standard-library/source-archive portability; finalize history preservation; FIX-004 runtime and evaluation continuity; historical Project Workflow evidence integrity; privacy and scope.
- Validation evidence: `python3 scripts/release_state.py check`; `python3 scripts/build_evals.py --check`; `python3 scripts/drift_smoke.py verify-result --result evidence/evaluations/drift-smoke/run-006/result.json`; `python3 scripts/validate.py`; `python3 -m unittest discover -s tests` (149 pass); `python3 -m py_compile`; `git diff --check`; `./.project-workflow/cli/workflow doctor`; live local/remote tag and GitHub release absence checks for alpha.4 and alpha.5.
- Findings: No blocking implementation finding remains. Review initially found that historical provenance re-opening had been applied too broadly to portable validator fixtures; it was narrowed so ordinary structural/package validation remains Git-independent while repository `release_state.py check` and mutating transitions verify committed supersession provenance. Updating the current product contract also exposed a stale historical evidence pointer; the exact alpha.4 contract bytes were retained under TASK-030 and its original hash was verified instead of rewriting the historical claim.
- Verdict: **Pass for local implementation and prepared alpha.5 state.** Completion remains pending protected-main integration, immutable publication, fresh-download verification, finalization, and personal-install verification.

## Outcome

- Disposition: Pending
- Decision: ____
- Closed by: ____
- Closed date: ____
- Promoted to: None
