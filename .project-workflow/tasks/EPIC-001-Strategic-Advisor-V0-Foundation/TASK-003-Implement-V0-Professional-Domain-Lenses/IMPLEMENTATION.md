## User Story

As a person making a consequential project, career, organisational, or people-leadership decision, I want the advisor to apply the right professional domain model while preserving evidence status and stakeholder agency, so that I receive useful strategic guidance without fantasy, mind-reading, ideal-actor assumptions, or personal-relationship moralisation of legitimate professional influence.

## Parent AC Coverage

- AC4

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

- AC4: owner `TASK-003, TASK-004`; required evidence: Four substantive lens contracts plus passing lens and boundary cases.

## Goal

Implement four substantive professional lens contracts and their pre-result case obligations inside the canonical skill, then provide deterministic evidence that the contracts, routing rules, boundary coverage, and synthetic case manifest are complete enough for TASK-004 to execute the behavioural proof required by parent AC4.

## Approach

- Add progressively loaded lens references under `skills/strategic-advisor/references/` for project/product, career, organisational influence, and people leadership. Each uses the common contract shape but contains domain-specific evidence, mechanisms, agency, failure modes, boundaries, and readiness implications.
- Integrate selection through the canonical `skills/strategic-advisor/SKILL.md`: exactly one primary lens for supported v0 cases, with at most one secondary lens when it materially changes evidence, causal analysis, risk, or action; wholly unsupported cases activate zero lenses. Reuse the reality protocol from TASK-002 instead of copying it into lenses.
- Encode the required synthetic normative lens and cross-cutting case specifications before behavioural results are generated. Cases declare routing, claim-status, required-behaviour, and forbidden-behaviour expectations; TASK-004 imports them into the combined executable inventory, freezes that complete inventory, and owns actual runs and verdicts.
- Extend the transparent repository validator established by TASK-001 so `python3 scripts/validate.py --scope lenses` checks contract shape, supported-scope claims, routing limits, case coverage, required tags/expectations, and synthetic-data declarations.
- Treat TASK-002's canonical core/loading contract and TASK-001's validation entrypoint as integration dependencies. Their absence is a dependency to resolve, not permission to create a second core or alternate validator.

## Phases

### Phase 1 — Contract and routing boundary

- Confirm the canonical core and progressive-loading seam from TASK-002.
- Define the shared lens-contract shape and exact four-lens routing/scope rules without duplicating core strategic logic.
- Validation: inspect each proposed field against AC1 and AC6; run `python3 scripts/validate.py --scope lenses` once validator support exists and confirm missing-lens and extra-lens negative fixtures fail.

### Phase 2 — Four domain lenses

- Implement the project/product and career contracts, including their distinct evidence, mechanisms, failure modes, agency, and decision options.
- Implement the organisational-influence and people-leadership contracts, preserving legitimate professional influence while exposing consequential conduct, motive uncertainty, resistance, and non-compliance dependencies.
- Validation: run `python3 scripts/validate.py --scope lenses`; review each contract against its corresponding AC2–AC5 matrix and confirm core claim/readiness rules are referenced rather than copied.

### Phase 3 — Adversarial case handoff and canonical integration

- Add at least two substantive synthetic normative specifications per lens and the additional professional/personal pair, inferred-motive, adaptive-resistance, and ideal-actor probes.
- Wire canonical routing to the four references and prevent unsupported personal/life or later commercial domains from being advertised as supported.
- Validation: run `python3 scripts/validate.py --scope lenses`, inspect the normative specification for all required expected and forbidden behaviours, and hand its identity to TASK-004 for import before the combined executable inventory is frozen or any treatment result is generated.

### Phase 4 — Validation, QA, and parent evidence handoff

- Run the deterministic lens check and repository diff hygiene check from the task boundary.
- Conduct QA/code review for scope leakage, copied core logic, professional/personal conflation, unearned motive claims, ideal-actor dependencies, and private example material.
- Record the contract and case-manifest evidence for TASK-003 and explicitly leave behavioural parent proof pending TASK-004.
- Validation: `python3 scripts/validate.py --scope lenses` and `git diff --check`; QA review must report no unresolved hard-gate or scope findings before TASK-003 completion.

## Acceptance Criteria

- [x] AC1: Four non-placeholder lens contracts exist under the canonical skill—project/product, career, organisational influence, and people leadership—and each explicitly defines supported decisions/outcomes, relevant evidence, causal mechanisms, stakeholder agency, characteristic failure modes, boundaries, and readiness implications. The deterministic lens validator fails if any contract or required section is absent.
- [x] AC2: The project/product contract requires outcome-versus-activity separation, user/value and causal assumptions, binding constraints and dependencies, sunk-cost or cherished-work challenges, and a choice among validated continuation, bounded experiment, pivot, stop, or not-yet-validated action.
- [x] AC3: The career contract requires an explicit objective and horizon, evidence about performance and decision criteria, sponsorship/power and timing, internal and external alternatives, and treatment of manager or colleague motives as reported or inferred rather than observed facts.
- [x] AC4: The organisational-influence contract supports framing, sequencing, negotiation, coalition building, incentive alignment, accountability, and private strategy; models decision rights, power, vetoes, alternatives, and adaptive response; distinguishes those actions from material deception, coercion, exploitation, and hidden monitoring; and does not apply the personal-relationship control boundary to legitimate professional influence.
- [x] AC5: The people-leadership contract requires observable outcome and performance evidence, role/system/capability/incentive hypotheses, support and accountability options, and stakeholder agency; it rejects diagnosis, unearned motive claims, deterministic optimisation of a person, and plans dependent on unquestioning compliance.
- [x] AC6: For supported v0 cases, canonical routing rules select one primary and no more than one materially relevant secondary lens and prevent duplicated core logic. Wholly unsupported personal, intimate, family, household, business, marketing, and general-life requests activate zero professional lenses unless a supported professional sub-decision is separable and explicitly bounded.
- [x] AC7: A committed synthetic normative lens-case specification contains at least two substantive cases per v0 lens plus the four additional cross-cutting probes, with expected routing, material claim statuses, required challenge or recommendation, and forbidden behaviours. TASK-004 owns the combined executable inventory and later freeze identity.
- [ ] AC8: `python3 scripts/validate.py --scope lenses` passes and `git diff --check` reports no errors. TASK-003 records the implemented contracts and case-definition identity as pending inputs to TASK-004; parent AC4 remains unsatisfied until TASK-004 retains passing behavioural outputs and hard-gate verdicts for the lens and boundary cases.

## Validation

- AC1: `python3 scripts/validate.py --scope lenses` reports exactly four complete lens contracts and fails the missing-contract/required-section negative fixtures.
- AC2: The same command passes project/product positive fixtures and fails fixtures missing outcome/activity distinction, value assumptions, dependency treatment, sunk-cost challenge, or a supported decision state.
- AC3: The same command passes career positive fixtures and fails fixtures missing objective/horizon, decision evidence, sponsorship/power, alternatives, or motive-status treatment.
- AC4: The same command passes organisational-influence positive fixtures and fails fixtures that moralise legitimate influence away, omit power/veto/adaptation, conflate the personal boundary, or euphemise material deception, coercion, exploitation, or hidden monitoring.
- AC5: The same command passes people-leadership positive fixtures and fails fixtures that omit causal rivals, support/accountability, agency, diagnosis avoidance, or non-compliance contingencies.
- AC6: The same command validates supported one-primary/optional-secondary routing, zero-lens handling for wholly unsupported cases, bounded professional sub-decisions, and no duplicated core logic; trigger fixtures cover each path.
- AC7: The same command validates minimum per-lens cases, all four additional probe obligations, expected/forbidden fields, claim-status expectations, and synthetic-data declarations; the private-data negative fixture must fail.
- AC8: Run `python3 scripts/validate.py --scope lenses` and `git diff --check`, then record the commit and case-manifest hash in task evidence. TASK-004 supplies the separate behavioural outputs and hard-gate verdicts needed for parent AC4.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Establish the shared contract and routing seam | Define the common lens obligations, exact v0 scope, one-primary/optional-secondary routing, and canonical-core reuse boundary. | AC1, AC6: all four contracts have a validated common shape and routing cannot activate unsupported or unnecessary lenses. | Run `python3 scripts/validate.py --scope lenses`; missing, extra, and duplicated-core fixtures must fail. | Done |
| 2 | Implement project/product guidance | Add evidence, mechanisms, agency, failure modes, and decision paths for outcome-led project and product strategy. | AC2: the lens distinguishes outcomes from activity and handles assumptions, constraints, dependencies, sunk cost, and continue/test/pivot/stop decisions. | Run `python3 scripts/validate.py --scope lenses` and inspect the project/product contract against AC2. | Done |
| 3 | Implement career guidance | Add evidence, mechanisms, agency, failure modes, and alternatives for role, advancement, performance, sponsorship, and career decisions. | AC3: the lens covers objective/horizon, decision evidence, power/sponsorship, timing, alternatives, and inferred-motive discipline. | Run `python3 scripts/validate.py --scope lenses` and inspect the career contract against AC3. | Done |
| 4 | Implement organisational-influence guidance | Model legitimate professional influence, decision rights, incentives, power, coalitions, vetoes, private strategy, adaptation, and consequential conduct precisely. | AC4: the lens supports legitimate influence, preserves the professional/personal distinction, and exposes deception, coercion, exploitation, or hidden monitoring without euphemism. | Run `python3 scripts/validate.py --scope lenses` and inspect the organisational-influence contract and boundary fixtures against AC4. | Done |
| 5 | Implement people-leadership guidance | Model observable performance, system and capability hypotheses, support, incentives, feedback, accountability, alternatives, and employee agency. | AC5: the lens rejects diagnosis, unearned motives, deterministic person optimisation, and ideal compliance assumptions. | Run `python3 scripts/validate.py --scope lenses` and inspect the people-leadership contract against AC5. | Done |
| 6 | Specify lens and boundary cases | Commit two substantive synthetic normative specifications per lens plus the additional professional/personal, inferred-motive, adaptive-resistance, and ideal-actor probes with explicit expected and forbidden behaviour. | AC7: the complete private-data-safe normative specification exists for TASK-004 import and is rejected when any required coverage or field is removed. | Run `python3 scripts/validate.py --scope lenses`; inspect the specification identity and all negative-fixture verdicts. | Done; commit identity pending |
| 7 | Integrate and hand off verifiable evidence | Wire progressive lens loading through the canonical skill, run deterministic validation and QA, and record exactly what TASK-003 proves versus what remains for TASK-004. | AC1, AC6, AC8: canonical integration and structural/case coverage pass with no false claim that parent AC4 behavioural proof is complete. | Run `python3 scripts/validate.py --scope lenses` and `git diff --check`; review task evidence and the explicit TASK-004 dependency. | In Progress: QA and commit evidence pending |

## Parent AC Evidence

- AC4: TASK-003 must provide the four substantive canonical lens contracts, routing/boundary rules, deterministic validator result, and frozen case-manifest identity. TASK-004 must separately provide passing current behavioural outputs and hard-gate verdicts for the lens and boundary cases. Parent AC4 remains pending until both evidence sets exist; contract presence or deterministic validation alone is not behavioural proof.

## QA & Code Review

- Verdict: Pending implementation and independent review.
- Evidence: Required inputs are the final diff, `python3 scripts/validate.py --scope lenses` output, `git diff --check` output, duplicate-logic and private-data negative-fixture verdicts, and task evidence identity.
- Findings: Review must explicitly cover scope leakage, core-rule duplication, professional/personal conflation, moralisation of legitimate influence, euphemised consequential conduct, motive promotion, stakeholder-agency loss, ideal-actor dependencies, unsupported-domain claims, and private example data.

## Retro

- Reusable lessons: Record after validation and behavioural-evaluation handoff.
- Conventions or agent assets updated: Update only when implementation reveals a durable repository rule not already captured by the constitution or guidance.
- Follow-up tasks: TASK-004 executes and scores the frozen lens cases; any later domain requires its own approved contract and evidence rather than extension by analogy.

## Notes

- Task: TASK-003
- Title: Implement v0 Professional Domain Lenses
- Created: 2026-07-22
- Dependencies: TASK-002 provides the canonical core/loading seam; TASK-001 provides `scripts/validate.py`; TASK-004 provides behavioural execution and retained verdicts.
- Scope authority: Parent EPIC-001 AC4 and its approved decomposition row; no personal-relationship or later commercial domain implementation is authorised here.
