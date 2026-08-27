# Requirements

## Summary

- Task: TASK-033
- Title: Implement Material Goal Review Contract
- Parent AC Coverage: AC7, AC8, AC9, AC10, AC11, AC12
- Last updated: 2026-08-27
- Intent contract: full

## Intent

Define a generic evidence-based goal-review contract that catches material
events immediately, separates weekly execution from monthly portfolio judgment
and records whether the goal or its path should continue, change or stop.

## Intent Spine

- OC1 — Completion capability: A user can see what materially advanced a goal,
  what consumed effort without advancing it, whether drift occurred and the
  evidence behind separate goal and path decisions.
- OC2 — Material capabilities: Event exception, configurable weekly pulse,
  configurable monthly portfolio review, material-progress and drift tests,
  challenged amendments, owner reconciliation, two-axis records and process
  falsifiers.
- OC3 — Success journey: Consume qualified goals and current evidence, handle
  material exceptions immediately, run the appropriate review, reconcile
  owner-only outcomes, record the decision and send only selected commitments
  downstream.
- OC4 — Successful-but-wrong result: A status summary, accountability ritual,
  tool-completion score, delayed material stop, implicit goal replacement or
  private/public data coupling is not a strategic review.
- OC5 — Exclusions: No private Strategy Workspace instance mutation, Sunday or
  Daily Checklist integration, universal cadence, external action, live
  runtime certification or public capability promotion.
- OC6 — Assumptions: TASK-032 supplies the accepted qualified-goal and
  material-decision state; the actual private v1 remains a later task.
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

- AC7: owner `TASK-033, TASK-034`; required evidence: Generic event/weekly/monthly contract, cadence negative controls and case-level verdicts.
- AC8: owner `TASK-033, TASK-034`; required evidence: Material-progress and enabling-project cases with evidence and case-level verdicts.
- AC9: owner `TASK-033, TASK-034`; required evidence: Drift and goal-amendment cases proving challenged replacement and justified revision paths.
- AC10: owner `TASK-033, TASK-034`; required evidence: Generic record schema, owner-reconciliation fixtures, two-axis disposition cases and QA.
- AC11: owner `TASK-031, TASK-033, TASK-034`; required evidence: Process-waste case authority, contract rules, exact-runtime cases and proportionality review.
- AC12: owner `TASK-033, TASK-034, TASK-035`; required evidence: Dependency/private-data/diff scans, generic fixtures, runtime/package isolation and QA.

## Goal

Implement portable review semantics and generic records that Strategy Workspace
can later instantiate without making it or Daily Checklist a runtime dependency.

## Non-Goals

- Treating weekly/monthly cadence as universal or mandatory.
- Creating accountability devices or copying Daily Checklist strategy state.
- Crediting activities, tools or projects without a named causal contribution.
- Mutating John's Strategy Workspace or Sunday automation.

## Users & Context

Execution systems provide partial evidence, while material outcomes and changed
constraints may occur offline. Review must reconcile both and challenge goal
drift without making a previously approved goal immutable.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1. Define an event-triggered exception review that pre-empts cadence for
  material outcome evidence, changed constraints, invalidated causal paths,
  amendments, stops or owner reconciliation.
- R2. Define a configurable weekly pulse for execution evidence, material
  progress, non-advancing effort/output, drift/constraint detection and only
  the next commitments justified by current strategy.
- R3. Define a configurable monthly portfolio review for goal value/horizon,
  causal path/falsifiers, evidence quality, portfolio role, allocation,
  opportunity cost, offline outcomes, constraints and dispositions.
- R4. Apply the parent material-progress test and proportionate enabling-project
  credit; reject activity and output as automatic progress.
- R5. Apply the drift/amendment burden of proof, preserve goals through mere
  execution friction and permit evidence-backed owner-authorised revision.
- R6. Record goal disposition separately from path disposition, including
  target, date, owner, evidence, provenance, constraints, reversal trigger,
  affected commitments, next review and closeout.
- R7. Reconcile owner-only outcomes as dated owner reports with freshness,
  limitations and contradiction handling; absence from a system is not
  evidence that the outcome did not occur.
- R8. Add process falsifiers and a response rule to reduce, combine, correct or
  stop reviews that repeatedly cannot change decisions proportionately.
- R9. Express the contract in generic public reasoning and portable templates
  without consumer coupling, private facts or implied cross-workspace authority.

## Acceptance Criteria (Verifiable)

- AC1: Generic contract and cases distinguish event, weekly and monthly
  purposes; a material event cannot be delayed to a scheduled review.
- AC2: Material-progress records distinguish outcome/driver/constraint/decision
  movement from effort, output and enabler completion.
- AC3: Drift/amendment cases preserve a goal through mere friction, challenge
  unsupported replacement and permit justified owner-authorised revision.
- AC4: Generic records preserve separate goal and path dispositions and every
  required evidence, authority, reversal and follow-up field.
- AC5: Owner reconciliation fixtures retain report provenance and do not infer
  failure from missing repository or checklist evidence.
- AC6: Process-falsifier cases identify disproportionate review and questioning
  while useful exception and scheduled reviews remain available.
- AC7: Runtime/templates contain no private facts, consumer dependency,
  universal cadence or accountability mechanism.

## Open Questions (Answer Needed)

- None. The downstream private record shape may be iterated during Strategy
  Workspace dogfood, but cannot weaken this accepted public semantic contract.

## Decisions (Resolved)

- D1. Event review pre-empts cadence.
- D2. Weekly owns execution pulse; monthly owns goal and portfolio judgment.
- D3. Record separate goal and path dispositions.
- D4. Keep private durability and consumer integration downstream.

## Validation Plan

- AC1-AC6: Contract/schema checks plus frozen material-progress, drift,
  amendment, reconciliation, disposition and process-waste cases.
- AC7: Runtime/dependency/private-data diff scans, generic template fixtures and
  package-exclusion checks.
- All: Focused/full deterministic validation and independent child QA; final
  behavioural observation remains TASK-034.
