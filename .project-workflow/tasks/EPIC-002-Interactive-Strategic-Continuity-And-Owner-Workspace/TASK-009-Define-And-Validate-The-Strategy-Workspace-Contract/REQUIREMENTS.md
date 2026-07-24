# Requirements

## Summary

- Task: TASK-009
- Title: Define And Validate The Strategy Workspace Contract
- Parent AC Coverage: AC4, AC5, AC7, AC9
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

## Goal

Provide an optional, portable Markdown Strategy Workspace contract that a user can inspect, own, and validate without making a workspace a prerequisite for Strategic Advisor. The public product must ship exact blank templates and instructions, a deterministic scaffold command, and fail-closed structural validation while keeping stale or conflicting context visible as attention rather than silently treating it as authority.

## Non-Goals

- Creating, reading, naming, locating, or testing the owner's private Strategy Workspace.
- Running private Codex dogfood, host activation, or any workflow owned by TASK-010.
- Adding private, employer, client, household, connector, credential, or reconstructable case data to this repository, fixtures, logs, or evidence.
- Copying the Strategic Advisor method into workspace templates or making workspace presence trigger the skill.
- Building a database, memory service, connector integration, automatic transcript capture, migration framework, or cross-project source of truth.
- Publishing the broader progressive onboarding journey owned by TASK-011.
- Claiming workspace behaviour, a host, a domain, or strategic effectiveness is validated or supported.
- Extending or rerunning the retired TASK-007 evaluation machinery.

## Users & Context

- A first-time user needs Strategic Advisor to remain useful immediately with no workspace or repository.
- A returning user may choose durable continuity after objectives, portfolio roles, claims, or prior decisions become decision-relevant.
- A workspace owner needs every durable record to retain provenance, freshness, limitations, conflicts, falsifiers or reversal conditions, and explicit approval.
- A contributor needs to reproduce and validate the blank public scaffold without seeing private case data.
- A compatible host may receive the allowlisted templates and instructions, but workspace presence alone grants no access, invocation, write, or integration authority.

## Requirements (Outcome-Focused)

- R1. The canonical runtime contains one concise workspace-use contract and an exact allowlist of blank portable Markdown templates; the templates contain structure, field definitions, and neutral placeholders but no copied strategic logic, evaluation content, private examples, or host-specific case data.
- R2. The scaffold separates workspace authority and approved context, portfolio roles, material claims, durable decisions, and approved change history into a small fixed file set that can be read independently and chunked by decision relevance.
- R3. Durable claim records distinguish Observation, Report, Inference, Assumption, Unknown, Preference, and Forecast, and retain provenance, freshness, material limitations, conflict links, falsifiers, review dates, and explicit owner approval.
- R4. Durable decisions retain their supporting claim IDs, decision status, decision and review dates, reversal trigger, supersession links, and explicit owner approval. Proposed updates are never silently applied.
- R5. A standard-library command builds the exact blank scaffold into a new destination, refuses overwrite or path/symlink escape, and produces byte-identical files from identical source.
- R6. A standard-library validator accepts the canonical blank scaffold, fails closed on structural or safety violations, and reports stale or explicitly conflicting records as attention without silently selecting or upgrading them.
- R7. Validation rejects missing or extra files, missing required headings or table fields, malformed or duplicate record IDs, invalid epistemic statuses, missing provenance/freshness/approval controls, copied canonical logic, evaluation leakage, secret patterns, and explicit private-data sentinels.
- R8. The runtime and install allowlist includes only the approved workspace instructions/templates. Existing deterministic package builders reproduce those bytes and continue excluding evaluation and private material.
- R9. Documentation and code state that the workspace is optional input rather than authority; its absence does not block normal use, and its presence grants no automatic reads, invocation, writes, integrations, or cross-project coupling.

## Acceptance Criteria (Verifiable)

- AC1: Parent AC4 — From a clean source tree, two scaffold builds produce the same exact five-file Markdown set and byte-identical content; build attempts against an existing destination, symlinked path, or unapproved source layout fail without overwriting data.
- AC2: Parent AC4 and AC5 — The workspace validator passes the canonical blank scaffold and deterministic positive fixture, and named negative tests fail for missing/extra files, required-heading or table-schema drift, malformed/duplicate IDs, invalid origin status, absent provenance/freshness/approval fields, copied canonical logic, evaluation leakage, secret patterns, and explicit private-case sentinels.
- AC3: Parent AC5 — A synthetic stale claim and a synthetic explicit claim conflict return a valid-with-attention result naming the affected record IDs; neither record is upgraded, resolved, deleted, or silently selected. Durable claim and decision rows require owner-approval references and the applicable falsifier or reversal condition.
- AC4: Parent AC7 — The workspace contract and canonical skill state that the workspace is optional; the scaffold builder is never invoked by normal validation or installation, and no-workspace use remains a documented valid path.
- AC5: Parent AC9 — Every workspace instruction/template shipped to a model is explicitly named by `runtime-manifest.json`; repeated runtime/install builds reproduce exact bytes and existing package leakage checks continue to exclude evaluation material and private data.
- AC6: Parent AC4, AC5, AC7, and AC9 — Repository validation, unit tests, workflow doctor, QA/code review, and child evidence contain no private workspace path/content and make no host, behavioural, domain, or effectiveness promotion claim.

## Open Questions (Answer Needed)

- None. File naming and the five-file split are reversible implementation details inside the approved parent envelope.

## Decisions (Resolved)

- D1. The public scaffold contains exactly `WORKSPACE.md`, `PORTFOLIO.md`, `CLAIMS.md`, `DECISIONS.md`, and `CHANGELOG.md`.
- D2. Templates and workspace-use instructions are canonical runtime inputs under `skills/strategic-advisor/`; the repository-only builder and validator live under `scripts/`.
- D3. The validator distinguishes invalid structure from valid content requiring attention. Staleness and declared conflicts are surfaced, not silently resolved.
- D4. The blank scaffold contains no illustrative case rows. Tests use synthetic neutral records only.
- D5. The builder writes only to a new destination and never overwrites. Updating an existing workspace is an owner-controlled manual action outside this task.
- D6. No separate virtual environment or dependency installation is introduced; implementation uses the repository's declared Python standard-library boundary.

## Validation Plan

- AC1: Build twice into separate temporary directories; compare relative paths and SHA-256 values; run existing-destination and symlink-path negative tests.
- AC2: Run focused workspace unit tests containing one synthetic mutation per named rejection class, then run the repository validator and full unit suite.
- AC3: Validate synthetic stale and conflict rows and assert machine-readable attention codes and record IDs while the command still distinguishes the workspace from an invalid scaffold.
- AC4: Inspect the canonical workspace contract and `SKILL.md` references; assert no build side effect occurs during repository validation or install packaging.
- AC5: Build the current runtime package and install artifacts twice in temporary directories; compare manifests/archive bytes and scan file inventories/content for evaluation and private-data leakage.
- AC6: Review the complete diff and generated inventories, run `./.project-workflow/cli/workflow doctor`, and record bounded parent-AC evidence and a no-promotion QA verdict.
