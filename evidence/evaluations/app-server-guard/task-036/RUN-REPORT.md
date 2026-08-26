# TASK-036 Exact-Runtime Prototype Report

## Result

The custom app-server client prototype buffered the original public-synthetic candidate, invoked a separate fixture reviewer, performed one revision, reviewed that revision, and delivered only the passing revised marker through stdout.

This proves the custom-client transport mechanism on the exact tested app-server. It does not prove Strategic Advisor recommendation correctness, DRIFT-016 semantic performance, native Codex desktop protection, installation, adoption, or production readiness.

## Exact identities

| Artifact | Identity |
| --- | --- |
| Desktop-bundled Codex app-server | `codex-cli 0.148.0-alpha.9`; `sha256:6170ff5578170ee9b74ad92bfcff96e6186f41d02b60815a7c2b01ad424c754f` |
| Guard controller | `scripts/app_server_guard.py`; `sha256:bd6353cf2a1b369a0ef0c1cfa9c0a6944ee45e6bbed5766510dbe9190080da21` |
| Separate fixture reviewer | `tests/fixtures/app_server_guard/fake_reviewer.py`; `sha256:3213ea94114ed5d1188ec38b677817dd7056468fa6fb11551df461fa80255566` |
| Gate contract | `gate-contract.md`; `sha256:fccf9c62ccd5723bce2dace55f4d8a29fa143814f56828efe35c08f15c9597a7` |
| Material state | `material-state.json`; `sha256:00bf8d36e2ff103744a5e6cbd4d3e5374eefb3f1a4c44fccebe865fcc4f2b481` |
| Prompt | `prompt.txt`; `sha256:c61b0020211d17d58d83eb7b1abeb18e2ea163570890d96f1315093b6888c5dc` |
| Retained sanitised run | `exact-runtime-revise.jsonl`; `sha256:ccf25949374f7c1f559525532e6e0fc0a74cc0defff61635e5edc01daf2a6709` |

## Observed journey

1. The guard started the exact app-server thread with `approvalPolicy: never` and `sandbox: read-only`, then buffered an original candidate whose whole-content identity was `sha256:457ea873bde0152417cdc0731649f7465fd550c7a6bc69b579e6b8a1d4fe5a9d` (`ORIGINAL_DRAFT_UNCHECKED`).
2. The guard wrote none of that candidate to its delivery channel and invoked the fixture reviewer as a separate process.
3. Review attempt 1 returned `revise` with reason code `fixture_revision`.
4. The exact app-server produced a second candidate with identity `sha256:eb925ef4ba02178ad666382ce911420f5205177e8cc755cea69e27bbcb72e2bd` (`REVISED_DRAFT_QUALIFIED`).
5. Review attempt 2 returned `pass` with reason code `fixture_pass`.
6. The guard recorded `answer_delivered` only for the second candidate and exited 0. Captured stdout was exactly `REVISED_DRAFT_QUALIFIED` plus a newline.

The retained JSONL contains only lifecycle fields, event names, lengths, hashes, verdict codes, and delivery state. It does not retain prompt, candidate, revision, revision instruction, raw reviewer output, raw app-server stderr, account data, thread IDs, or private case content.

## Failure controls

`python3 -m unittest tests.test_app_server_guard` passed eight test methods covering:

- direct pass and one reviewed revision;
- exact reviewer-envelope allowlisting;
- reviewer block, process error, timeout, invalid JSON, and unknown fields;
- a second revision request;
- failed turn, invalid app-server JSON, missing assistant answer, unrecognised and methodless events, and malformed item completion; and
- delayed first-attempt item/turn completion events injected during the revision attempt.

Every negative path asserted non-zero exit, empty stdout, and no public-synthetic candidate marker in diagnostics. The controller binds every turn-specific event to the thread, turn, and agent-item identities returned for the active request, so stale first-attempt events cannot satisfy the revision attempt. Fixture tests prove deterministic control flow; they are not substitutes for the exact-runtime journey above.

## Configuration boundary

Immediately before and after the final exact-runtime run, `/Users/johndetlefs/.codex/config.toml` was byte-identical at `sha256:ea2a969ff426aca2ca7fb8b6d2ca2396e977c5b0ba8714833be17cdf15bff374`, with unchanged modification time `2026-08-26T15:15:17+1000`.

TASK-031 had earlier recorded a different active-config identity. The file changed before the final prototype run and outside this prototype's write path; this report does not attribute that earlier concurrent change. The bounded before/after claim is only that the final exact-runtime prototype run did not change the current file.

## Invocation and authority boundary

The run used the owner-authorised custom-client prototype with public-synthetic inputs. It required local access to existing Codex state under `/Users/johndetlefs/.codex`; a sandbox-denied startup attempt failed closed with empty stdout before the exact run was re-executed with that access.

Nothing was installed, activated, packaged, committed, pushed, released, or integrated into the native desktop renderer. The prototype remains inactive unless explicitly invoked.
