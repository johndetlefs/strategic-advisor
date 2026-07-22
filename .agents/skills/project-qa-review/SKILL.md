---
name: project-qa-review
description: Use after implementation validation to run the QA and code review gate before a project-workflow task is completed.
---
<!-- project-workflow:generated -->

# Project QA & Code Review

Run the post-implementation quality gate for a project-workflow task.

## Invocation Rules

- Use this skill whenever the user asks for QA, review, code review, verification, release readiness, or completion approval for a project-workflow task.
- Read `AGENTS.md` and `.project-workflow/guidance.md` if present, then follow the project-workflow managed block and CLI requirements.
- If implementation has not reached `Testing`, use `project-implement` first.
- QA/code review is a document and validation workflow unless the CLI adds an explicit review command.

## Required Files

- `.project-workflow/tasks/<TASK>/REQUIREMENTS.md`
- `.project-workflow/tasks/<TASK>/IMPLEMENTATION.md`
- `.project-workflow/TRACKER.md`
- Repo instruction files such as `AGENTS.md` or `.github/copilot-instructions.md`

## Workflow

1. Infer the task ID from the user prompt or current branch if possible. Ask only if it cannot be inferred.
2. Read requirements, implementation notes, tracker status, and the current diff before reviewing.
3. Confirm the task or work item is in `Testing`. If not, stop and route to `project-implement`.
4. Run `./.project-workflow/cli/workflow task status --id <TASK-ID> --to Review` before review work begins.
5. Map every relevant acceptance criterion ID to validation evidence.
6. If requirements or claims trigger a proof recipe, verify child-local `EVIDENCE.json` has passing structured claim records. QA prose cannot satisfy recipe-triggered visual/reference fidelity, external contract alignment, deployed artifact alignment, runtime target/source, or responsive visual behavior claims.
7. Run any missing narrow validation needed to support the review. Do not ask the user to manually test behavior that the agent can validate directly with available commands, tests, scripts, or local tools.
8. Review the changed code for correctness, scope control, maintainability, edge cases, tests, docs, security, permissions, privacy, data integrity, and operational risk.
9. Record results in `IMPLEMENTATION.md` under `## QA & Code Review` with date, reviewed areas, validation evidence, findings, and verdict. Clearly separate verified evidence from deferred setup, owner-only actions, unavailable connector/OAuth checks, and invalid substitutes.
10. Run `./.project-workflow/cli/workflow doctor` and include any workflow-state warnings or errors in the review output.
11. If findings exist, report them first with severity and file references. Keep status as `Review` or set `Blocked` for release-blocking issues.
12. If review passes, say so. Run `./.project-workflow/cli/workflow task status --id <TASK-ID> --to Complete` only when the user explicitly asks to complete the task after review.
13. After completion, route to `project-retro`.

## Verdicts

- `Pass`: no blocking findings and validation evidence covers the acceptance criteria by AC ID.
- `Pass with follow-ups`: safe to complete, but separate follow-up work is recommended.
- `Changes requested`: completion is blocked until findings are addressed.
