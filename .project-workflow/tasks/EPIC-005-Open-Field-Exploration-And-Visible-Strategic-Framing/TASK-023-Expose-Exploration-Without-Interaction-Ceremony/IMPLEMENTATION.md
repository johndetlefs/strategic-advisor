## User Story

As a new or returning user, I want to discover that I can bound or widen the
advisor's search using ordinary language, so that useful capabilities are not
hidden behind product terminology.

## Parent AC Coverage

- AC3, AC4, AC8, AC9

## Acceptance Criteria

- [x] AC1: Parent AC3 and AC4 — framing examples show autonomous inference
  without a mandatory menu or routine ceremony.
- [x] AC2: Parent AC8 — plain-language overrides preserve exact context and
  authority.
- [x] AC3: Parent AC9 — portable onboarding and generated starters expose broad
  and bounded use cases from canonical logic.

## Goal

Expose the capability proportionately across portable user-facing surfaces.

## Approach

Update README, installation/onboarding guidance, response examples, and
generated conversation starters while keeping strategic behaviour canonical.

## Phases

1. Add plain-language discoverability.
2. Update portable examples and starters.
3. Verify thin-host and no-ceremony boundaries.

## Validation

- AC1-AC3: source scans, install-artifact tests, runtime packaging, aggregate
  validation, and TASK-024 routine-direct-assistance case.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Document ordinary-language controls | Explain current-only, clean-slate, and compare-both requests without requiring terminology. | AC2, AC3 | Review portable docs and run link checks. | Done |
| 2 | Add broad and bounded examples | Add one outcome-led and one project-bounded example to onboarding/starters. | AC1, AC3 | Build install artifacts and inspect config. | Done |
| 3 | Preserve direct assistance | Ensure framing appears only when material and routine responses remain direct. | AC1 | Run source-contract and synthetic checks. | Done |
| 4 | Verify canonical ownership | Confirm adapters expose but do not duplicate strategic logic. | AC3 | Run runtime/package validators. | Done |

## Parent AC Evidence

- AC3, AC4, AC8, AC9: README, install guidance, architecture, Custom GPT
  starters, response contract, and synthetic no-ceremony authority implemented
  at `b9acb84`; exact-runtime evidence remains owned by TASK-024.

## QA & Code Review

- Verdict: Pass — 2026-07-26.
- Evidence: Reviewed README, installation guidance, architecture, response
  contract, and two identical clean Custom GPT builds. Final packages expose
  compare-both, clean-slate, and current-project-only starters; the focused
  20-test install suite, full 125-test suite, validators, and Doctor pass.
- Findings: Initial QA found that generated starters exposed compare-both and
  clean-slate but not current-project-only. Commit `4295912` corrected the
  omission and added a package regression. No blocking finding remains.

## Retro

- Reusable lessons: Documentation discoverability does not prove host-surface
  discoverability; generated configuration needs its own assertion.
- Conventions or agent assets updated: Install-artifact tests now require all
  three ordinary-language search controls in generated starters.
- Follow-up tasks: Host-specific live activation remains separate from package
  readiness.

## Notes

- Task: TASK-023
- Title: Expose Exploration Without Interaction Ceremony
- Created: 2026-07-26
