---
name: gstack-contracts
description: Define, inspect, or propose corrections to gstack data and interface contracts connecting UI, backend, persistence, and integrations to acceptance criteria.
---

# gstack-contracts

Read the brief, architecture, existing contracts, and affected source interfaces. Use [contractTemplate.md](../../contractTemplate.md) when writing contracts.

- Assign stable operation IDs such as C-1 linked to acceptance criteria.
- Specify input/output shapes, data constraints and relationships, ownership, permissions, errors, side effects, persistence, and UI states.
- Include examples and observable checks. Check consistency and coverage of required journeys.
- Scale detail to scope. Reference existing schemas and symbols; use the application's actual interface mechanism.
- Mark unresolved decisions and resolve blocking ones before dependent implementation. Keep exact boundary behavior in `contracts.md` and reference it from architecture.
- Report contradictions, gaps, or infeasible rules by ID with proposed resolutions. Route scope changes to planner and contract decisions to architect; preserve unrelated contracts and record revisions in the decision log.
- Identify affected increments when contracts change so prior verdicts are invalidated and checks updated before advancement.

The architect owns updates to `contracts.md`. Other roles inspect or propose corrections without silently changing contracts or acceptance criteria. Return a short summary referencing files and IDs.
