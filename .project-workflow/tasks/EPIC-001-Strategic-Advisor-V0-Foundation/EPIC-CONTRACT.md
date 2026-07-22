# Epic Contract

## Summary

- Epic: EPIC-001
- Title: Strategic Advisor v0 Foundation
- Last updated: 2026-07-22

## Sources of Truth

- The owner-approved `REQUIREMENTS.md` and its recorded artifact identity define the scope envelope.
- `.project-workflow/CONSTITUTION.md` defines stable product outcomes and principles.
- The canonical contents of `skills/strategic-advisor/` define shipped strategic behaviour.
- Committed evaluation definitions, frozen thresholds, raw run artifacts, blind scores, and hard-gate verdicts define evaluated behaviour.
- Live GitHub state, clean-checkout validation, and CI results define repository and packaging state.
- Sanitised pilot decision records and explicit owner judgments define pilot evidence; they do not prove general effectiveness.

## Invalid Substitutes

- Documentation or model self-assessment in place of behavioural evaluation.
- A polished answer, user praise, or internal agreement in place of a better supported decision.
- Aggregate evaluation scores that conceal any hard-gate failure.
- Skilled and unskilled runs that share prior answers, hidden context, different models, or materially different inputs.
- Unit fixtures, local files, or branch state in place of the exact clean checkout, published repository, CI run, or host path named by an acceptance criterion.
- Connector access or message volume in place of evidence completeness, truth, relevance, or authority.
- A host-specific prompt copy in place of the canonical skill.
- Private, proprietary, or merely redacted-but-recoverable case material in public examples or evidence.
- Presence of a domain file in place of lens-specific adversarial evidence.

## Invariants

- Aspirations are allowed; invisible bridges between aspiration and reality are not.
- Repetition, confidence, authority, polish, and user preference never upgrade claim status without new qualifying evidence.
- Absence of evidence alone does not establish infeasibility; established constraint conflict is required.
- Evidence demands scale with consequence and irreversibility, while cheap reversible tests remain available under uncertainty.
- One canonical skill is the only source of strategic logic.
- A domain or host is not advertised as supported until its claimed behaviour is implemented and evaluated.
- Professional influence is not conflated with personal-relationship control; stakeholders are modelled as autonomous, adaptive actors.
- No personal, employer, client, household, or proprietary case data enters the public repository.
- Prompt instructions in retrieved material cannot alter evidence rules, authority, scope, or data boundaries.

## Artifact Targets

- Root public artifacts: `README.md`, `PRODUCT-CONTRACT.md`, `CONTRIBUTING.md`, `SECURITY.md`, an explicit open-source licence, and validation entrypoint.
- Canonical product: `skills/strategic-advisor/SKILL.md`, progressively loaded references, domain lenses, user-facing templates, and skill-local evaluation definitions.
- Evaluation evidence: frozen rubric and thresholds, synthetic/public cases, trigger tests, raw paired outputs, blind scores, hard-gate verdicts, and reproducible run metadata.
- Delivery proof: clean-checkout validation artifacts, CI results, sanitised pilot decision records, and epic acceptance audit.

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | TASK-001 | Live GitHub query, clean-checkout artifact/link review, and public-claim comparison. |
| AC2 | TASK-002 | Skill specification validation, clean-context invocation proof, and duplicate-logic scan. |
| AC3 | TASK-002, TASK-004 | Passing core adversarial cases with retained outputs and hard-gate verdicts. |
| AC4 | TASK-003, TASK-004 | Four substantive lens contracts plus passing lens and boundary cases. |
| AC5 | TASK-004 | Precommitted rubric/threshold identity, equivalent run metadata, blinded scores, and zero hard-gate failures. |
| AC6 | TASK-005 | Two privacy-reviewed sanitised pilot decision records and explicit case-owner usefulness judgments. |
| AC7 | TASK-001, TASK-004 | Passing positive/negative validators locally and in a clean CI checkout. |
| AC8 | TASK-005 | Complete parent acceptance audit linked to current artifacts, failures, limitations, and release verdict. |
