---
name: project-constitution
description: Use when creating or refining .project-workflow/CONSTITUTION.md with stable product outcomes for a repository.
---
<!-- project-workflow:generated -->

# Project Constitution

Create or update the product outcome guide for the repository.

## Invocation Rules

- Use this skill whenever the user asks for project-workflow constitution work, even if they ask in natural language.
- Read `AGENTS.md` and `.project-workflow/guidance.md` if present, then follow the project-workflow managed block and CLI requirements.
- Do not use the CLI for constitution work unless `.project-workflow/cli/workflow` adds an explicit constitution command.
- If the user asks for implementation or workflow rules while discussing the constitution, put those rules in `.project-workflow/guidance.md` rather than `.project-workflow/CONSTITUTION.md`.

## Required Context

Read these when present:

- `README.md`
- `.project-workflow/TRACKER.md`
- `.project-workflow/guidance.md`
- `.project-workflow/CONSTITUTION.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- Product docs under `docs/**`, `specs/**`, `product/**`, or `roadmap/**`

## Workflow

1. Summarize current product intent from the repo and user brief.
2. If the brief is missing or too vague, ask the minimum questions needed.
3. Create or update `.project-workflow/CONSTITUTION.md`.
4. Keep the constitution outcome-focused and stable. Do not include framework choices, lint rules, folder layouts, or implementation details.
5. Preserve useful existing content while removing technical directives.
6. Use this structure:

```md
# Constitution

## Mission

- <What this project exists to achieve>

## Target Users

- <Primary users>

## Core Outcomes

- <Outcome 1>

## Product Principles

- <Principle>

## Non-Goals

- <What this project should not optimize for>
```

7. If technical workflow guidance is missing, offer to add it to `.project-workflow/guidance.md` rather than the constitution.
