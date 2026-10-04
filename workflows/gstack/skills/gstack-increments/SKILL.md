---
name: gstack-increments
description: Plan ordered gstack increments with exactly one goal each, or maintain their dependencies and progress during implementation and validation.
---

# Plan and track increments

## Inputs

Read `brief.md`, `collaboration.md`, `architecture.md`, and `contracts.md`. Read existing `increments.md` when available. Use [incrementTemplate.md](../../incrementTemplate.md) to create or update the plan.

## Procedure

- Give each increment a stable ID, one goal, scope, dependencies, acceptance/contract references, required checks with prerequisites and expected outcomes, regression checks, and evidence limits. Require at least one observable goal-specific check.
- Features, components, setup capabilities, and integration connections may each be goals. Split independently evaluable goals; multiple files or layers may serve one goal.
- Have planner confirm one selected owner per increment, collaborators, communication H-IDs, and shared-file ownership. Keep assignments consistent with `collaboration.md`; implementation cannot start with unresolved ownership.
- Map every planner AC-ID to concrete automated behavioral tests, test writers, and verification increments using [acceptanceTestTemplate.md](../../acceptanceTestTemplate.md). No criterion may be omitted; identify supporting isolated evidence versus complete acceptance coverage.
- Plan integration explicitly when pieces are built separately. Isolated checks do not prove a connected journey. Ensure the full plan covers required criteria.
- Prerequisites must pass before dependent work starts. Validate every increment and correction; advance only with a validator-owned passed verdict.
- Track the statuses and allowed transitions in the increment template, current increment, validation attempt references, correction counts, and separate final validation state.
- When plans or contracts change, update affected dependencies and checks. Mark affected increments and dependents with obsolete evidence pending revalidation, record why, and reset final validation to pending. Preserve prior evidence in `validation.md`; only validator grants new passes.

## Ownership and handoff

- Architect owns goals, dependencies, and planned checks. Planner owns agent assignments and communication paths. Increment owner updates implementation progress; validator owns verdicts.
- Other roles propose changes to the relevant owner.
- Follow orchestrator retry limits; renaming or splitting failed work does not reset its correction count.
- Return a short summary of affected IDs and the next action.
