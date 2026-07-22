# Project Workflow Guidance

Use this file for repo-specific workflow guidance that should survive project-workflow init refreshes.

- Keep stable product outcomes in `.project-workflow/CONSTITUTION.md` and approved scope in the relevant task or epic requirements.
- `.agents/skills/project-*` and `.project-workflow/` are development-process tooling. The distributable product lives under `skills/strategic-advisor/`; never present workflow skills as product capabilities.
- `skills/strategic-advisor/` is the single source of strategic logic. Host adapters may package or point to it but must not copy its instructions.
- Preserve the epistemic status and provenance of material claims in requirements, implementation notes, reviews, evaluations, and release documentation.
- Proof must target the exact claim. Documentation proves documented intent; static validation proves structure; behavioural evaluation proves observed model behaviour; neither is a substitute for the other.
- Freeze comparative evaluation cases, rubric, thresholds, model identity, and context controls before viewing treatment results. Retain raw outputs and hard-gate verdicts.
- Use only synthetic, public, or irreversibly sanitised examples. Never commit employer, client, household, connector, credential, or other private case data.
- Do not mark a domain, host, connector, or release ready based on placeholder files, happy-path examples, aggregate scores, or model self-assessment.
- Add dependencies and automation only when they enforce an approved invariant or proof obligation. Prefer portable Markdown and small transparent validators.
- Use `./.project-workflow/cli/workflow doctor` after workflow-state changes. Record exact validation commands and artifacts in child evidence before review.
