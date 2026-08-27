---
name: project-delegate
description: Use when coordinating approved Task implementation rows or Epic child Tasks through a capability-aware dependency graph.
---
<!-- project-workflow:generated -->

# Project Delegate

Compatibility entry: `project-coordinator` is the owner-facing role. Invoking Delegate enters that
same Coordinator contract for an already-approved execution graph; it does not create a second role
or shared-state writer. This entry is retained for the first Coordinator release and becomes
removal-eligible only after one full minor release and observed migration evidence.

Coordinate existing execution units for exactly one approved Task or Epic. Delegate executes authority already recorded in requirements and the canonical plan; it never creates scope, approves requirements, invents rows/children, or batches unrelated standalone Tasks.

## Invocation Rules

- Use this skill whenever the user asks to delegate, coordinate, batch, parallelize, monitor, resume, or run multiple planned work items.
- Read `AGENTS.md`, `.project-workflow/guidance.md`, target requirements, and the canonical implementation or decomposition plan first.
- Requirements, clarification, approval, and planning must already be complete. Use an Epic for coordinated standalone Tasks.
- Delegation does not bypass Implement, independent QA/code review, evidence, audit, retro, owner acceptance, or delivery gates.

## Property-Based Selection

For each canonical unit, read or conservatively derive its execution needs. Supported tokens are:

- `bounded-return` or blank legacy metadata: a result that can return within the current coordinator session;
- `durable-resume`: work must survive coordinator/session interruption;
- `direct-owner-steering`: the owner must be able to interact with the child directly;
- `isolated-worktree`: filesystem isolation is binding;
- `peer:<group-id>`: workers in that group require direct peer communication.

Also enforce `Parallel Safe`, write scope, repository scope, dependencies, evidence, and validation. Target kind is context, not executor policy: an Epic child may use a subagent, and a Task row may use a persistent task when its binding needs require one.

Choose the lightest sufficient surface:

- `coordinator` for coupled, unsafe, sequential, or safely downgraded work;
- `subagent` for bounded coordinator-mediated work, using an isolated subagent only when that distinct capability is verified;
- `persistent-task` for authorised durable, direct-owner-steered, or isolated ownership that cannot be satisfied by a verified subagent surface;
- `peer-team` only for an explicit `peer:<group-id>` need and verified peer-team plus peer-messaging support.

Ordinary dependency graphs stay coordinator-mediated. Do not select a team merely because several units can run in parallel.

For current-contract plans, verified capacity never earns a non-Coordinator surface by itself.
Every such unit must declare `benefit:<slug>`, `overhead:<slug>`, and `tradeoff:<slug>` in Execution
Needs. Missing basis defaults non-binding work to Coordinator/sequential and blocks a binding
surface need. The benefit cannot override dependency, scope, authority, or capability failure.

## Capability And Authority Gate

Inspect tools callable in this current Codex session. Resolve every relevant capability as `verified`, `unsupported`, or `unknown`, with dated observation provenance (`YYYY-MM-DD`):

- `subagent` and available child slots;
- `subagent-isolated-worktree`;
- `persistent-task`, persistent `isolated-worktree`, `persistent-task-owner-steering`, `task-monitoring`, and `task-reconciliation`;
- `peer-team` and `peer-messaging`;
- `task-retirement` and `task-retirement-reconciliation`.

Only current-runtime `verified` capability authorises native launch or retirement. Installed guidance, repository tests, fixtures, another session, or one available tool do not prove a complete capability set or general Codex support. `unsupported` and `unknown` fail closed for that path.

Creating a persistent Codex task requires explicit owner authority applicable to the current request plus verified task creation, isolated-worktree creation for every persistent Codex child, monitoring, reconciliation, task retirement, and retirement reconciliation. Task or Epic approval alone is not task-creation authority. If a native surface is unavailable, use sequential/coordinator work only when it still satisfies every binding need; otherwise block with the exact unmet property.

Never hard-code four workers or any other fixed capacity. Effective child concurrency is bounded by requested concurrency, observed free child slots excluding the coordinator, eligible units, dependency readiness, and collision-free parallel-safe scopes.

## Required Files

- `.project-workflow/tasks/<TASK>/REQUIREMENTS.md`
- `.project-workflow/tasks/<TASK>/IMPLEMENTATION.md`, or the target Epic's `DECOMPOSITION.md` and tracker
- `.project-workflow/TRACKER.md`
- child-local `EVIDENCE.json` when a proof recipe applies
- repo instructions such as `AGENTS.md`

## Workflow

1. Identify exactly one target and optional dependency-closed unit subset. Reject mixed targets and arbitrary Task batches.
2. Run `./.project-workflow/cli/workflow delegate plan --id <TARGET>` or `delegate status`, passing only current-runtime observed capabilities/provenance, observed capacity, execution needs, and explicit persistent-task authority. Planning and status are read-only: they do not launch or retire work.
3. Validate approved lifecycle, canonical graph, unknown/self/cyclic dependencies, subset closure, execution needs, `Write Scope`, `Parallel Safe`, and current shared baseline before launch.
4. Keep one coordinator as the only writer of shared trackers, implementation-row status, acceptance maps, evidence indexes, delegation runtime state, and target lifecycle.
5. Give each executor a bounded packet containing target/unit identity, acceptance criteria, dependencies, repository/write scope, required validation/evidence, forbidden actions, stop conditions, exact source revision, and return format.
6. Workers may not push, merge, release, deploy, contact others, create unapproved persistent tasks/worktrees, mutate shared workflow state, or write outside the packet.
7. Launch only eligible units on their selected surface. A failed unit blocks its descendants. Unrelated work continues only while the shared baseline and premises remain valid.
8. Treat dependencies as satisfied only after coordinator inspection verifies returned identity, source/worktree, allowed diff, validation, and evidence. A worker completion claim is not proof. Reconcile missing, duplicate, stale, orphaned, or mismatched handles before integration or status changes.
9. Assign each unit a visibility class: `ephemeral`, `visible-retirable`, or `visible-retained`. Temporary persistent children default to `archive-on-verified`; direct-owner-steered, promoted, or explicitly retained work stays visible.
10. For a visible-retirable child, emit one stable retirement intent only after its result is terminal, coordinator-verified, durably integrated or closed with a verified no-integration disposition and durable receipt, and free of unresolved attention. Then call the current Codex task-archive capability and record the observed result.
11. Never archive the coordinator, active, returned-but-unverified, failed, rejected, orphaned, blocked, awaiting-owner, unintegrated, explicitly retained, or owner-promoted tasks. Preserve their handles and report the exact retention reason.
12. Archival is reversible retirement, not deletion. Make it idempotent and resumable: do not repeat a confirmed archive; retain a failed or unknown archive as pending and never claim cleanup without observed reconciliation.
13. Persist only machine-local handles, leases, cursors, and retirement state under ignored runtime storage. Never store credentials or private transcripts. Canonical evidence remains reviewable and contains no runtime secrets.
14. Move a Task to `Testing` only when every required implementation row is complete. Route implementation through `project-implement`, then independent review through `project-qa-review`; after authorised completion, run `project-retro`.

## Cross-Host Proof Boundary

Codex tool observation proves only this current Codex runtime. Claude Code may be expected to use subagents, isolated subagents, or teams; GitHub Copilot may be expected to use its native parallel agent surface; Cursor may be expected to use foreground or background agents. In every case, select by the same execution needs and require current-host verification and authority. Source parity and tests show contract alignment; never describe an unexercised host as runtime-validated.

## Required Report

Report target/source, graph and dependencies, per-unit execution needs, requested/effective executor and `sequential`/`parallel` schedule, requested/effective concurrency, visibility and retention, tri-state capability matrix and provenance, launches/returns/coordinator verification, retirement intents and observed outcomes, retained attention reasons, failures and blocked descendants, unrelated continuation decisions, validation/evidence, privacy and cross-host proof boundaries, and all remaining QA/closeout/delivery gates. Never present Delegate's aggregate or archive result as independent QA, owner acceptance, integration, release, deployment, adoption, or effectiveness proof.
