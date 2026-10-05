---
name: gstack-validate
description: Validate a gstack increment or complete application against acceptance criteria and contracts, recording evidence, regressions, verdicts, and blockers.
---

# Validate application behavior

## Inputs

Read `brief.md`, `collaboration.md`, relevant `communications.md` entries, `architecture.md`, `contracts.md`, `increments.md`, `validationState.json`, `handoff.md`, and affected source. Select increment validation, correction validation, or final application validation.

## Procedure

- Validate immediately after every increment and correction. Check the one goal, required checks, contracts, and regressions in prior behavior; identify unrelated bundled goals.
- Review the acceptance-test matrix and assertions against planner criteria using [acceptanceTestTemplate.md](../../acceptanceTestTemplate.md). Independently run the mapped cases; reject missing, skipped, todo, or zero-collected required tests. Future criteria remain pending, and final validation needs automated behavioral coverage of every AC-ID.
- Run build, lint, type, and behavior checks appropriate to the stack and planned goal. Record commands and expected/actual outcomes; identify unrun checks. Inspection alone does not prove runtime success.
- Verify selected roles, ownership, and required handoff acknowledgements against `collaboration.md`. Acknowledgements alone are not proof that integration works.
- Check that setup instructions and configuration examples match the implementation.
- For interface increments, use `gstack-frontend` to check generated styles, responsive layouts, keyboard focus, accessible controls, and contracted UI states. Record browser evidence separately from compilation results.
- For server increments, use `gstack-backend` in review mode to check boundary validation, permissions, business outcomes, errors, and real integration evidence.
- For persistence increments, use `gstack-database` in review mode to check stored data, constraints, migrations, queries, transaction behavior, and test-environment evidence.
- Check contracted shapes, permissions, errors, UI states, and persistence against the brief and implementation. Map evidence to increment, acceptance, and contract IDs.
- Evaluate components within scope. Label stub-based evidence and defer integrated claims until real connections are verified. Future criteria remain pending during intermediate checks.
- After reviewing criteria, collection, handoffs, and supplemental checks, use [validationGate.md](../../validationGate.md) to run `validate --through <ID> --reviewed`. The gate records attempts, fingerprints, verdicts, and logs in `validationState.json`. Link each attempt and log from `validation.md`; use `--correction <ID>` for fixes. Follow orchestrator limits without resetting counts on resume. Required checks must pass for advancement; defects are failed and unavailable prerequisites are blocked. If both occur, record both and do not advance.
- After all increments pass, check complete journeys, relevant failure/access cases, full criterion/contract coverage, and reproducible setup. Run `validate --final --reviewed`, then `check --final` before declaring completion. Include `--correction final` and affected increment IDs when final failures required fixes.
- Route scope, assignment, and communication defects to planner; technical contract or design defects to architect; and implementation defects to the increment owner and affected role. Include IDs and file references. Recheck affected behavior and necessary regressions after correction.
- Source changes make prior fingerprints stale; rerun the earlier prefix and final checks as required by the gate. Preserve all old attempts as historical evidence rather than proof of the current version.

## Ownership and handoff

- Only validator runs authoritative validation and records verdicts through the gate. `validationState.json` owns machine results; `validation.md` owns narrative review and manual evidence.
- Other roles may run self-checks and report evidence; they cannot grant a pass.
- Do not modify application code or weaken contracts or acceptance criteria to make validation pass.
- Return a short verdict with a report reference and remaining issues.
