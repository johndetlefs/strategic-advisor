# Epic Contract

## Summary

- Epic: EPIC-007
- Title: Strategic Alignment And Goal Review Control
- Last updated: 2026-08-27

## Sources of Truth

- Owner-approved `REQUIREMENTS.md` for the exact Intent, R1-R25 and AC1-AC17
  authority envelope.
- `skills/strategic-advisor/SKILL.md` for the one canonical executable method,
  material-decision state, selective routing and response contract.
- `skills/strategic-advisor/references/recommendation-delta.md` for the released
  state-preservation and qualifying-delta contract that this Epic extends.
- `skills/strategic-advisor/references/conversational-strategy.md`,
  `evidence.md`, `readiness.md`, `competing-worlds.md`, `action-policy.md`,
  `response-contract.md`, `strategy-workspace.md` and `project-product.md` for
  adjacent interaction, evidence, action, workspace and outcome boundaries.
- `skills/strategic-advisor/workspace-templates/OBJECTIVES.md`, `DECISIONS.md`,
  `CHANGELOG.md` and `WORKSPACE.md` for generic portable record semantics, not
  John's private instance data.
- `PRODUCT-CONTRACT.md`, `ARCHITECTURE.md` and
  `skills/strategic-advisor/runtime-manifest.json` for product claims,
  canonical/runtime boundaries and exact model-visible bytes.
- `skills/strategic-advisor/evals/`, `scripts/build_evals.py`,
  `scripts/validate.py`, `scripts/drift_smoke.py`,
  `scripts/run_drift_smoke_live.py` and their tests for frozen synthetic case
  authority, deterministic validation and bounded exact-runtime proof.
- `distribution.json`, `scripts/release_state.py` and package builders/verifiers
  for prepared/current release identity and deterministic package authority.
- The approved 2026-08-27 Goal Review Workshop and Clarification Alignment
  Audit conclusions as design evidence only. Private task transcripts and
  Strategy Workspace facts are never repository sources of truth.
- The final durable disposition of `codex/proportionate-verification-runner` as
  a prerequisite source/base for runtime and evaluation implementation.
- Repository `AGENTS.md`, `.project-workflow/guidance.md`, Constitution and
  approved child requirements for delivery and proof rules.

## Invalid Substitutes

- A stated goal, metric, timeframe, desired tool or preferred solution in place
  of the confirmed underlying outcome and unacceptable substitutes.
- Activity, effort, task completion, output count, tool delivery, praise or
  visibility in place of material progress toward the goal.
- An initiative or recurring task labelled as a leading indicator without
  evidence that it predicts or drives the lag outcome.
- Arbitrary milestone interpolation in place of a causal/driver model.
- More questions in place of better alignment, or questions whose answers
  cannot materially change the supported action.
- Owner preference on an empirical fork in place of accessible evidence, or
  external evidence in place of an owner-only value or trade-off decision.
- Preserving all prior research after a material scope change in place of
  selective validity review, or restarting unaffected research in place of
  state preservation.
- Execution friction, sunk cost, non-execution, boredom, preference repetition
  or mechanism failure in place of evidence that the goal should change.
- Prior approval in place of justified revision when the goal is obsolete,
  mistaken, infeasible or no longer worth pursuing.
- A weekly status report, monthly summary or accountability ritual in place of
  decision-relevant review.
- Documentation, schema checks, unit tests, a plausible answer or model
  self-assessment in place of exact-runtime behavioural evidence.
- A bounded smoke, owner dogfood or exact-runtime case in place of comparative
  effectiveness, general support, parity, adoption or cross-host proof.
- Private transcripts, renamed private cases, Strategy Workspace facts, Daily
  Checklist data or reconstructable owner detail in place of synthetic,
  public or irreversibly sanitised regressions.
- A generic public template in place of accepted private Strategy Workspace
  operation, or private dogfood in place of public package/source identity.
- A package build or local prepared ZIP in place of protected-main integration,
  public publication, fresh download verification or host activation.

## Invariants

- `skills/strategic-advisor/` remains the only executable source of Strategic
  Advisor logic. This Epic extends existing state and reasoning; it does not
  add another advisor or state subsystem.
- Stated request, underlying outcome, object class, goal-purpose class,
  candidate action and readiness remain distinct.
- Bounded reconnaissance may precede alignment. Re-clarification requires both
  a material delta and an answer that can change the supported action.
- Empirical forks are researched proportionately; owner-only values,
  constraints, authority and trade-offs remain owner decisions.
- Settled state and unaffected evidence survive a reframe; only evidence whose
  scope, baseline or meaning changed is invalidated.
- Aspirations may remain visible. Discovery goals require bounded learning and
  operational goals require proportionate causal support. Readiness is never
  inferred from the goal-purpose label.
- Tasks and initiatives are not automatic leading indicators. Material
  progress requires evidence of outcome, driver, constraint or decision
  movement.
- Goal change is challenged but not prohibited. A qualifying evidence,
  constraint, value, trade-off or opportunity-cost delta and explicit owner
  authority permit proportionate revision.
- Event review can pre-empt scheduled cadence. Weekly and monthly cadence are
  configurable conventions, not universal laws or accountability devices.
- Goal and path dispositions remain separate and identify the exact target of
  continue, correct, pivot, pause, replace or stop.
- Strategy Workspace is the private durable strategic authority. Daily
  Checklist, Sunday and Project Workflow remain separate consumers or process
  systems with no implicit runtime, data or authority coupling.
- Only synthetic, public or irreversibly sanitised cases may be committed. No
  private or reconstructable task, workspace, employer, client or household
  data enters public source, runtime, evaluation or package artifacts.
- Exact proof claims remain separated across documented semantics,
  deterministic/static validation, exact-runtime synthetic behaviour, private
  real-task dogfood, package identity, publication, host activation, support,
  adoption and effectiveness.
- The in-flight proportionate-verification-runner worktree is preserved and
  reconciled before runtime/evaluation implementation; this Epic does not
  absorb, overwrite or recreate it.
- The downstream Strategy Workspace process is a real v1 to dogfood and
  iterate, not a disposable pilot, but it remains a separate repository task.
- An allowlisted runtime-byte change prepares the next immutable distribution
  in the same implementation branch. Push, PR, merge, publication,
  finalisation, activation and private-workspace mutation require separate
  authority and exact evidence.

## Artifact Targets

- Canonical reasoning: `skills/strategic-advisor/SKILL.md`,
  `references/recommendation-delta.md`,
  `references/conversational-strategy.md`, `references/evidence.md`,
  `references/action-policy.md`, `references/response-contract.md`,
  `references/strategy-workspace.md`, `references/project-product.md`, and only
  other directly affected allowlisted references.
- Generic portable records: `workspace-templates/OBJECTIVES.md`,
  `DECISIONS.md`, `CHANGELOG.md`, `WORKSPACE.md` and validator/builder tests,
  without any private instance data.
- Evaluation authority: `evals/core_cases.json`, `eval_queries.json`,
  `recommendation_gate_cases.json`, `drift_smoke_cases.json`, generated
  `evals.json`, the smallest necessary case/assertion/runner changes and exact
  raw result artifacts kept outside the model-visible runtime.
- Public contract: `PRODUCT-CONTRACT.md`, `ARCHITECTURE.md`, `README.md`,
  `INSTALL.md`, onboarding/agent metadata and only directly affected
  contributor/security documentation.
- Runtime/package declarations: `runtime-manifest.json`, `distribution.json`,
  generated install-artifact provenance, exact inventories and deterministic
  package comparison.
- Retained proof: child `EVIDENCE.json`, deterministic validation output,
  exact-runtime target/source/activation evidence, sanitised raw case outputs,
  case-level verdicts, independent QA, parent audit and explicit blockers.
- Downstream handoff: a public-contract-derived Strategy Workspace v1 brief
  identifying private record, dogfood, Sunday and Daily Checklist boundaries
  without mutating that repository or copying its facts.
- Workflow: EPIC-007 requirements, contract, decomposition, child artifacts,
  tracker, intent audit, acceptance map/audit, deferrals/amendments if required
  and retro.

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | TASK-032 | Canonical state/recommendation-delta diff, duplicate-state scan, matched preservation assertions and QA. |
| AC2 | TASK-031, TASK-032, TASK-034 | Frozen positive/negative authority, direct/reconnaissance/alignment cases, exact-runtime verdicts and QA. |
| AC3 | TASK-031, TASK-032, TASK-034 | Stateful delta/fork/selective-invalidation cases, raw sequence outputs, exact-runtime verdicts and QA. |
| AC4 | TASK-031, TASK-032, TASK-034 | Goal/proxy ladder cases, object-class assertions and exact-runtime review. |
| AC5 | TASK-031, TASK-032, TASK-034 | Aspiration/discovery/operational and readiness cases with stateful assertions and verdicts. |
| AC6 | TASK-031, TASK-032, TASK-034 | Causal indicator/milestone cases, evidence-field assertions and exact-runtime verdicts. |
| AC7 | TASK-033, TASK-034 | Generic event/weekly/monthly contract, cadence negative controls and case-level verdicts. |
| AC8 | TASK-033, TASK-034 | Material-progress and enabling-project cases with evidence and case-level verdicts. |
| AC9 | TASK-033, TASK-034 | Drift and goal-amendment cases proving challenged replacement and justified revision paths. |
| AC10 | TASK-033, TASK-034 | Generic record schema, owner-reconciliation fixtures, two-axis disposition cases and QA. |
| AC11 | TASK-031, TASK-033, TASK-034 | Process-waste case authority, contract rules, exact-runtime cases and proportionality review. |
| AC12 | TASK-033, TASK-034, TASK-035 | Dependency/private-data/diff scans, generic fixtures, runtime/package isolation and QA. |
| AC13 | TASK-031, TASK-034, TASK-035 | Frozen inventory, deterministic rebuild, category/ID validation, privacy and leakage proof. |
| AC14 | TASK-034, TASK-035 | Passing runtime-target/source claims, raw bounded outputs, exact identity, case verdicts and honest claim boundary. |
| AC15 | TASK-034, TASK-035 | Focused/full validation, bounded smoke, privacy/diff/package checks, Doctor, child QA and parent audit. |
| AC16 | TASK-035 | Cross-artifact claim matrix, generic template alignment, canonical release preparation and deterministic package proof. |
| AC17 | TASK-035 | Reviewed downstream brief with explicit repository, privacy, authority, dogfood and consumer boundaries. |
