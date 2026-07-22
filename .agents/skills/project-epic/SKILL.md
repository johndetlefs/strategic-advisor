---
name: project-epic
description: Use when creating, decomposing, approving, or scaffolding proposal-first project-workflow epics.
---
<!-- project-workflow:generated -->

# Project Epic

Manage proposal-first epic work under `.project-workflow/tasks/`.

## Invocation Rules

- Use this skill whenever the user asks for an epic, epic decomposition, proposed child work, approval of epic rows, or scaffolding an approved epic child task.
- Read `AGENTS.md` and `.project-workflow/guidance.md` if present, then follow the project-workflow managed block and CLI requirements.
- Use the local workflow CLI for every supported epic operation.
- Do not scaffold child task folders until the relevant epic tracker row is `Approved`.

## Workflows

Create a new epic:

```bash
./.project-workflow/cli/workflow epic init --title "<TITLE>"
```

Decompose an epic into proposed child rows only:

```bash
./.project-workflow/cli/workflow epic approve-requirements --epic-id <EPIC-ID> --approved-by "<OWNER>" --source "<APPROVAL SOURCE>"
./.project-workflow/cli/workflow epic decompose --epic-id <EPIC-ID> --limit 5 --type Task
```

Approve one proposed child row:

```bash
./.project-workflow/cli/workflow epic approve --epic-id <EPIC-ID> --id <TASK-ID>
```

Scaffold one approved child row:

```bash
./.project-workflow/cli/workflow epic scaffold-child --epic-id <EPIC-ID> --id <TASK-ID>
```

Scaffold one approved child row with a branch from an existing epic branch:

```bash
./.project-workflow/cli/workflow epic scaffold-child --epic-id <EPIC-ID> --id <TASK-ID> --create-branch --epic-branch <EPIC-BRANCH>
```

Move one epic tracker row through lifecycle statuses:

```bash
./.project-workflow/cli/workflow epic status --epic-id <EPIC-ID> --id <TASK-ID> --to Testing
./.project-workflow/cli/workflow epic status --epic-id <EPIC-ID> --id <TASK-ID> --to Review
./.project-workflow/cli/workflow epic status --epic-id <EPIC-ID> --id <TASK-ID> --to Complete
```

Generate an epic acceptance audit:

```bash
./.project-workflow/cli/workflow epic audit --epic-id <EPIC-ID>
```

Validate epic requirements before decomposition:

```bash
./.project-workflow/cli/workflow epic ready --epic-id <EPIC-ID>
```

Move the global epic row through the minimal epic lifecycle:

```bash
./.project-workflow/cli/workflow epic lifecycle --epic-id <EPIC-ID> --to Ready
./.project-workflow/cli/workflow epic lifecycle --epic-id <EPIC-ID> --to "In Progress"
./.project-workflow/cli/workflow epic lifecycle --epic-id <EPIC-ID> --to Closeout
```

Validate one child task before implementation/testing:

```bash
./.project-workflow/cli/workflow epic ready-child --epic-id <EPIC-ID> --id <TASK-ID>
```

Validate epic closeout, optionally completing the global epic row when gates pass:

```bash
./.project-workflow/cli/workflow epic closeout --epic-id <EPIC-ID> [--complete]
```

## Rules

- `epic init` creates an epic `REQUIREMENTS.md`, `EPIC-CONTRACT.md`, epic `TRACKER.md`, `DEFERRALS.md`, `AMENDMENTS.md`, `RETRO.md`, and `ACCEPTANCE-MAP.md`.
- `ACCEPTANCE-MAP.md` is a working parent AC coverage view derived from requirements, epic tracker rows, deferrals, and child evidence. Epic lifecycle commands refresh it when coverage state changes.
- Epic acceptance criteria should use stable IDs (`AC1`, `AC2`, etc.).
- `epic ready` must pass before decomposition; if it fails, ask the owner only for missing product decisions/context and record answers in `REQUIREMENTS.md`.
- `epic approve-requirements` records the owner-approved authority envelope once requirements/ACs are ready. Do not require repeated owner approval for unchanged child rows inside that envelope.
- Approval gates are drift checks. If a gate fails, fix the concrete stale-requirements, out-of-envelope, or evidence gap unless an actual amendment/deviation decision is needed.
- `EPIC-CONTRACT.md` records sources of truth, invalid substitutes, invariants, artifact targets, and parent AC proof owners. New/adopted epics must replace placeholder contract content before decomposition, child approval/scaffolding, or movement into `Ready`/`In Progress`.
- `epic lifecycle` updates the global epic row through `Analysing`, `Ready`, `In Progress`, and `Closeout`. `Ready`, `In Progress`, and `Closeout` are gated; `Complete` remains owned by `epic closeout --complete`.
- `epic decompose` writes Proposed child rows and `DECOMPOSITION.md`, the approved child-row authority plan. It does not create child task folders.
- If requirements include a `Proposed Child Work` table, `epic decompose` uses that owner-reviewed decomposition before falling back to generated requirement/AC candidates.
- `epic decompose` reads `.project-workflow/config.json` namespace and ID generation guidance by default and may produce mixed child prefixes such as `MCP-001` or `UI-K7F3Q`; use `--prefix <PREFIX>` only for an explicitly homogeneous batch.
- Proposed child rows should preserve source AC IDs in the epic tracker `Parent ACs` field when they come from numbered acceptance criteria. Legacy trackers may still carry coverage in `Notes` as `Covers AC1, AC3`.
- `epic approve`, `epic scaffold-child`, `epic ready-child`, and `epic status` reject child rows whose ID, title, or parent AC coverage does not match `DECOMPOSITION.md`; matching rows inside the plan do not need separate per-row owner approval.
- `epic amend` records an owner-approved amendment in `AMENDMENTS.md` and appends the matching Proposed child row. Use it for mid-epic reactive fixes, new child work, or material changes outside the approved decomposition plan; direct tracker edits remain blocked.
- `epic adopt` brings pre-existing epics under current approval gates with a `Legacy Adoption` block. Pre-adoption inferred evidence is untrusted unless `--evidence-refreshed` is used after proof has been rerun.
- `epic scaffold-child` only accepts `Approved` child rows and moves them to `In Progress` after scaffold. It copies parent AC coverage plus a contract-derived `Child Charter` into the child docs.
- `epic scaffold-child` also creates child-local `EVIDENCE.json`. Fill it when requirements or material claims trigger a proof recipe.
- Built-in proof recipes are `visual-reference-fidelity`, `external-contract-alignment`, `deployed-artifact-alignment`, `runtime-target-source`, and `responsive-visual-behavior`.
- When a proof recipe is triggered, `epic status` blocks `Review`/`Complete`, `epic audit` refuses parent AC credit, and `doctor` fails invalid current states until `EVIDENCE.json` has passing structured claim records with recipe-specific fields and evidence artifacts.
- Invalid substitutes are rejected. Visual/reference fidelity needs rendered comparison against the delivered user-facing artifact, not code review, tests, build output, or surrogate surfaces. Runtime target/source proof needs the exact execution target, source/artifact under test, observation method, and positive proof that the target used that source.
- `epic status` moves planned child rows through `Testing`, `Review`, and `Complete`; `Complete` requires QA/code-review evidence and parent AC evidence.
- Scaffolded epic child task docs must include parent AC coverage, child charter, and parent AC evidence sections. Their implementation plans must map every task row to one or more stable child AC IDs and keep the parent AC mapping visible.
- `epic ready-child` must pass before implementation/testing; if it fails, remediate missing child requirements, planning, validation, parent AC coverage, or owner decisions first.
- The global tracker summarizes epic rows; the epic tracker owns child rows. Proposed child rows must stay in the epic tracker and must not be added to the global tracker.
- `epic audit` writes `ACCEPTANCE-AUDIT.md` with parent AC coverage, child evidence, deferrals, and verdicts. The audit is the closeout evidence artifact; the acceptance map is the in-progress coverage view.
- `epic closeout` must block if any parent AC is unmapped, lacks evidence, lacks a QA pass verdict, lacks an approved deferral with follow-up, or if `RETRO.md` is missing/incomplete.
- `RETRO.md` must record lessons, follow-up tasks, deferrals, and missed in-scope work before closeout. Explicit `None.` entries are valid when there is nothing to report.
- Child IDs remain globally unique within their configured task prefix namespaces across standalone and epic-managed work.
- When `--create-branch` is used, the epic branch must already exist; do not fall back to a base branch.
- After any epic tracker or child scaffold change, run `./.project-workflow/cli/workflow doctor` and report workflow-state warnings or errors.
