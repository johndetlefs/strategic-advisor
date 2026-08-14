# Requirements

## Summary

- Task: TASK-029
- Title: Expand Architecture And Baseline Evaluations
- Parent AC Coverage: AC2, AC4, AC5, AC6, AC7, AC8
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

- AC2: owner `TASK-026, TASK-029`; required evidence: Baseline/update normative cases, generated-inventory proof, case results and false-precision negative review.
- AC4: owner `TASK-027, TASK-029`; required evidence: Matched project-product/architecture routing cases and case-level verdicts.
- AC5: owner `TASK-027, TASK-029`; required evidence: Architecture mechanism, ownership, migration, framework and specialist-boundary cases with QA evidence.
- AC6: owner `TASK-028, TASK-029`; required evidence: Stable labelled trigger inventory, category validator negatives and difficult-positive coverage.
- AC7: owner `TASK-028, TASK-029`; required evidence: Matched operational negative controls, over-invocation assertions and case-level verdicts.
- AC8: owner `TASK-029`; required evidence: Synthetic provenance review, privacy scan, deterministic rebuild and runtime-exclusion proof.

## Goal

Turn the audited failure mechanisms into deterministic, synthetic,
non-reconstructable architecture, baseline, routing and over-invocation
regressions.

## Non-Goals

- Copying task transcripts or private workspace/product data.
- Running or claiming the full comparative-effectiveness evaluation.
- Changing frozen thresholds after behavioural output is observed.

## Users & Context

- Maintainers who need normative cases and trigger queries to prevent future
  wrong-baseline, topology and invocation drift.
- Users whose ordinary wording or implementation context sits near the
  invocation boundary.

## Requirements (Outcome-Focused)

- R1. Add baseline cases for stale state, wrong revision, uninspected artifact,
  mismatched scope/incomparability, false precision and later evidence update.
- R2. Add technical-architecture cases for project/product routing,
  responsibility versus topology, presentation/authority boundaries,
  build/adopt/migrate, runtime/data/auth ownership, framework capture,
  migration/rollback and specialist dependencies.
- R3. Expand trigger queries with explicit categories for latent architecture,
  emergent implementation, cross-project/portfolio conflict, evidence update,
  and matched operational negatives.
- R4. Keep every case synthetic and non-reconstructable, regenerate the
  executable inventory deterministically, and preserve runtime exclusion.

## Acceptance Criteria (Verifiable)

- AC1: Parent AC2 — matched baseline/update cases cover every approved gap.
- AC2: Parent AC4/AC5 — architecture cases freeze routing, distinct mechanisms
  and boundary/failure-mode expectations.
- AC3: Parent AC6/AC7 — stable trigger queries cover each difficult positive
  and matched negative category and validator negatives.
- AC4: Parent AC8 — deterministic import, synthetic provenance, privacy scan
  and runtime-exclusion checks pass.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- D1. Extend `core_cases.json`, `lens_cases.json`, `eval_queries.json` and the
  deterministic generated `evals.json`; do not create a new evaluator.
- D2. Use generic mechanisms and invented entities rather than renamed cases.

## Validation Plan

- Generated-inventory equality, required probe/category coverage, malformed and
  missing-case negative tests, privacy/secret scans, runtime package exclusion,
  and human case review before TASK-030 smoke output.
