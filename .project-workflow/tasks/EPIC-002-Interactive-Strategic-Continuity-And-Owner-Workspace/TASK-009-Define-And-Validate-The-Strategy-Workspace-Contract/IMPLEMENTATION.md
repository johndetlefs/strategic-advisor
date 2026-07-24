## User Story

As a returning Strategic Advisor user, I want an optional, inspectable Markdown workspace for owner-approved strategic context, so that continuity can improve later decisions without turning stored material into authority or making setup mandatory.

## Goal

Ship a small public Strategy Workspace contract that can be reproduced and validated deterministically while remaining optional, user-owned, least-data, and subordinate to current evidence.

## Approach

- Keep model-visible workspace guidance in one concise canonical reference and five blank Markdown templates under `skills/strategic-advisor/`.
- Use one dependency-free repository command with explicit `build` and `validate` subcommands so the safety rules and schemas have one implementation.
- Build only into a new directory from canonical templates; never update or overwrite an existing workspace.
- Validate the exact file allowlist, required headings and table schemas, record IDs, epistemic statuses, provenance/freshness/approval controls, and forbidden leakage patterns.
- Emit deterministic JSON. Structural and safety breaches are errors; past review dates and declared conflicts are attention items because they must be surfaced rather than silently resolved.
- Reuse the existing runtime/install builders and their leakage boundaries instead of creating a parallel packaging system.

## Phases

1. Contract: author the canonical instructions/templates and bind them to the runtime allowlist.
2. Tooling: implement deterministic scaffold build/validation and focused synthetic tests.
3. Integration: extend repository checks and verify runtime/install reproduction.
4. Closeout: run workflow gates, QA/code review, evidence mapping, and retro.

## Parent AC Coverage

- AC4, AC5, AC7, AC9

## Child Charter

### Inherited Invariants

- Strategic Advisor remains useful without a repository or workspace.
- The full strategic protocol is selectively invoked by decision intent and consequence, not by keywords, repository location, or workspace presence.
- Open exploration may remain conversational until a decision object emerges; readiness is not manufactured merely to complete a response template.
- Operate at the minimum sufficient altitude and return from exploration to a bounded decision or validation step.
- Dialogue may expand the option set; only qualifying evidence, scope, or constraints may change claim support or readiness.
- Opposite user preferences on the same material facts do not change the diagnosis.
- Stored context is input, never authority; provenance, conflict, freshness, and material limitations remain visible.
- Durable writes require explicit owner approval of the proposed change.
- Discussing projects in the same conversation does not authorise integration, shared storage, or a dependency between them.
- The private owner workspace never enters public source, examples, evaluations, packages, logs, or retained evidence.
- One canonical skill remains the only source of strategic logic.
- Host, workspace, connector, domain, and behavioural claims do not exceed direct current proof.
- Business/venture and marketing/growth may be implemented for alpha use while remaining explicitly unvalidated and unsupported.

### Invalid Substitutes

- A repository template, documentation, or first-party enthusiasm in place of observed multi-turn behaviour.
- More conversational prose, more questions, or longer answers in place of genuinely distinct alternatives and decision-relevant exploration.
- Project or strategy vocabulary, repository location, or workspace presence in place of a material strategic decision that justifies invoking the full protocol.
- A readiness verdict, formal section structure, or strategic terminology added as ceremony to an ordinary factual, status, implementation, summarisation, simple-edit, or casual-ideation response.
- User agreement, repeated claims, polished narrative, or stored prior decisions in place of qualifying evidence.
- A single-turn prompt that narrates several turns in place of an actual fresh multi-turn interaction.
- A public fixture, copied example, or template-only check in place of authorised private-owner dogfood.
- Private workspace prose, reconstructable summaries, repository identifiers, or raw transcripts committed as public evidence.
- A host project, connector, memory store, or adapter-side prompt copy in place of the canonical skill and portable workspace contract.
- Local source files or a different package revision in place of exact runtime-package and host-source proof.
- Codex proof in place of Claude, ChatGPT, or general connector support.
- A supplied whole-person preference in place of a supported general-life, financial, medical, legal, family, or relationship domain.
- Structural checks, a small conversational review, or the retired TASK-007 attempt in place of behavioural validation for business, marketing, or interactive-strategy claims.

### Artifact Targets

- Canonical behaviour: updated core skill/reference files under `skills/strategic-advisor/`, including the invocation boundary and proportional exploration-to-checkpoint transition.
- Workspace product surface: portable Markdown templates/instructions named by the runtime allowlist plus a deterministic scaffold builder and validator.
- Evaluation authority: existing evaluation material remains excluded from model-visible packages; the retired TASK-007 attempt cannot be used as passing evidence. A new evaluation authority is required only before capability promotion and must bind the then-current source.
- Host proof: sanitised Codex trace identifying exact model, host, runtime package, workspace template, authorised source class, and observed result/write-control class.
- Public contract: bounded README, installation, architecture, and structured capability updates.
- Private dogfood: a separate private repository with no path, content, or reconstructable case data required in public artifacts.

### Parent AC Proof Ownership

- AC4: owner `Strategy Workspace child`; required evidence: Deterministic scaffold reproduction, required-field validation, and negative forbidden-content fixtures.
- AC5: owner `Strategy Workspace child`; required evidence: Provenance/freshness/conflict validation and stale-context adversarial behaviour.
- AC7: owner `Interactive Discovery child, Strategy Workspace child, Codex Owner Dogfood child, Onboarding child`; required evidence: Fresh no-workspace journey plus optional continuity journey.
- AC9: owner `Strategy Workspace child, Onboarding child`; required evidence: Runtime/install allowlist identity, deterministic builds, tests, and forbidden-content scans.

## Acceptance Criteria

- [x] AC1: Parent AC4 — two clean scaffold builds produce the exact same approved five-file Markdown set and bytes; unsafe or existing destinations fail without overwrite.
- [x] AC2: Parent AC4 and AC5 — deterministic validation accepts the canonical scaffold and rejects every required structural, provenance, leakage, secret, and private-sentinel negative fixture.
- [x] AC3: Parent AC5 — synthetic stale and conflicting records are surfaced by record ID as attention without silent selection, resolution, or epistemic upgrade.
- [x] AC4: Parent AC7 — the contract preserves no-workspace use and does not let workspace location trigger reads, invocation, writes, or integrations.
- [x] AC5: Parent AC9 — runtime and install artifacts reproduce the explicitly allowlisted workspace instructions/templates and exclude evaluation/private material.
- [x] AC6: Parent AC4, AC5, AC7, and AC9 — QA and workflow evidence remain public, synthetic, bounded, and make no unsupported promotion claim.

## Validation

- AC1: Focused builder tests compare file inventory and bytes and exercise refusal paths.
- AC2: Focused validator tests cover the canonical positive scaffold and each named negative mutation.
- AC3: Synthetic stale/conflict tests assert attention codes, IDs, and non-error validity.
- AC4: Static contract checks and review confirm optionality and zero implicit authority.
- AC5: Existing runtime/install reproduction and leakage tests run against the expanded allowlist.
- AC6: Full deterministic validation, unit suite, workflow doctor, diff review, and child evidence audit.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Define the portable workspace contract | Add the concise runtime instructions and exact five blank Markdown templates with authority, provenance, freshness, conflict, falsifier, review, and approval controls. | AC2, AC3, AC4: required structure is explicit; stale/conflicting context remains input; absence and presence grant no implicit authority. | Inspect the allowlisted files and run the focused structural tests. | Done |
| 2 | Build and validate safely | Add a dependency-free build/validate command that creates only new exact scaffolds, rejects unsafe structure/content, and emits machine-readable attention for stale/conflicting synthetic records. | AC1, AC2, AC3: deterministic bytes, fail-closed invalid cases, attention without silent resolution. | Run `python3 -m unittest tests.test_strategy_workspace -v`. | Done |
| 3 | Bind the runtime and repository checks | Add approved workspace files to the runtime allowlist and repository validator without adding any private instance, evaluation material, automatic build, or host claim. | AC4, AC5: optional use remains explicit and package inputs are exact. | Run `python3 scripts/validate.py` and runtime/install package tests. | Done |
| 4 | Validate and close the child | Run the focused and full suites, deterministic package reproductions, workflow gates, QA/code review, bounded parent-AC evidence, and retro. | AC1, AC2, AC3, AC4, AC5, AC6: all evidence passes without capability promotion. | Review `## Parent AC Evidence`, `## QA & Code Review`, and `## Retro`. | Done |

## Parent AC Evidence

- Parent AC4: `tests.test_strategy_workspace` passed 12 focused tests covering exact repeated builds, existing/symlink destination refusal, exact source layout, schema drift, record controls, and named leakage failures.
- Parent AC5: Synthetic stale and conflict rows returned `valid_with_attention` with `WORKSPACE_STALE` and `WORKSPACE_CONFLICT` record IDs and no errors; invalid provenance, freshness, approval, falsifier, and references failed closed.
- Parent AC7: `SKILL.md`, the canonical workspace reference, and README explicitly preserve no-workspace use and deny location-triggered invocation, access, writes, integration, or coupling. No workspace is built during repository validation or packaging.
- Parent AC9: `runtime-manifest.json` names the one contract reference and five templates. Two final current-source exploratory install builds produced byte-identical outputs: standalone SHA-256 `02db0e7b0e4f59cb383cb129c3f55362fe29a4b9a6128ae5469b00e7c237a0a8`, OpenAI local-marketplace SHA-256 `7c4b545dfebecdfb7d7c46e5a2eba3706e67276a06c79917de559989027027c1`, and provenance SHA-256 `19b155dfebe36272cef6589b3d7467851b193d930e719c64dc68afb6119f0a55`. These `--allow-dirty` builds prove deterministic current bytes, not release provenance or host support.
- Cross-cutting: `python3 scripts/validate.py` passed all seven scopes; `python3 scripts/build_evals.py --check` passed with 31 current cases; the final `python3 -m unittest discover -s tests -v` run passed 109 tests after approval/reference hardening.

## QA & Code Review

- Date: 2026-07-24
- Reviewed areas: owner/write authority, optional no-workspace path, least-data reading, exact scaffold inventory, destination and symlink safety, schema and reference validation, stale/conflict handling, leakage/privacy sentinels, canonical runtime allowlist, deterministic install artifacts, public claim boundaries, and workflow state.
- Acceptance mapping: AC1 passed through exact repeated-build and refusal tests; AC2 through named positive/negative validator fixtures; AC3 through machine-readable stale/conflict attention; AC4 through canonical optionality/access boundaries and absence of implicit build; AC5 through runtime allowlist checks, current-source repeated install artifacts, and package leakage tests; AC6 through final public-only diff review and workflow doctor.
- Validation evidence: `python3 -m unittest tests.test_strategy_workspace -v` passed 12 tests; `python3 -m unittest discover -s tests -v` passed 109 tests; `python3 scripts/validate.py` passed seven scopes; `python3 scripts/build_evals.py --check` passed 31 current cases; `python3 -m py_compile ...` passed; `git diff --check` passed; repeated current-source exploratory install artifacts were byte-identical with hashes recorded above; `./.project-workflow/cli/workflow doctor` reported no issues before review.
- Proof boundary: these checks prove the public contract, deterministic structure, safety controls, and package bytes. They do not prove private dogfood, host behaviour, strategic effectiveness, or supported workspace capability. No private workspace was created, read, named, or retained.
- Findings: None blocking. The validator intentionally detects bounded sentinels and exact copied logic, not all possible sensitive content; least-data owner review remains mandatory.
- Verdict: Pass.

## Retro

- Date: 2026-07-24
- Reusable lessons: A useful workspace validator must distinguish invalid structure from valid records requiring attention; staleness and declared conflict should be surfaced without pretending to resolve them. An explicit `--as-of` date keeps freshness observations reproducible. Public templates, deterministic tooling, and a private owner instance are separate artifacts and must remain separate. Epic proof-owner labels must include actual task IDs or the acceptance audit cannot attribute otherwise valid child evidence.
- Conventions or agent assets updated: `.project-workflow/guidance.md` now requires recipe-free children to use an empty `EVIDENCE.json` claim set rather than retaining generated visual-proof placeholders. `EPIC-CONTRACT.md` now binds every existing proof-owner role to its approved TASK-008/009/010/011 ID without changing coverage.
- Follow-up tasks: No new task. Existing TASK-010 owns optional private Codex dogfood and remains unstarted; existing TASK-011 owns progressive public onboarding.
- Deferrals: Private dogfood, exact host/runtime activation, and broader onboarding remain with their existing children. Behavioural or support claims remain unpromoted.
- Missed in-scope work: None.

## Notes

- Task: TASK-009
- Title: Define And Validate The Strategy Workspace Contract
- Created: 2026-07-24
