# Install Strategic Advisor

Strategic Advisor is available for **early-access testing**. Installation and strategic effectiveness are different claims: a host may load the package correctly even though the project has not yet passed its comparative behavioural or real-pilot release gates.

Use only a generated install artifact. Do not point an end-user host at the development directory under `skills/strategic-advisor/`; that directory deliberately contains evaluation authority that must remain outside model context.

## Get the artifacts

A distribution contains three files:

- `strategic-advisor.zip` — the standalone Agent Skills archive for Codex, Claude Code, Claude.ai, and ChatGPT surfaces that accept a custom Skill;
- `strategic-advisor-plugin.zip` — a skill-only OpenAI local marketplace and plugin bundle for Codex and ChatGPT desktop Work mode; and
- `install-artifacts.json` — external provenance, entry inventory, runtime-package identity, source revision, and archive hashes.

Download all three files together from the current [`v0.1.0-alpha.1` early-access release](https://github.com/johndetlefs/strategic-advisor/releases/tag/v0.1.0-alpha.1). Keep the provenance document beside both ZIPs.

### Verify the downloaded alpha

Use the consumer-side verifier with the trusted identities for `v0.1.0-alpha.1`:

```sh
python3 scripts/build_install_artifacts.py verify \
  --skill-archive strategic-advisor.zip \
  --plugin-archive strategic-advisor-plugin.zip \
  --provenance install-artifacts.json \
  --expected-provenance-sha256 86a3133b4591f19f13f5ab98e4fa4e886d86d7d92870f42ca28f9b0a253d70ce \
  --expected-runtime-identity 743bcdd018c192a0ba9a4721cad38027587153b04f30689376cd028ae94940ea
```

This checks archive safety, deterministic metadata, package identity, cross-archive runtime-byte equality, consistency with the provenance document, and equality with the named alpha identities. It does not prove source authenticity if an attacker can replace the release page and every trusted reference; download from the named GitHub release and compare its commit and digests through a separately trusted route when that threat matters.

### Build from a checkout

Choose three paths that do not already exist:

```sh
mkdir -p dist
python3 scripts/build_install_artifacts.py build \
  --license LICENSE \
  --skill-archive dist/strategic-advisor.zip \
  --plugin-archive dist/strategic-advisor-plugin.zip \
  --provenance-out dist/install-artifacts.json
```

For a Git checkout, the builder also refuses a dirty source tree so the recorded revision cannot silently describe different bytes. `--allow-dirty` exists only for local exploration and marks the revision as inexact; never publish that output. The builder intentionally refuses to overwrite any destination.

Verify a local build for structural and internal consistency without pinning it to the alpha identities:

```sh
python3 scripts/build_install_artifacts.py verify \
  --skill-archive dist/strategic-advisor.zip \
  --plugin-archive dist/strategic-advisor-plugin.zip \
  --provenance dist/install-artifacts.json
```

That command does not assert that the local build is the published alpha. If you intend to distribute a later revision, establish and publish new trusted provenance and runtime identities for that revision.

## Codex

### Project installation

Extract `strategic-advisor.zip` under a project's `.agents/skills/` directory. The resulting path must be:

```text
PROJECT_ROOT/.agents/skills/strategic-advisor/SKILL.md
```

Start a fresh Codex task in that project and invoke `$strategic-advisor` explicitly for the first check. A natural strategic request may trigger it automatically, but automatic routing is a separate test.

### Personal installation

Extract the same archive under `$HOME/.agents/skills/`, producing:

```text
$HOME/.agents/skills/strategic-advisor/SKILL.md
```

This makes the Skill discoverable across Codex projects for that user. Use the generated package, not a copy of the source development directory.

### Local marketplace/plugin installation

Extract `strategic-advisor-plugin.zip` to a stable directory, then register that extracted directory as a local marketplace and install the plugin:

```sh
codex plugin marketplace add /absolute/path/to/extracted/strategic-advisor-plugin
codex plugin add strategic-advisor@strategic-advisor
codex plugin list --json
```

The plugin contains the same runtime files as the standalone archive. Marketplace registration proves only that Codex accepts the plugin envelope; perform the fresh-task activation smoke test below as well.

## Claude Code

Extract `strategic-advisor.zip` at either documented Claude Code scope:

```text
# Personal
$HOME/.claude/skills/strategic-advisor/SKILL.md

# Project
PROJECT_ROOT/.claude/skills/strategic-advisor/SKILL.md
```

Start or restart Claude Code, then invoke `/strategic-advisor` explicitly. Claude Code and Claude.ai do not share personal Skill installations, so install each surface separately when both are needed.

## Claude.ai

Use `strategic-advisor.zip` unchanged. In Claude, open **Customize → Skills → + → Create skill → Upload a skill**, upload the ZIP, enable it, and open a fresh chat. Custom Skills require code execution and can be subject to organisation-level controls.

Ask Claude to use the Strategic Advisor skill explicitly for the first check. Confirm the visible skill-activation event. A successful upload without activation is not sufficient evidence that the response used the package.

## ChatGPT

Personal Skills are currently generally available to ChatGPT Business, Enterprise, Healthcare, and Edu users, subject to workspace permissions. Availability on an individual personal plan must be checked in the current UI.

If ChatGPT exposes **Plugins → Skills**, open the Skills page, select **Create → Upload**, and upload `strategic-advisor.zip` unchanged. ChatGPT scans uploaded Skills before they become available.

`strategic-advisor-plugin.zip` is **not** a direct ChatGPT Skill upload or public Plugin Directory submission artifact. It is the documented local-marketplace shape used by Codex and by ChatGPT desktop Work mode, but ChatGPT activation remains unverified in this release.

For the local-plugin experiment, extract `strategic-advisor-plugin.zip` to a stable directory, register that directory with `codex plugin marketplace add`, restart the ChatGPT desktop app, switch to Work mode, open the Plugins Directory, choose the Strategic Advisor marketplace source, and install the plugin. This route depends on the current desktop app, Work mode, and any workspace controls; a marketplace listing without fresh-chat activation is not proof of use.

ChatGPT Personal Skill installations on the desktop app and on web/mobile are separate and do not currently sync. Install and verify the surface that will actually be used.

If the Skills UI is absent or uploading is disabled, direct ChatGPT installation is not currently available on that account. Do not replace it by pasting the strategic instructions into a custom prompt. After a successful Skill upload, enable it and use a fresh chat for the activation check. A Codex result does not validate ChatGPT, and a ChatGPT upload receipt does not establish Claude compatibility.

## Fresh-context activation smoke test

Use only a fictional case for the first check. Ask the host:

> Use the Strategic Advisor skill. State the selected engagement mode and lens, list the exact Strategic Advisor reference paths loaded, and give the four readiness-state labels exactly as defined by the installed source. Then assess this fictional case: a team completed every milestone, but the only outcome measure shows zero active users after six weeks; the sponsor wants to scale because the delivery dashboard is green.

Record:

- host, host version, model, plan/workspace, and relevant capability settings;
- archive SHA-256 and runtime-package identity;
- whether the package appeared in the installed-skill list;
- explicit activation and the host's visible activation event or source-access trace;
- the loaded reference paths and source-bound response; and
- any error or unavailable prerequisite.

Treat the model's answer alone as a smoke-test result, not proof. Discovery and activation are proven only when an independently observable host event or source-access trace is tied to the installed archive identity. Even then, the result does not prove superior advice, cross-host parity, or suitability for consequential use.

## How to use it day to day

The Skill supplies the method; the host task or chat holds the current conversation context. Use one task/chat per substantive decision or coherent update cycle. Keep durable claims, evidence, decisions, falsifiers, and review dates in a private decision record rather than relying on an indefinitely growing conversation.

Repository, Slack, Teams, email, calendar, and document connectors are optional evidence-access channels, not required installation components. Grant the minimum relevant access. Connector visibility does not make data complete, true, current, authorised for disclosure, or sufficient for a decision.

Until the published release gates pass, treat recommendations as experimental decision support: inspect the claim ledger, challenge assumptions, and retain human authority over consequential action.

## Current host references

- OpenAI: [Build skills](https://learn.chatgpt.com/docs/build-skills), [Build plugins](https://learn.chatgpt.com/docs/build-plugins), and [Skills in ChatGPT](https://help.openai.com/en/articles/20001066)
- Anthropic: [Use Skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude), [Create custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills), and [Claude Code Skills](https://code.claude.com/docs/en/slash-commands)

Host interfaces, plan eligibility, and administrative controls change independently of this repository. Recheck the relevant official documentation when an installation path is unavailable or materially changed.
