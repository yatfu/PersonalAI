# Orchestrator — gstack

Execution specification for creating an application or changing an existing one. An AI session or runner follows these stages.

## Execution conventions

- Use file-first handoffs: each agent writes its artifacts and returns a short status summary. Downstream agents read the files directly.
- Keep documents in `outputs/gstack/<applicationName>/`. Source lives at the supplied `applicationPath` for an existing app, otherwise under the output folder's `app/`. Record both locations in the brief and handoff; resolve source paths against the repository root unless supplied as absolute paths.
- For an existing app, inspect its guidance and implementation before planning. Preserve its conventions and stack unless the request requires a change. Do not copy it into a new `app/` directory.
- Follow user constraints and repository instructions. Record assumptions; ask for missing information when it blocks meaningful implementation.
- Use current official documentation when framework or integration behavior needs verification.
- Use Tailwind CSS as the styling default for new applications, following `gstack-ui`. User-specified styling takes precedence; preserve an existing application's styling system unless a change is requested.
- Patch existing artifacts when revising. Do not overwrite unrelated user work.

Every agent can use the [shared skills](skills/README.md). Read the selected skill before performing its procedure. Skill access does not change role ownership, stage order, or validation gates; these are file-based instructions, not an automated runner.

## Sequence

1. **Planner** uses `gstack-plan` and `gstack-coordinate` to write `brief.md` and `collaboration.md`. Explicitly create the acceptance-criteria table in the brief using [acceptanceTestTemplate.md](acceptanceTestTemplate.md). Select required frontend, backend, and database roles, their responsibilities, and their communication paths. Mark technical details awaiting architect explicitly.
2. **Architect** uses `gstack-design`, `gstack-contracts`, and `gstack-increments` to write `architecture.md`, `contracts.md`, and draft `increments.md`. Map every criterion to automated behavioral tests, compatible test libraries, assigned test writers, and verification increments. Use `gstack-ui` for interface specifications. Reference planner's communication H-IDs from technical C-IDs and propose any required team changes.
3. **Planner** reviews the design and increment plan, resolves team/communication changes, and confirms one selected owner per increment, collaborators, handoff IDs, and shared-file ownership. Planner and architect resolve blocking gaps before dependent implementation.
4. Select the next increment in dependency order. Its prerequisites must have passed. Dispatch only its assigned frontend, backend, and database roles. The owner uses `gstack-build`, `gstack-coordinate`, and `gstack-increments` to coordinate contributions to the single goal, have assigned roles write acceptance tests before implementing behavior, update `handoff.md`, and mark it validating. Contributions run sequentially by default; communication is logged in `communications.md`.
5. **Validator** validates immediately after the increment, checking ownership, required handoffs, goal-specific behavior, and regression evidence. Record results in `validation.md` and update `increments.md`. Only a passed verdict permits the next increment.
6. On failure, the owner coordinates corrections from the affected assigned roles and returns to validator. Scope, team, or communication-rule defects return to planner; technical design or application-contract defects return to architect. Do not advance on failed or blocked verdicts.
7. Repeat steps 4–6 through all increments, including integration increments with explicit owners. Changes invalidate affected increments and dependent evidence, and reset final validation to pending. Revalidate in dependency order; rebuild only when corrections are needed.
8. **Validator** checks complete user journeys, all acceptance criteria and contracts, and reproducible local setup. Record a separate final verdict; individual passes or acknowledged messages alone do not establish completion.

## Handoff contract

- `brief.md`: application name, source and document directories, problem, target users, in-scope and out-of-scope behavior, user journeys, numbered acceptance criteria, constraints, assumptions, and open questions.
- `collaboration.md`: selected and omitted roles with reasons, responsibility boundaries, communication H-IDs, required payloads/artifacts, receiver checks, blockers, and planner-confirmed increment assignments. See [collaborationTemplate.md](collaborationTemplate.md).
- `communications.md`: append-only short messages in the common contract format, with artifact references and acknowledgements. Needed when implementation agents exchange work.
- `architecture.md`: stack and versions, rationale, directory structure, frontend routes, UI layouts and tokens, styling setup, integration boundaries, configuration, implementation steps, validation strategy, and references to `contracts.md` for exact boundary behavior. Mark UI sections not applicable for tasks without an interface.
- `contracts.md`: affected data constraints, stable operation IDs linked to acceptance criteria, interfaces and input/output shapes, permissions, success/failure behavior, side effects, UI states, examples, required verification, and unresolved decisions. Use the shared template proportionally to scope.
- `increments.md`: ordered IDs, one goal per increment, scope, planner-confirmed owner and collaborators, handoff IDs, shared-file ownership, dependencies, acceptance/contract references, required checks with prerequisites and expected outcomes, regression checks, evidence limits, statuses, correction counts, latest validation references, and execution state. Include integration work explicitly.
- Application source: working code at the selected source directory, dependency manifests and lockfiles where supported, example configuration without secrets, and tests appropriate to behavior.
- `handoff.md`: source and document directories, prerequisites, exact installation/start/test commands and their working directory, environment variable names, database setup, known limitations, and deployment prerequisites. Distinguish working integrations from mocks or unavailable services.
- `validation.md`: per-increment attempts and verdicts (`passed`, `failed`, or `blocked`), acceptance-criterion and contract coverage, checks and outcomes, unexecuted checks and reasons, actionable issues identifying the increment owner, affected role, and file references, and a separate final application verdict. Preserve earlier attempts.

## Loops / retries

- Each increment gets an initial validation and up to two correction passes. A correction pass includes the needed scope, communication, technical contract, or code fixes followed by validation. If it still fails after two corrections, stop before starting another increment and report the remaining issues.
- Missing prerequisites produce a blocked verdict. Record what is needed and stop progression; resuming after the prerequisite becomes available does not itself consume a correction pass.
- Final validation gets an initial attempt and up to two correction passes. Route fixes to affected increments, revalidate them in dependency order, then repeat final checks. Those fixes also count against the affected increments' remaining correction allowance. Stop if either limit is exhausted with unresolved failures.
- Record counts and attempt references in `increments.md` and preserve full evidence in `validation.md`. Resume from those files; do not reset counts by restarting, renaming, or splitting failed work. Read-only rechecks do not consume correction passes.

## Stopping condition

Complete when every increment has passed, the final application verdict is passed, acceptance criteria and required communication handoffs are satisfied, and the local handoff is reproducible. Otherwise stop after the applicable revision limit or a blocking prerequisite and state remaining issues. Unrun required checks cannot count as passing.

## Output location

Documents: `outputs/gstack/<applicationName>/`, using descriptive camelCase. Source: the selected application directory. Avoid overwriting existing source or documents unless updating or resuming them is part of the request; report a location conflict before writing affected files.
