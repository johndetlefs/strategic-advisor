# Requirements

## Summary

- Task: TASK-013
- Title: Build Current Cross-Host Alpha Distribution
- Parent AC Coverage: AC1, AC2, AC7, AC8, AC9
- Last updated: 2026-07-24

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

- One canonical Strategic Advisor runtime owns strategic logic.
- Host adapters are deterministic projections or unchanged packages of that runtime, never independently maintained strategic prompts.
- The evaluation plane, Project Workflow files, private cases, credentials, and retained hidden reasoning never enter install artifacts.
- A Strategy Workspace is optional and is never created or accessed by this Epic.
- One host's package acceptance, activation, or behaviour does not prove another host.
- Package build, installation, discovery, activation, behavioural smoke, validation, support, and effectiveness remain distinct claims.
- No enterprise control is bypassed, and unavailable account/admin prerequisites remain explicit.
- All live checks use public fictional cases and retain only bounded evidence.

### Invalid Substitutes

- The repository authoring symlink in place of John's personal Codex install.
- A stale global install in place of the current release artifact.
- Archive structure or upload success in place of visible host discovery and activation.
- A model statement that it used the Skill in place of an independently observable activation/source event.
- Codex evidence in place of ChatGPT or Claude evidence.
- A personal ChatGPT Custom GPT in place of an unavailable ChatGPT Personal Skill claim.
- A generated Custom GPT prompt that has drifted from canonical `SKILL.md`.
- A ChatGPT or Claude screenshot containing private account, employer, or case information in public evidence.
- Administrator denial in place of claiming the Claude package is defective, or package readiness in place of claiming Claude activation passed.
- The bounded Codex drift smoke in place of ChatGPT/Claude behavioural parity or effectiveness evidence.

### Artifact Targets

- Deterministic standalone Skill ZIP for Codex and Claude.
- Existing deterministic OpenAI local-plugin ZIP where applicable.
- Deterministic ChatGPT Custom GPT kit with generated Instructions, declared Knowledge inventory, configuration, first-use guide, and provenance.
- One cross-artifact provenance authority tied to exact source revision and runtime identity.
- Public release assets and concise host-specific onboarding.
- Bounded Codex, ChatGPT, and Claude host evidence only where live execution occurs.

### Parent AC Proof Ownership

- AC1: owner `Cross-host distribution child`; required evidence: Repeated clean build identity, exact provenance, safe inventories, and leakage scans.
- AC2: owner `Cross-host distribution child`; required evidence: Generated Instructions/source binding, exact Knowledge inventory/bytes, file-limit check, and negative drift tests.
- AC7: owner `All children`; required evidence: Structured and prose claim comparison against exact retained evidence.
- AC8: owner `Cross-host distribution child`; required evidence: Current lens/workspace runtime inventory plus no-workspace/no-connector first-use proof.
- AC9: owner `All children`; required evidence: Unit, aggregate, artifact, privacy, clean-checkout, QA, doctor, and closeout evidence.

## Goal

Produce one current, deterministic, downloadable alpha distribution whose Codex/Claude Skill, OpenAI plugin, and ChatGPT Custom GPT kit all derive from the same canonical runtime and carry exact external provenance.

## Non-Goals

- Live account installation or activation, owned by TASK-014 and TASK-015.
- Public marketplace or GPT Store submission.
- New strategic behaviour, connectors, infrastructure, dependencies, or private data.

## Users & Context

- John and Christina need installable files rather than repository source.
- Host-specific adapters must not create a second strategic source of truth.
- Maintainers need a release that can be rebuilt, verified, and safely supersede the stale alpha.

## Requirements (Outcome-Focused)

- R1. Extend the existing install-artifact builder and provenance schema with one deterministic ChatGPT Custom GPT kit.
- R2. Generate the Custom GPT Instructions from canonical `SKILL.md` with only a bounded host bootstrap; copy the remaining runtime references/templates as Knowledge with exact byte hashes.
- R3. Keep the Knowledge inventory within the official 20-file limit and exclude `SKILL.md`, host metadata, evaluations, workflow files, and unexpected content.
- R4. Include deterministic GPT configuration, first-use prompts, capability settings, and source/runtime identities.
- R5. Build all artifacts twice from a clean exact revision, verify identical bytes, and publish them together as a new GitHub alpha prerelease.
- R6. Update public product/install claims to distinguish this build from live host activation and supported capability.

## Acceptance Criteria (Verifiable)

- AC1: Repeated clean builds produce byte-identical standalone, plugin, ChatGPT-kit, and provenance artifacts bound to one exact source revision and runtime identity.
- AC2: The verifier rejects Instructions drift, Knowledge inventory/byte drift, unsafe paths, over-limit files, configuration drift, evaluation/workflow/private leakage, and cross-artifact inconsistency.
- AC3: The Custom GPT kit contains a generated canonical strategic body, exactly 19 declared Knowledge files, no apps/actions, useful first prompts, and a human-authority/pre-release boundary.
- AC4: The new alpha prerelease exposes all required assets and their published hashes; a clean download verifies against those exact identities.
- AC5: README, INSTALL, architecture, product contract, and structured status make no stronger claim than built-and-ready artifacts until TASK-014/TASK-015 provide exact host evidence.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- D1. Extend `scripts/build_install_artifacts.py`; do not create a parallel packaging tool.
- D2. Use one additional deterministic ZIP for the Custom GPT kit.
- D3. Keep executable dependencies at Python standard library only.
- D4. Treat the GitHub prerelease and exact asset hashes as deployed-artifact proof, not host activation proof.

## Validation Plan

- AC1-AC3: Focused positive/negative builder tests, repeated build comparison, archive inspection, source/runtime recomputation, and leakage scans.
- AC4: Publish a new prerelease, download its assets in a clean temporary directory, and run the consumer verifier against published hashes.
- AC5: Run aggregate claim validation and manually compare every changed public claim with the exact evidence state.
