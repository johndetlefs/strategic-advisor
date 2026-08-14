# Requirements

## Summary

- Task: EPIC-006
- Title: Technical Architecture And Evidence-Grounded Invocation
- Last updated: 2026-08-14

## Classification

This is an Epic, not a Task or Fix. The audited gap is not one bounded defect:
it requires coordinated changes to the canonical evidence protocol, a new
selective decision lens, invocation behaviour, normative and trigger evaluation
inventories, runtime packaging, current-source dogfood, public claims, and
release preparation. Those workstreams have different proof obligations and
can fail independently, while packaging and dogfood depend on the canonical and
evaluation work landing first.

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-08-14
- Approval note / source: Owner approval in Codex task on 2026-08-14 for exact R1-R15 and AC1-AC13 envelope sha256:0cdba31d13a872c09f75bc8aa087bf48955754f13a822d4ee4223aa73a616ec7
- Approved artifact identity: sha256:0cdba31d13a872c09f75bc8aa087bf48955754f13a822d4ee4223aa73a616ec7

## Goal

Make Strategic Advisor proportionately intervene in material, hard-to-reverse
technical architecture decisions from the correct inspected evidence baseline.
It should provide a selective technical/system architecture lens inside the one
canonical advisor, catch architecture decisions that emerge through ordinary
language or during implementation, remain silent for routine technical work,
and ship as an honestly bounded `implemented-not-validated` alpha capability.

## Non-Goals

- Creating a separate technical advisor, multi-agent architecture function, or
  architecture logic inside Project Workflow.
- Replacing framework, repository, platform, security, privacy, legal,
  compliance, reliability, or other specialist expertise.
- Turning every code, infrastructure, framework, data, authentication, or
  repository question into strategic analysis.
- Reopening an owner-approved technical direction merely because routine
  implementation encounters ordinary detail, setup, test, or defect work.
- Adding whole-person/personal strategy or operating-model cadence as new
  lenses without separate evidence and owner-approved requirements.
- Coupling Strategic Advisor to Strategy Workspace or Daily Checklist, copying
  either product into this repository, or adding cross-product integration.
- Reading, reproducing, sanitising in place, or committing private task
  transcripts, private Strategy Workspace content, employer/client material,
  or reconstructable owner cases.
- Calling the lens, invocation behaviour, a host, or the advisor generally
  validated or supported from written instructions, structural checks, a
  bounded smoke, package production, or owner dogfood.
- Completing the still-open comparative-effectiveness, independent-pilot, or
  general v0 release gates owned by EPIC-001.
- Publishing, merging, or finalising a public release without the separate
  authority and exact protected-main/public-download evidence those actions
  require.

## Users & Context

- A user may ask “what is the right way to structure this?” or “sense check
  this” without naming strategy, architecture, or Strategic Advisor.
- A routine implementation task can expose a newly material decision about a
  shared boundary, repository, package, service, runtime, data or authentication
  owner, migration, platform, or cross-project capability. The advisor should
  recognise that decision without converting the remainder of the task into a
  strategy ceremony.
- A user also needs direct technical explanations, status, approved
  implementation, small fixes, local setup, and ordinary test/build assistance
  without forced strategic invocation.
- Architecture proposals often arrive through framework artifacts, design
  documents, repository conventions, or specialist recommendations. Those are
  evidence to inspect and challenge, not authority to accept.
- The completed cross-thread audit found two recurring failure classes:
  rigorous reasoning from a stale or mismatched product baseline, and
  opportunistic architecture reasoning that did not consistently distinguish
  conceptual responsibility from justified technical topology.
- Current repository evidence proves six implemented-but-not-validated lenses,
  a 45-case generated normative inventory, a 28-query trigger inventory with
  only four difficult implicit positives and four difficult operational
  negatives, and a seven-scenario bounded Codex drift smoke. It does not prove
  automatic invocation, comparative improvement, or general support.

## Requirements (Outcome-Focused)

- R1. Add a proportionate evidence-baseline preflight to the canonical core.
  Before scoring, comparing, diagnosing, or recommending on a consequential
  decision, identify the exact decision object and the material product,
  repository, artifact, revision, environment, state, scope, and user journey
  being assessed. Require only the fields that could change the conclusion.
- R2. The preflight must distinguish inspected observation from user/source
  report and assumption. If a stale reference, wrong product state,
  uninspected artifact, incomparable alternative, or scope mismatch could
  overturn the conclusion, the advisor must expose the gap and inspect or
  propose the cheapest decisive check before giving a score or commitment
  recommendation. It must revise an earlier conclusion when qualifying current
  evidence changes the baseline.
- R3. Add `references/technical-architecture.md` as a selectively loaded lens
  inside `skills/strategic-advisor/`, routed by the canonical `SKILL.md`. It is
  not an independent advisor and must reuse rather than redefine claim status,
  contradiction, readiness, competing-world, and action rules.
- R4. The lens must cover material choices about system/repository/deployment
  and ownership boundaries; shared versus duplicated architecture;
  build/buy/adopt/extend/migrate; runtime, data, identity, authentication and
  authorisation ownership; coupling and cohesion; interoperability and drift;
  operational burden, reliability, observability, testability, cost and team
  capability; current versus target architecture; coexistence, migration,
  rollback, reversibility, option preservation, and future change cost.
- R5. The lens must distinguish conceptual responsibilities from packages,
  services, repositories, deployables, teams, or other topology. It must test
  the strongest simpler or more reversible rival and address architecture
  astronautics, premature extraction, framework capture, accidental
  distributed monoliths, duplicated security boundaries, prototype-to-
  production leakage, shared-data permission mistakes, proof-layer
  substitution, migration without coexistence/rollback, and elegance that
  ignores operating cost or team capability.
- R6. Project/product and technical architecture must remain complementary.
  Project/product owns intended user or operational outcome, product scope and
  sequencing; technical architecture owns the material technical shape and
  its change/operating consequences. Select one primary lens and add the other
  only when it materially changes evidence, causal risk, or action.
- R7. Architecture analysis may identify security, privacy, safety, legal,
  regulatory, financial, or specialist dependencies, but must not claim a
  substitute audit or professional determination. Framework skills, vendor
  guidance, architecture documents, and code-generation methods remain
  inspectable inputs rather than decision authority.
- R8. Strengthen selective invocation for ordinary language and latent
  decisions. Phrases such as “what is the right way to structure this?”,
  “sense check this”, “should these be shared?”, or an implementation task that
  exposes a material hard-to-reverse cross-project or system boundary may
  activate the protocol proportionately even without explicit strategy terms.
  When the decision emerges mid-task, name the decision briefly, resolve or
  bound it, then return to implementation.
- R9. Preserve strong negative controls. Factual technical explanation,
  architecture description without a pending decision, status/reporting,
  local setup, routine work inside an approved direction, simple fixes,
  mechanical refactors, and ordinary tests/builds must receive direct
  assistance unless a new material decision actually emerges.
- R10. Expand normative and trigger coverage with synthetic,
  non-reconstructable cases for evidence-baseline mismatch and update,
  conceptual responsibilities versus topology, authoritative geometry versus
  presentation ownership, build/adopt/migrate and framework-authority choices,
  data/auth/runtime ownership, portfolio and cross-project conflicts, latent
  architecture decisions, emergent implementation checkpoints, missed
  invocation, over-invocation, and routine controls. The cases may preserve the
  audited failure mechanism but must not preserve private facts or task prose.
- R11. Run a bounded current-source exact-runtime dogfood/smoke that includes
  at least three materially different architecture decisions, one stale or
  mismatched-baseline correction, ordinary-language and emergent-
  implementation activation, and strong routine negative controls. Review
  whether the lens found a material issue earlier, improved the decision rather
  than merely lengthening it, preserved product/framework boundaries, avoided
  invented topology, and stayed silent when appropriate.
- R12. Keep Strategy Workspace and Daily Checklist separate. Their operating
  cadence may supply future owner workflow evidence, but neither is a runtime
  dependency, new lens, committed case source, or integration target for this
  Epic.
- R13. Update the product contract, capability registry, architecture, README,
  installation/onboarding material, canonical runtime manifest, validation,
  evaluation inventories, and generated package expectations consistently.
  Add the technical architecture domain only as
  `implemented-not-validated`; keep `supported_capabilities` empty unless a
  separate existing promotion gate is genuinely satisfied.
- R14. Because the new lens and core guard alter allowlisted runtime bytes,
  prepare the next immutable alpha distribution in the same branch through the
  canonical release command and prove deterministic standalone Skill, local
  plugin, and ChatGPT Custom GPT package alignment. Until protected-main
  publication and fresh public verification occur under separate authority,
  the current public release remains alpha.3 and the new alpha is prepared,
  not published or supported.
- R15. Use the repository's existing standard-library implementation and
  evaluation machinery unless an approved invariant cannot be enforced
  without a new dependency. Preserve evaluation/runtime isolation and retain
  exact source/package/host identity for any behavioural observation.

## Acceptance Criteria (Verifiable)

- AC1: Canonical core instructions require the proportionate evidence-baseline
  preflight in R1-R2 and explicitly block unsupported scoring or commitment
  recommendations when a material baseline gap remains; routine direct
  assistance does not acquire a mandatory checklist.
- AC2: Matched synthetic cases prove that stale state, wrong revision,
  uninspected artifacts, mismatched scope, incomparable alternatives, and a
  later qualifying evidence update are handled without false precision or
  silent state carryover.
- AC3: `technical-architecture.md` exists under the canonical runtime, is
  allowlisted and structurally validated, contains the distinct decisions,
  evidence, mechanisms, agency/ownership, failure modes, boundaries, readiness
  implications and application checklist required by R3-R5, and introduces no
  second executable advisor.
- AC4: Matched routing cases distinguish project/product outcome decisions
  from technical architecture decisions and use the other lens secondarily
  only when it materially changes the conclusion; neither lens duplicates the
  other's contract or creates more than one secondary lens.
- AC5: Architecture cases challenge framework or vendor authority, distinguish
  conceptual responsibility from justified topology, model runtime/data/auth
  ownership and migration/rollback, and surface specialist/security
  dependencies without claiming a substitute audit or unsupported expertise.
- AC6: The trigger inventory includes ordinary-language latent architecture
  decisions, emergent implementation checkpoints, cross-project/portfolio
  conflicts, and evidence-update prompts with stable IDs and explicit slices;
  deterministic validation rejects missing, mislabelled, duplicate, or
  under-covered categories.
- AC7: Matched negative controls for factual explanation, architecture
  description, status work, approved implementation, local setup, simple fixes,
  mechanical refactors, tests and builds remain non-triggering unless a new
  material hard-to-reverse decision is present.
- AC8: The normative inventories include synthetic non-reconstructable
  regressions for every category in R10, regenerate deterministically, preserve
  evaluation/runtime isolation, and contain no private transcript, Strategy
  Workspace, Daily Checklist, employer, client, or reconstructable owner data.
- AC9: A fresh exact-runtime bounded smoke/dogfood satisfies R11 on the
  identified source/package/model/host, retains raw outputs and case-level
  verdicts, and reports every failure. A passing result is described only as a
  bounded behavioural observation, not validation, support, parity, or general
  effectiveness.
- AC10: Strategy Workspace and Daily Checklist remain absent from runtime
  dependencies and integration code; whole-person/personal strategy and
  operating cadence are not added as lenses or capability claims.
- AC11: `PRODUCT-CONTRACT.md`, `ARCHITECTURE.md`, `README.md`, `INSTALL.md`,
  `SKILL.md`, host metadata, validator declarations, runtime manifest, and
  package metadata consistently describe seven selectively loaded lenses and
  classify technical architecture and changed invocation behaviour no more
  strongly than `implemented-not-validated`.
- AC12: The canonical release preparation command binds the changed runtime to
  the next alpha identity; two clean package builds are byte-identical and
  independently verify their allowlisted runtime contents and evaluation-
  exclusion boundary. Public alpha.3 and any prepared-but-unpublished next
  alpha remain explicitly distinct.
- AC13: Focused tests, deterministic evaluation rebuild, every aggregate
  validation scope, full unit tests, current-source drift smoke, package
  verification, privacy/diff checks, Project Workflow Doctor, child QA/code
  review, and the parent acceptance audit pass or record an explicit blocking
  failure without weakening claims.

## Open Questions (Answer Needed)

- None before owner review. The owner must explicitly approve this exact
  R1-R15 / AC1-AC13 envelope before decomposition or implementation.

## Decisions (Resolved)

- D1. Classify the programme as EPIC-006 with five coordinated child
  workstreams; it is not a post-completion Fix or one bounded Task.
- D2. Add technical/system architecture as the seventh selective lens inside
  the canonical Strategic Advisor core.
- D3. Keep Project Workflow as repository process tooling and framework skills
  as implementation evidence/execution aids; neither owns the lens.
- D4. Put the evidence-baseline guard in the domain-independent core because
  stale or mismatched evidence can corrupt non-technical decisions too.
- D5. Permit ordinary-language and emergent mid-implementation invocation only
  for a material decision where reality-testing could change the action.
- D6. Preserve strong negative controls and return to implementation after a
  bounded architecture checkpoint.
- D7. Treat the audit as design evidence, not behavioural validation. Convert
  its mechanisms into synthetic non-reconstructable cases rather than copying
  task transcripts or private workspace material.
- D8. Keep whole-person/personal strategy and operating cadence as possible
  future candidates or workflows; do not add them as lenses in this Epic.
- D9. Keep Strategy Workspace and Daily Checklist independent and uncoupled.
- D10. Retain `implemented-not-validated`, pre-release, and unsupported claim
  boundaries unless stronger existing gates are directly satisfied.
- D11. Prepare the next immutable alpha because canonical runtime bytes change;
  do not infer authority to push, merge, publish, or finalise it.
- D12. Reuse the current deterministic evaluator, validator and packaging
  architecture rather than building a new evaluation system for this scope.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose |
| --- | --- | --- |
| Establish Proportionate Evidence Baseline Guard | AC1, AC2 | Add the core decision-object/state preflight and matched baseline/update regressions without forcing ceremony on direct assistance. |
| Implement Technical Architecture Lens | AC3, AC4, AC5 | Add the canonical lens, its distinct mechanisms and boundaries, and project/product complementarity. |
| Strengthen Latent And Emergent Invocation | AC6, AC7 | Extend ordinary-language and mid-implementation routing while preserving hard negative controls. |
| Expand Architecture And Baseline Evaluations | AC2, AC4, AC5, AC6, AC7, AC8 | Build deterministic synthetic normative/trigger coverage for the audited mechanisms and privacy boundaries. |
| Integrate Runtime Packaging And Bounded Dogfood | AC9, AC10, AC11, AC12, AC13 | Align claims, validators and packages; prepare the next alpha; run exact-runtime bounded smoke, QA and closeout proof. |

## Validation Plan

- AC1-AC2: Review canonical core text and run matched deterministic case
  assertions covering exact decision object, state/revision/scope identity,
  stale or absent inspection, false precision, and evidence-led revision.
- AC3-AC5: Run lens-structure validation, routing assertions, duplicate-logic
  scans, synthetic architecture cases, and human QA against the project/product
  and specialist boundaries.
- AC6-AC8: Validate stable trigger IDs, labels/slices/category minima,
  deterministic generated inventory equality, privacy/secret scans, and
  case-by-case synthetic provenance review. Passing JSON structure alone is an
  invalid substitute for behavioural observations.
- AC9: Use the runtime-target/source proof recipe. Retain the exact execution
  target, source revision, runtime package identity, model/host, isolation and
  activation method, prompts, raw outputs, case-level assertions/forbidden
  behaviours, and positive proof that the target used those bytes. A plausible
  answer, visible skill name, source-tree run, or model self-assessment is an
  invalid substitute.
- AC10-AC11: Diff and claim audits verify no cross-product dependency, private
  case data, extra lens, unsupported domain, supported capability, or divergent
  host prompt is introduced.
- AC12: Run canonical release preparation, two clean deterministic builds, the
  independent artifact verifier, archive inventory/byte comparison, and
  evaluation-leakage checks. A local ZIP does not prove public publication or
  host activation.
- AC13: Run focused and full unit tests, `build_evals.py --check`, all aggregate
  validator scopes, current-source drift smoke, compilation, package checks,
  privacy/diff hygiene, workflow Doctor, child QA/review, and the Epic
  acceptance audit. Record failures rather than relaxing the gate.
