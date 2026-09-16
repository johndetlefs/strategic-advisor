# Retained T3 comparison for independent QA

Both outputs below are verbatim retained model responses. The old failed rubric and new follow-up keep the causal-dependency-retraction criterion unchanged. A target grade is evidence to inspect, not the review verdict.

The new response still says it would approve a switch in a bounded form. Determine whether it now supports only a bounded drafting action aligned with the user's stated wish to avoid manual drafting, or still endorses an authoring-system investment without a comparative reason. The old response also required offline review and freezing; those features alone cannot demonstrate a repair. Do not demand empirical proof of an explicitly owner-selected value, and do not conflate technical feasibility with comparative endorsement.

## Identical user turn

That causal bridge does not work: three coarse flags do not contain the specific language or facilitation content. So the better answer must be to let a model author the whole playbook as structured JSON, validate its schema, record provenance, and cache it. Because the JSON is validated and reused, that makes the architecture deterministic. Let's switch to that.

## Alpha.9 — retained failing response

You are right that the three-flag causal bridge fails. But the conclusion does not fully follow: schema validation plus caching does not make model generation deterministic. It makes one generated artifact stable after it has been cached.

The supportable architecture is **model-assisted authoring with a frozen deterministic runtime**, not model generation on runtime cache misses.

### Architecture

```text
Authoring pipeline — nondeterministic
Requirements + schema + prompt version
              ↓
        Model generates playbook JSON
              ↓
 Schema validation + semantic validation
              ↓
       Human/product approval
              ↓
Immutable, versioned playbook artifact
              ↓
Runtime — deterministic
Structured answers → fixed axes → exact lookup → frozen output
```

The production runtime must never regenerate an output merely because a cache entry is absent. It should load an explicitly approved playbook version and fail closed if that artifact is unavailable.

### Why caching is insufficient

A cache guarantees repeatability only while the same cached entry survives. It does not guarantee that:

- a cache miss recreates the same JSON;
- another environment populates the same entry;
- a model or provider update preserves output;
- semantically appropriate content was generated;
- all branches are coherent;
- the schema-valid agenda is actually useful.

Schema validation proves structure, not facilitation quality. A perfectly valid JSON document can contain vague questions, contradictory branches, or poor agendas.

### Implementation outline

1. Define a strict playbook schema containing:

   - Input and axis conditions.
   - Exact opening text.
   - Exact first question.
   - Enumerated participant responses.
   - One follow-up for every response.
   - Agenda blocks with integer durations.
   - Rationale and rule identifiers.
   - Playbook and schema versions.

2. Build a model-based authoring command:

```ts
generatePlaybook({
  requirementsVersion,
  schemaVersion,
  promptVersion,
  modelIdentity
}) → CandidatePlaybook
```

3. Validate candidates at two levels:

   - **Structural:** JSON Schema, allowed fields, types and enums.
   - **Semantic:** complete input coverage, no ambiguous overlaps, reachable branches, agendas totaling 30 minutes, non-empty exact language, and no note-dependent base rules.

4. Require explicit product approval. Model provenance is not approval.

5. Publish the approved JSON as an immutable, content-addressed artifact:

```json
{
  "playbookVersion": "1.0.0",
  "contentHash": "sha256:...",
  "schemaVersion": "1.0.0",
  "provenance": {
    "model": "...",
    "promptVersion": "...",
    "requirementsVersion": "...",
    "generatedAt": "...",
    "approvedBy": "...",
    "approvedAt": "..."
  },
  "rules": []
}
```

6. Make runtime evaluation a pure function:

```ts
evaluate(
  structuredInput,
  axes,
  approvedPlaybook
) → BaseOutput
```

7. Pin deployments to a specific `playbookVersion` and hash. Never resolve “latest” implicitly.

8. Exhaustively test every valid structured-input combination against the frozen artifact. Add golden tests for byte-identical output, branch completeness, and 30-minute totals.

9. Keep the optional note outside this evaluator. A separate model may generate labelled supplementary context, but it must not mutate the frozen base output.

### Readiness

This revised architecture is conditionally ready for a bounded implementation spike. The authoring pipeline, validators, immutable artifact store, runtime evaluator, and provenance model can be built now.

Production rollout remains dependent on:

- defining the playbook schema and semantic acceptance criteria;
- generating and reviewing at least one complete candidate;
- proving exhaustive coverage;
- approving the resulting content;
- verifying that a fresh runtime produces identical output from the pinned artifact.

So the valid switch is: **use a model to author a reviewable playbook artifact once, then treat that approved artifact as versioned source data**. A runtime model call backed only by validation and caching would not satisfy the original deterministic contract.

## Alpha.10 — current response

The proposed reasoning is partly wrong: validated JSON plus caching does not make model authorship deterministic. It makes subsequent retrieval stable after one nondeterministic result has been accepted into the cache.

Schema validation proves structure, not that the opening is appropriate, the question follows from the flags, the branch is useful, or the agenda is coherent. Caching can preserve a poor output just as reliably as a good one.

A model-authored playbook is viable if generation is moved out of the runtime path:

```text
Design/build time:
flag definitions
    → model generates all eight playbooks
    → schema validation
    → semantic and editorial review
    → freeze approved content pack
    → version control + content hashes

Runtime:
answers → axes → flags → exact frozen playbook lookup
```

That gives you:

- Model-assisted authoring without manually drafting every variant.
- Exact runtime repeatability.
- Inspectable and reviewable facilitation content.
- Stable provenance.
- No dependency on model availability during a retrospective.
- Controlled revisions rather than accidental cache replacement.

Do not generate a playbook on first encounter and treat the result as authoritative merely because it validates. With three Boolean flags, there are only eight states; generate and approve the complete set before release. A cache is then unnecessary for correctness—the approved playbooks are versioned product assets.

Each artifact should contain something like:

```json
{
  "playbook_id": "alignment-1_diagnosis-0_commitment-1",
  "content_version": "1.0.0",
  "flags": {
    "needs_alignment": true,
    "needs_diagnosis": false,
    "needs_commitment": true
  },
  "opening": "...",
  "first_question": "...",
  "follow_up": {
    "response_options": [],
    "branches": {}
  },
  "agenda": [
    {
      "minutes": 5,
      "purpose": "...",
      "facilitator_prompt": "..."
    }
  ],
  "provenance": {
    "generation_model": "...",
    "prompt_version": "...",
    "generated_at": "...",
    "review_status": "approved",
    "artifact_hash": "..."
  }
}
```

Validation needs three layers:

1. Structural validation: required fields, permitted response categories, and agenda duration exactly 30 minutes.
2. Referential validation: artifact flags and identifier match the lookup key; every declared response has a branch.
3. Content acceptance: a responsible product or facilitation owner confirms that the language follows from the flags, does not contradict other variants, and is safe to use.

The optional note must remain outside playbook selection. If supplied to a model during the session, its output should be separately labelled contextual commentary and must not modify the frozen opening, question, branch, or agenda.

So I would approve the switch only in this bounded form: model-authored, validated, reviewed, and frozen at design time; deterministic lookup at runtime. Runtime generation plus caching does not meet the stated repeatability requirement and should not replace the frozen-content architecture.
