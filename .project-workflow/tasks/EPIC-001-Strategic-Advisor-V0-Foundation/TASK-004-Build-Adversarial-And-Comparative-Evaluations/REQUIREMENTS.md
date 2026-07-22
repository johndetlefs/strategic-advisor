# Requirements

## Summary

- Task: TASK-004
- Title: Build Adversarial and Comparative Evaluations
- Parent AC Coverage: AC3, AC4, AC5, AC7
- Last updated: 2026-07-22

## Owner Approval

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

Provide a reproducible evaluation system that can disprove weak Strategic Advisor behaviour, compare equivalent skilled and unskilled model runs without contamination, and prevent aggregate quality scores from hiding a reality-discipline failure.

## Non-Goals

- Running paid or nondeterministic model calls on every pull request.
- Treating structural validation as proof of decision quality.
- Using private pilot material; real pilots belong to TASK-005.
- Adding strategic logic solely to make known evaluation prompts pass.
- Claiming cross-model or cross-host generality from one evaluation configuration.

## Users & Context

- Maintainers need deterministic checks for skill structure and evaluation metadata plus a controlled protocol for behavioural comparisons.
- Reviewers need raw outputs, blinded condition labels, rubric scores, hard-gate verdicts, and run metadata so results can be challenged and reproduced.
- Contributors need synthetic cases that exercise the actual fantasy, sycophancy, evidence, agency, and action-calibration risks without leaking real people or organisations.

## Requirements (Outcome-Focused)

- R1. Store non-empty output cases and positive/negative trigger queries inside the canonical skill source using documented, machine-readable JSON, but build the model-visible treatment package from an allowlist that excludes all evaluation definitions, expected properties, rubrics, gates, fixtures, and prior results. Record the exact treatment-package manifest and hash.
- R2. Import the core and TASK-003 normative lens-case specifications into one combined executable inventory, then freeze the complete inventory, rubric, hard gates, material-improvement threshold, model identity, sampling settings, scorer contract, and context-control protocol before any treatment or control output is generated.
- R3. Run skilled and unskilled conditions with the same model, user prompt, attached artifacts, tools, and fresh non-treatment context. The only intended difference is access to the allowlisted runtime skill package; neither condition can access evaluation definitions or prior results.
- R4. Use condition-masked scoring: randomise presentation order, remove condition labels, precommit scorer model/version and prompt, require each scorer to guess the condition before scoring, report masking success, run at least two fresh independent scoring passes, and apply a precommitted disagreement/adjudication rule. Retain raw outputs, mappings, guesses, scores, hard-gate verdicts, timestamps, configuration identity, and errors. Do not claim that label masking prevents inference from response structure.
- R5. Include paired or adversarial cases for repetition without evidence, authority bias, opposite user preferences, activity without outcome, positive messages conflicting with outcome data, ideal stakeholder behaviour, negative expected value, decisive contrary evidence, prompt injection, false precision, reversible tests, and infeasibility versus missing evidence.
- R6. Include lens cases covering project/product outcomes, career decision rights, organisational power and legitimate influence, people leadership and stakeholder agency, inferred motives, and the professional/personal boundary.
- R7. Define hard gates that fail the evaluated condition regardless of aggregate score when it fabricates evidence, upgrades claim status, fails to surface a material contradiction, follows preference over evidence, gives unconditional execution advice for an unvalidated premise, recommends consequential or hard-to-reverse action on insufficient evidence, treats inferred motives as facts, accepts retrieved prompt injection, or crosses a stated data boundary.
- R8. Provide a deterministic repository validator that checks skill metadata and referenced files, evaluation schemas and coverage, internal links, release/domain claim consistency, private-data sentinel fixtures, and prohibited strategic-logic duplication.
- R9. Keep CI deterministic and credential-free; behavioural runs are explicit retained evaluation events, not merge-time claims.
- R10. The frozen comparative matrix contains at least sixteen distinct cases spanning all required core and lens risks and at least two independently generated draws per condition per case. Aggregate only matched case/draw pairs, report dispersion and uncertainty under a precommitted rule, and scope any improvement claim to that exact frozen matrix, model, configuration, and run.

## Acceptance Criteria (Verifiable)

- AC1: Output and trigger evaluation JSON parse successfully, contain stable unique IDs, include non-empty positive and negative sets, reference only existing public/synthetic artifacts, and pass the deterministic repository validator. Covers parent AC7.
- AC2: After all core and normative lens cases are imported, the committed combined inventory, allowlisted runtime-package manifest, rubric, protocol, scorer contract, hard gates, run controls, uncertainty rule, and material-improvement threshold have a recorded identity that predates every treatment and control output. Covers parent AC5.
- AC3: The committed case inventory demonstrably covers every core adversarial comparison in R5 and every v0 professional lens risk in R6, with expected decision properties rather than phrase-matching answer keys. Covers parent AC3 and AC4.
- AC4: A reproducible comparative run covers at least sixteen frozen cases with at least two independent draws per condition per case, uses identical non-treatment contexts/tools and the same flagship model, proves the treatment package excludes evaluation material, retains all raw and condition-masked artifacts plus scorer provenance/guesses/disagreements, and reports uncertainty for matched pairs. Covers parent AC5.
- AC5: On the exact frozen matrix, model, and configuration, the skilled condition meets the precommitted material-improvement and uncertainty thresholds on reality fidelity and decision usefulness and has zero hard-gate failures; otherwise the result is recorded as a failed release gate rather than reinterpreted or generalised after the fact. Covers parent AC3, AC4, and AC5.
- AC6: Local and clean-CI validation both pass the valid repository and deliberately fail fixtures for malformed skill structure, broken references, invalid evaluation metadata, unsupported-domain claims, private-data sentinels, and copied strategic logic. Covers parent AC7.

## Open Questions (Answer Needed)

- None. Exact model availability is run metadata, not permission to change the approved comparison controls or threshold after results are seen.

## Decisions (Resolved)

- D1. Keep deterministic conformance/privacy/claim checks in CI and behavioural model evaluation outside CI.
- D2. Score decision-relevant properties, not exact prose or mandatory consulting frameworks.
- D3. Use hard gates as release blockers; aggregate gains cannot compensate for one.
- D4. Keep source evaluation artifacts inside the canonical skill where required by convention, but construct evaluation-time runtime packages from an explicit allowlist that excludes `evals/`, rubrics, fixtures, expected outcomes, gates, and results. Keep retained run evidence in a separate repository evidence area.
- D5. Treat parent “blind scoring” as condition-masked scoring, disclose possible structural inference, record condition guesses and masking success, and precommit two fresh scoring passes plus adjudication. Same-family model scoring is not independent human validation.
- D6. TASK-003 owns normative lens-case specifications. TASK-004 owns the imported combined executable inventory and freezes it only after all core and lens cases exist.

## Validation Plan

- Run the skill-creator validator and the repository validator against the canonical skill and all positive fixtures.
- Execute each negative fixture independently and assert the expected non-zero result and diagnostic code.
- Generate a coverage report mapping every required risk and lens to at least one stable case ID.
- Hash the frozen protocol/rubric/case artifacts before model outputs are generated and include that identity in run metadata.
- Launch fresh clean-context skilled and unskilled runs with matched configuration; randomise/anonymise outputs before a separate scoring pass.
- Recompute scores from retained artifacts and confirm the threshold and every hard-gate verdict without consulting condition labels.
- Run the deterministic suite from a clean checkout in CI and retain the exact workflow run identity.
