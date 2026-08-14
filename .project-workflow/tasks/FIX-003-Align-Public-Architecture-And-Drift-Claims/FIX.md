# Fix

## Summary

- Fix: FIX-003
- Title: Align Public Architecture And Drift Claims
- Status: Complete
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

- Delivered scope: Corrected the README to name all seven canonical
  implemented-not-validated lenses and the twelve-group `run-005` smoke. The
  claims validator now derives lens names from every implemented domain in the
  product contract, the canonical lens-reference mapping, and the lens H1; it
  derives the scenario count/current run only after the frozen spec and retained
  result verify.
- Verification result: Pass. All 142 tests, all seven validation scopes, the
  56-case evaluation rebuild check, the retained twelve-group `run-005`
  verifier, release-state check, Python compilation, diff hygiene, privacy
  checks, and Workflow Doctor passed. The 27 focused release-state,
  publication-workflow, and install-artifact tests also passed.
- Adjacent behavior checked: `distribution.json` still identifies alpha.3 as
  current public and alpha.4 as prepared. The main-push release workflow reads
  that prepared intent, runs the complete source gate, builds and verifies
  twice, conditionally creates immutable `v0.2.0-alpha.4` with all four assets,
  then freshly downloads and independently verifies them. `INSTALL.md` directs
  managed Claude Enterprise users to upload `strategic-advisor.zip` unchanged,
  enable it, and verify a visible Skill activation in a fresh chat.
- Original acceptance criteria result: EPIC-006's public seven-lens,
  implemented-not-validated and prepared-not-published boundaries now agree
  with the public README; the Epic remains closed and is not reopened.
- Regression evidence: Four focused negative fixtures prove that the claims
  scope rejects an omitted technical lens, a stale scenario count/run, a
  changed canonical lens title, and a newly implemented contract domain with no
  canonical lens authority. These fixtures interrogate the underlying
  authorities rather than blessing duplicated README literals.
- Residual risk: Local package readiness does not publish alpha.4, make it the
  current public download, prove Christina's account has the required Claude
  controls, prove an in-place host-version replacement UI, or prove Claude
  activation/behaviour. Those remain external lifecycle and exact-host checks.

### Prepared artifact proof

- Exact clean source revision: `a6a92512b098e3e87cbf9a16e64eba96774f7abb`
- Distribution version/state: `0.2.0-alpha.4` / `prepared`
- Current public version: `0.2.0-alpha.3`
- Runtime package identity:
  `0dd720757af6ccda598f2333b74ef055af625e48f10bb7824cced064c9f15bf1`
- Standalone Skill ZIP:
  `c7d40e023315d054e0422df196bb1face5a4c02dca6eb2fd66c67b44b335d1ab`
- OpenAI local-marketplace ZIP:
  `2d965ce233cef649774f1bf72d0911f190c9e2629a3f78d77507ea5a4e8453ee`
- ChatGPT kit ZIP:
  `4c09dfe3b91beb2927f22e0d206fe44acdee9399a4c001bd281264eb75e6623d`
- Install provenance:
  `025326ff8f6133b6a91ba497edc564ea9d36178faaeebfb30b87c5d9e5d16e80`
- The two complete builds were byte-identical. Both trusted independent
  verifications passed. The standalone archive's
  `references/technical-architecture.md` SHA-256
  `cb9d109052e1aaf8e5e36e6641dec330e15de7345789281d415d377ed1043289`
  exactly matched canonical source; no evaluation/result path or inspected
  private-data marker was present.

## QA & Code Review

- Date: 2026-08-14
- Reviewed areas: Fix classification and scope; README accuracy; authority
  derivation; fail-closed handling; regression strength; canonical-runtime and
  distribution-state preservation; release workflow; Claude instructions;
  archive inventory, provenance, privacy, and exact-source boundaries.
- Acceptance evidence: The owner-approved envelope is covered by the public
  diff, four authority-sensitive negative fixtures, the full repository gate,
  and the two exact clean artifact builds recorded above.
- Findings: No blocking or non-blocking code, documentation, privacy, packaging,
  or workflow finding remains in the bounded Fix.
- Verdict: Pass. This proves local implementation and prepared artifact
  readiness only; publication, public finalisation, and exact Claude account
  activation remain outside this Fix.

## Prevention / Retro

- Durable prevention is the new claims-scope assertion tied to the product
  contract, canonical lens titles, frozen smoke spec, and verified current run.
- No separate retro task is warranted: the prevention gap was bounded, fixed in
  the same work item, and introduced no reusable process or workflow change
  beyond the regression guard.

## Outcome

- Disposition: Fixed
- Decision: Aligned public seven-lens and twelve-group run-005 claims with canonical authorities and added authority-derived regression coverage without publishing alpha.4.
- Closed by: Codex
- Closed date: 2026-08-14
- Promoted to: None
