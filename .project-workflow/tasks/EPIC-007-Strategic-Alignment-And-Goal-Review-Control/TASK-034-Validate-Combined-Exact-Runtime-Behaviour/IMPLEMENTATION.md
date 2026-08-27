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

- [ ] AC1: Exact authority, target, source, activation and runner identities are proven.
- [ ] AC2: Progressive proof stops before unplanned full work on blocking failure.
- [ ] AC3: Every frozen category retains raw output and case-level verdicts.
- [ ] AC4: Strong negative controls remain direct or proportionate.
- [ ] AC5: Product/evaluator/provider/harness outcomes and history remain distinct.
- [ ] AC6: Deterministic, privacy, leakage and isolation checks pass.
- [ ] AC7: One independent QA verdict preserves the bounded claim.

## Validation

- AC1-AC6: Runtime-target/source evidence, runner telemetry, raw outputs,
  case-level adjudication and deterministic/privacy/isolation checks.
- AC7: Independent QA against frozen authority and exact retained artifacts.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | not recorded | not recorded | not recorded | not recorded |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Certify proof inputs | Verify frozen authority, source/package, model/host/activation, runner controls and receipt compatibility. | AC1, AC5 | Inspect exact identities and run runner certification without target calls. | To Do | TASK-033 and external runner disposition | Validation configuration and evidence only | No | bounded-return |
| 2 | Run cheap and canary proof | Run deterministic gates and the frozen new/high-risk/previously-failing canaries with fail-fast limits. | AC2, AC4, AC6 | Inspect telemetry and confirm blocking canary failure launches no full suite. | To Do | 1 | Retained validation/evaluation outputs only | No | bounded-return |
| 3 | Run affected and required full proof | After green canaries, execute the declared affected/full frozen matrix and stateful sequences. | AC3, AC4, AC5 | Inspect raw outputs, target-use proof, timing/calls and case verdicts. | To Do | 2 | Retained sanitised raw results and receipts only | No | bounded-return |
| 4 | Adjudicate and verify boundaries | Separate product/evaluator/provider/harness outcomes, regrade without target calls where valid, and run privacy/leakage/isolation checks. | AC3, AC5, AC6 | Reproduce adjudication and confirm history is not overwritten. | To Do | 3 | Evaluation results, graders and validation artifacts only | No | bounded-return |
| 5 | Obtain independent QA | Review frozen authority, raw outputs, hard gates, proof recipes and claim wording; issue one verdict. | AC7 | Inspect QA independence, findings and bounded conclusion. | To Do | 4 | Child QA/evidence artifacts only | No | bounded-return |

## Owner Hold

- Status: Blocked before implementation.
- Authority: Owner-directed sequencing checkpoint in Codex task
  `01a04143-8e71-7dd3-9340-d83b002ebe76` on 2026-08-27.
- Dogfood state: The bounded read-only real-context review was presented to the
  owner. Its three private reconciliation questions remain owner-only and are
  not reproduced in this public repository.
- Release conditions: TASK-034 may leave `Blocked` only after all three
  conditions are durably established: (1) the owner answers those three
  reconciliation questions; (2) the coordinator assesses whether the dogfood
  changed a decision, commitment, causal belief, drift finding, or non-progress
  finding enough to justify further cost; and (3) the owner explicitly
  authorises the exact-runtime proof and release cost.
- Until then: Do not launch evaluation, make target calls, prepare packages,
  publish, activate, mutate Strategy Workspace, or treat completed TASK-033 as
  authority to resume. TASK-035 remains dependent on TASK-034.

## Parent AC Evidence

- AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15: Pending implementation evidence. Recipe-triggered claims must also be backed by `EVIDENCE.json`.

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
