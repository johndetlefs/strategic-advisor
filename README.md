# Strategic Advisor

Strategic Advisor is an experimental Agent Skill for reality-tested strategy under uncertainty. The project is designed to help a capable model distinguish what is known from what is merely reported, inferred, preferred, forecast, or unknown before recommending action.

> **Current status: pre-release.** The canonical skill and initial professional lenses are implemented but have not yet passed the project's behavioural evaluation and release gates. A deterministic early-access artifact builder exists, and any published alpha artifacts are experimental test candidates rather than supported releases. No domain, host, connector, or installation path is currently supported.

The public capability authority is [PRODUCT-CONTRACT.md](PRODUCT-CONTRACT.md). If this README and that contract ever disagree, treat the more conservative claim as current and report the drift.

The design is one canonical reality protocol plus selectively loaded professional lenses, with thin host links and a separate evaluation plane. See [ARCHITECTURE.md](ARCHITECTURE.md) for the rationale and boundaries.

## Current capability summary

| Field | Current state |
| --- | --- |
| Maturity | Pre-release |
| Early-access distribution | [`v0.1.0-alpha.1` GitHub prerelease](https://github.com/johndetlefs/strategic-advisor/releases/tag/v0.1.0-alpha.1) |
| Canonical product | [`skills/strategic-advisor/`](skills/strategic-advisor/) |
| Supported installation | None |
| Early-access installation | Deterministic standalone Skill and OpenAI local-marketplace plugin builders; see [INSTALL.md](INSTALL.md) |
| Validated domains | None |
| Supported connectors | None |
| v0 candidates, implemented but not validated | Project/product, career, organisational influence, people leadership |
| Evaluation | Definitions and protocol exist; no frozen comparative run, result, or release verdict |
| Outside the current v0 | Business/venture, marketing/growth, personal relationships, family/household, legal, medical/clinical, financial |

“Implemented but not validated” means reviewable source exists and structural checks can inspect it. It does not mean the model behaves as intended, improves decisions, or works in a particular host. The current evaluation definitions are likewise not evidence that an evaluation ran or passed.

## Early-access installation

Build or install only the generated allowlisted artifacts described in [INSTALL.md](INSTALL.md). The standalone ZIP is intended for compatible Codex, Claude Code, Claude.ai, and eligible ChatGPT Personal Skill surfaces. The plugin ZIP is a skill-only OpenAI local-marketplace envelope for Codex and ChatGPT desktop Work mode. It is not a Personal Skill upload or public Plugin Directory submission package. Both contain the same runtime skill bytes and exclude the evaluation plane.

Artifact compatibility, successful host activation, comparative behavioural improvement, and useful real-world outcomes are separate claims. A retained exact-release-package Codex activation check exists; Claude and ChatGPT activation remain unverified. The product remains pre-release and unsupported until the relevant host and behavioural gates are promoted with current structured evidence.

## Host and installation boundary

- **Codex:** the repository's relative symlink at `.agents/skills/strategic-advisor` is for authoring only. The generated standalone and local-marketplace artifacts provide the end-user boundary. A fresh isolated Codex task loaded the exact released standalone package and produced a retained source-access trace; this proves that one activation path, not strategic effectiveness or general support.
- **ChatGPT:** the standalone archive is structurally prepared for eligible Personal Skills upload. The OpenAI local-marketplace archive is also structurally prepared for ChatGPT desktop Work mode. Personal Skills are currently generally available on managed ChatGPT plans, subject to workspace controls; live upload/installation and activation remain unverified on both routes. The plugin ZIP is not a direct Skill upload or public Plugin Directory submission.
- **Claude or Claude Code:** the standalone archive follows the current custom-Skill shape. Claude Code is not installed on the maintainer's current test machine and no authorised Claude.ai upload has yet been retained, so both paths remain experimental.
- **Connectors:** no Slack, Teams, repository, email, calendar, document-store, or other connector is shipped. Connecting a data source would not by itself make its contents complete, true, relevant, or authorised.

Do not copy the advisor instructions into host-specific prompts. The only canonical strategic logic belongs under [`skills/strategic-advisor/`](skills/strategic-advisor/).

## Repository validation

The deterministic validation boundary uses Python's standard library, makes no model or network calls, and requires no credentials:

```sh
python3 scripts/build_evals.py --check
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Run one scope with `python3 scripts/validate.py --scope <scope>`.

`build_evals.py --check` proves that the committed 31-case executable inventory is the deterministic import of the normative core and lens inventories. `build_runtime_package.py` can construct a content-addressed, allowlisted package for a future frozen run; its existence and unit tests do not constitute a host installation or behavioural result.

`build_install_artifacts.py` wraps those allowlisted runtime bytes in deterministic standalone-Skill and OpenAI local-marketplace ZIPs and writes external provenance. Repeated-build and adversarial unit tests prove the archive contract; [INSTALL.md](INSTALL.md) explains the host-specific early-access steps.

`evaluation_harness.py` is the deterministic freeze/run verifier. It makes no model calls: it freezes and rechecks the exact authority/runtime/context identity, emits the complete matched work plan, and rejects incomplete, contaminated, non-inverted, or source-mismatched retained artifacts. It can establish a failed release gate from confirmed hard-gate or leakage evidence, but it deliberately cannot emit a passing effectiveness verdict until the still-pending aggregation, assertion, trigger, holdout, and human-review requirements exist.

| Scope | What it proves | What it does not prove |
| --- | --- | --- |
| `skill` | Canonical location, basic Agent Skill structure, required resources, and runtime allowlist integrity | Model behaviour or host loading |
| `lenses` | Required v0 lens files and their contract headings exist | Lens usefulness or correct application |
| `evals` | Committed JSON is parseable, synthetic-labelled where applicable, complete against declared probe coverage, current against its source inventories, and excluded from the runtime package | That behavioural evaluations ran or passed |
| `pilots` | Pilot registry, schemas, accounting fields, and public-record template satisfy the committed structural contract | Consent, privacy in an external run, owner usefulness, or pilot completion |
| `privacy` | Bounded synthetic sentinel and credential patterns were not found | Absence of all sensitive or proprietary information |
| `claims` | Public artifacts and structured capability claims obey the support rule | General truth of unstructured prose |
| `links` | Internal links in public and product Markdown resolve | External link availability |

See [CONTRIBUTING.md](CONTRIBUTING.md) before proposing changes and [SECURITY.md](SECURITY.md) for private vulnerability reporting. The project is licensed under [Apache License 2.0](LICENSE).

## Limits

This is decision support, not delegated authority or professional legal, medical, clinical, or financial advice. Static checks are guardrails, not behavioural evidence. Behavioural claims require retained adversarial and comparative evaluation evidence; release claims additionally require clean-checkout and current CI proof.
