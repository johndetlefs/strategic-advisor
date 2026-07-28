# Requirements

## Summary

- Task: TASK-025
- Title: Automate Current Runtime Distribution
- Last updated: 2026-07-27

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: No
- Approved for implementation: Yes
- Approved scope envelope: Yes
- Approved by: owner
- Approval date: 2026-07-28
- Approval note / source: Codex task owner message on 2026-07-28: Yeah, that's approved. Go for it. Thank you.
- Approved artifact identity: sha256:fc3dd175e81d9befe14ba1590f28e08db0a5e2aba0f33c1182b2c39575758f74

## Goal

Keep the public early-access ZIPs aligned with every accepted canonical runtime
change without relying on the owner to remember or request a separate release,
starting with a new immutable release that contains FIX-002.

## Non-Goals

- Automatically choose the strategic meaning of a semantic version bump.
- Publish a new release for documentation, evaluation, workflow, or test-only
  changes that do not alter the allowlisted runtime bytes.
- Overwrite or mutate an existing release, tag, asset, or historical evidence
  record.
- Promote Strategic Advisor from pre-release, claim a supported installation,
  or prove account activation, host parity, strategic effectiveness, adoption,
  or comparative improvement.
- Copy private Strategy Workspace content into source, artifacts, release
  notes, tests, or evidence.

## Users & Context

- The owner needs accepted Strategic Advisor improvements to become publicly
  installable without remembering a second packaging/release task.
- Codex and Claude users consume `strategic-advisor.zip`; Codex/ChatGPT desktop
  users may consume the plugin ZIP; paid personal ChatGPT users may consume the
  Custom GPT kit.
- Maintainers need PR validation to expose stale distribution intent before
  merge and a deterministic post-merge mechanism that publishes exactly once.
- The current public release is `v0.2.0-alpha.2` from source `582ff0e`; the
  accepted FIX-002 runtime is newer and has not been published.

## Requirements (Outcome-Focused)

- R1. Publish `v0.2.0-alpha.3` as an immutable GitHub prerelease containing the
  FIX-002 canonical runtime in all applicable deterministic distributions.
- R2. Make one committed release authority identify the intended distribution
  version and exact current runtime-package identity; the builder, public
  contract, documentation, validation, and release automation must agree with
  that authority.
- R3. Add one simple maintainer command that prepares a runtime release by
  advancing the version and synchronising the required committed release
  intent and public references. It must fail safely on invalid versions,
  non-advancing versions, or inconsistent source state.
- R4. Make pull-request validation fail when allowlisted canonical runtime bytes
  change without a newly prepared distribution version and matching runtime
  identity. Non-runtime changes must not require a release bump.
- R5. After a prepared runtime change reaches `main`, automatically build the
  standalone Skill, OpenAI local-plugin, ChatGPT Custom GPT kit, and provenance
  twice from the exact clean revision; verify byte equality and archive
  boundaries; then publish a new prerelease and all four assets.
- R6. Release automation must never overwrite an existing version or assets.
  Re-running against an already published version may succeed as an idempotent
  verification only when the public release, source revision, runtime identity,
  and asset digests match exactly; otherwise it must fail.
- R7. Retain structured release evidence and update public current-download
  references only after the new public assets have been clean-downloaded and
  independently verified.
- R8. Preserve current proof boundaries: package publication is not host
  installation, activation, support, adoption, parity, or effectiveness.

## Acceptance Criteria (Verifiable)

- AC1: Public `v0.2.0-alpha.3` exposes all four required assets from one exact
  merged source revision; fresh downloads match GitHub digests, local clean
  builds, trusted provenance, and the FIX-002 runtime identity.
- AC2: A deterministic negative test proves that changing any allowlisted
  runtime byte without advancing the release version and intent fails
  validation, while a documentation-only change does not require a bump.
- AC3: One documented preparation command advances a valid prerelease version
  and synchronises the release authority, builder metadata, contract, and
  public links; invalid, stale, reused, or inconsistent inputs fail without a
  partial update.
- AC4: The protected `main` release workflow publishes a prepared version once,
  uses only exact clean source bytes, pinned actions, least-required
  permissions, deterministic double builds, and independent artifact
  verification.
- AC5: An attempted existing-tag or existing-asset mismatch fails without
  modifying the historical release; an exact rerun reports the already
  published release as verified and performs no mutation.
- AC6: README, INSTALL, product contract, release notes, and structured evidence
  identify `alpha.3` as the current experimental distribution and do not
  promote package readiness into host activation or supported capability.
- AC7: The full unit suite, all aggregate validation scopes, release-focused
  negative tests, clean CI, workflow Doctor, and diff/privacy checks pass at
  the exact released revision.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- D1. Use immutable versioned prereleases rather than a mutable `current` tag or
  overwritten ZIP.
- D2. Require a release for every change to allowlisted canonical runtime bytes;
  do not require one for non-runtime changes.
- D3. Use a committed release authority plus a preparation command so humans and
  agents do not hand-edit the same version in several places.
- D4. Trigger publication from a prepared version reaching `main`; pull-request
  validation prevents an unprepared runtime change from reaching that trigger.
- D5. Publish `0.2.0-alpha.3` for the current FIX-002 runtime.
- D6. Keep the implementation Python-standard-library plus Git/GitHub Actions;
  introduce no service, database, registry, or long-lived publishing secret.

## Validation Plan

- AC1 and AC6 use deployed-artifact alignment: merge the exact prepared source,
  publish `v0.2.0-alpha.3`, download all four assets into a fresh temporary
  directory, compare GitHub/local digests and runtime identity, run the
  independent consumer verifier, inspect the standalone runtime file bytes, and
  retain `evidence/releases/v0.2.0-alpha.3.json`. A local build, workflow log,
  or release-page listing alone is an invalid substitute.
- AC2, AC3, and AC5 use deterministic positive and negative fixtures for
  runtime drift, non-runtime changes, version advancement, partial-write
  prevention, exact reruns, and existing-version mismatches.
- AC4 uses external-contract alignment between the approved workflow contract,
  the committed GitHub workflow, exact permissions/actions, the merged revision,
  the completed workflow run, and public release metadata. A passing local
  script does not prove the GitHub workflow.
- AC7 runs the focused release tests, full unit suite, aggregate validator,
  deterministic double build, artifact verifier, Python compilation, diff
  hygiene, privacy scan, Project Workflow Doctor, and GitHub PR/main checks.
