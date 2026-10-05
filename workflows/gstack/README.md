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

## Default technologies

| Area | Default |
|---|---|
| Styling | Tailwind CSS; use v4 for new compatible applications. |
| UI design | Shared [gstack-ui](skills/gstack-ui/SKILL.md) skill with concrete utility classes and semantic theme tokens. |
| Frontend framework and language | Architect selects for the application; no fixed framework or language default. |
| Backend, database, and authentication | Architect selects according to requirements; no fixed defaults. |
| Testing and deployment | Architect selects suitable tools and documents the setup; no fixed tools or hosting provider. |

Explicit user choices override these defaults. For an existing application, preserve its styling system and versions unless a migration is requested. Record the selected technologies and versions in `architecture.md`; Tailwind is the default styling approach, not a requirement to change an existing app's stack.

## Output

Planning documents and reports live in `outputs/gstack/<applicationName>/`. Source lives at `applicationPath` when supplied, otherwise in that folder's `app/` directory. Record both locations in `brief.md` and `handoff.md`. For an existing application, inspect its instructions and implementation first; preserve its stack and behavior unless the request requires a change.

- `brief.md` — scope, assumptions, user journeys, and acceptance criteria explicitly created by planner; see [acceptanceTestTemplate.md](acceptanceTestTemplate.md).
- `collaboration.md` — planner-selected agents, responsibilities, communication paths, and handoff requirements; see [collaborationTemplate.md](collaborationTemplate.md).
- `communications.md` — short file-based requests, deliveries, acknowledgements, and blockers when inter-agent communication is needed.
- `architecture.md` — stack, application structure, UI specification, and implementation sequence.
- `contracts.md` — precise data, interface, permission, error, and UI behavior linked to acceptance criteria; see [contractTemplate.md](contractTemplate.md).
- `increments.md` — ordered work with exactly one goal per increment, dependencies, checks, and progress; see [incrementTemplate.md](incrementTemplate.md).
- Application source — code, dependency manifests, configuration examples, and tests at the selected source directory.
- `validationState.json` — executable test plan, authoritative verdicts/attempts, and source/contract fingerprints; see [validationGate.md](validationGate.md).
- `validationLogs/` — immutable command output linked by each validation attempt.
- `validation.md` — validator findings, manual evidence, and links to increment/final attempts.
- `handoff.md` — setup, local run commands, and deployment prerequisites.

## Agents

| Agent | Role |
|---|---|
| `agents/planner.md` | Defines scope, selects implementation agents, and owns their communication contract. |
| `agents/architect.md` | Selects the stack and designs the application contracts. |
| `agents/frontend.md` | Implements interfaces and frontend integration. |
| `agents/backend.md` | Implements server behavior and backend integration. |
| `agents/database.md` | Implements schemas, migrations, and persistence operations. |
| `agents/validator.md` | Checks the implementation against the brief and records evidence. |

See [orchestrator.md](orchestrator.md) for stage order and revision rules.

## Shared skills

Reusable procedures live in [skills/](skills/README.md), separate from agent roles. All agents can use every skill; their role files list usual skills and retain ownership of assigned outputs. Repository discovery links under `.agents/skills/` make this library available to Codex without duplicate definitions. Skill folders use lowercase hyphenated names required by the skill format. Skills are instructions, not an automated runner.

## Implementation team

Planner chooses frontend, backend, and database only when their responsibilities need changes. Planner writes `collaboration.md` to identify required communication paths and handoff rules. Architect defines technical interfaces in `contracts.md`; planner confirms role assignments after increments are drafted.

Each increment has one selected owner, optional selected collaborators, and explicit handoff IDs. The owner coordinates contributions and integration within the single goal. Acknowledged handoffs do not replace validation after every increment. See [collaborationTemplate.md](collaborationTemplate.md) for the message format and examples.

## Incremental execution

Planner explicitly creates acceptance criteria. Builders write automated tests for the current goal before implementation, using libraries suited to the application. The test plan covers every criterion; final validation executes its complete coverage.

Run the increment gate before starting work. Build one goal, then have validator review and run the gate validation command; advance only after fresh passing evidence. Changes to source or planning invalidate earlier passes. A feature, component, or connection between components can each be an increment. Integration work counts explicitly, and complete user journeys are checked again during final validation.

## Status

Initial workflow specification. No application has been generated or validated with it yet. The Python gate executes configured validation suites and checks progression; an AI session or runner still dispatches agents. Deployment is a separate action requiring user authorization.
