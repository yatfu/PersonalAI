# Orchestrator — gstack

Execution specification for creating an application or changing an existing one. An AI session or runner follows these stages.

## Execution conventions

- Use file-first handoffs: each agent writes its artifacts and returns a short status summary. Downstream agents read the files directly.
- Keep documents in `outputs/gstack/<applicationName>/`. Source lives at the supplied `applicationPath` for an existing app, otherwise under the output folder's `app/`. Record both locations in the brief and handoff; resolve source paths against the repository root unless supplied as absolute paths.
- For an existing app, inspect its guidance and implementation before planning. Preserve its conventions and stack unless the request requires a change. Do not copy it into a new `app/` directory.
- Follow user constraints and repository instructions. Record assumptions; ask for missing information when it blocks meaningful implementation.
- Use current official documentation when framework or integration behavior needs verification.
- Use Tailwind CSS as the styling default for new applications, following `gstack-frontend`. User-specified styling takes precedence; preserve an existing application's styling system unless a change is requested.
- Patch existing artifacts when revising. Do not overwrite unrelated user work.

Every agent can use the [shared skills](skills/README.md). Read the selected skill before performing its procedure. Skill access does not change role ownership, stage order, or validation gates; these are file-based instructions, not an automated runner.

## Sequence

1. **Planner** uses `gstack-plan` and `gstack-coordinate` to write `brief.md` and `collaboration.md`. Explicitly create the acceptance-criteria table in the brief using [acceptanceTestTemplate.md](acceptanceTestTemplate.md). Select required frontend, backend, and database roles, their responsibilities, and their communication paths. Mark technical details awaiting architect explicitly.
2. **Architect** uses `gstack-design`, `gstack-contracts`, and `gstack-increments` to write `architecture.md`, `contracts.md`, and draft `increments.md`. Map every criterion to automated behavioral tests, compatible test libraries, assigned test writers, and verification increments. Use `gstack-frontend`, `gstack-backend`, and `gstack-database` in design mode for affected layers. Reference planner's communication H-IDs from technical C-IDs and propose required team changes.
3. **Planner** reviews the design and increment plan, resolves team/communication changes, and confirms one selected owner per increment, collaborators, handoff IDs, and shared-file ownership. Architect creates the executable test plan in `validationState.json` using [validationGate.md](validationGate.md). Its AC-IDs must exactly match the planner table. Resolve blocking gaps before dependent implementation; create the source directory if it does not exist yet.
4. Run `checkIncrementGate.py check --state <validationState.json> --increment <ID>` immediately before starting or correcting an increment. Any nonzero exit stops dispatch. All earlier increments must have fresh passing evidence. Dispatch only assigned roles: frontend uses `gstack-frontend`, backend uses `gstack-backend`, and database uses `gstack-database` in implementation mode. Each reads [shared implementation rules](skills/references/implementation.md). The owner uses `gstack-coordinate` and `gstack-increments` to coordinate one goal, have roles write acceptance tests before behavior, and report ready progress in `handoff.md`. Contributions run sequentially by default; communication is logged in `communications.md`.
5. **Validator** reviews assertions, actual test collection, ownership, handoffs, and supplemental manual evidence, then runs `checkIncrementGate.py validate --state <validationState.json> --through <ID> --reviewed`. This executes required tests and regressions, records fingerprints and verdicts, and stops on failure or blockage. Link attempts/logs from `validation.md`. Only fresh passing evidence permits the next increment. See [validationGate.md](validationGate.md) for full commands and correction flags.
6. On failure, the owner coordinates corrections from the affected assigned roles and returns to validator. Scope, team, or communication-rule defects return to planner; technical design or application-contract defects return to architect. Do not advance on failed or blocked verdicts.
7. Repeat steps 4–6 through all increments, including integration increments with explicit owners. Source, test-plan, or planning-document changes invalidate prior gate evidence. The gate conservatively reruns the complete earlier prefix before validating the current increment; rebuild only when corrections are needed.
8. **Validator** checks complete journeys, all criteria/contracts, and reproducible setup, then runs `validate --final --reviewed` and `check --final` using the gate. Every AC-ID needs integrated automated coverage. Individual passes or acknowledged messages alone do not establish completion.

## Handoff contract

- `brief.md`: application name, source and document directories, problem, target users, in-scope and out-of-scope behavior, user journeys, numbered acceptance criteria, constraints, assumptions, and open questions.
- `collaboration.md`: selected and omitted roles with reasons, responsibility boundaries, communication H-IDs, required payloads/artifacts, receiver checks, blockers, and planner-confirmed increment assignments. See [collaborationTemplate.md](collaborationTemplate.md).
- `communications.md`: append-only short messages in the common contract format, with artifact references and acknowledgements. Needed when implementation agents exchange work.
- `architecture.md`: stack and versions, rationale, directory structure, frontend routes, UI layouts and tokens, styling setup, integration boundaries, configuration, implementation steps, validation strategy, and references to `contracts.md` for exact boundary behavior. Mark UI sections not applicable for tasks without an interface.
- `contracts.md`: affected data constraints, stable operation IDs linked to acceptance criteria, interfaces and input/output shapes, permissions, success/failure behavior, side effects, UI states, examples, required verification, and unresolved decisions. Use the shared template proportionally to scope.
- `increments.md`: ordered IDs, one goal per increment, scope, planner-confirmed owner/collaborators, handoff IDs, shared-file ownership, dependencies, acceptance-test matrix, required checks, prerequisites, expected outcomes, and evidence limits. Include integration explicitly; live execution results belong in JSON.
- `validationState.json`: executable criterion/test mappings, dependencies, test commands/files, authoritative statuses, correction counts, numbered attempts, source/planning fingerprints, and final validation. Initialize from [validationStateTemplate.json](validationStateTemplate.json); never reset history on plan revisions.
- `validationLogs/`: immutable command output, referenced and hashed by machine attempts.
- Application source: working code at the selected source directory, dependency manifests and lockfiles where supported, example configuration without secrets, and tests appropriate to behavior.
- `handoff.md`: source and document directories, prerequisites, exact installation/start/test commands and their working directory, environment variable names, database setup, known limitations, and deployment prerequisites. Distinguish working integrations from mocks or unavailable services.
- `validation.md`: links to numbered JSON attempts/logs, assertion and criterion/contract review, manual evidence, unexecuted checks/reasons, and actionable issues identifying increment owner, role, and files. Preserve earlier findings; JSON is authoritative for machine verdicts.

## Loops / retries

- Each increment gets an initial validation and up to two correction passes. A correction pass includes the needed scope, communication, technical contract, or code fixes followed by validation. If it still fails after two corrections, stop before starting another increment and report the remaining issues.
- Missing prerequisites produce a blocked verdict. Record what is needed and stop progression; resuming after the prerequisite becomes available does not itself consume a correction pass.
- Final validation gets an initial attempt and up to two correction passes. Route fixes to affected increments, revalidate them in dependency order, then repeat final checks. Those fixes also count against the affected increments' remaining correction allowance. Stop if either limit is exhausted with unresolved failures.
- Validator records correction passes through `--correction <ID>` (and `--correction final` when applicable). The gate stores counts and attempt references in `validationState.json`; preserve narrative evidence in `validation.md`. Do not reset counts by restarting, renaming, or splitting failed work. Read-only rechecks do not consume correction passes.

## Stopping condition

Complete when `check --final` exits zero, every criterion and required handoff is satisfied, and the local handoff is reproducible. Otherwise stop after the applicable correction limit or blocking prerequisite and state remaining issues. Unrun required checks cannot count as passing. A session or runner must honor gate exits; the script does not intercept arbitrary file edits.

## Output location

Documents: `outputs/gstack/<applicationName>/`, using descriptive camelCase. Source: the selected application directory. Avoid overwriting existing source or documents unless updating or resuming them is part of the request; report a location conflict before writing affected files.
