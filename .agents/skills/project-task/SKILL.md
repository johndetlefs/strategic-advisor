---
name: project-task
description: Use when creating a new project-workflow task folder, tracker row, and optional branch for a feature or bugfix.
---
<!-- project-workflow:generated -->

# Project Task

Create the minimal workflow artifacts for one new task.

Project Workflow is owner-directed and agent-operated: the owner provides product context and decisions conversationally, while the agent runs commands and records workflow state.

Task creation is only scaffolding. Requirements and ACs still need one explicit owner confirmation
before planning; record that confirmation with `task approve-requirements` after requirements are
ready. The agent then normally plans, clarifies, validates readiness, and moves to `Ready`
autonomously. Do not repeatedly ask for approval inside the unchanged envelope.

## Invocation Rules

- Use this skill whenever the user asks to create a project-workflow task, story, feature folder, tracker row, or new tracked work item, even if they ask in natural language.
- Read `AGENTS.md` and `.project-workflow/guidance.md` if present, then follow the project-workflow managed block and CLI requirements.
- The local workflow CLI is mandatory for supported task scaffold operations. Do not manually create task folders, starter files, or tracker rows when the CLI command is available.
- If another project-workflow skill needs a task folder that does not exist, route through this skill first.

## Inputs

Determine these from the user prompt, current branch, or follow-up questions:

- Task title, such as `Account Usage Export`
- Whether to create a branch
- If creating a branch: base branch, default `develop`, and branch prefix, default `feature/`

Minimum context to gather before planning or implementation:

- Problem or opportunity
- Desired outcome
- Affected user, actor, or system
- Scope boundaries and non-goals
- Acceptance signal for done
- Constraints, priority/risk, and examples or failure modes

## Workflow

1. Confirm `.project-workflow/TRACKER.md` exists. If missing, tell the user to run `project init` first.
2. If creating a branch, ensure the working tree is clean before switching branches.
3. Run the local scaffolder from the repo root and let it assign the next ID.
   Repositories may choose task ID namespaces and ID generation in
   `.project-workflow/config.json`; pass `--prefix <PREFIX>` only when the user
   or repo guidance calls for a configured non-default prefix.

Without branch:

```bash
./.project-workflow/cli/workflow task init --title "<TITLE>" --update-tracker
```

Configured prefix:

```bash
./.project-workflow/cli/workflow task init --prefix <PREFIX> --title "<TITLE>" --update-tracker
```

With branch:

```bash
./.project-workflow/cli/workflow task init --title "<TITLE>" --update-tracker --create-branch --base-branch <BASE> --branch-prefix <PREFIX>
```

4. Run `./.project-workflow/cli/workflow doctor` and report any workflow-state warnings or errors.
5. Report the created task folder, assigned task ID, tracker update, and branch name if one was created.
6. Continue to requirements capture when the user is ready, then proceed through owner
   confirmation, `task approve-requirements`, planning, post-plan clarification, `task ready`,
   `Ready`, implementation, QA/code review, and retro. Pause after scaffolding only when the user
   explicitly requested setup/review-only work.
