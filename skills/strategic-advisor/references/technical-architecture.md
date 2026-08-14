# Technical architecture lens

Use this lens for material technical commitments whose boundaries, ownership, coupling, operating burden, migration path, or future change cost could alter the strategic action. Apply the canonical reality protocol first; this file specialises the questions and evidence without redefining claim statuses or readiness states.

## Routing boundary

- Select this as the primary lens when the central decision is the technical shape: system, repository, package, service, deployment, runtime, data, identity, authentication, authorisation, shared capability, platform, build/adopt/extend/migrate path, or target architecture.
- Use project/product as primary when the central question is which user or operational outcome, product scope, experiment, or sequence should exist. Add technical architecture secondarily only when the technical shape materially changes feasibility, risk, cost, or action.
- Use technical architecture as the primary and project/product as the secondary when a technical boundary decision is live but its outcome or product consequences materially change the choice.
- Do not activate this lens for factual technical explanation, architecture description without a pending decision, local setup, routine implementation inside an approved direction, simple fixes, mechanical refactors, tests, or builds.
- Frameworks, vendor guidance, architecture documents, code and specialist recommendations are evidence to inspect, not decision authority.

## Supported decisions and outcomes

- Choose system, repository, deployment and ownership boundaries that fit the intended outcome and operating reality.
- Decide what should be shared, duplicated, colocated, separated, bought, adopted, extended, migrated, retired, or deliberately left local.
- Assign runtime, data, identity, authentication, authorisation, operational and change ownership explicitly.
- Compare current and target architecture, including coexistence, migration sequence, rollback, option preservation and the cost of future change.
- Decide whether a conceptual responsibility has earned a package, service, repository, deployable, platform or team boundary.

## Decision-relevant evidence

- The exact current artifact, repository, revision, runtime environment, deployment topology, data flow, trust boundary and user journey when each is material.
- Measured change frequency, shared consumers, independent deployment needs, failure isolation, latency, throughput, reliability, recovery, observability, security and privacy requirements.
- Team capability, ownership stability, delivery capacity, on-call and support load, infrastructure cost, vendor constraints, contractual obligations and exit costs.
- Concrete duplication and drift, coupling and cohesion, dependency direction, interface change history, test/runtime evidence and the cost of maintaining compatibility.
- Migration prerequisites, coexistence constraints, data conversion, rollback proof, failure modes and the evidence that the target can operate in the named environment.

## Causal mechanisms

- Trace how the proposed boundary changes coordination cost, failure propagation, release independence, security/trust exposure, runtime performance, operability and future change cost.
- Distinguish conceptual responsibilities from physical topology. A useful domain boundary does not automatically justify another package, service, repository, deployable or team.
- Compare sharing with deliberate duplication. Sharing can reduce drift while increasing coupling, release coordination and blast radius; duplication can preserve autonomy while increasing divergence and maintenance.
- Treat build, buy, adopt, extend and migrate as alternative causal paths with different ownership, lock-in, capability, transition and exit consequences.
- Model current-to-target coexistence, sequencing, rollback and learning. A target diagram without a credible transition is not an executable architecture.

## Stakeholder agency

- Name the owners of runtime, data, identity, authentication, authorisation, interfaces, operations, migration, security decisions and consumer adoption.
- Treat teams, platform owners, vendors and consumers as autonomous actors with incentives, capacity, roadmaps, decision rights and alternatives.
- Do not assume a shared component will be adopted, a vendor will close a gap, another team will accept operational ownership, or consumers will migrate on schedule without current evidence and a fallback.
- Separate documented authority and commitment from inferred willingness, competence or future cooperation.

## Characteristic failure modes

- Architecture astronautics: optimising conceptual elegance before a material boundary has earned physical separation.
- Premature extraction: turning contracts, layers or responsibilities into packages, services or repositories without independent change, ownership or deployment evidence.
- Framework capture: treating a framework, generated artifact, vendor reference architecture or methodology as authority rather than a constrained option.
- Accidental distributed monolith: adding network and operational failure modes while preserving coordinated releases and tightly coupled change.
- Duplicated or confused security boundaries, including treating shared data as shared permission or authentication as authorisation.
- Prototype-to-production leakage: carrying demonstration topology, fixtures, privileges, scale assumptions or operational shortcuts into a production commitment.
- Proof-layer substitution: treating tests or builds as runtime, deployment, security, operability, migration, usability or outcome proof.
- Migration without coexistence, rollback, ownership, data integrity or stop conditions.
- Local elegance that ignores team capability, support load, observability, cost, delivery speed or the strongest simpler rival.
- Technical debt as an unmeasured slogan rather than a causal constraint with a named change cost and decision implication.

## Out-of-scope boundaries

- Do not replace security, privacy, safety, legal, regulatory, financial, procurement, reliability or other specialist audits and decisions. Identify the dependency and what evidence could change the architecture conclusion.
- Do not infer that a technically coherent system will create product value, adoption, demand or commercial viability.
- Do not use this lens to prescribe framework-specific implementation when the material architecture direction is already approved; return to the relevant implementation skill or repository process.
- Do not create a reusable platform, shared package or service merely because multiple projects use similar vocabulary.

## Readiness implications

- **Ready:** the exact current baseline is inspected enough for the consequence; the boundary and ownership mechanisms are supported; operational and migration constraints are understood; and downside controls match reversibility.
- **Conditional:** a bounded spike, coexistence stage, permission, capacity threshold, rollback proof, specialist review or consumer commitment can responsibly limit exposure. Name and verify every condition.
- **Not validated:** a load-bearing topology, ownership, runtime, data, trust, operability, migration, adoption or cost claim lacks discriminating evidence. Prefer the cheapest boundary or migration test.
- **Infeasible as posed:** current evidence establishes that a binding technical, contractual, operational or authority constraint conflicts with the proposed shape. State what scope, architecture, owner or constraint must change.

## Application checklist

1. Lock the exact current and proposed decision baseline, including only the artifact, revision, environment, state, scope and journey fields that matter.
2. State the intended product or operational outcome and whether project/product or technical architecture is primary.
3. Map conceptual responsibilities, physical boundaries, owners, trust/data flows, coupling and independent change needs separately.
4. Compare the strongest simpler or more reversible rival across build/adopt/migrate, operating burden, failure modes and future change cost.
5. Define coexistence, migration, rollback, observability, stop conditions and the specialist evidence still required.
