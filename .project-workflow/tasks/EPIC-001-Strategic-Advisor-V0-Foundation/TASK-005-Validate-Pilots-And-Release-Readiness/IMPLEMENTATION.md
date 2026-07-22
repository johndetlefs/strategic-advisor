## User Story

As a prospective user or maintainer, I want v0 release claims grounded in consented real decisions and a criterion-level evidence audit so that an impressive scaffold is never presented as validated strategic capability.

## Parent AC Coverage

- AC6, AC8

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

Obtain the consented real-case evidence and criterion-level audit needed to decide whether v0 can be released without leaking private data or upgrading case-owner enthusiasm into efficacy evidence.

## Approach

- Build the preregistration, consent, intake, sanitisation, calibration, run-manifest, and review templates before accepting real case content or generating advice.
- Conduct one project/product and one career/organisational pilot only with informed case-owner participation.
- Keep raw source material outside the repository and publish only owner-approved, irreversibly sanitised decision records plus non-sensitive execution manifests; use random non-semantic pilot IDs and no low-entropy private hashes.
- Label immediate usefulness judgments as reports and preserve predictions/review dates for later outcome evidence.
- Generate a fail-closed acceptance audit from exact current artifacts; align public status to its verdict.

## Phases

### Phase 1 — Pilot and privacy protocol

- Implement and validate the preregistration registry, consented intake, sanitised decision record, non-sensitive run manifest, privacy checklist, and structural checks using synthetic data only.
- Validation: a complete synthetic record passes; missing consent/calibration fields and private-data sentinels fail.

### Phase 2 — Consented real pilots

- Run the project/product and career/organisational cases with distinct consenting owners.
- Obtain approval of each public abstraction and an explicit decision-usefulness judgment.
- Validation: completeness and exact-artifact privacy review for each record; no raw source is added to the repository.

### Phase 3 — Acceptance audit and release state

- Map AC1–AC8 to current evidence, status, QA verdict, limitations, failures, and deferrals.
- Execute the fail-closed release gate and update public status only to the supported level.
- Validation: remove or fail one required evidence item to prove the gate blocks, then restore and independently follow every final evidence link.

## Acceptance Criteria

- [x] AC1: Pilot protocol and sanitised record template enforce consent, privacy, epistemic status, calibration, and review fields.
- [ ] AC2: A project/product pilot has owner consent, a complete approved sanitised record, and an explicitly labelled usefulness judgment. Covers parent AC6.
- [ ] AC3: A career/organisational pilot has the equivalent evidence. Covers parent AC6.
- [ ] AC4: Exact committed pilot artifacts pass automated and human privacy review with no recoverable private case data.
- [x] AC5: The Epic audit maps AC1–AC8 to exact evidence/status/QA and blocks on every missing criterion or hard gate. Covers parent AC8.
- [x] AC6: Public release status and scope exactly match the audit verdict; incomplete evidence remains visibly pre-release. Covers parent AC8.
- [x] AC7: Every preregistered random pilot ID is accounted for as enrolled, excluded, withdrawn, failed, inconclusive, or completed without exposing private context or permitting silent favourable-case selection.

## Validation

- AC1: Inspect the protocol/template field checklist and run its structural validator.
- AC2: Verify external consent, public-record approval, record completeness, and labelled owner report for the project/product pilot.
- AC3: Repeat for the career/organisational pilot.
- AC4: Run private-data/recoverable-redaction checks and record a human review of the exact staged files.
- AC5: Generate the acceptance audit, follow every evidence link, and prove the release gate fails when a criterion or hard gate is removed.
- AC6: Compare README/product-contract/version language with the final audit verdict.
- AC7: Validate the preregistration ledger against all pilot records and manifests; every ID has one allowed terminal status and no private-content-derived identifier or hash.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Build preregistered consented pilot protocol | Create the random-ID registry, eligibility/status rules, intake, consent boundary, sanitisation checklist, run manifest, decision-record template, and structural validation without storing raw case content. | AC1, AC7: Every required consent, privacy, provenance, epistemic, recommendation, calibration, review, and pilot-accounting field is enforced. | Inspect and validate complete and deliberately invalid synthetic instances. | Done structurally; no pilots enrolled |
| 2 | Run project/product pilot | Preregister and conduct the canonical skill process with a consenting real case owner, retain non-sensitive execution provenance, and publish only the owner-approved sanitised decision record and manifest. | AC2, AC4, AC7: Accounted pilot ID, complete approved record/manifest, labelled owner judgment, and passing exact-artifact privacy review. | Case owner confirms consent, execution attestation, accuracy of abstraction, and usefulness judgment outside the public record. | To Do |
| 3 | Run career/organisational pilot | Repeat the controlled preregistered process for a distinct consenting career or organisational case. | AC3, AC4, AC7: Accounted pilot ID, complete approved record/manifest, labelled owner judgment, and passing exact-artifact privacy review. | Case owner confirms consent, execution attestation, accuracy of abstraction, and usefulness judgment outside the public record. | To Do |
| 4 | Generate criterion-level release audit | Map AC1–AC8 to current artifacts, evidence status, QA verdicts, failures, limitations, and deferrals; implement fail-closed release decision logic. | AC5: Audit is complete and the gate fails on any missing parent evidence or hard gate. | Follow every audit link and run a deliberate negative release-gate test. | Done: current audit returns gaps for every unproved parent AC |
| 5 | Align public release state | Update status and scope claims only to the level supported by the final audit, preserving visible blockers when incomplete. | AC6: Public claims and version state match the audit verdict exactly. | Compare README/product contract/release metadata with the generated verdict. | Done for current blocked state |

## Parent AC Evidence

- AC6: pending consented pilot records, non-sensitive run manifests, and privacy review. AC8: the generated acceptance audit currently blocks release and public claims remain pre-release; final criterion evidence and QA verdicts remain pending. No visual proof recipe applies.

## QA & Code Review

- Verdict: ____
- Evidence: ____
- Findings: ____

## Retro

- Reusable lessons: ____
- Conventions or agent assets updated: ____
- Follow-up tasks: ____

## Notes

- Task: TASK-005
- Title: Validate Pilots and Release Readiness
- Created: 2026-07-22
