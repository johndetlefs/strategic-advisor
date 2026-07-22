---
name: project-clarify
description: Use when project-workflow requirements, implementation plan, repo constraints, or user intent conflict or need clarification.
---
<!-- project-workflow:generated -->

# Project Clarify

Resolve ambiguity before planning or implementation continues. Also run this skill after Planner
as the normal autonomous consistency pass.

## Invocation Rules

- Use this skill whenever the user asks to clarify, resolve ambiguity, reconcile conflicting requirements, or decide between unclear options for a project-workflow task, even if they ask in natural language.
- Read `AGENTS.md` and `.project-workflow/guidance.md` if present, then follow the project-workflow managed block and CLI requirements.
- If the task folder does not exist, use `project-task` first when a tracked task is needed.
- Clarification is a document workflow unless the CLI adds an explicit clarify command.

## Required Files

- `.project-workflow/tasks/<TASK>/REQUIREMENTS.md`
- `.project-workflow/tasks/<TASK>/IMPLEMENTATION.md`
- `.project-workflow/CONSTITUTION.md` if present
- Repo instruction files such as `AGENTS.md` or `.github/copilot-instructions.md`

## Workflow

1. Read the `## User Story` section from `IMPLEMENTATION.md`.
2. Read `REQUIREMENTS.md` and treat it as the source of truth for agreed outcomes and decisions.
3. Cross-check for ambiguities or conflicts that affect scope, safety, security, billing, data correctness, validation, or user-visible behavior.
4. If the user story is missing or unusable, stop and direct the user to run requirements capture first.
5. Record each ambiguity in `REQUIREMENTS.md` as a numbered open question with:
   - the conflict or missing decision
   - why it matters
   - 2 to 4 actionable options
6. Ask one unresolved question at a time unless the user explicitly wants batching.
7. After the user answers, immediately update `REQUIREMENTS.md` decisions and open questions.
8. Preserve existing acceptance criteria IDs (`AC1`, `AC2`, etc.) when updating
   requirements. Do not renumber ACs unless the user explicitly approves that
   requirements change.
9. Keep `IMPLEMENTATION.md` aligned with confirmed decisions, including any
   AC-to-task mapping affected by the decision.
10. Repeat until no unresolved blocking questions remain or the user explicitly accepts remaining risks.
11. During a post-plan pass, resolve implementation-detail inconsistencies inside the approved
    envelope autonomously. If resolution changes requirements, ACs, proof obligations, artifact
    identity, or scope materially, return the changed envelope to the owner for re-approval.
12. When the post-plan pass is clean, run `task ready`, move the task to `Ready`, and continue when
    implementation is authorized.
