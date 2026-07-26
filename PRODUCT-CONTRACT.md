# Product contract

This document is the public source of truth for what Strategic Advisor may claim. It is deliberately stricter than a roadmap.

## Capability states

- **Planned:** an intended artifact or behaviour does not yet exist in reviewable form.
- **Implemented but not validated:** relevant source exists, but required behavioural, host, or release evidence is absent or incomplete.
- **Validated:** the current revision has direct evidence satisfying its declared gate. Only a validated capability may be called **supported**.
- **Out of scope:** the capability is not promised by the current v0 scope.

Documentation, a passing structural validator, model self-assessment, maintainer confidence, and user praise are not behavioural validation. Evidence must identify the exact revision and target the exact claim.

## Machine-readable claim registry

The validator treats the JSON between the markers below as authoritative. `supported_capabilities` must contain exactly the capability IDs whose state is `validated` and whose structured evidence passes validation.

A validated capability's `evidence` array contains objects with exactly `artifact`, `claim_id`, `gate`, `sha256`, `source_revision`, and `verdict`. The artifact must be a regular JSON file under `evidence/capabilities/`; its bytes must match `sha256`; and its own `claim_id`, kind-specific gate, non-zero 40-character source revision, and `pass` verdict must match the registry entry. A non-empty string, documentation link, model self-assessment, or unverified URL is not capability evidence. Capabilities in every other state keep an empty evidence array.

<!-- strategic-advisor-contract:start -->
```json
{
  "schema_version": 1,
  "release_status": "pre-release",
  "early_access_distribution_version": "0.2.0-alpha.2",
  "capability_promotion_enabled": false,
  "canonical_product_path": "skills/strategic-advisor/",
  "supported_installation_available": false,
  "runtime_package_manifest": "skills/strategic-advisor/runtime-manifest.json",
  "install_artifact_builder": "scripts/build_install_artifacts.py",
  "supported_capabilities": [],
  "capabilities": [
    {
      "id": "core.reality-protocol",
      "kind": "behaviour",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "core.interactive-strategy",
      "kind": "behaviour",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "core.open-field-exploration",
      "kind": "behaviour",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "core.personal-context",
      "kind": "behaviour",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "workspace.durable-personal-context",
      "kind": "behaviour",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "domain.project-product",
      "kind": "domain",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "domain.career",
      "kind": "domain",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "domain.organizational-influence",
      "kind": "domain",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "domain.people-leadership",
      "kind": "domain",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "domain.business-venture",
      "kind": "domain",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "domain.marketing-growth",
      "kind": "domain",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "domain.legal",
      "kind": "domain",
      "state": "out-of-scope",
      "evidence": []
    },
    {
      "id": "domain.medical-clinical",
      "kind": "domain",
      "state": "out-of-scope",
      "evidence": []
    },
    {
      "id": "domain.financial",
      "kind": "domain",
      "state": "out-of-scope",
      "evidence": []
    },
    {
      "id": "host.codex-local-authoring",
      "kind": "host",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "host.codex-runtime-package",
      "kind": "host",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "host.chatgpt-custom-skill",
      "kind": "host",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "host.chatgpt-custom-gpt",
      "kind": "host",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "host.chatgpt-desktop-local-plugin",
      "kind": "host",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "host.chatgpt-web-plugin",
      "kind": "host",
      "state": "planned",
      "evidence": []
    },
    {
      "id": "host.claude-code",
      "kind": "host",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "host.claude-ai-custom-skill",
      "kind": "host",
      "state": "implemented-not-validated",
      "evidence": []
    },
    {
      "id": "connector.external-workspaces",
      "kind": "connector",
      "state": "out-of-scope",
      "evidence": []
    },
    {
      "id": "evaluation.comparative",
      "kind": "evaluation",
      "state": "implemented-not-validated",
      "evidence": []
    }
  ]
}
```
<!-- strategic-advisor-contract:end -->

## Current interpretation

The repository is pre-release and capability promotion is disabled. The canonical core, selective interactive-strategy contract, decision-relevant personal-context contract, configurable retention policy, eight-file Strategy Workspace, six bounded lenses, comparative-evaluation definitions, deterministic install builder, standalone Agent Skills envelope, skill-only OpenAI local-marketplace envelope, and paid-personal ChatGPT Custom GPT kit are implemented. Exact personal facts may be used and durably retained in an owner-authorised user workspace; they are not copied into this public product repository or its generic packages. Personal context may shape strategy without claiming specialist legal, medical, clinical, or financial authority. The Custom GPT kit mechanically derives its Instructions from canonical `SKILL.md` and supplies the remaining runtime references/templates as Knowledge; it is not a Personal Skill. Existing host observations prove only the exact recorded artifacts and accounts, not strategic effectiveness, general host support, or another host. A public ChatGPT Plugin Directory or GPT Store submission has not been implemented. No passing frozen comparative run or improvement result exists. These artifacts are candidates for early testing and evaluation, not supported capabilities. There is no supported installation, validated domain, or connector.

The runtime package is an explicit allowlist in [`skills/strategic-advisor/runtime-manifest.json`](skills/strategic-advisor/runtime-manifest.json). [`scripts/build_install_artifacts.py`](scripts/build_install_artifacts.py) wraps those exact runtime bytes in deterministic standalone-Skill, OpenAI local-marketplace plugin, and ChatGPT Custom GPT envelopes and identifies the added Apache-2.0 licence separately. The Custom GPT envelope contains generated canonical Instructions and an exact Knowledge projection rather than a hand-maintained prompt fork. Evaluation definitions, expected properties, rubrics, fixtures, and prior results must never enter the model-visible treatment or install package.

## Promotion rule

A capability cannot move to `validated` while `capability_promotion_enabled` is false. Enabling promotion requires a separately reviewed validator transition that verifies the relevant Git revision, tested source and runtime-package identities, gate-specific measurements, and result artifacts rather than trusting a self-authored pass attestation. After that transition, a capability may move to `validated` only when its required current evidence passes the new gate, and its ID must appear in `supported_capabilities`. If evidence goes stale or a hard gate fails, the state and public language must be demoted in the same change.

Repository structure checks are run with [`scripts/validate.py`](scripts/validate.py). Contribution rules are in [CONTRIBUTING.md](CONTRIBUTING.md), and private vulnerability reports belong in the channel described by [SECURITY.md](SECURITY.md).
