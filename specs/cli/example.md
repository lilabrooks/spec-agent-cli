---
status: draft
owner: product
deciders: [Lila Brooks]
---
# Example greeting command

## Purpose
Add a small greeting command that proves the spec-to-implementation loop works.

## Commands
- `agent greet NAME`

## Inputs
- `NAME`: required positional argument.

## Outputs
- Prints `Hello, NAME`.
- Returns exit code `0`.

## Behavior
The command should preserve the exact name passed by the user.

## Acceptance tests
- Given `agent greet Lila`, stdout is `Hello, Lila`.
- Given `agent greet "Python CLI"`, stdout is `Hello, Python CLI`.

