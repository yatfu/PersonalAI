---
name: gstack-validate
description: Validate a gstack increment or complete application against acceptance criteria and contracts, recording evidence, regressions, verdicts, and blockers.
---

# gstack-validate

Read the brief, architecture, contracts, increment plan, handoff, and affected source. Select increment, correction, or final application validation.

- Validate immediately after every increment and correction. Check the one goal, required checks, contracts, and regressions in prior behavior; identify unrelated bundled goals.
- Run build, lint, type, and behavior checks appropriate to the stack and planned goal. Record commands and expected/actual outcomes; identify unrun checks. Inspection alone does not prove runtime success.
- Check that setup instructions and configuration examples match the implementation.
- Check contracted shapes, permissions, errors, UI states, and persistence against the brief and implementation. Map evidence to increment, acceptance, and contract IDs.
- Evaluate components within scope. Label stub-based evidence and defer integrated claims until real connections are verified. Future criteria remain pending during intermediate checks.
- Preserve each numbered attempt and verdict in `validation.md`; update its reference and correction count in `increments.md`. Follow orchestrator limits without resetting counts on resume. Required checks must pass for advancement; defects are failed and unavailable prerequisites are blocked. If both occur, record both and do not advance.
- After all increments pass, check complete journeys, relevant failure/access cases, full criterion/contract coverage, and reproducible setup. Record a separate final verdict.
- Route scope defects to planner, contract/design defects to architect, and implementation defects to builder with IDs and file references. Recheck affected behavior and necessary regressions after correction.
- When source changes affect a previously passed increment, invalidate its pass and dependent evidence, reset final validation to pending, and require revalidation. Prior evidence remains historical rather than proof of the current version.

Only validator records authoritative verdicts in `validation.md` and `increments.md`. Other roles may run self-checks and report evidence but cannot grant a pass. Do not modify application code or weaken contracts/criteria to make validation pass. Return a short verdict and report reference.
