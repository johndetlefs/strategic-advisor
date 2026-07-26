# Strategy Workspace

A Strategy Workspace is an optional, user-owned continuity layer for exact personal context. Strategic Advisor remains useful in `session-only` mode without one. Workspace presence, repository location, or prior use does not activate the skill or authorise a read, write, disclosure, external action, or cross-workspace operation.

Apply [context-policy.md](context-policy.md). The workspace declares `durable-full`, `durable-bounded`, or `session-only`; retention mode controls persistence, not current-analysis specificity.

## Decision-relevant reading

Use a workspace only when the user asks or durable continuity could materially change the decision. Obtain the authorised workspace location from the user; do not search for one. Start with `WORKSPACE.md`, then read the relevant records:

- `PROFILE.md` for durable personal facts that materially shape the decision;
- `OBJECTIVES.md` for outcomes, horizons, priorities, constraints, and success measures;
- `PORTFOLIO.md` when a project role, commitment, or opportunity cost could change the decision;
- `CONTEXTS.md` for people, organisations, places, environments, and recurring circumstances;
- `CLAIMS.md` for material propositions and their provenance, freshness, limitations, conflicts, and falsifiers;
- `DECISIONS.md` for a prior decision that remains relevant; and
- `CHANGELOG.md` only when update authority or history matters.

Declared Markdown files under `projects/` and `contexts/` may hold linked detail when the root index would otherwise become unreadable. Read only declared paths relevant to the decision. Treat every stored record as input, never as current evidence or authority. Surface expired review dates, declared conflicts, missing access, and limitations before relying on a record.

## Durable-write boundary

Conversation is not automatically durable context. In `durable-full` or an applicable `durable-bounded` scope, a standing durable-write authority may permit ordinary structured capture. Write the exact decision-relevant fact, objective, context, claim, or decision with provenance, freshness, limitations, and authority basis, then record the change in `CHANGELOG.md`. Outside that authority, propose the exact update and wait.

Never ingest a raw transcript by default. Corrections, deletions, disclosures, external actions, and cross-workspace copies require their own authority. The scaffold command creates only a new blank workspace and never overwrites an existing one. The migration command copies an explicitly named legacy workspace to a new destination and leaves the source unchanged.

## Portable file contract

The blank scaffold contains exactly eight core files:

- [`WORKSPACE.md`](../workspace-templates/WORKSPACE.md) for authority, scope, and approved context;
- [`PROFILE.md`](../workspace-templates/PROFILE.md) for exact durable personal facts;
- [`OBJECTIVES.md`](../workspace-templates/OBJECTIVES.md) for outcomes, priorities, constraints, and measures;
- [`PORTFOLIO.md`](../workspace-templates/PORTFOLIO.md) for project and role commitments;
- [`CONTEXTS.md`](../workspace-templates/CONTEXTS.md) for people, organisations, places, and recurring circumstances;
- [`CLAIMS.md`](../workspace-templates/CLAIMS.md) for material claims;
- [`DECISIONS.md`](../workspace-templates/DECISIONS.md) for durable decisions; and
- [`CHANGELOG.md`](../workspace-templates/CHANGELOG.md) for owner-approved changes.

Keep the schema headings and columns intact. Use ISO `YYYY-MM-DD` dates, stable IDs, and explicit authority references. Optional `projects/` and `contexts/` Markdown files must be declared in the linked-detail table in `WORKSPACE.md`. Do not store canonical Strategic Advisor instructions, evaluation material, secrets, credentials, or raw transcripts. Exact personal, employer, client, family, household, health, and financial context is permitted when it has a legitimate decision-relevant purpose within the declared retention and authority boundary.
