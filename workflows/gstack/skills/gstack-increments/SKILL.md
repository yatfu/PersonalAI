---
name: gstack-increments
description: Plan ordered gstack increments with exactly one goal each, or maintain their dependencies and progress during implementation and validation.
---

# Plan and track increments

## Inputs

Read `brief.md`, `collaboration.md`, `architecture.md`, and `contracts.md`. Read existing `increments.md` and `validationState.json` when available. Use [incrementTemplate.md](../../incrementTemplate.md) to create or update the plan.

## Procedure

- Give each increment a stable ID, one goal, scope, dependencies, acceptance/contract references, required checks with prerequisites and expected outcomes, regression checks, and evidence limits. Require at least one observable goal-specific check.
- Features, components, setup capabilities, and integration connections may each be goals. Split independently evaluable goals; multiple files or layers may serve one goal.
- Have planner confirm one selected owner per increment, collaborators, communication H-IDs, and shared-file ownership. Keep assignments consistent with `collaboration.md`; implementation cannot start with unresolved ownership.
- Map every planner AC-ID to concrete automated behavioral tests, test writers, and verification increments using [acceptanceTestTemplate.md](../../acceptanceTestTemplate.md). No criterion may be omitted; identify supporting isolated evidence versus complete acceptance coverage.
- Plan integration explicitly when pieces are built separately. Isolated checks do not prove a connected journey. Ensure the full plan covers required criteria.
- Prerequisites must pass before dependent work starts. Validate every increment and correction; advance only with a validator-owned passed verdict.
- Architect creates the executable test plan using [validationGate.md](../../validationGate.md), with criterion mappings, ordered dependencies, concrete test files, commands, and final integrated checks. Keep definitions consistent with `increments.md`. `validationState.json` owns verdicts, attempt history, and correction counts; preserve those fields when revising plans.
- Use the gate before implementation and after every increment. Builders report progress in `handoff.md`; validator runs the suites and links machine attempts from `validation.md`.
- When plans or contracts change, update dependencies and checks while preserving machine history/counts. Record the reason in `validation.md`. Gate fingerprints reject obsolete evidence and require prefix revalidation; only validator grants fresh passes.

## Ownership and handoff

- Architect owns goals, dependencies, and planned checks. Planner owns agent assignments and communication paths. Increment owner reports progress in `handoff.md`; validator owns machine verdicts through the gate.
- Other roles propose changes to the relevant owner.
- Follow orchestrator retry limits; renaming or splitting failed work does not reset its correction count.
- Return a short summary of affected IDs and the next action.
