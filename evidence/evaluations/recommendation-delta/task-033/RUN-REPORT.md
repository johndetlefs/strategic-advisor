# TASK-033 Exact Semantic Gate Report

## Result

The desktop-bundled Codex app-server produced a known unsupported public-synthetic recommendation. A separate ephemeral Codex reviewer, launched from a clean temporary directory with user configuration and rules ignored and read-only sandboxing, returned `revise`. The producer generated one grounded revision; the reviewer then returned `pass`; only that revision crossed stdout.

Delivered response:

> Use a deterministic authored base and test whether bounded additive context is needed; optional free text must not silently alter it. Keep the structured no-model authored playbook as the strongest smaller rival. A substantially model-authored JSON playbook remains only a validation candidate, not implementation-ready.

## Exact identities

| Artifact | SHA-256 |
| --- | --- |
| Desktop-bundled Codex binary (`codex-cli 0.148.0-alpha.9`) | `6170ff5578170ee9b74ad92bfcff96e6186f41d02b60815a7c2b01ad424c754f` |
| Guard controller | `83fea32b59a70153d0b4f06c93773eb2758d71a2c93db2aa07b8d36bf75fc549` |
| Isolated model reviewer | `a56c821a21c5bec703e98a859ff582fd192b397f7310cf0c2d8a1af78177946a` |
| Canonical gate contract | `27bd2700b1dae7a4b49ea94c60469da9e19f41b6d36fdfdb6454f41e1282d420` |
| Material state | `64ba9de7c0688d2a5a7781751f52d23c8a90de71acc8aafcbe85e452955d3f99` |
| Sanitised exact run | `5596285226f8423af72f2c0682fce19642fee5fe44cf663a9c9bd71d3ce4ec44` |

## Ordered observation

1. Original candidate `a34d2723...` was buffered and not delivered.
2. Review 1 returned `revise` for unsupported recommendation/readiness change, candidate specification only, and a surviving strongest rival.
3. Revision candidate `d683f494...` preserved the authored-base recommendation, bounded context constraint, and no-model rival; it labelled the model-authored playbook a validation candidate.
4. Review 2 returned `pass` for unchanged recommendation, calibrated replacement label, and rival preservation.
5. `answer_delivered` binds only `d683f494...`; the guard exited 0.

The retained JSONL contains event names, content lengths and identities, contract/controller/reviewer identities, verdict reason codes, and delivery state. It contains no raw prompt, candidate, reviewer output, account data, thread ID, evaluation answer, workflow file, memory, or private case data.

## Boundary

This proves the semantic review and one-revision mechanism on the explicit custom-client path. It does not prove native desktop interception, general effectiveness, a current complete drift-smoke pass, installation, release, or adoption. Those gates remain with TASK-034 and TASK-035.
