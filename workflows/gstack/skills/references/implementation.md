# Shared implementation rules

Frontend, backend, and database skills use this procedure in implementation mode. Architect uses their design guidance; validator uses their review guidance. Shared skill access does not transfer role ownership.

## Enter one increment

- Read `brief.md`, `collaboration.md`, `architecture.md`, `contracts.md`, `increments.md`, `validationState.json`, relevant `communications.md` entries, and validator issues when correcting work.
- Work only as a planner-selected implementation role assigned to the current increment. Follow responsibility and shared-file ownership in `collaboration.md`; the increment owner coordinates collaborators.
- Before the first contribution to an increment or correction pass, its owner runs the read-only entry check in [validationGate.md](../../validationGate.md). Contributors confirm that successful check rather than repeating it after each contribution. Stop on denial; a Markdown status or self-check cannot authorize advancement.
- Implement only the increment's one goal and included scope. Features, components, and connections can be separate increments. Return control to validator after every increment and correction; never start a later increment with failed, blocked, or stale prerequisite evidence.

## Tests and implementation

- Create or extend assigned automated acceptance tests before implementing behavior, following [acceptanceTestTemplate.md](../../acceptanceTestTemplate.md). Use compatible libraries, planner AC-IDs, observable assertions, and exact non-watch commands. Future criteria remain planned; do not weaken outcomes or count skipped cases as coverage.
- Follow contracted shapes, validation, permissions, errors, persistence, and UI states applicable to the active role. Use shared types or schemas where supported; documents alone do not enforce contracts. Internal implementation choices may vary when they preserve behavior.
- Report contradictory, incomplete, or infeasible technical contracts to architect with IDs and a proposed resolution before dependent implementation. Continue only unaffected work within the current increment. Assignment or communication changes return to planner.
- Use `gstack-coordinate` for required messages and acknowledgements. Missing or incompatible handoffs block dependent work. Respect the current shared-file writer and keep contributions sequential by default.
- Connect layers in designated integration increments. Label stubs, doubles, and unavailable services; replace them wherever real connected evidence is required.
- Keep credentials outside committed files and supply configuration examples with names and placeholders. Record exact setup, run, and check commands and their working directories.
- Patch affected files during corrections rather than regenerating the application; preserve unrelated work. Check remaining correction allowances in `validationState.json` before fixes and report corrected increment IDs for validator's correction flags. Preserve all prior attempts and counts.

## Output and handoff

- Change only owned source and tests at `applicationPath` for an existing app, otherwise the application's output folder `app/`. Preserve its conventions and chosen technologies unless a change is required.
- Contributors report increment ID, artifact references, AC/C/H IDs, test cases and commands, checks, blockers, and limitations to the owner. Append required messages in `communications.md`.
- Increment owner maintains progress and `handoff.md`: source/document paths, prerequisites, commands, configuration names, database setup where needed, integration status, limitations, and deployment prerequisites. It returns ready work to validator.
- Implementation self-checks and acknowledged handoffs cannot grant a pass. Only validator runs authoritative gate validation and records findings through `gstack-validate`.
- Deployment or publication requires user authorization.
