# Validation

## Result

TASK-031 local implementation validation passes after adversarial-QA
remediation. This proves the pre-treatment authority, identities,
deterministic inventory and freeze-scope properties it actually checks. It
does not prove Strategic Advisor runtime behaviour. The affected-only peer
re-review of clean commit `cc893b7d2943029e531bfe1ad96ff9e726a73746`
accepted all five remediated findings and returned Pass.

## Commands And Results

| Command | Result |
| --- | --- |
| `python3 scripts/build_goal_review_freeze.py --check` | Pass: 20 cases, 37 criteria, 3 state assertions and 3 control pairs; exact categories, ordered turns, baseline/current identities, frozen support hashes and pre-treatment path scope verified. |
| `python3 -m unittest tests.test_goal_review_freeze` | Pass: 8 focused tests, including reversed-turn, placeholder-text, missing-state and altered-pair failures. |
| `python3 scripts/build_evals.py --check` | Pass: existing 56-case generated evaluation inventory remains current. |
| `python3 scripts/validate.py --scope evals` | Pass. |
| `python3 scripts/validate.py --scope privacy` | Pass. |
| `python3 -m unittest discover -s tests` | Pass: 179 tests in 83.047 seconds. |
| Scoped private-identifier scan of `CASE-AUTHORITY.json` | Pass: no matches. Human case-by-case provenance review is retained separately. |
| `git diff --check` | Pass. |

## Frozen Identities

- Untreated source: `6d65830fa6d6fcc919957594c9ff1f2d763aab96`
- Untreated tree: `771e009464dee70fcfdcfb64ff18d92ce7108fd8`
- Case authority: `sha256:d94ab8fad7dab599ab045068152d7f67c48f569902d49f986bc4a6c673cb2274`
- Derived inventory: `sha256:c41908344bb5fd2bbb4a47661534530361eeb27fb14b72434e38805e8855bd2a`
- Freeze manifest: `sha256:e2f378507dd32eb52af81d511c6b7b94809fdf8f38ca0d9db90bef14fd42730d`
- Claim/proof matrix: `sha256:ce35a7d82e68d12495f70c84d3c77fa6bfd5c4d4326f271caa01301cd14a5252`
- Provenance review: `sha256:ba974e4b56cf7f0402fdc24c225966789fda0e8d8a56cc544f0b59c353cf97a8`
- Freeze authority commit: `c3b6790e93af8bccc59b76a712e47e2a0991ca07`

## Boundaries And Blockers

- No canonical runtime, existing evaluation-authority or package byte changed.
- No live model execution occurred and no behavioural claim is promoted.
- The alpha.6 model/host observation is bound to run-009. The treatment source,
  installed runtime and reconciled runner identities must be sealed before the
  first new target output; they cannot exist before implementation creates that
  candidate.
- The separate `codex/proportionate-verification-runner` stream is durably
  committed at `82b44a0aabe81662917c44b8e99d3a2a6fd021c4`, based on unchanged
  `origin/main` `6d65830fa6d6fcc919957594c9ff1f2d763aab96`, with a clean worktree and
  reported passing focused, full-suite and seven-scope checks. It is not
  pushed, merged, released, installed or present on this branch. TASK-032 and
  TASK-034 must use an explicitly authorised integration or deliberately base
  treatment on that exact commit; they may not assume `main` contains it.
- Project Workflow Doctor still reports the pre-existing TASK-030 CLM-002 stale
  evidence hash against the current runtime-manifest hash. TASK-031 did not
  create or alter that blocker.
