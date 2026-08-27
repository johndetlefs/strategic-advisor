# Requirements

## Summary

- Task: TASK-031
- Title: Freeze Combined Contract And Behaviour Baseline
- Parent AC Coverage: AC2, AC3, AC4, AC5, AC6, AC11, AC13
- Last updated: 2026-08-27
- Intent contract: full

## Intent

Freeze the exact claims, alpha.6 baseline and sanitised behavioural authority
before runtime treatment results are visible, so later implementation is judged
against the approved user job rather than post-hoc tests.

## Intent Spine

- OC1 — Completion capability: A reviewer can identify the exact baseline,
  claim, case, assertion, forbidden behaviour and proof layer for every
  material alignment, goal and review behaviour before implementation begins.
- OC2 — Material capabilities: Frozen stable case IDs, positive and negative
  pairs, sequenced state assertions, privacy provenance, runtime/evaluation
  isolation and an explicit runner/base dependency.
- OC3 — Success journey: Inspect alpha.6 and existing cases, define the minimum
  claim matrix, author synthetic non-reconstructable cases, deterministically
  rebuild and validate them, then retain a reviewed freeze identity.
- OC4 — Successful-but-wrong result: A case set written after treatment output,
  derived from private transcripts, missing direct-assistance controls, or able
  to pass through wording alone is not a valid baseline.
- OC5 — Exclusions: No canonical runtime change, live model execution, runner
  modification, private dogfood, claim promotion or package/release mutation.
- OC6 — Assumptions: Alpha.6 at source commit `6d65830` is the pre-treatment
  public baseline; runner implementation is still external and unresolved.
- OC7 — Authority source: Parent Epic Intent and approved decomposition row.

## Owner Approval

- Intent reviewed and accurately reflected: Inherited from parent epic envelope when unchanged
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

- `skills/strategic-advisor/` remains the only executable source of Strategic Advisor logic. This Epic extends existing state and reasoning; it does not add another advisor or state subsystem.
- Stated request, underlying outcome, object class, goal-purpose class, candidate action and readiness remain distinct.
- Bounded reconnaissance may precede alignment. Re-clarification requires both a material delta and an answer that can change the supported action.
- Empirical forks are researched proportionately; owner-only values, constraints, authority and trade-offs remain owner decisions.
- Settled state and unaffected evidence survive a reframe; only evidence whose scope, baseline or meaning changed is invalidated.
- Aspirations may remain visible. Discovery goals require bounded learning and operational goals require proportionate causal support. Readiness is never inferred from the goal-purpose label.
- Tasks and initiatives are not automatic leading indicators. Material progress requires evidence of outcome, driver, constraint or decision movement.
- Goal change is challenged but not prohibited. A qualifying evidence, constraint, value, trade-off or opportunity-cost delta and explicit owner authority permit proportionate revision.
- Event review can pre-empt scheduled cadence. Weekly and monthly cadence are configurable conventions, not universal laws or accountability devices.
- Goal and path dispositions remain separate and identify the exact target of continue, correct, pivot, pause, replace or stop.
- Strategy Workspace is the private durable strategic authority. Daily Checklist, Sunday and Project Workflow remain separate consumers or process systems with no implicit runtime, data or authority coupling.
- Only synthetic, public or irreversibly sanitised cases may be committed. No private or reconstructable task, workspace, employer, client or household data enters public source, runtime, evaluation or package artifacts.
- Exact proof claims remain separated across documented semantics, deterministic/static validation, exact-runtime synthetic behaviour, private real-task dogfood, package identity, publication, host activation, support, adoption and effectiveness.
- The in-flight proportionate-verification-runner worktree is preserved and reconciled before runtime/evaluation implementation; this Epic does not absorb, overwrite or recreate it.
- The downstream Strategy Workspace process is a real v1 to dogfood and iterate, not a disposable pilot, but it remains a separate repository task.
- An allowlisted runtime-byte change prepares the next immutable distribution in the same implementation branch. Push, PR, merge, publication, finalisation, activation and private-workspace mutation require separate authority and exact evidence.

### Invalid Substitutes

- A stated goal, metric, timeframe, desired tool or preferred solution in place of the confirmed underlying outcome and unacceptable substitutes.
- Activity, effort, task completion, output count, tool delivery, praise or visibility in place of material progress toward the goal.
- An initiative or recurring task labelled as a leading indicator without evidence that it predicts or drives the lag outcome.
- Arbitrary milestone interpolation in place of a causal/driver model.
- More questions in place of better alignment, or questions whose answers cannot materially change the supported action.
- Owner preference on an empirical fork in place of accessible evidence, or external evidence in place of an owner-only value or trade-off decision.
- Preserving all prior research after a material scope change in place of selective validity review, or restarting unaffected research in place of state preservation.
- Execution friction, sunk cost, non-execution, boredom, preference repetition or mechanism failure in place of evidence that the goal should change.
- Prior approval in place of justified revision when the goal is obsolete, mistaken, infeasible or no longer worth pursuing.
- A weekly status report, monthly summary or accountability ritual in place of decision-relevant review.
- Documentation, schema checks, unit tests, a plausible answer or model self-assessment in place of exact-runtime behavioural evidence.
- A bounded smoke, owner dogfood or exact-runtime case in place of comparative effectiveness, general support, parity, adoption or cross-host proof.
- Private transcripts, renamed private cases, Strategy Workspace facts, Daily Checklist data or reconstructable owner detail in place of synthetic, public or irreversibly sanitised regressions.
- A generic public template in place of accepted private Strategy Workspace operation, or private dogfood in place of public package/source identity.
- A package build or local prepared ZIP in place of protected-main integration, public publication, fresh download verification or host activation.

### Artifact Targets

- Canonical reasoning: `skills/strategic-advisor/SKILL.md`, `references/recommendation-delta.md`, `references/conversational-strategy.md`, `references/evidence.md`, `references/action-policy.md`, `references/response-contract.md`, `references/strategy-workspace.md`, `references/project-product.md`, and only other directly affected allowlisted references.
- Generic portable records: `workspace-templates/OBJECTIVES.md`, `DECISIONS.md`, `CHANGELOG.md`, `WORKSPACE.md` and validator/builder tests, without any private instance data.
- Evaluation authority: `evals/core_cases.json`, `eval_queries.json`, `recommendation_gate_cases.json`, `drift_smoke_cases.json`, generated `evals.json`, the smallest necessary case/assertion/runner changes and exact raw result artifacts kept outside the model-visible runtime.
- Public contract: `PRODUCT-CONTRACT.md`, `ARCHITECTURE.md`, `README.md`, `INSTALL.md`, onboarding/agent metadata and only directly affected contributor/security documentation.
- Runtime/package declarations: `runtime-manifest.json`, `distribution.json`, generated install-artifact provenance, exact inventories and deterministic package comparison.
- Retained proof: child `EVIDENCE.json`, deterministic validation output, exact-runtime target/source/activation evidence, sanitised raw case outputs, case-level verdicts, independent QA, parent audit and explicit blockers.
- Downstream handoff: a public-contract-derived Strategy Workspace v1 brief identifying private record, dogfood, Sunday and Daily Checklist boundaries without mutating that repository or copying its facts.
- Workflow: EPIC-007 requirements, contract, decomposition, child artifacts, tracker, intent audit, acceptance map/audit, deferrals/amendments if required and retro.

### Parent AC Proof Ownership

- AC2: owner `TASK-031, TASK-032, TASK-034`; required evidence: Frozen positive/negative authority, direct/reconnaissance/alignment cases, exact-runtime verdicts and QA.
- AC3: owner `TASK-031, TASK-032, TASK-034`; required evidence: Stateful delta/fork/selective-invalidation cases, raw sequence outputs, exact-runtime verdicts and QA.
- AC4: owner `TASK-031, TASK-032, TASK-034`; required evidence: Goal/proxy ladder cases, object-class assertions and exact-runtime review.
- AC5: owner `TASK-031, TASK-032, TASK-034`; required evidence: Aspiration/discovery/operational and readiness cases with stateful assertions and verdicts.
- AC6: owner `TASK-031, TASK-032, TASK-034`; required evidence: Causal indicator/milestone cases, evidence-field assertions and exact-runtime verdicts.
- AC11: owner `TASK-031, TASK-033, TASK-034`; required evidence: Process-waste case authority, contract rules, exact-runtime cases and proportionality review.
- AC13: owner `TASK-031, TASK-034, TASK-035`; required evidence: Frozen inventory, deterministic rebuild, category/ID validation, privacy and leakage proof.

## Goal

Create a treatment-independent behavioural and proof contract for alignment,
re-clarification, goal qualification, material review and strong negative
controls.

## Non-Goals

- Editing allowlisted runtime instructions or generic workspace templates.
- Running treatment behaviour or changing expected results after seeing it.
- Copying, lightly sanitising or reconstructing the audited private tasks.
- Building a new evaluator, runner or general proof framework.

## Users & Context

Implementation and QA need a fixed authority that prevents moving the
goalposts. Existing cases cover adjacent recommendation drift and activity
substitution, but not the complete two-checkpoint, goal-ladder and review
contract approved by EPIC-007.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1. Record the exact alpha.6 source, runtime manifest, package and current
  evaluation/runner identities that form the untreated baseline.
- R2. Freeze one stable case matrix covering every parent R22 category with
  explicit prompt/turn sequence, required assertions, forbidden behaviours,
  proof layer and applicability.
- R3. Include matched controls for direct assistance, bounded reconnaissance,
  evidence-resolvable and owner-value forks, the same robust move, selective
  invalidation, goal/proxy classification, discovery goals, causal indicators,
  activity/progress, goal amendment, exception review, owner reconciliation and
  process waste.
- R4. Convert audited mechanisms into synthetic non-reconstructable cases.
  Record case provenance as synthetic design derivation without private facts,
  phrasings, identifiers or cross-task reconstruction.
- R5. Keep normative case authority outside the model-visible runtime and
  deterministically regenerate derived inventories without treatment output.
- R6. Name the smallest proof needed for each claim. Do not require new
  machinery where existing deterministic validation and drift smoke suffice.
- R7. Record the external prerequisite that runtime/evaluation implementation
  uses the durable disposition of `codex/proportionate-verification-runner`.

## Acceptance Criteria (Verifiable)

- AC1: The freeze manifest binds source commit `6d65830`, current runtime and
  evaluation identities, public claim boundary and the unresolved runner
  dependency without modifying treatment bytes.
- AC2: Stable sanitised cases cover every R3 category with required and
  forbidden behaviour, matched positive/negative controls and stateful
  sequences where later evidence or answers matter.
- AC3: Case provenance review proves no private or reconstructable task,
  workspace, employer, client or household data is present.
- AC4: Deterministic builders reproduce the frozen derived inventory, reject
  missing/duplicate categories or unstable IDs and preserve runtime/evaluation
  isolation.
- AC5: The proof matrix distinguishes documented semantics, static checks,
  exact-runtime behaviour and later private dogfood, and does not overbuild a
  proof mechanism without a named claim.

## Open Questions (Answer Needed)

- None. Exact runtime execution waits for the runner stream, but freezing the
  pre-treatment contract does not depend on its implementation.

## Decisions (Resolved)

- D1. Freeze claims and cases before runtime edits.
- D2. Preserve only synthetic/public/irreversibly sanitised mechanisms.
- D3. Keep direct-assistance and same-robust-move cases as hard negatives.
- D4. Do not modify or absorb the in-flight runner worktree.

## Validation Plan

- AC1: Hash and inventory the exact baseline source/runtime/evaluation files.
- AC2-AC3: Review every committed case and provenance record before treatment.
- AC4: Run deterministic evaluation rebuild, category/ID validators, privacy
  scans and runtime-package exclusion checks.
- AC5: Review the claim/proof matrix against repository guidance and remove any
  machinery without a live claim.
