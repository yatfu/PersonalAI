---
name: gstack-contracts
description: Define, inspect, or propose corrections to gstack data and interface contracts connecting UI, backend, persistence, and integrations to acceptance criteria.
---

# Define and inspect contracts

## Inputs

Read `brief.md`, `collaboration.md`, and `architecture.md`. Inspect existing `contracts.md` and affected source interfaces when available. Use [contractTemplate.md](../../contractTemplate.md) when writing contracts.

## Procedure

- Connect technical operations to planner-defined H-IDs and selected role boundaries. Request planner updates for new communication paths; keep technical schemas here and message rules in `collaboration.md`.
- Assign stable operation IDs such as C-1 linked to acceptance criteria.
- Specify input/output shapes, data constraints and relationships, ownership, permissions, errors, side effects, persistence, and UI states.
- Include examples and observable checks. Check consistency and coverage of required journeys.
- Scale detail to scope. Reference existing schemas and symbols; use the application's actual interface mechanism.
- Mark unresolved decisions and resolve blocking ones before dependent implementation. Keep exact boundary behavior in `contracts.md` and reference it from architecture.
- Report contradictions, gaps, or infeasible rules by ID with proposed resolutions. Route scope changes to planner and contract decisions to architect; preserve unrelated contracts and record revisions in the decision log.
- Identify affected increments and dependent evidence when contracts change. Use `gstack-increments` to invalidate their passes, update checks, and reset final validation to pending before advancement.

## Ownership and handoff

- Architect owns updates to `contracts.md`.
- Other roles inspect or propose corrections; they must not silently change contracts or acceptance criteria.
- Return a short summary referencing files and affected IDs.
