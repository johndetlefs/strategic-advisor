## User Story

As a person making a consequential professional decision, I want a capable model to separate observations and reports from inferences, assumptions, preferences, forecasts, and unknowns, while surfacing contradictions, before it recommends action, so that I receive a strategy grounded in reality rather than a persuasive extension of my preferred story.

## Parent AC Coverage

- AC2, AC3

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

## Goal

Implement and directly validate the canonical, portable reality protocol that supplies TASK-002's contribution to parent AC2 and AC3, while leaving professional lenses and formal comparative evaluation to their assigned child tasks.

## Approach

1. Initialize `skills/strategic-advisor/` with the system `skill-creator` rather than hand-creating a skill-shaped directory. Generate only the required metadata and `references/` resource surface.
2. Keep `SKILL.md` concise and imperative. Put only orchestration, gates, output ordering, and conditional reference routing in it; put the detailed claim, readiness, world-model, action, and response contracts in directly linked one-level references.
3. Implement the core as explicit inspectable artifacts: a claim ledger, contradiction handling, one readiness verdict, competing-world comparison where material, and a bounded recommendation contract. Do not force domain-lens rules into the core.
4. Add deterministic repository validation for the canonical path and structure, then independently run the skill-creator structural validator.
5. Forward-test the actual installed skill in fresh contexts on synthetic core cases. Retain raw artifacts and hard-gate verdicts without leaking expected answers into the run prompt. Treat this as direct behavioural smoke proof, not the paired comparative evaluation owned by TASK-004.

## Acceptance Criteria

- [ ] AC1: Parent AC2 — `skills/strategic-advisor/` is initialized with `skill-creator/scripts/init_skill.py`, contains a valid `SKILL.md` plus matching `agents/openai.yaml`, uses only the required `name` and `description` frontmatter fields, and passes both `skill-creator/scripts/quick_validate.py` and `python3 scripts/validate.py --scope skill` from the repository root.
- [x] AC2: Parent AC2 — `SKILL.md` is under 500 lines, keeps core orchestration concise, and directly routes to one-level core reference files for detailed rules; no placeholder, unused resource directory, auxiliary skill README, or broken reference remains.
- [ ] AC3: Parent AC2 — The skill metadata and canonical instructions define an accurate installation/invocation boundary, a clean-context invocation loads the repository skill, and the repository validation finds no host-specific or second executable copy of strategic logic outside `skills/strategic-advisor/`.
- [ ] AC4: Parent AC3 — In retained synthetic core cases, every material claim keeps an explicit permitted status and provenance; repeated or authoritative reports are not promoted, inferred motives remain inference or unknown, and material contradictions are surfaced rather than reconciled without evidence.
- [ ] AC5: Parent AC3 — Retained cases exercise all four readiness states and pass their definitions, including a matched pair where absent evidence produces Not validated while an established constraint conflict produces Infeasible as posed.
- [ ] AC6: Parent AC3 — For cases with decision-relevant uncertainty, the actual skilled output compares genuinely distinct world models with support, contradiction, prediction, discriminating evidence, and robust action; for a case with decisive evidence it rejects false balance, and no output claims to reveal private chain-of-thought.
- [ ] AC7: Parent AC3 — Actual skilled outputs identify the binding constraint and opportunity cost, limit immediate recommendations to one to three moves, include falsifiers, stop conditions, leading indicators, and a review horizon, avoid unsupported numerical precision, and choose validation or action proportionately in both a cheap-reversible and a high-consequence case.
- [ ] AC8: Parent AC3 — A fresh-context core behavioural run retains exact synthetic inputs, raw outputs, host/model/run metadata, and per-case hard-gate verdicts with zero hard-gate failures; documentation, model self-assessment, or a polished answer is not accepted as behavioural proof. This task makes no skilled-versus-unskilled material-improvement claim, which remains TASK-004 scope.

## Phases

### Phase 1: Canonical skill structure

- Confirm the target skill path is absent or contains no unrelated work before initialization.
- Run the exact `skill-creator` initializer with explicit interface values and only the `references` resource.
- Replace every generated placeholder and verify `agents/openai.yaml` remains aligned with the final trigger contract.
- Phase validation: run the skill-creator `quick_validate.py` command and `python3 scripts/validate.py --scope skill`; inspect the generated diff for unrequested resources.

### Phase 2: Reality protocol and progressive disclosure

- Implement concise orchestration and conditional reference routing in `SKILL.md`.
- Implement one-level core references for claim/provenance discipline, contradiction and readiness rules, competing-world analysis, consequence/reversibility policy, and the response contract.
- Keep all executable strategic instructions canonical; external docs may describe or link to the skill but cannot reproduce its prompt logic.
- Phase validation: run `python3 scripts/validate.py --scope skill`, inspect reference reachability and line count, and manually trace each AC3-AC7 output obligation to one canonical instruction.

### Phase 3: Direct behavioural smoke proof

- Define synthetic core cases that isolate repetition, authority, contradiction, readiness, alternative-world, false-balance, false-precision, and reversibility/consequence failures.
- Invoke the actual installed skill in isolated fresh contexts without passing expected answers or prior diagnoses.
- Retain exact inputs, raw outputs, model/host/skill revision metadata, and hard-gate verdicts; keep the broader paired unskilled condition and blind comparative scoring out of this task.
- Phase validation: independently inspect every retained verdict, require zero hard-gate failures, and rerun `python3 scripts/validate.py --scope skill`.

### Phase 4: QA and handoff

- Run all structural and behavioural validation from a clean task state, including the task-specific `python3 scripts/validate.py --scope skill` check and the full deterministic `python3 scripts/validate.py` repository check.
- Run the required QA/code-review gate, resolve findings, and map current evidence to child AC1-AC8 and parent AC2/AC3 contributions.
- Phase validation: retain exact command outputs and evidence identities; do not claim parent AC3 complete until TASK-004's assigned proof also exists.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Initialize canonical Agent Skill | Use the system skill-creator initializer with explicit interface metadata and only the required `references` resource, then remove every generated placeholder. | AC1: The canonical folder, valid frontmatter, and matching UI metadata exist and pass both validators. | Run `python3 /Users/johndetlefs/.codex/skills/.system/skill-creator/scripts/init_skill.py strategic-advisor --path skills --resources references --interface 'display_name=Strategic Advisor' --interface 'short_description=Reality-tested strategy under uncertainty' --interface 'default_prompt=Use $strategic-advisor to test my account of reality and identify the highest-leverage supportable next move.'` once from an absent target path; then run `/opt/homebrew/bin/uv run --with pyyaml python /Users/johndetlefs/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/strategic-advisor` and `python3 scripts/validate.py --scope skill`. | Initialized; exact system quick validator currently unavailable |
| 2 | Establish progressive-disclosure boundary | Keep `SKILL.md` concise and route detailed core logic to direct, conditionally described one-level references without auxiliary or unused files. | AC2: The skill is under the line limit, every reference is direct and reachable, and no placeholder or unused resource remains. | Run `python3 scripts/validate.py --scope skill`; inspect `SKILL.md` reference links and confirm every bundled file is required by the workflow. | Done |
| 3 | Enforce one canonical invocation surface | Align trigger metadata, UI metadata, and clean-context invocation while preventing executable strategic prompt copies outside the product skill. | AC3: A clean-context invocation loads the repository skill and canonical-path validation finds no second or host-specific strategic-logic copy. | Run `python3 scripts/validate.py --scope skill`; install from the documented repository path in a fresh supported host context, invoke `$strategic-advisor` on a synthetic case, and retain the host/model/loaded-skill identity. | Canonical scan passes; host invocation pending |
| 4 | Implement claim and contradiction discipline | Define inspectable claim status, provenance, limitation, and contradiction handling that conserves epistemic status under repetition, authority, confidence, and preference. | AC4: Synthetic outputs preserve permitted statuses, keep motives inferred or unknown, and expose unresolved contradictions. | Run fresh-context skilled cases for repetition, authority, inferred motive, and conflicting outcomes; inspect retained raw outputs and hard-gate verdicts. | Source implemented; behavioural proof pending |
| 5 | Implement the four-state readiness gate | Require one current readiness state before execution advice and encode the evidence/constraint distinction between Not validated and Infeasible as posed. | AC5: All four states pass representative cases and the matched missing-evidence/constraint-conflict pair is classified correctly. | Run the four state cases and matched pair; fail on an omitted/ambiguous state, missing evidence labelled infeasible, or proven conflict labelled merely unvalidated. | Source implemented; behavioural proof pending |
| 6 | Implement competing-world search | Compare materially distinct explanations when they alter the decision, expose discriminators and robust actions, and reject false balance after decisive evidence without revealing private reasoning. | AC6: Multi-world and decisive-evidence outputs contain the required inspectable conclusions and no cosmetic alternatives or chain-of-thought claim. | Run one multi-explanation case and one decisive-evidence case in fresh contexts; inspect raw outputs against the AC6 hard gates. | Source implemented; behavioural proof pending |
| 7 | Implement bounded action contract | Tie recommendations to the binding constraint, opportunity cost, consequence, reversibility, falsifiers, controls, indicators, and review horizon. | AC7: Cheap-reversible and high-consequence cases receive proportionate responses with no more than three immediate moves and no unsupported precision. | Run the paired consequence/reversibility cases in fresh contexts and inspect each required response field and hard-gate verdict. | Source implemented; behavioural proof pending |
| 8 | Retain direct core behavioural evidence | Execute the actual skill on the synthetic core suite in isolated contexts and preserve raw run artifacts and independently checked hard-gate verdicts without making a comparative-improvement claim. | AC8: Complete run metadata and raw evidence exist for every core case with zero hard-gate failures; TASK-004 boundaries remain intact. | Review exact prompt/output/model/host/revision metadata and all verdicts; rerun `python3 scripts/validate.py --scope skill`. | To Do |
| 9 | Complete QA and parent evidence mapping | Run structural validation and QA/code review, resolve findings, and map only this task's direct proof to parent AC2 and its portion of AC3. | AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8: All child criteria have current evidence and no invalid substitute is used. | Run the skill-creator quick validator, `python3 scripts/validate.py --scope skill`, `python3 scripts/validate.py`, the task-local fresh-context core suite, and the project QA/review gate; inspect the final evidence map. | To Do |

## Validation

- AC1 / parent AC2: Retain the successful initializer output, then run `/opt/homebrew/bin/uv run --with pyyaml python /Users/johndetlefs/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/strategic-advisor` and `python3 scripts/validate.py --scope skill`; require zero exit status.
- AC2 / parent AC2: Use `python3 scripts/validate.py --scope skill` plus direct inspection of `SKILL.md` line count, one-level link reachability, placeholder absence, and resource necessity.
- AC3 / parent AC2: Use the canonical-scope/duplication validation and a fresh supported host invocation; retain loaded-skill, host, model, and revision identity. Manual prompt pasting is invalid proof.
- AC4 / parent AC3: Inspect fresh-context raw outputs and hard-gate verdicts for repetition, authority, inferred motive, and contradiction cases.
- AC5 / parent AC3: Inspect all readiness-state cases and the missing-evidence/constraint-conflict matched pair; require one correct current state per output.
- AC6 / parent AC3: Inspect multi-world and decisive-evidence raw outputs for distinctness, support, contradictions, predictions, discriminators, robust actions, false balance, and private-reasoning claims.
- AC7 / parent AC3: Inspect cheap-reversible and high-consequence outputs for proportionality, binding constraint, opportunity cost, one to three moves, falsifiers, stop conditions, indicators, horizon, and unsupported precision.
- AC8 / parent AC3: Independently audit retained exact inputs, raw outputs, host/model/run/skill metadata, and hard-gate verdicts; require zero hard-gate failures and make no comparative claim.

## Parent AC Evidence

- AC2: The open Agent Skills reference validator and repository canonical-scope/duplicate-logic checks pass. The exact system quick validator and clean-context host invocation remain pending; recipe-triggered claims must also be backed by `EVIDENCE.json`.
- AC3: Pending task-local core adversarial outputs and hard-gate verdicts. Parent completion also depends on TASK-004's assigned evidence; recipe-triggered claims must also be backed by `EVIDENCE.json`.

## QA & Code Review

- Verdict: Pending implementation validation and the required QA/code-review gate.
- Evidence: To be recorded from the implemented artifacts, exact validation commands, retained behavioural runs, and reviewer output.
- Findings: None yet; this section must be updated with resolved and unresolved findings before completion.

## Retro

- Reusable lessons: To be recorded after direct implementation and forward-testing evidence exists.
- Conventions or agent assets updated: None during planning; record only proven reusable changes after implementation.
- Follow-up tasks: None identified during planning; TASK-003 and TASK-004 already own the adjacent lens and comparative-evaluation work.

## Notes

- Task: TASK-002
- Title: Implement Canonical Reality Protocol Skill
- Created: 2026-07-22
