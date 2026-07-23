## User Story

As a person making a material professional, business, or marketing decision, I want the advisor to widen and explore only when that could change the answer, so that I get candid strategic help without ceremony on ordinary requests.

## Parent AC Coverage

- AC1, AC2, AC3, AC7, AC10, AC11, AC12, AC13, AC14, AC15

## Goal

Implement the owner-approved TASK-008 product behaviour in the canonical skill, package it deterministically, and leave rigorous behavioural validation for later.

## Approach

- Extend the core skill with intent-sensitive invocation and a minimum-sufficient-altitude conversational loop.
- Add concise business/venture and marketing/growth references that specialise the existing evidence and readiness protocol.
- Update public claim surfaces and runtime allowlists without promoting support.
- Add structural contract tests and review a fixed twelve-scenario synthetic checklist; do not build a new evaluator.

## Phases

1. Canonical behaviour: implement routing, altitude, exploration, reality reset, and convergence.
2. Commercial lenses: add bounded business and marketing references and route them from the core.
3. Packaging and claims: update manifest, public documentation, and implemented-not-validated states.
4. Validation and review: run existing checks, scenario review, QA/code review, and retro.

## Acceptance Criteria

- AC1: Shared vocabulary routes ordinary requests directly and material strategic decisions through the full protocol.
- AC2: Minimum-sufficient altitude, active exploration, evidence reset, convergence, and bounded return are explicit in canonical behaviour.
- AC3: Preference or repetition alone cannot change diagnosis or readiness.
- AC4: The business/venture lens covers commercial evidence, economics, capability, position, and staged commitment.
- AC5: The marketing/growth lens covers audience, positioning, message, channel, incremental effect, economics, and bounded experiments.
- AC6: Public and packaged artifacts include the behaviour and lenses only as implemented-not-validated.
- AC7: Existing deterministic checks and unit tests pass.
- AC8: Twelve synthetic scenarios receive a recorded qualitative contract review without capability promotion.

## Validation

- Run the current deterministic build check, repository validator, full unit suite, and diff whitespace check.
- Review twelve synthetic scenarios against the written routing and lens contracts.
- Treat the scenario review as implementation feedback only, not as behavioural validation or support evidence.

## Task List

|  ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Implement conversational routing | Add intent-sensitive invocation, minimum-sufficient altitude, exploration, evidence reset, and convergence to canonical behaviour. | AC1, AC2, AC3 | Inspect `SKILL.md` and the conversational reference. | Done |
| 2 | Add commercial lenses | Add bounded business/venture and marketing/growth evidence contracts and route them from the core. | AC4, AC5 | Inspect both lens references and routing boundaries. | Done |
| 3 | Align package and claims | Include new runtime files and update public capability language without promoting support. | AC6 | Run repository validator and inspect the claim registry. | Done |
| 4 | Validate proportionately | Run existing checks and record the twelve-scenario qualitative review. | AC7, AC8 | Review command output and scenario record. | Done |
| 5 | Complete QA and retro | Run the project QA/code-review gate and record reusable lessons. | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8 | Inspect QA and retro sections. | Done |

## Parent AC Evidence

- AC1: `SKILL.md`, `references/conversational-strategy.md`, and S04/S11 in `SCENARIO-REVIEW.md` cover working position, exploration, convergence, and direct-assistance control.
- AC2: The minimum-sufficient-altitude ladder plus S05/S06 demonstrate step-up only for a material upstream constraint and return to a bounded action.
- AC3: The evidence-only reset and S09/S10 preserve the same diagnosis across opposite preferences on identical facts.
- AC7: The canonical behavior has no workspace prerequisite; all twelve synthetic scenarios were reviewed without a workspace.
- AC10: `README.md`, `ARCHITECTURE.md`, and `PRODUCT-CONTRACT.md` keep all new behavior and lenses at implemented-not-validated with no supported capability promotion.
- AC11: S01-S03 remain direct assistance while S04 activates the material-decision protocol despite shared project vocabulary.
- AC12: S11 remains open exploration without a manufactured verdict; S04-S10 converge only around a candidate action.
- AC13: Invocation depends on decision intent rather than repository or workspace location; S01 remains direct assistance inside the repository context.
- AC14: `references/business-venture.md` and S07 distinguish completion and praise from a real offer, payment behavior, economics, and staged commitment.
- AC15: `references/marketing-growth.md` and S08 distinguish platform attribution from incrementality and contribution economics.

## QA & Code Review

- Verdict: Pass
- Evidence: `python3 scripts/build_evals.py --check` passed; `python3 scripts/validate.py` passed all 7 scopes; `python3 -m unittest discover -s tests -v` passed 95 tests; targeted post-review tests passed 3 of 3; `git diff --check` passed; workflow Doctor passed; qualitative synthetic review passed 12 of 12 against the written contract.
- Findings: No blocking correctness, scope, privacy, packaging, leakage, or claim-boundary findings. Code review corrected one conflict between open exploration and the prior forced-readiness wording. The existing 31-case evaluation inventory predates the new interactive and commercial behavior and remains non-authoritative for effectiveness; no host, behavioral, or support claim is made.

## Retro

- Date: 2026-07-24
- Reusable lessons: Treat fail-closed evaluation as a claim boundary, not an automatic feature-delivery blockade. Keep conversational strategy proportional by testing intent routing, altitude changes, evidence reset, and bounded return rather than requiring every reply to exhibit the full protocol. Resolve contradictions between core and reference files during review, especially around when readiness is required.
- Conventions or agent assets updated: `.project-workflow/guidance.md` now separates implementation readiness from capability validation and requires a live claim or promotion gate before evaluation machinery is expanded.
- Follow-up tasks: TASK-007 is superseded and removed from active work. Create a new current-source evaluation task only if a rigorous comparative, validated, or supported claim is proposed.
- Missed in-scope work: None. Private Strategy Workspace work, host dogfood, and later EPIC-002 children remain intentionally untouched.

## Notes

- Task: TASK-008
- Title: Implement Selective Invocation, Interactive Discovery, Altitude Calibration And Commercial Lenses
- Created: 2026-07-24
- The private Strategy Workspace and later EPIC-002 children are explicitly excluded.
