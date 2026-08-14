## User Story

As a Strategic Advisor maintainer, I want the audited gaps frozen as synthetic
regressions, so that future changes cannot quietly lose the baseline guard,
architecture discipline, or selective-invocation boundary.

## Parent AC Coverage

- AC2, AC4, AC5, AC6, AC7, AC8

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

- AC2: owner `TASK-026, TASK-029`; required evidence: Baseline/update normative cases, generated-inventory proof, case results and false-precision negative review.
- AC4: owner `TASK-027, TASK-029`; required evidence: Matched project-product/architecture routing cases and case-level verdicts.
- AC5: owner `TASK-027, TASK-029`; required evidence: Architecture mechanism, ownership, migration, framework and specialist-boundary cases with QA evidence.
- AC6: owner `TASK-028, TASK-029`; required evidence: Stable labelled trigger inventory, category validator negatives and difficult-positive coverage.
- AC7: owner `TASK-028, TASK-029`; required evidence: Matched operational negative controls, over-invocation assertions and case-level verdicts.
- AC8: owner `TASK-029`; required evidence: Synthetic provenance review, privacy scan, deterministic rebuild and runtime-exclusion proof.

## Acceptance Criteria

- [ ] AC1: Parent AC2 — baseline mismatch/update cases are complete.
- [ ] AC2: Parent AC4/AC5 — architecture routing/mechanism cases are complete.
- [ ] AC3: Parent AC6/AC7 — difficult positive and matched negative trigger
  categories are complete and fail-closed validated.
- [ ] AC4: Parent AC8 — inventory, provenance, privacy and runtime isolation
  pass deterministically.

## Goal

Expand the current 45-case/28-query authority before any new smoke output is
generated.

## Approach

Add the smallest case set that covers every approved mechanism, assign stable
probe/category metadata, extend validators and negative fixtures, regenerate
the canonical executable inventory, and review sanitisation before execution.

## Phases

1. Add baseline and architecture normative cases.
2. Add latent/emergent positive and matched negative trigger queries.
3. Enforce coverage, provenance and isolation deterministically.

## Validation

- AC1-AC4: `build_evals.py --check`, eval/privacy/skill scopes, focused
  validator/build tests, package inventory inspection and human case review.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Add baseline regressions | Freeze wrong-state/revision/artifact/scope and evidence-update behaviour without private case details. | AC1, AC4 | Inspect cases and run deterministic build/coverage checks. | To Do |
| 2 | Add architecture regressions | Freeze routing, topology, ownership, framework, migration and specialist-boundary decisions. | AC2, AC4 | Inspect cases and run lens/eval validation. | To Do |
| 3 | Expand trigger boundary | Add stable labelled latent/emergent/cross-project/update positives and factual/routine/status/fix/build negatives. | AC3, AC4 | Run trigger validation and negative fixtures. | To Do |
| 4 | Prove isolation and provenance | Regenerate `evals.json`; verify synthetic provenance, privacy and runtime exclusion. | AC4 | Run builder, privacy scope and package inventory check. | To Do |

## Parent AC Evidence

- AC2, AC4, AC5, AC6, AC7, AC8: Pending case inventory, deterministic build,
  validator/privacy results and QA review.

## QA & Code Review

- Verdict: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-029
- Title: Expand Architecture And Baseline Evaluations
- Created: 2026-08-14
