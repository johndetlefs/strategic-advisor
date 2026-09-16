<!-- project-workflow:generated -->

# Project Workflow Claude Code execution control

This package-owned plugin is loaded ephemerally by `project execute`. Its hooks are subordinate to
one sealed Project Workflow execution envelope. Package presence alone does not prove that hooks are
enabled, permitted by managed policy, or active in a real Claude Code dispatch.

`project execute` first runs a model-free SessionStart activation preflight. The material invocation
then uses native `dontAsk` permission rules for sealed file paths and exact commands, with the hooks
providing aggregate accounting and sticky interruption. SessionStart adds context; PreToolUse can
deny before execution; post-tool hooks detect resulting state; PostToolBatch can stop the loop before
another model call. Hook failure never grants broader native tool, command, or path authority.
