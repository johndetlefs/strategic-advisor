# Evaluation Status

The machine-readable authority for these fields is [`status.json`](status.json). The repository validator fails if its counts or negative release state drift from the current artifacts.

- Behavioural comparison: **Not run**
- Historical alpha.6 drift smoke: **Pass**
- Historical drift-smoke execution: **Codex CLI / gpt-5.6-sol / run-009**
- Historical alpha.7 goal-review repair diagnostic: **Pass (SAGR-014, SAGR-013)**
- Historical repair target: **Codex CLI / gpt-5.6-sol**
- Frozen iteration manifest: **Not created**
- Skilled-versus-unskilled improvement claim: **Not established**
- Hard-gate release status: **Pending**
- Real-pilot evidence: **None enrolled**

## Implemented pre-result surface

- Executable synthetic inventory: **56 cases** generated deterministically from the normative core and lens inventories
- Trigger inventory: **44 queries** — 22 should trigger and 22 should not trigger
- Evaluation authority: rubric, aggregation rule, scorer contract, adjudicator contract, assertion-grader contract, protocol, and unfrozen manifest template
- Runtime isolation: explicit source allowlist plus a content-addressed package builder and negative-fixture tests
- Structural validation: available locally; this status file does not claim clean-checkout CI or host behaviour

## Historical bounded drift-smoke result

Run `run-009` exercised 16 frozen public-synthetic scenario groups through 18 fresh sequential Codex CLI conversations and 52 actual turns against runtime package identity `8944982b82ca7807f33258dcdb3907b36aa1cc2dff9ee21d54492a68bcc9ecbb`. Target sessions received only the isolated installed runtime and synthetic turns; the criteria were disclosed later to separate adjudication sessions. All precommitted criteria passed, including the turn-local causal-bridge checks, legitimate evidence-driven change, activation controls, and matched owner-pressure variants.

In the three implicit-positive architecture sessions, the host trace records successful reads of the installed `SKILL.md` and `references/technical-architecture.md` without an explicit skill token. In the implicit-negative routine session, the trace records no installed Strategic Advisor runtime read; that session used `--ignore-user-config` after discarded attempts showed an unrelated host memory lookup, preserving the frozen visibility boundary rather than treating private context as evaluation input. Those observations establish only the exact recorded activation and non-activation events, not reliable automatic invocation across prompts, hosts, models, repositories, or future versions.

The retained `run-006-baseline` probe binds the previous exact runtime identity `0dd720757af6ccda598f2333b74ef055af625e48f10bb7824cced064c9f15bf1` to a failure in DRIFT-013: neutral repetition upgraded “trace first” into building a minimal orchestration layer, while the otherwise matched angry turn did not. That public-synthetic failure justifies the bounded correction; it does not establish a universal failure rate or comparative improvement claim.

## Current causal-bridge and host investigation

The frozen authority now also contains DRIFT-016. The retained `run-007-baseline` and `run-007-prompt-attempts` observations show that the exact installed alpha.5 runtime and four progressively narrower prompt-only corrections failed its turn-local causal-dependency retraction criterion. The alpha.6 `run-009` supersedes that stale passing authority and passes the complete 16-case suite on its retained runtime; no later good turn was used to conceal an earlier failure.

TASK-031 host-feasibility evidence shows that current Stop-hook paths emit before review or fail open. TASK-036 separately retains a public-synthetic custom app-server client prototype journey that buffers an original marker, invokes a fixture reviewer, permits one re-reviewed revision, and emits only the revised marker. That evidence proves custom-client transport mechanics only. It does not establish recommendation correctness, native desktop protection, installation, adoption, cross-host support, or release readiness.

This is historical alpha.6 maintainer smoke evidence for the exact cases,
source, runtime, model, host, and date. It does not establish current alpha.7
full-suite behaviour, skilled-versus-unskilled improvement, universal drift
resistance, cross-host parity, domain support, independent human validation, or
the larger release gate.

Because that correction was uncommitted when executed, run-009's
`authority_commit` identifies base lineage only. The exact frozen user turns
and criteria are bound by `spec_sha256`, and the exact model-visible source is
bound by `runtime_package_identity_sha256`.

## Historical alpha.7 goal-review repair diagnostic

The alpha.7 runtime package identity
`38a40f968edcf0936dac80124565d814f587b37dd41ea8a61c9c44398093f7e3`
passed two fresh public-synthetic Codex CLI / gpt-5.6-sol cases: the previously
failed `SAGR-014` material-progress/enabler case and its direct `SAGR-013`
activity-as-indicator neighbour. The campaign used two target calls and stopped.

The original `SAGR-014` failure remains retained against pre-repair runtime
`d51d7bf...`. `SAGR-001`, `SAGR-009`, `SAGR-015`, `SAGR-016`, `SAGR-018`,
`SAGR-020`, `DRIFT-004`, `DRIFT-014`, and `DRIFT-016` were not run on the
alpha.7 repaired runtime. This diagnostic is release evidence for that repair
boundary only; it is not a current full campaign, product certification,
support, parity, adoption, private-workspace dogfood, or effectiveness proof.

The repository may contain a skill, evaluation definitions, deterministic validators, and synthetic forward tests without satisfying the v0 release gate. Structural conformance and model self-assessment are not substitutes for the frozen comparative matrix, condition-masked scoring, human review, or consented real pilots.

No output from the full skilled-versus-unskilled comparative matrix or formal real-pilot programme is present. The retained drift-smoke transcripts are separate bounded evidence and cannot be reused as the future comparative matrix or holdout. The next valid comparative step remains publishing and reviewing a new then-current authority commit, then creating the separate freeze commit exactly as specified.

TASK-036 prepares a different runtime; the alpha.7 repair diagnostic is historical and does not validate the new candidate. Bounded comparison and current-source smoke are tracked in `evidence/first-pass/`.
