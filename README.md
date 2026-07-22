# Strategic Advisor

Strategic Advisor is an experimental Agent Skill for reality-tested strategy under uncertainty. The project is designed to help a capable model distinguish what is known from what is merely reported, inferred, preferred, forecast, or unknown before recommending action.

> **Current status: pre-release.** The canonical skill and initial professional lenses are implemented but have not yet passed the project's behavioural evaluation and release gates. No domain, host, connector, or installation path is currently supported.

The public capability authority is [PRODUCT-CONTRACT.md](PRODUCT-CONTRACT.md). If this README and that contract ever disagree, treat the more conservative claim as current and report the drift.

The design is one canonical reality protocol plus selectively loaded professional lenses, with thin host links and a separate evaluation plane. See [ARCHITECTURE.md](ARCHITECTURE.md) for the rationale and boundaries.

## Current capability summary

| Field | Current state |
| --- | --- |
| Maturity | Pre-release |
| Canonical product | [`skills/strategic-advisor/`](skills/strategic-advisor/) |
| Supported installation | None |
| Validated domains | None |
| Supported connectors | None |
| v0 candidates, implemented but not validated | Project/product, career, organisational influence, people leadership |
| Evaluation | Definitions and protocol exist; no frozen comparative run, result, or release verdict |
| Outside the current v0 | Business/venture, marketing/growth, personal relationships, family/household, legal, medical/clinical, financial |

“Implemented but not validated” means reviewable source exists and structural checks can inspect it. It does not mean the model behaves as intended, improves decisions, or works in a particular host. The current evaluation definitions are likewise not evidence that an evaluation ran or passed.

## Host and installation boundary

- **Codex:** the repository includes a relative repo-local symlink at `.agents/skills/strategic-advisor` pointing to the canonical source for authoring discovery. It is not a released Codex plugin or a validated installation; no fresh-context host invocation has yet established supported behaviour.
- **ChatGPT web:** plugin packaging and installation are deferred. This repository does not provide a ChatGPT web plugin.
- **Claude or Claude Code:** no Claude-specific adapter or installation path has been tested. Similarity to an Agent Skills directory layout is not compatibility evidence.
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
