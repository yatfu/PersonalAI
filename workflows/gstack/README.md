# gstack

Foundation for AI-generated full stack applications: turn an application idea into a defined scope, an implementation plan, a working frontend and backend, and a verified local handoff.

## When to run it

When creating a new full stack application from an idea or requirements brief.

## Inputs

- `applicationName` (required) — descriptive name used to derive a camelCase output folder.
- `idea` (required) — intended users, problem, and desired behavior.
- `requirements` (optional) — user journeys, acceptance criteria, and scope constraints.
- `stack` (optional) — preferred frameworks, database, and hosting target. If omitted, the architect chooses and explains a suitable stack.
- `integrations` (optional) — external services and available configuration; credentials stay outside workflow documents.

## Output

`outputs/gstack/<applicationName>/`

- `brief.md` — scope, assumptions, user journeys, and acceptance criteria.
- `architecture.md` — stack, data model, API contracts, and implementation sequence.
- `app/` — application source, dependency manifests, configuration examples, and tests.
- `validation.md` — verification results, unresolved issues, and limitations.
- `handoff.md` — setup, local run commands, and deployment prerequisites.

## Agents

| Agent | Role |
|---|---|
| `agents/productPlanner.md` | Defines a concrete, testable application scope. |
| `agents/architect.md` | Selects the stack and designs the application contracts. |
| `agents/appBuilder.md` | Implements frontend, backend, persistence, and integration points. |
| `agents/appValidator.md` | Checks the implementation against the brief and records evidence. |

See [orchestrator.md](orchestrator.md) for stage order and revision rules.

## Status

Initial workflow specification. No application has been generated or validated with it yet. These files describe execution; they do not provide an automated runner. Deployment is a separate action requiring user authorization.
