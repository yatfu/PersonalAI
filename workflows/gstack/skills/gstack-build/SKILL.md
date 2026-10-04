---
name: gstack-build
description: Implement or correct one gstack increment across frontend, backend, persistence, or integration while preserving contracts and single-goal scope.
---

# Build one increment

## Inputs

Read `brief.md`, `collaboration.md`, `architecture.md`, `contracts.md`, `increments.md`, and relevant `communications.md` entries, plus validator issues when correcting work. Identify the current increment; its prerequisites must have passed.

## Procedure

- Work only as a planner-selected implementation role assigned to the current increment. Follow responsibility and shared-file ownership in `collaboration.md`; the increment owner coordinates any collaborators.
- Use `gstack-coordinate` for contracted messages and acknowledgements. Missing or incompatible handoffs block dependent work.
- Implement only its one goal and included scope. The increment owner marks it building, then validating. Return control for validation before starting another increment.
- Follow contracted field shapes, validation, permissions, errors, persistence, and applicable UI states: loading, empty, success, and failure.
- Use shared types or schemas where supported. Choose internal details autonomously when they preserve behavior; documents alone do not enforce contracts.
- Report contradictory, incomplete, or infeasible contracts by ID and proposed resolution to architect before dependent implementation. Continue only unaffected work in the current increment.
- Backend validates server input and enforces access controls. Database implements assigned constraints, migrations, and persistence adapters; frontend consumes contracted interfaces and implements UI behavior. Do only the responsibilities assigned to the active role.
- Keep credentials outside committed files and provide configuration examples with variable names and placeholders.
- Connect layers in designated integration increments. Label isolated stubs, mocks, and unavailable services; replace them where real integration is required.
- Before implementing current increment behavior, create or extend its automated acceptance tests following [acceptanceTestTemplate.md](../../acceptanceTestTemplate.md). Cover assigned planner criteria through observable behavior using compatible libraries; reference AC-IDs in test names and report test files, cases, fixtures, and exact non-watch commands. Future criteria remain planned, not prematurely implemented. Tests must not weaken planner outcomes or count skipped cases as coverage.
- Use `gstack-ui` for interface styling and behavior. Tailwind CSS is the default for new apps; follow the chosen architecture and preserve an existing app's styling system unless a change is requested. Compile CSS through the application build and use complete utility class strings.
- Patch affected files and update the handoff on corrections instead of regenerating the application; preserve unrelated work.
- Before a correction, check the remaining allowance in `increments.md`. Record the correction pass and identify previously passed increments affected by source changes so validator can invalidate and recheck their evidence. Do not start later increments while a gate is failed or blocked.

## Ownership and handoff

- Each assigned implementation agent writes owned source to the directory recorded in the brief: `applicationPath` for an existing app, otherwise the output folder's `app/`.
- Increment owner maintains `handoff.md` using collaborator contributions, with source and document paths, prerequisites, commands and their working directory, environment names, database setup, limitations, and deployment prerequisites.
- Other roles may diagnose or propose fixes within their authority. Implementation self-checks do not grant a validation pass.
- Contributors report to the increment owner with artifact and communication references. Owner returns increment ID, goal, changed files, handoff IDs, checks, and limitations to validator.
- Deployment or publication requires user authorization.
