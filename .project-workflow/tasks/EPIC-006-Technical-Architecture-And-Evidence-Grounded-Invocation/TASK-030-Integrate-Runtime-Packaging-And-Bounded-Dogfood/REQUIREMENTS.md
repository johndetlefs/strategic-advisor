# Requirements

## Summary

- Task: TASK-030
- Title: Integrate Runtime Packaging And Bounded Dogfood
- Parent AC Coverage: AC9, AC10, AC11, AC12, AC13
- Last updated: 2026-08-14

## Owner Approval

- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Inherited from parent epic envelope when unchanged
- Approval date: Inherited from parent epic envelope when unchanged
- Approval note / source: Inherited from parent epic envelope when unchanged
- Approved artifact identity: Inherited from parent epic envelope when unchanged

## Child Charter

### Inherited Invariants

- `skills/strategic-advisor/` remains the only executable source of Strategic
- The evidence-baseline guard remains domain-independent and proportionate;
- Project/product and technical architecture retain distinct ownership; one is
- Conceptual responsibilities do not automatically become packages, services,
- Frameworks, vendors, code, documents, connectors and stored context are
- Specialist security, privacy, legal, financial, safety, reliability and
- Evaluation authority, expected answers, private material and prior outputs
- Only synthetic, public or irreversibly sanitised cases may be committed; no
- Strategy Workspace and Daily Checklist remain separate products/data planes
- Whole-person/personal strategy and operating cadence are not added as lenses
- Capability and release language remains no stronger than exact evidence.
- Any accepted allowlisted runtime-byte change prepares the next immutable
- No new dependency or automation is added unless it enforces an approved

### Invalid Substitutes

- Documentation, static validation, unit tests, model self-assessment, owner
- A bounded smoke or dogfood result in place of comparative evaluation,
- A source-tree invocation, visible skill name, or matching prose in place of
- A package build, archive listing, workflow log, or release-page entry in
- A stale screenshot, obsolete prototype, demonstration state, uninspected
- A framework artifact, vendor recommendation, architecture diagram, passing
- Tests/builds in place of rendered, runtime, usability, security, operational,
- Private task transcripts, Strategy Workspace content, Daily Checklist data,
- Strategy Workspace cadence, Daily Checklist integration, or a separate

### Artifact Targets

- Canonical runtime: `skills/strategic-advisor/SKILL.md`,
- Runtime/package declarations: `skills/strategic-advisor/runtime-manifest.json`,
- Evaluation authority: `skills/strategic-advisor/evals/core_cases.json`,
- Public contract: `PRODUCT-CONTRACT.md`, `ARCHITECTURE.md`, `README.md`,
- Retained proof: child `EVIDENCE.json`, synthetic raw bounded-smoke artifacts
- Workflow: EPIC-006 requirements, contract, decomposition, child task

### Parent AC Proof Ownership

- AC9: owner `TASK-030`; required evidence: Passing runtime-target/source claims, raw bounded-smoke outputs, exact identity and honest result boundary.
- AC10: owner `TASK-030`; required evidence: Runtime/dependency/capability diff proving no cross-product coupling or extra lens.
- AC11: owner `TASK-030`; required evidence: Cross-artifact claim matrix, seven-lens declarations, capability registry and validator pass.
- AC12: owner `TASK-030`; required evidence: Canonical release preparation, exact runtime identity, two byte-identical builds and independent verifier output.
- AC13: owner `TASK-030`; required evidence: Focused/full validation, current-source drift smoke, package/privacy/diff checks, Doctor, child QA and parent audit.

## Goal

Integrate the changed runtime, claims, package and next-alpha preparation, then
observe the exact runtime on bounded synthetic dogfood without overstating what
that observation proves.

## Non-Goals

- Public push, PR, merge, protected-main publication or release finalisation
  without separate authority and exact external evidence.
- Comparative effectiveness, cross-host parity, supported capability or
  private-case publication.

## Users & Context

- Early-alpha users who need one consistent seven-lens package and honest
  maturity language.
- Maintainers who need exact runtime/source identity, deterministic packages,
  bounded current-source smoke and complete QA/closeout evidence.

## Requirements (Outcome-Focused)

- R1. Align canonical/public claims, validator declarations, runtime manifest,
  host metadata and package contents around seven implemented-not-validated
  lenses and no supported capability.
- R2. Preserve Strategy Workspace/Daily Checklist separation, specialist
  boundaries and evaluation/private-data exclusion.
- R3. Prepare the next immutable alpha through `release_state.py` and prove two
  exact deterministic builds plus independent verification while retaining
  public alpha.3 versus prepared-next-alpha distinction.
- R4. Run the exact runtime on the approved synthetic architecture/baseline/
  invocation/control smoke, retain raw outputs and explicit case verdicts, and
  describe results only as bounded observations.
- R5. Complete focused/full validation, QA/review, child evidence, parent audit
  and retro; record failures rather than weakening claims.

## Acceptance Criteria (Verifiable)

- AC1: Parent AC9 — exact runtime-target/source smoke satisfies the approved
  case mix with raw artifacts and honest boundaries.
- AC2: Parent AC10/AC11 — cross-artifact/dependency diff proves seven lenses,
  no cross-product coupling, no extra lens and no stronger claim.
- AC3: Parent AC12 — canonical next-alpha preparation and two independently
  verified byte-identical package builds pass.
- AC4: Parent AC13 — full validation, drift smoke, privacy/diff hygiene,
  workflow Doctor, QA, audit and retro pass or retain blocking evidence.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- D1. Use alpha.4 as the next sequential prepared distribution unless current
  release authority changes before preparation.
- D2. Extend the bounded drift-smoke authority rather than create a new
  comparative evaluator.
- D3. Retain only synthetic public evidence; exact owner/product cases remain
  outside the repository.

## Validation Plan

- Runtime-target/source evidence, raw smoke artifacts and verifier; claim/dependency
  diff; canonical release preparation; two clean package builds and independent
  verifier; focused/full tests, all scopes, privacy, Doctor, QA and parent audit.
