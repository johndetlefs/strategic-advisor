## User Story

As an early-alpha user, I want the architecture lens and baseline guard in the
same exact packaged Strategic Advisor with honest evidence boundaries, so that
I can dogfood current behaviour without mistaking implementation for support.

## Parent AC Coverage

- AC9, AC10, AC11, AC12, AC13

## Child Charter

### Inherited Invariants

- `skills/strategic-advisor/` remains the only executable source of Strategic
- The evidence-baseline guard remains domain-independent and proportionate;
- Project/product and technical architecture retain distinct ownership; one is
- Conceptual responsibilities do not automatically become packages, services,
- Frameworks, vendors, code, documents, connectors and stored context are
- Specialist security, privacy, legal, financial, safety, reliability and
- Evaluation authority, expected answers, private material and prior outputs
- Only synthetic, public or irreversibly sanitised cases may be committed; no
- Strategy Workspace and Daily Checklist remain separate products/data planes
- Whole-person/personal strategy and operating cadence are not added as lenses
- Capability and release language remains no stronger than exact evidence.
- Any accepted allowlisted runtime-byte change prepares the next immutable
- No new dependency or automation is added unless it enforces an approved

### Invalid Substitutes

- Documentation, static validation, unit tests, model self-assessment, owner
- A bounded smoke or dogfood result in place of comparative evaluation,
- A source-tree invocation, visible skill name, or matching prose in place of
- A package build, archive listing, workflow log, or release-page entry in
- A stale screenshot, obsolete prototype, demonstration state, uninspected
- A framework artifact, vendor recommendation, architecture diagram, passing
- Tests/builds in place of rendered, runtime, usability, security, operational,
- Private task transcripts, Strategy Workspace content, Daily Checklist data,
- Strategy Workspace cadence, Daily Checklist integration, or a separate

### Artifact Targets

- Canonical runtime: `skills/strategic-advisor/SKILL.md`,
- Runtime/package declarations: `skills/strategic-advisor/runtime-manifest.json`,
- Evaluation authority: `skills/strategic-advisor/evals/core_cases.json`,
- Public contract: `PRODUCT-CONTRACT.md`, `ARCHITECTURE.md`, `README.md`,
- Retained proof: child `EVIDENCE.json`, synthetic raw bounded-smoke artifacts
- Workflow: EPIC-006 requirements, contract, decomposition, child task

### Parent AC Proof Ownership

- AC9: owner `TASK-030`; required evidence: Passing runtime-target/source claims, raw bounded-smoke outputs, exact identity and honest result boundary.
- AC10: owner `TASK-030`; required evidence: Runtime/dependency/capability diff proving no cross-product coupling or extra lens.
- AC11: owner `TASK-030`; required evidence: Cross-artifact claim matrix, seven-lens declarations, capability registry and validator pass.
- AC12: owner `TASK-030`; required evidence: Canonical release preparation, exact runtime identity, two byte-identical builds and independent verifier output.
- AC13: owner `TASK-030`; required evidence: Focused/full validation, current-source drift smoke, package/privacy/diff checks, Doctor, child QA and parent audit.

## Acceptance Criteria

- [x] AC1: Parent AC9 — exact-runtime bounded smoke passes the approved case
  mix with runtime-target/source evidence.
- [x] AC2: Parent AC10/AC11 — every runtime/public artifact agrees on seven
  implemented-not-validated lenses and preserved separation/boundaries.
- [x] AC3: Parent AC12 — alpha.4 preparation and two byte-identical
  independently verified package builds pass.
- [x] AC4: Parent AC13 — full validation, current-source drift smoke, privacy,
  Doctor, QA, audit and retro pass or remain explicitly blocking.

## Goal

Integrate and verify the approved programme without crossing public-release or
capability-promotion authority.

## Approach

Align claims and declarations after sibling source/eval work, prepare alpha.4,
build and verify twice, run isolated exact-runtime smoke with retained source
proof, then perform QA, acceptance audit and retro.

## Phases

1. Align public/runtime declarations and proof boundaries.
2. Prepare and verify deterministic alpha.4 artifacts.
3. Run exact-runtime bounded smoke and current-source drift regression.
4. Complete full QA, parent audit and retro.

## Validation

- AC1: validate child `EVIDENCE.json` against exact smoke artifacts.
- AC2: run claim/dependency scans and every validator scope.
- AC3: prepare alpha.4, build twice and independently verify identities.
- AC4: run focused/full tests, drift smoke, privacy/diff/Doctor, QA and audit.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Align product and runtime claims | Update contract, architecture, README, install, host metadata, validator and manifest around seven bounded lenses. | AC2 | Run claim, link, skill and lens validation. | Done |
| 2 | Prepare deterministic alpha.4 | Bind the runtime change with the canonical command, build twice and verify exact contents/identities. | AC3 | Inspect release authority and compare verifier outputs. | Done |
| 3 | Run bounded exact-runtime dogfood | Execute isolated synthetic architecture/baseline/invocation/control cases and retain runtime-target/source proof. | AC1 | Validate raw artifacts and case verdicts against frozen criteria. | Done |
| 4 | Close validation and QA | Run full regression, current-source drift smoke, privacy/diff/Doctor, QA, parent audit and retro. | AC2, AC4 | Review evidence map, findings and proof boundaries. | Done |

## Parent AC Evidence

- AC9: Run-005 passed 12 frozen scenario groups, 13 fresh sessions, 36 turns and all 38 criteria against exact runtime `0dd720…f15bf1`; three implicit positives loaded the architecture lens and the routine negative loaded no advisor files.
- AC10/AC11: Runtime, contract, architecture, README, install guide, host metadata and validator consistently declare seven implemented-not-validated lenses; no Daily Checklist coupling, cadence lens or separate advisor was added.
- AC12: `release_state.py prepare --version 0.2.0-alpha.4` bound runtime `0dd720…f15bf1`. Two clean builds from `3ddf77a` were byte-identical: standalone `c7d40e…d1ab`, plugin `2d965c…53ee`, ChatGPT `4c09df…623d`, provenance `75c064…0ac2`; both independent verifications passed.
- AC13: 138 unit tests, all seven validator scopes, deterministic eval build, run verifier, privacy/diff checks and Workflow Doctor pass.

## QA & Code Review

- Verdict: Pass for local implementation, bounded behaviour, packaging and closeout gates.
- Evidence: retained run-005 artifacts; exact release authority; two verified clean builds; full validation and Doctor.
- Findings: Alpha.4 remains prepared release intent only. No push, PR, merge, deployment, public release, capability promotion, comparative run or real-user validation occurred.

## Retro

- Reusable lessons: Automatic-invocation claims require both response evidence and host source traces; package determinism must be proven from a clean committed source.
- Conventions or agent assets updated: Drift-smoke activation modes, source-access verifier, local alpha preparation and install checks.
- Follow-up tasks: Public alpha.4 publication requires separate authority; comparative and real-pilot gates remain pending.

## Notes

- Task: TASK-030
- Title: Integrate Runtime Packaging And Bounded Dogfood
- Created: 2026-08-14
