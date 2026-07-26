# Fix

## Summary

- Fix: FIX-002
- Title: Prevent Preference Drift In Candidate Ranking
- Status: In Progress
- Created: 2026-07-26

## Report

- Observed or requested: A review of an owner Strategy Workspace conversation
  found one minor but real ranking drift: after owner enthusiasm and temporary
  rejection of a rival route, the advisor used an economic-engine
  front-runner label even though no new demand, payment, retention, or economic
  evidence had arrived.
- Expected: Preference, owner fit, search-boundary changes, and rival
  availability may alter which hypothesis is investigated first, but only
  qualifying outcome evidence may upgrade commercial readiness or economic
  viability.
- Affected users or systems: Strategic Advisor users comparing unvalidated
  portfolio and clean-slate candidates across multiple turns.
- Delivered baseline: The canonical runtime already states that preference,
  confidence, repetition, agreement, and narrative polish do not upgrade
  evidence. The six-case actual-turn drift smoke checks preference invariance,
  repeated pressure, irrelevant context, evidence deltas, stale context, and
  search-boundary switching, but does not explicitly separate owner fit,
  validation priority, and commercial readiness.
- Report evidence: Owner-authorised review of the private Strategy Workspace
  conversation, plus
  `skills/strategic-advisor/references/conversational-strategy.md`,
  `skills/strategic-advisor/references/evidence.md`, and
  `skills/strategic-advisor/evals/drift_smoke_cases.json`. Private case content
  is not retained in this public repository.

## Routing

- Decision: Fix
- Rationale: This is one bounded correction to an existing evidence-conservation
  behaviour and its regression coverage. It does not create a new strategic
  workflow, decision outcome, or evaluation programme.
- Related work state: EPIC-002 and EPIC-005 are complete.
- Bounded correction: Add an explicit three-axis candidate-ranking rule to the
  canonical conversational runtime, add one public-synthetic multi-turn drift
  scenario for preference and rival-removal pressure, and retain a fresh
  current-source actual-turn smoke.
- New outcome or material decisions: No
- Independent work items: One

## Classification

- Type: Defect
- Mode: Normal
- Severity: Medium
- Impact: An unvalidated preferred hypothesis can be described as the leading
  economic candidate even while the surrounding caveats remain correct,
  creating more confidence than the evidence warrants.
- Urgency: Before the next consequential candidate-ranking conversation.
- Owner: John Detlefs

## Related Work

- Originating work: EPIC-005 Open-Field Exploration And Visible Strategic
  Framing; TASK-012 Validate Sycophancy And Context Drift
- External links: None

## Risk

- Risk level: Medium
- Risks: Overcorrecting into performative neutrality, suppressing legitimate
  owner-fit information, making the runtime verbose, or writing a regression
  that encodes private case facts or evaluation authority into the installable
  package.
- Rollback or containment: Revert the bounded runtime paragraph and synthetic
  case. Keep private case material outside the repository, and do not promote
  commercial-readiness or broad drift-resistance claims from this smoke.

## Fix Plan

- Scope: Separate owner fit, validation priority, and commercial readiness in
  candidate ranking; state that removing a rival changes the option set rather
  than the survivor's evidence; reserve economic-front-runner language for
  qualifying comparative evidence; add deterministic and actual-turn
  regression proof.
- Non-goals: Change any owner Strategy Workspace decision, select or reject a
  commercial-games route, copy private owner facts into the public repository,
  reopen the comparative evaluation programme, or claim universal
  sycophancy resistance.
- Affected target: Canonical Strategic Advisor conversational runtime and its
  bounded current-source drift smoke.
- Primary repo: .
- Repos touched: .
- Branch, PR, and evidence links: Local `main`; no PR or push authorised;
  planned evidence `evidence/evaluations/drift-smoke/run-004/`.
- Verification plan: Run focused drift-smoke and runtime-package tests, the
  aggregate validator and full unit suite, build and verify the exact runtime
  package, execute every frozen scenario as fresh/resumed Codex CLI turns in an
  isolated neutral repository, review every precommitted criterion, verify the
  retained result, run diff hygiene, and run Project Workflow Doctor.

### Repository Links

| Repo | Branch | PR | Evidence |
|---|---|---|---|
| . | `main` (local) | None | `evidence/evaluations/drift-smoke/run-004/` (planned) |

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
