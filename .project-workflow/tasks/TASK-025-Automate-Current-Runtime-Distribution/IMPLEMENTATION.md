## User Story

As the Strategic Advisor owner, I want every accepted canonical runtime change
to require and automatically publish a new deterministic public distribution,
so that users receive the current ZIP without me remembering to request a
separate release.

## Acceptance Criteria

- [x] AC1: Public `v0.2.0-alpha.3` exposes the four required artifacts from one exact merged source revision, and fresh downloads match the local clean build, trusted provenance, and FIX-002 runtime identity.
- [x] AC2: Runtime-byte drift without a prepared version fails deterministically; a documentation-only change does not require a version bump.
- [x] AC3: One preparation command advances and synchronises valid release intent without partial writes; invalid, stale, reused, or inconsistent input fails.
- [x] AC4: The protected-main workflow uses pinned actions, least-required permissions, exact clean source, double builds, verification, and publish-once semantics.
- [x] AC5: Existing-release mismatch fails without mutation; an exact rerun verifies idempotently without mutation.
- [x] AC6: Public documentation, contract, release notes, and evidence identify alpha.3 as experimental without claiming host activation, support, parity, adoption, or effectiveness.
- [x] AC7: Focused and full validation, clean CI, Doctor, diff hygiene, and privacy checks pass for the exact released revision.

## Goal

Make public runtime ZIP freshness an enforced release invariant rather than a
separate owner reminder, beginning with the accepted FIX-002 runtime.

## Approach

- Add one canonical distribution authority that records the prepared version,
  exact runtime-package identity, lifecycle state, and previously verified
  public version. The builder and repository validator read this authority
  instead of maintaining independent version constants.
- Add one standard-library release command with explicit `prepare`, `check`,
  `build`, `publish`, and `verify-public` operations. `prepare` stages all
  synchronized source updates and commits them atomically only after every
  validation succeeds.
- Treat “prepared” and “current public” references as distinct states. A
  prepared change may name its immutable future tag, but the current-download
  claim and retained release evidence are promoted only after a fresh public
  download passes. This resolves the timing boundary between AC3 and R7
  without weakening either.
- Extend pull-request validation so any byte change selected by the canonical
  runtime allowlist requires a new prepared version and matching runtime
  identity, while non-runtime changes leave the release invariant satisfied.
- Add a protected-main release workflow that builds twice from the exact clean
  commit, verifies the four artifacts independently, publishes only a new
  immutable prerelease, and treats an exact existing release as a read-only
  verification path.
- Publish and independently verify `v0.2.0-alpha.3`, then commit the verified
  evidence and current-download promotion as closeout state.

## Phases

### Phase 1 — Canonical release state and preparation

- Introduce the distribution authority and remove duplicated version
  ownership.
- Implement atomic preparation, release-state validation, and negative
  fixtures.
- Validation: focused release tests plus repository validation for runtime and
  documentation-only fixture changes.

### Phase 2 — Deterministic publish and public verification

- Implement clean double-build orchestration, immutable GitHub release
  inspection/publication, exact-rerun verification, and mismatch refusal.
- Add the pinned, least-permission protected-main workflow.
- Validation: isolated command fixtures, workflow contract inspection, full
  unit suite, aggregate validator, and local double-build comparison.

### Phase 3 — Alpha.3 integration and release

- Prepare alpha.3 against the exact FIX-002 runtime, update candidate-facing
  contract/docs, and open the integration pull request.
- Merge only after clean PR checks; observe the exact main workflow and public
  release.
- Validation: GitHub PR/main checks and public metadata against the merged
  revision.

### Phase 4 — Verified public closeout

- Download alpha.3 into a fresh directory, compare all public/local/GitHub
  digests, verify provenance and archive boundaries, inspect runtime bytes,
  and retain structured release evidence.
- Promote alpha.3 to the public current-download reference only after that
  proof passes, then run QA, Doctor, diff/privacy checks, and closeout.
- Validation: deployed-artifact alignment and external-contract alignment in
  child-local `EVIDENCE.json`.

## Task List

|  ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
|   1 | Establish canonical release authority | Add one version/runtime/state authority, make builder and validator consume it, and add an atomic preparation command with safe failure behavior. | AC2: unprepared runtime drift fails while documentation-only drift passes.<br>AC3: valid preparation synchronises state; invalid or reused versions leave every file unchanged.<br>AC6: candidate and current-public states remain explicitly bounded. | Run focused preparation tests and inspect one successful alpha.3 preparation plus unchanged-file hashes for each negative fixture. | Done |
|   2 | Enforce deterministic immutable publication | Add release orchestration and a pinned protected-main workflow that double-builds, verifies, publishes once, and verifies exact existing releases read-only. | AC4: workflow source, permissions, actions, checkout identity, and build/verify sequence match the approved external contract; retain external-contract-alignment evidence.<br>AC5: mismatch is non-mutating and exact rerun is read-only. | Run local release-command fixtures, inspect the workflow, and verify GitHub’s completed run at the merged revision. | Done |
|   3 | Integrate and publish alpha.3 | Prepare the FIX-002 runtime as `0.2.0-alpha.3`, pass PR validation, merge, and let the main workflow publish all four required assets. | AC1: the immutable prerelease and four assets identify one merged revision and exact runtime identity.<br>AC6: release notes remain experimental and preserve proof boundaries.<br>AC7: PR and main CI pass on the released revision. | Inspect the merged commit, completed release workflow, release metadata, and required asset inventory. | Done |
|   4 | Verify public downloads and close out | Fresh-download alpha.3, compare public/local/GitHub identities, run the independent verifier, retain release evidence, promote current links, and complete QA/retro. | AC1: deployed-artifact-alignment evidence proves fresh public bytes match the trusted build and FIX-002 runtime.<br>AC6: README, INSTALL, contract, notes, and evidence agree after proof.<br>AC7: full tests, seven validation scopes, Doctor, diff/privacy checks, and final CI pass. | Reproduce from a fresh temporary directory using the recorded commands and inspect child-local `EVIDENCE.json` plus `evidence/releases/v0.2.0-alpha.3.json`. | Done |

## Validation

- AC1: Build twice from the exact clean merged revision; compare all four
  outputs; download all public assets into a fresh directory; match GitHub,
  local, provenance, runtime, and archive identities; retain deployed-artifact
  alignment evidence.
- AC2: Run deterministic fixtures that alter an allowlisted runtime byte
  without preparation and alter a documentation-only byte without preparation.
- AC3: Run successful advancement plus invalid syntax, non-advancing, reused,
  dirty/inconsistent source, and partial-write prevention fixtures.
- AC4: Compare the approved workflow contract with the committed workflow,
  pinned action SHAs, permissions, exact merged revision, completed GitHub run,
  and published metadata; retain external-contract alignment evidence.
- AC5: Exercise a simulated existing-release mismatch and exact rerun locally,
  then verify the public alpha.3 rerun path without mutation.
- AC6: Validate README, INSTALL, product contract, release notes, release
  authority, and structured evidence for consistent experimental wording and
  proof boundaries.
- AC7: Run focused release tests, `python3 -m unittest discover -s tests -v`,
  `python3 scripts/validate.py`, `python3 scripts/build_evals.py --check`,
  deterministic double builds, independent artifact verification,
  `python3 -m compileall`, diff/privacy scans, Project Workflow Doctor, and
  GitHub PR/main checks on the released revision.

## QA & Code Review

- Date: 2026-07-28
- Reviewed areas: canonical version/runtime ownership; transactional
  preparation/finalization; runtime-drift enforcement; builder/provenance
  integration; immutable GitHub publication and exact-rerun paths; workflow
  permissions and pinned actions; tests, docs, structured evidence, privacy,
  and proof-boundary language.
- AC1: `EVIDENCE.json` CLM-001 and
  `evidence/releases/v0.2.0-alpha.3.json` retain the merged source, four public
  asset hashes, runtime identity, workflow download proof, separate closeout
  download, independent verifier result, and all 25 runtime-byte comparisons.
- AC2: validator and release-state fixtures prove unprepared allowlisted-byte
  drift fails while a documentation-only change passes.
- AC3: preparation fixtures prove valid advancement plus invalid,
  non-advancing, reused, and replace-failure rollback behavior; alpha.3 was
  prepared with the documented command.
- AC4: `EVIDENCE.json` CLM-002, workflow SHA-256
  `89c3ae3a0cf4f9e949fa566f4d43267e69a49605e84ef452a9475023843eb4d8`,
  and successful run 30317434367 align the approved workflow contract with the
  exact merged execution.
- AC5: mismatch fixtures remain non-mutating. Live rerun 30317826554 detected
  the existing release, skipped publication, freshly downloaded and verified
  the same assets, and left tag, publication time, asset IDs, and digests
  unchanged.
- AC6: finalized README, INSTALL, product contract, release notes, authority,
  and evidence identify alpha.3 as experimental and keep every host,
  activation, support, parity, adoption, and effectiveness claim false or
  separate.
- AC7: PR 16, main validation run 30317434382, and both release workflow runs
  passed. The exact release run recorded 134 tests, seven scopes, 45 generated
  cases, two clean identical builds, and fresh-public verification. Final
  closeout reran 134 tests, seven scopes, the 45-case inventory, Python
  compilation, diff hygiene, privacy validation, and Doctor successfully.
- Findings: No blocking correctness, security, privacy, data-integrity, scope,
  or maintainability findings. GitHub emitted non-blocking upstream Node 20
  deprecation annotations for the latest pinned action releases while running
  them successfully on Node 24; this does not weaken the recorded execution.
- Verdict: Pass.

## Retro

- Date: 2026-07-28
- Reusable lessons: Runtime acceptance and public packaging must be one
  enforced lifecycle, but prepared intent and verified-current public state
  must remain separate. A workflow success is insufficient without a fresh
  public download, and a first publication does not prove the read-only rerun
  path.
- Conventions or agent assets updated: `CONTRIBUTING.md` documents the
  maintainer prepare/publish/finalize lifecycle. `.project-workflow/guidance.md`
  now requires every accepted allowlisted runtime-byte change to prepare its
  immutable distribution in the same work item and forbids deferring the ZIP
  to an owner reminder.
- Follow-up tasks: None required. The non-blocking GitHub annotation about
  upstream action Node runtimes should be reassessed when new official action
  releases exist, not worked around with an unpinned or insecure runtime.
- Missed in-scope work: None. The post-finalization fixture assumption was
  found and corrected before completion.

## Notes

- Task: TASK-025
- Title: Automate Current Runtime Distribution
- Created: 2026-07-27
- 2026-07-28: Owner approval recorded for requirements identity
  `sha256:fc3dd175e81d9befe14ba1590f28e08db0a5e2aba0f33c1182b2c39575758f74`.
- 2026-07-28: `release_state.py prepare --version 0.2.0-alpha.3`
  bound the candidate to runtime identity
  `sha256:200a91f4a988a55450ae7859541ca12b2169a08ba192f0dbd7a8f905c903e590`.
- 2026-07-28: Local implementation validation passed 134 unit tests, all
  seven aggregate scopes, the 45-case generated evaluation inventory,
  release-state and publish negative fixtures, Python compilation, YAML
  parsing, diff checks, Project Workflow Doctor, and two byte-identical
  exploratory artifact builds. Clean exact-revision release proof remains
  pending until the implementation commit exists.
- 2026-07-28: PR 16 merged as `cfacb3b16ba035996e732aa1680f2628b67446d3`.
  PR CI, main CI, and release workflow run 30317434367 passed. The workflow
  built twice, published `v0.2.0-alpha.3`, downloaded the four public assets,
  independently verified them, and retained evidence artifact 8672677936.
- 2026-07-28: A separate closeout download matched all four GitHub digests,
  trusted provenance, runtime identity, and all 25 canonical runtime files.
  Alpha.3 was then promoted from prepared intent to current public state.
- 2026-07-28: The first post-finalization suite exposed that two publish
  fixtures assumed perpetual prepared state. The fixtures now establish their
  own prepared alpha.4 state; the final closeout run passed all 134 tests,
  seven scopes, 45-case inventory, compilation, diff checks, and Doctor.
