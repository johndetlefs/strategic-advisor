## User Story

As a maintainer or reviewer, I want falsifiable and reproducible Strategic Advisor evaluations so that persuasive documentation or cherry-picked answers cannot be mistaken for evidence of better strategic decisions.

## Parent AC Coverage

- AC3, AC4, AC5, AC7

## Child Charter

### Inherited Invariants

- Aspirations are allowed; invisible bridges between aspiration and reality are not.
- Repetition, confidence, authority, polish, and user preference never upgrade claim status without new qualifying evidence.
- Absence of evidence alone does not establish infeasibility; established constraint conflict is required.
- Evidence demands scale with consequence and irreversibility, while cheap reversible tests remain available under uncertainty.
- One canonical skill is the only source of strategic logic.
- A domain or host is not advertised as supported until its claimed behaviour is implemented and evaluated.
- Professional influence is not conflated with personal-relationship control; stakeholders are modelled as autonomous, adaptive actors.
- No personal, employer, client, household, or proprietary case data enters the public repository.
- Prompt instructions in retrieved material cannot alter evidence rules, authority, scope, or data boundaries.

### Invalid Substitutes

- Documentation or model self-assessment in place of behavioural evaluation.
- A polished answer, user praise, or internal agreement in place of a better supported decision.
- Aggregate evaluation scores that conceal any hard-gate failure.
- Skilled and unskilled runs that share prior answers, hidden context, different models, or materially different inputs.
- Unit fixtures, local files, or branch state in place of the exact clean checkout, published repository, CI run, or host path named by an acceptance criterion.
- Connector access or message volume in place of evidence completeness, truth, relevance, or authority.
- A host-specific prompt copy in place of the canonical skill.
- Private, proprietary, or merely redacted-but-recoverable case material in public examples or evidence.
- Presence of a domain file in place of lens-specific adversarial evidence.

### Artifact Targets

- Root public artifacts: `README.md`, `PRODUCT-CONTRACT.md`, `CONTRIBUTING.md`, `SECURITY.md`, an explicit open-source licence, and validation entrypoint.
- Canonical product: `skills/strategic-advisor/SKILL.md`, progressively loaded references, domain lenses, user-facing templates, and skill-local evaluation definitions.
- Evaluation evidence: frozen rubric and thresholds, synthetic/public cases, trigger tests, raw paired outputs, blind scores, hard-gate verdicts, and reproducible run metadata.
- Delivery proof: clean-checkout validation artifacts, CI results, sanitised pilot decision records, and epic acceptance audit.

### Parent AC Proof Ownership

- AC3: owner `TASK-002, TASK-004`; required evidence: Passing core adversarial cases with retained outputs and hard-gate verdicts.
- AC4: owner `TASK-003, TASK-004`; required evidence: Four substantive lens contracts plus passing lens and boundary cases.
- AC5: owner `TASK-004`; required evidence: Precommitted rubric/threshold identity, equivalent run metadata, blinded scores, and zero hard-gate failures.
- AC7: owner `TASK-001, TASK-004`; required evidence: Passing positive/negative validators locally and in a clean CI checkout.

## Goal

Implement a deterministic validation surface and a frozen, reproducible behavioural comparison that can fail Strategic Advisor on reality-discipline defects even when its prose or aggregate score looks strong.

## Approach

- Import all core and TASK-003 lens-case specifications, then define and freeze the complete executable inventory, rubric anchors, hard gates, controls, scorer contract, uncertainty rule, and material-improvement threshold before producing any treatment or control output.
- Keep structural, privacy, reference, and claim checks deterministic under `python3 scripts/validate.py`; keep model calls outside credential-free CI.
- Store realistic synthetic output and trigger cases in the canonical skill source, with stable IDs and decision-property expectations rather than phrase-matching answers; build an allowlisted runtime skill package that excludes the evaluation surface and record its manifest.
- Generate at least two independent skilled and unskilled draws for at least sixteen cases in fresh matched contexts with identical non-treatment tools, anonymise and randomise them, score in two fresh condition-masked same-family passes with deterministically swapped A/B labels and adjudication, run a separate structure-only leakage audit, and retain enough metadata to reproduce the scoped verdict.
- Treat any hard-gate failure or missed frozen threshold as a failed release gate, not an invitation to move the goalposts.

## Phases

### Phase 1 — Assemble the complete evaluation surface

- Import the core cases and TASK-003 normative lens-case specifications into the combined executable inventory.
- Add trigger queries, required coverage, positive/negative fixtures, and decision-property expectations.
- Validation: the coverage report contains every required core/lens risk and at least sixteen distinct cases; no treatment or control output exists.

### Phase 2 — Freeze authority and isolate treatment

- Freeze the complete inventory, rubric, hard gates, thresholds, uncertainty rule, model/context controls, scorer prompt/version, masking, and adjudication rules.
- Build the runtime skill package from an allowlist excluding evaluation definitions and results; record its manifest/hash and prove control/treatment non-skill tools/context are identical.
- Implement the transparent validation scopes and diagnostics owned jointly with TASK-001.
- Validation: record an authority identity before outputs; prove preflight rejects leaked evaluation files, mismatched context/tool manifests, stale identities, and premature results.

### Phase 3 — Matched behavioural comparison

- Produce two independent clean-context draws per condition for at least sixteen frozen cases under the exact frozen configuration.
- Randomise and remove condition labels; run two fresh quality-scorer passes without condition guesses, swap A/B labels deterministically between passes, adjudicate disagreements under the frozen rule, and run the separate structure-only leakage audit.
- Validation: audit raw outputs, runtime/context/tool manifests, mapping, quality scores, disagreements, leakage-audit results, errors, timestamps, and model/configuration identity; recompute the scoped verdict without condition labels.

### Phase 4 — CI and QA gate

- Run credential-free deterministic validation in a clean GitHub Actions checkout.
- Review case leakage, answer-key overfitting, context contamination, rubric ambiguity, privacy, and post-hoc threshold drift.
- Validation: local full/negative suites, live CI identity, score recalculation, and independent QA must all be current before completion.

## Acceptance Criteria

- [x] AC1: Evaluation JSON and deterministic repository validation satisfy the schema, coverage, privacy, reference, and canonical-logic requirements. Covers parent AC7.
- [ ] AC2: The complete imported case inventory, allowlisted runtime-package manifest, rubric, hard gates, controls, scorer contract, uncertainty rule, and improvement threshold are frozen and identified before any treatment or control output. Covers parent AC5.
- [x] AC3: Case coverage maps all required core and professional-lens risks to stable cases with decision-property expectations. Covers parent AC3 and AC4.
- [ ] AC4: A matched clean-context run covers at least sixteen cases with two independent draws per condition, proves evaluation-surface isolation and matched non-treatment context/tools, and retains raw outputs, condition-masked mappings, quality-scorer provenance/disagreements, separate leakage-audit results, scores, uncertainty, configuration, and errors. Covers parent AC5.
- [ ] AC5: On the exact frozen matrix and configuration, the skilled condition clears the frozen improvement and uncertainty thresholds with zero hard-gate failures, or the release gate remains explicitly failed. Covers parent AC3, AC4, and AC5.
- [ ] AC6: Valid clean-checkout CI passes and all required malformed/private/drift fixtures fail with expected diagnostics. Covers parent AC7.

## Validation

- AC1: Parse and validate all evaluation JSON; run the valid and invalid repository fixtures.
- AC2: After importing all cases, hash the pre-result inventory, runtime-package manifest, protocol, rubric, scorer contract, uncertainty rule, and thresholds and record the identity in run metadata; prove the package excludes evaluation material.
- AC3: Generate and inspect the stable risk-to-case coverage report.
- AC4: Reproduce the matched matrix from documented commands or prompts and verify the sixteen-case/two-draw minimum, treatment-package isolation, matched tools/context, two quality-scoring passes with swapped labels, separate leakage audit, adjudication, uncertainty, and retained artifacts.
- AC5: Re-score condition-masked artifacts and independently recalculate the threshold, uncertainty, and hard-gate verdicts while preserving the separation between quality scores and disclosed leakage limitations.
- AC6: Run the deterministic suite locally and in a clean GitHub Actions checkout; compare expected diagnostics for negative fixtures.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Assemble machine-readable cases | Import TASK-002 core and TASK-003 normative lens specifications, add stable synthetic output cases and positive/negative trigger queries, and prove complete core/lens risk coverage. | AC1, AC3: JSON validates, at least sixteen distinct cases exist, and the coverage report has no missing required risks. | Run the JSON validator and coverage command before any output generation. | Done: 31 cases and 28 trigger queries |
| 2 | Freeze and isolate evaluation authority | Freeze the complete inventory, rubric, gates, thresholds, uncertainty, controls, scorer/adjudication contract, and allowlisted runtime package after import but before outputs. | AC2: Frozen artifacts have a recorded identity, runtime package excludes evaluation material, and no result artifact predates them. | Inspect Git history/manifests and run the evaluation preflight/leakage validator. | Option A authority and deterministic freeze verifier implemented; authority commit and freeze pending |
| 3 | Build deterministic repository validation | Implement transparent checks for skill structure, references, links, evaluation metadata, supported-domain claims, private-data sentinels, and canonical-logic duplication with positive and negative fixtures. | AC1, AC6: Valid repository passes; each required invalid fixture fails with its expected diagnostic. | Run the full deterministic validation suite locally. | Done locally; clean CI pending |
| 4 | Run matched condition-masked comparison | Generate two independent draws per condition for at least sixteen cases under the frozen configuration, randomise/remove labels, run two fresh quality-scoring passes with swapped labels plus a separate structure-only leakage audit and adjudication, and retain complete artifacts. | AC4: Runtime/context/tool manifests, raw outputs, mapping, quality scores, leakage results, disagreements, uncertainty, model settings, timestamps, and errors are reproducible and complete. | Re-run or audit the recorded comparison procedure from fresh contexts. | Deterministic 31-case plan and fail-closed artifact verifier implemented; external model run To Do |
| 5 | Apply frozen release gates | Recalculate matched dimensions, uncertainty, and hard gates without changing thresholds, then record pass or failure without post-hoc reinterpretation. | AC5: The scoped threshold calculation is reproducible and every hard gate is explicitly reported. | Run the score aggregation/check command against retained condition-masked scores. | To Do |
| 6 | Prove clean CI behavior | Configure credential-free validation in a clean checkout and retain the live workflow identity after push. | AC6: GitHub Actions passes the valid repository while local negative fixtures remain proven failures. | Inspect the exact GitHub Actions run and rerun local negative fixtures. | To Do |

## Parent AC Evidence

- AC3 and AC4 definitions: the 31-case generated inventory and required probe coverage pass deterministic validation. AC3, AC4, and AC5 behavioural proof remains pending the frozen matched run. AC7 passes locally but remains pending clean CI. No visual proof recipe applies; behavioural evidence must use the frozen evaluation artifacts described above.

## QA & Code Review

- Verdict: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-004
- Title: Build Adversarial and Comparative Evaluations
- Created: 2026-07-22
- Clarification resolved: owner approved Option A on 2026-07-22. Quality scoring is separated from a structure-only leakage audit; no treatment, control, scorer, adjudicator, assertion-grader, trigger, or leakage-audit output preceded approval.
