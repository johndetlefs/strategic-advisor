## User Story

As a first-time or returning Strategic Advisor user, I want a progressive
onboarding path that starts with one useful decision and introduces durable
continuity only when needed, so that setup does not obscure the product or grant
implicit authority.

## Parent AC Coverage

- AC7, AC9, AC10, AC13

## Child Charter

### Inherited Invariants

- Strategic Advisor remains useful without a repository or workspace.
- The full strategic protocol is selectively invoked by decision intent and consequence, not by keywords, repository location, or workspace presence.
- Open exploration may remain conversational until a decision object emerges; readiness is not manufactured merely to complete a response template.
- Operate at the minimum sufficient altitude and return from exploration to a bounded decision or validation step.
- Dialogue may expand the option set; only qualifying evidence, scope, or constraints may change claim support or readiness.
- Opposite user preferences on the same material facts do not change the diagnosis.
- Stored context is input, never authority; provenance, conflict, freshness, and material limitations remain visible.
- Durable writes require explicit owner approval of the proposed change.
- Discussing projects in the same conversation does not authorise integration, shared storage, or a dependency between them.
- The private owner workspace never enters public source, examples, evaluations, packages, logs, or retained evidence.
- One canonical skill remains the only source of strategic logic.
- Host, workspace, connector, domain, and behavioural claims do not exceed direct current proof.
- Business/venture and marketing/growth may be implemented for alpha use while remaining explicitly unvalidated and unsupported.

### Invalid Substitutes

- A repository template, documentation, or first-party enthusiasm in place of observed multi-turn behaviour.
- More conversational prose, more questions, or longer answers in place of genuinely distinct alternatives and decision-relevant exploration.
- Project or strategy vocabulary, repository location, or workspace presence in place of a material strategic decision that justifies invoking the full protocol.
- A readiness verdict, formal section structure, or strategic terminology added as ceremony to an ordinary factual, status, implementation, summarisation, simple-edit, or casual-ideation response.
- User agreement, repeated claims, polished narrative, or stored prior decisions in place of qualifying evidence.
- A single-turn prompt that narrates several turns in place of an actual fresh multi-turn interaction.
- A public fixture, copied example, or template-only check in place of authorised private-owner dogfood.
- Private workspace prose, reconstructable summaries, repository identifiers, or raw transcripts committed as public evidence.
- A host project, connector, memory store, or adapter-side prompt copy in place of the canonical skill and portable workspace contract.
- Local source files or a different package revision in place of exact runtime-package and host-source proof.
- Codex proof in place of Claude, ChatGPT, or general connector support.
- A supplied whole-person preference in place of a supported general-life, financial, medical, legal, family, or relationship domain.
- Structural checks, single-turn prompts that narrate multiple reviews, or the retired TASK-007 attempt in place of observed actual-turn behaviour. The compact drift smoke proves only its named invariants and cannot promote business, marketing, comparative-superiority, or broad support claims.

### Artifact Targets

- Canonical behaviour: updated core skill/reference files under `skills/strategic-advisor/`, including the invocation boundary and proportional exploration-to-checkpoint transition.
- Workspace product surface: portable Markdown templates/instructions named by the runtime allowlist plus a deterministic scaffold builder and validator.
- Evaluation authority: existing evaluation material remains excluded from model-visible packages; the retired TASK-007 attempt cannot be used as passing evidence. TASK-012 binds a compact actual-turn drift smoke to the then-current runtime and host. The larger comparative authority remains required before capability promotion or superiority claims.
- Host proof: sanitised Codex trace identifying exact model, host, runtime package, workspace template, authorised source class, and observed result/write-control class.
- Public contract: bounded README, installation, architecture, and structured capability updates.
- Private dogfood: a separate private repository with no path, content, or reconstructable case data required in public artifacts.

### Parent AC Proof Ownership

- AC7: owner `TASK-008, TASK-009, TASK-010, TASK-011`; required evidence: Fresh no-workspace journey plus optional continuity journey.
- AC9: owner `TASK-009, TASK-011`; required evidence: Runtime/install allowlist identity, deterministic builds, tests, and forbidden-content scans.
- AC10: owner `TASK-008, TASK-010, TASK-011, TASK-012`; required evidence: Current public-claim comparison against structured capability and exact retained proof.
- AC13: owner `TASK-008, TASK-009, TASK-010, TASK-011`; required evidence: Fresh-context host/workspace controls proving no location-triggered invocation, unnecessary reads, silent writes, or inferred coupling.

## Acceptance Criteria

- [x] AC1: README and INSTALL provide an ordered no-workspace first-use path and
  optional workspace-backed continuity path. Covers parent AC7.
- [x] AC2: Deterministic runtime/install builds, allowlist validation, privacy
  checks, and forbidden-content scans pass against the delivered source. Covers
  parent AC9.
- [x] AC3: README, INSTALL, PRODUCT-CONTRACT, and structured capability claims
  retain current pre-release and implemented-not-validated boundaries. Covers
  parent AC10.
- [x] AC4: Public onboarding states that workspace or repository presence grants
  no invocation, read, write, disclosure, integration, external-action, or
  cross-workspace authority. Covers parent AC13.

## Validation

- AC1 / parent AC7: inspect the ordered onboarding sections and internal links.
- AC2 / parent AC9: run `python3 scripts/build_evals.py --check`,
  `python3 scripts/validate.py`, `python3 -m unittest discover -s tests -v`,
  and two clean deterministic install-artifact builds.
- AC3 / parent AC10: run claims validation and manually compare public prose
  with the machine-readable product contract.
- AC4 / parent AC13: inspect README, INSTALL, canonical invocation boundary, and
  workspace contract for explicit authority separation.

## Task List

| ID | Title | Description | Acceptance Criteria | User Verification | Status |
| --: | ----- | ----------- | ------------------- | ----------------- | ------ |
| 1 | Publish progressive onboarding | Add one clear no-workspace first-use path followed by optional authorised continuity without duplicating strategic logic. | AC1, AC4 | Inspect README and INSTALL ordering and authority language. | Done |
| 2 | Verify runtime and public claims | Prove the documentation points to deterministic allowlisted artifacts and does not overstate maturity, host, domain, workspace, or behavioural evidence. | AC2, AC3 | Run deterministic builders, repository checks, unit tests, privacy scans, and claim review. | Done |
| 3 | Complete QA and parent evidence | Record child evidence, run QA/code review and Doctor, then complete the child and refresh the Epic audit. | AC1, AC2, AC3, AC4 | Review the child evidence map and EPIC-002 acceptance audit. | Done |

## Parent AC Evidence

- AC7: `README.md` and `INSTALL.md` now present immediate no-workspace use before
  optional workspace-backed continuity.
- AC9: `python3 scripts/build_evals.py --check`, all seven repository validator
  scopes, and the full unit suite passed on 2026-07-26. Two independent
  install-artifact builds were byte-identical with runtime identity
  `fbe0b4f80d3af8c373f728549c1011e3e3d70212400fc3c4e7a7166c0691eaee`.
- AC10: README and INSTALL retain the pre-release and exact-proof boundaries
  enforced by `PRODUCT-CONTRACT.md`; the claims validator passed.
- AC13: README, INSTALL, canonical `SKILL.md`, and the workspace contract all
  state that repository/workspace presence grants no automatic invocation or
  authority.
- No structured proof recipe applies to this documentation-only child.

## QA & Code Review

- Date: 2026-07-26
- Reviewed areas: Progressive onboarding order, optional-continuity boundary,
  invocation and authority separation, canonical runtime/install references,
  public maturity claims, deterministic packaging, privacy, and workflow state.
- Validation evidence:
  - `python3 scripts/build_evals.py --check`: PASS, 45 combined cases current.
  - `python3 scripts/validate.py`: PASS, all seven scopes.
  - `python3 -m unittest discover -s tests -v`: PASS, 125 tests.
  - Two independent dirty-source exploratory install builds produced identical
    standalone, plugin, Custom GPT, provenance, and runtime identities.
  - Runtime identity:
    `fbe0b4f80d3af8c373f728549c1011e3e3d70212400fc3c4e7a7166c0691eaee`.
  - `git diff --check`: PASS.
  - `./.project-workflow/cli/workflow doctor`: PASS, no issues.
- Findings: None. The documentation does not promote any host, domain,
  workspace, or behaviour beyond the current product contract.
- Verdict: Pass.

## Retro

- Date: 2026-07-26
- Reusable lessons:
  - Progressive onboarding is clearer when first value and optional durable
    continuity are separate stages rather than one setup ceremony.
  - Authority separation must be visible at the point where the workspace is
    introduced, not only in the deeper workspace contract.
  - Explicit proof-recipe IDs in task prose trigger structured evidence even
    when the prose says the recipe does not apply.
- Conventions or agent assets updated:
  - `.project-workflow/guidance.md` now requires generic no-recipe wording when
    no structured proof applies.
- Follow-up tasks:
  - None from this child. Owner dogfood through 2026-08-31 is an observation
    period, not a pre-created implementation task.
- Missed in-scope work: None.

## Notes

- Task: TASK-011
- Title: Publish Progressive Workspace Onboarding
- Created: 2026-07-26
