# Retired Child Record: TASK-007

## Disposition

- Status: Superseded
- Decision date: 2026-07-24
- Owner: John Detlefs
- Active work required: No

## What It Was

TASK-007 was intended to freeze a multi-turn evaluation contract and capture the exact pre-TASK-008 skill as a trustworthy baseline before conversational behaviour changed.

## Why It Was Retired

The evaluation attempt failed closed before producing an authoritative baseline. TASK-008 subsequently changed canonical behaviour under an owner-approved recovery, so the original pre-change baseline can no longer be captured honestly and no longer informs a current implementation decision.

The failed attempt remains part of Git history and cannot be used as behavioural, host, effectiveness, or support evidence. The former task folder was removed so TASK-007 no longer appears as active, blocked, or awaiting owner action.

## What Still Matters

Rigorous behavioural evaluation is required only if a future change proposes to call the interactive behaviour validated or supported. At that point, create a new task that binds its cases, rules, and source identity to the then-current product. Do not reopen TASK-007 or reconstruct a fictional pre-change baseline.
