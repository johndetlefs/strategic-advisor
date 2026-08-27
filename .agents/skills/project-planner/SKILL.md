---
name: project-planner
description: Use when turning confirmed project-workflow requirements into a phased implementation plan and testable work-item table.
---
<!-- project-workflow:generated -->

# Project Planner

Turn confirmed requirements into a safe, incremental implementation plan.

## Invocation Rules

- Use this skill whenever the user asks for an implementation plan, phases, or testable work items for a project-workflow task, even if they ask in natural language.
- Read `AGENTS.md` and `.project-workflow/guidance.md` if present, then follow the project-workflow managed block and CLI requirements.
- If the task folder does not exist, use `project-task` first so the CLI creates the required files and tracker row.
- If requirements are missing or unclear, use `project-requirements` or `project-clarify` before planning.
- Verify the owner-approved requirements/AC envelope before planning. Planning must not be used to
  manufacture or infer that approval.
- Planning is a document workflow unless the CLI adds an explicit planner command.

## Required Files

- `.project-workflow/tasks/<TASK>/REQUIREMENTS.md`
- `.project-workflow/tasks/<TASK>/IMPLEMENTATION.md`
- `.project-workflow/TRACKER.md`
- `.project-workflow/CONSTITUTION.md` if present
- `AGENTS.md` and other repo instructions if present

## Workflow

1. Read requirements first and treat them as the source of truth.
2. If requirements are missing, unclear, or internally inconsistent, stop and use `project-requirements` or `project-clarify`.
3. Produce or update `IMPLEMENTATION.md` with:
   - `## User Story` at the top
   - `## Goal`
   - `## Approach`
   - `## Phases`
   - `## Tasks`
4. Assign or preserve stable acceptance criteria IDs (`AC1`, `AC2`, etc.) from
   `REQUIREMENTS.md` and the `## Acceptance Criteria` section in
   `IMPLEMENTATION.md`.
5. Make every task independently testable and outcome-based.
6. Map every task row to one or more AC IDs, and ensure every AC ID is covered
   by at least one task row.
   If a row claims visual/reference fidelity, external contract alignment,
   deployed/published artifact alignment, runtime target/source verification,
   or responsive/multi-context behavior, include the matching proof recipe and
   evidence artifact expectation in the row. Do not use code review, tests,
   builds, surrogate surfaces, or related environments as recipe substitutes.
7. Use this table shape for tasks:

```md
|  ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
|   1 | <Outcome> | <What changes for the user/system?> | AC1: <observable pass/fail criteria> | <steps or command> | To Do |
```

8. Keep each table row on one physical line. Use `<br>` for multiple items
   inside a cell and escape literal `|` characters.
9. Include validation steps for each phase.
10. In workspace mode, preserve the approved `Repository Scope` and add one `Repository
    Evidence` row per touched repository. Plan explicit branch/PR state, repository-specific
    validation, delivery state, and evidence attribution; do not plan automatic cross-repository
    Git mutations unless separately authorized.
11. Move to `Analysing`, write the plan, then run `project-clarify` as a post-plan consistency pass.
12. Run `./.project-workflow/cli/workflow task ready --id <TASK-ID>` and fix repo-gatherable
    gaps. If it passes, move to `Ready` and continue inside the approved envelope. `Plan Confirmed`
    remains legacy-compatible; explicit human plan review is optional for requested or exceptional
    high-risk plans, not the default checkpoint.
13. Return to the owner if the plan exposes material scope drift, a new product decision,
    exceptional authority, or changed proof obligations/artifact identity.
14. For a child of a full-contract Epic, preserve every assigned OC commitment in the plan and
    update its sourced `INTENT-AUDIT.json` coverage. `epic intent-audit` must not classify a full
    capability as a canary, preview, internal representation, subset, debug-only path or other
    proxy without a plain owner-approved capability amendment.
15. Include QA/code review as the required gate after implementation validation
    and before completion.
16. Do not implement code during planning.

For Coordinator execution plans, extend the task table with `Dependencies`, `Write Scope`,
`Parallel Safe`, and `Execution Needs`. Use blank or `bounded-return` for ordinary work that should
remain Coordinator/sequential. A non-Coordinator surface must also declare exactly one
`benefit:<slug>`, `overhead:<slug>`, and `tradeoff:<slug>` basis explaining its delivery benefit,
expected setup/synthesis overhead, and why the benefit outweighs that overhead. Use
`durable-resume`, `direct-owner-steering`, `isolated-worktree`, or `peer:<group-id>` only when the
approved work actually requires that binding property. These are work facts, not host-capability claims.
Keep Task rows distinct from Epic child Tasks. Plan no fixed worker count: runtime
capacity is observed at execution. Include coordinator-only workflow writes, bounded worker packets,
coordinator verification, descendant blocking, and independent-branch continuation while shared
premises remain valid.
