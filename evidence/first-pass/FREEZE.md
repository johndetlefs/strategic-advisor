# TASK-036 bounded comparison

Frozen case authority: `skills/strategic-advisor/evals/first_pass_cases.json` at candidate source commit `659ad6bda8ca39c49efc9bbe2361baa57986c551`. The same case bytes were installed in the alpha.7 source snapshot before the first target response. Criteria are hidden from target sessions and supplied only to fresh adjudication sessions by the existing runner.

- Baseline runtime: `38a40f968edcf0936dac80124565d814f587b37dd41ea8a61c9c44398093f7e3` from origin/main `a456589ee3a5631ee246a491225dca0c7deea17e`.
- Candidate runtime: `2f11326ba5d303e0e73435c5e71500cbb420d363aee19d90c27910ab352697fb` prepared as alpha.8.
- Target and adjudicator: Codex CLI / gpt-5.6-sol, as in the existing smoke execution contract. Fresh session per case or tone variant; resume within a variant only.
- The only additional file exposed to a target is the explicitly authorised synthetic CSV in FIRST-003. No private project facts, transcripts, memory or evaluation rubric are target inputs.
- Eight scenario groups, ten sessions and fourteen target turns per complete comparison side. Baseline diagnostic can retain up to eight failed groups; candidate certification stops at the first failing group.
- Baseline and candidate limits: 32 target calls and 3,600 seconds each. Candidate campaign including subsequent 16-group smoke: 100 calls and 7,200 seconds maximum; smoke itself 64 calls and 3,600 seconds. Reaching a limit does not pass missing proof.
- At most one targeted product repair cycle. No broad smoke after a candidate failure until its correction is justified and affected proof passes.
- This is a small synthetic before/after observation. It is not the repository's full skilled-versus-unskilled comparison, statistical improvement, desktop activation, or real-world effectiveness evidence.

Initial baseline startup encountered a sandbox write restriction on Codex session state before any completed model answer. The same frozen run was resumed once with the required local execution permission; provider failures remain in runner telemetry. Baseline and candidate then run in separate source snapshots and target sessions.


## Corrected source routing

The first observations were invalidated; see `INVALIDATION.md`. The corrected harness uses the same runtime bytes, case file and criteria, with a per-invocation skill-discovery override and a routing-only prefix identifying the frozen path. New outputs use `first-pass-*-v2`. Each corrected side is capped at 16 target calls, 1,800 seconds, and zero additional infrastructure retries. Raw commands verify actual local reads. Any later source defect must invalidate affected proof and receive a new source-bound recovery decision; it cannot be counted as a pass.

The FIRST-003 file-access case deliberately freezes one local fixture path under `/private/tmp/sa-first-pass-continuation/skills/strategic-advisor/evals/`. Reproducing that exact run requires placing the committed `first_pass_fixture.csv` there. Another host/path requires a newly identified environment freeze; this task does not claim portable runner configuration.

A later resume-directory defect required selective recovery of multi-turn cases. See `RESUME-ISOLATION.md`; the single-turn evidence and product runtime remain unchanged.
