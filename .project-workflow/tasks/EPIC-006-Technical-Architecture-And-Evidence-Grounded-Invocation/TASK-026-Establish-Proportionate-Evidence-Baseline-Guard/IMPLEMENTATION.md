## User Story

As a Strategic Advisor user, I want consequential advice grounded in the exact
current decision object, so that rigorous reasoning cannot be applied to a
stale, uninspected, or mismatched baseline.

## Parent AC Coverage

- AC1, AC2

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

## Acceptance Criteria

- [ ] AC1: Parent AC1 — canonical runtime requires a proportionate evidence-
  baseline gate and blocks unsupported scoring/commitment advice.
- [ ] AC2: Parent AC2 — deterministic negative fixtures cover stale state,
  wrong revision, uninspected artifacts, scope mismatch and evidence updates.

## Goal

Add one domain-independent baseline guard before architecture and routing work
builds on the canonical protocol.

## Approach

Define a compact decision-object preflight in the evidence protocol, reference
it from the reality protocol and conversational activation rule, then make the
validator fail when the material safeguards disappear.

## Phases

1. Add the canonical baseline contract.
2. Add deterministic source and negative-fixture validation.
3. Hand matched model-case ownership to TASK-029.

## Validation

- AC1: inspect canonical runtime and run `python3 scripts/validate.py --scope skill`.
- AC2: run focused validator tests and the generated evaluation checks.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Define evidence baseline | Add exact-object/state/revision/scope inspection and report/assumption separation proportionately. | AC1 | Inspect canonical diff and run skill validation. | To Do |
| 2 | Fail closed on material mismatch | Block scores and commitments when baseline gaps could overturn the decision; require evidence-led revision. | AC1, AC2 | Run focused negative validator fixtures. | To Do |
| 3 | Preserve direct assistance | Keep the preflight conditional on consequential decisions rather than every response. | AC1 | Review matched source rules and routine control. | To Do |

## Parent AC Evidence

- AC1, AC2: Pending canonical diff, focused tests, TASK-029 cases and QA review.

## QA & Code Review

- Verdict: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-026
- Title: Establish Proportionate Evidence Baseline Guard
- Created: 2026-08-14
