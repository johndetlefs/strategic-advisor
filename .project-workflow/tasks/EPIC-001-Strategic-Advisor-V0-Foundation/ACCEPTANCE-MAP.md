# Acceptance Map

- Epic: EPIC-001
- Last updated: 2026-07-22

| Parent AC | Summary | Child Coverage | Evidence State | Deferral State | Status |
| --- | --- | --- | --- | --- | --- |
| AC1 | The public GitHub repository has `main` as its default branch and contains a README, product contract, contributing guide, security policy, and explicit OSI-compatible licence whose claims match the current release state; a live GitHub query and clean-checkout review verify the repository identity, visibility, default branch, and artifact set. | TASK-001 (In Progress), TASK-006 (Testing) | None | None | Mapped - evidence pending |
| AC2 | `skills/strategic-advisor/` is the only source of strategic logic, passes the selected Agent Skill specification validator, has documented installation/invocation boundaries, and has no host-specific copies that can drift. | TASK-002 (In Progress), TASK-006 (Testing) | None | None | Mapped - evidence pending |
| AC3 | Adversarial cases prove that the core protocol preserves claim status, exposes contradictions, uses the four readiness states correctly, compares distinct world models, avoids false precision, and chooses action or validation proportionately to consequence and reversibility. | TASK-002 (In Progress), TASK-004 (In Progress) | None | None | Mapped - evidence pending |
| AC4 | The four v0 professional lenses each contain their domain contract and pass lens-specific cases, including cases that require professional influence without personal-relationship moralisation and cases that prevent inferred motives or ideal stakeholder behaviour from being treated as facts. | TASK-003 (In Progress), TASK-004 (In Progress) | None | None | Mapped - evidence pending |
| AC5 | Before comparative results are viewed, the evaluation rubric, hard gates, sample set, model/context controls, and material-improvement threshold are committed. Blind scoring then shows the skilled condition materially improves reality fidelity and decision usefulness over the unskilled condition, with zero hard-gate failures. | TASK-004 (In Progress) | None | None | Mapped - evidence pending |
| AC6 | At least two sanitised real pilots—one project/product and one career/organisational—produce a decision or decisive validation step judged useful by the case owner, preserve assumptions and predictions for later review, and introduce no hidden private data into the repository. | TASK-005 (In Progress) | None | None | Mapped - evidence pending |
| AC7 | Repository validation fails on private-data fixtures, unsupported-domain claims, strategic-logic duplication, malformed skill structure, broken internal links, and invalid evaluation metadata; the same validation passes from a clean checkout in continuous integration. | TASK-001 (In Progress), TASK-004 (In Progress), TASK-006 (Testing) | None | None | Mapped - evidence pending |
| AC8 | A release-readiness audit maps every acceptance criterion to current evidence, distinguishes direct proof from report or inference, records limitations and failed cases, and blocks a v0 release if any hard gate or parent criterion is unsatisfied. | TASK-005 (In Progress) | None | None | Mapped - evidence pending |

## Notes

- This is a working coverage map derived from requirements, the epic tracker, deferrals, and child task evidence.
- `ACCEPTANCE-AUDIT.md` remains the closeout evidence artifact.
