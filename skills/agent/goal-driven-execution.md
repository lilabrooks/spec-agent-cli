---
source: https://github.com/multica-ai/andrej-karpathy-skills
---
# Goal-driven execution

## Purpose
Convert a CLI spec into verifiable implementation goals so the agent can work until the feature is done.

## When to use
Use this for multi-step CLI work, bug fixes, validation rules, and any change that needs tests.

## Rules
- Define success criteria before implementation.
- Turn vague requests into observable behavior, such as stdout, stderr, exit code, files written, or tests passing.
- Work in small steps where each step has a verification check.
- Reproduce a bug with a test before fixing it when enough context exists.
- Keep looping until the agreed checks pass or a real blocker appears.

## Verification
- The implementation includes tests for the behavior in the spec.
- The final response reports which checks passed.
- Any skipped check has a concrete reason.

