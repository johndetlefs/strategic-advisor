# Requirements

## Summary

- Task: EPIC-002
- Title: Interactive Strategic Continuity And Owner Workspace
- Last updated: 2026-07-23

## Owner Approval

- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Not approved
- Approval date: Not approved
- Approval note / source: Not approved
- Approved artifact identity: Not approved

## Backlog Source

- ID: BL-001
- Title: Interactive Strategic Continuity And Owner Workspace
- Type: Epic Candidate
- Priority: High
- Status before promotion: Proposed
- Outcome: Strategic Advisor conducts active multi-turn exploration, calibrates decision altitude, preserves reality through a final evidence reset, and can use an owner-approved private Strategy Workspace in Codex without making repository setup mandatory.
- Notes: Immediate owner-directed programme: working-position dialogue, question reframing, portfolio roles, private workspace scaffold, Codex dogfood, freshness/permission controls, and multi-turn preference-capture evaluation.

## Goal

Make Strategic Advisor useful as an ongoing, reality-constrained collaborator: it should widen a bounded question when a higher decision altitude could change the answer, actively explore alternatives with the user, reconverge through an evidence-only reality reset, and optionally use a private, owner-controlled Strategy Workspace for continuity in Codex.

## Non-Goals

- Making a repository mandatory before a user receives first value.
- Storing private owner context in this public product repository, install artifacts, examples, evaluations, or retained public evidence.
- Automatically writing conversation content into durable context without explicit owner review and approval.
- Treating stored preferences, prior conclusions, or narrative coherence as current evidence.
- Claiming general-life, financial, medical, legal, family, relationship, business, marketing, or growth advice is supported through this Epic.
- Implementing the business and marketing lenses tracked separately in `BL-002`.
- Claiming Claude, ChatGPT, or external-workspace support; those paths remain separately gated by `BL-005` and host-specific evidence.
- Building a central memory service, custom database, or broad connector layer.

## Users & Context

- A first-time user needs useful strategic analysis without setup friction or a repository prerequisite.
- A returning user may want an inspectable, portable record of approved objectives, project roles, material claims, decisions, falsifiers, and review conditions.
- A user can ask a valid tactical question whose proposed intervention is nevertheless at the wrong decision altitude; the advisor must not answer it in isolation when stepping up could materially change the recommendation.
- A user can also ask a small reversible question where portfolio or whole-person analysis would add noise; the advisor must operate at the minimum sufficient altitude.
- The owner will dogfood the first private Strategy Workspace in Codex while both the workspace contract and Strategic Advisor remain experimental.
- Contributors need sanitised evidence that the exact canonical/runtime skill and workspace scaffold were used without receiving the owner's private workspace contents.

## Requirements (Outcome-Focused)

- R1. Initial findings are presented as a current working position when material exploration remains, not as conversational closure disguised as certainty.
- R2. The advisor can conduct an active discovery loop that invites uncued user alternatives, contributes genuinely distinct pathways, tests load-bearing assumptions, and avoids cosmetic option lists.
- R3. The advisor operates at the minimum sufficient altitude: begin with the requested task or project question, step up to project or portfolio context only when it could change the decision, and return to a bounded next move.
- R4. Before reconverging, the advisor performs an inspectable reality reset that distinguishes new evidence from new ideas, preferences, repetition, confidence, and agreement; readiness changes only when qualifying evidence, scope, or constraints change.
- R5. The advisor remains invariant to opposite user preferences on materially identical facts and surfaces the strongest live rival without preserving rejected alternatives for symmetry.
- R6. Strategic Advisor remains fully useful without a Strategy Workspace and offers durable continuity only after continuity has decision value or the user asks for it.
- R7. A portable Markdown Strategy Workspace scaffold records approved context, portfolio roles, durable decisions, provenance, freshness, falsifiers, and review conditions without copying canonical strategic logic.
- R8. Workspace access is least-data and case-scoped. Stored content is input rather than authority, stale context is surfaced, and any proposed durable update requires explicit owner approval before writing.
- R9. A private owner workspace can be created and used in Codex with an exact skill/runtime identity and a retained sanitised activation/source trace; no private workspace content enters this repository or public evidence.
- R10. Multi-turn evaluation tests exploration quality, altitude calibration, preference capture, unsupported claim upgrades, stale-context capture, failure to revise, and return from broad exploration to a decision-useful next move.
- R11. Public documentation presents a progressive onboarding path: immediate one-decision use first, optional workspace-backed continuity second, with precise host and maturity boundaries.
- R12. Product, install, runtime-manifest, validation, and capability claims remain deterministic and fail closed when workspace, host, or behavioural proof is absent.

## Acceptance Criteria (Verifiable)

- AC1: In multi-turn cases with unresolved option space, the advisor states a working position, conducts active exploration, and later reconverges; in bounded low-consequence cases it answers without unnecessary altitude escalation.
- AC2: Adversarial cases demonstrate that altitude changes occur only when the higher-level objective, constraint, project role, or opportunity cost could materially change readiness or action, and that every escalated case returns to a bounded decision or decisive validation step.
- AC3: Matched opposite-preference and repeated-assertion cases retain the same diagnosis on the same facts; the final reality reset explicitly identifies the evidence delta and does not upgrade readiness from conversational agreement alone.
- AC4: A deterministic, allowlisted Strategy Workspace scaffold contains only the approved portable files and required headings, excludes strategic-logic copies and evaluation material, and can be validated from a clean checkout.
- AC5: The workspace contract distinguishes user-approved durable context from reports, inferences, assumptions, forecasts, unknowns, and prior decisions; stale or conflicting content is surfaced rather than silently selected.
- AC6: Codex can load the exact identified Strategic Advisor runtime and the owner-authorised private workspace in a fresh context, answer one bounded portfolio/project question, and propose rather than silently write a durable update; retained public evidence contains only sanitised identities, result class, and pass/fail observations.
- AC7: Strategic Advisor continues to work in a fresh context with no workspace present, and onboarding does not require repository creation before the first substantive answer.
- AC8: The frozen multi-turn evaluation includes required and forbidden assertions for active discovery, genuine alternatives, minimum-sufficient altitude, evidence-only readiness change, preference invariance, stale-context handling, and convergence; no skilled result may pass with a relevant hard-gate failure.
- AC9: Runtime and install artifacts contain the approved workspace instructions/templates only when named by the runtime allowlist, reproduce deterministically, and contain no private owner data, host-specific strategic copy, or evaluation leakage.
- AC10: README, installation guidance, product contract, and capability registry describe the workspace and Codex dogfood state no more strongly than current retained evidence permits; unsupported hosts and general-life, business, marketing, and financial domains remain explicitly unpromoted.

## Open Questions (Answer Needed)

- None for the proposed requirements envelope. Workspace naming and exact file layout are reversible implementation details to be resolved during planning without changing these outcomes or proof obligations.

## Decisions (Resolved)

- D1. The method is not repository-bound; the continuity layer is an optional workspace-aware capability.
- D2. Codex is the first target host for owner dogfood. Other hosts require their own later proof.
- D3. The private owner repository is real operational context but is not public product evidence; only sanitised activation and behaviour observations may be retained here.
- D4. The workspace is user-owned and portable. Host projects and adapters are clients, not canonical sources of truth.
- D5. Start with portable Markdown and Git history. Do not add a database, memory service, or complex schema before dogfood demonstrates a stable invariant.
- D6. Conversation transcripts are not canonical context. Only owner-approved distilled claims, decisions, and review conditions may become durable.
- D7. This Epic may use supplied whole-person objectives as context for bounded professional/project decisions, but broader holistic advisory scope remains owned by `BL-003`.
- D8. Contextual adjacency does not create product coupling. Cross-repository integration, shared storage, or source-of-truth relationships require explicit owner direction.

## Validation Plan

- AC1-AC3: Run frozen multi-turn synthetic cases in fresh contexts with byte-identical matched facts, opposite preferences, repeated user pressure, bounded tactical controls, and higher-altitude triggers. Retain raw outputs, assertion grades, hard-gate verdicts, and evidence-delta findings.
- AC4-AC5: Build the workspace scaffold twice from a clean checkout, compare byte identities, validate required headings/status fields, and run negative fixtures for copied strategic logic, evaluation leakage, missing freshness, malformed provenance, secrets, and private-data sentinels.
- AC6: In a fresh Codex context, retain the exact model/host, runtime-package identity, workspace template identity, authorised source path class, discovery/selection trace when exposed, tool/result class, and explicit-write-control observation. Retain no private workspace prose, project names, identifiers, or reconstructable facts.
- AC7: Run the same supported professional case without a workspace and verify that absence produces labeled unknowns or bounded questions rather than setup refusal.
- AC8: Freeze cases, prompts, assertions, hard gates, context-turn rules, and aggregation before generating candidate outputs. Treat missing turns, reused contexts, or leaked expected properties as invalid rather than incomplete success.
- AC9: Run deterministic runtime/install builders, structural validators, unit tests, forbidden-content scans, and clean-checkout reproduction against exact source revisions.
- AC10: Compare every public workspace/host/domain claim with `PRODUCT-CONTRACT.md`, structured capability state, current evidence, and exact host proof; fail on stronger unsupported language.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose |
| --- | --- | --- |
| Implement Interactive Discovery And Altitude Calibration | AC1, AC2, AC3, AC7 | Add the working-position, active exploration, minimum-sufficient-altitude, evidence-delta, and reconvergence behaviour without making ordinary tactical use verbose. |
| Define And Validate The Strategy Workspace Contract | AC4, AC5, AC7, AC9 | Create the optional portable scaffold, user-approval lifecycle, provenance/freshness contract, deterministic builder, and negative validation fixtures. |
| Prove Private Codex Owner Dogfood | AC6, AC7, AC10 | Create the private owner workspace, prove exact Codex/runtime/workspace use with sanitised retained evidence, and keep private content outside the public repository. |
| Build Multi-Turn Reality Guardrail Evaluation | AC1, AC2, AC3, AC5, AC8 | Add precommitted multi-turn cases and fail-closed assertions for exploration, altitude, preference invariance, stale context, revision, and convergence. |
| Publish Progressive Workspace Onboarding | AC7, AC9, AC10 | Document one-decision quick use and optional continuity, update bounded capability claims, and reproduce install artifacts without overstating host or domain support. |
