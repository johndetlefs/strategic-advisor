# Requirements

## Summary

- Task: TASK-003
- Title: Implement v0 Professional Domain Lenses
- Parent AC Coverage: AC4
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

- AC4: owner `TASK-003, TASK-004`; required evidence: Four substantive lens contracts plus passing lens and boundary cases.

## Overview

TASK-003 specialises the canonical reality protocol for the four professional domains authorised in v0. It defines what each lens must notice, how it reasons about causal mechanisms and autonomous stakeholders, where its scope ends, and which pre-result cases must later prove the behaviour. It does not itself satisfy parent AC4's behavioural half; TASK-004 must execute the frozen cases and retain passing hard-gate evidence.

## User Story

As a person making a consequential project, career, organisational, or people-leadership decision, I want the advisor to apply the right professional domain model while preserving evidence status and stakeholder agency, so that I receive useful strategic guidance without fantasy, mind-reading, ideal-actor assumptions, or personal-relationship moralisation of legitimate professional influence.

## Goal

Give the canonical Strategic Advisor enough domain-specific structure to reason usefully about project/product, career, organisational-influence, and people-leadership decisions without weakening the shared reality protocol, treating stakeholder motives or cooperation as facts, or importing the distinct personal-relationship boundary into legitimate professional influence.

## Non-Goals

- Reimplementing or forking the canonical reality protocol for each domain.
- Supporting business, venture, marketing, growth, personal relationship, family, household, or general life advice in v0.
- Treating a lens document, example, or model self-description as behavioural proof; TASK-004 owns execution and retained verdicts for the parent AC4 cases.
- Diagnosing stakeholders, claiming to read motives, or modelling people as deterministic components that can be optimised into compliance.
- Prohibiting ordinary professional influence, private strategy, negotiation, accountability, performance management, or coalition building merely because those actions intentionally affect other people.
- Normalising material deception, coercion, exploitation, or hidden monitoring by relabelling them as influence; the advisor must identify their dependencies, likely consequences, and effect on the recommendation.
- Building connectors, host-specific prompt copies, autonomous actions, or case memory.

## Users & Context

- Project and product leaders deciding what outcome to pursue, what work to stop, and how to act under user, delivery, resource, dependency, and stakeholder uncertainty.
- People navigating role choice, advancement, performance signals, sponsorship, management relationships, internal politics, and external career alternatives.
- People seeking to influence professional decisions through framing, sequencing, negotiation, coalition building, incentive alignment, accountability, and private preparation.
- People leaders deciding how to improve team outcomes while preserving each person's agency and distinguishing evidence about performance from assumptions about character or motive.
- Cases may contain conflicting reports, incomplete metrics, desired narratives, and adaptive stakeholders with vetoes, alternatives, and the ability to resist, renegotiate, or leave.

## Requirements (Outcome-Focused)

- R1. All four lenses use one shared domain-contract shape: supported decisions and outcomes, decision-relevant evidence, causal mechanisms, stakeholder agency, characteristic failure modes, out-of-scope boundaries, and domain-specific application of the readiness states.
- R2. Lens guidance remains progressively loaded content inside the one canonical `skills/strategic-advisor/` skill; it may specialise the core protocol but must not copy, replace, or contradict its claim-status, readiness, competing-world, consequence, reversibility, or response rules.
- R3. The project/product lens distinguishes intended outcomes from output and activity, examines user/value and causal assumptions, exposes binding constraints and dependencies, accounts for sunk-cost and cherished-work bias, and supports bounded experiments, sequencing, stopping, pivoting, or continuation decisions.
- R4. The career lens distinguishes preferences from evidence about advancement or fit, examines actual performance and decision signals, formal and informal criteria, sponsorship and power, timing and opportunity cost, and internal versus external alternatives without treating a manager's or colleague's motive as known.
- R5. The organisational-influence lens treats legitimate deliberate influence as part of professional reality. It models decision rights, power, incentives, coalitions, vetoes, alternatives, framing, sequencing, negotiation, accountability, private strategy, and likely adaptation. It identifies material deception, coercion, exploitation, and hidden monitoring with their factual dependencies and consequences rather than moralising ordinary influence away or euphemising consequential conduct.
- R6. The people-leadership lens focuses on observable outcomes, role and expectation clarity, capability, environment, incentives, feedback, support, accountability, and alternatives. It treats staff as autonomous actors, compares rival explanations for performance, avoids diagnosis and character claims, and exposes recommendations that assume perfect compliance or control.
- R7. Routing selects exactly one primary lens for a supported v0 case and at most one secondary lens only when the second changes material evidence, causal analysis, risks, or action. A wholly unsupported case activates zero professional lenses and is named as outside v0; a separable supported professional sub-decision may be bounded and routed independently.
- R8. The same professional interaction is not governed by the personal-relationship boundary merely because it involves persuasion, incentives, private preparation, or asymmetrical power. Conversely, changing otherwise similar facts from a professional setting to an intimate or family setting must change the routing and supported advice rather than treating the other person as an organisational component.
- R9. Statements about a stakeholder's motive, intent, loyalty, competence, future cooperation, or reaction preserve their actual epistemic status. Material inferences require rival explanations and discriminating evidence or an action robust across plausible motives.
- R10. Plans that depend on an ideal actor—such as a rational manager, compliant staff member, truthful peer, cooperative veto holder, or executive honouring informal support—must expose that dependency and either validate it, add a contingency, or lower readiness.
- R11. TASK-003 owns the normative lens-case specifications. They are synthetic, public, or irreversibly sanitised and specify expected routing, material claim statuses, required analytical behaviour, and forbidden failure modes. TASK-004 imports these specifications into the combined case inventory and freezes that complete inventory before generating any behavioural output.

## Acceptance Criteria (Verifiable)

- AC1: Four non-placeholder lens contracts exist under the canonical skill—project/product, career, organisational influence, and people leadership—and each explicitly defines supported decisions/outcomes, relevant evidence, causal mechanisms, stakeholder agency, characteristic failure modes, boundaries, and readiness implications. The deterministic lens validator fails if any contract or required section is absent.
- AC2: The project/product contract requires outcome-versus-activity separation, user/value and causal assumptions, binding constraints and dependencies, sunk-cost or cherished-work challenges, and a choice among validated continuation, bounded experiment, pivot, stop, or not-yet-validated action.
- AC3: The career contract requires an explicit objective and horizon, evidence about performance and decision criteria, sponsorship/power and timing, internal and external alternatives, and treatment of manager or colleague motives as reported or inferred rather than observed facts.
- AC4: The organisational-influence contract supports framing, sequencing, negotiation, coalition building, incentive alignment, accountability, and private strategy; models decision rights, power, vetoes, alternatives, and adaptive response; distinguishes those actions from material deception, coercion, exploitation, and hidden monitoring; and does not apply the personal-relationship control boundary to legitimate professional influence.
- AC5: The people-leadership contract requires observable outcome and performance evidence, role/system/capability/incentive hypotheses, support and accountability options, and stakeholder agency; it rejects diagnosis, unearned motive claims, deterministic optimisation of a person, and plans dependent on unquestioning compliance.
- AC6: For supported v0 cases, canonical routing rules select one primary and no more than one materially relevant secondary lens and prevent duplicated core logic. Wholly unsupported personal, intimate, family, household, business, marketing, and general-life requests activate zero professional lenses unless a supported professional sub-decision is separable and explicitly bounded.
- AC7: A committed synthetic normative lens-case specification contains at least two substantive cases per v0 lens plus, in addition, four cross-cutting probes: a same-facts professional-versus-personal framing pair, an asserted inferred-motive case, an adaptive stakeholder refusal or resistance case, and an ideal-actor dependency case. Every case declares expected lens routing, material claim statuses, required challenge or recommendation, and forbidden behaviours; the deterministic validator rejects missing coverage or private case data. TASK-004 owns the combined executable inventory and its later freeze identity.
- AC8: `python3 scripts/validate.py --scope lenses` passes and `git diff --check` reports no errors. TASK-003 records the implemented contracts and case-definition identity as pending inputs to TASK-004; parent AC4 remains unsatisfied until TASK-004 retains passing behavioural outputs and hard-gate verdicts for the lens and boundary cases.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- D1. Use four progressively loaded domain references within one canonical skill, not four independent advisors or vendor-specific prompt copies.
- D2. Use one common lens-contract shape so validation can detect missing domain obligations without forcing identical reasoning across domains.
- D3. Permit one primary lens and at most one secondary lens for supported v0 cases; activate zero lenses for a wholly unsupported case. Additional perspectives remain competing explanations inside the core analysis rather than extra activated lenses.
- D4. Treat deliberate professional influence as legitimate subject matter. Describe conduct and consequences precisely instead of applying a blanket manipulation label or silently approving consequential deception, coercion, exploitation, or hidden monitoring.
- D5. Personal and intimate relationships remain a separate, unsupported v0 domain. The boundary changes routing and advice; it is not a pretext to suppress professional stakeholder analysis.
- D6. TASK-003 defines the lens contracts and normative lens-case specifications. TASK-004 imports core and lens specifications, owns the combined executable case inventory and freezes it only after import, then owns the isolated runtime packages, behavioural runs, condition-masked scoring, retained outputs, and hard-gate verdicts required to finish parent AC4.
- D7. Use `python3 scripts/validate.py --scope lenses` as the exact deterministic structural and case-coverage check; `python3 scripts/validate.py` remains the repository-wide validation entrypoint.

## Validation Plan

- AC1: Run `python3 scripts/validate.py --scope lenses` and inspect its per-contract required-section report for exactly the four v0 lenses.
- AC2: Run the lens validator against project/product positive and negative fixtures covering outcome/activity substitution, untested value assumptions, dependency exposure, sunk cost, and continue/experiment/pivot/stop outcomes.
- AC3: Run the lens validator against career fixtures covering objective/horizon, promotion or role evidence, sponsorship/power, alternatives, and inferred manager motives.
- AC4: Run the lens validator against organisational-influence fixtures covering legitimate private preparation, coalition/framing/negotiation, veto and incentive maps, adaptive response, consequential-conduct classification, and the professional/personal boundary.
- AC5: Run the lens validator against people-leadership fixtures covering performance evidence, rival causal explanations, support/accountability, worker agency, diagnosis avoidance, and refusal or non-compliance contingencies.
- AC6: Inspect the canonical loading/routing rules and run trigger fixtures for supported primary-only, justified-secondary, unjustified-extra-lens, bounded professional sub-decision, personal relationship, and wholly unsupported-domain inputs; require zero lenses for the wholly unsupported case and scan for copied core rules outside their canonical source.
- AC7: Validate the manifest count, lens coverage, cross-cutting probe tags, expected/forbidden fields, synthetic-data declaration, and private-data negative fixture with `python3 scripts/validate.py --scope lenses`.
- AC8: Run `python3 scripts/validate.py --scope lenses` and `git diff --check`; record the current commit and manifest hash in TASK-003 evidence. TASK-004 must then execute the frozen lens cases and retain current outputs and hard-gate verdicts before parent AC4 can pass; contract presence, validator success, or model self-assessment are invalid substitutes.
