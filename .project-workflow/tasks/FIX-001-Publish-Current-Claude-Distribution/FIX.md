# Fix

## Summary

- Fix: FIX-001
- Title: Publish Current Claude Distribution
- Status: Complete
- Created: 2026-07-26

## Report

- Observed or requested: The public Claude download still resolves to
  `v0.2.0-alpha.1` at source revision
  `fe834cd13f0fa4bcdcad0e5dd491c8bddbe92655`, while current `main` is
  `d6561163380d7dc79fba972fe3fce0098e63e712` and contains the subsequently
  delivered personal-context, open-field exploration, and phase-one onboarding
  changes.
- Expected: The documented current alpha and public `strategic-advisor.zip`
  should contain the current canonical runtime and be independently verifiable
  from a clean download.
- Affected users or systems: Claude users, and any Codex or ChatGPT user
  following the current release links.
- Delivered baseline: `v0.2.0-alpha.1` remains a valid deterministic package
  for its named source revision, but it is not the current runtime.
- Report evidence: Live `gh release view v0.2.0-alpha.1` metadata, current
  `origin/main`, `README.md`, `INSTALL.md`, `PRODUCT-CONTRACT.md`, and
  `scripts/build_install_artifacts.py`.

## Routing

- Decision: Fix
- Rationale: This is one release-alignment correction against the completed
  cross-host packaging outcome; it introduces no new strategic behaviour or
  host contract.
- Related work state: EPIC-003, EPIC-004, EPIC-005, and EPIC-002 are complete.
- Bounded correction: Advance the experimental distribution to
  `v0.2.0-alpha.2`, publish current deterministic artifacts, update current
  download references, and retain exact release verification.
- New outcome or material decisions: No
- Independent work items: One

## Classification

- Type: Defect
- Mode: Normal
- Severity: Medium
- Impact: Users following the documented Claude path receive a valid but stale
  runtime that lacks later accepted behaviour.
- Urgency: Before the ZIP is shared with the next Claude user.
- Owner: John Detlefs

## Related Work

- Originating work: EPIC-003 Cross-Host Personal Installation And Distribution
- External links: https://github.com/johndetlefs/strategic-advisor/releases/tag/v0.2.0-alpha.1

## Risk

- Risk level: Medium
- Risks: Publishing artifacts from a dirty or stale source, mismatching release
  notes and bytes, overwriting historical host evidence, or implying Claude
  account activation from package verification.
- Rollback or containment: Do not modify the immutable prior release. If the
  new release is incorrect, mark it superseded and publish a new prerelease;
  retain the exact failed evidence and keep host activation claims separate.

## Fix Plan

- Scope: Bump only the early-access package version, update current distribution
  links, build twice from the clean merged release commit, publish all four
  assets, verify a fresh public download, and record the resulting identities.
- Non-goals: Claude account upload or activation, comparative effectiveness,
  supported-installation promotion, host parity, strategic runtime changes, or
  retroactively changing `v0.2.0-alpha.1` evidence.
- Affected target: Public GitHub prerelease and the shared canonical
  `strategic-advisor.zip` used by Claude and Codex.
- Primary repo: .
- Repos touched: .
- Branch, PR, and evidence links: Preparation branch
  `agent/fix-001-current-claude-release`; closeout branch
  `agent/fix-001-release-closeout`; PR
  https://github.com/johndetlefs/strategic-advisor/pull/14; release
  https://github.com/johndetlefs/strategic-advisor/releases/tag/v0.2.0-alpha.2;
  evidence `evidence/releases/v0.2.0-alpha.2.json`.
- Verification plan: Run the full unit suite, aggregate validator, workflow
  Doctor, two clean deterministic builds from the exact merged source, artifact
  verifier, byte comparisons, archive inventory and sensitive-path checks,
  then download all public assets into a fresh temporary directory and verify
  their GitHub digests and shared provenance.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | `agent/fix-001-current-claude-release` and `agent/fix-001-release-closeout` | [#14](https://github.com/johndetlefs/strategic-advisor/pull/14) | [`v0.2.0-alpha.2`](../../../evidence/releases/v0.2.0-alpha.2.json) |

## Verification

- Delivered scope: Published `v0.2.0-alpha.2` from exact clean source
  `582ff0e961c128fdab54c953b3c394543d8030d2`, updated the current download
  references, and retained the public asset identities and package boundaries.
- Verification result: Pass. Two clean builds were byte-identical; both local
  verifications passed; all four freshly downloaded public assets matched the
  local build byte-for-byte and passed the trusted provenance/runtime verifier.
- Adjacent behavior checked: 125 unit tests, all seven aggregate validation
  scopes, PR #14 GitHub CI, workflow Doctor, archive inventory, and public
  release metadata passed.
- Original acceptance criteria result: Not applicable because FIX-001 corrects
  release freshness after the originating work was accepted; it does not reopen
  or alter any originating acceptance criterion.
- Regression evidence: Historical `v0.2.0-alpha.1` evidence and exact-host
  activation records were not changed or promoted. The new evidence explicitly
  keeps account activation, parity, effectiveness, and support unproven.
- Residual risk: The ZIP has not been uploaded to or activated in the owner's
  Claude account. Host eligibility and UI remain externally controlled and must
  be observed separately when that installation occurs.

## Outcome

- Disposition: Fixed
- Decision: Published and independently verified v0.2.0-alpha.2 from the current canonical runtime; retained Claude activation as unobserved.
- Closed by: Codex
- Closed date: 2026-07-26
- Promoted to: None
