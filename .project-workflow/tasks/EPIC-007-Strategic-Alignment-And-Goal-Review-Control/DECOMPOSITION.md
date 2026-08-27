# Decomposition Plan

## Summary

- Epic: EPIC-007
- Status: Approved by parent requirements envelope
- Authority source: Parent REQUIREMENTS.md Owner Approval
- Source requirements identity: sha256:cdbd03660ff1ac27a395209ca8cf128a3894a8a581edcf7717974cdc8358235c
- Last updated: 2026-08-27

## Authorized Child Rows

| ID | Title | Parent ACs | Source | Dependencies | Execution Needs |
|---|---|---|---|---|---|
| TASK-031 | Freeze Combined Contract And Behaviour Baseline | AC2, AC3, AC4, AC5, AC6, AC11, AC13 | Proposed Child Work |  | bounded-return |
| TASK-032 | Implement Alignment And Goal Qualification Core | AC1, AC2, AC3, AC4, AC5, AC6 | Proposed Child Work | TASK-031 | bounded-return |
| TASK-033 | Implement Material Goal Review Contract | AC7, AC8, AC9, AC10, AC11, AC12 | Proposed Child Work | TASK-032 | bounded-return |
| TASK-034 | Validate Combined Exact-Runtime Behaviour | AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12, AC13, AC14, AC15 | Proposed Child Work | TASK-033 | bounded-return |
| TASK-035 | Integrate Runtime Packages And Downstream Handoff | AC12, AC13, AC14, AC15, AC16, AC17 | Proposed Child Work | TASK-034 | bounded-return |

## Authority Rules

- Matching rows inside this plan may be approved and scaffolded without separate per-row owner approval.
- Rows outside this plan require an approved amendment before gated lifecycle movement.
- Matching is by ID, title, and parent AC coverage.
