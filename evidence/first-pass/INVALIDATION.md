# Initial comparison invalidated

The initial baseline and candidate outputs under `invalid-source/` are retained diagnostic artifacts, not evidence about the frozen runtimes. Raw command events show successful reads from the globally installed Strategic Advisor. The runner falsely credited these because it matched a relative suffix inside an absolute path.

This invalidates all apparent before/after behavioural conclusions from those sessions, including the apparently improved history-intent case. The candidate stopped on FIRST-004; the baseline was explicitly interrupted before completion. No full smoke or release certification followed this failure.

Narrow harness correction: count whole local paths, resolve absolute paths against the frozen package, reject a successful read of another installation, and disable global Strategic Advisor discovery for the target invocation only. Local prompt rendering verified that this CLI version requires the SKILL.md path for per-skill disablement. The routing wrapper identifies the frozen package without adding strategic rules or changing activation criteria. Tests cover relative/absolute candidate reads, global and mixed-installation rejection, failed commands, and permitted synthetic data.

The eight case prompts, criteria, target model, runtime bytes and adjudication policy remain unchanged. A single fresh comparison under the corrected source routing replaces the invalid observations. This is a harness correction, not a product-prompt repair or a regrade of contaminated outputs. If this corrected run cannot establish source identity, stop and report missing behavioural proof.

Historical smoke artifacts have not been re-audited by this task; no claim is made that a historical generic source-access summary repairs this defect. Current claims require the corrected runner and retained actual command events.
