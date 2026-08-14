# Requirements

## Summary

- Task: TASK-028
- Title: Strengthen Latent And Emergent Invocation
- Parent AC Coverage: AC6, AC7
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

- AC6: owner `TASK-028, TASK-029`; required evidence: Stable labelled trigger inventory, category validator negatives and difficult-positive coverage.
- AC7: owner `TASK-028, TASK-029`; required evidence: Matched operational negative controls, over-invocation assertions and case-level verdicts.

## Goal

Recognise material architecture decisions expressed in ordinary language or
emerging during implementation while preserving strong direct-assistance
controls.

## Non-Goals

- Automatic invocation for code/architecture vocabulary alone, generic
  strategic ceremony, or reopening unchanged approved directions.
- Authoring the architecture lens or evaluation cases owned by sibling tasks.

## Users & Context

- Users asking for a “sense check” or “right way to structure this”.
- Implementers who discover a newly hard-to-reverse cross-project or system
  boundary after routine work has begun.

## Requirements (Outcome-Focused)

- R1. Canonical activation recognises ordinary-language material decisions
  without requiring strategy or architecture keywords.
- R2. Mid-implementation activation requires a newly exposed material,
  hard-to-reverse decision that could change the approved action; name and
  bound the checkpoint, then return to implementation.
- R3. Factual explanation, status, approved implementation, local setup,
  simple fixes, mechanical refactors, tests and builds remain direct.
- R4. Trigger validation records explicit difficult categories and rejects
  absent or mislabelled coverage.

## Acceptance Criteria (Verifiable)

- AC1: Parent AC6 — source rules and category validation support latent,
  emergent, cross-project/portfolio and evidence-update positives.
- AC2: Parent AC7 — source rules preserve the approved operational negative
  controls and require a genuinely new decision before shifting.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- D1. Extend selective activation in canonical source; do not add a host prompt.
- D2. TASK-029 owns concrete query inventory and case assertions.

## Validation Plan

- Focused source/validator tests, category-negative fixtures, TASK-029 trigger
  inventory, and TASK-030 exact-runtime smoke.
