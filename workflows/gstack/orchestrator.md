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

1. **planner** uses `gstack-plan` on the request and writes `brief.md`.
2. **architect** uses `gstack-design`, `gstack-contracts`, and `gstack-increments` to write the planning files using [contractTemplate.md](contractTemplate.md) and [incrementTemplate.md](incrementTemplate.md). For interface work, use `gstack-ui` to include a UI specification in `architecture.md`. Check coverage, consistency, dependencies, and one-goal boundaries before handoff.
3. Select the next pending increment in dependency order. Its prerequisites must have passed and blocking decisions must be resolved. **builder** uses `gstack-build` and `gstack-increments` to implement only that increment's goal in the selected source directory, updates `handoff.md`, and marks it ready for validation in `increments.md`.
4. **validator** uses `gstack-validate` and `gstack-increments` to validate that increment immediately, records checks and verdict in `validation.md`, and updates its status in `increments.md`. Required checks must pass before the next increment starts. Isolated component checks do not count as proof of a connected journey.
5. If validation fails, **builder** patches that increment and the handoff; **validator** revalidates it. Do not advance on a failed or blocked verdict.
   - Scope defects return to **planner**; design or contract defects return to **architect** before dependent implementation resumes. Changes propagate to affected downstream files and checks. The validator does not change code or acceptance criteria.
6. Repeat steps 3–5 until all increments pass, including planned integration increments. Contract or plan changes invalidate affected increments and dependent evidence, and reset final validation to pending. Revalidate in dependency order before advancing; rebuild only when corrections are needed.
7. **validator** uses `gstack-validate` for final application validation against the full brief and contracts, including complete user journeys and reproducible local setup. Record a separate final verdict; individual increment passes alone do not establish application completion.

## Handoff contract

- `brief.md`: application name, source and document directories, problem, target users, in-scope and out-of-scope behavior, user journeys, numbered acceptance criteria, constraints, assumptions, and open questions.
- `architecture.md`: stack and versions, rationale, directory structure, frontend routes, UI layouts and tokens, styling setup, integration boundaries, configuration, implementation steps, validation strategy, and references to `contracts.md` for exact boundary behavior. Mark UI sections not applicable for tasks without an interface.
- `contracts.md`: affected data constraints, stable operation IDs linked to acceptance criteria, interfaces and input/output shapes, permissions, success/failure behavior, side effects, UI states, examples, required verification, and unresolved decisions. Use the shared template proportionally to scope.
- `increments.md`: ordered IDs, one goal per increment, scope, dependencies, acceptance/contract references, required checks with prerequisites and expected outcomes, regression checks, evidence limits, statuses, correction counts, latest validation references, and execution state. Include integration work explicitly.
- Application source: working code at the selected source directory, dependency manifests and lockfiles where supported, example configuration without secrets, and tests appropriate to behavior.
- `handoff.md`: source and document directories, prerequisites, exact installation/start/test commands and their working directory, environment variable names, database setup, known limitations, and deployment prerequisites. Distinguish working integrations from mocks or unavailable services.
- `validation.md`: per-increment attempts and verdicts (`passed`, `failed`, or `blocked`), acceptance-criterion and contract coverage, checks and outcomes, unexecuted checks and reasons, actionable issues with responsible role and file references, and a separate final application verdict. Preserve earlier attempts.

## Loops / retries

- Each increment gets an initial validation and up to two correction passes. A correction pass includes the needed scope, contract, or code fixes followed by validation. If it still fails after two corrections, stop before starting another increment and report the remaining issues.
- Missing prerequisites produce a blocked verdict. Record what is needed and stop progression; resuming after the prerequisite becomes available does not itself consume a correction pass.
- Final validation gets an initial attempt and up to two correction passes. Route fixes to affected increments, revalidate them in dependency order, then repeat final checks. Those fixes also count against the affected increments' remaining correction allowance. Stop if either limit is exhausted with unresolved failures.
- Record counts and attempt references in `increments.md` and preserve full evidence in `validation.md`. Resume from those files; do not reset counts by restarting, renaming, or splitting failed work. Read-only rechecks do not consume correction passes.

## Stopping condition

Complete when every increment has passed, the final application verdict is passed, acceptance criteria are satisfied, and the local handoff is reproducible. Otherwise stop after the applicable revision limit or a blocking prerequisite and state remaining issues. Unrun required checks cannot count as passing.

## Output location

Documents: `outputs/gstack/<applicationName>/`, using descriptive camelCase. Source: the selected application directory. Avoid overwriting existing source or documents unless updating or resuming them is part of the request; report a location conflict before writing affected files.
