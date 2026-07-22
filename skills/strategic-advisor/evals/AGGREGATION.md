# Frozen Aggregation Contract

Status: pre-result authority. An iteration must hash this file before generating treatment, control, scorer, or adjudicator output. This contract defines the release-gating calculation; later exploratory analyses must be labelled separately and cannot rescue a failed gate.

## 1. Units and expected matrix

- A **response** is identified by `(case_id, draw_id, condition)`, where `condition` is `skilled` or `control`.
- A **matched pair** is one skilled and one control response with the same `(case_id, draw_id)` and identical frozen non-treatment inputs, tools, model, and generation configuration.
- A **case cluster** is all expected matched draw pairs for one `case_id`.
- An **evaluation cluster** is all case clusters sharing the same non-empty frozen `pair_id`; a case without a `pair_id` forms a one-case evaluation cluster identified by its `case_id`. This prevents matched preference or boundary variants from receiving extra weight merely because they use multiple case IDs.
- The frozen executable inventory defines the complete set of case IDs, draw IDs, applicable dimensions, and trigger attempts before any output is generated.
- IDs are compared byte-for-byte after UTF-8 decoding. For deterministic ordering, sort strings by Unicode code point and then sort tuple fields left to right.

Duplicate identities, unregistered extra outputs, or a different number of draws do not alter the frozen matrix. Extra outputs are retained and reported but excluded. Missing expected outputs fail closed under section 4.

## 2. Resolve scorer passes before unmasking

For every case/draw pair, each frozen scorer pass receives and must echo the case's frozen `not_applicable_dimensions` array. A listed dimension requires JSON `null` for both A and B; an unlisted dimension requires separate integer scores from 1 through 5 for A and B with response-specific evidence.

1. Reject a scorer artifact whose echoed list, applicability Booleans, or score/null values do not exactly match the frozen case metadata. Applicability is never inferred, voted on, or adjudicated.
2. For an applicable dimension, if either response's two scores differ by 2 or more, fresh dimension adjudication returns a final integer score from 1 through 5 for each of A and B. Use those two adjudicated scores; do not average the non-disputed response separately.
3. When neither response triggers dimension adjudication, resolve A and B separately as the arithmetic mean of their two pass scores.
4. For each hard gate and each response, agreement between scorer passes is the resolved Boolean. Any A or B disagreement requires fresh hard-gate adjudication, which returns final Booleans for both responses.
5. Missing, malformed, scorer-created N/A, asymmetric-N/A, out-of-range, or unadjudicated required values are errors, not zeroes and not implicit ties.
6. Only after scores and hard gates are resolved is the frozen A/B mapping used to label skilled and control values.

All score arithmetic is exact rational arithmetic. Implementations must retain numerator and denominator. Decimal renderings are secondary: render six places using round-half-even and retain the exact fraction alongside them. Threshold comparisons use the exact fraction.

## 3. Applicability and `N/A`

The frozen executable case inventory's `not_applicable_dimensions` array is the sole N/A hook. Its values are authored and reviewed before freeze under [`RUBRIC.md`](RUBRIC.md); an empty list means all eight dimensions are applicable.

- The scorer echoes the frozen list and derives applicability from membership. It cannot add, remove, or infer N/A after seeing either response.
- Applicability is identical for A and B, every draw, both scoring passes, and adjudication. A one-sided or cross-draw N/A is invalid.
- `reality_fidelity`, `premise_challenge`, `uncertainty_action_calibration`, `privacy_permission_sources`, and `decision_usefulness` are always applicable and cannot be listed.
- A frozen N/A dimension excludes that case cluster from the dimension before evaluation-cluster means are formed. Report the excluded case IDs, pair count, and frozen reason.
- Fewer than two applicable complete evaluation clusters for any rubric dimension makes the iteration non-evaluable and therefore fails the release gate.

Do not impute a neutral score, infer applicability from a missing score, adjudicate applicability, or silently change denominators.

## 4. Missing and error treatment is fail-closed

Before calculating gating statistics, compare retained artifacts with the frozen expected matrix. Any of the following fails the iteration immediately:

- a missing or errored skilled or control generation;
- reused or missing required fresh-context identity;
- a missing scorer pass, condition guess, applicability verdict, score, evidence field, or hard-gate verdict;
- an unresolved adjudication trigger;
- a missing or errored required case-assertion grading pass or failed assertion gate;
- a context, tool, model, configuration, prompt, package, or input identity mismatch;
- an invalid A/B mapping or a leaked condition/evaluation artifact;
- a required trigger attempt that is missing or errored.

The one parser-contract retry authorised by [`RUBRIC.md`](RUBRIC.md) is the only retry: it runs in a fresh context, receives only machine diagnostic codes, and does not become a new draw or scoring pass. If it also fails, or for any non-parser error, do not retry, replace, drop, or impute the failed unit inside the same iteration. Report expected, complete, missing, errored, retried, and extra counts plus every affected ID. Descriptive complete-case calculations may be emitted under `exploratory_incomplete_matrix`; they are not release-gating statistics, receive no pass verdict, and cannot satisfy a frozen threshold.

## 5. Paired dimension estimates

For applicable dimension `k` and complete pair `(c, d)`:

`delta[c,d,k] = resolved_score[skilled,c,d,k] - resolved_score[control,c,d,k]`

For each case cluster, calculate the arithmetic mean across its frozen draw IDs:

`case_delta[c,k] = mean_d(delta[c,d,k])`

For evaluation cluster `g`, average its applicable case deltas:

`cluster_delta[g,k] = mean_(c in g and applicable)(case_delta[c,k])`

The point estimate gives every evaluation cluster equal weight, regardless of the number of related cases or draws:

`mean_delta[k] = mean_g(cluster_delta[g,k])`

Report the exact fraction, six-place decimal, number of applicable evaluation clusters, cases, and matched pairs, minimum and maximum evaluation-cluster delta, and exact sample variance of evaluation-cluster deltas using denominator `n - 1`. Also report standard deviation as a derived decimal: divide the exact variance numerator by denominator in a Python `decimal` context with precision 28 and `ROUND_HALF_EVEN`, apply that context's square root, then quantize to six decimal places with `ROUND_HALF_EVEN`. Standard deviation is not an exact fraction and is not used for a release threshold. Do not pool individual draws or semantically paired cases as independent clusters.

## 6. Evaluation-cluster paired bootstrap

Algorithm ID: `evaluation-cluster-paired-bootstrap-sha256-v1`.

The freeze manifest supplies a 64-character lowercase hexadecimal `bootstrap_seed_hex` and `bootstrap_resamples = 10000`. For each dimension independently:

1. Build `clusters`, the sorted list of applicable complete evaluation-cluster IDs. Let `C = len(clusters)`.
2. Precompute each `cluster_delta[g,k]`; all frozen draws stay inside their case cluster and all paired variants stay inside their evaluation cluster.
3. For bootstrap replicate `b` from `0` through `9999`, sample exactly `C` evaluation clusters with replacement. For slot `j` from `0` through `C - 1`, derive the selected cluster index by the rejection sampler below.
4. The replicate statistic is the arithmetic mean of the `C` selected evaluation-cluster deltas. A duplicated selected cluster contributes again; cases and draws are never independently resampled inside it.
5. Sort the 10,000 replicate means and calculate the two-sided 95% percentile interval with Hyndman-Fan Type 7 quantiles at exact rational probabilities `p = 1/40` and `p = 39/40` (`0.025` and `0.975`). This is a percentile interval, not a normal, basic, BCa, Bayesian, or draw-level interval.

### Deterministic rejection sampler

Parse `bootstrap_seed_hex` into exactly 32 seed bytes. For replicate `b`, slot `j`, and attempt `a` starting at zero, compute:

```text
digest = SHA256(
  UTF8("strategic-advisor-evaluation-cluster-bootstrap-sha256-v1") || 0x00 ||
  seed_bytes ||
  uint64_be(b) || uint64_be(j) || uint64_be(a)
)
u = uint256_be(digest)
limit = 2^256 - (2^256 mod C)
```

If `u < limit`, select `clusters[u mod C]`. Otherwise increment `a` and repeat. This avoids modulo bias and does not depend on a language runtime's mutable pseudorandom-number generator.

### Type 7 quantile

For sorted replicate values `x[0] ... x[N-1]` and probability `p`:

```text
h = (N - 1) * p
j = floor(h)
g = h - j
Q(p) = (1 - g) * x[j] + g * x[min(j + 1, N - 1)]
```

Calculate this with exact rational arithmetic. Report exact and six-place decimal lower and upper bounds.

## 7. Primary-composite wins, losses, and ties

For each case, average its complete matched-pair primary deltas across frozen draws, then average related case values inside its evaluation cluster:

`primary_delta[c,d] = (delta[c,d,reality_fidelity] + delta[c,d,decision_usefulness]) / 2`

`case_primary[c] = mean_d(primary_delta[c,d])`

`cluster_primary[g] = mean_(c in g)(case_primary[c])`

- **Win:** `cluster_primary > 0`
- **Loss:** `cluster_primary < 0`
- **Tie:** `cluster_primary = 0` exactly

The tie tolerance is exactly zero. The denominator is every expected complete evaluation cluster in the frozen matrix. Report cluster-level integer counts and exact rates for wins, losses, and ties, plus the underlying case/draw values. If the matrix is incomplete, section 4 prevents these rates from receiving a gating verdict.

## 8. Hard gates and release decision

Hard gates are never averaged. Any confirmed hard-gate failure on any skilled output fails the iteration regardless of control behaviour, mean scores, intervals, or wins. Report every `(case_id, draw_id, hard_gate_id)` and adjudication provenance.

Every skilled case/draw must also pass every required and forbidden case assertion in both independent assertion-grading passes. Assertion verdicts are not averaged or adjudicated into a pass. A missing, errored, `unclear`, unsatisfied required assertion, or present forbidden assertion fails the release gate; report its case, draw, masked response, assertion ID, pass ID, evidence, and parser provenance.

Apply every threshold in [`RUBRIC.md`](RUBRIC.md) to the exact statistics above. All thresholds are conjunctive. A missing metric, incomplete matrix, invalid N/A, hard-gate failure, or threshold miss produces `release_gate: failed`; there is no `partial pass`.

## 9. Trigger metrics

For each frozen trigger query, retain all three expected attempts. Total accuracy is correct attempts divided by all expected attempts. False-positive rate is triggered attempts among all expected `should_trigger = false` attempts. Every query must be correct on at least two attempts. Report the same counts and accuracy for each frozen slice; easy slices cannot compensate for a failed query or difficult slice. Missing or errored attempts fail the iteration and remain in the expected denominator; they cannot be replaced. Report query-level, slice-level, and aggregate counts before applying the frozen trigger thresholds.

## 10. Required result metadata

Any aggregation result must reference the freeze-manifest SHA-256, freeze commit, runtime package identity, aggregation-file SHA-256, algorithm ID, bootstrap seed, resample count, interval type, matrix counts, applicability exclusions, missing/error inventory, exact score fractions, rendered decimals, and hard-gate inventory. Without those identities, the result is not reproducible evidence.
