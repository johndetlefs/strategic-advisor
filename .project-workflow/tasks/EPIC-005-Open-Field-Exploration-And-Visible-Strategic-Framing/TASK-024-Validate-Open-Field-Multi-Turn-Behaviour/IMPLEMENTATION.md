## User Story

As a maintainer, I want exact-source behavioural and regression evidence for
open-field exploration, so that the Epic closes only if widening, overrides,
evidence reset, and reconvergence are actually observed.

## Parent AC Coverage

- AC6, AC7, AC8, AC10, AC11, AC12

## Acceptance Criteria

- [x] AC1: Parent AC6, AC7, AC8, and AC10 — all eight synthetic scenario
  families have deterministic required and forbidden assertions.
- [x] AC2: Parent AC11 — a fresh exact-runtime multi-turn smoke passes the
  frozen open-field, override, reset, and convergence criteria.
- [x] AC3: Parent AC12 — all repository, package, privacy, workspace,
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
| 1 | Freeze synthetic authority | Add eight fictional scenario families and required/forbidden assertions before model execution. | AC1 | Run evaluation builder and inspect coverage. | Done |
| 2 | Freeze runtime smoke | Bind source, package, host/model, access, turns, criteria, and failure handling. | AC2 | Validate smoke specification before outputs. | Done |
| 3 | Execute and review smoke | Run fresh isolated turns and review every binary criterion. | AC2 | Verify retained result and source identity. | Done |
| 4 | Run complete regression | Execute tests, validators, repeated packages, privacy, and workflow checks. | AC3 | Review command outputs and hashes. | Done |

## Parent AC Evidence

- AC6, AC7, AC8, AC10, AC11: Frozen synthetic authority and exact-runtime
  `run-003` pass against source `b9acb84` and runtime identity
  `fbe0b4f80d3af8c373f728549c1011e3e3d70212400fc3c4e7a7166c0691eaee`.
- AC12: The final 125-test suite, seven validation scopes, Workflow Doctor,
  two identical clean package builds, two independent trusted-identity
  verifications, and archive inspection pass at `4295912`.

## QA & Code Review

- Verdict: Pass — 2026-07-26.
- Evidence: Run-003 passes every frozen criterion across six scenario groups,
  seven fresh sessions, and 21 actual turns against runtime identity
  `fbe0b4f8…`. The machine verifier, 45-case inventory, 125 tests, seven
  validation scopes, privacy and claims checks, two identical clean release
  builds, two independent artifact verifications, and Workflow Doctor pass.
- Findings: The external runtime call was paused until the owner explicitly
  approved the generic runtime and fictional prompt transmission. Execution
  then remained within the installed-runtime read boundary. No model reasoning
  trace or private workspace content was retained. No blocking finding remains.

## Retro

- Reusable lessons: A search-boundary feature needs multi-turn proof; a
  plausible first response does not prove that overrides, evidence reset, and
  reconvergence survive pressure.
- Conventions or agent assets updated: Drift-smoke authority now includes
  DRIFT-006 and dynamically validates the six-case current suite.
- Follow-up tasks: Comparative effectiveness and owner/colleague pilots remain
  separate evidence gates.

## Notes

- Task: TASK-024
- Title: Validate Open-Field Multi-Turn Behaviour
- Created: 2026-07-26
