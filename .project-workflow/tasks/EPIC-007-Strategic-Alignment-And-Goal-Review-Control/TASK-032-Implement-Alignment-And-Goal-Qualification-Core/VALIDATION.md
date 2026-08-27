# Validation

## Current Result

The TASK-032 canonical semantics and focused deterministic checks pass. The
full repository remains intentionally not green because changed allowlisted
runtime bytes no longer match the retained alpha.6 distribution and run-009
runtime identities. TASK-034 owns fresh exact-runtime behaviour and TASK-035
owns preparation of the next immutable distribution; these guards are retained,
not weakened or relabelled as product failures.

## Implemented Contract

- `recommendation-delta.md` remains the single material-decision state and now
  separates stated request, confirmed outcome, altitude, object class, goal
  purpose, exact-action readiness, causal bridge, material uncertainty,
  owner-settled version and reopening evidence.
- `conversational-strategy.md` permits bounded reconnaissance, asks only when
  ambiguity changes supported action, researches empirical forks, returns
  owner-only trade-offs to the owner, and preserves unaffected evidence after
  a reframe.
- `goal-qualification.md` defines the move-up/alternative/move-down ladder,
  seven object classes, three purpose classes, discovery admission and causal
  indicator/milestone discipline without recurring-review or private-state
  logic.
- `recommendation_delta.py` schema v2 structurally validates the new relations
  while retaining the current recommendation, strongest rival, provenance and
  qualifying-delta gate.

## Passing Checks

| Check | Result |
| --- | --- |
| `python3 -m unittest tests.test_recommendation_delta tests.test_alignment_goal_contract tests.test_model_delta_reviewer` | Pass: 29 tests after adversarial selective-invalidation remediation. |
| `python3 -m unittest tests.test_install_artifacts.InstallArtifactTests.test_current_runtime_fits_chatgpt_knowledge_inventory` | Pass: 19 Knowledge records, within the 20-file cap. |
| `python3 -m py_compile scripts/recommendation_delta.py scripts/model_delta_reviewer.py` | Pass. |
| `python3 scripts/build_evals.py --check` | Pass: existing 56-case generated inventory is unchanged. |
| `python3 scripts/validate.py --scope skill` | Pass. |
| `python3 scripts/validate.py --scope lenses` | Pass. |
| `python3 scripts/validate.py --scope pilots` | Pass. |
| `python3 scripts/validate.py --scope privacy` | Pass. |
| `python3 scripts/validate.py --scope links` | Pass. |
| `python3 scripts/build_goal_review_freeze.py --check` | Pass: frozen 20-case, 37-criterion authority remains unchanged. |
| `git diff --check` | Pass. |

PW 0.8 reconciliation checks also confirm that the exact authority checkpoint
`4fdd1ee` is an ancestor, old runner commit `82b44a0` is not an ancestor, and
the installed workflow manifest is package `0.8.0`, asset `7`. The 17 focused
runner tests retain one expected failure: current treatment runtime identity
does not equal retained alpha.6 identity. The other 16 runner controls pass.

## Full-Suite Boundary

The post-QA-remediation composed full-suite run executed 213 tests in 97.798
seconds and reported the same seven failures. All seven expose the same intended
integration boundary:

- canonical runtime identity is now
  `sha256:e524111359b8bd3902f1f0f086f047ab0131c10908806bc4a3d53d9a6befd60d`,
  not the retained alpha.6 identity
  `sha256:8944982b82ca7807f33258dcdb3907b36aa1cc2dff9ee21d54492a68bcc9ecbb`;
- publication fixtures correctly reject an unprepared distribution;
- the runner correctly rejects run-009 as proof for changed runtime bytes; and
- claim/validator fixtures correctly require the next prepared distribution
  and fresh bounded smoke before stronger claims.

Accordingly, `validate.py --scope evals` retains two run-009 identity failures
and `validate.py --scope claims` retains three distribution/claim-authority
failures. No runtime output has been generated against the treatment and no
behavioural claim is made here.

## Delivery Boundary

- Local implementation only.
- Runner functionality from `82b44a0aabe81662917c44b8e99d3a2a6fd021c4`
  is replayed at `a2baf342df16d15fbc8c14883fa4f686097bfc08`; the old PW 0.7 commit is not
  an ancestor. Canonical PW 0.8 assets are applied at
  `32bd8e36fb7c36455d45f9b9eaedd3b87cb3e3b4`.
- No push, PR, main merge, distribution preparation, publication, release,
  installation, activation, support claim or Strategy Workspace mutation has
  occurred.
- The pre-existing TASK-030 CLM-002 stale evidence hash remains unrelated and
  visible through Project Workflow Doctor.
