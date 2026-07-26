# Requirements

## Summary

- Task: EPIC-005
- Title: Open-Field Exploration And Visible Strategic Framing
- Last updated: 2026-07-26

## Owner Approval

- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Not approved
- Approval date: Not approved
- Approval note / source: Not approved
- Approved artifact identity: Not approved

## Goal

Strategic Advisor should infer the most useful strategic frame by default while
making consequential framing choices visible and easy to override. A user's
current projects, roles, and workspace records should inform opportunity cost
and feasibility without silently becoming the complete option set.

For broad outcome-led questions, the advisor must be capable of comparing
current-portfolio vehicles with adjacent or entirely new pathways. It must also
remain proportionate: ordinary project questions should not trigger repetitive
mode menus or unbounded brainstorming.

## Non-Goals

- A permanent mode-selection questionnaire at the start of every conversation.
- Treating “clean slate” as context-free analysis; exact personal objectives,
  constraints, evidence, and authorities still apply.
- Requiring novelty, an outside-portfolio recommendation, or a fixed number of
  options when the current path is clearly strongest.
- Treating exploration ideas as evidence, approved projects, durable
  commitments, or readiness.
- Automatically writing speculative opportunities into a Strategy Workspace.
- Building a graphical interface, settings product, database, connector, or
  host-specific orchestration layer.
- Providing medical, clinical, financial, investment, tax, legal, or other
  specialist advice beyond the existing product boundary.
- Copying private Strategy Workspace content into product source, evaluation
  cases, logs, or public artifacts.

## Users & Context

The product remains for generic individual users. Initial owner dogfood uses a
private Strategy Workspace containing current projects plus exact personal
objectives and constraints, but the product must transfer to colleagues using
their own accounts, repositories, and optional workspaces.

The key interaction problem is progressive disclosure. Most users will not know
the names of the engagement modes or search boundaries. The advisor should
therefore infer them from the request, reveal the framing only when it could
materially affect the answer, accept plain-language overrides, and ask one short
clarifying question only when rival interpretations would produce materially
different analysis and a safe default is unavailable.

## Requirements (Outcome-Focused)

- R1. Keep three concerns orthogonal:
  - engagement mode: `Scan`, `Explore`, `Decision`, `Review`, or `Update`;
  - decision altitude: intervention/task, project/outcome, portfolio/scarce
    capacity, or whole-person objective/context; and
  - search boundary: `portfolio-bounded`, `open-field`, or `dual-track`.
  Retention mode and workspace authority remain separate from all three.
- R2. The advisor selects engagement mode, decision altitude, and search
  boundary autonomously by default. The user is never required to understand
  product vocabulary before receiving useful help.
- R3. Add `Explore` as the engagement mode for discovering or reframing
  candidate pathways when no settled decision object exists. A named mode is
  not sufficient evidence of exploration: behaviour must include genuinely
  distinct mechanisms, uncued contribution where useful, evidence separation,
  and proportionate reconvergence.
- R4. When a framing choice could materially change the analysis, state it in
  one natural-language sentence. Examples include:
  - “I’ll treat your current projects as candidates, not as the boundary, and
    compare them with outside paths.”
  - “I’ll keep this bounded to the current project unless a portfolio conflict
    changes the answer.”
  Do not prepend mode labels or framing ceremony to routine direct assistance.
- R5. Accept plain-language user overrides at any point, including the
  equivalents of:
  - “Use only my current projects.”
  - “Start with a clean slate.”
  - “Compare both.”
  “Clean slate” widens candidate vehicles but does not discard the user's
  objectives, evidence, constraints, exact personal context, or authority
  boundaries.
- R6. Ask a short boundary question only when:
  - the request plausibly supports materially different bounded and open-field
    interpretations;
  - those interpretations could change the recommendation or the cost of the
    investigation; and
  - proceeding with an explicit assumption would be irresponsible.
  Otherwise infer the frame, state a material assumption when needed, and
  proceed.
- R7. For broad outcome-led questions, default to `dual-track` when both current
  and outside vehicles remain plausible. For clearly project-specific requests,
  default to `portfolio-bounded` unless moving upward or outward could
  materially change the recommendation.
- R8. A Strategy Workspace portfolio represents current commitments, roles,
  known candidate vehicles, and opportunity costs. It is not an exhaustive
  opportunity set and does not create a presumption that listed projects should
  be commercialised, continued, or prioritised.
- R9. When no current project has a supported causal bridge to an objective, say
  so. Consider outside-portfolio pathways when material, but keep them as
  hypotheses until evidence supports a candidate action.
- R10. During open-field or dual-track exploration, contribute two to four
  genuinely different strategy families only when their causal mechanisms,
  resource allocations, sequences, or trade-offs differ. Include the strongest
  live rival and avoid cosmetic lists, novelty theatre, or claims of
  exhaustiveness.
- R11. Exploration must reconverge proportionately. Once a candidate action
  emerges, reset to evidence, apply readiness to that exact action, and return
  to a bounded decision or discriminating test. If no candidate exists, name
  the next question or observation that would improve the search.
- R12. Make the capability discoverable without forcing it:
  - document the three plain-language boundary overrides;
  - include at least one broad-outcome example and one bounded-project example
    in portable onboarding or conversation starters;
  - make material framing visible in the response; and
  - preserve direct assistance for ordinary requests.
- R13. Durable storage remains deliberate. Speculative options stay in the
  conversation unless the applicable durable-write authority permits a
  structured proposal or capture. A current portfolio record is not silently
  created or changed by exploration.
- R14. Keep canonical behaviour under `skills/strategic-advisor/`; host adapters
  may expose the same behaviour but must not create divergent prompt copies.
- R15. Validate the behaviour with synthetic, non-reconstructable cases and a
  bounded exact-runtime multi-turn smoke. Private owner dogfood may test
  usefulness separately but cannot substitute for product evidence or enter
  public artifacts.

## Acceptance Criteria (Verifiable)

- AC1: Canonical runtime sources distinguish engagement mode, decision
  altitude, search boundary, retention mode, and authority without conflating
  their effects.
- AC2: `Explore` is implemented as an engagement mode whose contract requires
  genuine pathway divergence, evidence separation, and proportionate
  reconvergence rather than a label or generic brainstorming.
- AC3: Runtime behaviour autonomously infers the frame by default and asks a
  boundary question only under the material-ambiguity gate in R6.
- AC4: Material framing is expressed in one concise natural-language sentence,
  is absent from routine direct assistance, and can be overridden using
  ordinary user language.
- AC5: Canonical workspace documentation and the portable `PORTFOLIO.md`
  template explicitly define listed projects as current commitments or
  candidates rather than an exhaustive opportunity set.
- AC6: Broad outcome-led analysis can state that no current project has a
  supported causal bridge and can compare current, adjacent, and outside
  pathways without inventing feasibility or promoting ideas into evidence.
- AC7: Clearly bounded project requests remain bounded unless a material
  objective, opportunity cost, or contradiction justifies widening; the
  advisor does not force outside alternatives for novelty.
- AC8: `portfolio-bounded`, `open-field`, and `dual-track` user overrides work
  consistently across initial and follow-up turns while exact personal context
  and authority boundaries remain in force.
- AC9: Portable onboarding and conversation starters expose plain-language ways
  to request current-project-only, clean-slate, or comparison analysis without
  requiring users to learn internal terminology.
- AC10: Synthetic cases cover at minimum:
  - a recurring-income objective for which current projects lack commercial
    evidence;
  - a current project that remains the strongest supported path;
  - an explicit current-project-only instruction;
  - an explicit clean-slate instruction;
  - an ambiguous high-consequence boundary requiring clarification;
  - a routine tactical request that must not trigger framing ceremony;
  - preference pressure that must not upgrade a new idea into evidence; and
  - exploration that reconverges on a bounded discriminating test.
- AC11: A fresh exact-runtime multi-turn smoke demonstrates uncued
  outside-portfolio contribution, user boundary override, evidence-only reset,
  and bounded reconvergence against the exact source being claimed.
- AC12: Current repository validation, runtime/install determinism, privacy and
  secret checks, package limits, and existing personal-context behaviour remain
  passing; capability claims remain bounded to the evidence actually produced.

## Open Questions (Answer Needed)

- None required before owner review. The interaction policy below resolves the
  question raised in the approval conversation; the owner may amend it before
  approving decomposition.

## Decisions (Resolved)

- D1. Mode selection is autonomous by default; it is not presented as a
  mandatory menu.
- D2. The advisor makes a material frame visible in one sentence and accepts
  plain-language overrides.
- D3. It asks whether to use current projects, a clean slate, or both only when
  the ambiguity is decision-relevant and no responsible default is available.
- D4. Broad outcome-led questions default to comparing both current and outside
  pathways when both remain plausible.
- D5. “Clean slate” means open candidate generation, not erasure of exact
  personal circumstances or established constraints.
- D6. `Explore` will be a first-class engagement mode, but behavioural
  requirements and evaluation—not the name—establish whether it works.
- D7. The current portfolio is evidence about commitments and opportunity cost,
  never an exhaustive search boundary.
- D8. No new durable `OPPORTUNITIES.md` file is introduced in this Epic unless
  implementation evidence demonstrates that the existing structured
  objective/claim/decision records cannot support a reviewed candidate.

## Validation Plan

- Static contract tests will verify the orthogonal axes, autonomous-selection
  rule, clarification gate, visible-framing rule, non-exhaustive workspace
  semantics, plain-language overrides, and canonical-source boundary.
- Synthetic cases will exercise the eight scenario families in AC10 with
  required and forbidden assertions, including no novelty forcing and no
  evidence laundering.
- A bounded fresh exact-runtime multi-turn smoke will freeze current source,
  runtime identity, model/host identity, source-access boundaries, user turns,
  required observations, and failure conditions before results are accepted.
- The full unit suite, aggregate validator, evaluation inventory check,
  deterministic runtime/install builds, Custom GPT Knowledge inventory check,
  privacy scan, package-content scan, and Workflow Doctor must pass.
- Optional private Strategy Workspace dogfood may follow under separate
  read/write authority. Only synthetic non-reconstructable lessons may be
  transferred back into the product repository.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose |
| --- | --- | --- |
| Define Open-Field Interaction And Search Contract | AC1, AC2, AC3, AC4, AC7, AC8 | Freeze the orthogonal mode/altitude/boundary model, inference defaults, clarification gate, visible framing, overrides, and bounded behaviour. |
| Implement Runtime And Workspace Non-Exhaustiveness | AC1, AC2, AC5, AC6, AC7, AC8 | Update canonical runtime and workspace semantics so current projects inform but do not constrain the opportunity set. |
| Expose Exploration Without Interaction Ceremony | AC3, AC4, AC8, AC9 | Make the feature discoverable through plain language, examples, and proportionate response framing across portable surfaces. |
| Validate Open-Field Multi-Turn Behaviour | AC6, AC7, AC8, AC10, AC11, AC12 | Freeze synthetic authority, run exact-runtime multi-turn proof, protect existing behaviour, and close package/privacy regressions. |
