# Requirements

## Summary

- Task: TASK-034
- Title: Validate Combined Exact-Runtime Behaviour
- Parent AC Coverage: AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15
- Last updated: 2026-08-27
- Intent contract: full

## Intent

Determine whether the exact implemented Strategic Advisor runtime performs the
owner-approved changed alignment, goal-qualification and review behaviours on
one reference Codex model while remaining proportionate for a strong negative
control and honest about every failure. This is an affected alpha-release smoke,
not comprehensive model, host or behavioural certification.

## Intent Spine

- OC1 — Completion capability: A reviewer can reproduce case-level verdicts
  against the exact source/package/model/host and know whether each claimed
  behaviour passed, failed or remained untested.
- OC2 — Material capabilities: Frozen deterministic checks, one capped canary
  and affected exact-runtime selection, raw outputs, target-use proof, case
  assertions, telemetry, privacy review and one independent release QA.
- OC3 — Success journey: Certify the reconciled runner, run cheap checks and a
  negative canary first, stop on blocking failure, execute only the ten
  owner-approved affected cases within a 20-target-call cap, retain exact
  receipts and adjudicate those cases once.
- OC4 — Successful-but-wrong result: Plausible prose, aggregate green despite a
  hard-gate failure, source-tree self-report, stale receipt, treatment-informed
  assertion, later recovery erasing an earlier failure, or private case leakage
  is not a pass.
- OC5 — Exclusions: No claim of comparative effectiveness, general support,
  cross-host parity, adoption, private Strategy Workspace success, publication
  or release finalisation.
- OC6 — Assumptions: TASK-031 through TASK-033 are current and the durable
  proportionate-verification-runner disposition is the execution base.
- OC7 — Authority source: Parent Epic Intent and approved decomposition row.

## Owner Approval

- Intent reviewed and accurately reflected: Yes
- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Inherited from approved parent decomposition
- Approved for implementation: Yes
- Approved scope envelope: One reference Codex model/host; ten selected cases; at most 20 target calls; fail-fast; one infrastructure retry; no comprehensive or cross-model certification
- Approved by: John (owner)
- Approval date: 2026-08-27
- Approval note / source: Current Codex task directive to finish the public release and local installation without further approval prompts; coordination amendment `owner-release-scope-2026-08-27`
- Approved artifact identity: Current requirements after this recorded amendment

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
- AC7: owner `TASK-033, TASK-034`; required evidence: Generic event/weekly/monthly contract, cadence negative controls and case-level verdicts.
- AC8: owner `TASK-033, TASK-034`; required evidence: Material-progress and enabling-project cases with evidence and case-level verdicts.
- AC9: owner `TASK-033, TASK-034`; required evidence: Drift and goal-amendment cases proving challenged replacement and justified revision paths.
- AC10: owner `TASK-033, TASK-034`; required evidence: Generic record schema, owner-reconciliation fixtures, two-axis disposition cases and QA.
- AC11: owner `TASK-031, TASK-033, TASK-034`; required evidence: Process-waste case authority, contract rules, exact-runtime cases and proportionality review.
- AC12: owner `TASK-033, TASK-034, TASK-035`; required evidence: Dependency/private-data/diff scans, generic fixtures, runtime/package isolation and QA.
- AC13: owner `TASK-031, TASK-034, TASK-035`; required evidence: Frozen inventory, deterministic rebuild, category/ID validation, privacy and leakage proof.
- AC14: owner `TASK-034, TASK-035`; required evidence: Passing runtime-target/source claims, raw bounded outputs, exact identity, case verdicts and honest claim boundary.
- AC15: owner `TASK-034, TASK-035`; required evidence: Focused/full validation, bounded smoke, privacy/diff/package checks, Doctor, child QA and parent audit.

## Goal

Produce bounded, reproducible and claim-matched affected-smoke evidence for the
next experimental public Strategic Advisor prerelease.

## Non-Goals

- Using the full suite as defect discovery before cheap/canary proof.
- Running the complete 20-case goal-review matrix or complete 16-case retained
  drift suite as an alpha-release prerequisite.
- Testing models or hosts that this release does not claim to support.
- Changing frozen cases, rubrics or hard gates after viewing treatment results.
- Treating private dogfood or owner satisfaction as public behavioural proof.
- Promoting the bounded result to general support, parity, comparative
  effectiveness, adoption or strategic effectiveness.

## Users & Context

Documentation and deterministic validation cannot prove model behaviour. The
existing runner is being separately hardened for fail-fast selection, limits,
receipts and regrade; this child consumes its durable result rather than
reimplementing it.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1. Verify the exact frozen authority, implemented source, runtime/package,
  model, host, activation and runner identities before any target call.
- R2. Use the reconciled runner's bounded controls: deterministic checks,
  canaries, affected selection, fail-fast, call/time limits, receipts,
  infrastructure retry and evaluator-only regrade where applicable.
- R3. Execute only the approved affected selection: `SAGR-001`, `SAGR-009`,
  `SAGR-014`, `SAGR-015`, `SAGR-016`, `SAGR-018`, `SAGR-020`, `DRIFT-004`,
  `DRIFT-014` and `DRIFT-016`. The selection contains 19 planned target turns;
  the campaign must cap target calls at 20 and must not expand after green.
- R4. Retain raw prompts/turns/outputs, case assertions, forbidden behaviours,
  target-use proof, timing/call telemetry and case-level verdicts outside the
  model-visible runtime.
- R5. Stop and replan on blocking product failure. Diagnostic continuation
  requires a named bounded information need; reaching a limit never creates a
  pass.
- R6. Distinguish product, evaluator, provider/infrastructure and harness
  failures. A later corrected run remains a separate candidate and never erases
  the earlier verdict.
- R7. Run deterministic rebuild, privacy, leakage, runtime/evaluation isolation
  and exact receipt-currentness checks around behavioural execution.
- R8. Obtain independent QA against the frozen user job, invalid substitutes,
  raw evidence and claim boundary before parent credit.

## Acceptance Criteria (Verifiable)

- AC1: Preflight proves exact authority/source/package/model/host/activation and
  runner identity before calls, and stale or mismatched receipts are rejected.
- AC2: Cheap checks and the routine-direct canary gate the selected affected
  work; a canary failure causes zero affected or full-suite target calls.
- AC3: Every owner-approved affected case has a case-level pass/fail verdict
  with raw stateful outputs and forbidden-behaviour review; unselected cases
  remain explicitly untested on this runtime.
- AC4: Strong direct-assistance, same-robust-move, empirical-fork and routine
  controls remain non-triggering or proportionate as specified.
- AC5: Product, evaluator, provider and harness failures remain distinct;
  bounded limits cannot waive proof and later recovery preserves history.
- AC6: Privacy, leakage, deterministic inventory and runtime/evaluation
  isolation checks pass around retained evidence.
- AC7: Independent QA issues one evidence-backed verdict and states that a
  bounded exact-runtime result is not comparative validation, support or
  private dogfood acceptance.

## Open Questions (Answer Needed)

- None before execution. If the runner stream does not land or expose the
  required controls, this child blocks rather than silently replacing it.

## Decisions (Resolved)

- D1. Consume the durable runner; do not recreate it.
- D2. Freeze before treatment and stage proof from cheap to expensive.
- D3. Fail closed without erasing history or weakening claims.
- D4. Keep exact-runtime synthetic proof separate from private dogfood.
- D5. One exact Codex/gpt-5.6-sol affected smoke is the release gate; model and
  host variability is a documented limitation, not an invitation to a matrix.
- D6. A green selected smoke ends behavioural testing for this release. Expand
  only when a material failure demonstrates broader affected scope.

## Validation Plan

- AC1-AC6 use the runtime-target/source proof recipe. `EVIDENCE.json` will
  retain execution target, source artifact, observation method, positive target
  use proof and hashed raw result artifacts for the exact claims.
- AC2: Runner telemetry must show exact selected scope, the 20-call cap,
  canary/affected boundaries and zero prohibited calls after a blocking failure.
- AC3-AC5: Case-by-case adjudication against frozen assertions and raw stateful
  transcripts; aggregate green cannot waive a hard gate.
- AC6-AC7: Deterministic/privacy/isolation checks and independent QA review of
  the exact evidence and bounded claim.
