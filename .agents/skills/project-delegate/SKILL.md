---
name: project-delegate
description: Use when coordinating multiple planned project-workflow work items with sequential or dependency-aware parallel execution.
---
<!-- project-workflow:generated -->

# Project Delegate

Coordinate multiple work items from an existing project-workflow implementation plan.

## Invocation Rules

- Use this skill whenever the user asks to delegate, coordinate, batch, parallelize, or run multiple planned work items.
- Read `AGENTS.md` and `.project-workflow/guidance.md` if present, then follow the project-workflow managed block and CLI requirements.
- Requirements, clarification, and planning must already be complete before delegation.
- Delegation routes each eligible work item through `project-implement`; it does not bypass validation, QA/code review, or retro.

## Required Files

- `.project-workflow/tasks/<TASK>/REQUIREMENTS.md`
- `.project-workflow/tasks/<TASK>/IMPLEMENTATION.md`
- `.project-workflow/TRACKER.md`
- Repo instruction files such as `AGENTS.md`

## Workflow

1. Identify the task and the requested work items from the user prompt or `IMPLEMENTATION.md`.
2. Read requirements and implementation plan before launching any work.
3. Validate the delegation mode:
   - `sequential` when order matters or mode is omitted
   - `parallel` only when dependencies are explicit and independent items can safely run together
4. Validate dependency maps strictly:
   - no unknown work item IDs
   - no self-dependencies
   - no cycles
5. Route each eligible item through `project-implement` with a clear scope boundary.
6. Use fail-fast launch behavior for new items while allowing in-flight work to finish and report results.
7. After delegated implementation reaches `Testing`, run `project-qa-review` before completion.
8. After completion, run `project-retro` for durable convention or agent updates.
