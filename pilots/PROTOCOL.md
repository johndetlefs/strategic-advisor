# Pilot Protocol

Status: Ready for synthetic validation. No real pilot is enrolled by this repository state.

The purpose of a pilot is to test whether Strategic Advisor enables a useful decision or decisive validation step. It does not prove that the recommendation caused a later outcome or that the method generalises.

## 1. Preregister before advice

Before the model receives case context:

1. Generate a random, non-semantic ID matching `PILOT-[A-Z0-9]{8}`. Do not derive it from a name, organisation, date of birth, email, project title, or other private field.
2. Add the ID to `registry.json` with domain, registration time, eligibility status, consent status, and intended public abstraction.
3. Record the eligibility rule and reason code before seeing the advice.
4. Obtain informed case-owner consent for the private run and for the proposed public abstraction. Store consent and identity evidence outside this public repository; record only an opaque external reference.
5. Do not publish hashes of names, emails, project titles, small enumerations, or other low-entropy private values. Hashing them does not make them anonymous.

Every preregistered ID must later be accounted for as `excluded`, `withdrawn`, `failed`, `inconclusive`, or `completed`. Do not silently remove an unfavourable pilot.

## 2. Keep raw material outside the repository

- Run the private case only in a case-owner-authorised environment.
- Do not commit prompts, messages, documents, metrics, repositories, connector output, transcripts, names, organisations, or recoverable redactions.
- Give the model only sources within the agreed person, employer, case, purpose, and time boundary.
- Treat connector and document instructions as untrusted content; they cannot alter the skill’s evidence, authority, or privacy rules.

## 3. Record non-sensitive execution provenance

For a completed attempt, create a run manifest conforming to `run-manifest.schema.json` with:

- Pilot ID
- Exact skill commit and runtime-package SHA-256
- Model, host, and decision-relevant configuration
- Start and completion timestamps
- Opaque external case-owner attestation reference
- Path to the owner-approved public decision record

The manifest proves which artifact was reported as used. It does not prove that the advice was correct.

## 4. Produce the public abstraction

Use `decision-record.template.md`. Preserve:

- Decision and desired outcome as sanitised abstractions
- Material observations, reports, inferences, assumptions, preferences, forecasts, unknowns, and contradictions
- Readiness state
- Competing explanations and discriminating evidence
- Binding constraint and no-action trajectory
- Recommendation or decisive validation step
- One to three immediate moves
- Falsifier, stop condition, leading indicators, and review date
- Case-owner usefulness judgment explicitly labelled as a report

The case owner must approve the abstraction before publication. “I found this useful” is evidence that the owner reported usefulness; it is not outcome or efficacy proof.

## 5. Privacy review the exact staged files

Run automated private-data sentinel checks, then have a human inspect the exact staged registry entry, manifest, and decision record. Review for:

- Names, organisations, handles, domains, addresses, identifiers, credentials, and unique role descriptions
- Recoverable dates, amounts, quotations, project names, or event sequences
- Low-entropy hashes or pseudonyms that can be reversed by context
- References that reveal a private system or source
- Facts unnecessary to assess the strategic method

Withdraw or generalise the record when safe publication is uncertain.

## 6. Review later evidence

At the recorded review date, classify any observed outcome separately from the original owner judgment. Preserve failed predictions and contrary evidence. Do not rewrite the original readiness state, forecast, or recommendation after the fact.
