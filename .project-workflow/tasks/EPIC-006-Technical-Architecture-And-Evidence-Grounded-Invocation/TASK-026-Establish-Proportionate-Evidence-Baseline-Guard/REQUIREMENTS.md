# Requirements

## Summary

- Task: TASK-026
- Title: Establish Proportionate Evidence Baseline Guard
- Parent AC Coverage: AC1, AC2
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

- AC1: owner `TASK-026`; required evidence: Canonical core diff plus matched baseline/direct-assistance assertions and QA verdict.
- AC2: owner `TASK-026, TASK-029`; required evidence: Baseline/update normative cases, generated-inventory proof, case results and false-precision negative review.

## Goal

Prevent Strategic Advisor from scoring or recommending against the wrong
decision object or product state while keeping routine direct assistance
proportionate.

## Non-Goals

- Architecture-lens rules, trigger inventory expansion, package publication,
  and behavioural-validation claims.
- A mandatory evidence form for every response.

## Users & Context

- Users comparing products, repositories, revisions, environments, states, or
  journeys where a stale or uninspected baseline could reverse the conclusion.
- Users asking routine questions where those identities cannot change the
  answer and no strategic preflight is warranted.

## Requirements (Outcome-Focused)

- R1. Canonical core instructions identify only the decision-object, artifact,
  state, revision, environment, scope and journey fields material to the live
  decision.
- R2. Inspected observations remain distinct from reports and assumptions.
- R3. A material stale, missing, incomparable or mismatched baseline blocks
  scoring and commitment advice until inspected or bounded by the cheapest
  decisive check.
- R4. Qualifying current evidence causes an explicit baseline and conclusion
  update; routine direct assistance remains direct.

## Acceptance Criteria (Verifiable)

- AC1: Parent AC1 — canonical source and fail-closed validators encode the
  proportionate baseline gate without imposing it on routine assistance.
- AC2: Parent AC2 — source-level matched fixtures reject stale/uninspected/
  mismatched scoring and require revision after qualifying evidence updates.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- D1. Put the guard in `references/evidence.md`, route it from `SKILL.md`, and
  connect it to selective activation in `conversational-strategy.md`.
- D2. Validate required semantics and negative fixtures deterministically;
  TASK-029 owns normative model cases.

## Validation Plan

- Focused validator unit tests, aggregate `skill` and `evals` scopes, canonical
  source review, and TASK-029 matched behavioural case definitions.
