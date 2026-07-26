# Strategic Advisor

Strategic Advisor is an experimental Agent Skill for reality-tested strategy under uncertainty. The project is designed to help a capable model distinguish what is known from what is merely reported, inferred, preferred, forecast, or unknown before recommending action.

> **Current status: pre-release.** The canonical skill, selective conversation, personal-context and continuity contract, six decision lenses, deterministic cross-host packages, and bounded Codex smoke evidence exist. The project has not passed its comparative or real-pilot release gates. Alpha artifacts are experimental test candidates, not supported releases; exact host installation and activation are recorded separately.

The public capability authority is [PRODUCT-CONTRACT.md](PRODUCT-CONTRACT.md). If this README and that contract ever disagree, treat the more conservative claim as current and report the drift.

The design is one canonical reality protocol, an owner-controlled personal-context layer, and selectively loaded lenses, with thin host links and a separate evaluation plane. See [ARCHITECTURE.md](ARCHITECTURE.md) for the rationale and boundaries.

## Current capability summary

| Field | Current state |
| --- | --- |
| Maturity | Pre-release |
| Early-access distribution | [`v0.2.0-alpha.2` GitHub prerelease](https://github.com/johndetlefs/strategic-advisor/releases/tag/v0.2.0-alpha.2) |
| Canonical product | [`skills/strategic-advisor/`](skills/strategic-advisor/) |
| Supported installation | None |
| Early-access installation | Deterministic standalone Skill, OpenAI local-marketplace plugin, and paid-personal ChatGPT Custom GPT kit; see [INSTALL.md](INSTALL.md) |
| Validated domains | None |
| Supported connectors | None |
| Alpha candidates, implemented but not validated | Selective interactive strategy; open-field and portfolio-bounded exploration; exact personal context; configurable durable continuity; project/product, career, organisational influence, people leadership, business/venture, marketing/growth |
| Evaluation | Bounded seven-scenario Codex drift smoke passed; no passing comparative run, improvement result, independent human validation, or release verdict |
| Specialist boundary | Personal context may shape strategy; the product does not replace legal, medical, clinical, financial, or other qualified professional judgment |

“Implemented but not validated” means reviewable source exists and structural checks can inspect it. It does not mean the model behaves as intended, improves decisions, or works in a particular host. The current evaluation definitions are likewise not evidence that an evaluation ran or passed.

No domain, host, connector, or installation path is currently supported.

## Install for first use

Use the generated files described in [INSTALL.md](INSTALL.md):

- **Codex:** install `strategic-advisor.zip` at personal or project Skill scope.
- **Paid personal ChatGPT:** build or use a Custom GPT from `strategic-advisor-chatgpt.zip`.
- **Claude Enterprise:** upload `strategic-advisor.zip` unchanged after the organisation enables Skills plus code execution and file creation.

No repository, Strategy Workspace, connector, database, or virtual environment is required for session-only use. The optional Strategy Workspace provides portable, owner-controlled durable continuity when the user wants it.

### Progressive onboarding

1. **Start with one material decision.** Install the current artifact for your
   host, invoke Strategic Advisor explicitly, and provide the exact current
   facts and constraints that could change the decision. No repository or
   Strategy Workspace is required.
2. **Add continuity only when it earns its place.** If recurring context or
   prior decisions would materially improve later work, create or name an
   owner-controlled Strategy Workspace and authorise the minimum relevant read
   for that decision.

Workspace or repository presence never invokes Strategic Advisor by itself and
grants no read, write, disclosure, integration, external-action, or
cross-workspace authority. The retention mode controls persistence; each other
authority remains separate. See the [optional workspace contract](#optional-strategy-workspace-contract).

Package compatibility, successful host activation, behavioural smoke results, comparative improvement, and useful real-world outcomes are separate claims. The product remains pre-release and unsupported until the relevant gates are promoted with current structured evidence.

### Exact current host status

| Host | Package | Account result |
| --- | --- | --- |
| Owner personal Codex | Exact `v0.2.0-alpha.1` standalone ZIP | Installed; fresh source-bound fictional smoke passed |
| Owner paid personal ChatGPT | Exact Custom GPT kit | Live by link; Knowledge upload and both Preview checks passed |
| Separate paid personal ChatGPT account | [Early-access Strategic Advisor GPT](https://chatgpt.com/g/g-6a632c0422688191b32d51fa147e441c-strategic-advisor) or the same kit | Shared path ready; separate-account open not yet observed |
| Managed Claude Enterprise account | Exact standalone ZIP | Package and preflight ready; private account upload/activation not run |

The bounded, non-private record is
[`evidence/hosts/v0.2.0-alpha.1/host-status.json`](evidence/hosts/v0.2.0-alpha.1/host-status.json).
It is an execution ledger, not a supported-capability registry.

## Host and installation boundary

- **Codex:** the repository's relative symlink at `.agents/skills/strategic-advisor` is for authoring only. The generated standalone and local-marketplace artifacts provide the end-user boundary. One exact current personal-install activation passed on the recorded CLI/model/date; that does not promote general Codex support.
- **ChatGPT:** managed plans can expose Personal Skills, but paid personal accounts use the deterministic Custom GPT kit. Its Instructions are generated from canonical `SKILL.md`; its Knowledge files are the exact remaining runtime resources. The plugin ZIP is not a Personal Skill, Custom GPT, or public Plugin Directory submission.
- **Claude or Claude Code:** the unchanged standalone archive follows the current custom-Skill shape. Claude Enterprise requires organisation-enabled Skills and code execution/file creation. Package readiness is not live Claude activation.
- **Connectors:** no Slack, Teams, repository, email, calendar, document-store, or other connector is shipped. Connecting a data source would not by itself make its contents complete, true, relevant, or authorised.

Do not copy the advisor instructions into host-specific prompts. The only canonical strategic logic belongs under [`skills/strategic-advisor/`](skills/strategic-advisor/).

## Optional Strategy Workspace contract

Strategic Advisor remains usable without a repository or workspace. The runtime includes an experimental, portable eight-file Markdown scaffold for exact, owner-approved personal context and continuity. The workspace defaults to preserving decision-relevant specificity. Stored records remain input rather than authority, and workspace presence grants no automatic invocation, read, write, disclosure, integration, or cross-workspace permission. This structural contract is implemented but has not been validated as a host capability.

Build a new blank scaffold only:

```sh
python3 scripts/strategy_workspace.py build --destination /path/to/new-workspace
```

Validate an explicitly named workspace against an explicit freshness date:

```sh
python3 scripts/strategy_workspace.py validate \
  --workspace /path/to/workspace \
  --as-of YYYY-MM-DD
```

Copy a legacy five-file workspace into the eight-file contract without changing
the source:

```sh
python3 scripts/strategy_workspace.py migrate \
  --source /path/to/legacy-workspace \
  --destination /path/to/new-workspace
```

The builder refuses existing destinations. The validator fails on structural or safety violations and returns `valid_with_attention` when synthetic or owner-provided records are stale or declare conflicts; it never resolves or upgrades those records. See the canonical [workspace contract](skills/strategic-advisor/references/strategy-workspace.md).

## Control the option search

The advisor normally infers how widely to search. A broad outcome with no established route defaults to comparing the strongest current-portfolio path with credible outside paths. A clearly project-specific question stays with that project unless a wider constraint would materially change the answer.

You can override this in ordinary language:

- “Use current projects only.”
- “Take a clean slate.”
- “Compare both.”

“Clean slate” excludes current projects from the candidate set; it does not discard authorised personal context, objectives, evidence, or constraints. The advisor states the inferred boundary only when it materially changes the analysis and asks a clarifying question only when the alternatives would lead to consequentially different advice and no responsible default exists.

## Repository validation

The deterministic validation boundary uses Python's standard library, makes no model or network calls, and requires no credentials:

```sh
python3 scripts/build_evals.py --check
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

Run one scope with `python3 scripts/validate.py --scope <scope>`.

`build_evals.py --check` proves that the committed executable inventory is the deterministic import of the normative core and original four-lens inventories. The newer interactive, business, and marketing source is packaged for alpha testing but is not covered by a passing comparative run. `build_runtime_package.py` can construct a content-addressed, allowlisted package; its existence and unit tests do not constitute a host installation or behavioural result.

`build_install_artifacts.py` wraps those allowlisted runtime bytes in deterministic standalone-Skill, OpenAI local-marketplace, and ChatGPT Custom GPT ZIPs with shared external provenance. Repeated-build and adversarial unit tests prove the archive contract; [INSTALL.md](INSTALL.md) explains the host-specific early-access steps.

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
