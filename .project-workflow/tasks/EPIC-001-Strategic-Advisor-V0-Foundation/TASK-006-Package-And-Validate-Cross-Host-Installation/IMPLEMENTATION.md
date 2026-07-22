## User Story

As an early Strategic Advisor user, I want to install the exact packaged, allowlisted runtime skill in my preferred flagship-model host so that I can start real decisions quickly while still seeing which installation and behavioural claims are proven, experimental, or untested.

## Parent AC Coverage

- AC1, AC2, AC7

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

- AC1: owner `TASK-001, TASK-006`; required evidence: Live GitHub query, clean-checkout artifact/link review, install-artifact identity, and public-claim comparison.
- AC2: owner `TASK-002, TASK-006`; required evidence: Skill specification validation, allowlisted runtime-package proof, clean-context exact-host invocation proof, and duplicate-logic scan.
- AC7: owner `TASK-001, TASK-004, TASK-006`; required evidence: Passing positive/negative validators locally and in a clean CI checkout, including package drift and forbidden evaluation-surface fixtures.

## Goal

Produce the deterministic early-access Agent Skills archive, prove every locally available host against the exact package, and give John and his wife truthful installation paths for Codex, Claude Code, Claude.ai, and ChatGPT without waiting for the full behavioural release gate or weakening it.

## Approach

- Extend the existing allowlist packager rather than create a second content-selection implementation.
- Generate a deterministic standalone ZIP plus a skill-only OpenAI local marketplace/plugin bundle with one `strategic-advisor/` skill root and separate provenance; never copy `evals/` or development files, and do not mislabel the local marketplace as a direct Skill upload or public Plugin Directory submission archive.
- Prove structure and negative behavior with standard-library tests before attempting host invocation.
- Validate Codex and Claude Code in fresh contexts when the executables are available; prepare the exact same archive for hosted ChatGPT and Claude.ai upload and retain live evidence when an authorised user performs those checks.
- Keep public claims granular: buildable, upload-compatible, activation-validated, behaviourally evaluated, and pilot-validated are different states.

## Phases

### Phase 1 — Deterministic distribution artifact

- Add deterministic standalone archive and generated local marketplace/plugin packaging plus external provenance using the existing runtime allowlist and package identity.
- Add positive and adversarial tests for archive structure, byte determinism, leakage, symlinks, traversal, and identity drift.
- Validation: two independent builds are byte-identical and the aggregate repository suite passes.

### Phase 2 — Thin host paths and local proof

- Add non-copying Codex and Claude Code project/personal installation guidance or links.
- Invoke the exact package in isolated fresh local contexts where available and retain runtime-target-source evidence.
- Validation: host discovery and source identity are positive; otherwise the host remains experimental with the missing proof explicit.

### Phase 3 — Hosted upload path

- Provide the same archive and current prerequisite/invocation steps for ChatGPT and Claude.ai.
- Capture live upload and fresh-chat activation evidence with an authorised account when available.
- Validation: each hosted path receives its own verdict; one host cannot satisfy another.

### Phase 4 — Public contract, clean checkout, and QA

- Align README, product contract, install guide, and generated metadata with exact evidence.
- Rebuild from a clean checkout, run deterministic CI-ready validation, and complete QA/code review.
- Validation: no copied strategic logic, no unsupported host claim, and exact package identity throughout.

## Acceptance Criteria

- [x] AC1: A deterministic allowlisted Agent Skills archive, generated skill-only OpenAI local marketplace/plugin bundle, and external manifest are byte-identical across equivalent builds and exclude all evaluation/development content. Covers parent AC2 and AC7. Two clean builds of release commit `c15c859dbdd69bac78c4708532f4fe2406320d17` are byte-identical and the published assets retain those identities.
- [x] AC2: Repository validation and positive/negative tests enforce artifact identity, archive safety, determinism, and leakage exclusion. Covers parent AC7. The fresh public clone passed 93 tests, all validator scopes, and strict workflow doctor; exact-main CI run `29900504587` passed including artifact reproduction.
- [x] AC3: A fresh Codex context discovers and invokes the exact packaged source with retained runtime-target-source proof. Covers parent AC2. The downloaded standalone archive was invoked in an isolated clean Codex project with retained hash and source-access events.
- [x] AC4: A fresh Claude Code context proves the equivalent path, or remains explicitly experimental with the missing proof named. Covers parent AC2. Claude Code is unavailable on the current test machine, and the missing live proof is explicit.
- [x] AC5: Claude.ai and eligible ChatGPT accept and invoke the same archive in fresh chats, or remain individually experimental with exact verification steps. Covers parent AC1 and AC2. Both hosted paths remain experimental pending authorised account checks.
- [ ] AC6: Public and machine-readable claims agree for every host on prerequisites, artifact identity, validation state, and behavioural limitations. Covers parent AC1. The corrected documents agree in this review branch; live default-branch verification must follow publication.
- [x] AC7: Clean-checkout build/validation reproduce the package identity and no host adapter copies strategic logic. Covers parent AC2 and AC7. Public-clone reproduction, independent download verification, exact-main CI, and negative drift/leakage coverage pass.

## Validation

- AC1: Build twice, compare bytes/hashes and archive entry hashes, and verify exact allowlist membership.
- AC2: Run the aggregate validator and full unit suite including isolated invalid archive fixtures.
- AC3–AC5: Retain one runtime-target-source record per host with exact source/package identity and fresh-context activation evidence.
- AC6: Run claims/link scopes and manually compare current official prerequisites with the host matrix.
- AC7: Rebuild and run the complete suite in a clean checkout; scan adapters and generated bundles for copied or evaluation logic.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Build deterministic install artifacts | Generate one content-addressed Agent Skills ZIP, skill-only local marketplace/plugin bundle, and external provenance from the existing runtime allowlist. | AC1, AC2: artifact bytes and manifest are reproducible, safe, allowlisted, and evaluation-free. | Build twice in fresh temporary targets; compare SHA-256 and inspect all ZIP/plugin entries. | Done — exact clean release and published-asset identities retained |
| 2 | Enforce package failure behavior | Extend validation and tests for leakage, extras, symlinks, traversal, metadata drift, and identity mismatch. | AC2, AC7: every invalid fixture fails with an expected diagnostic and the valid clean build passes. | Run `python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v`. | Done — 93-test clean suite, all scopes, exact-main CI, and strict doctor pass |
| 3 | Prove Codex installation | Install or link the packaged source in a clean Codex target and retain discovery, activation, and exact-source proof. | AC3: runtime-target-source evidence identifies the tested package and fresh context. | Invoke the skill explicitly on a synthetic canary and inspect loaded source identity. | Done — exact downloaded package and observable source-access trace retained |
| 4 | Prove Claude Code installation | Install or link the same package at a documented Claude Code scope and retain equivalent proof if the host is available. | AC4: exact-host evidence passes, or public state remains experimental with the missing step explicit. | List available skills and invoke `/strategic-advisor` in a fresh clean project. | Done as explicit experimental path; executable unavailable locally |
| 5 | Prepare and validate hosted uploads | Document and exercise the same ZIP in Claude.ai and eligible ChatGPT using authorised fresh chats. | AC5: each host has its own upload/activation evidence or an explicit experimental verdict and exact user check. | Upload, enable/install, explicitly invoke, and retain non-private host evidence. | Done as explicit experimental paths; authorised UI proof pending |
| 6 | Align public host matrix | Update README, installation guide, product contract, and claim validation without implying behavioural parity. | AC6: public and structured claims match current proof for all four host paths. | Run claim/link validation and compare every host row with its evidence record. | In Testing — corrected documents await default-branch publication and live recheck |
| 7 | Reproduce and hand off | Rebuild from a clean checkout, run the full suite, complete QA/code review, and prepare the exact early-access artifact. | AC7 and all ACs: clean proof is current and no invalid substitute is used. | Compare clean archive identity, CI-ready results, evidence records, and QA verdict. | In Testing — QA changes requested; public-claim closure remains |

## Parent AC Evidence

- AC1: CLM-001 remains pending until the corrected README, installation guide, and product contract are merged to the public default branch and rechecked there. Release existence and artifact identities are already observed, but they are not an invalid substitute for live public-claim alignment.
- AC2: `EVIDENCE.json` CLM-002, `evidence/CLM-002-codex-runtime-source.json`, and its linked trace/output retain exact downloaded-package source use in a fresh Codex target.
- AC7: `EVIDENCE.json` CLM-006 and `evidence/CLM-006-clean-release-reproduction.json` retain the fresh public clone, two-build comparison, independent verifier result, 93-test suite, exact-main CI, and downloaded-asset recheck.

## QA & Code Review

- Date: 2026-07-22
- Verdict: Changes requested
- Evidence: 93/93 unit tests pass; all seven repository validator scopes pass; the 31-case generated inventory is current; strict workflow doctor and `git diff --check` pass; exact artifact and nested evidence hashes were independently recomputed.
- Findings: The first review rejected CLM-001 because it claimed live public-claim alignment at release commit `c15c859dbdd69bac78c4708532f4fe2406320d17`, whose README and installation guide still predated the published release and retained Codex proof. The review also required the exact Codex invocation prompt and separation of alpha-pinned verification from local-build verification. The prompt and verifier documentation are now corrected in this branch. CLM-001, AC6, task row 6, and final handoff remain open until these documentation changes are public and verified on `main`.
- Follow-ups not blocking this early-access packaging task: Claude Code, Claude.ai, ChatGPT Personal Skills, and ChatGPT desktop Work-mode activation remain experimental; matched behavioural evaluation and real-pilot validation remain outside this task and incomplete.

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-006
- Title: Package and Validate Cross-Host Installation
- Created: 2026-07-22
