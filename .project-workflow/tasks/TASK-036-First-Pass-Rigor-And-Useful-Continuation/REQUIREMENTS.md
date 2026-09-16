# Requirements

## Summary

- Task: TASK-036
- Title: First-pass rigor and useful continuation
- Last updated: 2026-09-16
- Intent contract: full

## Intent

Make Strategic Advisor do the necessary scrutiny before its first recommendation, turn uncertainty into a useful next step, and revise conclusions only for a demonstrable reason. Include the existing canonical Project Workflow 0.9.2 upgrade on the same branch and push both changes after bounded verification.

## Intent Spine

- OC1 — Completion capability: A supported first recommendation or an owned investigation/question, with an inspectable reason for retaining or correcting it on review.
- OC2 — Material capabilities: Outcome alignment, authorised relevant context, empirical investigation, strongest-rival scrutiny, action-specific evidence calibration, and selective correction.
- OC3 — Success journey: User asks a strategic question; advisor resolves material ambiguity, checks accessible evidence and rivals, offers a supported move, and meaningfully continues through uncertainty or re-review.
- OC4 — Successful-but-wrong result: More polished headings or stubborn consistency without stronger first-pass work; static tests presented as behavioural effectiveness.
- OC5 — Exclusions: New evaluation infrastructure, new connectors or orchestration, changes in other projects, legacy epic cleanup, publication and host installation.
- OC6 — Assumptions: Existing synthetic evaluation runner is usable; bounded observations cannot establish universal reliability or eliminate sycophancy.
- OC7 — Authority source: Owner approval in this Codex task on 2026-09-16 of the bounded proposal, followed by explicit inclusion of Project Workflow on the same branch and authorisation to push.

## Owner Approval

- Intent reviewed and accurately reflected: Yes
- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: No
- Approved for implementation: Yes
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-09-16
- Approval note / source: Codex task 01a0a7cf-f784-7341-884c-4475eb211baf: approved bounded proposal with "No, I love everything about it. Let us go"; then explicitly included Project Workflow on the same branch and authorised pushing the whole change.
- Approved artifact identity: sha256:a07141cdb4d2af207da1250c29e6d3ca5b82d15b1b09f4458d56494535500726

## Goal

Earn confidence through observed first-pass scrutiny, actionable uncertainty and evidence-based continuity.

## Non-Goals

No new skills, mandatory multi-agent advice, evaluation platform, private case data, unrelated legacy workflow repairs, merge, publication, or host installation.

## Users & Context

People seeking consequential strategic advice and asking for re-review when the first answer has not earned confidence.

## Repository Scope

- Primary repository: .
- Repositories touched: .

## Requirements (Outcome-Focused)

- Strengthen the canonical skill and its seven affected references; keep the six functions internal and proportionate.
- Remove mandatory public readiness labels and eight-section presentation while preserving action-specific support and constraints.
- Review the recommendation rather than infer disagreement; explicitly correct proven reasoning errors even without new outside facts.
- Preserve unaffected conclusions and require independent support for a replacement.
- Update affected synthetic fixtures and assertions, prepare the next immutable distribution, and retain the existing tooling upgrade in its own commit.

## Acceptance Criteria (Verifiable)

- AC1: Ambiguous outcomes trigger a decision-changing question; relevant history remains a checked inference; accessible empirical evidence is investigated before asking the owner to do agent-accessible work.
- AC2: First-pass advice tests the causal bridge and strongest live rival. Unsupported commitment becomes an owned next investigation or question, not a final-looking dead end.
- AC3: Neutral, positive and sceptical re-review on unchanged facts does not itself reverse the conclusion; a specific new fact or demonstrated reasoning error can justify correction; unaffected claims survive and the opposite is not presumed true.
- AC4: Existing deterministic validation and bounded current-source drift smoke are run; eight frozen synthetic cases compare previous and revised runtime; failures and proof limits remain explicit. At most one targeted repair cycle, fail-fast candidate certification, no broadening while failed.
- AC5: Project Workflow 0.9.2 generated upgrade is included unchanged; next immutable runtime distribution is prepared and packaging verified; one independent QA gate is performed after sufficient proof, and both commits are pushed on one branch. Publication and installation remain separate.

## Open Questions (Answer Needed)

None within approved scope. A failed bounded evaluation limits delivery claims and is reported rather than waived.

## Decisions (Resolved)

- Reuse the existing evaluation runner and retain synthetic evidence only.
- Same branch, separate upgrade commit. Owner authorised this explicitly after approving the proposal.
- No repeated approval needed for this faithful transcription of the approved envelope.

## Validation Plan

- Freeze eight cases before outputs; compare alpha.7 and candidate under identical model/context controls.
- Run affected deterministic checks and repository CI commands; one current-source drift smoke and at most one affected repair.
- Retain raw synthetic outputs, independent adjudication and package identities; show concrete before/after examples.
- Independent QA inspects scope, evidence and truthful limits. Full real-world effectiveness remains unestablished.
