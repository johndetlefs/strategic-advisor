# Requirements

## Summary

- Task: EPIC-004
- Title: Personal Context And Durable Strategic Continuity
- Last updated: 2026-07-26

## Backlog Source

- ID: BL-003
- Title: Holistic Strategy Scope Contract
- Type: Discovery
- Priority: High
- Status before promotion: Accepted
- Outcome: Define how Strategic Advisor can support whole-person strategic clarity and use supplied life objectives without drifting into unsupported financial, medical, legal, relationship, or generic life advice.
- Notes: Required before claiming holistic advisory support; current professional-only boundary conflicts with the desired whole-person altitude.

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-07-26
- Approval note / source: Codex task 2026-07-26: owner confirmed the corrected generic-individual personal-context plan was exactly desired and directed implementation to proceed
- Approved artifact identity: sha256:6a7f8fccd3d27a90b5ddb2577225ff5b75401042e1afc2f2691423b1ea5b30ff

## Goal

Make Strategic Advisor capable of useful, specific, durable strategy for any
individual who chooses an owner-controlled context store. Exact personal
details are first-class strategic inputs when they can change the causal
account, recommendation, or trade-off. They remain exact inside the authorised
workspace rather than being anonymised, generalised, or omitted.

Keep the reusable product generic and portable. Initial owner dogfood and later
colleague evaluation are validation cohorts, not identities or product scope
embedded in canonical instructions, public positioning, templates, or
configuration.

## Non-Goals

- Building a hosted SaaS, central user database, multi-tenant service, consent
  registry, compliance framework, telemetry system, billing system, or
  enterprise administration layer.
- Hard-coding initial users, household members, employers, projects, or private
  case details into product instructions, templates, packages, examples,
  evaluations, or current product-facing documentation.
- Copying private workspace content into this public repository, public
  evidence, install artifacts, logs, or synthetic fixtures.
- Storing every conversational utterance by default. Durable memory contains
  structured facts, objectives, constraints, claims, decisions, and
  corrections whose future decision value justifies retention.
- Treating access to personal health, financial, legal, relationship, or
  household facts as authority to diagnose, prescribe, invest, transact, or
  replace qualified professional judgment.
- Claiming general effectiveness, supported specialist advice, colleague
  adoption, or cross-host parity from structural validation or initial
  dogfood.
- Rewriting Git history solely to remove names from historical commits. Current
  product-facing material and new evidence must be generic; any history rewrite
  requires separate explicit authority.

## Users & Context

- The product user is an individual using Strategic Advisor in a personal,
  work, or shared host environment and choosing whether and how durable context
  may be stored.
- Personal users need exact names, ages, dates, relationships, amounts,
  locations, goals, health context, financial position, projects, capabilities,
  preferences, and constraints preserved when those details materially affect
  strategy.
- Work or shared-account users need the same specificity inside an explicitly
  bounded set of domains, or a session-only mode that performs no durable
  capture.
- Initial owner dogfood proves usefulness and failure modes for the first two
  private users. Selected colleagues may later test transferability using the
  same generic package and their own separately controlled workspaces.
- Maintainers need a strict boundary between generic public product source and
  exact private instance data without using anonymisation as a substitute for
  that architecture.

## Requirements (Outcome-Focused)

- R1. Product mission, target-user, README, installation, capability, and
  architecture language define a portable advisor for individuals. Initial
  dogfood identities and household relationships do not define the product or
  appear in current product-facing setup paths.
- R2. Whole-person context is a core input to strategy. The advisor may use
  exact personal, household, health, financial, legal, relationship, and life
  circumstances whenever they materially change an otherwise in-scope
  decision, while keeping specialist advice boundaries explicit.
- R3. Every workspace declares exactly one generic context mode:
  `durable-full`, `durable-bounded`, or `session-only`. The mode controls
  retention, not whether exact details may be used in the current analysis.
- R4. `durable-full` permits exact decision-relevant personal details and
  standing maintenance authority inside the named workspace.
  `durable-bounded` permits exact durable details only in declared domains.
  `session-only` permits contextual use but no durable capture.
- R5. Read authority, durable-write authority, external-action authority,
  disclosure authority, and cross-workspace authority remain separate.
  Workspace maintenance never implies messages, transactions, file changes
  outside the workspace, publication, or sharing with another person.
- R6. The portable workspace provides compact generic indexes for workspace
  policy, profile, objectives, portfolio, contexts, material claims, durable
  decisions, and change history, plus optional linked `projects/` and
  `contexts/` detail files. It preserves exact names, values, ages, dates, and
  relationships.
- R7. Durable records preserve origin status, provenance, freshness, material
  limitations, corrections, and supersession. Current evidence may challenge a
  stored record; the advisor must not silently alter an exact fact merely to
  make it less identifying.
- R8. Default durable capture stores the structured fact, objective,
  constraint, claim, or decision rather than a raw transcript. A user may
  explicitly retain source material, but credentials and secret-like values
  remain prohibited from the portable workspace.
- R9. Workspace tooling deterministically builds and validates the generic
  scaffold, supports a reviewed migration from the existing five-file schema,
  allows declared owner extensions, and detects malformed policy, invalid
  authority, broken indexes, secrets, evaluation leakage, or copied strategic
  logic without rejecting ordinary personal content.
- R10. Canonical runtime behaviour retrieves decision-relevant context at its
  useful specificity, asks for a missing detail when different values could
  materially change the answer, and avoids both unnecessary anonymisation and
  irrelevant personal-detail recital.
- R11. Under standing authority the runtime may maintain approved workspace
  record classes with an auditable change entry. Corrections, deletions,
  disclosure, cross-workspace copying, and changes outside the declared mode
  remain explicit user decisions.
- R12. Health, financial, legal, relationship, family, and household facts may
  shape strategy. Domain competence and consequence determine the advice
  boundary: the advisor may frame goals, trade-offs, research, monitoring,
  experiments, and professional questions, but may not infer that stored facts
  confer specialist authority.
- R13. Synthetic evaluation covers specificity fidelity, causal relevance,
  non-relevance, all three context modes, durable capture, retrieval,
  correction, deletion, staleness, isolation, disclosure, and specialist-domain
  boundaries. An evaluation fails if it unnecessarily replaces a material
  exact detail with a generic abstraction.
- R14. Runtime and install artifacts remain deterministic and generic. They
  include the context contract and blank templates but no private instance
  content, person-specific configuration, evaluation answer keys, or host-side
  prompt forks.
- R15. Initial private dogfood and later colleague testing use separately
  controlled workspaces. Public evidence retains exact source/runtime identity
  and bounded behaviour/result classes, not private workspace prose or
  reconstructable case facts.

## Acceptance Criteria (Verifiable)

- AC1: Constitution, canonical skill description, README, installation,
  architecture, and product contract consistently define a portable advisor for
  individuals and no longer define initial named users or professional-only
  scope as the product.
- AC2: Product and runtime contracts explicitly distinguish exact personal
  context use from specialist advice authority, public disclosure, and external
  action.
- AC3: A workspace must validate under exactly one of `durable-full`,
  `durable-bounded`, or `session-only`; malformed, missing, or contradictory
  policy fails with an actionable diagnostic.
- AC4: Mode and authority tests prove exact context is retained in
  `durable-full`, retained only within declared domains in `durable-bounded`,
  never durably captured in `session-only`, and never silently disclosed,
  copied, or used as external-action authority.
- AC5: A deterministic generic scaffold contains the approved compact personal
  strategy indexes and supports exact personal values plus declared linked
  project/context details without requiring anonymisation.
- AC6: A reviewed migration path upgrades the existing five-file workspace
  contract without overwriting an existing workspace, losing valid records, or
  copying private content into the public repository; validator negative
  fixtures still reject secrets, evaluation leakage, and copied strategic
  logic.
- AC7: Canonical runtime instructions require decision-relevant specificity,
  structured durable capture under standing authority, provenance/freshness,
  correction, and supersession while rejecting raw-transcript accumulation as
  the default memory mechanism.
- AC8: Matched synthetic cases show that changing a causally relevant exact
  detail can change the recommendation, while irrelevant personal facts neither
  activate the protocol nor appear gratuitously in the answer.
- AC9: Synthetic mode, persistence, correction, deletion, isolation,
  disclosure, and stale-context cases pass against the exact current runtime;
  any relevant hard-gate failure blocks a behavioural pass claim.
- AC10: Health, financial, legal, relationship, family, and household context
  cases use exact supplied facts for bounded strategy while refusing unsupported
  diagnosis, prescription, transaction, or professional-authority claims.
- AC11: Repeated runtime and install builds produce identical generic artifacts,
  existing aggregate privacy/secret/evaluation-leakage checks pass, and current
  product-facing artifacts contain no initial-user-specific positioning or
  private instance content.
- AC12: One fresh generic first-use journey creates or selects a mode, records
  an exact durable fact when authorised, retrieves it in a later decision, and
  corrects or deletes it without public or cross-workspace leakage. Private
  owner dogfood may strengthen the result but public synthetic evidence is not a
  substitute for a claimed real-use outcome.

## Open Questions (Answer Needed)

- None. The owner explicitly approved the preceding implementation plan and
  clarified that initial users are the first validation cohort, not the product
  definition.

## Decisions (Resolved)

- D1. Build for general individual use; validate first with the initial private
  users and then selected colleagues.
- D2. Store exact durable, decision-relevant details. Do not anonymise them
  inside an authorised workspace.
- D3. Keep the reusable public product and every private user workspace as
  separate data planes.
- D4. Provide three small context modes rather than a general compliance or
  policy framework.
- D5. Recommend `durable-full` for personal user-controlled environments;
  `durable-bounded` and `session-only` remain available for work/shared
  environments or user preference.
- D6. Standing authority applies only to declared workspace maintenance.
  Disclosure, external action, and cross-workspace copying remain separately
  authorised.
- D7. Store structured durable records rather than every raw conversational
  utterance by default.
- D8. Allow health, financial, legal, relationship, family, and household facts
  to shape strategy while keeping specialist competence boundaries.
- D9. Current product-facing material becomes generic. Historical Git history
  is not rewritten in this Epic.
- D10. No hosted service, database, connector, telemetry, authentication, or
  dependency is added.
- D11. Existing completed Epic evidence remains historical. This Epic
  supersedes conflicting product behaviour and positioning rather than editing
  prior acceptance records to imply they proved the new contract.

## Discovery Resolution

- Question: How can Strategic Advisor preserve and use exact personal context
  for useful strategy without embedding private instance data or initial users
  into the reusable product?
- Decision enabled: Promote the accepted holistic-scope discovery into the
  five-child implementation programme defined below.
- Boundary: Resolve the product contract, portable workspace, runtime
  behaviour, deterministic packaging, and bounded validation in this Epic; do
  not build hosted or multi-tenant infrastructure.
- Output artifact: This owner-approved `REQUIREMENTS.md`,
  `EPIC-CONTRACT.md`, and the decomposition generated from `Proposed Child
  Work`.
- Validation: `epic ready` must accept the exact requirements and contract;
  every parent AC must map to approved child work and later pass child QA or an
  explicit owner-approved deferral before closeout.

## Validation Plan

- AC1-AC2: Compare Constitution, canonical runtime, README, installation,
  architecture, product contract, and current host-facing guidance; fail
  professional-only or named-initial-user product positioning.
- AC3-AC6: Extend workspace builder, validator, fixtures, and unit tests; build
  repeatedly; validate all modes; exercise safe copy-based migration and
  negative authority, secret, leakage, schema, link, and overwrite cases.
- AC7-AC10: Add matched synthetic specificity and context-policy cases bound to
  the exact runtime; retain case authority and machine-verifiable hard-gate
  results without adding private case material.
- AC11: Build runtime/install artifacts twice, compare identities and
  inventories, run aggregate validation, secret/privacy scans, unit tests, and
  diff checks.
- AC12: Run a fresh synthetic end-to-end workspace journey against the exact
  current runtime/tooling. Any later private dogfood records only bounded
  technical and result classes in this repository.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose |
| --- | --- | --- |
| Correct The Personal-Context Product Contract | AC1, AC2, AC11 | Make the product generic, whole-person, and specific while removing initial-user and professional-only product positioning. |
| Implement Configurable Context And Authority Policy | AC2, AC3, AC4 | Define and validate the three context modes plus separate read, write, action, disclosure, and cross-workspace authority. |
| Expand The Strategy Workspace And Migration Contract | AC5, AC6, AC11 | Deliver the generic personal-strategy schema, safe migration path, extension rules, and deterministic validation. |
| Implement Decision-Relevant Specificity And Durable Capture | AC7, AC8, AC10 | Correct canonical behaviour so exact personal facts are retrieved, used, maintained, corrected, and bounded without anonymisation or irrelevant recital. |
| Validate Specificity, Isolation And Transferability | AC4, AC8, AC9, AC10, AC11, AC12 | Bind synthetic and fresh end-to-end proof to the exact runtime, modes, packages, and generic first-use journey. |
