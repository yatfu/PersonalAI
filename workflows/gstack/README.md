# gstack

Define, build, and validate full stack applications and features through a shared set of agent roles and skills.

## When to run it

Use this workflow to create a new application or change an existing one.

See [promptTemplate.md](promptTemplate.md) for short and expanded prompts covering feature requests of different sizes, including changes to existing applications.

## Inputs

- `applicationName` — descriptive name used for the camelCase output folder. For an existing application, derive it from the project when the request does not supply one.
- `idea` (required) — application idea or feature request: users, problem, and desired behavior.
- `applicationPath` — source directory for an existing application; required when modifying one. For a new application, source defaults to `outputs/gstack/<applicationName>/app/`.
- `requirements` (optional) — user journeys, acceptance criteria, and scope constraints.
- `stack` (optional) — preferred frameworks, database, and hosting target. If omitted, the architect chooses and explains a suitable stack.
- `integrations` (optional) — external services and available configuration; credentials stay outside workflow documents.

## Output

Planning documents and reports live in `outputs/gstack/<applicationName>/`. Source lives at `applicationPath` when supplied, otherwise in that folder's `app/` directory. Record both locations in `brief.md` and `handoff.md`. For an existing application, inspect its instructions and implementation first; preserve its stack and behavior unless the request requires a change.

- `brief.md` — scope, assumptions, user journeys, and acceptance criteria.
- `architecture.md` — stack, application structure, and implementation sequence.
- `contracts.md` — precise data, interface, permission, error, and UI behavior linked to acceptance criteria; see [contractTemplate.md](contractTemplate.md).
- `increments.md` — ordered work with exactly one goal per increment, dependencies, checks, and progress; see [incrementTemplate.md](incrementTemplate.md).
- Application source — code, dependency manifests, configuration examples, and tests at the selected source directory.
- `validation.md` — validation after every increment, correction attempts, and the final application verdict.
- `handoff.md` — setup, local run commands, and deployment prerequisites.

## Agents

| Agent | Role |
|---|---|
| `agents/planner.md` | Defines a concrete, testable application scope. |
| `agents/architect.md` | Selects the stack and designs the application contracts. |
| `agents/builder.md` | Implements frontend, backend, persistence, and integration points. |
| `agents/validator.md` | Checks the implementation against the brief and records evidence. |

See [orchestrator.md](orchestrator.md) for stage order and revision rules.

## Shared skills

Reusable procedures live in [skills/](skills/README.md), separate from agent roles. All agents can use every skill; their role files list usual skills and retain ownership of assigned outputs. Repository discovery links under `.agents/skills/` make this library available to Codex without duplicate definitions. Skill folders use lowercase hyphenated names required by the skill format. Skills are instructions, not an automated runner.

## Incremental execution

Build one goal, validate it, then advance only after it passes. A feature, component, or connection between components can each be an increment. Integration work counts explicitly, and complete user journeys are checked again during final validation.

## Status

Initial workflow specification. No application has been generated or validated with it yet. These files describe execution; they do not provide an automated runner. Deployment is a separate action requiring user authorization.
