# Requirements

## Summary

- Task: TASK-021
- Title: Define Open-Field Interaction And Search Contract
- Parent AC Coverage: AC1, AC2, AC3, AC4, AC7, AC8
- Last updated: 2026-07-26

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

- The advisor infers mode, altitude, and search boundary by default.
- The user can override the search boundary in ordinary language at any turn.
- Material framing is visible; routine direct assistance remains direct.
- Clarification is reserved for ambiguity that could materially change the
- Current portfolio records are current-state evidence, not the complete
- Broad outcome-led questions may compare current, adjacent, and outside
- Clean-slate candidate generation retains exact personal context and
- Ideas remain hypotheses until qualifying evidence changes claim support or
- Exploration returns to a bounded decision, test, or discriminating question.
- Retention mode and read/write/disclosure/action/cross-workspace authorities
- No private case data, identifiers, or reconstructable summaries enter public
- One canonical skill remains the source of strategic behaviour.

### Invalid Substitutes

- Adding the word `Explore` without observing genuine uncued alternatives and
- A permanent menu, mode recital, or repeated clarification question in place
- A long list of variations on one mechanism in place of genuinely distinct
- Mentioning an outside option without testing its causal bridge, constraints,
- Treating a user preference, attractive narrative, or stored project as
- Forcing a new project when an existing path is strongest, or retaining a
- Treating “clean slate” as permission to ignore exact personal context,
- Automatically persisting speculative ideas or creating portfolio records.
- Static source inspection in place of exact-runtime multi-turn behaviour.
- Private owner dogfood, a prior model run, or a different host in place of the
- Host-specific prompt copies in place of canonical runtime changes.

### Artifact Targets

- Canonical engagement-mode and search-boundary contract.
- Updated conversational loop and response-framing rules.
- Explicit non-exhaustive portfolio semantics in runtime documentation and
- Plain-language discoverability examples and conversation starters.
- Deterministic synthetic open-field cases with positive and negative
- Fresh exact-runtime multi-turn smoke artifacts bound to source, target, and
- Passing full regression, package, privacy, and workflow validation.

### Parent AC Proof Ownership

- AC1: owner `TASK-021; TASK-022`; required evidence: Canonical source comparison and deterministic contract checks for the orthogonal axes.
- AC2: owner `TASK-021; TASK-022`; required evidence: Runtime contract plus behavioural assertions proving Explore is more than a label.
- AC3: owner `TASK-021; TASK-023`; required evidence: Inference/clarification decision table, source checks, and matched interaction cases.
- AC4: owner `TASK-021; TASK-023`; required evidence: Material-framing and routine-direct-assistance cases with plain-language overrides.
- AC7: owner `TASK-021; TASK-022; TASK-024`; required evidence: Matched bounded-request and no-forced-novelty evidence.
- AC8: owner `TASK-021; TASK-022; TASK-023; TASK-024`; required evidence: Multi-turn override cases preserving personal context and authority boundaries.

## Goal

Define one canonical interaction contract that lets Strategic Advisor infer how
to engage, how high to reason, and how widely to search while keeping those
choices visible and overridable only when they materially affect the answer.

## Non-Goals

- Editing workspace templates or onboarding surfaces owned by TASK-022/023.
- Claiming behavioural success before TASK-024 executes the exact runtime.
- Adding a mandatory mode menu or treating clean slate as context-free.

## Users & Context

- Users who ask either broad outcome-led questions or bounded project
  questions without knowing internal mode vocabulary.
- Returning users who change the desired search boundary in a follow-up turn.

## Requirements (Outcome-Focused)

- R1. Define engagement mode, decision altitude, search boundary, retention
  mode, and authority as orthogonal controls.
- R2. Add `Explore` for unresolved option discovery while preserving
  evidence-only reconvergence.
- R3. Default to autonomous inference, with `dual-track` for broad outcome-led
  questions and `portfolio-bounded` for clearly local requests unless a
  material wider factor changes the answer.
- R4. Require one natural-language framing sentence only when the selected
  boundary could materially change the analysis.
- R5. Ask a boundary question only when bounded and open-field interpretations
  would materially diverge and no responsible assumption is available.
- R6. Accept ordinary-language overrides for current-project-only, clean-slate,
  and comparison analysis at any turn.
- R7. Clean-slate search retains exact personal context, evidence, constraints,
  and authority.
- R8. Do not force novelty or an outside path when the current option is
  strongest.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC1 and AC2 — canonical sources distinguish all five
  control dimensions and define Explore as behavioural divergence plus
  evidence-based reconvergence.
- AC2: Covers parent AC3 — a deterministic decision table defines autonomous
  inference and the material-ambiguity clarification gate.
- AC3: Covers parent AC4 and AC8 — material framing and plain-language
  overrides are explicit while clean-slate search preserves context and
  authority.
- AC4: Covers parent AC7 — bounded requests stay bounded and outside options
  are not forced for novelty.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- D1. Autonomous inference is the default.
- D2. Only material framing is surfaced.
- D3. Clarification is exceptional, not ceremonial.
- D4. Search width and personal-context use are independent.

## Validation Plan

- Static source-contract assertions will check the complete control model,
  defaults, clarification gate, framing sentence, overrides, and no-novelty
  rule. TASK-024 owns exact-runtime observation.
