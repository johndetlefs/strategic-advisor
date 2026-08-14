# Epic Contract

## Summary

- Epic: EPIC-006
- Title: Technical Architecture And Evidence-Grounded Invocation
- Last updated: 2026-08-14

## Sources of Truth

- Owner-approved `REQUIREMENTS.md` for the exact R1-R15 / AC1-AC13 authority
  envelope.
- `skills/strategic-advisor/SKILL.md` and its allowlisted references for the
  one canonical executable method and selective-routing boundary.
- `PRODUCT-CONTRACT.md` for capability states and claim-promotion rules.
- `ARCHITECTURE.md` for canonical core/lens, host/package and evaluation-plane
  boundaries.
- `skills/strategic-advisor/runtime-manifest.json` for the exact model-visible
  runtime allowlist.
- `skills/strategic-advisor/evals/` plus `scripts/build_evals.py`,
  `scripts/validate.py`, `scripts/drift_smoke.py` and
  `scripts/evaluation_harness.py` for normative cases, trigger definitions,
  deterministic inventory, bounded smoke and proof limits.
- `distribution.json`, `scripts/release_state.py` and
  `scripts/build_install_artifacts.py` for prepared/current release identity
  and deterministic package authority.
- The owner-directed 2026-08-14 cross-thread audit conclusions as design input
  only. Private transcripts and Strategy Workspace content are not repository
  sources of truth and must not be copied here.
- Repository `AGENTS.md`, `.project-workflow/guidance.md`, Constitution, and
  approved child requirements for delivery and proof rules.

## Invalid Substitutes

- Documentation, static validation, unit tests, model self-assessment, owner
  preference, or a plausible answer in place of observed behaviour.
- A bounded smoke or dogfood result in place of comparative evaluation,
  independent human validation, a supported capability, or general host/domain
  proof.
- A source-tree invocation, visible skill name, or matching prose in place of
  exact runtime-target/source and activation evidence.
- A package build, archive listing, workflow log, or release-page entry in
  place of exact package bytes or fresh public verification.
- A stale screenshot, obsolete prototype, demonstration state, uninspected
  artifact, mismatched revision/environment, or incomparable scope in place of
  the current decision baseline.
- A framework artifact, vendor recommendation, architecture diagram, passing
  build, or test result in place of evidence that the proposed technical shape
  causes the intended outcome and is operable in the target environment.
- Tests/builds in place of rendered, runtime, usability, security, operational,
  migration, or owner evidence when those higher proof layers are claimed.
- Private task transcripts, Strategy Workspace content, Daily Checklist data,
  renamed private cases, or reconstructable owner details in place of
  synthetic non-reconstructable regression evidence.
- Strategy Workspace cadence, Daily Checklist integration, or a separate
  technical advisor in place of the approved canonical-lens implementation.

## Invariants

- `skills/strategic-advisor/` remains the only executable source of Strategic
  Advisor logic; technical architecture is one selective lens, not another
  advisor or a Project Workflow capability.
- The evidence-baseline guard remains domain-independent and proportionate;
  it must prevent wrong-baseline conclusions without forcing ceremony on
  routine direct assistance.
- Project/product and technical architecture retain distinct ownership; one is
  primary and at most one materially relevant secondary lens is loaded.
- Conceptual responsibilities do not automatically become packages, services,
  repositories, deployables, teams, or other topology.
- Frameworks, vendors, code, documents, connectors and stored context are
  evidence inputs, never truth, consent, decision authority, or specialist
  certification.
- Specialist security, privacy, legal, financial, safety, reliability and
  other professional boundaries remain explicit.
- Evaluation authority, expected answers, private material and prior outputs
  never enter the model-visible runtime or generated install packages.
- Only synthetic, public or irreversibly sanitised cases may be committed; no
  private transcript, workspace, employer/client or reconstructable owner data
  is permitted.
- Strategy Workspace and Daily Checklist remain separate products/data planes
  with no runtime dependency or integration added by this Epic.
- Whole-person/personal strategy and operating cadence are not added as lenses
  or promoted capabilities in this Epic.
- Capability and release language remains no stronger than exact evidence.
  Technical architecture and changed invocation remain
  `implemented-not-validated`; package readiness is not activation, support,
  adoption, parity or effectiveness.
- Any accepted allowlisted runtime-byte change prepares the next immutable
  distribution in the same branch. Prepared, published and fresh-publicly-
  verified states remain separate, and external publication/finalisation
  requires its own authority and exact evidence.
- No new dependency or automation is added unless it enforces an approved
  invariant or proof obligation that current standard-library machinery cannot
  enforce.

## Artifact Targets

- Canonical runtime: `skills/strategic-advisor/SKILL.md`,
  `references/evidence.md`, `references/conversational-strategy.md`, new
  `references/technical-architecture.md`, and only other directly affected
  allowlisted references.
- Runtime/package declarations: `skills/strategic-advisor/runtime-manifest.json`,
  `skills/strategic-advisor/agents/openai.yaml`, `distribution.json`, generated
  install-artifact provenance and exact package inventories.
- Evaluation authority: `skills/strategic-advisor/evals/core_cases.json`,
  `lens_cases.json`, `eval_queries.json`, generated `evals.json`, bounded smoke
  cases/results, and the smallest necessary validator/builder/test updates.
- Public contract: `PRODUCT-CONTRACT.md`, `ARCHITECTURE.md`, `README.md`,
  `INSTALL.md`, and only directly affected contributor/security material.
- Retained proof: child `EVIDENCE.json`, synthetic raw bounded-smoke artifacts
  with exact source/package/host identity, deterministic package comparison,
  test/validator output, QA review, and parent acceptance audit.
- Workflow: EPIC-006 requirements, contract, decomposition, child task
  artifacts, tracker, acceptance map/audit, deferrals/amendments if required,
  and retro.

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | TASK-026 | Canonical core diff plus matched baseline/direct-assistance assertions and QA verdict. |
| AC2 | TASK-026, TASK-029 | Baseline/update normative cases, generated-inventory proof, case results and false-precision negative review. |
| AC3 | TASK-027 | Canonical lens, runtime allowlist, lens validator and duplicate-advisor scan. |
| AC4 | TASK-027, TASK-029 | Matched project-product/architecture routing cases and case-level verdicts. |
| AC5 | TASK-027, TASK-029 | Architecture mechanism, ownership, migration, framework and specialist-boundary cases with QA evidence. |
| AC6 | TASK-028, TASK-029 | Stable labelled trigger inventory, category validator negatives and difficult-positive coverage. |
| AC7 | TASK-028, TASK-029 | Matched operational negative controls, over-invocation assertions and case-level verdicts. |
| AC8 | TASK-029 | Synthetic provenance review, privacy scan, deterministic rebuild and runtime-exclusion proof. |
| AC9 | TASK-030 | Passing runtime-target/source claims, raw bounded-smoke outputs, exact identity and honest result boundary. |
| AC10 | TASK-030 | Runtime/dependency/capability diff proving no cross-product coupling or extra lens. |
| AC11 | TASK-030 | Cross-artifact claim matrix, seven-lens declarations, capability registry and validator pass. |
| AC12 | TASK-030 | Canonical release preparation, exact runtime identity, two byte-identical builds and independent verifier output. |
| AC13 | TASK-030 | Focused/full validation, current-source drift smoke, package/privacy/diff checks, Doctor, child QA and parent audit. |
