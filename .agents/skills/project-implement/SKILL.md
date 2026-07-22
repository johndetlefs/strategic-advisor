---
name: project-implement
description: Use when implementing one project-workflow work item with requirements alignment, tracker updates, validation, and concise reporting.
---
<!-- project-workflow:generated -->

# Project Implement

Implement one scoped work item from a project-workflow task and move it to testing.

## Invocation Rules

- Use this skill whenever the user asks to implement a project-workflow task or planned work item, even if they ask in natural language.
- Read `AGENTS.md` and `.project-workflow/guidance.md` if present, then follow the project-workflow managed block and CLI requirements.
- If the task folder does not exist, use `project-task` first so the CLI creates the required files and tracker row.
- If requirements or implementation tasks are missing, use `project-requirements` and `project-planner` before coding.
- Use the CLI for any supported tracker-safe operation before editing Markdown manually.

## Required Files

- `.project-workflow/tasks/<TASK>/REQUIREMENTS.md`
- `.project-workflow/tasks/<TASK>/IMPLEMENTATION.md`
- `.project-workflow/TRACKER.md`
- Repo instruction files such as `AGENTS.md`

## Workflow

1. Infer the task ID from the user prompt or current branch if possible. Ask only if it cannot be inferred.
2. Infer the work item from the user prompt or the next `To Do` task in `IMPLEMENTATION.md`. Ask only if ambiguous.
3. Read `REQUIREMENTS.md` and `IMPLEMENTATION.md` before editing code.
4. Run `./.project-workflow/cli/workflow task ready --id <TASK-ID>` before coding. If approval is missing or stale after requirements are ready, record the single owner approval envelope with `task approve-requirements`; for pre-existing legacy tasks use `task adopt` and treat pre-adoption evidence as untrusted until refreshed. Otherwise remediate the listed drift/evidence gaps without asking for generic approval.
5. Restate the selected work item and scope boundary.
6. Map each planned change to the relevant AC IDs. If a change does not map,
   stop and ask for direction.
7. Ensure the new-task lifecycle is `Ready` (or legacy `Plan Confirmed`) after the post-plan
   clarification/readiness pass, then run
   `./.project-workflow/cli/workflow task status --id <TASK-ID> --to "In Progress"` before coding.
   Do not ask for repeated approval for unchanged work inside the approved envelope.
8. Make the smallest safe code change that satisfies the selected work item.
9. Add or update tests when appropriate.
10. Run relevant automated checks and any required manual verification steps.
11. Run `./.project-workflow/cli/workflow task status --id <TASK-ID> --to Testing` after implementation and validation have run.
12. Run `./.project-workflow/cli/workflow doctor` and report workflow-state warnings or errors.
13. Do not set status to `Complete`; completion is owned by `project-qa-review` after QA/code review passes and the user explicitly asks.
14. Report changed files, validation results, remaining risks, and that `project-qa-review` is the next required lifecycle step.

If requirements conflict with repo constraints or validation is not testable, stop and use `project-clarify`.
