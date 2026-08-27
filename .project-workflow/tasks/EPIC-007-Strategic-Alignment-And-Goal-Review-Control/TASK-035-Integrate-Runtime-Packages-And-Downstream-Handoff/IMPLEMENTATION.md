## User Story

As the product owner, I want one coherent prepared Strategic Advisor change and
an exact private-workspace handoff, so that public implementation, package
proof and real dogfood are neither conflated nor tightly coupled.

## Parent AC Coverage

- AC12, AC13, AC14, AC15, AC16, AC17

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

- AC12: owner `TASK-033, TASK-034, TASK-035`; required evidence: Dependency/private-data/diff scans, generic fixtures, runtime/package isolation and QA.
- AC13: owner `TASK-031, TASK-034, TASK-035`; required evidence: Frozen inventory, deterministic rebuild, category/ID validation, privacy and leakage proof.
- AC14: owner `TASK-034, TASK-035`; required evidence: Passing runtime-target/source claims, raw bounded outputs, exact identity, case verdicts and honest claim boundary.
- AC15: owner `TASK-034, TASK-035`; required evidence: Focused/full validation, bounded smoke, privacy/diff/package checks, Doctor, child QA and parent audit.
- AC16: owner `TASK-035`; required evidence: Cross-artifact claim matrix, generic template alignment, canonical release preparation and deterministic package proof.
- AC17: owner `TASK-035`; required evidence: Reviewed downstream brief with explicit repository, privacy, authority, dogfood and consumer boundaries.

## Acceptance Criteria

- [ ] AC1: Public declarations and generic templates match the proven behaviour.
- [ ] AC2: Generic records remain private-data-free and consumer-independent.
- [ ] AC3: Changed runtime packages are prepared, deterministic and independently verified.
- [ ] AC4: Full validation, QA and parent audits pass or retain explicit blockers.
- [ ] AC5: Downstream Strategy Workspace v1 brief is complete and non-mutating.
- [ ] AC6: Preparation is not misreported as publication, activation or support.

## Validation

- AC1-AC2: Claim-matrix, template, dependency, privacy and package-inventory checks.
- AC3-AC4: Runtime-target/source package evidence, full validation, QA and audits.
- AC5-AC6: Handoff and delivery-boundary review.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | not recorded | not recorded | not recorded | not recorded |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Align public contract | Update affected product, architecture, onboarding, host, runtime and generic-template declarations to the proven behaviour and claim boundary. | AC1, AC2, AC6 | Inspect cross-artifact matrix and dependency/private-data scans. | To Do | TASK-034 | Public contract, generic templates, runtime declarations and focused tests | No | bounded-return |
| 2 | Prepare deterministic packages | If allowlisted bytes changed, run canonical release preparation, build twice and independently verify exact identities and evaluation exclusion. | AC3, AC6 | Compare package bytes, provenance, manifest and verifier output. | To Do | 1 | Release state, generated packages/provenance and validation artifacts | No | bounded-return |
| 3 | Run integrated validation | Execute focused/full tests, validators, deterministic evaluations, affected smoke, privacy/diff/package checks and workflow audits. | AC4 | Re-run declared gates and inspect every explicit blocker. | To Do | 2 | Validation and workflow evidence only | No | bounded-return |
| 4 | Complete independent QA and parent audit | Review implementation, exact-runtime/package proof, intent preservation and invalid substitutes; generate parent acceptance evidence. | AC4, AC6 | Inspect QA independence, current intent audit and parent audit verdicts. | To Do | 3 | QA and parent workflow artifacts only | No | bounded-return |
| 5 | Produce private v1 handoff | Write the separate Strategy Workspace task brief with records, cadence, dogfood, falsifiers and consumer/authority boundaries. | AC5, AC6 | Confirm the brief is complete and no Strategy Workspace mutation occurred. | To Do | 4 | Handoff artifact only | No | bounded-return |

## Parent AC Evidence

- AC12, AC13, AC14, AC15, AC16, AC17: Pending implementation evidence. Recipe-triggered claims must also be backed by `EVIDENCE.json`.

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

- Task: TASK-035
- Title: Integrate Runtime Packages And Downstream Handoff
- Created: 2026-08-27
