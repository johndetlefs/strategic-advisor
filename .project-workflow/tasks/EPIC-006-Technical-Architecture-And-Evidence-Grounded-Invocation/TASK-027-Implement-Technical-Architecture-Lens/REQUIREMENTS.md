# Requirements

## Summary

- Task: TASK-027
- Title: Implement Technical Architecture Lens
- Parent AC Coverage: AC3, AC4, AC5
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

- AC3: owner `TASK-027`; required evidence: Canonical lens, runtime allowlist, lens validator and duplicate-advisor scan.
- AC4: owner `TASK-027, TASK-029`; required evidence: Matched project-product/architecture routing cases and case-level verdicts.
- AC5: owner `TASK-027, TASK-029`; required evidence: Architecture mechanism, ownership, migration, framework and specialist-boundary cases with QA evidence.

## Goal

Add one selective technical/system architecture lens that improves material
technical commitments without duplicating project/product or specialist work.

## Non-Goals

- A separate advisor, framework implementation guide, security audit,
  repository reorganisation, or host-specific prompt copy.
- Behavioural validation, trigger expansion, and release publication.

## Users & Context

- Users choosing boundaries, sharing, topology, ownership, build/adopt/migrate
  paths, or hard-to-reverse runtime/data/auth architecture.
- Project/product users whose intended outcome remains primary and needs only a
  material architecture secondary lens.

## Requirements (Outcome-Focused)

- R1. Add an allowlisted `technical-architecture.md` lens with the standard lens
  contract and the approved distinct mechanisms, evidence and failure modes.
- R2. Route it from canonical `SKILL.md` as one primary or material secondary
  lens while preserving at most one secondary.
- R3. Distinguish conceptual responsibilities from technical topology and test
  simpler/reversible rivals, coexistence, rollback and future change cost.
- R4. Keep project/product outcome ownership and specialist/security
  boundaries explicit; treat framework/vendor artifacts as evidence.

## Acceptance Criteria (Verifiable)

- AC1: Parent AC3 — the lens is canonical, allowlisted, structurally validated
  and introduces no second advisor.
- AC2: Parent AC4 — routing and lens text preserve project/product
  complementarity and the one-secondary limit.
- AC3: Parent AC5 — mechanisms and failure modes cover topology, ownership,
  migration, framework capture and specialist boundaries.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- D1. Use the existing lens headings and validator architecture.
- D2. Add `domain.technical-architecture` as implemented-not-validated; TASK-030
  owns public cross-artifact claim alignment.

## Validation Plan

- Lens validator and negative fixtures, runtime allowlist/duplicate-logic scan,
  canonical review, and TASK-029 matched routing/mechanism cases.
