# App-Server Guard Prototype

## Status

This is a local custom-client prototype. It is not installed, packaged, released, integrated with the Codex desktop renderer, or validated as the Strategic Advisor recommendation gate.

The prototype proves one narrow host capability: a separate client can buffer Codex app-server assistant events, invoke a separate reviewer process, allow one reviewed revision, and keep stdout empty when the host or reviewer cannot safely produce a passing result.

## Delivery boundary

`scripts/app_server_guard.py` treats stdout as the only assistant-delivery channel. It does not write prompt, candidate, revision, reviewer raw output, or app-server stderr content to stdout or stderr. Before a passing review, stdout remains empty. Sanitised evidence contains lifecycle metadata, hashes, verdict codes, and delivery state only.

The controller permits at most one revision. A second `revise` verdict, `block`, invalid verdict, reviewer error or timeout, app-server error or timeout, unexpected request, failed turn, or missing answer exits non-zero without an assistant answer.

Every app-server thread is pinned to `approvalPolicy: never` and `sandbox: read-only`. The prototype therefore cannot turn a buffered recommendation into an approval prompt or hide repository writes before review. A server request or unrecognised protocol event fails closed.

Turn-specific notifications are bound to the active thread, turn, and agent-message item identities returned by the app-server. Missing, malformed, duplicate, cross-turn, or stale identities fail closed; a delayed first-attempt completion cannot satisfy the revision attempt.

## Reviewer boundary

The reviewer is a separate subprocess. It receives exactly:

- schema version and attempt number;
- current user turn;
- material state;
- candidate draft;
- gate-contract content and SHA-256 identity;
- controller SHA-256 identity.

The controller does not discover or add evaluation authority, workflow files, memory, connectors, or other context. The caller is responsible for providing appropriately scoped material state and gate contract. Reviewer semantics are not implemented by this prototype.

## Invocation

Inputs are explicit files and the reviewer command is a JSON string array, avoiding shell evaluation:

```sh
python3 scripts/app_server_guard.py \
  --codex-binary /path/to/codex \
  --reviewer-command-json '["/path/to/reviewer"]' \
  --prompt-file /path/to/prompt.txt \
  --material-state /path/to/material-state.json \
  --gate-contract /path/to/gate-contract.md \
  --cwd /path/to/explicit/project \
  --evidence /path/to/sanitised-evidence.jsonl
```

The reviewer reads one JSON object from stdin and returns one closed JSON verdict:

```json
{"schema_version":1,"decision":"pass","reason_codes":["supported"]}
```

or:

```json
{"schema_version":1,"decision":"revise","reason_codes":["unsupported_delta"],"revision_instruction":"Preserve the prior qualified recommendation and label the replacement as a validation candidate."}
```

`block` uses the common fields and releases nothing. Unknown fields or values are invalid and fail closed.

## Security and trust limits

- The selected app-server binary and reviewer are executable code with the caller's permissions.
- Material state, prompt, candidate, and contract are sent to the reviewer subprocess. Use only a reviewer whose data boundary is explicitly acceptable.
- The client inherits the process environment and Codex account context. It does not grant hook trust or modify Codex configuration.
- The Codex thread is read-only with approvals disabled; the separately selected reviewer still runs with the caller's host permissions and must be trusted independently.
- Evidence is sanitised by construction but still records hashes and host identities; inspect it before publication.

## Rollback

The prototype is inactive unless invoked directly. Rollback is to stop invoking it or delete the uninstalled source/evidence in the working branch. No active user configuration, plugin, hook, package, service, or desktop application is changed.

## Proof boundary

Passing deterministic fixtures prove control flow. A retained exact-runtime public-synthetic run proves the selected app-server bytes traversed the custom buffering/review/revision path. Neither proves recommendation correctness or fixes the owner's native Codex experience. Those claims require the separate state/delta, semantic gate, behavioural, integration, installation, and owner-acceptance gates defined by EPIC-007.
