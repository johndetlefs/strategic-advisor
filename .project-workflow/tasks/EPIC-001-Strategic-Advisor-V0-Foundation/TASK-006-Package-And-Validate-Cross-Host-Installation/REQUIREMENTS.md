# Requirements

## Summary

- Task: TASK-006
- Title: Package and Validate Cross-Host Installation
- Parent AC Coverage: AC1, AC2, AC7
- Last updated: 2026-07-22

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: Yes
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-07-22
- Approval note / source: Codex conversation on 2026-07-22: owner approved Option A and directed the project to move as quickly as possible toward installable Codex, Claude, and ChatGPT use with further testing acknowledged.
- Approved artifact identity: `.project-workflow/tasks/EPIC-001-Strategic-Advisor-V0-Foundation/TASK-006-Package-And-Validate-Cross-Host-Installation/REQUIREMENTS.md`

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

Deliver one reviewable, content-addressed Strategic Advisor runtime bundle that John and his wife can install for real-world testing in Codex, Claude, or ChatGPT without exposing the evaluation surface or creating host-specific copies of the strategic method. Distinguish a structurally installable path, exact-host activation proof, and behaviourally supported advice so early access can begin without inflating product claims.

## Overview

The development repository contains the canonical skill and its deliberately adjacent evaluation authority. Pointing a host at the raw repository is therefore neither a portable installation method nor an acceptable production boundary. This task turns the allowlisted runtime bytes already owned by TASK-004 into a deterministic end-user archive, documents thin installation paths for Codex, Claude Code, Claude.ai, and ChatGPT, and records exact runtime-target/source evidence for every host actually tested.

## User Story

As an early Strategic Advisor user, I want to install the exact packaged, allowlisted runtime skill in my preferred flagship-model host so that I can start real decisions quickly while still seeing which installation and behavioural claims are proven, experimental, or untested.

## Non-Goals

- Copying or translating the strategic instructions into vendor-specific prompts.
- Claiming behavioural parity across hosts or models from archive compatibility or one successful invocation.
- Broad Slack, Teams, email, calendar, repository, or document ingestion.
- Publishing to the public Plugin Directory before the install artifact and current host paths pass their own gates.
- Treating an upload receipt, visible skill name, unit test, or documentation screenshot as proof that a response used the packaged source.
- Adding domains beyond the four v0 professional lenses.

## Users & Context

- John needs a Codex installation usable from another project repository without exposing Strategic Advisor's evaluation files.
- An early non-maintainer user needs a low-friction Claude.ai, Claude Code, or eligible ChatGPT installation using the same canonical runtime bytes.
- Maintainers need deterministic artifact identity and host-specific evidence so a successful upload cannot silently become a general support claim.
- Hosted-product availability, workspace permissions, and upload UI may differ by plan or administrator; those facts are recorded as current host constraints rather than hidden by generic instructions.

## Requirements (Outcome-Focused)

- R1. Build operative skill bytes only from `skills/strategic-advisor/runtime-manifest.json`. The archive contains one top-level `strategic-advisor/` directory with the allowlisted `SKILL.md` and resources plus a byte-identical copy of the repository's Apache-2.0 `LICENSE`, deterministic ordering/metadata, and no evaluation, result, fixture, freeze, rubric, score, or repository-development content.
- R2. Record the runtime-package identity, archive SHA-256, operative file hashes, source allowlist hash, source revision, Apache-2.0 licence hash, and archive structure in a machine-readable manifest outside the model-visible skill directory. Rebuilding the same source produces byte-identical archive and manifest identities.
- R3. The repository validator and standard-library tests fail on archive drift, a missing allowlisted file, an extra or symlinked file, path traversal, non-deterministic archive metadata, a mismatched package identity, or any evaluation-surface content.
- R4. Codex installation uses either a documented personal/plugin path or a project-local thin link to the packaged canonical directory. A clean context must prove discovery, activation, and exact source identity before the Codex path is called validated.
- R5. Claude Code installation uses its documented personal, project, or plugin skill location without copying logic. A clean context must prove discovery, activation, and exact source identity before the Claude Code path is called validated.
- R6. Claude.ai and ChatGPT installation use the same generated archive. Public instructions state current plan/workspace prerequisites and provide an exact upload/invocation check; each hosted path remains experimental until a live fresh chat proves successful upload, activation, and source-bound behaviour.
- R7. Host and installation claims remain separate from behavioural claims. An installed host may be described as structurally compatible or activation-validated while the advisor remains pre-release, and no host inherits another host's evidence.
- R8. Public documentation explains the recommended operating model: install once, keep case state in a private project/repository and decision record, use one thread per substantive decision/update, and treat connectors as optional scoped evidence access rather than memory or truth.
- R9. Generate a skill-only OpenAI local marketplace/plugin bundle from the same runtime bytes without committing a separately maintained strategic copy. Its plugin and marketplace metadata are deterministic and validated for the documented structure used by Codex and ChatGPT desktop Work mode. Do not represent that two-root local-marketplace archive as a direct Personal Skill upload or public Plugin Directory submission package; those remain distinct contracts.
- R10. Generated distribution artifacts are suitable for an early-access GitHub release or direct download, but repository validation never depends on committing generated ZIP bytes or generated plugin skill copies.

## Acceptance Criteria (Verifiable)

- AC1: A clean build produces a deterministic Agent Skills archive, skill-only local marketplace/plugin bundle, and external manifest from the runtime allowlist; two builds from identical source are byte-identical, every model-visible byte is allowlisted, and no evaluation/development content is present. Covers parent AC2 and AC7.
- AC2: Positive and negative standard-library tests plus `python3 scripts/validate.py` enforce package identity, archive structure, path/symlink safety, determinism, and evaluation-surface exclusion locally and in credential-free CI. Covers parent AC7.
- AC3: A fresh Codex context discovers and invokes the packaged skill, and retained runtime-target-source evidence positively identifies the tested package rather than the raw repository or another skill copy. Covers parent AC2.
- AC4: A fresh Claude Code context discovers and invokes the same packaged bytes, or its capability remains explicitly experimental with the missing live proof named. Covers parent AC2.
- AC5: The same archive is accepted by Claude.ai and eligible ChatGPT upload flows and invoked in fresh chats, or each untested/unavailable path remains explicitly experimental with exact user verification steps and no supported claim. Covers parent AC1 and AC2.
- AC6: README, installation guidance, product contract, generated artifact metadata, and live evidence agree independently for Codex, Claude Code, Claude.ai, and ChatGPT on availability, prerequisites, artifact identity, validation state, and behavioural limitations. Covers parent AC1.
- AC7: A clean-checkout build and validation reproduce the same package identity, and no host adapter contains copied executable strategic instructions. Covers parent AC2 and AC7.

## Open Questions (Answer Needed)

- None. Hosted UI proof is externally evidence-dependent, but failure to obtain it does not block creation of the honest experimental archive or the locally testable Codex/Claude Code paths; it blocks only the corresponding validated-host claim.

## Decisions (Resolved)

- D1. Use one deterministic Agent Skills ZIP whose top-level directory is `strategic-advisor/`; do not create separate strategic source archives per host.
- D2. The install archive is derived from the allowlisted runtime package, never from the raw `skills/strategic-advisor/` development tree.
- D3. Generate one skill-only OpenAI local marketplace/plugin bundle now. Current OpenAI documentation uses the same repo/personal marketplace layout for Codex and ChatGPT desktop Work mode. ChatGPT may therefore be tested through either the standalone Personal Skill where eligible or the local plugin in desktop Work mode, but each route needs its own live proof. The bundle is not a direct Skill upload or public Plugin Directory submission, and generated plugin contents cannot become a second source of strategic logic.
- D4. Installation compatibility, exact-host activation, comparative behavioural improvement, and real-world usefulness are separate claims with separate evidence.
- D5. Permit early experimental use after deterministic packaging and clear instructions, while retaining pre-release status until the existing behavioural and pilot gates pass.
- D6. Keep broad connectors deferred; this task includes no external workspace access.
- D7. Owner approved this amended child scope on 2026-07-22 to accelerate real-world Codex, Claude, and ChatGPT testing while continuing stronger evaluation.

## Validation Plan

- AC1: Build twice into separate temporary directories, compare standalone archive, local marketplace/plugin bundle, and manifest bytes/hashes, list every model-visible entry, and compare each skill file with the runtime-package manifest.
- AC2: Run the aggregate validator and full unit suite; exercise isolated malformed archives for extra files, evaluation content, traversal, symlinks, metadata drift, and identity mismatch.
- AC3 and AC4: Use the `runtime-target-source` proof recipe. Retain host/version/model, clean-context identity, execution target, archive/package hashes, invocation prompt, output, observation method, and positive proof that the host loaded that source. A visible skill name or plausible answer is an invalid substitute.
- AC5: Use the same runtime-target-source recipe for each hosted UI. Retain upload acceptance plus fresh-chat activation and source-bound proof; a local ZIP, documentation, or another host's success is not evidence.
- AC6: Validate the machine-readable claim registry and compare public instructions with exact current host evidence and official platform prerequisites.
- AC7: Rebuild and validate in a clean checkout, scan host adapters for copied logic, and retain the exact commit and CI run identity.
