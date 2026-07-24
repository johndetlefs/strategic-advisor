# Requirements

## Summary

- Task: TASK-008
- Title: Implement Selective Invocation, Interactive Discovery, Altitude Calibration And Commercial Lenses
- Parent AC Coverage: AC1, AC2, AC3, AC7, AC10, AC11, AC12, AC13, AC14, AC15
- Last updated: 2026-07-24

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for implementation: Yes
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-07-24
- Approval note / source: Dedicated Codex conversation 2026-07-24; owner accepted the pragmatic recovery recommendation and instructed delivery to proceed.
- Approved artifact identity: inherited from the refreshed EPIC-002 envelope `sha256:d315970cc00231d8ce03016378c8949a80a5de982d3b2c7506649761a3c9fefd`

## User Story

As a person making a material professional, business, or marketing decision, I want the advisor to widen and explore only when that could change the answer, so that I get candid strategic help without ceremony on ordinary requests.

## Goal

Ship the canonical conversational behaviour and bounded commercial lenses needed for useful alpha testing while keeping validation and support claims conservative.

## Non-Goals

- Building or repairing the rigorous TASK-007 evaluation system.
- Creating or accessing a private Strategy Workspace.
- Implementing workspace scaffolding, host dogfood, connectors, or later Epic children.
- Treating structural checks or a small qualitative review as behavioural validation.
- Expanding into legal, medical, financial, family, relationship, or general-life advice.

## Users & Context

- Ordinary requests need direct assistance even when they contain project or strategy vocabulary.
- Material decisions may need active exploration and a higher objective or portfolio context before a recommendation is useful.
- Founders and operators need commercial and growth-specific reasoning without having technical delivery mistaken for market validation.

## Requirements (Outcome-Focused)

- R1. Invoke the full protocol only for an explicit or clearly implied material decision, prioritisation, strategic claim, plan, or risk where reality-testing could change action.
- R2. Answer factual, status, summarisation, routine implementation, simple-edit, and casual-ideation requests directly unless the user asks for strategic review or a material decision emerges.
- R3. Begin at the requested decision level; move up only when a broader objective, project role, scarce-capacity conflict, or opportunity cost could materially change the recommendation; then return to a bounded move.
- R4. For unresolved material decisions, use a conversational loop: provisional working position, genuine exploration, evidence-only reality reset, and proportionate convergence. Do not force a readiness verdict before execution advice or commitment exists.
- R5. User ideas and preferences may expand options but do not change claim support or readiness. Surface the strongest live rival and revise only for qualifying evidence, scope, or constraint changes.
- R6. Use business/venture and marketing/growth lenses only for bounded decisions in those domains. Each lens must define evidence, mechanisms, failure modes, readiness implications, and safe boundaries.
- R7. Product documentation and the claim registry describe the two lenses and conversational behaviour as implemented but not validated; no capability is promoted to supported.
- R8. Product behaviour stays canonical under `skills/strategic-advisor/`; private data, evaluation prompts, and host-specific prompt copies stay outside the runtime package.

## Acceptance Criteria (Verifiable)

- AC1: Shared strategic vocabulary routes to direct assistance for ordinary requests and to the full protocol for a material decision.
- AC2: The canonical skill defines minimum-sufficient altitude, genuine exploration, an evidence-only reset, proportionate convergence, and a bounded return.
- AC3: The protocol preserves diagnosis across preference pressure and forbids readiness changes based only on agreement, confidence, repetition, or narrative polish.
- AC4: A business/venture lens distinguishes solution completion from demand, willingness to pay, viable economics, capability, and strategic advantage.
- AC5: A marketing/growth lens distinguishes activity and attributed metrics from incremental customer behaviour and economics.
- AC6: README, architecture, runtime allowlist, and the machine-readable registry include both lenses as implemented-not-validated and retain all existing unsupported-domain boundaries.
- AC7: Existing deterministic validation and unit tests pass, including checks that the new references are required runtime files and remain excluded from evaluation material.
- AC8: A bounded qualitative review of twelve synthetic conversational scenarios records expected routing and contract coverage without claiming behavioural validation.

## Open Questions (Answer Needed)

- None. The owner approved the recovery envelope and the claim boundary.

## Decisions (Resolved)

- D1. TASK-007 is superseded, removed from active work, and non-authoritative; no recovery task or evaluation harness is created.
- D2. TASK-008 owns conversational behaviour plus both bounded commercial lenses for this alpha.
- D3. Testing is proportionate: current repository checks plus twelve synthetic scenario expectations and at most one correction pass.
- D4. Business/venture and marketing/growth remain implemented-not-validated and unsupported.

## Validation Plan

- Run `python3 scripts/build_evals.py --check`, `python3 scripts/validate.py`, `python3 -m unittest discover -s tests -v`, and `git diff --check`.
- Review twelve synthetic scenarios covering direct assistance, material invocation, altitude movement, open exploration, evidence reset, business validation, marketing incrementality, and unsupported-domain boundaries.
- Record qualitative results as implementation review evidence only. Do not use them to promote capability state.
