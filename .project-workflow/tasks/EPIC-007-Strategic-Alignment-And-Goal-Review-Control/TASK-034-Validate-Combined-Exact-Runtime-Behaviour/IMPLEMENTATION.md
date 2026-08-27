## User Story

As the capability reviewer, I want exact-runtime evidence against a frozen
contract, so that polished instructions or plausible answers cannot be mistaken
for demonstrated Strategic Advisor behaviour.

## Parent AC Coverage

- AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15

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

## Acceptance Criteria

- [x] AC1: Exact authority, target, source, activation and runner identities are proven.
- [x] AC2: Progressive proof stops before affected work on canary failure and never launches unplanned full work.
- [x] AC3: Every executed affected case retains raw output and a case-level verdict; stopped and unselected cases remain explicitly untested.
- [x] AC4: Strong negative controls remain direct or proportionate.
- [x] AC5: Product/evaluator/provider/harness outcomes and history remain distinct.
- [x] AC6: Deterministic, privacy, leakage and isolation checks pass.
- [ ] AC7: One independent QA verdict preserves the bounded claim.

## Validation

- AC1-AC6: Runtime-target/source evidence, runner telemetry, raw outputs,
  case-level adjudication and deterministic/privacy/isolation checks.
- AC7: Independent QA against frozen authority and exact retained artifacts.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/strategic-alignment-goal-review-pw08` from `d6756f9`; exact runtime `38a40f968edcf0936dac80124565d814f587b37dd41ea8a61c9c44398093f7e3` | Current freeze (20 cases/37 criteria), 54 core tests, 17 runner controls and skill/privacy/links/diff checks pass; current-runtime SAGR-014 and SAGR-013 pass | Local Testing evidence only; no certification, public release or activation claim | `EVIDENCE.json`; `evidence/evaluations/goal-review/run-001-*`; `run-002-*` |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Confirm proof inputs | Verify frozen authority, source/package, model/host/activation, runner controls and receipt compatibility. | AC1, AC5 | Inspect exact identities and initialise the bounded diagnostic campaign without target calls. | Done | TASK-033 and external runner disposition | Validation configuration and evidence only | No | bounded-return |
| 2 | Configure cheap and canary proof | Bind deterministic gates and SAGR-001 as the one-turn fail-fast canary before affected work. | AC2, AC4, AC6 | Inspect the frozen selection and campaign limits before target use. | Done | 1 | Validation configuration and evidence only | No | bounded-return |
| 3 | Configure capped affected proof | Bind only SAGR-009/014/015/016/018/020 and DRIFT-004/014/016 after the canary, for 18 further turns and 19 total. | AC3, AC4, AC5 | Inspect the selected cases, call arithmetic and 20-call hard cap. | Done | 2 | Validation configuration and evidence only | No | bounded-return |
| 4 | Configure adjudication boundaries | Require typed product/evaluator/provider/harness outcomes, retained raw outputs, regrade-without-target-use where valid, and privacy/leakage/isolation checks. | AC3, AC5, AC6 | Inspect the runner receipt contract and confirm history cannot be overwritten. | Done | 3 | Evaluation configuration and evidence only | No | bounded-return |
| 5 | Prepare independent QA packet | Bind frozen authority, exact runtime, raw pass/failure history, deterministic proof, repair scope and explicit non-certification boundary for one read-only reviewer. | AC7 | Reviewer can reproduce the bounded claim without relying on the coordinator's summary. | Done | 4 | Child QA/evidence artifacts only | No | bounded-return |

The campaign is intentionally recorded as `diagnostic`, not `certification`:
Project Workflow correctly reserves certification for a full campaign. The
owner-approved release claim is only a bounded exact-runtime affected smoke for
an experimental alpha, so the ten selected cases and 20-call hard cap remain
the authoritative boundary.

## Testing Outcome

- The first campaign passed SAGR-001 and SAGR-009, then failed SAGR-014 because
  broad `enabled` wording did not name the enabler's causal limit. Fail-fast
  stopped every later selected case; their absence is retained as untested, not
  silently upgraded to pass.
- The bounded correction made named causal limits part of the always-loaded
  review route and made unsupported enabler contribution remain unknown.
- A second SAGR-014 answer correctly withheld enabler credit; its first grading
  still failed because the evaluator treated a conditional criterion as a
  requirement to invent an unstated training-information constraint. The
  general evaluator policy was corrected and bound into evaluator identity.
- Fresh exact-runtime runs then passed SAGR-014 and the direct neighbouring
  SAGR-013 case. No full, legacy, cross-model or cross-host campaign followed.
- Retained raw results and receipts preserve the sandbox provider failure, the
  original product failure, the evaluator defect, stopped selections and both
  current-runtime passes. Total target attempts remained below the original
  20-call ceiling.

## Owner Release Authority

- Status: Hold released for the bounded amended scope on 2026-08-27.
- Authority: John explicitly directed the coordinator in the current Codex task
  to run the proportionate reference-model check, push the public prerelease,
  install the public artifact locally and stop without further approval prompts.
- Dogfood state: The durable coordination checkpoint records that the bounded
  read-only review changed the progress and allocation decision enough to justify
  this release check; private reconciliation answers are not reproduced here.
- Limits: one Codex/gpt-5.6-sol campaign; exactly the ten approved cases; at most
  20 target calls; fail-fast on product failure; at most one infrastructure
  retry; no full-suite, cross-model or cross-host expansion after green.
- Boundary: This authority includes release preparation, push, PR, merge,
  publication, public verification, local installation and activation for the
  resulting experimental prerelease. It excludes Strategy Workspace mutation
  and any support, parity, adoption or effectiveness claim.

## Parent AC Evidence

- AC2: Frozen direct/control authority plus SAGR-001 canary and fail-fast receipts.
- AC3: SAGR-009 and retained stopped-run history; current SAGR-014/SAGR-013 repair receipts.
- AC4: Direct SAGR-001 control and causal activity/enabler cases SAGR-013/SAGR-014.
- AC5: Typed provider, product, evaluator, limit and pass outcomes remain separately retained.
- AC6: Goal-object/proxy evidence in retained SAGR-009; broader selected cases remain untested after fail-fast.
- AC7: Review cadence source contract remains deterministic-only here; later selected cadence cases are explicitly untested.
- AC8: Current exact-runtime SAGR-014 material-progress and enabler-boundary pass.
- AC9: Goal-change selected cases remain explicitly untested after fail-fast.
- AC10: Reconciliation/disposition selected cases remain explicitly untested after fail-fast.
- AC11: Current exact-runtime SAGR-013 activity-as-indicator pass; process-waste case remains untested.
- AC12: Privacy, runtime isolation and evaluation-material-exclusion checks pass.
- AC13: Frozen 20-case/37-criterion inventory, package identity and deterministic checks are retained.
- AC14: `EVIDENCE.json` CLM-001/CLM-002 bind current target/source receipts and the non-certification boundary.
- AC15: Focused deterministic checks, fail-fast history, bounded repair and pending independent QA.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: ____
- Intent adversarial verdict: ____
- Could every AC pass while the approved user job remains undone: ____
- Intent audit state: ____
- Outcome journey evidence: ____
- Reviewer independence: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-034
- Title: Validate Combined Exact-Runtime Behaviour
- Created: 2026-08-27
