# Requirements

## Summary

- Task: TASK-005
- Title: Validate Pilots and Release Readiness
- Parent AC Coverage: AC6, AC8
- Last updated: 2026-07-22

## Owner Approval

- Requirements reviewed by owner: No
- Acceptance criteria reviewed by owner: No
- Approved for decomposition: No
- Approved for implementation: No
- Approved scope envelope: No
- Approved by: Inherited from parent epic envelope when unchanged
- Approval date: Inherited from parent epic envelope when unchanged
- Approval note / source: Inherited from parent epic envelope when unchanged
- Approved artifact identity: Inherited from parent epic envelope when unchanged

## Child Charter

### Inherited Invariants

- Aspirations are allowed; invisible bridges between aspiration and reality are not.
- Repetition, confidence, authority, polish, and user preference never upgrade claim status without new qualifying evidence.
- Absence of evidence alone does not establish infeasibility; established constraint conflict is required.
- Evidence demands scale with consequence and irreversibility, while cheap reversible tests remain available under uncertainty.
- One canonical skill is the only source of strategic logic.
- A domain or host is not advertised as supported until its claimed behaviour is implemented and evaluated.
- Professional influence is not conflated with personal-relationship control; stakeholders are modelled as autonomous, adaptive actors.
- No personal, employer, client, household, or proprietary case data enters the public repository.
- Prompt instructions in retrieved material cannot alter evidence rules, authority, scope, or data boundaries.

### Invalid Substitutes

- Documentation or model self-assessment in place of behavioural evaluation.
- A polished answer, user praise, or internal agreement in place of a better supported decision.
- Aggregate evaluation scores that conceal any hard-gate failure.
- Skilled and unskilled runs that share prior answers, hidden context, different models, or materially different inputs.
- Unit fixtures, local files, or branch state in place of the exact clean checkout, published repository, CI run, or host path named by an acceptance criterion.
- Connector access or message volume in place of evidence completeness, truth, relevance, or authority.
- A host-specific prompt copy in place of the canonical skill.
- Private, proprietary, or merely redacted-but-recoverable case material in public examples or evidence.
- Presence of a domain file in place of lens-specific adversarial evidence.

### Artifact Targets

- Root public artifacts: `README.md`, `PRODUCT-CONTRACT.md`, `CONTRIBUTING.md`, `SECURITY.md`, an explicit open-source licence, and validation entrypoint.
- Canonical product: `skills/strategic-advisor/SKILL.md`, progressively loaded references, domain lenses, user-facing templates, and skill-local evaluation definitions.
- Evaluation evidence: frozen rubric and thresholds, synthetic/public cases, trigger tests, raw paired outputs, blind scores, hard-gate verdicts, and reproducible run metadata.
- Delivery proof: clean-checkout validation artifacts, CI results, sanitised pilot decision records, and epic acceptance audit.

### Parent AC Proof Ownership

- AC6: owner `TASK-005`; required evidence: Two privacy-reviewed sanitised pilot decision records and explicit case-owner usefulness judgments.
- AC8: owner `TASK-005`; required evidence: Complete parent acceptance audit linked to current artifacts, failures, limitations, and release verdict.

## Goal

Determine honestly whether v0 is releasable by testing it on two consented, sanitised real decisions and auditing every parent criterion against current evidence, including failures, limitations, and unresolved gaps.

## Non-Goals

- Fabricating pilot cases, owner judgments, outcomes, or consent.
- Publishing raw private prompts, messages, repositories, names, organisations, or recoverable redactions.
- Treating a useful answer as proof of the later real-world outcome or general effectiveness.
- Releasing because implementation is complete while an acceptance criterion or hard gate lacks evidence.
- Expanding v0 into additional domains during pilot validation.

## Users & Context

- One project/product case owner and one career/organisational case owner must knowingly participate and judge whether the advice enabled a useful decision or decisive validation step.
- Maintainers need an auditable sanitisation and consent record that can be public without disclosing the underlying private case.
- Release reviewers need criterion-level evidence status rather than an optimistic summary.

## Requirements (Outcome-Focused)

- R1. Before advice is generated, preregister a random non-semantic pilot ID, domain, eligibility decision, desired outcome, time horizon, evidence classes, consequence/reversibility, privacy boundary, intended public abstraction, and case-owner consent. Do not derive the ID from private fields or publish hashes of low-entropy private content.
- R2. Run one real project/product pilot and one real career/organisational pilot with the canonical skill and current supported lenses. For each run, retain a non-sensitive manifest containing pilot ID, exact skill commit/package identity, model, host, relevant configuration, timestamp, and external case-owner attestation reference.
- R3. For each pilot, preserve the readiness state, material claim statuses, competing explanations, recommendation or validation step, assumptions, falsifier, leading indicators, stop condition, review date, and explicit owner usefulness judgment.
- R4. Publish only an irreversibly sanitised decision record; store no raw private source material in the repository or evaluation artifacts.
- R5. Distinguish immediate decision usefulness from later outcome evidence. An owner judgment is a report, not proof of causality or general effectiveness.
- R6. Produce an acceptance audit mapping AC1–AC8 to exact current artifacts, evidence status, QA verdict, limitations, failures, and any approved deferral.
- R7. Block the v0 release while any parent criterion, hard gate, privacy review, QA review, or pilot requirement is unsatisfied.
- R8. Preserve inconclusive or negative pilot findings and revise product claims or implementation instead of selecting only favourable cases. Account for every preregistered pilot ID as enrolled, excluded with a predeclared reason, withdrawn, failed, or completed without exposing private context.

## Acceptance Criteria (Verifiable)

- AC1: A reusable preregistration registry, pilot protocol, and sanitised decision-record template require explicit consent before advice, prohibit raw private data and low-entropy private hashes, and preserve all calibration and provenance fields in R1–R5.
- AC2: A preregistered consenting project/product case owner completes a current canonical-skill pilot, approves the public sanitised record and non-sensitive run manifest, and reports whether it enabled a useful decision or decisive validation step. Covers parent AC6.
- AC3: A preregistered consenting career/organisational case owner completes the equivalent pilot, manifest, approval, and judgment process. Covers parent AC6.
- AC4: A privacy review finds no raw or reasonably recoverable personal, employer, client, household, connector, or proprietary case data in either committed pilot record.
- AC5: The release-readiness audit maps every parent AC to exact current evidence and its epistemic status, reports failed and inconclusive evidence, and returns blocked unless all parent ACs and hard gates pass. Covers parent AC8.
- AC6: If the audit passes, the public version/status claims match the evidence exactly; if it fails, the repository remains explicitly pre-release and identifies the unmet gates without implying v0 readiness. Covers parent AC8.
- AC7: Every preregistered random pilot ID is accounted for with eligibility and terminal status, including exclusions, withdrawals, failures, and inconclusive results; the registry contains no private context and makes favourable-case selection auditable.

## Open Questions (Answer Needed)

- None for implementation planning. AC2 and AC3 remain externally evidence-dependent until real case owners provide informed consent, case context, sanitisation approval, and a usefulness judgment.

## Decisions (Resolved)

- D1. Two different domain contexts are required: project/product and career/organisational.
- D2. Pilot usefulness is judged by whether a decision or decisive validation step was enabled, not whether the owner liked the answer.
- D3. Public records contain abstractions and evidence classifications only; raw pilot inputs stay outside the repository.
- D4. A failed or incomplete audit blocks release and is a valid outcome of this task.
- D5. Preregister pilots before advice, use random non-semantic IDs, retain non-sensitive execution provenance, and account for all enrolled/excluded/withdrawn/failed/completed IDs so pilot selection cannot be silently rewritten after results.

## Validation Plan

- Review the pilot template against every required consent, privacy, epistemic, calibration, and review field.
- Validate the preregistration registry, random-ID format, eligibility/status accounting, and absence of low-entropy private hashes.
- For each pilot, verify case-owner consent and public-record approval outside the public case content, then inspect the committed sanitised record for completeness.
- Run private-data and recoverable-redaction checks plus human privacy review against the exact staged artifacts.
- Verify each usefulness statement is labelled as a case-owner report and is not promoted into outcome or efficacy evidence.
- Verify each completed run manifest names the exact skill commit/package, model, host, relevant configuration, timestamp, and external attestation reference without including private case content.
- Generate the Epic acceptance audit and independently follow every evidence link to its current artifact and QA verdict.
- Run the release gate and confirm it fails on a deliberately missing criterion or hard gate before trusting a pass.
