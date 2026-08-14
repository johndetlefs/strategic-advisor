# Fix

## Summary

- Fix: FIX-003
- Title: Align Public Architecture And Drift Claims
- Status: Testing
- Created: 2026-08-14

## Report

- Observed or requested: Independent review found that `README.md` omits
  technical architecture from the implemented-but-not-validated alpha
  candidates and still describes the current bounded Codex drift smoke as
  seven scenarios although retained `run-005` contains twelve scenario groups.
  Every existing validation scope passes despite both public-claim drifts.
- Expected: The public capability row must stay aligned with the canonical
  implemented lens contract, and the public evaluation row must stay aligned
  with the validated frozen drift-smoke authority and its retained current run.
- Affected users or systems: Readers assessing Strategic Advisor capability or
  evaluation maturity, including a Claude Enterprise user deciding whether the
  prepared standalone archive is the intended upgrade candidate.
- Delivered baseline: EPIC-006 is complete on
  `codex/EPIC-006-architecture-invocation`. It prepared, but did not publish,
  `v0.2.0-alpha.4` with seven implemented-not-validated lenses and retained
  twelve-group `run-005`; `v0.2.0-alpha.3` remains the current public release.
- Report evidence: `README.md`, `PRODUCT-CONTRACT.md`, the seven entries in
  `scripts/validate.py::LENS_REFERENCES`, canonical lens headings,
  `skills/strategic-advisor/evals/drift_smoke_cases.json`, retained
  `evidence/evaluations/drift-smoke/run-005/result.json`, and a passing
  pre-fix aggregate validator.

## Routing

- Decision: Fix
- Rationale: This is one bounded post-completion regression in EPIC-006's
  public status surface plus the missing assertion that allowed it. It adds no
  product behaviour, lens, host, release outcome, or independent workstream.
- Related work state: EPIC-006 is Complete.
- Bounded correction: Correct the two README cells and add one focused,
  authority-derived regression guard so future implemented-lens or current
  drift-smoke changes cannot leave those public claims stale.
- New outcome or material decisions: No
- Independent work items: One

## Classification

- Type: Regression
- Mode: Normal
- Severity: Medium
- Impact: The public summary understates an implemented alpha lens and
  misstates the breadth of the only retained current-source behavioural smoke,
  weakening capability and proof-boundary accuracy.
- Urgency: Before EPIC-006 is reviewed for protected-main merge or alpha.4
  publication.
- Owner: John Detlefs

## Related Work

- Originating work: EPIC-006 Technical Architecture And Evidence Grounded
  Invocation, especially TASK-030 Integrate Runtime Packaging And Bounded
  Dogfood
- External links: None

## Risk

- Risk level: Low
- Risks: Duplicating public literals into tests, coupling README claims to an
  unvalidated or stale result, accidentally promoting alpha.4 to public,
  changing canonical runtime bytes, or implying Claude activation/support from
  archive readiness.
- Rollback or containment: Revert the README and focused validator changes.
  Keep `distribution.json` prepared, do not run the publication/finalisation
  path, and retain alpha.3 as the public download authority.

## Fix Plan

- Scope: Derive the README lens list from implemented capability IDs and their
  canonical lens titles; derive the README scenario-group count and current run
  from the validated frozen spec and retained result; add negative fixtures for
  omitted lenses, wrong counts/runs, and changed underlying lens authority;
  inspect and verify the protected release workflow and Claude instructions;
  prove two deterministic standalone alpha.4 builds, exact runtime identity,
  technical-architecture inclusion, and evaluation/private-data exclusion.
- Non-goals: Runtime behaviour changes, new behavioural evaluation, public
  alpha.4 publication or finalisation, push, merge, deployment, GitHub release
  creation, Claude account upload/activation, supported-host promotion, or
  contacting Christina.
- Affected target: Public README claim accuracy, repository claims validation,
  and local prepared-release evidence for the standalone Claude/Codex Skill ZIP.
- Primary repo: .
- Repos touched: .
- Branch, PR, and evidence links: Existing local branch
  `codex/EPIC-006-architecture-invocation`; originating EPIC-006; no PR, push,
  release, or external evidence mutation authorised.
- Verification plan: Run focused validator tests; the complete unit suite; all
  seven validation scopes; deterministic evaluation rebuild check; retained
  `run-005` verifier; release-state check; release-workflow tests; Python compile;
  two clean deterministic artifact builds and byte comparison; independent
  verification bound to the prepared runtime identity and provenance; archive
  inventory/content/hash and privacy checks; diff hygiene; and Workflow Doctor.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | `codex/EPIC-006-architecture-invocation` | None | Local validation and deterministic build outputs only |

## Verification

- Delivered scope: ____
- Verification result: ____
- Adjacent behavior checked: ____
- Original acceptance criteria result: Not applicable
- Regression evidence: ____
- Residual risk: ____

## Outcome

- Disposition: Pending
- Decision: ____
- Closed by: ____
- Closed date: ____
- Promoted to: None
