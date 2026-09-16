## User Story

As a person seeking strategic advice, I want a rigorous first answer and useful continuation so I do not have to provoke arbitrary revisions to discover whether the work was done.

## Acceptance Criteria

- [ ] AC1: Outcome alignment, relevant context and accessible investigation.
- [ ] AC2: First-pass rival scrutiny and owned continuation without mandatory labels.
- [ ] AC3: Stable re-review and specific evidence-based correction.
- [ ] AC4: Frozen eight-case comparison, current-source smoke and deterministic checks with honest failure bounds.
- [ ] AC5: Canonical tooling upgrade, immutable candidate, independent QA and same-branch push.

## Validation

- AC1–AC3: Frozen synthetic eight-case comparison of alpha.7 and candidate; exact outputs and adjudication retained.
- AC4: Current-source drift smoke; validate.py, build_evals.py --check, unittest discovery.
- AC5: Canonical tooling provenance already byte-checked against PyPI 0.9.2 wheel; Doctor; prepare alpha.8; reproducible installation artifacts and verification; one independent QA gate; pushed commit identity.
- Evaluation budget: one baseline diagnostic comparison, one candidate certification, one current-source smoke, at most one targeted repair and affected validation. Per run finite call/time/failure limits; stop certification on first product failure. No efficacy or desktop-host claims.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/advisor-first-pass-continuation from origin/main a456589ee3a5631ee246a491225dca0c7deea17e | pending | push authorised; merge/publication/install excluded | synthetic evidence only |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Preserve tooling upgrade and freeze proof | Include canonical PW 0.9.2; freeze eight cases and baseline controls | AC4, AC5 | Review bounded evidence | Done | | .project-workflow, AGENTS.md, skills/strategic-advisor/evals | No | bounded-return |
| 2 | Strengthen first-pass and continuation | Update canonical runtime and affected assertions; prepare immutable candidate | AC1, AC2, AC3, AC5 | Inspect before/after examples | Done | 1 | skills/strategic-advisor, scripts, tests, distribution metadata | No | bounded-return |

## Post-plan Clarify

The plan preserves the approved outcomes. Removing mandatory public labels does not remove evidence calibration. Same-evidence corrections require inspectable error and replacement support; no requirement to invent a reversal. Project Workflow is included unchanged, with no legacy state repair. No unresolved material choice requires another owner question.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Pending
- Intent adversarial verdict: Pending
- Could every AC pass while the approved user job remains undone: Pending
- Intent audit state: approved task requirements
- Outcome journey evidence: Pending synthetic actual-turn evidence
- Reviewer independence: One independent reviewer after campaign proof
- Evidence: Pending
- Findings: Pending

## Notes

- Task: TASK-036
- Loaded Project Workflow package 0.9.2, asset 8, coordination contract 2.
- Coordinator executes sequentially; independent reviewer owns no shared workflow writes.
- Python 3.14.6 available locally; CI declares 3.11. Project is standard-library-only and has no lockfile or Codex environment to bootstrap.

Verification follows implementation rows: bounded baseline comparison, candidate certification and smoke. Independent QA then reviews proof before the authorised commits and push. These are lifecycle gates, not prerequisite implementation rows.
