## User Story

As a person seeking strategic advice, I want a rigorous first answer and useful continuation so I do not have to provoke arbitrary revisions to discover whether the work was done.

## Architecture Impact

- Classification: no
- Reason: Canonical instruction and synthetic scoring changes use the existing skill, evaluator and packaging. No component, dependency, ownership boundary, shared-state boundary or extension point changes.
- Architecture authority: Not applicable

## Acceptance Criteria

- [x] AC1: Outcome alignment, relevant context and accessible investigation are implemented; historical first-pass observations remain source-labelled.
- [x] AC2: Rival scrutiny and owned continuation without mandatory labels are implemented and included in the bounded affected observation.
- [x] AC3: Evidence-based continuity plus explicit exploration/testing/endorsement distinction; genuine changed priorities remain effective. Automatic 12-turn check passes; substantive independent QA pending.
- [x] AC4: Owner-amended affected-only proof executed once: three groups, five sessions, twelve turns. Original failure and rubric retained; no current full-suite claim.
- [ ] AC5: Canonical PW0.9.2/0.10 upgrades and clean-source alpha.10 artifacts verified; independent QA and updated same-branch push pending.

## Validation

- Current alpha.10: evidence/recommendation-update/run/result.json, source-audit.json, structural-validation.log, generated-inventory.log, package-verification.json and install-artifacts.json.
- Scope: twelve target turns, three adjudications, 453 recorded seconds, zero retries or retuning. This is the complete owner-approved affected envelope; the CLI calls this its full stage without implying the historical full regression suite.
- Historical alpha.9: evidence/first-pass/comparison.json (8/8 focused) and drift-summary.json (15/16 regression with DRIFT-016 failure). These are not reused as current-runtime passing observations.
- Earlier code-level tests remain at their recorded sources; no runner or validator code changed in this follow-up. CI remains the repository-declared integration check.
- T3-COMPARISON.md is an explicit substantive-review concern; automatic grades do not settle whether the recommendation gap is fixed.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/advisor-first-pass-continuation; PR #24 | current 12-turn affected result and package verification pass; independent QA pending | prior draft pushed; latest follow-up push pending; merge/publication/install excluded | evidence/recommendation-update/REPORT.md |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Preserve tooling upgrade and freeze proof | Include canonical PW upgrades and frozen authority | AC4, AC5 | Inspect retained evidence | Done | | .project-workflow, AGENTS.md, skills/strategic-advisor/evals | No | bounded-return |
| 2 | Strengthen first-pass and continuation | Canonical runtime and affected assertions | AC1, AC2, AC3, AC5 | Inspect before/after examples | Done | 1 | skills/strategic-advisor, scripts, tests, distribution metadata | No | bounded-return |
| 3 | Separate exploration from endorsement | One targeted update correction, versioned rubric and 12-turn proof | AC2, AC3, AC4, AC5 | Inspect new responses | Done | 2 | skills/strategic-advisor, distribution metadata, evidence/recommendation-update | No | bounded-return |

## Post-plan Clarify

The owner approved FOLLOWUP-AMENDMENT.md and its explicit affected-only proof scope. The old failure is retained. There is one implementation attempt and one independent QA; no further model test or prompt repair is authorised after output. Routine direct help and legitimate owner-value changes remain permitted.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pending
- Intent adversarial verdict: Pending
- Could every AC pass while the approved user job remains undone: Pending independent judgment
- Intent audit state: Current owner-approved requirements and FOLLOWUP-AMENDMENT.md
- Outcome journey evidence: evidence/recommendation-update/run/result.json and T3-COMPARISON.md
- Reviewer independence: One separate sealed Codex context; no shared workflow write authority; not yet launched
- Evidence: Pending independent report
- Findings: Pending independent judgment; T3 endorsement language explicitly called out for review

## Execution and proof boundaries

Coordinator is the sole shared-state writer. Independent review: benefit:substantive-independent-assessment; overhead:one-bounded-context; tradeoff:review-only-after-affected-proof. The sealed review permits eight exact read commands and one report file; no tests or worker launches. The external behavioural runner separately enforces the frozen twelve-call limit. No claim of aggregate nested-model enforcement is made.

Historical failed campaigns remain in evidence/first-pass and evidence/recommendation-update/previous-coordination.json. Current release metadata supersedes unpublished alpha.9 with prepared alpha.10. Publication, installation, adoption and owner acceptance are not established.
