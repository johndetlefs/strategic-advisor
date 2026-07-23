## User Story

As a maintainer or independent reviewer, I want the selective-invocation and multi-turn evaluation contract frozen before further behaviour changes, so that later claims can be tested against evidence that was not designed around the candidate answers.

## Goal

Extend the existing fail-closed evaluation system to actual multi-turn strategic dialogue, freeze the EPIC-002 authority, and retain an exact current-skill baseline that TASK-008 cannot silently redefine.

## Approach

- Extend the existing `skills/strategic-advisor/evals/` authority and `scripts/evaluation_harness.py` rather than creating a second evaluation system.
- Represent each multi-turn case as stable ordered turns with declared context boundaries, decision-property assertions, forbidden outcomes, and case-level hard gates.
- Add matched routing, altitude, preference-inversion, repetition, stale-context, and project-adjacency cases using synthetic/public content only.
- Freeze and commit authority plus runtime/context/tool identities before any baseline output exists; reject premature or incomplete artifacts.
- Run the exact current canonical/runtime skill as the baseline in fresh case contexts and retain failures without revising the frozen contract.

## Phases

### Phase 1 — Define complete EPIC-002 evaluation authority

- Add the case families, ordered turn schema, assertions, hard gates, aggregation rules, and coverage mapping.
- Validation: deterministic schema/coverage validation passes and no TASK-007 baseline output exists.

### Phase 2 — Enforce turn, identity, isolation, and leakage controls

- Extend freeze, planning, and artifact verification for real turn sequences and fresh case contexts.
- Add negative tests for premature results, authority drift, missing/reordered turns, context reuse, contamination, leaked authority, mismatched identities, and incomplete matrices.
- Validation: every isolated mutation fails with its expected stable diagnostic.

### Phase 3 — Freeze and capture the current-skill baseline

- Freeze the committed authority and exact current runtime identity, generate the declared work plan, and execute each case in a fresh context.
- Retain sanitised raw turns, classifications, assertion grades, and hard-gate verdicts; preserve failed or incomplete outcomes.
- Validation: the verifier recomputes completeness and verdicts against the frozen identities without reading private data.

### Phase 4 — Prove packaging boundaries and hand off

- Reproduce runtime/install artifacts and prove evaluation authority/results remain excluded.
- Record the frozen authority, baseline, known failure, and rerun identities for TASK-008.
- Validation: full local and clean-checkout gates pass, then QA/code review evaluates leakage, post-hoc drift, false activation controls, and result claims.

## Parent AC Coverage

- AC1, AC2, AC3, AC5, AC8, AC11, AC12, AC13

## Child Charter

### Inherited Invariants

- Strategic Advisor remains useful without a repository or workspace.
- The full strategic protocol is selectively invoked by decision intent and consequence, not by keywords, repository location, or workspace presence.
- Open exploration may remain conversational until a decision object emerges; readiness is not manufactured merely to complete a response template.
- Operate at the minimum sufficient altitude and return from exploration to a bounded decision or validation step.
- Dialogue may expand the option set; only qualifying evidence, scope, or constraints may change claim support or readiness.
- Opposite user preferences on the same material facts do not change the diagnosis.
- Stored context is input, never authority; provenance, conflict, freshness, and material limitations remain visible.
- Durable writes require explicit owner approval of the proposed change.
- Discussing projects in the same conversation does not authorise integration, shared storage, or a dependency between them.
- The private owner workspace never enters public source, examples, evaluations, packages, logs, or retained evidence.
- One canonical skill remains the only source of strategic logic.
- Host, workspace, connector, domain, and behavioural claims do not exceed direct current proof.

### Invalid Substitutes

- A repository template, documentation, or first-party enthusiasm in place of observed multi-turn behaviour.
- More conversational prose, more questions, or longer answers in place of genuinely distinct alternatives and decision-relevant exploration.
- Project or strategy vocabulary, repository location, or workspace presence in place of a material strategic decision that justifies invoking the full protocol.
- A readiness verdict, formal section structure, or strategic terminology added as ceremony to an ordinary factual, status, implementation, summarisation, simple-edit, or casual-ideation response.
- User agreement, repeated claims, polished narrative, or stored prior decisions in place of qualifying evidence.
- A single-turn prompt that narrates several turns in place of an actual fresh multi-turn interaction.
- A public fixture, copied example, or template-only check in place of authorised private-owner dogfood.
- Private workspace prose, reconstructable summaries, repository identifiers, or raw transcripts committed as public evidence.
- A host project, connector, memory store, or adapter-side prompt copy in place of the canonical skill and portable workspace contract.
- Local source files or a different package revision in place of exact runtime-package and host-source proof.
- Codex proof in place of Claude, ChatGPT, or general connector support.
- A supplied whole-person preference in place of a supported general-life, financial, medical, legal, family, relationship, business, or marketing domain.

### Artifact Targets

- Canonical behaviour: updated core skill/reference files under `skills/strategic-advisor/`, including the invocation boundary and proportional exploration-to-checkpoint transition.
- Workspace product surface: portable Markdown templates/instructions named by the runtime allowlist plus a deterministic scaffold builder and validator.
- Evaluation authority: frozen multi-turn cases, turn/context rules, case assertions, hard gates, and aggregation updates excluded from model-visible packages.
- Host proof: sanitised Codex trace identifying exact model, host, runtime package, workspace template, authorised source class, and observed result/write-control class.
- Public contract: bounded README, installation, architecture, and structured capability updates.
- Private dogfood: a separate private repository with no path, content, or reconstructable case data required in public artifacts.

### Parent AC Proof Ownership

- AC1: owner `Interactive Discovery child, Multi-Turn Evaluation child`; required evidence: Actual multi-turn outputs showing working position, exploration, reconvergence, and bounded tactical control.
- AC2: owner `Interactive Discovery child, Multi-Turn Evaluation child`; required evidence: Trigger and negative cases proving material altitude changes and return to a bounded decision.
- AC3: owner `Interactive Discovery child, Multi-Turn Evaluation child`; required evidence: Matched opposite-preference/repetition cases plus explicit evidence-delta findings and hard-gate verdicts.
- AC5: owner `Strategy Workspace child, Multi-Turn Evaluation child`; required evidence: Provenance/freshness/conflict validation and stale-context adversarial behaviour.
- AC8: owner `Multi-Turn Evaluation child`; required evidence: Frozen actual-turn matrix, assertions, hard gates, raw artifacts, and fail-closed result.
- AC11: owner `Interactive Discovery child, Multi-Turn Evaluation child`; required evidence: Matched intent-routing cases with shared vocabulary, false-positive controls, and a material-decision activation case.
- AC12: owner `Interactive Discovery child, Multi-Turn Evaluation child`; required evidence: Actual multi-turn exploration showing open dialogue, justified checkpoint timing, no manufactured readiness, and proportionate reconvergence.
- AC13: owner `Interactive Discovery child, Strategy Workspace child, Codex Owner Dogfood child, Multi-Turn Evaluation child, Onboarding child`; required evidence: Fresh-context host/workspace controls proving no location-triggered invocation, unnecessary reads, silent writes, or inferred coupling.

## Acceptance Criteria

- [ ] AC1: The frozen machine-readable inventory contains actual ordered-turn cases for active discovery, open exploration, checkpoint timing, reconvergence, bounded tactical response, and a return to a decision-useful next move. Covers parent AC1, AC8, and AC12.
- [ ] AC2: Matched shared-vocabulary routing cases hard-gate all six direct-assistance controls and a material strategic trigger. Covers parent AC11 and AC13.
- [ ] AC3: Altitude cases identify the decision-changing higher-level factor, reject unjustified escalation, and require a bounded return after justified escalation. Covers parent AC2.
- [ ] AC4: Preference-inversion and repetition cases conserve diagnosis/readiness on identical facts and classify the evidence delta explicitly. Covers parent AC3.
- [ ] AC5: Stale-context and project-adjacency cases hard-gate silent context selection, unnecessary access, unapproved writes, location-triggered invocation, and inferred coupling. Covers parent AC5 and AC13.
- [ ] AC6: Freeze and artifact verification fail on premature results, authority drift, turn defects, context reuse/contamination, leakage, identity mismatch, and incomplete results. Covers parent AC8.
- [ ] AC7: A sanitised exact-identity current-skill baseline is retained from fresh actual-turn contexts and can be independently rechecked without private content. Covers all assigned parent ACs.
- [ ] AC8: Deterministic clean-checkout validation passes, runtime/install artifacts exclude evaluation material, and public/task claims keep the baseline descriptive rather than validated candidate proof. Covers parent AC8 and AC13.

## Validation

- AC1-AC5: Validate schema and coverage, inspect stable case/turn IDs and matched facts, and review required/forbidden decision properties before freezing.
- AC6: Run isolated negative fixtures and assert stable diagnostics for every freeze, turn, isolation, leakage, identity, and completeness failure.
- AC7: Verify the retained baseline against the frozen manifest, exact runtime identity, declared fresh contexts, and complete raw-turn inventory.
- AC8: Run full local and clean-checkout validation, reproduce runtime/install artifacts twice, compare manifests, and inspect bounded capability language.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Define ordered-turn authority | Extend the evaluation schema and authority with actual multi-turn case/turn identities, context boundaries, assertions, hard gates, and aggregation rules. | AC1, AC6: ordered turns are machine-checkable and narrated/batch simulations cannot satisfy completeness. | Run `python3 scripts/validate.py --scope evals` and inspect generated coverage before any baseline result exists. | To Do |
| 2 | Add selective-routing and altitude cases | Add matched shared-vocabulary direct-assistance controls, material-decision triggers, justified altitude changes, and bounded-return expectations. | AC2, AC3: all routing controls and altitude outcomes are covered by stable cases and hard gates. | Inspect matched facts and run the eval coverage validator. | To Do |
| 3 | Add reality and continuity adversaries | Add opposite-preference, repetition, evidence-delta, stale-context, and cross-project-adjacency cases without private content. | AC4, AC5: unsupported readiness changes, silent context authority, unapproved writes, and inferred coupling are hard failures. | Review the paired inputs byte-for-byte and run private-data/coverage validation. | To Do |
| 4 | Enforce freeze and context integrity | Extend the harness and unit suite to reject premature output, authority drift, turn defects, context reuse/contamination, leakage, identity mismatch, and incomplete matrices. | AC6: every isolated invalid fixture fails with its named diagnostic while valid fixtures pass. | Run `python3 -m unittest discover -s tests -v`. | To Do |
| 5 | Freeze authority and runtime identity | Commit the complete authority, freeze it with exact runtime/context/tool identities, and generate the multi-turn baseline work plan before outputs. | AC1-AC6: the frozen identity predates every result and any authority change invalidates the plan. | Inspect Git and freeze manifests, then run the harness verification command. | To Do |
| 6 | Capture and verify current baseline | Execute the exact current skill in fresh actual-turn case contexts, retain sanitised raw artifacts, and calculate assertion/hard-gate outcomes without altering authority. | AC7: the baseline is complete or explicitly failed/incomplete, exact-identity, reproducible, and free of private data. | Re-run artifact verification and independently inspect a sample from each case family. | To Do |
| 7 | Prove exclusion and handoff | Reproduce runtime/install artifacts, prove evaluation files are excluded, run clean-checkout gates, and record exact TASK-008 comparison inputs and limitations. | AC8: deterministic validation passes and no claim treats the current baseline as proof of candidate effectiveness. | Compare repeated artifact hashes, inspect manifests, run `python3 scripts/validate.py`, and complete QA/code review. | To Do |

## Parent AC Evidence

- AC1, AC2, AC3, AC5, AC8, AC11, AC12, AC13: Pending the frozen authority, exact-identity current baseline, assertion grades, hard-gate verdicts, and deterministic validation described above. No built-in visual, external-contract, deployed-artifact, runtime-target/source, or responsive-visual proof recipe applies; behavioural evidence is owned by the frozen evaluation artifacts.

## QA & Code Review

- Verdict: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-007
- Title: Freeze Selective Invocation And Multi-Turn Evaluation Contract
- Created: 2026-07-23
