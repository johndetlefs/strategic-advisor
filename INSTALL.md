# Install Strategic Advisor

Strategic Advisor is experimental early-access decision support. Start with the
one host you use; a repository, Strategy Workspace, connector, or developer
environment is not required.

## Choose your path

| User and host | File | First action |
| --- | --- | --- |
| John — Codex | `strategic-advisor.zip` | Extract to personal `.agents/skills/` |
| John or Christina — paid personal ChatGPT | `strategic-advisor-chatgpt.zip` | Build a Custom GPT from its Instructions and 19 Knowledge files |
| Christina — Canva Claude Enterprise | `strategic-advisor.zip` | Confirm enterprise Skills settings, then upload unchanged |
| Codex/ChatGPT desktop Work experiment | `strategic-advisor-plugin.zip` | Register the local marketplace bundle |

These paths install the same canonical runtime but do not inherit one another's
activation or behaviour evidence.

## Download the current alpha

Download these four files together from the current
[`v0.2.0-alpha.1` prerelease](https://github.com/johndetlefs/strategic-advisor/releases/tag/v0.2.0-alpha.1):

- `strategic-advisor.zip`
- `strategic-advisor-plugin.zip`
- `strategic-advisor-chatgpt.zip`
- `install-artifacts.json`

The release notes publish the trusted provenance SHA-256 and runtime-package
identity. Verify all files together:

```sh
python3 scripts/build_install_artifacts.py verify \
  --skill-archive strategic-advisor.zip \
  --plugin-archive strategic-advisor-plugin.zip \
  --chatgpt-kit strategic-advisor-chatgpt.zip \
  --provenance install-artifacts.json \
  --expected-provenance-sha256 <FROM_RELEASE_NOTES> \
  --expected-runtime-identity <FROM_RELEASE_NOTES>
```

This proves archive/provenance consistency and equality with the named release
identities. It does not prove account installation, activation, advice quality,
or publisher authenticity if every trusted reference has been replaced.

## John: install in Codex

Extract `strategic-advisor.zip` so the final personal path is:

```text
$HOME/.agents/skills/strategic-advisor/SKILL.md
```

Restart Codex if the Skill does not appear. Start a fresh task outside this
source repository and invoke `$strategic-advisor` explicitly for the first
check.

Project-only installation is also supported:

```text
PROJECT_ROOT/.agents/skills/strategic-advisor/SKILL.md
```

Do not use the development folder under `skills/strategic-advisor/` as an
end-user package; it also contains evaluation authority.

## John and Christina: install in paid personal ChatGPT

Personal paid accounts use a **Custom GPT**. This is not a ChatGPT Personal
Skill; Personal Skills are currently a managed-workspace feature.

1. Extract `strategic-advisor-chatgpt.zip`.
2. On the web, open `https://chatgpt.com/gpts/editor` and create a GPT.
3. Copy all of `INSTRUCTIONS.md` into **Instructions**.
4. Upload all 19 files under `KNOWLEDGE/` as **Knowledge**.
5. Apply `CONFIG.json`: name, description, starters, Web search on, Canvas on,
   Image generation off, Data Analysis off, and no Apps or Actions.
6. Preview the fictional trigger and direct-assistance control below.
7. Save privately first. After the check passes, choose **Share → Anyone with
   the link** when available.

John can send that link to Christina for immediate use. Christina can instead
create an independently owned copy by repeating the same seven steps with the
same verified kit.

Custom GPTs do not use saved memory, custom instructions, or previous
conversations. Keep one coherent decision per chat and restate material current
evidence when starting a new one.

## Christina: install in Canva Claude Enterprise

Before downloading or uploading anything, check:

1. **Organization settings → Skills:** Skills is enabled.
2. **Organization settings → Skills:** Code execution and file creation is
   enabled.

If Christina cannot see those settings or **Customize → Skills**, a Canva Claude
owner must enable them. Do not treat that administrator control as a package
failure.

When enabled:

1. In Claude, open **Customize → Skills**.
2. Select **+ → Create skill → Upload a skill**.
3. Upload `strategic-advisor.zip` unchanged.
4. Enable Strategic Advisor in the Skills list.
5. Open a fresh chat and run the fictional trigger and control below.
6. Confirm Claude shows a visible Skill activation/source event before treating
   the path as activated.

The upload is private to Christina unless her organisation separately permits
sharing. Organisation-wide provisioning is outside this alpha.

## Fictional first-use checks

Material trigger:

> Use Strategic Advisor. A fictional software team completed every milestone,
> but the only outcome measure shows zero active users after six weeks. The
> sponsor wants to scale because the delivery dashboard is green. What is the
> current readiness state and the smallest decisive next move?

Direct-assistance control:

> Summarise this fictional status in one sentence: all milestones are complete
> and active users remain at zero after six weeks.

Expected boundaries:

- The first prompt should invoke Strategic Advisor, distinguish delivery from
  outcome evidence, avoid endorsing scale, and propose a bounded validation
  step.
- The second should answer directly without a strategic ledger, forced
  readiness verdict, or unnecessary ceremony.
- A plausible answer alone is not source proof. Record the host's visible
  activation/source event separately.

Use only fictional data for installation checks.

## Optional local marketplace

`strategic-advisor-plugin.zip` is for Codex and compatible ChatGPT desktop Work
mode local-marketplace experiments. It is not a Personal Skill, Custom GPT, or
public Plugin Directory package.

```sh
codex plugin marketplace add /absolute/path/to/extracted/strategic-advisor-plugin
codex plugin add strategic-advisor@strategic-advisor
codex plugin list --json
```

## Build from a clean checkout

No virtual environment or third-party dependency is required.

```sh
mkdir -p dist
python3 scripts/build_install_artifacts.py build \
  --license LICENSE \
  --skill-archive dist/strategic-advisor.zip \
  --plugin-archive dist/strategic-advisor-plugin.zip \
  --chatgpt-kit dist/strategic-advisor-chatgpt.zip \
  --provenance-out dist/install-artifacts.json
```

The builder refuses a dirty release source and existing output paths. Use
`--allow-dirty` only for explicitly inexact local exploration.

## Current proof boundary

- Deterministic package verification proves selected bytes and archive safety.
- Exact-host evidence proves only the installation/activation actually observed.
- The bounded Codex drift smoke proves only its five recorded public-synthetic
  scenarios on its exact model/runtime/date.
- No current artifact proves cross-host parity, comparative improvement,
  universal drift resistance, supported professional domains, or suitability
  for delegated consequential decisions.

Current official references:

- OpenAI: [Skills in ChatGPT](https://help.openai.com/en/articles/20001066),
  [Creating GPTs](https://help.openai.com/en/articles/8554397-creating-and-editing-gpts),
  and [Build skills](https://learn.chatgpt.com/docs/build-skills)
- Anthropic: [Use Skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
  and [Create custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)

Host eligibility and administrator controls change independently of this
repository. Recheck official documentation when the current UI differs.
