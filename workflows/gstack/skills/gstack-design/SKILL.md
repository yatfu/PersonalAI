---
name: gstack-design
description: Design or assess gstack application architecture from a brief, including stack selection, application structure, integrations, and local setup.
---

# Design application architecture

## Inputs

Read `brief.md`, `collaboration.md`, stack preferences, and integration constraints. Inspect existing design documents and source when relevant.

## Procedure

- Honor an explicit stack choice; otherwise choose a suitable stack and explain why.
- Default new applications to Tailwind CSS for styling. Use `gstack-frontend` to specify layouts, tokens, accessible controls, UI states, and framework-compatible build setup in `architecture.md`. Record selected versions and any departure from defaults; existing apps keep their styling system unless a change is requested.
- For an existing app, preserve its stack and conventions unless the requested change requires otherwise. Design against its actual source directory recorded in the brief.
- Respect planner's team and responsibility boundaries. If design requires another role or communication path, propose it to planner before dependent work.
- For server behavior, use `gstack-backend` in design mode to specify public boundaries, business rules, permissions, persistence connections, and service failure behavior.
- For persistence, use `gstack-database` in design mode to specify data models, integrity constraints, migrations, queries, transactions, and test-environment setup.
- Define frontend routes, a simple application directory structure, persistence setup, configuration, and integration boundaries.
- Identify required authentication, authorization, input validation, and error handling.
- Specify unavailable-service behavior and identify incompatible constraints or missing prerequisites before dependent work proceeds.
- Reference `contracts.md` for exact boundary behavior and `increments.md` for ordered work rather than duplicating them.
- Select compatible testing libraries and non-watch commands for the application. Preserve suitable existing tools; Vitest, Playwright, and pytest are examples, not fixed requirements.
- Specify meaningful validation and local setup requirements. Verify unfamiliar or changing details with current official documentation.

## Ownership and handoff

- Architect writes or patches `architecture.md` with stack rationale, structure, routes, integrations, configuration, implementation overview, and validation strategy, including gate setup and executable test commands from [validationGate.md](../../validationGate.md).
- Other roles report findings to architect. Keep this procedure focused on design documents; application implementation belongs to the selected implementation agents.
- Return a short summary with file references and unresolved prerequisites.
