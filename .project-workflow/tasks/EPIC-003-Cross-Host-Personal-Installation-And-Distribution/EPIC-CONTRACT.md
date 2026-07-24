# Epic Contract

## Epic

- ID: EPIC-003
- Title: Cross-Host Personal Installation And Distribution

## Sources Of Truth

- Product behaviour: `skills/strategic-advisor/`
- Runtime allowlist: `skills/strategic-advisor/runtime-manifest.json`
- Product claims: `PRODUCT-CONTRACT.md`
- Install pipeline: `scripts/build_install_artifacts.py`
- Public onboarding: `README.md` and `INSTALL.md`
- Host eligibility and UI prerequisites: current official OpenAI and Anthropic documentation, refreshed during implementation
- Execution lifecycle: this Epic tracker and scaffolded child documents

## Invariants

- One canonical Strategic Advisor runtime owns strategic logic.
- Host adapters are deterministic projections or unchanged packages of that runtime, never independently maintained strategic prompts.
- The evaluation plane, Project Workflow files, private cases, credentials, and retained hidden reasoning never enter install artifacts.
- A Strategy Workspace is optional and is never created or accessed by this Epic.
- One host's package acceptance, activation, or behaviour does not prove another host.
- Package build, installation, discovery, activation, behavioural smoke, validation, support, and effectiveness remain distinct claims.
- No enterprise control is bypassed, and unavailable account/admin prerequisites remain explicit.
- All live checks use public fictional cases and retain only bounded evidence.

## Invalid Substitutes

- The repository authoring symlink in place of John's personal Codex install.
- A stale global install in place of the current release artifact.
- Archive structure or upload success in place of visible host discovery and activation.
- A model statement that it used the Skill in place of an independently observable activation/source event.
- Codex evidence in place of ChatGPT or Claude evidence.
- A personal ChatGPT Custom GPT in place of an unavailable ChatGPT Personal Skill claim.
- A generated Custom GPT prompt that has drifted from canonical `SKILL.md`.
- A ChatGPT or Claude screenshot containing private account, employer, or case information in public evidence.
- Administrator denial in place of claiming the Claude package is defective, or package readiness in place of claiming Claude activation passed.
- The bounded Codex drift smoke in place of ChatGPT/Claude behavioural parity or effectiveness evidence.

## Artifact Targets

- Deterministic standalone Skill ZIP for Codex and Claude.
- Existing deterministic OpenAI local-plugin ZIP where applicable.
- Deterministic ChatGPT Custom GPT kit with generated Instructions, declared Knowledge inventory, configuration, first-use guide, and provenance.
- One cross-artifact provenance authority tied to exact source revision and runtime identity.
- Public release assets and concise host-specific onboarding.
- Bounded Codex, ChatGPT, and Claude host evidence only where live execution occurs.

## Parent AC Proof Ownership

| Parent AC | Proof Owner | Required Evidence |
| --- | --- | --- |
| AC1 | Cross-host distribution child | Repeated clean build identity, exact provenance, safe inventories, and leakage scans. |
| AC2 | Cross-host distribution child | Generated Instructions/source binding, exact Knowledge inventory/bytes, file-limit check, and negative drift tests. |
| AC3 | Codex and ChatGPT child | Fresh neutral Codex discovery/activation trace tied to John's exact personal install and release identity. |
| AC4 | Codex and ChatGPT child | Current Custom GPT configuration plus Preview trigger/non-trigger observations and link/copy handoff result. |
| AC5 | Claude handoff child | Official-structure verification, enterprise preflight result, and live upload/activation evidence or explicit admin blocker. |
| AC6 | Codex and ChatGPT child, Claude handoff child | Named-user first-use walkthroughs reaching a fictional activation check without developer setup. |
| AC7 | All children | Structured and prose claim comparison against exact retained evidence. |
| AC8 | Cross-host distribution child | Current lens/workspace runtime inventory plus no-workspace/no-connector first-use proof. |
| AC9 | All children | Unit, aggregate, artifact, privacy, clean-checkout, QA, doctor, and closeout evidence. |
