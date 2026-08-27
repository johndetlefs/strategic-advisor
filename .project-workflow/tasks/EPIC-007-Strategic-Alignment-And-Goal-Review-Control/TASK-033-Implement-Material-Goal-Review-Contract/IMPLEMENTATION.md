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
- Retained proof for this source-only child: deterministic contract, schema,
  privacy, manifest and frozen-authority checks plus one affected-only
  independent QA verdict. TASK-034 remains the separately authorised owner of
  exact-runtime behavioural evidence and is held by the owner checkpoint.
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

- [x] AC1: Event, weekly and monthly review purposes are distinct and configurable.
- [x] AC2: Material-progress and enabler-credit rules reject activity substitution.
- [x] AC3: Drift and goal-amendment controls challenge changes but permit justified revision.
- [x] AC4: Goal/path decisions retain complete evidence, authority and closeout fields.
- [x] AC5: Offline owner evidence is reconciled with provenance and freshness.
- [x] AC6: Process-waste falsifiers cause proportionate correction or stopping.
- [x] AC7: Generic runtime/templates stay private-data-free and consumer-independent.

## Validation

- AC1-AC6: Frozen review contract cases and generic schema fixtures.
- AC7: Dependency, privacy, diff, runtime-manifest and package-exclusion checks.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/strategic-alignment-goal-review-pw08` from `41a383b`; QA source `4fe1537` | 26 focused tests plus skill, privacy, links and frozen-build checks pass; one affected-only independent QA Pass | Local source only; no push, package, release, activation or private mutation | `VALIDATION.md`; Clarification Alignment affected-only review |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Define review control | Add event, weekly and monthly purposes and route qualified decision state into the appropriate review. | AC1 | Inspect the contract and run event-versus-cadence cases. | Done | TASK-032 | Canonical review reference and directly affected core routing | No | bounded-return |
| 2 | Implement progress and drift tests | Add material-progress, enabler-credit, drift and amendment burden rules. | AC2, AC3 | Run activity/progress and justified/unjustified amendment cases. | Done | 1 | Same review reference and directly affected tests | No | bounded-return |
| 3 | Add generic records and reconciliation | Update portable templates/semantics for two-axis decisions, evidence, owner reports, reversal and closeout. | AC4, AC5, AC7 | Build generic fixtures and inspect for private facts or consumer coupling. | Done | 2 | Generic workspace templates, validator and focused tests | No | bounded-return |
| 4 | Add process falsifiers | Define waste signals and proportionate reduce/combine/correct/stop response. | AC6 | Run useful-review and wasteful-review matched cases. | Done | 3 | Review reference, generic records and tests | No | bounded-return |
| 5 | Validate review contract | Run focused deterministic validation and privacy/diff checks before the separate affected-only QA gate. | AC1, AC2, AC3, AC4, AC5, AC6, AC7 | Inspect validation evidence against the parent AC map. | Done | 4 | Validation artifacts and child workflow evidence | No | bounded-return |

## Parent AC Evidence

- AC7: `goal-review.md` event/weekly/monthly rules and cadence checks.
- AC8: `goal-review.md` material-progress/enabler test and focused checks.
- AC9: `goal-review.md` drift/amendment burden and focused checks.
- AC10: `goal-review.md`, `strategy-workspace.md` and generic template record
  and owner-reconciliation checks.
- AC11: `goal-review.md` process-waste falsifiers and SAGR-020 mapping.
- AC12: Runtime manifest, privacy checks and consumer-independent generic
  templates. Exact-runtime and delivery proof remain held in TASK-034/TASK-035.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pass
- Intent adversarial verdict: Pass
- Could every AC pass while the approved user job remains undone: No
- Intent audit state: current
- Intent scope note: The verdict covers the bounded deterministic
  source-semantics job. Runtime behaviour and real-task value remain explicitly
  unproved; QA inspected source `4fe1537`.
- Outcome journey evidence: Not claimed by TASK-033. The next authorised gate
  is one owner-visible read-only dogfood before any TASK-034/TASK-035 work.
- Reviewer independence: Existing Clarification Alignment Audit task; read-only
  affected scope, no implementation edits.
- Evidence: Reviewer inspected `41a383b..4fe1537`, reproduced 26 focused tests,
  skill/privacy/link validation, the unchanged 56-case eval inventory and the
  unchanged 20-case/37-criterion freeze.
- Findings: None. No correction pass was required.

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-033
- Title: Implement Material Goal Review Contract
- Created: 2026-08-27
- Owner checkpoint: finish the smallest usable TASK-033 and one affected-only
  QA verdict, then stop for a read-only owner-visible dogfood. TASK-034 and
  TASK-035 require new explicit owner authority.
