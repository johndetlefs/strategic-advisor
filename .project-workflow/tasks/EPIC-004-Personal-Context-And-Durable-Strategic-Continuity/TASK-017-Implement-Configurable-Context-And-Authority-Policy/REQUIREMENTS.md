# Requirements

## Summary

- Task: TASK-017
- Title: Implement Configurable Context And Authority Policy
- Parent AC Coverage: AC2, AC3, AC4
- Last updated: 2026-07-26

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

- The reusable product is generic and portable; private instance data supplies
- Exact decision-relevant details remain exact inside an authorised workspace.
- Context mode controls retention, not whether supplied details may inform the
- Stored context is attributable input, not unquestioned truth or instruction.
- Provenance, freshness, limitations, conflicts, corrections, and supersession
- Structured durable facts are preferred to raw transcripts for memory quality
- Read, durable-write, external-action, disclosure, and cross-workspace
- No workspace access authorises messages, transactions, publication,
- Health, financial, legal, relationship, family, and household facts may shape
- Credentials, secret-like values, evaluation authority, and copied canonical
- Private user workspaces never enter public source, packages, evaluations,
- One canonical skill remains the only source of strategic logic.
- Structural, behavioural, host, real-use, support, and effectiveness claims

### Invalid Substitutes

- Initial owner preference, fluent output, or repository prose in place of
- A named initial user or household presented as the generic product target.
- Anonymising or omitting a causally relevant authorised fact in place of
- Raw transcript accumulation in place of structured durable context.
- A personal account label in place of a declared workspace mode and authority
- Workspace read access in place of durable-write, disclosure, external-action,
- Storing health, financial, legal, relationship, family, or household facts
- Static schema tests in place of exact-runtime specificity and relevance
- A public synthetic case in place of a claimed private owner-use outcome.
- One user's workspace, account, or host proof in place of another's.
- Private workspace prose, reconstructable summaries, identifiers, or raw
- A host-specific prompt copy in place of the canonical skill.
- A successful build in place of package identity, source binding, or observed

### Artifact Targets

- Stable product contract and current generic public positioning.
- Canonical context-mode, authority, specificity, durable-capture, correction,
- Generic portable workspace templates with compact profile, objective,
- Deterministic builder, validator, and reviewed migration tool.
- Synthetic specificity, relevance, mode, persistence, correction, deletion,
- Exact-runtime result artifacts for the bounded behavioural claims.
- Deterministic generic runtime/install packages with no private instance data.
- Fresh generic first-use proof; separately authorised private dogfood may

### Parent AC Proof Ownership

- AC2: owner `Correct The Personal-Context Product Contract; Implement Configurable Context And Authority Policy`; required evidence: Explicit context-versus-advice/action/disclosure contract across product and runtime.
- AC3: owner `Implement Configurable Context And Authority Policy`; required evidence: Deterministic positive and negative validation for exactly three modes.
- AC4: owner `Implement Configurable Context And Authority Policy; Validate Specificity, Isolation And Transferability`; required evidence: Mode and authority matrix tests plus exact-runtime isolation/disclosure results.

## Goal

Give every workspace one small, explicit retention mode and authority contract
so exact context can be used without confusing personal-account assumptions,
workspace maintenance, disclosure, external action, or cross-workspace access.

## Non-Goals

- General-purpose policy engines, per-field ACLs, hosted identity, telemetry, or
  enterprise administration.
- Implementing the expanded workspace schema or migration owned by TASK-018.
- Claiming mode behaviour passed before TASK-020 exact-runtime validation.

## Users & Context

- Personal users need durable exact context with low-friction standing
  maintenance authority.
- Work or shared-account users need bounded or session-only retention without
  losing exact context during the current analysis.

## Requirements (Outcome-Focused)

- R1. Canonical runtime documentation defines exactly `durable-full`,
  `durable-bounded`, and `session-only`.
- R2. Every mode permits exact supplied details in current analysis; modes
  differ only in durable retention and maintenance authority.
- R3. Bounded mode declares allowed durable domains explicitly and rejects an
  empty or malformed domain boundary.
- R4. Read, durable-write, action, disclosure, and cross-workspace authorities
  are independently declared and never inferred from account type.
- R5. Standing write authority permits structured maintenance only inside the
  declared workspace and mode; correction, deletion, disclosure, and
  cross-workspace copying remain explicit decisions.

## Acceptance Criteria (Verifiable)

- AC1: Covers parent AC2 — the canonical policy reference separates context
  use, retention, maintenance, specialist advice, disclosure, and action.
- AC2: Covers parent AC3 — exactly three modes are normative and malformed,
  missing, contradictory, or empty bounded policy is invalid.
- AC3: Covers parent AC4 — an authority matrix proves no mode implies external
  action, disclosure, or cross-workspace access and no mode anonymises current
  analysis.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- D1. Use three enumerated modes in a readable Markdown policy block.
- D2. Recommend `durable-full` for personal user-controlled environments
  without silently selecting it for an existing workspace.
- D3. Account type is advisory context, not authority.

## Validation Plan

- AC1: Review the canonical context-policy and strategy-workspace references.
- AC2-AC3: Add positive and negative policy fixtures and deterministic
  validation; TASK-020 owns exact-runtime behavioural proof.
