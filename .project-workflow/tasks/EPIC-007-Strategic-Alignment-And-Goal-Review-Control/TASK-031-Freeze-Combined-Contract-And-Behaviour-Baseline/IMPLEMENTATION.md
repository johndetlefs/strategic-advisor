## User Story

As the Strategic Advisor implementation and QA owner, I want one frozen
pre-treatment contract and baseline, so that implementation cannot redefine
success after observing its own behaviour.

## Parent AC Coverage

- AC2, AC3, AC4, AC5, AC6, AC11, AC13

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
- Retained proof for this child: deterministic validation output, frozen
  identities, sanitised case authority and provenance review, independent QA,
  parent audit and explicit blockers. Behavioural execution evidence and raw
  verdicts belong to TASK-034.
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

## Acceptance Criteria

- [ ] AC1: `FREEZE-MANIFEST.json` binds untreated source commit `6d65830`,
  its tree, alpha.6 release/runtime identity and 19 current runtime/evaluation
  file hashes. The freeze check reads baseline bytes from that Git commit, so
  later treatment cannot redefine the baseline.
- [ ] AC2: `CASE-AUTHORITY.json` contains 20 stable SAGR cases and 37 criteria,
  with all 20 approved categories represented exactly once, required and
  forbidden behaviours, hard negative controls and three multi-turn sequences.
- [ ] AC3: `PROVENANCE-REVIEW.md` records a case-by-case synthetic privacy
  review. A scoped identifier scan found no owner, private-workspace, named
  project or audited-example strings in the authority.
- [ ] AC4: `build_goal_review_freeze.py --check` reproduces the derived
  inventory, validates exact IDs/categories/turn references and rejects runtime
  inclusion. Four focused mutation tests and the existing evaluation/privacy
  validators pass.
- [ ] AC5: `CLAIM-PROOF-MATRIX.md` separates documented semantics,
  deterministic structure, exact-runtime synthetic behaviour and private
  dogfood. `FREEZE-MANIFEST.json` retains the unresolved runner/base dependency;
  no new general evaluator or treatment byte was added.

## Validation

- AC1: Baseline hash/inventory review.
- AC2-AC3: Case-by-case authority and provenance review.
- AC4: Deterministic builder, category/ID, privacy and package-exclusion checks.
- AC5: Claim/proof sufficiency review against repository guidance.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | `codex/strategic-alignment-goal-review` from `6d65830` | 175 unit tests; freeze, evaluation-build, evaluation-scope, privacy and diff checks pass | Local implementation only; no push, PR, merge, package, publication, activation or private-workspace mutation | `VALIDATION.md`, frozen artifacts and repository diff |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Capture untreated baseline | Record exact alpha.6 source, runtime, package, evaluation and current runner identities plus claim boundaries. | AC1, AC5 | Inspect retained identities and confirm no runtime byte changed. | Done |  | Workflow docs and freeze artifact only | No | bounded-return |
| 2 | Freeze sanitised case authority | Add the minimum synthetic matched and sequenced cases with stable IDs, assertions, forbidden behaviours and provenance. | AC2, AC3 | Review every case against the approved R22 matrix and privacy boundary. | Done | 1 | Evaluation authority and freeze artifacts only | No | bounded-return |
| 3 | Prove deterministic isolation | Rebuild derived inventories and run category, ID, privacy, leakage and runtime-package exclusion checks. | AC3, AC4 | Re-run the declared commands and compare generated bytes. | Done | 2 | Builders, validators and focused tests only if required by frozen claim | No | bounded-return |
| 4 | Close the baseline handoff | Record the final freeze identity, proof matrix and runner/base prerequisite for TASK-032 and TASK-034. | AC1, AC5 | Confirm downstream tasks cite the exact frozen identity and external blocker. | Done | 3 | Child workflow evidence and handoff notes | No | bounded-return |
| 5 | Remediate adversarial QA | Add omitted phase-change, classification and milestone behaviours; strengthen pairing, state, identity and isolation checks; correct downstream lifecycle; obtain affected-only re-review. | AC1-AC5 | Re-run the frozen checks and inspect the peer QA disposition without viewing treatment output. | In Progress | 4 | TASK-031 authority, builder/tests and workflow evidence only | No | bounded-return |

## Parent AC Evidence

- AC2-AC6, AC11 and AC13: TASK-031 now owns a frozen, privacy-reviewed case
  authority and proof boundary. This establishes only pre-treatment authority
  and deterministic structure; TASK-032, TASK-033 and TASK-034 still own the
  documented runtime semantics and exact-runtime behavioural results required
  for parent acceptance. No structured proof recipe applies to this
  baseline-only child, so `EVIDENCE.json` remains empty by design.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Changes Requested on commit `03dc06c`; remediation in progress.
- Intent adversarial verdict: Fail. The structural checks could pass while
  approved state-resumption, classification and milestone behaviours remained
  absent.
- Could every AC pass while the approved user job remains undone: Yes, before
  remediation.
- Intent audit state: Current at review time.
- Outcome journey evidence: Review found no owner-answer/resumed-recommendation
  turn after re-clarification and no executable state-transition assertions.
- Reviewer independence: Adversarial peer reviewer supplied some audit
  requirements but did not implement this branch; not fully implementation-blind.
- Evidence: Clarification Alignment Audit task, read-only QA of commit `03dc06c`,
  2026-08-27.
- Findings: P1 incomplete approved behaviours; P1 wording/restatement controls;
  P1 overclaimed identity binding; P2 weak runtime-isolation guard; P2
  downstream tasks incorrectly marked In Progress. All are accepted.

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-031
- Title: Freeze Combined Contract And Behaviour Baseline
- Created: 2026-08-27
