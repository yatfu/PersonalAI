---
name: gstack-build
description: Implement or correct one gstack increment across frontend, backend, persistence, or integration while preserving contracts and single-goal scope.
---

# Build one increment

## Inputs

Read `brief.md`, `architecture.md`, `contracts.md`, and `increments.md`, plus validator issues when correcting work. Identify the current increment; its prerequisites must have passed.

## Procedure

- Implement only its one goal and included scope. Mark it building, then validating. Return control for validation before starting another increment.
- Follow contracted field shapes, validation, permissions, errors, persistence, and applicable UI states: loading, empty, success, and failure.
- Use shared types or schemas where supported. Choose internal details autonomously when they preserve behavior; documents alone do not enforce contracts.
- Report contradictory, incomplete, or infeasible contracts by ID and proposed resolution to architect before dependent implementation. Continue only unaffected work in the current increment.
- Validate input server-side and enforce required access controls at backend boundaries.
- Keep credentials outside committed files and provide configuration examples with variable names and placeholders.
- Connect layers in designated integration increments. Label isolated stubs, mocks, and unavailable services; replace them where real integration is required.
- Include meaningful checks for important success and failure paths, plus exact setup, run, and check commands. Use [styleNewsletter.md](../../../../resources/styleNewsletter.md) for visual guidance where appropriate.
- Patch affected files and update the handoff on corrections instead of regenerating the application; preserve unrelated work.
- Before a correction, check the remaining allowance in `increments.md`. Record the correction pass and identify previously passed increments affected by source changes so validator can invalidate and recheck their evidence. Do not start later increments while a gate is failed or blocked.

## Ownership and handoff

- Builder writes source to the directory recorded in the brief: `applicationPath` for an existing app, otherwise the output folder's `app/`.
- Maintain `handoff.md` with source and document paths, prerequisites, commands and their working directory, environment names, database setup, limitations, and deployment prerequisites.
- Other roles may diagnose or propose fixes within their authority. Builder self-checks do not grant a validation pass.
- Return increment ID, goal, changed files, checks, and limitations.
- Deployment or publication requires user authorization.
