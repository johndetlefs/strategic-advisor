## User Story

As a Strategic Advisor user, I want the advisor to infer and reveal the useful
strategic frame proportionately, so that I can receive broad or bounded help
without learning internal modes or being trapped inside my current projects.

## Parent AC Coverage

- AC1, AC2, AC3, AC4, AC7, AC8

## Acceptance Criteria

- [x] AC1: Parent AC1 and AC2 — the canonical contract separates engagement,
  altitude, search boundary, retention, and authority and makes Explore
  behavioural.
- [x] AC2: Parent AC3 — autonomous inference and clarification use the approved
  material-ambiguity decision rule.
- [x] AC3: Parent AC4 and AC8 — material framing and all three ordinary-language
  overrides are explicit and preserve context.
- [x] AC4: Parent AC7 — bounded requests remain bounded and novelty is not
  forced.

## Goal

Freeze the interaction and search-boundary contract before downstream runtime,
onboarding, and behavioural proof changes.

## Approach

Update the canonical skill and conversational/response references with the
orthogonal control model and deterministic selection rules. Add static
validators that fail on incomplete or conflated contracts.

## Phases

1. Define the control model and inference defaults.
2. Define clarification, framing, and override behaviour.
3. Add fail-closed source-contract validation.

## Validation

- AC1-AC4: canonical-source assertions, aggregate validator, runtime packaging,
  and downstream TASK-024 behavioural authority.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Define orthogonal controls | Add engagement, altitude, search, retention, and authority separation plus Explore behaviour. | AC1 | Inspect canonical runtime and run source validation. | Done |
| 2 | Define inference and clarification | Encode broad/ bounded defaults and the material-ambiguity question gate. | AC2, AC4 | Run matched source-contract checks. | Done |
| 3 | Define visible overrides | Encode one-sentence material framing and ordinary-language boundary changes without losing context. | AC3 | Inspect response contract and run validation. | Done |
| 4 | Add contract regressions | Extend deterministic validators to fail incomplete, ceremonial, or novelty-forcing variants. | AC1, AC2, AC3, AC4 | Run focused and aggregate validation. | Done |

## Parent AC Evidence

- AC1, AC2, AC3, AC4, AC7, AC8: Canonical source and fail-closed validation
  implemented at `b9acb84`; behavioural evidence remains owned by TASK-024.

## QA & Code Review

- Verdict: Pending.
- Evidence: Pending.
- Findings: Pending.

## Retro

- Reusable lessons: Pending.
- Conventions or agent assets updated: Pending.
- Follow-up tasks: Pending.

## Notes

- Task: TASK-021
- Title: Define Open-Field Interaction And Search Contract
- Created: 2026-07-26
