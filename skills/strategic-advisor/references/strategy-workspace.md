# Optional Strategy Workspace

A Strategy Workspace is an optional, user-owned continuity layer for approved context. Strategic Advisor must remain fully useful without one. Workspace presence, repository location, or prior use does not activate the skill, authorise a read or write, broaden scope, or create an integration between projects.

## Minimum-data reading

Use a workspace only when the user asks or durable continuity could materially change the current professional or commercial decision. Obtain the authorised workspace location from the user; do not search for one. Start with `WORKSPACE.md`, then read only the relevant rows or files:

- `PORTFOLIO.md` when a project role, commitment, or opportunity cost could change the decision;
- `CLAIMS.md` for material propositions and their provenance, freshness, limitations, conflicts, and falsifiers;
- `DECISIONS.md` for a prior decision that remains relevant; and
- `CHANGELOG.md` only when update authority or history matters.

Do not load the whole workspace merely because it exists. Treat every stored record as input, never as current evidence or authority. Surface expired review dates, declared conflicts, missing access, and limitations before relying on a record. Current qualifying evidence may supersede stored content; narrative continuity may not.

## Durable-write boundary

Conversation is not durable context. When a durable update would help:

1. propose the exact target file, record ID, field values, provenance, review date, and reason;
2. wait for explicit owner approval of that proposed change;
3. write only the approved change when the host grants file authority; and
4. record the approved change in `CHANGELOG.md`.

Never create a workspace, apply a proposed update, ingest a transcript, or copy content across projects without explicit authority. The repository scaffold command creates only a new blank workspace and never updates an existing one.

## Portable file contract

The blank scaffold contains exactly:

- [`WORKSPACE.md`](../workspace-templates/WORKSPACE.md) for authority, scope, and approved context;
- [`PORTFOLIO.md`](../workspace-templates/PORTFOLIO.md) for project and role commitments;
- [`CLAIMS.md`](../workspace-templates/CLAIMS.md) for material claims;
- [`DECISIONS.md`](../workspace-templates/DECISIONS.md) for durable decisions; and
- [`CHANGELOG.md`](../workspace-templates/CHANGELOG.md) for owner-approved changes.

Keep the schema headings and columns intact. Use ISO `YYYY-MM-DD` dates, stable IDs, and explicit owner-approval references. Do not store canonical Strategic Advisor instructions, evaluation material, secrets, raw transcripts, or unnecessary personal, employer, client, household, or credential data.
