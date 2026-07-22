---
name: project-backlog
description: Use when capturing, refining, validating, or promoting optional project-workflow backlog items before they become task or epic workflow state.
---
<!-- project-workflow:generated -->

# Project Backlog

Capture future intent in `.project-workflow/BACKLOG.md` before it becomes executable task or epic workflow state.

## Invocation Rules

- Use this skill when the user asks to create, review, refine, validate, accept, defer, reject, supersede, or promote project backlog items.
- Read `.project-workflow/guidance.md` if present, `.project-workflow/CONSTITUTION.md`, `.project-workflow/BACKLOG.md` if present, `.project-workflow/TRACKER.md`, and active epic trackers before drafting candidates from a broad objective.
- Backlog is optional. If the user gives clear immediate implementation scope, `project-task` or `project-epic` can be used directly.
- Do not use backlog rows as implementation lifecycle state.

## Required Files

- `.project-workflow/BACKLOG.md`
- `.project-workflow/CONSTITUTION.md` if present
- `.project-workflow/TRACKER.md`
- `.project-workflow/guidance.md` if present

## Backlog Model

- `CONSTITUTION.md` records durable product outcomes and principles.
- `BACKLOG.md` records future intent, rough priority, options, and promotion history.
- `TRACKER.md` and epic trackers record committed execution lifecycle state.
- Task/epic folders record executable requirements, plans, validation evidence, QA, and retros.

Allowed type values: `Idea`, `Task Candidate`, `Epic Candidate`, `Discovery`, `Follow-Up`.

Allowed priority values: `High`, `Medium`, `Low`, `Unset`.

Allowed status values: `Proposed`, `Accepted`, `Deferred`, `Rejected`, `Superseded`, `Promoted`.

`Accepted` means worth keeping or preparing; it does not mean ready to implement.

Promoted rows stay in the backlog with status `Promoted` and `Promoted To` set to the created task or epic ID.

Existing roadmap/backlog documents outside `.project-workflow/BACKLOG.md` must be preserved. Do not import or transform them automatically; create a repo-local migration task if needed.

## Workflow

1. For broad objectives, read project context first and draft outcome-focused candidate rows.
2. Recommend whether each candidate should remain an idea, become a task, become an epic, or require discovery.
3. Do not create tracker rows, task folders, or epic folders while only proposing backlog candidates.
4. Ask for owner review before accepting or promoting rows.
5. If context is insufficient, ask focused questions instead of inventing strategy.
6. Use the CLI for deterministic row operations.

## CLI

Initialize backlog if missing:

```bash
./.project-workflow/cli/workflow backlog init
```

Add a row:

```bash
./.project-workflow/cli/workflow backlog add --title "<TITLE>" --outcome "<OUTCOME>" --type "Idea" --priority Unset
```

List rows:

```bash
./.project-workflow/cli/workflow backlog list
```

Update status:

```bash
./.project-workflow/cli/workflow backlog status --id BL-001 --to Accepted
```

Update fields:

```bash
./.project-workflow/cli/workflow backlog update --id BL-001 --priority High --notes "<NOTES>"
```

Validate backlog:

```bash
./.project-workflow/cli/workflow backlog validate
```

Promote an accepted row:

```bash
./.project-workflow/cli/workflow backlog promote --id BL-001 --to task
./.project-workflow/cli/workflow backlog promote --id BL-001 --to epic
```

Use `--accept` only when the owner explicitly confirms accepting and promoting in one operation.

## Output

- Report commands run.
- Summarize created or updated rows.
- For promotion, report the created task/epic ID and generated files.
- Run `./.project-workflow/cli/workflow doctor` after promotion or structural backlog edits and report warnings/errors.
