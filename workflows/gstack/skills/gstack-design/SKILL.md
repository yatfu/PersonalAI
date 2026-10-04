---
name: gstack-design
description: Design or assess gstack application architecture from a brief, including stack selection, application structure, integrations, and local setup.
---

# gstack-design

Read `brief.md`, stack preferences, integration constraints, and existing design/source where relevant.

- Honor an explicit stack choice; otherwise choose a suitable stack and explain why.
- For an existing app, preserve its stack and conventions unless the requested change requires otherwise. Design against its actual source directory recorded in the brief.
- Define frontend routes, a simple application directory structure, persistence setup, configuration, and integration boundaries.
- Identify required authentication, authorization, input validation, and error handling.
- Specify unavailable-service behavior and identify incompatible constraints or missing prerequisites before dependent work proceeds.
- Reference `contracts.md` for exact boundary behavior and `increments.md` for ordered work rather than duplicating them.
- Specify meaningful validation and local setup requirements. Verify unfamiliar or changing details with current official documentation.

The architect writes or patches `architecture.md` with stack rationale, structure, routes, integrations, configuration, implementation overview, and validation strategy. Other roles report findings to architect. This procedure produces design documents, not application code. Return a short summary and unresolved prerequisites.
