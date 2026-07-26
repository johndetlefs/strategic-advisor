## User Story

As a maintainer, I want exact-source behavioural and regression evidence for
open-field exploration, so that the Epic closes only if widening, overrides,
evidence reset, and reconvergence are actually observed.

## Parent AC Coverage

- AC6, AC7, AC8, AC10, AC11, AC12

## Acceptance Criteria

- [ ] AC1: Parent AC6, AC7, AC8, and AC10 — all eight synthetic scenario
  families have deterministic required and forbidden assertions.
- [ ] AC2: Parent AC11 — a fresh exact-runtime multi-turn smoke passes the
  frozen open-field, override, reset, and convergence criteria.
- [ ] AC3: Parent AC12 — all repository, package, privacy, workspace,
  personal-context, and workflow regressions pass.

## Goal

Bind the implemented behaviour to current source and record only the claims the
observed evidence supports.

## Approach

Extend the existing bounded drift-smoke machinery, freeze synthetic and
multi-turn authority before accepting outputs, run isolated sessions, retain
source/target identities, and execute full regression.

## Phases

1. Freeze eight synthetic scenario families.
2. Freeze and run the exact-runtime multi-turn smoke.
3. Verify artifacts and complete regression.

## Validation

- AC1: deterministic evaluation inventory and assertion audit.
- AC2: runtime-target-source evidence with exact user turns and binary review.
- AC3: full unit suite, seven-scope validator, evaluation check, repeated
  runtime/install builds, package/privacy scans, and Doctor.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Freeze synthetic authority | Add eight fictional scenario families and required/forbidden assertions before model execution. | AC1 | Run evaluation builder and inspect coverage. | To Do |
| 2 | Freeze runtime smoke | Bind source, package, host/model, access, turns, criteria, and failure handling. | AC2 | Validate smoke specification before outputs. | To Do |
| 3 | Execute and review smoke | Run fresh isolated turns and review every binary criterion. | AC2 | Verify retained result and source identity. | To Do |
| 4 | Run complete regression | Execute tests, validators, repeated packages, privacy, and workflow checks. | AC3 | Review command outputs and hashes. | To Do |

## Parent AC Evidence

- AC6, AC7, AC8, AC10, AC11, AC12: Pending retained exact-source evidence.

## QA & Code Review

- Verdict: Pending.
- Evidence: Pending.
- Findings: Pending.

## Retro

- Reusable lessons: Pending.
- Conventions or agent assets updated: Pending.
- Follow-up tasks: Pending.

## Notes

- Task: TASK-024
- Title: Validate Open-Field Multi-Turn Behaviour
- Created: 2026-07-26
