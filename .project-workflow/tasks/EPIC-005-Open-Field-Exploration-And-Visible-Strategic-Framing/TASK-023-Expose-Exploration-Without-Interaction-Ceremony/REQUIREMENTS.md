# Requirements

## Summary

- Task: TASK-023
- Title: Expose Exploration Without Interaction Ceremony
- Parent AC Coverage: AC3, AC4, AC8, AC9
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

- AC3: owner `TASK-021; TASK-023`; required evidence: Inference/clarification decision table, source checks, and matched interaction cases.
- AC4: owner `TASK-021; TASK-023`; required evidence: Material-framing and routine-direct-assistance cases with plain-language overrides.
- AC8: owner `TASK-021; TASK-022; TASK-023; TASK-024`; required evidence: Multi-turn override cases preserving personal context and authority boundaries.
- AC9: owner `TASK-023`; required evidence: Portable onboarding/installation/source comparison and discoverability tests.

## Goal

Make open-field exploration discoverable through ordinary language and
portable examples without forcing users through mode vocabulary, repeated
questions, or response ceremony.

## Non-Goals

- A graphical settings interface or persistent mode selector.
- Host-specific strategic logic or divergent prompt copies.
- Behavioural effectiveness claims owned by TASK-024.

## Users & Context

- New and returning users who do not know that they can bound analysis to
  current projects, widen it, or compare both.
- Users receiving routine assistance that should remain concise and direct.

## Requirements (Outcome-Focused)

- R1. Document three plain-language controls: current projects only, clean
  slate, and compare both.
- R2. Explain that clean slate widens candidate vehicles but retains personal
  context and established constraints.
- R3. Add one broad-outcome and one bounded-project example to portable
  onboarding or conversation starters.
- R4. Ensure model-visible response guidance surfaces one framing sentence only
  when material and omits mode recital for routine assistance.
- R5. Keep host adapters thin and source all behaviour from the canonical skill.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC3 and AC4 — visible-framing guidance and examples express
  autonomous inference without a mandatory menu.
- AC2: Covers parent AC8 — all three plain-language overrides preserve context
  and authority semantics.
- AC3: Covers parent AC9 — README, installation/onboarding, and generated
  conversation starters expose both broad and bounded use cases without
  duplicating canonical logic.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- D1. Progressive disclosure is the discoverability mechanism.
- D2. Product terminology may appear in documentation but is not required user
  vocabulary.
- D3. Routine assistance does not announce mode or boundary.

## Validation Plan

- Static source comparisons and install-artifact tests will verify portable
  wording, starter coverage, thin adapters, and the absence of framing ceremony
  in the direct-assistance contract.
