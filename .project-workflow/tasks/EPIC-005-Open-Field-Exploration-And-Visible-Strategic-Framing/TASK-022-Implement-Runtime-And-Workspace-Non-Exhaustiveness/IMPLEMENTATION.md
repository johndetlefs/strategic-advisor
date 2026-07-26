## User Story

As a user with an existing portfolio, I want current projects treated as
candidates and commitments rather than the entire opportunity set, so that the
advisor can identify a better outside path when evidence warrants it.

## Parent AC Coverage

- AC1, AC2, AC5, AC6, AC7, AC8

## Acceptance Criteria

- [x] AC1: Parent AC1 and AC2 — canonical runtime implements the approved search
  and Explore contract.
- [x] AC2: Parent AC5 — workspace portfolio semantics are explicitly
  non-exhaustive.
- [x] AC3: Parent AC6 — broad outcomes can compare current, adjacent, and
  outside hypotheses and reject unsupported bridges.
- [x] AC4: Parent AC7 and AC8 — bounded requests, overrides, context, and
  non-persistence remain intact.

## Goal

Make the current portfolio useful evidence without allowing it to become a
silent search boundary.

## Approach

Edit only canonical runtime and workspace sources, preserve existing context and
authority rules, and add deterministic contract checks and synthetic authority.

## Phases

1. Implement runtime search semantics.
2. Correct workspace portfolio meaning.
3. Freeze broad and bounded behavioural authority.

## Validation

- AC1-AC4: source validation, workspace tests, synthetic inventory checks,
  runtime/package builds, and TASK-024 exact-runtime observation.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Implement search boundaries | Add portfolio-bounded, open-field, and dual-track behaviour to canonical runtime. | AC1, AC3, AC4 | Inspect source and run validator. | Done |
| 2 | Correct portfolio semantics | State that portfolio records are current commitments and candidates, not an exhaustive set. | AC2 | Run workspace template and schema tests. | Done |
| 3 | Protect evidence and persistence | Keep new paths hypothetical and non-durable until evidence and authority justify capture. | AC3, AC4 | Run source-contract and workspace checks. | Done |
| 4 | Freeze broad/bounded cases | Add synthetic required/forbidden assertions for outcome-led widening and no-forced-novelty. | AC3, AC4 | Run evaluation inventory validation. | Done |

## Parent AC Evidence

- AC1, AC2, AC5, AC6, AC7, AC8: Runtime, workspace semantics, and eight
  synthetic scenario families implemented at `b9acb84`; exact-runtime evidence
  remains owned by TASK-024.

## QA & Code Review

- Verdict: Pending.
- Evidence: Pending.
- Findings: Pending.

## Retro

- Reusable lessons: Pending.
- Conventions or agent assets updated: Pending.
- Follow-up tasks: Pending.

## Notes

- Task: TASK-022
- Title: Implement Runtime And Workspace Non-Exhaustiveness
- Created: 2026-07-26
