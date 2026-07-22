## User Story

As a prospective user or contributor evaluating Strategic Advisor, I want the public repository to distinguish demonstrated capability from intent and to provide reproducible packaging checks, so that I can decide whether to use, inspect, or contribute to it without relying on promotional claims or the maintainer's local workspace.

## Parent AC Coverage

- AC1, AC7

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

- AC1: owner `TASK-001`; required evidence: Live GitHub query, clean-checkout artifact/link review, and public-claim comparison.
- AC7: owner `TASK-001, TASK-004`; required evidence: Passing positive/negative validators locally and in a clean CI checkout.

## Acceptance Criteria

- [ ] AC1: (Parent AC1) At the same commit, the required root public artifacts exist, contain the complete Apache License 2.0 text, have resolving internal links, and agree on current maturity, installation availability, canonical path, validated and unsupported domains, and connector status.
- [x] AC2: (Parent AC1, AC7) The public capability contract classifies advertised capability accurately, links evidence for validated capability, and the claims scope rejects an injected unsupported-domain claim with a stable diagnostic.
- [x] AC3: (Parent AC7) The aggregate validator and all declared scopes are deterministic, credential-free, network-free, emit stable check identifiers, pass the valid repository, and preserve the single canonical strategic-logic boundary.
- [x] AC4: (Parent AC7) The standard-library unit suite proves a valid baseline and all six required negative-fixture categories independently, using the committed TASK-002 and TASK-004 contracts for skill and evaluation semantics.
- [ ] AC5: (Parent AC7) Least-privilege CI and a clean checkout of the same published commit both pass the aggregate validator and complete unit suite.
- [ ] AC6: (Parent AC1) Live GitHub and unauthenticated Git evidence prove the exact repository is public with default branch `main`, and child evidence records the current artifact set, commit, commands, results, and invalid substitutes.

## Goal

Create the truthful public packaging and deterministic validation boundary needed to prove parent AC1 and the repository-orchestration portion of parent AC7 without duplicating the advisor or guessing downstream contracts.

## Approach

- Establish the public capability contract first, using the repository's actual state as the baseline. Until downstream implementation and evaluation evidence exist, label those capabilities as planned or implemented-but-not-validated rather than supported.
- Build one standard-library Python validator at `scripts/validate.py`. Its unscoped mode orchestrates all applicable checks; scoped modes isolate `skill`, `lenses`, `evals`, `pilots`, `privacy`, `claims`, and `links` while preserving stable diagnostic identifiers.
- Make claim state explicit enough for validation to compare public language with committed capability and evidence. Do not attempt unrestricted natural-language truth detection.
- Exercise failure behavior with isolated synthetic repository fixtures through standard-library `unittest`. The harness owns mutation isolation and expected diagnostics; TASK-002 and TASK-004 remain authoritative for skill and evaluation structure.
- Run deterministic checks in least-privilege CI. Gather network-dependent publication facts separately through live GitHub and unauthenticated clean-checkout proof, then record them in child evidence.

## Phases

### Phase 1 — Public contract and legal surface

1. Inspect the committed repository and live public state before writing capability claims.
2. Add `LICENSE` with the complete Apache License 2.0 text and create README, product contract, contribution guide, and security policy.
3. Define the capability-state vocabulary and evidence rule in `PRODUCT-CONTRACT.md`; align every root public claim to it.
4. Configure or verify the non-public GitHub vulnerability-reporting path referenced by `SECURITY.md`.

Validation: inspect the complete artifact set, compare all public claims with the current commit and parent scope, and run `python3 scripts/validate.py --scope claims` plus `python3 scripts/validate.py --scope links` once those scopes exist.

### Phase 2 — Deterministic validation and adversarial fixtures

1. Implement `python3 scripts/validate.py` using only Python's standard library, with an aggregate mode, six explicit scopes, stable check IDs, actionable diagnostics, and non-zero failure semantics.
2. Implement repository-owned checks for required public artifacts and licence, claims, canonical strategic-logic location, bounded privacy patterns, and internal links.
3. Integrate the selected TASK-002 Agent Skill validator/contract, TASK-003 lens structure, and TASK-004 evaluation metadata contract through the matching scopes. Treat a missing required dependency as a named failure; do not create local substitute semantics.
4. Add isolated synthetic fixtures and unit tests for a valid baseline and each of the six parent AC7 failure classes. Ensure the suite cannot mutate the working repository.

Validation: run `python3 scripts/validate.py`, every individual `--scope` command, `python3 -m unittest discover -s tests -v`, and compare `git status --short` before and after fixture execution.

### Phase 3 — CI and published-state proof

1. Add a least-privilege GitHub Actions workflow that runs the aggregate validator and full unit suite on pull requests and pushes to `main` without secrets.
2. Publish the completed commit to `main`, verify live visibility/default-branch state, and resolve remote `HEAD` through unauthenticated Git transport.
3. Clone the exact published commit into a new empty temporary directory and rerun the validator and unit suite there.
4. Replace placeholder child evidence with the live query, clean-checkout, artifact, commit, CI, and invalid-substitute proof required by AC5 and AC6.

Validation: inspect the green workflow run for the exact SHA; run the live and clean-checkout recipes from REQUIREMENTS.md; verify evidence references the same commit and contains no credential or private local data.

### Phase 4 — QA and contract audit

1. Audit every public support statement against committed capability/evidence and inspect the negative-fixture diagnostics for false passes.
2. Run repository Doctor after workflow evidence changes, then complete the QA/code-review gate.
3. Leave parent AC7 explicitly partial if TASK-004 evaluation metadata proof is not current; do not close TASK-001 by silently omitting the dependent check.

Validation: rerun all local, clean-checkout, and CI checks; perform a criterion-by-criterion AC1–AC6 review; confirm no invalid substitute is used as final evidence.

## Validation

- AC1 / parent AC1: inspect the five root artifacts at one commit, verify complete Apache-2.0 text, run the links scope, and compare the README/product-contract claim inventory.
- AC2 / parent AC1, AC7: run the claims scope against valid state and the unsupported-domain fixture; require the stable unsupported-claim diagnostic for the mutation.
- AC3 / parent AC7: run aggregate plus every declared scope offline; verify deterministic exit status/diagnostics and scan for operative strategic instructions outside `skills/strategic-advisor/`.
- AC4 / parent AC7: run `python3 -m unittest discover -s tests -v`; require the valid baseline and six independently named negative tests, then confirm no working-tree mutation.
- AC5 / parent AC7: inspect CI for the exact SHA and run the same aggregate/unit commands in a fresh clean checkout of that SHA.
- AC6 / parent AC1: run the exact GitHub CLI and `git ls-remote --symref` commands from REQUIREMENTS.md, inspect the clean clone, and verify populated child evidence records current identity, visibility, default branch, commit, results, and invalid substitutes.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Establish truthful public surface | Add the Apache-2.0 licence and public documentation whose capability claims match the current committed state. | AC1: required artifacts, licence, links, and cross-document claims agree.<br>AC2: capability status and evidence rules reject unsupported support claims. | Inspect root artifacts; run `python3 scripts/validate.py --scope claims` and `python3 scripts/validate.py --scope links`. | Done locally; published-commit proof pending |
| 2 | Build deterministic validation entrypoint | Implement the standard-library aggregate validator, stable diagnostics, explicit scopes, and canonical-boundary checks without network or credential dependencies. | AC3: aggregate and scoped validation are deterministic and enforce the canonical product boundary. | Run `python3 scripts/validate.py` and every declared `--scope` invocation offline; inspect exit codes and check IDs. | Done |
| 3 | Prove failure behavior with synthetic fixtures | Add isolated positive and negative fixtures for every parent AC7 failure category, integrating rather than redefining downstream skill and evaluation contracts. | AC4: valid baseline and six required negative cases pass with expected diagnostics and no working-tree mutation. | Run `python3 -m unittest discover -s tests -v`; compare `git status --short` before and after. | Done: 40 tests |
| 4 | Enforce checks in least-privilege CI | Run the aggregate validator and full test suite on pull requests and pushes to `main` using the checked-out commit and no secrets. | AC5: CI and a clean checkout of the exact published SHA both pass the same commands. | Inspect the workflow permissions, commands, trigger set, run SHA, and green conclusion; reproduce in a fresh clone. | Implemented; live run pending |
| 5 | Prove public repository state | Query live GitHub and unauthenticated Git state, validate a clean checkout, and populate child evidence with exact current proof. | AC6: public visibility, default `main`, artifact set, commit identity, clean-checkout result, and CI proof are recorded without invalid substitutes. | Run the REQUIREMENTS.md live/clean recipes and compare outputs with `EVIDENCE.json`. | To Do |
| 6 | Complete QA and claim audit | Review all public claims and validation boundaries, rerun every proof target, and complete QA/code review without masking downstream dependency gaps. | AC1–AC6: every child criterion has current direct evidence or remains explicitly unsatisfied. | Review the criterion evidence map, Doctor output, clean worktree, and exact published CI SHA. | To Do |

## Parent AC Evidence

- Parent AC1: root artifacts and conservative claims pass local validation; live GitHub visibility/default-branch query, unauthenticated clean checkout, and populated `EVIDENCE.json` remain pending at the delivered commit.
- Parent AC7: local aggregate validation passes all seven scopes and 40 standard-library tests, including independent negative fixtures. Clean-checkout execution and green CI for the delivered commit remain pending. TASK-004 remains co-owner of evaluation metadata validity and comparative-evaluation proof.
- Recipe-triggered published/runtime claims must be backed by current child `EVIDENCE.json`; local files, local remotes, or prose are invalid substitutes.

## QA & Code Review

- Verdict: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-001
- Title: Establish Public Product Contract and Packaging
- Created: 2026-07-22
