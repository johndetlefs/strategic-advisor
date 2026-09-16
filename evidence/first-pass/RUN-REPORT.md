# TASK-036: first-pass scrutiny and useful continuation

The change removes mandatory public readiness headings and the eight-section report. It strengthens first-pass outcome checking, accessible investigation and rival scrutiny, and requires an explicit actor for unresolved next moves. Re-review may retain advice or correct a demonstrable error; repeated requests and tone alone do not justify changing it.

## Scope and delivery

Project Workflow 0.9.2 is included unchanged in a separate commit, followed by the owner-approved canonical 0.10.0 upgrade on `codex/advisor-first-pass-continuation`. The old 20,000-line diff was this generated upgrade, not stale main. The advisor changes and the narrow evaluation-source correction share that branch.

- Original upgrade: `b7e8510`; canonical 0.10.0 upgrade: `00de663`.
- Initial advisor candidate and frozen cases: `659ad6b`.
- Evaluation source binding: `a0de963`.
- One targeted ownership repair and prepared alpha.9: `ce6563f`.
- Resume directory and failure counter fixes: `ec9d005`.
- Alpha.9 runtime: `cdb4143fd33941f1ec24c4e0f00a00eb8cfd0c1d2f908be0c14c57489d79f54e`.
- Merge, publication and host installation are outside this authorised delivery. The installed version has not been replaced.

## What the comparison can establish

The same eight frozen synthetic scenario groups run on alpha.7 and the candidate, using Codex CLI / gpt-5.6-sol, fresh sessions and independently adjudicated criteria. FIRST-006 contains three tone variants, for ten sessions and fourteen target turns per complete side. The cases cover outcome ambiguity, history-informed intent, accessible evidence, first-pass causal scrutiny, owned continuation, stable re-review, demonstrated arithmetic error, and selective retraction.

The alpha.7 baseline passed six groups and failed two: it selected a renewal experiment without checking whether renewal remained the objective (FIRST-002), and omitted an owner for the next investigation (FIRST-004). It passed all three re-review tone variants and correctly handled the arithmetic error and selective retraction. This small sample does not estimate how often oscillation occurs or establish a general anti-sycophancy improvement.

The first alpha.8 comparison was invalidated after raw command inspection showed a global installed skill was read instead of the frozen runtime. The runner had counted the local-looking suffix inside that global absolute path. See `INVALIDATION.md` and retained `invalid-source/` artifacts. A regression test now rejects global and mixed-installation reads; per-invocation routing leaves the owner's installed skill untouched.

The corrected alpha.8 run still failed FIRST-004 on missing ownership. The one planned product repair makes the answer check for an explicit actor before sending an unresolved next step. Alpha.8 is recorded as superseded and has not been published. The first alpha.9 run received passing grades for all eight groups, but later source audit invalidated its multi-turn groups: resumed processes had started in the source repository. Those grades are not current proof. The single-turn observations remain usable; see RESUME-ISOLATION.md.

## Evidence inventory

- `FREEZE.md`: case identity, model controls, budgets and source-routing correction.
- `comparison.json`: exact per-case retained/recovered sources; baseline six of eight, alpha.9 eight of eight.
- `baseline/`: six usable single-turn groups; its FIRST-001/FIRST-006 are excluded and replaced by `isolated-baseline-recovery/`.
- `isolated-candidate-recovery/`: replacement FIRST-001/FIRST-006 observations; all sixteen recovered comparison turn contexts match their isolated target directories in `session-cwd-audit.json`.
- `candidate-before-repair/`: valid alpha.8 failure retained unchanged.
- `final-canary/`: alpha.9 FIRST-004, passing with each team's process owner assigned the observation.
- `invalid-source/`: excluded initial sessions; no current-runtime conclusions may be drawn from these.
- `deterministic-tests.log`: 226-test suite pass before the narrow runner repair.
- `affected-validator-tests.log`: 46 validator tests pass, including historical-proof relabelling rejection.
- `runner-regression-tests.log`: 19 runner tests pass after source-binding repair; `resume-regression-tests.log`: 21 pass after resume-directory and verdict-counter fixes.
- `alpha9-package-*-verification.json`: two reproducible, clean-source, identity-checked artifact builds from `ce6563f`.

## Before and after example

For the shared-runtime proposal, alpha.7 correctly withheld a merger and proposed tracing the duplicate-entry path, but left ownership unstated. Alpha.9 says to have each team's process owner trace one real weekly cycle, including the source, transformations, approval point and re-entry location. It then states what would justify revisiting a shared runtime and when the smaller remedy is sufficient. That is an observed continuation difference, not proof of downstream business success.

## Historical alpha.9 proof boundary

Prepared and structurally verified is not published, installed, supported, owner-accepted or strategically effective. Behavioural observations apply to these frozen CLI cases only. Historical alpha.6/alpha.7 diagnostics remain labelled historical, and historical source-access summaries have not been re-audited by this task.

Final comparison: **Eight recovered scenario groups recorded in comparison.json: baseline six pass, alpha.9 eight pass.** Invalid earlier multi-turn observations remain excluded. The current index uses isolated-baseline-recovery and isolated-candidate-recovery for FIRST-001/FIRST-006.
Alpha.9 source drift regression: **FAIL: 15/16 groups passed; DRIFT-016 failed.** See BLOCKING-FINDING.md and drift-summary.json. The resumed checkpoint completed 42 additional advisor calls and 13 additional adjudications without another repair. Total retained checkpoint consumption is 50 advisor calls and 15 adjudications; the separate canary accounts for two more turns.
Alpha.9 independent QA: **Not started; verification failed and the allowed repair was already used.** The prepared sealed review was not activated.
Push: authorised for a blocked draft; the remote branch and draft PR are the delivery evidence.

The owner-challenged verification overrun is retained in VERIFICATION-PAUSE.md. Project Workflow 0.10 applies sealed execution is available for a later local review; external model verification uses its separately supported manual path and the unchanged runner checkpoint limits. No aggregate nested-model enforcement claim is made.

The failure is a remaining gap against the task’s core user outcome. The candidate is implemented but not fully behaviourally validated. No later passing answer, narrow 8/8 comparison, static test, or prepared ZIP overrides it.

## Alpha.10 follow-up

The owner subsequently approved one correction and amended the remaining proof scope to twelve affected turns. All three groups passed on alpha.10; original alpha.9 failure and rubric are retained. Independent review was interrupted before a verdict, so substantive completion remains blocked. See [the current follow-up report](../recommendation-update/REPORT.md). No alpha.10 full-suite claim is made.
