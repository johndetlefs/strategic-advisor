# Fix

## Summary

- Fix: FIX-001
- Title: Publish Current Claude Distribution
- Status: In Progress
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
- Branch, PR, and evidence links: `agent/fix-001-current-claude-release`;
  public release evidence will be retained in
  `evidence/releases/v0.2.0-alpha.2.json`, with the PR and release URLs added
  after publication.
- Verification plan: Run the full unit suite, aggregate validator, workflow
  Doctor, two clean deterministic builds from the exact merged source, artifact
  verifier, byte comparisons, archive inventory and sensitive-path checks,
  then download all public assets into a fresh temporary directory and verify
  their GitHub digests and shared provenance.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | `agent/fix-001-current-claude-release` | Pending | Pending |

## Verification

- Delivered scope: ____
- Verification result: ____
- Adjacent behavior checked: ____
- Original acceptance criteria result: Not applicable
- Regression evidence: ____
- Residual risk: ____

## Outcome

- Disposition: Pending
- Decision: ____
- Closed by: ____
- Closed date: ____
- Promoted to: None
