# Orchestrator — gstack

Execution specification for creating an application or changing an existing one. An AI session or runner follows these stages.

## Execution conventions

- Use file-first handoffs: each agent writes its artifacts and returns a short status summary. Downstream agents read the files directly.
- Keep documents in `outputs/gstack/<applicationName>/`. Source lives at the supplied `applicationPath` for an existing app, otherwise under the output folder's `app/`. Record both locations in the brief and handoff; resolve source paths against the repository root unless supplied as absolute paths.
- For an existing app, inspect its guidance and implementation before planning. Preserve its conventions and stack unless the request requires a change. Do not copy it into a new `app/` directory.
- Follow user constraints and repository instructions. Record assumptions; ask for missing information when it blocks meaningful implementation.
- Use current official documentation when framework or integration behavior needs verification.
- Patch existing artifacts when revising. Do not overwrite unrelated user work.

Every agent can use the [shared skills](skills/README.md). Read the selected skill before performing its procedure. Skill access does not change role ownership, stage order, or validation gates; these are file-based instructions, not an automated runner.

## Sequence

1. **planner** uses `gstack-plan` on the request and writes `brief.md`.
2. **architect** uses `gstack-design`, `gstack-contracts`, and `gstack-increments` to write `architecture.md`, `contracts.md`, and `increments.md` using [contractTemplate.md](contractTemplate.md) and [incrementTemplate.md](incrementTemplate.md). Checks coverage, consistency, dependencies, and one-goal boundaries before handing off.
3. Select the next pending increment in dependency order. Its prerequisites must have passed and blocking decisions must be resolved. **builder** uses `gstack-build` and `gstack-increments` to implement only that increment's goal in the selected source directory, updates `handoff.md`, and marks it ready for validation in `increments.md`.
4. **validator** uses `gstack-validate` and `gstack-increments` to validate that increment immediately, records checks and verdict in `validation.md`, and updates its status in `increments.md`. Required checks must pass before the next increment starts. Isolated component checks do not count as proof of a connected journey.
5. If validation fails, **builder** patches that increment and the handoff; **validator** revalidates it. Do not advance on a failed or blocked verdict.
   - Scope defects return to **planner**; design or contract defects return to **architect** before dependent implementation resumes. Changes propagate to affected downstream files and checks. The validator does not change code or acceptance criteria.
6. Repeat steps 3–5 until all increments pass, including explicitly planned integration increments. Contract or plan changes invalidate affected prior verdicts; revalidate affected increments before advancing.
7. **validator** uses `gstack-validate` for final application validation against the full brief and contracts, including complete user journeys and reproducible local setup. Record a separate final verdict; individual increment passes alone do not establish application completion.

## Handoff contract

- `brief.md`: application name, source and document directories, problem, target users, in-scope and out-of-scope behavior, user journeys, numbered acceptance criteria, constraints, assumptions, and open questions.
- `architecture.md`: stack and rationale, directory structure, frontend routes, integration boundaries, configuration, implementation steps, validation strategy, and references to `contracts.md` for exact boundary behavior.
- `contracts.md`: affected data constraints, stable operation IDs linked to acceptance criteria, interfaces and input/output shapes, permissions, success/failure behavior, side effects, UI states, examples, required verification, and unresolved decisions. Use the shared template proportionally to scope.
- `increments.md`: ordered IDs, exactly one goal per increment, included/excluded scope, dependencies, acceptance/contract references, required checks and expected outcomes, regression checks, evidence limits, status, and current execution state. Integration work is explicitly represented.
- Application source: working code at the selected source directory, dependency manifests and lockfiles where supported, example configuration without secrets, and tests appropriate to behavior.
- `handoff.md`: source and document directories, prerequisites, exact installation/start/test commands and their working directory, environment variable names, database setup, known limitations, and deployment prerequisites. Distinguish working integrations from mocks or unavailable services.
- `validation.md`: per-increment attempts and verdicts (`passed`, `failed`, or `blocked`), acceptance-criterion and contract coverage, checks and outcomes, unexecuted checks and reasons, actionable issues with responsible role and file references, and a separate final application verdict. Preserve earlier attempts.

## Loops / retries

Allow up to two revision passes per increment after its initial validation, including required scope or contract corrections and implementation updates. Validate after every revision. If issues remain, stop before starting the next increment and report current artifacts. A missing prerequisite is blocked, with the next action needed. Final validation also allows up to two correction passes; route corrections to affected increments and revalidate them before repeating final checks. Do not reset retry counts merely by renaming or splitting a failed increment.

## Stopping condition

Complete when every increment has passed, the final application verdict is passed, acceptance criteria are satisfied, and the local handoff is reproducible. Otherwise stop after the applicable revision limit or a blocking prerequisite and state remaining issues. Unrun required checks cannot count as passing.

## Output location

Documents: `outputs/gstack/<applicationName>/`, using descriptive camelCase. Source: the selected application directory. Avoid overwriting existing source or documents unless updating or resuming them is part of the request; report a location conflict before writing affected files.
