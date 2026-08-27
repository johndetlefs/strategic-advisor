## User Story

As a goal owner, I want reviews to tell me whether the goal and path are
actually advancing, so that busyness, tool completion or execution friction do
not silently dictate strategy.

## Parent AC Coverage

- AC7, AC8, AC9, AC10, AC11, AC12

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

- AC7: owner `TASK-033, TASK-034`; required evidence: Generic event/weekly/monthly contract, cadence negative controls and case-level verdicts.
- AC8: owner `TASK-033, TASK-034`; required evidence: Material-progress and enabling-project cases with evidence and case-level verdicts.
- AC9: owner `TASK-033, TASK-034`; required evidence: Drift and goal-amendment cases proving challenged replacement and justified revision paths.
- AC10: owner `TASK-033, TASK-034`; required evidence: Generic record schema, owner-reconciliation fixtures, two-axis disposition cases and QA.
- AC11: owner `TASK-031, TASK-033, TASK-034`; required evidence: Process-waste case authority, contract rules, exact-runtime cases and proportionality review.
- AC12: owner `TASK-033, TASK-034, TASK-035`; required evidence: Dependency/private-data/diff scans, generic fixtures, runtime/package isolation and QA.

## Acceptance Criteria

- [ ] AC1: Event, weekly and monthly review purposes are distinct and configurable.
- [ ] AC2: Material-progress and enabler-credit rules reject activity substitution.
- [ ] AC3: Drift and goal-amendment controls challenge changes but permit justified revision.
- [ ] AC4: Goal/path decisions retain complete evidence, authority and closeout fields.
- [ ] AC5: Offline owner evidence is reconciled with provenance and freshness.
- [ ] AC6: Process-waste falsifiers cause proportionate correction or stopping.
- [ ] AC7: Generic runtime/templates stay private-data-free and consumer-independent.

## Validation

- AC1-AC6: Frozen review contract cases and generic schema fixtures.
- AC7: Dependency, privacy, diff, runtime-manifest and package-exclusion checks.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | not recorded | not recorded | not recorded | not recorded |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Define review control | Add event, weekly and monthly purposes and route qualified decision state into the appropriate review. | AC1 | Inspect the contract and run event-versus-cadence cases. | To Do | TASK-032 | Canonical review reference and directly affected core routing | No | bounded-return |
| 2 | Implement progress and drift tests | Add material-progress, enabler-credit, drift and amendment burden rules. | AC2, AC3 | Run activity/progress and justified/unjustified amendment cases. | To Do | 1 | Same review reference and directly affected tests | No | bounded-return |
| 3 | Add generic records and reconciliation | Update portable templates/semantics for two-axis decisions, evidence, owner reports, reversal and closeout. | AC4, AC5, AC7 | Build generic fixtures and inspect for private facts or consumer coupling. | To Do | 2 | Generic workspace templates, validator and focused tests | No | bounded-return |
| 4 | Add process falsifiers | Define waste signals and proportionate reduce/combine/correct/stop response. | AC6 | Run useful-review and wasteful-review matched cases. | To Do | 3 | Review reference, generic records and tests | No | bounded-return |
| 5 | Validate and hand off review | Run focused/full deterministic validation, privacy/diff checks and independent QA before exact-runtime work. | AC1, AC2, AC3, AC4, AC5, AC6, AC7 | Inspect validation and QA evidence against the parent AC map. | To Do | 4 | Validation artifacts and child workflow evidence | No | bounded-return |

## Parent AC Evidence

- AC7, AC8, AC9, AC10, AC11, AC12: Pending implementation evidence. Recipe-triggered claims must also be backed by `EVIDENCE.json`.

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

- Task: TASK-033
- Title: Implement Material Goal Review Contract
- Created: 2026-08-27
