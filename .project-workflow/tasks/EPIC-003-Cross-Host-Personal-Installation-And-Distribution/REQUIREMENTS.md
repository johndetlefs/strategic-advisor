# Requirements

## Summary

- Task: EPIC-003
- Title: Cross-Host Personal Installation And Distribution
- Last updated: 2026-07-24

## Backlog Source

- ID: BL-005
- Title: Cross-Host Personal Installation And Distribution
- Type: Epic Candidate
- Priority: High
- Status before promotion: Proposed
- Outcome: John and Christina can install the same current Strategic Advisor alpha in Codex, a personal ChatGPT custom GPT, and managed Claude.ai through deterministic host-appropriate packages, concise onboarding, and exact activation evidence without requiring a Strategy Workspace.
- Notes: Promoted by owner direction in dedicated Codex conversation 2026-07-24. ChatGPT Plus uses a custom GPT because Personal Skills are limited to managed plans; Claude Enterprise upload remains subject to organisation Skills and code-execution controls.

## Owner Approval

- Requirements reviewed by owner: Yes
- Acceptance criteria reviewed by owner: Yes
- Approved for decomposition: Yes
- Approved for implementation: No
- Approved scope envelope: Yes
- Approved by: John Detlefs
- Approval date: 2026-07-24
- Approval note / source: Dedicated Codex conversation 2026-07-24: owner replied Approved, go for it to the exact EPIC-003 nine-AC envelope
- Approved artifact identity: sha256:eb405315a3d27351b2c3c3b1272ee9db5112131294727a3db6f03e402faf666d

## Goal

Make the current Strategic Advisor alpha genuinely installable and usable by John and Christina on the host surfaces they actually have: Codex, personal paid ChatGPT, and Canva-managed Claude Enterprise. Each route must use deterministic artifacts derived from the same canonical runtime, have concise account-appropriate installation steps, and retain only the proof needed to distinguish package readiness from live host activation.

## Non-Goals

- Creating or accessing a private Strategy Workspace, private case repository, Daily Checklist, or private decision data.
- Making a Strategy Workspace, repository, connector, MCP server, database, or external service a prerequisite for first use.
- Publishing a public ChatGPT Plugin Directory entry, GPT Store listing, Claude organisation-wide skill, or marketplace submission.
- Adding actions, apps, connectors, code dependencies, telemetry, authentication, billing, or hosted infrastructure.
- Claiming cross-host parity, universal drift resistance, independent human validation, comparative superiority, supported domains, or consequential-use fitness.
- Circumventing Canva or other enterprise administrator controls. If Claude Skills or code execution is disabled, record the exact admin prerequisite instead.
- Repeating the large comparative evaluation programme. The existing bounded drift smoke remains the behavioural evidence for its exact runtime/model/host only.

## Users & Context

- John currently sees the repository-linked authoring Skill in Codex, but his personal global Codex installation is an older runtime and must be replaced by a generated current artifact.
- John wants a usable Strategic Advisor inside personal ChatGPT.
- Christina has a paid personal ChatGPT account but not ChatGPT Pro. Paid personal accounts can create custom GPTs, while ChatGPT Personal Skills are currently generally available only on managed Business, Enterprise, Healthcare, and Edu plans.
- Christina uses a Canva-managed Claude Enterprise account. Claude custom Skills are available on Enterprise only when organisation owners enable Skills plus code execution and file creation; an individual member can then upload a Skill ZIP unless further organisation policy prevents it.
- John and Christina need immediate one-decision onboarding before any optional continuity workflow.
- Maintainers need a release whose host adapters are mechanically derived from one canonical runtime and whose public language does not treat a package build, upload receipt, or model answer as stronger host or behavioural proof.

## Requirements (Outcome-Focused)

- R1. Publish one current early-access release containing a standalone Agent Skill ZIP for Codex and Claude, the existing OpenAI local-plugin ZIP where applicable, a deterministic ChatGPT Custom GPT kit, and one provenance document tying every artifact to the exact source revision and runtime-package identity.
- R2. The standalone Skill and plugin contain the allowlisted runtime bytes unchanged and exclude evaluations, evaluation results, workflow files, private data, credentials, and host-specific strategic copies.
- R3. The ChatGPT kit contains a generated Instructions artifact whose strategic body is byte-derived from canonical `SKILL.md`, not independently authored, plus exactly the remaining runtime reference/template files needed as Custom GPT Knowledge. The adapter may add a short host bootstrap and provenance metadata but may not fork strategic logic.
- R4. The ChatGPT configuration names the GPT, describes its bounded professional/commercial purpose, supplies useful conversation starters, enables no apps or actions, and explains the pre-release/human-authority boundary without bloating ordinary responses.
- R5. John can install the exact release Skill globally in Codex, start a fresh task, and produce an independently observable source-access/activation trace tied to the release identity. The repository authoring symlink is not a substitute.
- R6. John can create and preview the Custom GPT from the exact kit. The resulting GPT can be shared by link for Christina's immediate use, and the same kit lets Christina create an independently owned copy on her paid personal account if she prefers.
- R7. Christina can upload the unchanged standalone ZIP through Claude **Customize → Skills** when her enterprise controls permit it. The onboarding must surface the exact Skills/code-execution admin prerequisite before upload and provide a short fictional activation check after enablement.
- R8. Each live host check uses only public fictional prompts, records the exact artifact identity and available host/model/account surface, and treats visible discovery/activation/source use as distinct from answer quality.
- R9. README and installation guidance lead with three short user paths—John in Codex, John/Christina in ChatGPT, Christina in Claude—then place verification, troubleshooting, workspace continuity, and developer build details behind those first-use paths.
- R10. No-workspace use is the default onboarding journey. The optional Strategy Workspace remains secondary, user-owned, and subject to its existing read/write/provenance controls.
- R11. Host capability state and release language fail closed: unperformed or admin-blocked live checks remain `implemented-not-validated`; one host's proof never promotes another host or the core behaviour generally.
- R12. The delivery remains maintainable: use Python standard library and existing builders/tests, extend the current deterministic artifact pipeline rather than creating a second packaging system, and test only material archive, provenance, leakage, configuration, and stale-source failure modes.

## Acceptance Criteria (Verifiable)

- AC1: A clean current checkout builds all release artifacts twice with identical bytes, one provenance authority, the exact current source revision/runtime identity, safe archive paths, and no evaluation, workflow, credential, private-data, or unexpected-file leakage.
- AC2: The ChatGPT kit verifier proves that its strategic Instructions body derives from the exact canonical `SKILL.md`, its Knowledge inventory is the exact declared set within ChatGPT's 20-file limit, all copied knowledge bytes match the runtime package, and any source/config/inventory drift fails.
- AC3: A fresh Codex task discovers and activates John's personal global install from the exact release artifact rather than the repository symlink; retained public evidence identifies the archive/runtime/source and source-access result without private case content.
- AC4: A Custom GPT can be built in John's paid ChatGPT account from the kit, passes the frozen fictional activation and selective-invocation smoke in Preview, and is either shared by link for Christina or accompanied by exact independent-copy steps. Account/UI/model facts are recorded; builder self-report alone is insufficient.
- AC5: The standalone ZIP passes official Claude custom-Skill structure and deterministic package checks. Christina's Claude Enterprise path has a verified preflight for Skills plus code execution, exact upload/enable steps, and a fictional fresh-chat smoke; if admin controls prevent execution, the artifact remains ready but Claude activation stays explicitly unverified.
- AC6: README and `INSTALL.md` let each named user reach their relevant install path and first fictional check without reading developer architecture, evaluation protocol, or Strategy Workspace material first.
- AC7: Product contract, structured capability state, release notes, and public prose distinguish built, installed, activated, behaviourally smoke-checked, validated, and supported for each exact host, with no cross-host or effectiveness inference.
- AC8: The current release contains the implemented business/venture and marketing/growth lenses plus the optional Strategy Workspace runtime files, but first use requires neither a workspace nor connector and does not promote those lenses beyond current evidence.
- AC9: Relevant unit tests, aggregate validation, install verification, privacy/secret scans, clean-checkout reproduction, QA/code review, and Project Workflow doctor pass before release or installation claims are closed.

## Open Questions (Answer Needed)

- None after owner approval of this envelope. Live ChatGPT and Claude account interfaces may expose admin or account-specific blockers; those are execution evidence to record, not reasons to invent alternative product behaviour.

## Decisions (Resolved)

- D1. Treat this as a coordinated cross-host distribution Epic rather than overloading the Codex-only EPIC-002 children.
- D2. Use the standard standalone Agent Skill ZIP unchanged for Codex and Claude.
- D3. Use a deterministic Custom GPT kit for personal ChatGPT accounts because current OpenAI Personal Skills availability excludes personal Plus/Pro accounts. Do not mislabel the Custom GPT as a Personal Skill.
- D4. The Custom GPT Instructions embed a generated canonical `SKILL.md` body because OpenAI directs builders to place behavioural rules in Instructions rather than Knowledge. Remaining runtime references/templates become Knowledge, keeping the total within the current 20-file limit.
- D5. Generated host configuration is an adapter artifact, not a second source of strategic truth. Any mismatch with canonical runtime fails validation.
- D6. Share-by-link is the fastest Christina ChatGPT path. An independently owned copy remains available from the same kit.
- D7. Christina or a Canva Claude administrator must perform account-scoped enterprise actions. The public repository will not contain employer data, organisation identifiers, screenshots with private content, or credentials.
- D8. Use fictional activation cases only. Real household, employer, client, or strategic cases begin only after installation and are not public validation artifacts.
- D9. Publish a new alpha release rather than silently replacing `v0.1.0-alpha.1`; exact version selection is a reversible release detail determined during planning.
- D10. No additional virtual environment is needed. The repository deliberately uses Python's standard library and existing deterministic scripts.

## Validation Plan

- AC1-AC2: Extend the deterministic install builder and tests; build twice from a clean checkout; compare archive/provenance bytes; run negative fixtures for source, inventory, path, configuration, and private/evaluation leakage.
- AC3: Install the generated standalone artifact at John's personal Codex scope, launch a fresh neutral task, and retain a bounded source-access trace plus exact artifact/runtime identities.
- AC4: Use the current ChatGPT Custom GPT editor in John's paid account, upload the generated knowledge files, paste the generated instructions, run frozen fictional trigger/non-trigger prompts in Preview, and record visible configuration/activation facts. Then exercise share-by-link or record the exact unavailable control.
- AC5: Validate the archive against the official Claude Skill structure, then have Christina run or observe the enterprise preflight/upload/enable/fresh-chat steps. Retain only account-class, setting/result class, artifact identity, and fictional output observations.
- AC6-AC8: Perform a first-use documentation walkthrough for each named route and compare every claim with the structured product contract and retained evidence.
- AC9: Run the full unit suite, aggregate validator, artifact verifier, syntax/diff checks, workflow doctor, clean-checkout build, project QA/code review, and retro before closing the Epic children.

## Proposed Child Work

| Proposed Child | Parent ACs | Purpose |
| --- | --- | --- |
| Build Current Cross-Host Alpha Distribution | AC1, AC2, AC7, AC8, AC9 | Extend the existing deterministic release pipeline with a Custom GPT kit, publish exact current artifacts, and keep all host packages tied to one canonical runtime. |
| Install And Prove Personal Codex And ChatGPT | AC3, AC4, AC6, AC7, AC9 | Replace John's stale personal Codex install, create/preview/share the personal Custom GPT, and retain bounded exact-host activation evidence. |
| Enable Christina Claude And First-Use Handoff | AC5, AC6, AC7, AC9 | Provide the enterprise-control preflight, unchanged Skill upload, fictional activation check, and concise Christina handoff without accessing private cases or bypassing administrators. |
