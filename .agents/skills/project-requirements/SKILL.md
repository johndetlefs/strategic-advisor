---
name: project-requirements
description: Use when drafting or updating project-workflow REQUIREMENTS.md with user story, scope, acceptance criteria, decisions, and open questions.
---
<!-- project-workflow:generated -->

# Project Requirements

Capture what is being built before planning or coding.

Project Workflow is owner-directed and agent-operated. The owner provides product context and decisions conversationally; the agent extracts them into workflow artifacts and asks focused questions only when needed.

Requirements capture must end with one explicit owner confirmation that the brief Intent
accurately reflects what they mean. Present the Intent, completion capability, exclusions and
proof journey before detailed requirements; do not ask the owner to approve IDs, hashes or a
document bundle as a substitute for meaning. Record that authority with `task approve-requirements`
or `epic approve-requirements` after confirmation. Do not treat an agent draft, silence, or
implementation request as approval. After approval, normally continue autonomously through
Planner, post-plan Clarify, `task ready`, and `Ready`; pause only for material drift, exceptional
authority, requested/high-risk plan review, or an explicit setup-only boundary.

## Invocation Rules

- Use this skill whenever the user asks for requirements, scope, acceptance criteria, open questions, decisions, or a validation plan, even if they ask in natural language.
- Read `AGENTS.md` and `.project-workflow/guidance.md` if present, then follow the project-workflow managed block and CLI requirements.
- If the task folder does not exist, use `project-task` first so the CLI creates the required files and tracker row.
- After the task exists, requirements capture is a document workflow unless the CLI adds an explicit requirements command.

## Required Files

- `.project-workflow/tasks/<TASK>/REQUIREMENTS.md`
- `.project-workflow/tasks/<TASK>/IMPLEMENTATION.md`
- `.project-workflow/CONSTITUTION.md` if present
- `.github/copilot-instructions.md` or `AGENTS.md` if present

## Workflow

1. Identify the task folder. If it does not exist, use `project-task` first.
2. Read existing `REQUIREMENTS.md` and the `## User Story` section of `IMPLEMENTATION.md`.
3. If the feature or bugfix is not clear, ask only for discovery context: what change, where in the product, who is affected, and what success looks like.
   Minimum context should cover problem/opportunity, desired outcome, affected user or system, scope boundaries, acceptance signal, constraints, priority/risk, and examples or failure modes.
4. Draft or update `REQUIREMENTS.md` with:
   - A one- or two-sentence plain-language `## Intent` stating the owner's desired outcome
   - An `## Intent Spine` with stable outcome commitments for completion capability, material
     capabilities, success journey, successful-but-wrong result, exclusions, assumptions and
     authority source when the full intent contract is triggered
   - Overview
   - User Story
   - Goal
   - Non-Goals
   - Users & Context
   - Repository Scope with one registered primary repository and every registered repository
     touched when `.project-workflow/config.json` declares workspace mode
   - Outcome-focused requirements
   - Verifiable acceptance criteria with stable IDs (`AC1`, `AC2`, etc.)
   - Open questions
   - Resolved decisions
   - Validation plan
5. Preserve existing AC IDs when requirements change. Do not renumber existing
   ACs unless the user explicitly approves the requirements change.
6. If requirements mention matching a visual/reference, deployed/runtime behavior, external contract, or responsive/multi-context behavior, record the relevant proof recipe, artifact identity, and invalid substitutes in the validation plan.
7. In workspace mode, use repository IDs from the parent registry. Do not create child workflow
   trackers, and do not treat repository registration as authority for Git or delivery mutations.
8. Keep only the `## User Story` section in `IMPLEMENTATION.md` synced with `REQUIREMENTS.md`. Do not add implementation tasks here.
9. If critical requirements are ambiguous, record them as open questions in `REQUIREMENTS.md`, then ask the user the minimum questions needed.
10. Do not proceed to planning or implementation until open questions are resolved or explicitly accepted as risks and recorded.
11. After requirements and ACs are complete, run `task approval-summary` or
    `epic approval-summary` and present its meaning-first synopsis. Ask: "Does this Intent
    accurately capture what you want and what success means?" Do not replace that question with
    a request to approve task IDs, AC IDs or artifact hashes. After confirmation, record approval
    with the workflow CLI; the artifact identity is provenance behind the approved meaning.
    Downstream work inside that unchanged envelope should not ask for repeated approval.
12. After approval, move to `Analysing`, run `project-planner`, run a post-plan
    `project-clarify` pass, validate with `task ready`, and move to `Ready` without another generic
    approval request.
13. If the work is intentionally exploratory, record it as discovery with a question, decision enabled, boundary, output artifact, and validation signal.
