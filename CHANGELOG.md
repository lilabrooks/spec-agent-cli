# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-07-02

### Added

- `anthropic` provider adapter backed by the Claude Messages API (default model `claude-opus-4-8`), installed via the `anthropic` optional extra.
- `openai` provider adapter backed by the Chat Completions API (default model `gpt-4o-mini`), installed via the `openai` optional extra. Both adapters defer their SDK import to `complete()`, so the CLI keeps working with neither extra installed.
- `AGENT_CLI_MODEL` environment variable to override which model the active provider adapter calls.
- `agent build` command: runs the same spec/skill-aware prompt as `agent run` with the `file-output-contract` skill always attached, parses `FILE:` blocks from the reply (`core/fileset.py`), prints the write plan by default, writes files with `--apply`, and refuses to overwrite existing files unless `--force` is given. Generated paths are rejected if absolute or containing `..`.
- `--strict` flag on `agent build` to fail before the model call when the attached spec has validation errors; the default warns on stderr and continues.
- `skills/agent/file-output-contract.md` documenting the `FILE:` reply format the build parser consumes.

## [0.2.0] - 2026-07-02

### Added

- Default specs and skills are bundled inside the package, so `agent spec` and `agent skill` work from any directory after a pipx or pip install. A `specs/cli` or `skills/agent` folder in the working directory still takes precedence.
- `resources.py` resolves the active spec and skill roots: the working directory first, the bundled defaults as a fallback.
- `providers/registry.py` as the single source of truth for provider adapters. The factory, the unknown-provider error, and the `providers` command all read from it.
- Warning on stderr when `agent run --all-skills` finds no skills, instead of silently doing nothing.
- `Makefile` with `make check` (active interpreter) and `make check-all` (every supported Python via uv), plus `lint`, `format`, `typecheck`, `test`, and `coverage` targets.
- Configuration section in the README documenting `AGENT_CLI_PROVIDER` and `AGENT_CLI_SYSTEM_PROMPT` with usage examples.
- Tests covering the provider registry, spec and skill root resolution, the empty-skills warning, and the echo adapter ignoring the system prompt.

### Changed

- Provider selection is driven by the registry rather than a hardcoded `match` statement.
- Coverage enforces a 70% floor (`fail_under = 70`).
- CI runs against Python 3.12, 3.13, and 3.14.
- README reorganized: a dedicated Configuration section, the Flow diagram moved up, and duplicated check commands removed.
- `docs/architecture.md` points provider registration at `providers/registry.py`.

### Removed

- `.env.example`, which implied a `.env` auto-loading the project does not perform. The environment variables are documented in the README instead.

### Fixed

- Spec and skill commands failing when the CLI was installed and run outside a repo checkout. They relied on working-directory-relative paths that were not shipped in the package.
