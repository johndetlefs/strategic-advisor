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
   For a full-contract Epic child, also require the parent `epic intent-audit` to be current before
   implementation and refresh it after material child-plan changes. A narrower proxy is not an
   implementation detail merely because the child ACs are internally consistent.
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
11. In workspace mode, keep Git and validation commands repository-scoped and update each touched
    repository's `Repository Evidence` row with branch/PR state, validation, delivery boundary,
    and evidence artifact. Registration is not authority to create branches, commit, push, merge,
    release, or deploy.
12. Run `./.project-workflow/cli/workflow task status --id <TASK-ID> --to Testing` after implementation and validation have run.
13. Run `./.project-workflow/cli/workflow doctor` and report workflow-state warnings or errors.
14. Do not set status to `Complete`; completion is owned by `project-qa-review` after QA/code review passes and the user explicitly asks.
15. Report changed files, validation results, remaining risks, and that `project-qa-review` is the next required lifecycle step.

## Continuation And Validation Sufficiency

- Once the current stage's approved Intent, in-scope acceptance criteria, required proof, and
  validation are satisfied, stop implementation-oriented investigation and advance to the next
  required gate.
- Reopen implementation only when a new finding shows that the owner cannot accomplish the
  approved Intent, a material delivery claim is false, an explicitly required lifecycle stage is
  blocked, or a material safety, security, privacy, data-integrity, or hard-to-reverse risk exists.
  Route adjacent improvements, optional consistency work, speculative hardening, and non-material
  diagnostics to a separate follow-up without implementing them.
- Validate the affected proof layer. Repeat broad or full-suite checks, packaging, deployment, or
  cross-host journeys only when the change can affect that layer or the approved delivery stage
  requires it; do not rerun them merely for additional reassurance.
- After sufficient proof passes, stop. Only an actual later change authorizes one governed
  `workflow validation impact` decision: `unaffected` advances without more validation,
  `affected` names the invalidated proof layer and permits one affected validation pass, and
  `ambiguous` asks the owner one concise clarification question before further investigation.
- A passed affected validation ends continuation work for that change identity. The impact
  decision never creates, broadens, or reopens independent QA; QA remains a separate gate only
  when the approved work item already requires it.
- When the Coordinator declares materially expensive verification, complete implementation before
  any verifier invocation, then execute only the campaign's current stage from cheapest to most
  expensive. A blocking certification failure returns to implementation and forbids later stages;
  extended investigation requires a separate bounded diagnostic campaign. Limits never waive
  missing proof, and unchanged current receipts must be reused.

If requirements conflict with repo constraints or validation is not testable, stop and use `project-clarify`.

When Delegate supplies a bounded worker packet, implement only that unit and return target/unit
identity, exact source, allowed diff, validation, evidence, and stop-condition results. Do not mutate
shared workflow state or lifecycle, create persistent tasks/worktrees, push, merge, release, deploy,
contact others, or write outside the packet. The coordinator must inspect the return before satisfying
dependencies or changing canonical state.
