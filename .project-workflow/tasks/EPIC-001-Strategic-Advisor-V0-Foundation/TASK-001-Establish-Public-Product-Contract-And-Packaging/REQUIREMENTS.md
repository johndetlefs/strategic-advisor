# Requirements

## Summary

- Task: TASK-001
- Title: Establish Public Product Contract and Packaging
- Parent AC Coverage: AC1, AC7
- Last updated: 2026-07-22

## Overview

Establish the public, inspectable boundary of Strategic Advisor before the repository claims a working product. The repository must state exactly what is planned, implemented, validated, and unsupported; provide the Apache-2.0 legal and contribution surface; and expose one deterministic validation entrypoint that can enforce repository-wide packaging invariants locally and in CI.

This child owns the public contract, validation orchestration, representative negative fixtures, and published-repository proof. It does not define the strategic method, professional lens semantics, or evaluation rubric. It integrates the canonical contracts produced by those children and must remain blocked rather than inventing a substitute when a downstream contract does not yet exist.

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

- AC1: owner `TASK-001`; required evidence: Live GitHub query, clean-checkout artifact/link review, and public-claim comparison.
- AC7: owner `TASK-001, TASK-004`; required evidence: Passing positive/negative validators locally and in a clean CI checkout.

## User Story

As a prospective user or contributor evaluating Strategic Advisor, I want the public repository to distinguish demonstrated capability from intent and to provide reproducible packaging checks, so that I can decide whether to use, inspect, or contribute to it without relying on promotional claims or the maintainer's local workspace.

## Goal

Deliver a truthful public repository surface and a deterministic validation boundary that make unsupported claims, broken packaging, representative private-data leakage, and drift from the canonical product structure observable before merge or release.

## Non-Goals

- Implementing or evaluating the canonical reality protocol; that belongs to TASK-002 and TASK-004.
- Defining or validating the substantive project/product, career, organisational-influence, or people-leadership lenses; that belongs to TASK-003 and TASK-004.
- Defining the evaluation rubric, paired-run protocol, scoring thresholds, or evaluation metadata schema; that belongs to TASK-004.
- Running real pilots or declaring v0 release readiness; that belongs to TASK-005.
- Shipping connectors, a service, an application, a package-registry release, or host-specific copies of strategic logic.
- Claiming that static scans can identify every form of personal, proprietary, or sensitive narrative data. The validator is a bounded guardrail, not a privacy guarantee.
- Validating the content or availability of arbitrary external web links during deterministic local checks.

## Users & Context

- Prospective users need to know whether the repository currently contains an installable and evaluated advisor or only a foundation under development.
- Contributors need one canonical product location, explicit contribution and disclosure boundaries, and commands that reproduce CI without hidden services or credentials.
- Maintainers need public claims to remain coupled to current capability evidence as downstream skill, lens, and evaluation artifacts are added.
- Reviewers need live GitHub state and a clean checkout to prove publication facts; a configured local remote, unpushed branch, or local passing run is not equivalent evidence.

## Requirements (Outcome-Focused)

- R1. The repository root contains an accurate `README.md`, `PRODUCT-CONTRACT.md`, `CONTRIBUTING.md`, `SECURITY.md`, and complete Apache License 2.0 text in `LICENSE`, with working internal links between the artifacts.
- R2. `PRODUCT-CONTRACT.md` is the public source of truth for capability claims. It distinguishes planned, implemented-but-not-validated, and validated capability; only validated capability may be described as supported, and each validated claim must identify current evidence.
- R3. The README states the repository's current maturity, canonical product path, installation and invocation availability, validated domains, unsupported domains, connector status, limitations, and validation commands without presenting future work as current capability.
- R4. The contribution and security surfaces prohibit private case data, explain the evidence and canonical-logic rules, provide a reproducible contribution check, and direct sensitive vulnerability reports to a non-public repository channel without promising unsupported response times or security guarantees.
- R5. The live repository is `johndetlefs/strategic-advisor`, is public, and uses `main` as its default branch. These facts are verified through the live GitHub API/CLI and unauthenticated Git transport, not inferred from local configuration.
- R6. `python3 scripts/validate.py` is the single deterministic repository validation entrypoint. It uses only declared repository code and Python's standard library, requires no network access, credentials, model call, or private input, returns non-zero on any failed check, and emits stable check identifiers with actionable diagnostics.
- R7. The entrypoint supports explicit `skill`, `lenses`, `evals`, `privacy`, `claims`, and `links` scopes and an unscoped aggregate run. Scope behavior is driven by the public product contract and the committed downstream contracts; a missing required contract or artifact fails explicitly rather than being silently skipped.
- R8. TASK-001 owns the validation orchestrator and repository-level claim, privacy, canonical-location, link, licence, and public-artifact checks. TASK-002 owns the selected Agent Skill structure contract; TASK-003 owns lens structure; TASK-004 owns evaluation metadata semantics. TASK-001 integrates those checks without duplicating or weakening their source contracts.
- R9. A standard-library `unittest` suite uses only synthetic fixtures and proves that isolated mutations for representative private data, unsupported-domain claims, strategic-logic duplication, malformed skill structure, broken internal links, and invalid evaluation metadata each fail with the expected named diagnostic. The suite also proves that the unmodified valid fixture passes.
- R10. Privacy fixtures cover explicitly labelled private/proprietary case material and representative secret/credential formats, but public documentation states that passing the scan does not prove a repository contains no sensitive data. No real secret, employer, client, or household content is used.
- R11. Continuous integration runs the aggregate validator and complete unit suite from the checked-out commit on pull requests and pushes to `main`, with read-only permissions and without secrets. A clean checkout of the same published `main` commit must produce the same passing result.
- R12. Proof for public visibility, default branch, clean-checkout validation, and CI is retained in child evidence with exact repository identity, commit SHA, command, timestamp, result, and CI run URL or identifier; the evidence does not contain credentials or local private paths.

## Acceptance Criteria (Verifiable)

- AC1: (Parent AC1) At the same commit, `README.md`, `PRODUCT-CONTRACT.md`, `CONTRIBUTING.md`, `SECURITY.md`, and `LICENSE` exist at repository root; `LICENSE` contains the complete Apache License 2.0 text; all internal links in those artifacts resolve; and the README and product contract agree on maturity, installation availability, canonical path, validated domains, unsupported domains, and connector status.
- AC2: (Parent AC1, AC7) The public capability contract identifies each advertised domain, host/packaging path, connector, and material behaviour as planned, implemented-but-not-validated, or validated with evidence; an injected claim that an unvalidated domain is supported makes `python3 scripts/validate.py --scope claims` fail with the stable unsupported-claim diagnostic.
- AC3: (Parent AC7) `python3 scripts/validate.py` and each declared scope run deterministically without network access or credentials, return zero for the valid repository state, return non-zero with stable check identifiers for failures, and do not contain strategic instructions outside `skills/strategic-advisor/`.
- AC4: (Parent AC7) `python3 -m unittest discover -s tests -v` passes and independently proves all six parent failure categories: representative private-data fixture, unsupported-domain claim, strategic-logic duplication, malformed skill structure, broken internal link, and invalid evaluation metadata. Each mutation is isolated, synthetic, expects its specific diagnostic, and leaves the working tree unchanged. Skill and evaluation fixtures are checked against the committed TASK-002 and TASK-004 contracts, not locally invented substitutes.
- AC5: (Parent AC7) A least-privilege GitHub Actions workflow runs `python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v` on pull requests and pushes to `main`; the same two commands pass in a fresh clean checkout of the exact published commit, and the CI run for that SHA is green.
- AC6: (Parent AC1) Live queries prove `johndetlefs/strategic-advisor` is public and its default branch is `main`; an unauthenticated clean clone resolves `HEAD` to `refs/heads/main` and contains the AC1 artifact set at the evidenced commit. The corresponding `EVIDENCE.json` claims record exact commands, timestamp, commit, artifacts, results, and invalid substitutes.

## Open Questions (Answer Needed)

- None. Completion of AC4 depends on the committed TASK-002 skill contract and TASK-004 evaluation metadata contract; this is a planned dependency, not authority to guess either contract.

## Decisions (Resolved)

- D1. Use Apache License 2.0, as explicitly approved by the owner on 2026-07-22.
- D2. Use `PRODUCT-CONTRACT.md` as the public capability-claim authority and permit the word “supported” only for validated capability with current evidence.
- D3. Use `python3 scripts/validate.py` as the sole validation entrypoint, with `skill`, `lenses`, `evals`, `privacy`, `claims`, and `links` scopes; use standard-library `unittest` for positive and negative fixture proof.
- D4. Keep the validator deterministic and standard-library-only. Live GitHub and clean-clone checks are delivery evidence gathered separately, not hidden network behavior inside the local validator.
- D5. Use GitHub's private vulnerability-reporting mechanism as the non-public security channel so the project does not require a personal email address in public documentation.
- D6. Treat static privacy checks as bounded detection of committed fixture classes, never as proof that no sensitive narrative data exists.
- D7. Keep strategic logic solely under `skills/strategic-advisor/`; the public docs, validator, tests, CI, and Project Workflow artifacts may describe or verify the boundary but must not contain a second operative advisor prompt.
- D8. A downstream scope may report “not present and not claimed” while that capability remains planned, but it must fail if the public contract claims the missing capability is implemented or validated.

## Validation Plan

- Local aggregate: run `python3 scripts/validate.py` and retain its stable check summary.
- Local scopes: run `python3 scripts/validate.py --scope skill`, `--scope lenses`, `--scope evals`, `--scope privacy`, `--scope claims`, and `--scope links`; confirm the declared capability state determines whether an absent downstream artifact is permissible or a failure.
- Negative fixtures: run `python3 -m unittest discover -s tests -v`; confirm there is one independently named test for each AC4 failure category plus a valid-baseline test, and confirm `git status --short` is unchanged after the suite.
- Public state: run `gh repo view johndetlefs/strategic-advisor --json nameWithOwner,url,visibility,defaultBranchRef` and `git ls-remote --symref https://github.com/johndetlefs/strategic-advisor.git HEAD`; retain the output fields required by AC6 without authentication material.
- Clean checkout: clone `https://github.com/johndetlefs/strategic-advisor.git` at the evidenced `main` SHA into a new empty temporary directory, run the aggregate validator and unit suite there, inspect the root artifact set and internal links, and record the commit with `git rev-parse HEAD`.
- CI: inspect the GitHub Actions run for the exact clean-checkout SHA and record workflow identity, run URL/ID, conclusion, and validation command output reference.
- Public-claim review: compare every supported statement in README, product contract, contribution guide, and security policy with current committed artifacts and evidence; record discrepancies as failures rather than interpreting intent.
- Evidence artifact: replace placeholder claims in child `EVIDENCE.json` with appropriate live-published-repository and clean-runtime proof recipes, current commit/timestamps, exact delivered artifacts, comparison methods, hashes where applicable, and invalid substitutes.
- Invalid substitutes: local `origin` configuration does not prove repository visibility or default branch; an unpushed local file does not prove a public artifact exists; a local passing run does not prove clean-checkout or CI behavior; a validator test does not prove strategic quality; absence of a scanner finding does not prove absence of private data.
