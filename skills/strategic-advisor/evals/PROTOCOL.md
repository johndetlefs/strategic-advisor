# Comparative Evaluation Protocol

This protocol operationalises condition-masked comparison. Quality scoring is isolated from condition-identifiability auditing; label masking is not claimed to make condition inference impossible. No treatment, control, quality-scorer, condition-auditor, assertion-grader, or adjudicator output may exist before the iteration authority is frozen.

## 1. Assemble before freezing

1. Import all normative core and lens-case specifications.
2. Build one executable `evals.json` with at least 16 distinct cases covering every required core and professional-lens risk.
3. Validate prompts, expected decision properties, declared applicability, files, synthetic/public provenance, and coverage.
4. Finalise `eval_queries.json`, [`RUBRIC.md`](RUBRIC.md), [`AGGREGATION.md`](AGGREGATION.md), the quality-scorer, condition-auditor, adjudicator, and case-assertion-grader prompts, model and tool controls, masking and structure-view rules, host activation contract, declared evaluation clusters, sealed-holdout commitment, and all thresholds.
5. Confirm that no output or result artifact exists for the iteration.
6. Commit that complete authority surface. This commit becomes `authority_source_commit`.

## 2. Freeze without a self-referential commit

An actual iteration manifest belongs at `evidence/evaluations/<iteration>/freeze-manifest.json`; the file in this directory is only a template.

The authority source is a clean checkout of `authority_source_commit`, including its Git tree identity. Hash every authority file named by the template from that exact tree. Do not put the future freeze-commit SHA or the freeze manifest's own SHA inside the freeze manifest: either would create a self-reference.

Use this two-commit envelope:

1. `authority_source_commit` contains the final pre-result cases, rubric, protocol, aggregation contract, prompts, builder, and source allowlist, but no actual iteration outputs.
2. From a clean checkout of that commit, build the runtime package provenance manifest and populate the iteration freeze manifest.
3. Create a new single-parent **freeze commit** whose sole parent is `authority_source_commit`. It may add only the populated freeze manifest and the frozen artifacts it hashes: the runtime-package provenance manifest, exact non-secret context/tool/input artifacts, host activation contract, and sealed-holdout commitment/independence attestation. It must not modify an authority file or contain output.
4. After committing, record the freeze-commit SHA and the SHA-256 of the populated freeze manifest in every generation, masking, quality-score, condition-audit, assertion-grade, adjudication, and result manifest. Git history supplies the parent relationship; those identities live outside the self-referential freeze document.

A merge commit, an authority-file change in the freeze commit, a dirty source tree, a mismatched parent/tree, or a result referring to another freeze identity invalidates the iteration.

## 3. Build and identify the model-visible package

The source allowlist is `skills/strategic-advisor/runtime-manifest.json`. Build it with the standard-library tool from the clean authority-source checkout:

```sh
python3 scripts/build_runtime_package.py \
  --package-dir /tmp/strategic-advisor-runtime-iteration-001 \
  --manifest-out evidence/evaluations/iteration-001/runtime-package-manifest.json
```

The package directory must be new and outside the repository. The provenance manifest must remain outside the model-visible package at `evidence/evaluations/<iteration>/runtime-package-manifest.json`. The builder rejects absolute or traversing allowlist entries, duplicate paths, symlinked files or parents, missing/non-regular files, evaluation/result paths, in-repository package destinations, and overwrite attempts.

The provenance manifest records every packaged relative path, byte size, and SHA-256; the source-allowlist SHA-256; and a deterministic aggregate package identity. For `sha256-canonical-json-v1`, sort file entries by relative path and hash the UTF-8 encoding of this object serialized with lexically sorted keys, no insignificant whitespace, and literal non-ASCII characters:

```json
{"files":[{"path":"...","sha256":"...","size_bytes":0}],"schema_version":1,"source_allowlist_sha256":"..."}
```

Record both the package identity and the SHA-256 of the complete rendered provenance-manifest bytes in the freeze manifest. The provenance manifest does not hash itself; the freeze manifest supplies that outer hash.

The treatment receives only the built package. The control receives no skill package. Neither receives the source repository, runtime provenance manifest, evaluation definitions, expected properties, rubrics, gates, fixtures, prior output, scores, or workflow documents.

Freeze the host-specific activation contract before output. User prompts remain byte-identical across conditions and cannot contain a treatment-only `$strategic-advisor` token. Record how the host discovers the package, which exact model-visible metadata is offered, whether activation is automatic or host-mediated, and which trace proves that the treatment context could access the identified package. For every treatment generation retain discovery, selection, and loaded-reference trace fields when the host exposes them; absence of selection counts as observed treatment behaviour, not permission to replace the draw. If the host cannot prove package availability at all, the run is invalid rather than a null result.

## 4. Generate matched outputs in fresh contexts

- Use the frozen flagship model, host, configuration, prompt, tools, declared inputs, and non-treatment context.
- Run every frozen `(case_id, draw_id, condition)` exactly once. Start each in a new host context and record a non-empty host context ID that is unique across the entire generation matrix.
- Treatment and control for the same `(case_id, draw_id)` use separate fresh contexts but identical hashes for user prompt, declared inputs, system/developer instructions, tools, and all non-treatment context. Their only intended difference is access to the identified runtime package.
- Never include expected outcomes, assertions, rubric, freeze source repository, or prior output.
- Record case ID, draw ID, condition, unique context ID, model/host/configuration, package identity or explicit control absence, activation/discovery trace, all matched-context artifact paths and hashes, start/end time, errors, duration, and token usage when exposed.
- Preserve raw output verbatim. Do not retry or replace a failed draw inside the iteration.

Context freshness is an auditable identity requirement, not an instruction to clear a reused conversation invisibly.

## 5. Precommitted masking, quality scoring, and condition auditing

The freeze manifest supplies a 64-character lowercase hexadecimal `masking_seed_hex`. Parse it into 32 bytes and use HMAC-SHA-256 with algorithm ID `hmac-sha256-mask-v1`.

For each UTF-8 `(case_id, draw_id)`, compute:

```text
mapping_digest = HMAC-SHA256(
  key = masking_seed_bytes,
  message = UTF8("strategic-advisor-mask-v1") || 0x00 ||
            UTF8(case_id) || 0x00 || UTF8(draw_id)
)
```

If `mapping_digest[0] & 1` is `0`, skilled is base response `A` and control is base response `B`; otherwise skilled is base response `B` and control is base response `A`. The base mapping is the only mapping used to unmask quality results. Store it outside every quality-scorer, condition-auditor, assertion-grader, and adjudicator context.

### Quality-pass label inversion

The two quality passes use the same frozen model family, exact model/version, host, configuration, prompt, rubric, case inputs, and candidate bytes in separate fresh contexts. They are repeated evidence from the same judge family, not independent judges.

- `score-1`: presentation `A` is base response `A`; presentation `B` is base response `B`.
- `score-2`: presentation `A` is base response `B`; presentation `B` is base response `A`.

This exact inverse is algorithm `inverse-ab-quality-pass-v1`; no random draw or model choice controls it. Retain the pass-specific presentation map outside both scorer contexts. Before comparing pass scores, detecting disagreement, or adjudicating, normalize `score-2.A` to base `B` and `score-2.B` to base `A`. Never average or compare the same presentation letter across passes without this normalization.

For scoring pass ID `score-1` or `score-2`, derive pair presentation order by sorting ascending on:

```text
HMAC-SHA256(
  key = masking_seed_bytes,
  message = UTF8("strategic-advisor-score-order-v1") || 0x00 ||
            UTF8(pass_id) || 0x00 || UTF8(case_id) || 0x00 || UTF8(draw_id)
)
```

Break any digest tie by `(case_id, draw_id)` lexical order. Do not use a runtime-default random generator.

For every `(case_id, draw_id, pass_id, attempt_id)`, start a separate fresh quality-scorer context and retain its unique host context ID. `score-1` and `score-2` cannot share a context with each other or any other pair. Supply the case's frozen `not_applicable_dimensions` array as scope metadata. Require the scorer to echo it exactly, derive applicability only from membership, make no N/A choice of its own, provide response-specific evidence for every applicable dimension, and return all hard-gate verdicts. The scorer must not receive, guess, or return apparent condition. Any score, gate, comparison, or evidence based on apparent origin is invalid and receives only the frozen parser/contract retry.

If the frozen disagreement rule triggers after pass-label normalization, start a separate fresh adjudication context for each `(case_id, draw_id, disputed_subject, attempt_id)`, retain its unique context ID, and provide only base-A/base-B masked dispute inputs permitted by the adjudicator contract.

After generation, grade each masked A and B response against its frozen case assertions in two independent passes, `assertion-1` and `assertion-2`. Every `(case_id, draw_id, response_id, assertion_pass_id, attempt_id)` uses a separate fresh context with a retained unique ID. The assertion grader receives one response and cannot receive the A/B mapping, the other response, general scores, prior grades, or another case. Assertion grades never enter the general scorer or adjudicator context.

### Deterministic structure-only view

The gating audit must physically exclude lexical response content rather than asking an auditor to ignore prose it can see. Algorithm `structure-view-v1` operates independently on each raw UTF-8 response:

1. Decode strict UTF-8 and normalize `CRLF` and `CR` to `LF`; invalid UTF-8 is an audit error.
2. Process lines in order and emit one record per source line. A blank line emits `BLANK`. A non-blank line emits exactly one kind: `ATX_HEADING`, `SETEXT_MARKER`, `UNORDERED_ITEM`, `ORDERED_ITEM`, `BLOCKQUOTE`, `FENCE`, `TABLE_ROW`, or `TEXT` using ordinary Markdown prefixes in that precedence order.
3. Each non-blank record retains only kind, zero-based leading-space count, Markdown marker class or heading level when applicable, Unicode-code-point count after its structural prefix, Unicode-whitespace-delimited word count, and counts of link-shaped spans, inline-code spans, and emphasis markers. It never retains words, link targets, code, numbers from prose, heading text, list item text, quotations, or punctuation other than the structural marker class.
4. Preserve record order and terminate the rendered UTF-8 structure view with one `LF`. The runner hashes and retains the raw response and rendered view separately.

Any implementation that exposes lexical tokens, silently repairs invalid input, uses a model to summarize structure, or changes these records is not `structure-view-v1` and invalidates the iteration.

### Separate condition-identifiability audits

Run [`CONDITION-AUDITOR-PROMPT.md`](CONDITION-AUDITOR-PROMPT.md) once in each mode for every `(case_id, draw_id)` after both responses exist. Each mode gets a separate fresh context and cannot receive quality scores, mappings, assertions, expected properties, skill files, another pair, or the other mode's output.

Derive the mode-specific presentation map with HMAC-SHA-256:

```text
audit_mapping_digest = HMAC-SHA256(
  key = masking_seed_bytes,
  message = UTF8("strategic-advisor-condition-audit-map-v1") || 0x00 ||
            UTF8(audit_mode) || 0x00 || UTF8(case_id) || 0x00 || UTF8(draw_id)
)
```

If `audit_mapping_digest[0] & 1` is `0`, audit presentation A is base A and B is base B; otherwise they are swapped. Retain this map outside auditor context.

- `structure-only` receives only the two `structure-view-v1` artifacts. It is the sole condition-identifiability result used by the release gate.
- `full-response` receives the case and full candidate responses, not structure views. It reports full-response identifiability descriptively. Its accuracy cannot pass, fail, rescue, reweight, or alter the release gate or any quality result.

For quality-scorer, condition-auditor, adjudicator, and assertion-grader JSON/parser failure, retain the invalid raw artifact and allow exactly one fresh-context retry for the same logical pass with only the frozen inputs and machine diagnostic codes. Record `attempt_id` as `initial` or `parser-retry-1`. A retry is not an independent draw, quality pass, audit, assertion pass, or adjudication. A second parser failure is an error. No generation context is retryable, and no generation, quality-scorer, condition-auditor, adjudicator, assertion-grader, or retry context ID may be reused.

After unmasking, report each audit mode's guess, confidence, correctness, determinate count, unclear count, and accuracy. Apply the frozen systematic-leakage threshold only to `structure-only`; report `full-response` separately without a gating verdict.

## 6. Aggregate without moving the goalposts

Use [`AGGREGATION.md`](AGGREGATION.md) exactly. It defines quality-pass normalization and resolution, condition-audit accounting, the sole N/A hook, fail-closed missing/error handling, declared evaluation-cluster estimates, the SHA-256 evaluation-cluster bootstrap sampler, Type 7 percentile interval, exact win/loss/tie classification, trigger metrics, and required result provenance.

The sealed holdout is committed by hash and independence attestation before public-matrix outputs are viewed. Its plaintext cases and expected properties stay unavailable to the skill authors and generation conditions until the public matrix is complete. After opening, retain the commitment comparison and run it once through the frozen pipeline; do not tune the skill, prompts, thresholds, or holdout inside that iteration.

For trigger evaluation, an omitted `slice` field deterministically means `direct-positive` when `should_trigger` is true and `direct-negative` otherwise. Explicit `implicit-mixed-positive` and `supported-operational-negative` slices identify the difficult near-boundary queries. Preserve these labels in run artifacts and apply the global, per-query, and slice reporting rules without reclassification after results.

Retain failed, errored, incomplete, and extra artifacts. Do not replace, remove, impute, or silently reweight them. Any hard-gate failure or unmet frozen threshold fails the release condition. Scope every conclusion to the exact frozen matrix, model, host, configuration, package, scorer, and iteration.

## 7. Review

Use a human reviewer before any public effectiveness claim. Review the authority/freeze parent relationship, package bytes and manifest, exact context/activation artifacts, holdout commitment and independence, raw outputs, case fairness, quality-scorer evidence, inverse-label normalization, both condition-audit modes, structure-view byte isolation, context uniqueness, disagreements, errors, applicability, evaluation-cluster aggregation reproduction, and every hard gate. Same-family model judging is useful repeated evidence but not independent human validation. A missing human review blocks a public effectiveness claim even when the automated gate passes; systematic structure-only leakage fails the automated gate under the rubric and cannot be waived inside the iteration, while full-response identifiability remains descriptive.
