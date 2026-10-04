---
name: gstack-coordinate
description: Select gstack implementation agents and define or follow their communication contract, ownership assignments, and file-based handoffs.
---

# Coordinate implementation agents

## Inputs

Read the request, `brief.md`, existing implementation, and any available architecture, application contracts, and increment plan. Use [collaborationTemplate.md](../../collaborationTemplate.md) for team decisions and communication requirements.

## Procedure

- Determine whether frontend, backend, and database are each required. Record a reason for selecting or omitting every role; select only roles whose responsibilities need changes.
- Identify communication paths between selected roles from actual dependencies. Define stable H-IDs, triggers, artifact references, payload requirements, receiver acceptance checks, blockers, and change handling.
- Keep technical schemas and application behavior in architect-owned `contracts.md`; reference C-IDs from the communication contract. Mark details awaiting architect as unresolved rather than inventing an interface.
- After architecture and increments are drafted, assign one selected owner per increment, collaborators, handoff IDs, and shared-file ownership. Default UI-to-backend integration to frontend and backend-to-persistence integration to backend. Explain deviations.
- Confirm `collaboration.md` and `increments.md` assignments agree and all required communication paths are covered before implementation starts. Missing or incompatible handoffs block dependent work.
- During implementation, write artifacts first and append the common message format to `communications.md`. Receiver acknowledges usable deliveries or reports blockers. Keep messages short and link evidence rather than copying artifacts.
- Keep contributions within the current increment's single goal. Serialize shared-file edits through the assigned writer. Handoff acknowledgement and self-checks do not replace validator's pass.
- Route assignment or communication changes to planner and technical interface changes to architect. Update plans and invalidate affected evidence through `gstack-increments` before continuing.

## Ownership and handoff

- Planner writes or revises `collaboration.md` and owns agent assignments in `increments.md`.
- Architect drafts technical contracts and increment goals, then requests planner confirmation of assignments.
- Selected implementation agents append their own messages to `communications.md` and follow assigned ownership. Validator inspects handoff evidence but does not implement code.
- Return selected roles, required communication paths, affected IDs, artifact references, and unresolved decisions. All agents may use this skill without taking another role's ownership.
