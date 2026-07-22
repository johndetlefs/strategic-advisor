---
name: project-retro
description: Use after a project-workflow task is complete to update durable conventions, agent guidance, and follow-up tasks.
---
<!-- project-workflow:generated -->

# Project Retro

Run the post-completion retro for a project-workflow task.

## Invocation Rules

- Use this skill whenever the user asks for a retro, retrospective, lessons learned, convention updates, agent updates, prompt updates, or post-completion cleanup for a project-workflow task.
- Read `AGENTS.md` and `.project-workflow/guidance.md` if present, then follow the project-workflow managed block and CLI requirements.
- Only run after QA/code review has passed and the task is marked `Complete`.
- Retro is a maintenance workflow unless the CLI adds an explicit retro command.

## Required Files

- `.project-workflow/tasks/<TASK>/REQUIREMENTS.md`
- `.project-workflow/tasks/<TASK>/IMPLEMENTATION.md`
- `.project-workflow/TRACKER.md`
- Repo instruction files and agent assets such as `AGENTS.md`, `.github/copilot-instructions.md`, `.github/prompts/`, `.agents/skills/`, and `.cursor/rules/` when present

## Workflow

1. Infer the task ID from the user prompt or current branch if possible. Ask only if it cannot be inferred.
2. Read the completed task docs, QA/code review notes, tracker row, final diff, and repo guidance.
3. Confirm the task is `Complete`. If not, stop and route to `project-qa-review`.
4. Identify reusable lessons:
   - repo conventions or coding patterns that should be documented
   - validation or QA checks that should become standard
   - agent prompt, skill, or rule gaps that caused drift or rework
   - follow-up work that should become a separate task
   - missed in-scope work that should have blocked completion unless explicitly deferred
5. Update the narrowest durable guidance file that owns each lesson. Do not add one-off task details to global instructions.
6. Record the retro in `IMPLEMENTATION.md` under `## Retro` with date, lessons, updated assets, follow-up suggestions, and a separate note for any missed in-scope work.
7. Leave tracker status as `Complete` unless the user explicitly asks to reopen the task.

## Placement Rules

- Product outcome changes belong in `.project-workflow/CONSTITUTION.md`.
- Technical workflow conventions belong in `.project-workflow/guidance.md`, or the narrowest equivalent repo guidance file.
- Copilot workflow behavior belongs in `.github/prompts/*.prompt.md`.
- Codex workflow behavior belongs in `.agents/skills/project-*/SKILL.md`.
- Cursor workflow behavior belongs in `.cursor/rules/project-workflow.mdc`.
- Packaged project-workflow behavior belongs in `src/project_workflow/**` when working in this repository.
