# Requirements

## Summary

- Task: TASK-035
- Title: Integrate Runtime Packages And Downstream Handoff
- Parent AC Coverage: AC12, AC13, AC14, AC15, AC16, AC17
- Last updated: 2026-08-27
- Intent contract: full

## Intent

Make the accepted public behaviour internally consistent across runtime,
generic templates, product claims and deterministic packages; publish and
fresh-verify the next experimental prerelease; then install that public artifact
in the owner's Codex. The separate Strategy Workspace handoff is deferred from
this release by owner authority.

## Intent Spine

- OC1 — Completion capability: A user can obtain one coherent, publicly
  downloadable Strategic Advisor prerelease whose exact artifact is verified
  and loaded in the owner's Codex with no ambiguity about proof boundaries.
- OC2 — Material capabilities: Cross-artifact claim alignment, generic record
  validation, runtime/package identity, deterministic release preparation,
  public-download verification and exact local activation.
- OC3 — Success journey: Accept the bounded TASK-034 evidence, align claims,
  prepare and verify immutable packages, merge and publish the prerelease,
  fresh-download it, install the public ZIP and confirm a fresh Codex load.
- OC4 — Successful-but-wrong result: A local ZIP called released, generic
  templates called private dogfood, unsupported claims, copied private facts,
  consumer coupling, or a handoff that silently authorises mutation is wrong.
- OC5 — Exclusions: No support, parity, adoption or effectiveness claim; no
  private workspace mutation, Sunday update or Daily Checklist integration.
- OC6 — Assumptions: TASK-034 has an honest exact-runtime verdict and the
  current canonical release tooling remains authoritative.
- OC7 — Authority source: Parent Epic Intent and approved decomposition row.

## Owner Approval

- Intent reviewed and accurately reflected: Yes
- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Inherited from approved parent decomposition
- Approved for implementation: Yes
- Approved scope envelope: Prepare, push, merge, publish, fresh-verify, install and activate the next experimental prerelease; defer the separate Strategy Workspace handoff
- Approved by: John (owner)
- Approval date: 2026-08-27
- Approval note / source: Current Codex task directive to finish the release and local update without further approval prompts; coordination amendment `owner-release-scope-2026-08-27`
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

- AC12: owner `TASK-033, TASK-034, TASK-035`; required evidence: Dependency/private-data/diff scans, generic fixtures, runtime/package isolation and QA.
- AC13: owner `TASK-031, TASK-034, TASK-035`; required evidence: Frozen inventory, deterministic rebuild, category/ID validation, privacy and leakage proof.
- AC14: owner `TASK-034, TASK-035`; required evidence: Passing runtime-target/source claims, raw bounded outputs, exact identity, case verdicts and honest claim boundary.
- AC15: owner `TASK-034, TASK-035`; required evidence: Focused/full validation, bounded smoke, privacy/diff/package checks, Doctor, child QA and parent audit.
- AC16: owner `TASK-035`; required evidence: Cross-artifact claim matrix, generic template alignment, canonical release preparation and deterministic package proof.
- AC17: owner `TASK-035`; required evidence: Reviewed downstream brief with explicit repository, privacy, authority, dogfood and consumer boundaries.

## Goal

Close the experimental public release boundary cleanly and leave the owner's
current Codex running the exact fresh-verified public artifact.

## Non-Goals

- Promoting the prerelease to supported, cross-model, cross-host, adopted or
  effective without separate evidence.
- Claiming the private review process has been dogfooded or accepted.
- Storing John's facts in public templates, cases or handoff examples.
- Adding runtime dependencies on any downstream consumer.

## Users & Context

Canonical runtime changes must stay aligned with product declarations and
immutable packages. The eventual private process must consume that accepted
contract, but this repository cannot own Strategy Workspace workflow state or
mutations.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- R1. Reconcile every changed canonical behaviour across product contract,
  architecture, README/install/onboarding, host metadata, runtime manifest,
  generic workspace templates, validators and package declarations.
- R2. Keep capability language no stronger than TASK-034 evidence; preserve
  implemented-not-validated, exact-host and private-dogfood boundaries.
- R3. Validate generic templates and fixtures for complete goal/review semantics
  without private facts, consumer identifiers or implied write authority.
- R4. If allowlisted runtime bytes changed, prepare the next immutable
  distribution through the canonical release command, build twice and verify
  source/runtime/provenance/package identity and evaluation exclusion.
- R5. Run focused and full deterministic tests, aggregate validators, the
  bounded TASK-034 affected smoke, privacy/diff/package checks, Project Workflow
  Doctor, one child QA and parent acceptance/intent audits; retain blockers
  honestly without commissioning another behavioural campaign.
- R6. Publish the prepared GitHub prerelease, fresh-download and verify its
  exact public artifacts, install the public standalone Skill into the owner's
  Codex and confirm fresh runtime loading.
- R7. Record the owner-approved deferral of the separate Strategy Workspace v1
  handoff; it is not a release or activation prerequisite.

## Acceptance Criteria (Verifiable)

- AC1: Product/runtime/architecture/onboarding/host/template declarations are
  internally consistent and no stronger than exact evidence.
- AC2: Generic template builds and fixtures pass complete review semantics,
  privacy, dependency and authority-boundary checks.
- AC3: Any changed runtime is bound to a newly prepared immutable identity; two
  clean package builds are byte-identical and independently verified with no
  evaluation leakage.
- AC4: Focused/full deterministic validation, bounded exact-runtime evidence,
  privacy/diff/package checks, one child QA, current intent audit and parent
  acceptance audit pass or retain explicit blockers without claim weakening.
- AC5: The public prerelease is fresh-downloaded, byte/provenance verified,
  installed locally and observed loading its new goal-review runtime; the
  separate private handoff remains an approved deferral.
- AC6: Publication and activation remain distinct from support, parity,
  adoption and effectiveness.

## Open Questions (Answer Needed)

- None. Creating the separate Strategy Workspace task and executing the handoff
  remains a later owner-authorised repository action.

## Decisions (Resolved)

- D1. Align every affected public artifact from one canonical runtime.
- D2. Prepare, merge and publish the changed runtime as the next immutable
  experimental prerelease, then verify it from the public download.
- D3. Treat generic templates and private dogfood as different proof layers.
- D4. Defer the downstream Strategy Workspace brief; end this task with public
  artifact verification and exact local Codex activation.

## Validation Plan

- AC1-AC2: Cross-artifact claim matrix, generic fixture validation,
  dependency/private-data scans and runtime/package inventory review.
- AC3: Runtime-target/source proof for canonical release preparation, repeated
  clean builds, independent verification and evaluation exclusion.
- AC4: Full repository validation, retained TASK-034 evidence, workflow Doctor,
  independent child QA, current intent audit and parent audit.
- AC5-AC6: Verify public release metadata and downloaded bytes, install the
  public standalone ZIP, prove fresh Codex source loading, and verify that no
  unsupported claim or private-workspace mutation occurred.
