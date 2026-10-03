# Orchestrator — gstack

Control-flow specification for generating a full stack application. An executing AI session or runner follows these stages.

## Execution conventions

- Use file-first handoffs: each agent writes its artifacts and returns a short status summary. Downstream agents read the files directly.
- Keep implementation and supporting documents in `outputs/gstack/<applicationName>/`, with source under `app/`.
- Follow user constraints and repository instructions. Record assumptions; ask for missing information when it blocks meaningful implementation.
- Use current official documentation when framework or integration behavior needs verification.
- Patch existing artifacts when revising. Do not overwrite unrelated user work.

## Sequence

1. **planner** reads the request and writes `brief.md`.
2. **architect** reads the brief and writes `architecture.md`.
3. **builder** reads both documents, implements `app/`, and writes `handoff.md`.
4. **validator** inspects the application, runs appropriate checks, and writes `validation.md`.
5. If validation fails, **builder** patches the affected implementation and handoff; **validator** repeats the affected checks.

## Handoff contract

- `brief.md`: application name, problem, target users, in-scope and out-of-scope behavior, user journeys, numbered acceptance criteria, constraints, assumptions, and open questions.
- `architecture.md`: stack and rationale, directory structure, data entities and relationships, API/request contracts, frontend routes, authentication and authorization needs, integration boundaries, configuration, implementation steps, and validation strategy.
- `app/`: working source code, dependency manifests and lockfiles where supported, example environment configuration without secrets, and tests appropriate to application behavior.
- `handoff.md`: prerequisites, exact installation/start/test commands, environment variable names, database setup, known limitations, and deployment prerequisites. Distinguish working integrations from mocks or unavailable services.
- `validation.md`: verdict (`passed`, `failed`, or `blocked`), acceptance-criterion coverage, checks and outcomes, unexecuted checks and reasons, and actionable issues with file references where possible.

## Loops / retries

Allow up to two implementation revision passes after the initial validation. Scope each revision to recorded issues. If issues remain, stop and report them with the current artifacts; do not declare success. A prerequisite that cannot be supplied is recorded as blocked, with the next action needed.

## Stopping condition

Complete when acceptance criteria are satisfied, required checks pass, and the local handoff is reproducible. Otherwise stop after the revision limit or a blocking prerequisite and state the remaining issues. Unrun checks cannot count as passing.

## Output location

`outputs/gstack/<applicationName>/`, where the name is converted to descriptive camelCase. Avoid overwriting an existing application unless updating it is part of the request.
