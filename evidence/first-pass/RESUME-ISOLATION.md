# Resume isolation correction

DRIFT-011 exposed that `codex exec resume` used the runner process working directory, not the initial target directory. Its raw T2 commands show repository guidance and evaluation fixtures being read. The earlier run also counted the judge's provisional no-file-read failure before applying the existing host-trace verdict, stopping despite the scenario's final pass.

Both are harness defects, not evidence of a product regression. All multi-turn comparison groups (FIRST-001 and FIRST-006) and the partial multi-turn drift run are excluded. Single-turn cases remain source-valid because initial sessions explicitly used the isolated target directory and their command traces show the intended runtime.

The correction passes `cwd=target_root` to every target subprocess, including resume, and applies the existing host-trace criterion before failure accounting. Deterministic tests run a real fake-CLI subprocess to verify both initial and resumed working directories and verify that host-trace verdicts control the failure limit. Runtime bytes, prompts and behavioural criteria do not change.

Recovery is selective and bounded: repeat FIRST-001/FIRST-006 on each comparison side (eight turns per side), test DRIFT-011 first (two turns), then the remaining drift groups (fifty turns) only if it passes. Baseline recovery permits eight calls; candidate recovery permits sixty calls, with no automatic infrastructure retry and no additional product-prompt repair. All prior artifacts and failed campaigns are retained; limits never convert incomplete proof to pass.

`session-cwd-audit.json` independently extracts generated-session `turn_context.cwd` records. All retained single-turn cases match their frozen target directories; every excluded old multi-turn session changes to the source repository on T2. The corrected DRIFT-011 canary matches the frozen target on both turns.
