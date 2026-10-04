---
name: gstack-plan
description: Define gstack scope and acceptance criteria, select required implementation agents, and coordinate their communication contract during planning.
---

# Plan application scope

## Inputs

Read the request, application name, requirements, and constraints. Read an existing `brief.md` and reported scope issues when available.

For an existing app, inspect its instructions and current behavior. Record the source directory (`applicationPath`) and the document directory (`outputs/gstack/<applicationName>/`) in the brief. For a new app, source defaults to the document directory's `app/` folder.

## Procedure

- Describe intended users, their problem, and the desired outcome.
- Define the smallest complete version fulfilling the request, including required frontend, backend, and persistence behavior.
- Explicitly create `## Acceptance criteria` in `brief.md` using [acceptanceTestTemplate.md](../../acceptanceTestTemplate.md). Give every required outcome a stable AC-ID, preconditions, action, and observable expected result, including relevant failure states. Planner owns these criteria; do not delegate their creation to builders.
- Separate required and deferred features; record assumptions, constraints, and open questions.
- Use `gstack-coordinate` to select required frontend, backend, and database roles and write `collaboration.md`. Review architecture and proposed increments, then confirm owners, collaborators, handoff IDs, and shared-file ownership before implementation.
- Resolve routine details from context. Ask when missing information changes essential behavior; identify blocked work.

## Ownership and handoff

- Planner writes or patches `brief.md` and `collaboration.md`, and confirms role assignments in `increments.md`. Technical application contracts remain architect-owned.
- Other roles assess scope or propose changes to planner.
- Return a short summary with the file path and unresolved questions.
