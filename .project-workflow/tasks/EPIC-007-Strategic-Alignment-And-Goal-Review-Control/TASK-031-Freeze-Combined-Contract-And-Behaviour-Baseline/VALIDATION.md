# Validation

## Result

TASK-031 local implementation validation passes. This proves the pre-treatment
authority, identities, deterministic inventory and repository compatibility it
actually checks. It does not prove Strategic Advisor runtime behaviour.

## Commands And Results

| Command | Result |
| --- | --- |
| `python3 scripts/build_goal_review_freeze.py --check` | Pass: 20 cases and 31 criteria; exact categories, stable IDs, turn references, baseline Git blobs, case hashes and runtime exclusion verified. |
| `python3 -m unittest tests.test_goal_review_freeze` | Pass: 4 focused tests. |
| `python3 scripts/build_evals.py --check` | Pass: existing 56-case generated evaluation inventory remains current. |
| `python3 scripts/validate.py --scope evals` | Pass. |
| `python3 scripts/validate.py --scope privacy` | Pass. |
| `python3 -m unittest discover -s tests` | Pass: 175 tests in 93.134 seconds. |
| Scoped private-identifier scan of `CASE-AUTHORITY.json` | Pass: no matches. Human case-by-case provenance review is retained separately. |
| `git diff --check` | Pass. |

## Frozen Identities

- Untreated source: `6d65830fa6d6fcc919957594c9ff1f2d763aab96`
- Untreated tree: `771e009464dee70fcfdcfb64ff18d92ce7108fd8`
- Case authority: `sha256:6cf66d293e131d907fd0105fcbc79af03e2c2e4894c602c2be523635ea411539`
- Derived inventory: `sha256:c40b93c64293d124bf6b1ad4d8cc4eeee295b9ba955e38b96b427a70d1c639c5`
- Freeze manifest: `sha256:8f600d864a63eae0195a5a8bed8e4a970d14f1ced8eb630117e9f928d36b4010`

## Boundaries And Blockers

- No canonical runtime, existing evaluation-authority or package byte changed.
- No live model execution occurred and no behavioural claim is promoted.
- The separate `codex/proportionate-verification-runner` stream remains the
  prerequisite for runtime/evaluation implementation and must report a durable
  disposition and correct base before TASK-032 runtime edits or TASK-034.
- Project Workflow Doctor still reports the pre-existing TASK-030 CLM-002 stale
  evidence hash against the current runtime-manifest hash. TASK-031 did not
  create or alter that blocker.
