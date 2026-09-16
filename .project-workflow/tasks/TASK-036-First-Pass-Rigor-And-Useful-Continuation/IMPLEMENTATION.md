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
- AC5: Canonical tooling provenance already byte-checked against PyPI 0.9.2 wheel; Doctor; prepare alpha.9; reproducible installation artifacts and verification; one independent QA gate; pushed commit identity.
- Evaluation budget: one baseline diagnostic comparison, one candidate certification, one current-source smoke, at most one targeted repair and affected validation. Per run finite call/time/failure limits; stop certification on first product failure. No efficacy or desktop-host claims.

## Repository Evidence

| Repository | Branch / PR | Validation | Delivery | Evidence |
| ---------- | ----------- | ---------- | -------- | -------- |
| . | codex/advisor-first-pass-continuation from origin/main a456589ee3a5631ee246a491225dca0c7deea17e | focused comparison 8/8; drift 15/16 and blocked; prepared alpha.9 artifacts verified | blocked draft push authorised; merge/publication/install excluded | evidence/first-pass/RUN-REPORT.md |

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status | Dependencies | Write Scope | Parallel Safe | Execution Needs |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ | ------------ | ----------- | ------------- | --------------- |
| 1 | Preserve tooling upgrade and freeze proof | Include canonical PW 0.9.2; freeze eight cases and baseline controls | AC4, AC5 | Review bounded evidence | Done | | .project-workflow, AGENTS.md, skills/strategic-advisor/evals | No | bounded-return |
| 2 | Strengthen first-pass and continuation | Update canonical runtime and affected assertions; prepare immutable candidate | AC1, AC2, AC3, AC5 | Inspect before/after examples | Done | 1 | skills/strategic-advisor, scripts, tests, distribution metadata | No | bounded-return |
| 3 | Separate exploration from endorsement | One recommendation-update correction and example; amended first-turn rubric; frozen 12-turn proof | AC2, AC3, AC4, AC5 | Inspect changed response and bounded evidence | Done | 2 | skills/strategic-advisor, distribution metadata, evidence/recommendation-update | No | bounded-return |

## Post-plan Clarify

The plan preserves the approved outcomes. Removing mandatory public labels does not remove evidence calibration. Same-evidence corrections require inspectable error and replacement support; no requirement to invent a reversal. Project Workflow is included unchanged, with no legacy state repair. No unresolved material choice requires another owner question.

## QA & Code Review

- Intent QA contract: adversarial
- Verdict: Not run — blocked by DRIFT-016 verification failure
- Intent adversarial verdict: Not run
- Could every AC pass while the approved user job remains undone: Not assessed by independent QA; the observed DRIFT-016 failure already shows an unresolved outcome gap
- Intent audit state: approved task requirements
- Outcome journey evidence: evidence/first-pass/comparison.json and drift-summary.json; the latter fails DRIFT-016
- Reviewer independence: No reviewer commissioned because campaign proof failed
- Evidence: evidence/first-pass/BLOCKING-FINDING.md
- Findings: Unsupported replacement in DRIFT-016 T3 and insufficient smaller-rival comparison in T1; no further repair authorised in this allowance

## Notes

- Task: TASK-036
- Loaded Project Workflow package 0.10.0, asset 8, coordination contract 2.
- Coordinator executes sequentially; independent reviewer owns no shared workflow writes.
- Python 3.14.6 available locally; CI declares 3.11. Project is standard-library-only and has no lockfile or Codex environment to bootstrap.

Verification follows implementation rows: bounded baseline comparison, candidate certification and smoke. Independent QA then reviews proof before the authorised commits and push. These are lifecycle gates, not prerequisite implementation rows.

Independent QA uses one read-only subagent after the campaign passes: benefit:independent-evidence-audit; overhead:one-bounded-context; tradeoff:review-only-after-proof. The Coordinator retains all tracker and evidence writes.

## Bounded continuation outcome

Owner approved canonical 0.10.0 and one fixed remaining allowance; see OWNER-AMENDMENT.md. The canonical upgrade changed four managed files, all matching the package plan. Existing completed tests and runtime were retained. The paused regression checkpoint resumed once: 42 additional target calls and 13 adjudications; no retries, product repairs or new campaigns. DRIFT-016 failed. No independent QA was launched, and no sealed-host enforcement claim is made. The task is Blocked and the branch is an explicitly incomplete draft.

AC1–AC3 remain unchecked as complete capabilities: the focused comparison passes, but the stronger regression exposes an unresolved first-pass/selective-retraction gap. AC4 has honest executed proof, not passing certification. AC5 has canonical tooling and prepared packaging, but independent QA remains blocked. Existing 226-test initial suite, 46 validator tests and 21 runner tests remain scoped to their recorded sources; no new broad suite was run after the owner imposed the continuation limit.

## Current follow-up

The owner-approved FOLLOWUP-AMENDMENT.md narrows new proof to 12 turns and allows one implementation attempt. The preceding failed campaign is historical and retained in evidence/recommendation-update/previous-coordination.json. Independent QA has never run; it remains one gate after passing affected proof.

## Architecture Impact

- Classification: no
- Reason: This correction changes canonical advice-handling prose and synthetic scoring wording within the existing skill and runner. It adds no component, dependency, ownership boundary, shared state, extension point, or measurable architecture constraint.
- Architecture authority: Not applicable
