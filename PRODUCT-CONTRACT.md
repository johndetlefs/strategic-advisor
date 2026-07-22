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
  "capability_promotion_enabled": false,
  "canonical_product_path": "skills/strategic-advisor/",
  "supported_installation_available": false,
  "runtime_package_manifest": "skills/strategic-advisor/runtime-manifest.json",
  "supported_capabilities": [],
  "capabilities": [
    {
      "id": "core.reality-protocol",
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
      "state": "out-of-scope",
      "evidence": []
    },
    {
      "id": "domain.marketing-growth",
      "kind": "domain",
      "state": "out-of-scope",
      "evidence": []
    },
    {
      "id": "domain.personal-relationships",
      "kind": "domain",
      "state": "out-of-scope",
      "evidence": []
    },
    {
      "id": "domain.family-household",
      "kind": "domain",
      "state": "out-of-scope",
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
      "id": "host.chatgpt-web-plugin",
      "kind": "host",
      "state": "out-of-scope",
      "evidence": []
    },
    {
      "id": "host.claude",
      "kind": "host",
      "state": "out-of-scope",
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

The repository is pre-release and capability promotion is disabled. The canonical core, four v0 professional lenses, Codex-oriented local authoring metadata, and comparative-evaluation definitions are implemented but not behaviourally or host validated. No frozen comparative run or improvement result exists. These artifacts are candidates for evaluation, not supported capabilities. There is no supported installation, validated domain, connector, ChatGPT web plugin, or Claude path.

The runtime package is an explicit allowlist in [`skills/strategic-advisor/runtime-manifest.json`](skills/strategic-advisor/runtime-manifest.json). Evaluation definitions, expected properties, rubrics, fixtures, and prior results must never enter the model-visible treatment package.

## Promotion rule

A capability cannot move to `validated` while `capability_promotion_enabled` is false. Enabling promotion requires a separately reviewed validator transition that verifies the relevant Git revision, tested source and runtime-package identities, gate-specific measurements, and result artifacts rather than trusting a self-authored pass attestation. After that transition, a capability may move to `validated` only when its required current evidence passes the new gate, and its ID must appear in `supported_capabilities`. If evidence goes stale or a hard gate fails, the state and public language must be demoted in the same change.

Repository structure checks are run with [`scripts/validate.py`](scripts/validate.py). Contribution rules are in [CONTRIBUTING.md](CONTRIBUTING.md), and private vulnerability reports belong in the channel described by [SECURITY.md](SECURITY.md).
