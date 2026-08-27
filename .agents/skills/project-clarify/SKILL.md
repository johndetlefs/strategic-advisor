---
name: project-clarify
description: Use when project-workflow requirements, implementation plan, repo constraints, or user intent conflict or need clarification.
---
<!-- project-workflow:generated -->

# Project Clarify

Resolve material ambiguity at three bounded points: before approval, after planning/decomposition,
or when the Coordinator routes a concrete mid-execution drift question. Clarify is a decision aid,
not periodic review.

## Invocation Rules

- Use this skill whenever the user asks to clarify, resolve ambiguity, reconcile conflicting requirements, or decide between unclear options for a project-workflow task, even if they ask in natural language.
- Read `AGENTS.md` and `.project-workflow/guidance.md` if present, then follow the project-workflow managed block and CLI requirements.
- If the work-item folder does not exist, use `project-task` or `project-epic` first when tracked
  work is needed.
- Clarification is a document workflow unless the CLI adds an explicit clarify command.

## Required Files

- `.project-workflow/tasks/<WORK-ITEM>/REQUIREMENTS.md`
- For a Task or Epic child: `IMPLEMENTATION.md` when present
- For an Epic parent: `EPIC-CONTRACT.md` and `DECOMPOSITION.md` when present; a parent
  `IMPLEMENTATION.md` is not required
- `.project-workflow/CONSTITUTION.md` if present
- Repo instruction files such as `AGENTS.md` or `.github/copilot-instructions.md`

## Modes

- `pre-approval`: resolve material product or authority questions before the owner confirms the
  requirements meaning.
- `post-plan`: compare a Task plan or Epic decomposition with approved Intent, requirements,
  boundaries, acceptance criteria, and proof obligations.
- `drift-ambiguity`: only when the Coordinator has identified a concrete ambiguity at an execution
  boundary and cannot classify it safely from current authority.

## Workflow

1. Read the substantive `## Intent` or `## Intent Spine` in `REQUIREMENTS.md` and treat approved
   requirements as the outcome authority. For an Epic parent, also read `EPIC-CONTRACT.md` and the
   decomposition when present. For a Task or child, read the User Story and plan when present.
2. Stop for requirements capture only when neither substantive Requirements Intent nor a usable
   User Story exists. Do not require a parent Epic to have `IMPLEMENTATION.md`.
3. Reuse relevant owner answers already present in conversation or repository evidence. Do not ask
   the owner to repeat them.
4. Cross-check only ambiguities or conflicts that could materially affect outcome, scope, safety,
   security, billing, data correctness, authority, validation, proof, or user-visible behavior.
5. In `pre-approval` mode, record each material ambiguity in `REQUIREMENTS.md` as a numbered open
   question with:
   - the conflict or missing decision
   - why it matters
   - 2 to 4 actionable options
6. Ask one unresolved material question at a time unless the user explicitly wants batching. If
   current authority answers it, record the resolution and continue without asking.
7. After the user answers, immediately update `REQUIREMENTS.md` decisions and open questions.
8. Preserve existing acceptance criteria IDs (`AC1`, `AC2`, etc.) when updating
   requirements. Do not renumber ACs unless the user explicitly approves that
   requirements change.
9. Keep the applicable plan or decomposition aligned with confirmed decisions, including affected
   AC-to-row or AC-to-child mappings.
10. During a `post-plan` pass, resolve implementation-detail inconsistencies inside the approved
    envelope autonomously. A clear narrowing, omission, or proxy substitution against unchanged
    approved Intent is `drift-detected`: restore the approved capability without asking the owner
    to repeat it. Return to the owner only for an unresolved material choice or a genuine proposed
    change to requirements, ACs, proof obligations, artifact identity, scope, or authority.
11. In `drift-ambiguity` mode, return exactly one classification to the Coordinator after the
    evidence is sufficient: `inside-envelope`, `drift-detected`, or `approved-change`. Name the
    controlling requirement and consequence. When existing authority cannot classify a material
    ambiguity, ask one focused owner question first and do not prematurely label it drift or an
    approved change; return the classification after the answer is recorded.
12. When a Task post-plan pass is clean, run `task ready`, move the task to `Ready`, and continue
    when implementation is authorized. For an Epic parent, return a clean result to the Coordinator;
    Epic readiness/decomposition commands retain lifecycle ownership.
13. For a full-contract Epic parent or child, run the parent `epic intent-audit` read-only and treat stale,
    unknown, review-required or changes-requested state as a real narrowing or coverage gap. Name
    the exact user-visible capability consequence; AC consistency is not Intent fidelity.
14. Clarify does not monitor boundaries, launch work, run QA, create review loops, or write shared
    tracker/evidence/lifecycle state. The Coordinator owns drift detection and state changes.
