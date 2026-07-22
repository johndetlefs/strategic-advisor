# Requirements

## Summary

- Task: EPIC-001
- Title: Strategic Advisor v0 Foundation
- Last updated: 2026-07-22

## Overview

Strategic Advisor v0 will establish one portable, reality-constrained advisory skill and the evidence needed to make bounded claims about its usefulness. It will use flagship models for broad hypothesis, reference-class, incentive, and counterfactual search while preventing aspiration, repetition, authority, or polished narrative from being promoted into evidence.

The foundation must be useful without broad connector access. Connectors, host-specific wrappers, and additional life domains come later only when they have a justified contract and evaluation evidence.

## User Story

As a person making a consequential project, career, organisational, or people-leadership decision, I want a capable model to challenge my account of reality, compare credible alternative explanations, and recommend the highest-leverage supportable next move so that I can act without being flattered into an attractive but ungrounded strategy.

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-07-22
- Approval note / source: Codex conversation on 2026-07-22: owner accepted Apache-2.0 and directed go for it after receiving the exact requirements and acceptance envelope.
- Approved artifact identity: sha256:cb114fa48dbb350a724f50715b4e4bb34f17f56a4e62b28703845cf1c50fff55

## Goal

Deliver an open-source v0 foundation whose scope is explicit, whose canonical strategic method is portable, and whose reality discipline and decision usefulness are demonstrated by adversarial and comparative evaluation rather than asserted by its own documentation.

## Non-Goals

- Autonomous external action.
- A central memory service or custom MCP server.
- Broad Slack, Teams, email, calendar, document, or repository ingestion.
- Vendor-specific copies of the strategic logic or guaranteed feature parity across hosts.
- Production support for business, venture, marketing, growth, personal relationship, family, household, or general life advice in v0.
- Correct predictions, guaranteed outcomes, mind-reading, diagnosis, or replacement of qualified legal, medical, clinical, or financial judgment.
- A fixed consulting-framework sequence that suppresses model-native search.

## Users & Context

- Primary users are project and product leaders, people navigating career decisions or organisational politics, and people leaders operating with incomplete or conflicting evidence.
- Users may provide reports, documents, messages, repository state, metrics, or other records. Those inputs vary in freshness, completeness, independence, and authority.
- Users often arrive with a desired outcome and a preferred explanation. The desired outcome is authoritative as a preference, but neither it nor the preferred explanation is evidence.
- Contributors need a clean separation between development-process tooling in `.agents/skills/project-*` and the public product in `skills/strategic-advisor/`.

## Requirements (Outcome-Focused)

- R1. The repository presents an accurate public product promise, validated scope, limitations, privacy boundary, contribution path, and explicit open-source licence.
- R2. One canonical Agent Skill contains all strategic logic and can be consumed without a bespoke agent framework or duplicated vendor-specific prompts.
- R3. The shared reality protocol preserves the epistemic status of every material claim and distinguishes observation, report, inference, assumption, unknown, preference, and forecast.
- R4. Every substantive case is classified as Ready, Conditional, Not validated, or Infeasible as posed before execution advice is presented.
- R5. The advisor compares genuinely distinct explanations and exposes their decision-relevant support, contradictions, predictions, discriminating evidence, and robust actions without exposing private chain-of-thought.
- R6. Recommendations scale proof demands with consequence and reversibility, identify the binding constraint, name opportunity cost, provide the next one to three moves, and include falsifiers, stop conditions, leading indicators, and a review horizon.
- R7. v0 has explicit lenses for project/product, career, organisational influence, and people leadership. Each lens defines outcomes, relevant evidence, causal mechanisms, stakeholder agency, characteristic failure modes, and domain boundaries.
- R8. Organisational influence is treated as a legitimate strategic domain—including framing, sequencing, negotiation, coalition building, incentive alignment, accountability, and private strategy—while material deception, coercion, exploitation, and hidden monitoring are identified with their dependencies and consequences. This must not be conflated with the distinct personal-relationship boundary.
- R9. Evaluation compares skilled and unskilled runs using the same flagship model and clean equivalent context, with thresholds fixed before results are inspected and hard failures that aggregate scores cannot hide.
- R10. Public examples and evaluation cases are synthetic, public, or irreversibly sanitised; no employer, client, household, or other private case data is committed.
- R11. Any future connector boundary is least-privilege, read-only by default, purpose-scoped, auditable, isolated by user/employer/case, and treats retrieved content as incomplete, untrusted input rather than truth or authority.
- R12. Release claims never exceed the domains, hosts, and behaviours actually implemented and proven.

## Acceptance Criteria (Verifiable)

- AC1: The public GitHub repository has `main` as its default branch and contains a README, product contract, contributing guide, security policy, and explicit OSI-compatible licence whose claims match the current release state; a live GitHub query and clean-checkout review verify the repository identity, visibility, default branch, and artifact set.
- AC2: `skills/strategic-advisor/` is the only source of strategic logic, passes the selected Agent Skill specification validator, has documented installation/invocation boundaries, and has no host-specific copies that can drift.
- AC3: Adversarial cases prove that the core protocol preserves claim status, exposes contradictions, uses the four readiness states correctly, compares distinct world models, avoids false precision, and chooses action or validation proportionately to consequence and reversibility.
- AC4: The four v0 professional lenses each contain their domain contract and pass lens-specific cases, including cases that require professional influence without personal-relationship moralisation and cases that prevent inferred motives or ideal stakeholder behaviour from being treated as facts.
- AC5: Before comparative results are viewed, the evaluation rubric, hard gates, sample set, model/context controls, and material-improvement threshold are committed. Blind scoring then shows the skilled condition materially improves reality fidelity and decision usefulness over the unskilled condition, with zero hard-gate failures.
- AC6: At least two sanitised real pilots—one project/product and one career/organisational—produce a decision or decisive validation step judged useful by the case owner, preserve assumptions and predictions for later review, and introduce no hidden private data into the repository.
- AC7: Repository validation fails on private-data fixtures, unsupported-domain claims, strategic-logic duplication, malformed skill structure, broken internal links, and invalid evaluation metadata; the same validation passes from a clean checkout in continuous integration.
- AC8: A release-readiness audit maps every acceptance criterion to current evidence, distinguishes direct proof from report or inference, records limitations and failed cases, and blocks a v0 release if any hard gate or parent criterion is unsatisfied.

## Open Questions (Answer Needed)

- None.

## Decisions (Resolved)

- D1. Build one shared reality protocol plus engagement mode, one primary domain lens, and at most one materially relevant secondary lens; do not build separate independent advisors.
- D2. Package v0 as one canonical Agent Skill, not a bespoke agent framework.
- D3. Validate project/product, career, organisational influence, and people leadership first. Later domains remain architectural intentions, not supported-product claims.
- D4. Treat model breadth, parallel hypothesis generation, counterfactual search, and low-ego revision as advantages in strategic search, not as privileged access to truth.
- D5. Professional stakeholder modelling and deliberate influence are legitimate. People remain adaptive actors, not deterministic components.
- D6. Personal and intimate relationships require a separate lens and are out of v0 implementation scope.
- D7. Defer connectors and vendor adapters until the canonical skill demonstrates value without them.
- D8. Use Project Workflow lightly: one v0 Epic coordinates genuine workstreams; ordinary design discussion does not become a task by default.
- D9. License the repository under Apache License 2.0, providing a permissive licence with an explicit patent grant.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose |
| --- | --- | --- |
| Establish Public Product Contract and Packaging | AC1, AC7 | Create the accurate public surface, licence, contributor/security boundaries, clean-checkout validation, and canonical packaging rules. |
| Implement Canonical Reality Protocol Skill | AC2, AC3 | Build the core skill, claim discipline, readiness gate, competing-world search, action policy, and response contract. |
| Implement v0 Professional Domain Lenses | AC4 | Add and evaluate project/product, career, organisational influence, and people-leadership contracts. |
| Build Adversarial and Comparative Evaluations | AC3, AC4, AC5, AC7 | Freeze the rubric and thresholds, implement hard gates and paired cases, and run reproducible skilled/unskilled comparisons. |
| Validate Pilots and Release Readiness | AC6, AC8 | Run sanitised pilots, preserve calibration records, assemble the acceptance audit, and make the bounded release decision. |

## Validation Plan

- AC1: Query the live GitHub repository, inspect a clean checkout, validate links, and compare all public claims with the product contract and current evidence.
- AC2: Run the selected official or reference Agent Skill validator; install from the documented path in a clean supported host context; scan for duplicated strategic instructions outside the canonical skill.
- AC3: Run paired adversarial cases covering repetition without new evidence, authority bias, preference reversal, contradictory outcome data, false precision, cherished negative-value work, decisive contrary evidence, cheap reversible tests, and infeasibility versus missing evidence.
- AC4: Run lens-specific cases with identical evidence and altered framing, including stakeholder power/incentives, inferred motives, ideal-actor dependencies, legitimate professional influence, and the professional/personal boundary.
- AC5: Commit rubric, thresholds, cases, model identity, and context controls before generating results; blind the scorer to condition; retain raw outputs, scores, hard-gate verdicts, and run metadata.
- AC6: Obtain explicit case-owner usefulness judgments and record only sanitised case descriptions, the decision enabled, assumptions, indicators, review date, and privacy review.
- AC7: Execute positive and negative validation fixtures locally and in CI from a clean checkout.
- AC8: Generate a criterion-by-criterion audit from retained artifacts; independently check that no aggregate score masks a hard-gate failure and that every release statement is supported.
