---
name: gstack-plan
description: Define or assess gstack scope, user journeys, and acceptance criteria when preparing or revising an application brief.
---

# Plan application scope

## Inputs

Read the request, application name, requirements, and constraints. Read an existing `brief.md` and reported scope issues when available.

For an existing app, inspect its instructions and current behavior. Record the source directory (`applicationPath`) and the document directory (`outputs/gstack/<applicationName>/`) in the brief. For a new app, source defaults to the document directory's `app/` folder.

## Procedure

- Describe intended users, their problem, and the desired outcome.
- Define the smallest complete version fulfilling the request, including required frontend, backend, and persistence behavior.
- Describe user journeys and assign stable IDs such as AC-1 to observable acceptance criteria, including relevant failure states.
- Separate required and deferred features; record assumptions, constraints, and open questions.
- Resolve routine details from context. Ask when missing information changes essential behavior; identify blocked work.

## Ownership and handoff

- Planner writes or patches `brief.md` with these decisions.
- Other roles assess scope or propose changes to planner.
- Return a short summary with the file path and unresolved questions.
