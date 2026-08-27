# Requirements

## Summary

- Task: TASK-032
- Title: Implement Alignment And Goal Qualification Core
- Parent AC Coverage: AC1, AC2, AC3, AC4, AC5, AC6
- Last updated: 2026-08-27
- Intent contract: full

## Intent

Extend the existing Strategic Advisor decision state so it can align the real
outcome, selectively re-clarify after material evidence and qualify goals and
causal paths without replacing readiness or interrupting routine assistance.

## Intent Spine

- OC1 — Completion capability: The advisor can distinguish a stated mechanism
  from the underlying outcome, preserve settled state, and admit aspirations,
  discovery goals or operational goals to the right next action.
- OC2 — Material capabilities: Existing-state extension, bounded
  reconnaissance, initial alignment, two-condition re-clarification,
  empirical/owner fork routing, selective invalidation, goal ladder,
  goal/readiness separation and causal-indicator discipline.
- OC3 — Success journey: Start from the frozen contract, reconcile the runner
  base, extend canonical instructions once, satisfy deterministic cases, then
  hand the exact core to review and runtime validation.
- OC4 — Successful-but-wrong result: A new state subsystem, universal
  questionnaire, owner guess on empirical truth, preserved mismatched evidence,
  infeasible goal type, or task-labelled leading indicator is not success.
- OC5 — Exclusions: No recurring review workflow, private workspace mutation,
  runner redevelopment, broad evaluation campaign, release publication or
  capability promotion.
- OC6 — Assumptions: TASK-031 is complete and the verification-runner stream
  has reported a durable disposition and correct base before runtime edits.
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

- AC1: owner `TASK-032`; required evidence: Canonical state/recommendation-delta diff, duplicate-state scan, matched preservation assertions and QA.
- AC2: owner `TASK-031, TASK-032, TASK-034`; required evidence: Frozen positive/negative authority, direct/reconnaissance/alignment cases, exact-runtime verdicts and QA.
- AC3: owner `TASK-031, TASK-032, TASK-034`; required evidence: Stateful delta/fork/selective-invalidation cases, raw sequence outputs, exact-runtime verdicts and QA.
- AC4: owner `TASK-031, TASK-032, TASK-034`; required evidence: Goal/proxy ladder cases, object-class assertions and exact-runtime review.
- AC5: owner `TASK-031, TASK-032, TASK-034`; required evidence: Aspiration/discovery/operational and readiness cases with stateful assertions and verdicts.
- AC6: owner `TASK-031, TASK-032, TASK-034`; required evidence: Causal indicator/milestone cases, evidence-field assertions and exact-runtime verdicts.

## Goal

Implement the single canonical alignment and goal-qualification control that
both audited workstreams require.

## Non-Goals

- Adding another advisor, memory store, goal database or public private state.
- Asking a clarification question for every consequential request.
- Implementing event, weekly or monthly review records owned by TASK-033.
- Running the final exact-runtime campaign owned by TASK-034.

## Users & Context

Users often state a proxy, mechanism, metric or implementation as the goal, and
research can later expose a framing fork. The current product has adjacent
pieces but lacks the complete selective ladder and re-clarification contract.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1. Extend the existing material-decision and recommendation-delta state with
  stated request, underlying outcome, altitude, object class, causal bridge,
  material uncertainty, owner-settled version and reopening evidence.
- R2. Preserve existing provenance, readiness, recommendation, rival and delta
  semantics and prevent a second state model or duplicate execution path.
- R3. Implement bounded reconnaissance and initial alignment exactly as frozen:
  ask only before materially divergent action when no responsible default
  exists, and proceed with labelled low-risk assumptions otherwise.
- R4. Implement re-clarification only for a material evidence/framing delta
  plus an answer that changes the supported action. State changed and settled
  state, live branches and decision-changing questions compactly.
- R5. Route evidence-resolvable forks to proportionate research and owner-only
  outcomes, values, constraints, authority and trade-offs to the owner.
- R6. Preserve unaffected state and evidence; invalidate only material that
  depends on the changed scope, baseline or meaning.
- R7. Implement the move-up, alternative-route and move-down goal ladder with
  object classification, causal path, horizon, constraints, lag measures,
  evidenced leading indicators, falsifiers and decisive validation.
- R8. Keep aspiration, discovery and operational goal purpose distinct from
  exact-candidate readiness. Discovery goals require a learning result,
  horizon, falsifier and unlocked decision.
- R9. Reject activities as automatic leading indicators and arbitrary lag
  interpolation; require evidence and causal role.
- R10. Preserve strong direct-assistance, same-robust-move and routine work
  negative controls.

## Acceptance Criteria (Verifiable)

- AC1: Canonical files extend the released state once, preserve current
  readiness and delta rules and pass duplicate-state/logic checks.
- AC2: Frozen initial-alignment cases pass for direct assistance, bounded
  reconnaissance, material divergence and same-robust-move controls.
- AC3: Frozen re-clarification sequences pass both-trigger, empirical/owner
  fork, state-preservation and selective-invalidation assertions.
- AC4: Goal ladder cases correctly classify underlying outcome and stated
  object, compare routes and expose an attractive proxy that does not satisfy
  the outcome.
- AC5: Aspiration, discovery and operational purpose remains separate from
  readiness and discovery cases retain their complete learning contract.
- AC6: Indicator cases reject unsupported task/activity proxies and arbitrary
  milestones while retaining evidenced driver role and falsifiers.

## Open Questions (Answer Needed)

- None. Implementation is operationally blocked until the runner stream reports
  its durable base; that is a known dependency, not an owner decision.

## Decisions (Resolved)

- D1. One sequential canonical implementation owns shared state and files.
- D2. Extend recommendation delta rather than add a goal subsystem.
- D3. Research empirical forks and ask only owner-only choices.
- D4. Preserve unaffected work and invalidate mismatched evidence.

## Validation Plan

- AC1: Canonical source, runtime-manifest and duplicate-logic review plus
  focused structural tests.
- AC2-AC6: Run the frozen deterministic cases and negative controls before the
  broader exact-runtime campaign.
- All: Run focused tests, deterministic evaluation rebuild, aggregate
  validators, privacy/diff checks and child QA.
