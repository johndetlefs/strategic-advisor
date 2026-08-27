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
- If a material verification campaign exists, its derived state must be `qa-required` (or already
  `delivery-ready`) before Review. A `verification-required` or `blocked` state returns to the
  Coordinator; QA must not start, broaden, or restart that campaign.
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
   For `user-outcome-journey`, inspect the exact actor, normal entry point, starting state, material
   operations, resulting artifact/state, observations, source/revision, environment and invalid
   substitutes. Tests, builds, screenshots, internal data, debug-only controls, related
   environments and one canary cannot alone prove a broader user job.
7. Run any missing narrow validation needed to support the review. Do not ask the user to manually test behavior that the agent can validate directly with available commands, tests, scripts, or local tools.
8. Review the changed code for correctness, scope control, maintainability, edge cases, tests, docs, security, permissions, privacy, data integrity, and operational risk.
9. In workspace mode, verify every touched repository has an explicit `Repository Evidence` row
   and that its branch/PR, validation, delivery, and evidence claims match repository-scoped
   read-only Git/status proof. Treat `not applicable` and `not authorized` as boundaries, not as
   delivered proof.
10. Record results in `IMPLEMENTATION.md` under `## QA & Code Review` with date, reviewed areas, validation evidence, findings, and verdict. Clearly separate verified evidence from deferred setup, owner-only actions, unavailable connector/OAuth checks, and invalid substitutes.
    For an adversarial Intent QA contract, also record `Intent adversarial verdict`, answer whether
    every AC could pass while the approved user job remains undone, record the current Intent audit,
    cite outcome-journey evidence, and state reviewer independence. If the answer is Yes or unknown,
    the only honest verdict is `Changes requested`.
11. Run `./.project-workflow/cli/workflow doctor` and include any workflow-state warnings or errors in the review output.
12. If findings exist, report them first with severity and file references. Keep status as `Review` or set `Blocked` for release-blocking issues.
    Preserve the independent `Changes Requested` and adversarial answers as issued. After the named
    fixes, record one `workflow validation impact` decision as `affected`, include `qa-review`, and
    set its validation verdict from the affected evidence. A passing final disposition also records
    `Findings disposition: Resolved`, `Affected validation verdict: Pass`, whether the user job can
    still remain undone (`No`), substantive affected-validation evidence, and
    `Second QA commissioned: No`. This closes the original gate; it is not a new QA verdict.
13. If review passes, say so. Run `./.project-workflow/cli/workflow task status --id <TASK-ID> --to Complete` only when the user explicitly asks to complete the task after review.
14. After completion, route to `project-retro`.

## Continuation And Validation Sufficiency

- Once the approved Intent, in-scope acceptance criteria, required proof, and QA verdict pass, stop
  review-oriented investigation and report the result.
- Continue or reopen work only when a finding shows that the owner cannot accomplish the approved
  Intent, a material delivery claim is false, an explicitly required lifecycle stage is blocked,
  or a material safety, security, privacy, data-integrity, or hard-to-reverse risk exists. Record
  adjacent improvements, optional consistency work, speculative hardening, and non-material
  diagnostics as separate follow-ups instead of extending the current review.
- Identify the affected proof layer for every blocking finding. Rerun broad or full-suite checks,
  packaging, deployment, or cross-host journeys only when the correction can affect that layer or
  the approved delivery stage requires it; do not repeat them merely for additional reassurance.
- A post-proof `workflow validation impact` decision never commissions another review. An
  `unaffected` decision advances, an `affected` decision permits one named validation pass, and an
  `ambiguous` decision returns one concise question to the owner.
- Run independent QA once for the approved work item when its requirements require that gate.
  Findings may trigger affected validation, but never a fresh open-ended review. Another reviewer
  invocation requires a new material change, an explicit high-consequence requirement, or direct
  owner authorization.
- QA may run a planned narrow check needed for its verdict, but it cannot schedule materially
  expensive verification. Missing campaign proof returns as `verification-required`; corrections
  close through one affected validation disposition, while the original independent verdict is
  retained and no second QA is commissioned.
- Completion accepts either the original independent `Pass` or a preserved `Changes Requested`
  verdict whose named findings have the exact passing affected-validation disposition above.
  Missing, pending, self-contradictory, or unevidenced resolution remains blocked.

## Verdicts

- `Pass`: no blocking findings and validation evidence covers the acceptance criteria by AC ID.
- `Pass with follow-ups`: safe to complete, but separate follow-up work is recommended.
- `Changes requested`: completion is blocked until findings are addressed and the one affected-
  validation disposition passes; do not overwrite it with a fictional independent `Pass`.

For delegated work, independently inspect coordinator-verified worker identity, exact source/worktree,
allowed diff, validations, evidence, capability/capacity provenance, descendant blocking, runtime
privacy, and single-writer behavior. Neither worker assertions nor Delegate's aggregate report replace
this QA gate.
