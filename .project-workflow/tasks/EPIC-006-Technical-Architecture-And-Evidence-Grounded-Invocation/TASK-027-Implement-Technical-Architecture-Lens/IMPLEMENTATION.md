## User Story

As a Strategic Advisor user, I want material architecture choices assessed
through explicit technical ownership, coupling and change-cost mechanisms, so
that frameworks or conceptual neatness do not silently determine topology.

## Parent AC Coverage

- AC3, AC4, AC5

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

## Acceptance Criteria

- [x] AC1: Parent AC3 — canonical allowlisted lens passes structure and
  duplicate-advisor checks.
- [x] AC2: Parent AC4 — project/product and architecture remain complementary
  under one-primary/one-secondary routing.
- [x] AC3: Parent AC5 — approved mechanisms, failure modes and specialist
  boundaries are explicit and case-testable.

## Goal

Implement the seventh selective decision lens without changing the canonical
core's evidence or readiness semantics.

## Approach

Create the lens using the existing domain contract, add canonical routing and
capability/validator declarations, then freeze its distinct boundary before
TASK-029 supplies behavioural cases.

## Phases

1. Author the architecture decision contract.
2. Integrate routing, allowlist and structural validation.
3. Review overlap and specialist boundaries.

## Validation

- AC1-AC3: run lens/skill validation, allowlist checks, negative fixtures and
  TASK-029 routing/mechanism cases.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Define architecture contract | Author distinct outcomes, evidence, mechanisms, ownership, failure modes, boundaries and readiness implications. | AC1, AC3 | Inspect the new lens and run lens validation. | Done |
| 2 | Integrate selective routing | Add canonical routing, allowlist and capability declarations without another advisor or secondary-lens expansion. | AC1, AC2 | Run skill, lens and duplicate-logic checks. | Done |
| 3 | Prove complementarity | Encode project/product ownership, topology discipline, framework evidence and specialist dependencies. | AC2, AC3 | Review source and TASK-029 matched cases. | Done |

## Parent AC Evidence

- AC3: `references/technical-architecture.md` is canonical, allowlisted and structurally validated as the seventh lens; no separate advisor or workflow logic was introduced.
- AC4/AC5: LENS-TA-001 through LENS-TA-006 freeze project/product complementarity, conceptual-versus-physical boundaries, auth ownership, migration, framework authority, proof layers and specialist limits. Run-005 passed the topology, auth and migration cases.

## QA & Code Review

- Verdict: Pass.
- Evidence: lens/skill/claims/privacy scopes, deterministic inventory, runtime manifest inspection, clean package archives and run-005.
- Findings: No blocking overlap. The lens is implemented-not-validated and security/reliability decisions remain specialist dependencies.

## Retro

- Reusable lessons: Conceptual responsibilities need independent ownership/change/deployment evidence before becoming physical topology.
- Conventions or agent assets updated: Seventh-lens structure and architecture probe requirements.
- Follow-up tasks: None; comparative capability promotion remains outside this epic.

## Notes

- Task: TASK-027
- Title: Implement Technical Architecture Lens
- Created: 2026-08-14
