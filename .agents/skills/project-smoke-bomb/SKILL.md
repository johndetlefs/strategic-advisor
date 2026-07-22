---
name: project-smoke-bomb
description: Use when preparing a sanitized client ZIP from an agency-owned project-workflow repository.
---

<!-- project-workflow:generated -->

# Project Smoke Bomb

Prepare a deliberate client handoff without transferring agency-only workflow state or stripping the project of useful human and agent context.

## Invocation Rules

- Use this skill when the user asks for a Smoke Bomb, sanitized client handoff, clean client ZIP, or removal of project-workflow from a delivery copy.
- Read `AGENTS.md`, `.project-workflow/guidance.md`, `README.md`, the active task state, and repository-specific delivery instructions before preparing the handoff.
- Use the canonical `project smoke-bomb` command for planning, mutation, validation, and export. Do not imitate it with broad deletion commands or an unconstrained ZIP operation.

## Workflow

1. Confirm the agency-owned repository is authoritative and identify the exact client, intended client agent targets, and ZIP output path.
2. Recommend a disposable branch such as `smoke-bomb/<client-or-handoff>`. Branch creation, commits, pushes, and deletion remain normal user-controlled Git operations; do not force them inside Smoke Bomb.
3. Review and prepare client-facing context before cleanup:
   - keep a substantive `README.md` with purpose, setup, architecture pointers, validation, and delivery guidance;
   - retain substantive user-authored `AGENTS.md` content outside the project-workflow managed block, or place verified repository guidance in `.project-workflow/guidance.md` so the command can produce the canonical client agent guide;
   - choose only the client agent targets actually needed: `codex`, `claude-code`, `cursor`, or `github-copilot`;
   - identify explicit non-interactive validation commands; never invent a command or claim undocumented architecture.
4. Commit or otherwise clean the dedicated worktree before planning. Smoke Bomb refuses dirty worktrees so the reviewed plan has an exact source state.
5. Run a non-mutating plan, preferably JSON for automation:

   ```bash
   project smoke-bomb \
     --client-agent codex \
     --validation-command "<reviewed command>" \
     --output "<path outside the repository>/client-handoff.zip" \
     --plan --format json
   ```

6. Review repository and branch identity, every delete/replace/create action, ownership evidence, README and agent targets, validation commands, exclusions, blockers, warnings, and the plan fingerprint.
7. Resolve every blocker in the source branch and regenerate the plan. Never bypass an ambiguous ownership, secret-like path, unsafe file type, missing guidance, dirty state, or residual project-workflow reference finding.
8. Apply only the exact reviewed plan. Authorized non-interactive agents add `--yes`; human invocation confirms interactively:

   ```bash
   project smoke-bomb \
     --client-agent codex \
     --validation-command "<reviewed command>" \
     --output "<path outside the repository>/client-handoff.zip" \
     --apply --plan-fingerprint <SHA256> --yes --format json
   ```

9. Verify the result reports `exported`, all reviewed validations passed, the ZIP path and SHA-256 are present, the inventory contains no `.git` or `.project-workflow`, and the intended README and client-agent instructions are included.
10. Hand over the ZIP and its SHA-256. Keep the agency repository and normal branches intact; the client may initialize its own repository from the snapshot.

## Guardrails

- Smoke Bomb is not a secret scanner, legal review, license audit, or proof that every file is client-appropriate. Resolve those responsibilities separately before handoff.
- Do not hand over the agency Git repository or history when the agreed deliverable is the sanitized ZIP.
- Do not treat the absence of the string `project-workflow` as sufficient proof; rely on the reviewed action inventory, exact Git-visible archive inventory, validation results, and client guidance checks.
- If validation fails, no ZIP is produced. Inspect the failure and the branch diff before deciding whether to restore, amend, or rerun.
