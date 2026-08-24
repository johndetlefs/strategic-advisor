# Contributing

Strategic Advisor welcomes evidence-led contributions. The repository is pre-release; a change is not accepted merely because it sounds persuasive or makes an example look better.

## Runtime distribution is part of the change

Every accepted change to bytes selected by
`skills/strategic-advisor/runtime-manifest.json` must prepare the next immutable
distribution in the same branch:

```sh
python3 scripts/release_state.py prepare --version 0.2.0-alpha.N
```

Do not hand-edit the version in the builder, product contract, README, or
installation guide. The preparation command binds the version to the exact
runtime-package identity and synchronises the candidate references
transactionally. Repository validation rejects runtime drift without that
prepared intent; documentation, evaluation, test, and workflow-only changes do
not require a version bump.

If a prepared candidate is found defective before publication, do not rewrite
its identity and do not publish it merely to unlock the next version. First
verify that its tag and GitHub release are absent, then atomically retain the
prepared intent and prepare an advancing replacement:

```sh
python3 scripts/release_state.py supersede \
  --next-version 0.2.0-alpha.N \
  --prepared-source-revision <COMMIT_WITH_EXACT_PREPARED_INTENT> \
  --reason "<WHY_THE_UNPUBLISHED_CANDIDATE_WAS_SUPERSEDED>" \
  --superseded-at YYYY-MM-DDTHH:MM:SSZ
```

The command requires the named commit to contain the exact prepared version
and runtime identity, refuses locally tagged or finalized candidates, retains
the superseded version, identity, source, reason, time, and replacement, and
prevents later version reuse. A repository-local absence check does not prove
GitHub absence; record the live remote tag and release checks in the governing
Fix before running the command.

When the prepared change reaches `main`, the protected release workflow
validates the exact revision, builds and verifies all four files twice, and
creates the prerelease only if the immutable tag does not exist. An existing
exact release is verified read-only; any source, runtime, or asset mismatch
fails without replacement.

After the workflow passes, fresh-download its retained verification evidence
and promote the verified release:

```sh
python3 scripts/release_state.py finalize \
  --evidence /path/to/strategic-advisor-release-evidence.json
```

Finalization records the evidence and changes the public current-download
references only after public verification. Publication and package alignment
do not prove host installation, activation, support, adoption, parity, or
strategic effectiveness.

## Before contributing

Read the [product contract](PRODUCT-CONTRACT.md) and the repository [agent guidance](AGENTS.md). Keep operative strategic instructions only under [`skills/strategic-advisor/`](skills/strategic-advisor/). Do not copy that logic into a host adapter, README, fixture, or evaluator.

Never submit personal, household, employer, client, credential, message-history, or proprietary case data. Examples and fixtures must be synthetic, public, or irreversibly sanitised. Replacing names alone is not sufficient sanitisation.

## Claim and evidence rules

- Separate observations, reports, inferences, assumptions, preferences, forecasts, and unknowns.
- Do not call a capability supported until the [product contract](PRODUCT-CONTRACT.md) classifies it as validated and identifies current evidence.
- Structural checks prove structure. Behavioural evaluations prove observed behaviour under their recorded conditions. Neither proves general effectiveness.
- Add dependencies only when they enforce an approved invariant. The repository validator must remain standard-library-only and deterministic.

## Local checks

From the repository root, run:

```sh
python3 scripts/build_evals.py --check
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

To isolate a diagnostic, run `python3 scripts/validate.py --scope skill`, `lenses`, `evals`, `pilots`, `privacy`, `claims`, or `links`. These commands require no network, credentials, model, or private input.

If a change adds or changes model-visible runtime files, update [`skills/strategic-advisor/runtime-manifest.json`](skills/strategic-advisor/runtime-manifest.json). The manifest is an allowlist: an omitted file is not packaged, and evaluation material must remain excluded.

Do not create an iteration freeze or generate treatment/control output while authority files are still changing. Follow the two-commit freeze envelope in [`skills/strategic-advisor/evals/PROTOCOL.md`](skills/strategic-advisor/evals/PROTOCOL.md); a test of the packaging mechanics is not a frozen behavioural run.

## Pull requests

Explain the decision-relevant outcome, the claim being made, the evidence that targets that claim, the limitations, and the exact validation commands run. Keep unrelated changes separate. A green deterministic check does not waive a required behavioural, host, clean-checkout, or human review gate.

For a security issue, do not open a public issue; follow [SECURITY.md](SECURITY.md).
