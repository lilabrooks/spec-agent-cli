---
status: draft
owner: product
---
# Host machine details command

## Purpose
Add a command that prints non-sensitive details about the host machine running the CLI.

## Commands
- `agent host --basic`
- `agent host --detailed`

## Inputs
- `--basic`: print a small host summary.
- `--detailed`: print the host summary plus OS/runtime details.
- Exactly one mode flag must be provided.

## Outputs
Basic output includes:

- `hostname`
- `system`
- `machine`

Detailed output includes all basic fields plus:

- `release`
- `version`
- `platform`
- `processor`
- `python_version`

## Behavior
The command should only print non-sensitive local machine details. It must not print environment variables, usernames, home directories, IP addresses, tokens, or shell history.

The output format is one `key: value` pair per line. Keys use lowercase snake case.

## Acceptance tests
- Given `agent host --basic`, stdout includes `hostname`, `system`, and `machine`.
- Given `agent host --basic`, stdout does not include `python_version`.
- Given `agent host --detailed`, stdout includes `hostname`, `system`, `machine`, `platform`, and `python_version`.
- Given no mode flag, the CLI returns a parser error.
- Given both mode flags, the CLI returns a parser error.

