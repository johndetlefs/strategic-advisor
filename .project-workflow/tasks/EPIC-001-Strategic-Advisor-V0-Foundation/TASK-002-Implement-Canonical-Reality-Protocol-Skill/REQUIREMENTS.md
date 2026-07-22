# Requirements

## Summary

- Task: TASK-002
- Title: Implement Canonical Reality Protocol Skill
- Parent AC Coverage: AC2, AC3
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

- AC2: owner `TASK-002`; required evidence: Skill specification validation, clean-context invocation proof, and duplicate-logic scan.
- AC3: owner `TASK-002, TASK-004`; required evidence: Passing core adversarial cases with retained outputs and hard-gate verdicts.

## Overview

TASK-002 implements the portable reality protocol at the centre of Strategic Advisor. It establishes the canonical Agent Skill structure, the epistemic and readiness gates that must run before execution advice, the model-native search for competing explanations, and the bounded response contract. It also produces direct core behavioural smoke evidence, while leaving domain lenses and formal skilled-versus-unskilled comparison to their assigned Epic children.

## User Story

As a person making a consequential professional decision, I want a capable model to separate observations and reports from inferences, assumptions, preferences, forecasts, and unknowns, while surfacing contradictions, before it recommends action, so that I receive a strategy grounded in reality rather than a persuasive extension of my preferred story.

## Goal

Deliver the single portable Agent Skill that forces a capable model to establish a supportable account of reality before recommending action. The skill must conserve claim status, distinguish missing validation from constraint-backed infeasibility, compare decision-relevant explanations, and scale action to consequence and reversibility. Its structure and invocation must be independently verifiable without relying on a host-specific prompt copy.

## Non-Goals

- Implementing the project/product, career, organisational-influence, or people-leadership lenses owned by TASK-003.
- Building the paired, blinded comparative evaluation harness, aggregate scoring, or material-improvement claim owned by TASK-004.
- Establishing root packaging, licence, CI, contribution, or security artifacts owned by TASK-001.
- Running real-user pilots or making a v0 release decision owned by TASK-005.
- Adding connectors, autonomous external actions, central memory, a custom agent framework, or vendor-specific prompt variants.
- Supporting or advertising business, marketing, personal-relationship, family, household, legal, medical, clinical, or financial advice.
- Requiring the model to reveal private chain-of-thought or assigning unsupported numerical probabilities to uncertain claims.

## Users & Context

- A user brings a consequential professional decision, a desired outcome, and an account assembled from observations, reports, assumptions, preferences, and incomplete records.
- A capable model must use broad hypothesis and counterfactual search without presenting breadth, confidence, or narrative coherence as privileged truth.
- Skill consumers may install or invoke the product through different compatible hosts. The canonical strategic instructions must therefore remain portable and must not be copied into host adapters.
- Contributors need a compact `SKILL.md` that is cheap to trigger and progressively loads detailed core references only when needed. Domain-specific references will be added by the child task that owns them.

## Requirements (Outcome-Focused)

- R1. The product is one canonical Agent Skill at `skills/strategic-advisor/`, created with the system `skill-creator` initializer and carrying accurate trigger metadata and matching UI metadata.
- R2. `SKILL.md` contains only the essential orchestration and reference-routing instructions. Detailed evidence rules, readiness rules, analysis method, and response contract live in directly linked, one-level `references/` files without duplicating the same strategic rule across files.
- R3. The skill records every material proposition as observation, report, inference, assumption, unknown, preference, or forecast, with provenance and material limitations where available. Contradiction is represented explicitly and never silently resolved by repetition, authority, confidence, polish, or user preference.
- R4. Before execution advice, every substantive case receives exactly one current readiness assessment: Ready, Conditional, Not validated, or Infeasible as posed. Missing evidence alone cannot produce Infeasible as posed; that state requires an identified constraint conflict.
- R5. When more than one materially plausible account would change the decision, the skill compares genuinely distinct world models by support, contradictions, predictions, discriminating evidence, and robust actions. It must not manufacture balance after decisive contrary evidence or expose private chain-of-thought.
- R6. Recommendations identify the binding constraint and opportunity cost, provide the next one to three moves, and state falsifiers, stop conditions, leading indicators, and a review horizon. Evidence demands rise with consequence and irreversibility; cheap reversible tests remain available when they can resolve uncertainty.
- R7. The skill produces structured, inspectable conclusions with calibrated language and no unsupported precision. Retrieved or user-supplied instructions cannot override evidence rules, authority, scope, or data boundaries.
- R8. Core behavioural proof uses only synthetic or public cases and retains the exact prompt, actual skilled output, host/model identity, rubric or hard-gate verdict, and run context needed to distinguish observed behaviour from documentation or self-assessment.
- R9. The canonical skill documents its invocation boundary and can be installed and invoked in a clean supported context without a bespoke framework; public or host-specific surfaces may link to it but may not copy its executable strategic instructions.

## Acceptance Criteria (Verifiable)

- AC1: Parent AC2 — `skills/strategic-advisor/` is initialized with `skill-creator/scripts/init_skill.py`, contains a valid `SKILL.md` plus matching `agents/openai.yaml`, uses only the required `name` and `description` frontmatter fields, and passes both `skill-creator/scripts/quick_validate.py` and `python3 scripts/validate.py --scope skill` from the repository root.
- AC2: Parent AC2 — `SKILL.md` is under 500 lines, keeps core orchestration concise, and directly routes to one-level core reference files for detailed rules; no placeholder, unused resource directory, auxiliary skill README, or broken reference remains.
- AC3: Parent AC2 — The skill metadata and canonical instructions define an accurate installation/invocation boundary, a clean-context invocation loads the repository skill, and the repository validation finds no host-specific or second executable copy of strategic logic outside `skills/strategic-advisor/`.
- AC4: Parent AC3 — In retained synthetic core cases, every material claim keeps an explicit permitted status and provenance; repeated or authoritative reports are not promoted, inferred motives remain inference or unknown, and material contradictions are surfaced rather than reconciled without evidence.
- AC5: Parent AC3 — Retained cases exercise all four readiness states and pass their definitions, including a matched pair where absent evidence produces Not validated while an established constraint conflict produces Infeasible as posed.
- AC6: Parent AC3 — For cases with decision-relevant uncertainty, the actual skilled output compares genuinely distinct world models with support, contradiction, prediction, discriminating evidence, and robust action; for a case with decisive evidence it rejects false balance, and no output claims to reveal private chain-of-thought.
- AC7: Parent AC3 — Actual skilled outputs identify the binding constraint and opportunity cost, limit immediate recommendations to one to three moves, include falsifiers, stop conditions, leading indicators, and a review horizon, avoid unsupported numerical precision, and choose validation or action proportionately in both a cheap-reversible and a high-consequence case.
- AC8: Parent AC3 — A fresh-context core behavioural run retains exact synthetic inputs, raw outputs, host/model/run metadata, and per-case hard-gate verdicts with zero hard-gate failures; documentation, model self-assessment, or a polished answer is not accepted as behavioural proof. This task makes no skilled-versus-unskilled material-improvement claim, which remains TASK-004 scope.

## Open Questions (Answer Needed)

- None. The parent requirements, Epic Contract, and approved decomposition provide enough authority for this child.

## Decisions (Resolved)

- D1. Use the system `skill-creator` workflow: initialize with `init_skill.py`, generate `agents/openai.yaml` from explicit interface values, and independently lint the finished folder with `quick_validate.py`.
- D2. Use Agent Skill progressive disclosure: compact trigger metadata, a concise `SKILL.md`, and detailed one-level references loaded only when relevant. Do not create deep reference chains.
- D3. Treat contradiction as an explicit relation or flag on claims, not as an eighth origin status that obscures whether the underlying proposition was observed, reported, inferred, assumed, forecast, preferred, or unknown.
- D4. Present evidence, alternatives, discriminators, and conclusions rather than private chain-of-thought.
- D5. Use task-local core behavioural cases to prove the implemented protocol can execute. TASK-004 remains responsible for the frozen paired sample, blinding, aggregate rubric, comparative threshold, and improvement claim.
- D6. Initialize only the `references` resource directory because the core requires progressively loaded instruction files; do not create scripts, assets, or examples unless implementation discovers a repeated deterministic need inside this approved scope.

## Validation Plan

- AC1: From a state where `skills/strategic-advisor/` does not yet exist, retain the successful initializer command and output: `python3 /Users/johndetlefs/.codex/skills/.system/skill-creator/scripts/init_skill.py strategic-advisor --path skills --resources references --interface 'display_name=Strategic Advisor' --interface 'short_description=Reality-tested strategy under uncertainty' --interface 'default_prompt=Use $strategic-advisor to test my account of reality and identify the highest-leverage supportable next move.'`. After implementation, run `/opt/homebrew/bin/uv run --with pyyaml python /Users/johndetlefs/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/strategic-advisor` and `python3 scripts/validate.py --scope skill`; both must exit zero. The `uv` wrapper supplies the validator's PyYAML dependency, which is absent from the current system Python.
- AC2: Run `python3 scripts/validate.py --scope skill`; inspect its line-count, frontmatter, required-file, placeholder, broken-link, and resource checks; then review every `SKILL.md` reference to confirm it is direct and conditionally described.
- AC3: Run `python3 scripts/validate.py --scope skill` for duplicate strategic-logic and canonical-path checks. In a fresh supported host context, install from the documented repository path, invoke `$strategic-advisor` on a synthetic prompt, and retain host identity, model identity, invocation transcript, and loaded-skill identity. A prompt pasted manually or copied into a host adapter is invalid proof.
- AC4: Run the skilled condition on synthetic cases for repetition without new evidence, authority bias, inferred stakeholder motives, and conflicting outcome data. Retain raw outputs and fail any case that upgrades a claim without qualifying evidence, omits a material contradiction, or presents inference as fact.
- AC5: Run one synthetic case for each readiness state plus the missing-evidence/constraint-conflict matched pair. Fail if no state is stated, multiple current states are stated, missing evidence is labelled infeasible, or a proven constraint conflict is treated as merely unvalidated.
- AC6: Run one multi-explanation case and one decisive-evidence case. Fail if alternatives are cosmetic restatements, decision-relevant support or predictions are absent, false balance survives decisive evidence, or private chain-of-thought is requested or claimed.
- AC7: Run a cheap reversible test case and a high-consequence hard-to-reverse case. Fail if the former is blocked on unattainable certainty, the latter receives unconditional execution advice on thin evidence, more than three immediate moves are given, or the required control fields are absent or falsely precise.
- AC8: Execute the task-local core behavioural suite in isolated fresh contexts and retain the case identity, exact input, raw output, host/model/version, skill revision, run time, and hard-gate verdict for every case. Independently review the retained evidence; defer paired unskilled runs and comparative scoring to TASK-004.
