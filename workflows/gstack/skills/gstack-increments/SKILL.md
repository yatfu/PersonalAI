---
name: gstack-increments
description: Plan ordered gstack increments with exactly one goal each, or maintain their dependencies and progress during implementation and validation.
---

# gstack-increments

Read the brief, architecture, contracts, and existing increment plan. Use [incrementTemplate.md](../../incrementTemplate.md) for `increments.md`.

- Give each increment a stable ID, one goal, included/excluded scope, dependencies, acceptance/contract references, required checks with expected outcomes, regression checks, and evidence limits.
- Features, components, setup capabilities, and integration connections may each be goals. Split independently evaluable goals; multiple files or layers may serve one goal.
- Plan integration explicitly when pieces are built separately. Isolated checks do not prove a connected journey. Ensure the full plan covers required criteria.
- Prerequisites must pass before dependent work starts. Validate every increment and correction; advance only with a validator-owned passed verdict.
- Track pending, building, validating, passed, failed, and blocked states, current increment, and separate final validation state.
- Update affected dependencies/checks when plans or contracts change and mark affected passed increments pending revalidation. Preserve prior evidence in `validation.md`.

The architect owns goals, dependencies, and planned checks. Builder updates implementation progress; validator owns verdicts. Other roles propose changes to those owners. Follow orchestrator retry limits; do not reset counts by renaming or splitting failures. Return a short summary of affected IDs.
