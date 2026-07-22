---
name: project-fix
description: Use when routing or managing a bounded post-completion defect, regression, change request, incident, or hotfix.
---
<!-- project-workflow:generated -->

# Project Fix

Manage one bounded post-completion correction using the lightweight Fix subtype. Fixes share
`.project-workflow/tasks/` and `.project-workflow/TRACKER.md` with tasks and epics and use one
`FIX.md`; never create a second fix directory tree or tracker.

## Routing

- Keep in-flight, in-scope corrections in the active task or epic child.
- Choose Fix for one bounded correction against delivered/accepted behavior.
- Choose Task for a new outcome, material product decision/discovery, or multiple independent
  work items.
- Choose Epic for several coordinated outcomes/workstreams.
- Treat the user's label as evidence, not a binding classification. State the rationale and
  proceed when clear and authorized; ask one focused question when materially ambiguous.
- Do not reopen completed work by default. Link it if identified; otherwise record
  `Not identified`, the delivered baseline, and report evidence without exhaustive archaeology.

## Commands

```bash
./.project-workflow/cli/workflow fix init --title "<TITLE>"
./.project-workflow/cli/workflow fix triage --id <FIX-ID>
./.project-workflow/cli/workflow fix status --id <FIX-ID> --to "In Progress"
./.project-workflow/cli/workflow fix status --id <FIX-ID> --to Testing
./.project-workflow/cli/workflow fix status --id <FIX-ID> --to Review
./.project-workflow/cli/workflow fix close --id <FIX-ID> --disposition Fixed --decision "<SUMMARY>" --closed-by "<IDENTITY>"
./.project-workflow/cli/workflow fix promote --id <FIX-ID> --to task --reason "<WHY>" --promoted-by "<IDENTITY>"
```

Complete the single `FIX.md` before triage. Classify the work as `Defect`, `Regression`,
`Change Request`, or `Incident`; use `Mode: Hotfix` only for emergency sequencing. Capture
severity, impact, urgency, owner, risk, rollback/containment, related work, primary repo, repos
touched, branch/PR/evidence links, verification plan, regression evidence, and residual risk.

A normal Fix must pass `fix triage` before implementation. A Hotfix may bypass `Ready` only when
the emergency minimum safety packet validates. Promote work that no longer fits a bounded Fix.
Run `doctor` after scaffold and lifecycle changes.

Use `fix close` with `Duplicate`, `Rejected`, or `Deferred` to record a non-delivery terminal
decision as `N/A`; do not move directly to `N/A` without its disposition and audit details.

Do not require a retro for every Fix. Route a repeatable workflow, process, quality, or prevention
gap to a retro or explicit follow-up task without reopening completed originating work.
