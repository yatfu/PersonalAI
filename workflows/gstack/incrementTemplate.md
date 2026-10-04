# Increment plan template

The architect writes `increments.md` in the application's output folder using this template. Every increment has exactly one goal: a feature, component, setup capability, or connection between existing pieces. If two goals can be completed and evaluated separately, split them. Multiple files or layers may change to achieve one goal.

Integration is explicit work: connecting a form to an endpoint or an endpoint to persistence is its own increment when built separately. A component can pass its scoped checks before integration, but that does not establish that the complete user journey works.

## Template

```markdown
# Increments — <application or feature>

## Plan

| ID | One goal | Owner | Depends on | Acceptance / contract IDs | Status |
|---|---|---|---|---|---|
| I-1 | <one observable outcome> | <selected role; planner confirms> | <IDs or none> | <AC / C IDs or supporting prerequisite> | pending |

## I-1 — <name>

- Goal: <one outcome>
- Owner: <one selected implementation role, confirmed by planner>
- Collaborators: <selected roles and contributions, or none>
- Communication: <H-IDs and required acknowledgements, or none>
- Shared-file ownership: <single writer per shared file for this increment>
- Included: <work needed for that outcome>
- Excluded: <adjacent work reserved for other increments>
- Dependencies: <previous increments that must pass>
- Contract references: <C IDs or not applicable with reason>
- Required checks: <command/test/manual check → expected outcome>
- Check prerequisites: <tools, services, configuration, and fixtures needed>
- Regression checks: <previous behavior at risk, or none with reason>
- Evidence limits: <what these checks do not establish yet>
- Correction passes used: 0
- Latest validation attempt: <number and validation.md section, or none>
- Revalidation reason: <changed contract/plan/source or none>

## Execution state

- Current increment: <ID or none>
- Final validation: <pending / passed / failed / blocked>
- Final correction passes used: 0
- Latest final validation attempt: <number and validation.md section, or none>
```

Statuses: `pending`, `building`, `validating`, `passed`, `failed`, `blocked`. Architect defines goals, dependencies, and checks. Planner confirms agent assignments and communication paths. Increment owner updates implementation progress. The validator owns validation verdicts. Keep failed attempts and evidence in `validation.md`; do not erase them when an increment later passes.

## State and evidence rules

- Increment owner moves the selected increment to `building`, then `validating`. Validator sets `passed`, `failed`, or `blocked` after checking it.
- A correction returns a failed increment to `building`; it must pass validation before progression. Resume blocked work only when its missing prerequisite is available.
- Planner requests revalidation for changed assignments or communication rules; architect updates affected technical plans and marks increments affected by a contract or plan change `pending` with a reason, including dependent increments whose prior evidence no longer applies. Also reset final validation to `pending`. Only validator can grant a new pass.
- Each increment needs at least one observable goal-specific check and its prerequisites. A build check alone is insufficient for a goal whose behavior requires runtime verification.
- Number validation attempts and record correction counts after each pass. Preserve counts and evidence when resuming a run. Link the latest attempt here; store full results in `validation.md`.
- Revalidation without implementation or planning corrections does not consume a correction pass. Corrections required after a failed recheck do consume one. Follow the orchestrator's limits.

## Example decomposition

1. **I-1: Persist a task record.** Validate data constraints and storage behavior directly.
2. **I-2: Implement the task creation endpoint.** Validate its input, permissions, and output using a clearly identified test double for persistence.
3. **I-3: Connect the endpoint to real persistence.** Validate requests against a test database and verify saved records.
4. **I-4: Build the task entry form.** Validate form interactions using a clearly identified stub submission handler.
5. **I-5: Connect the form to the endpoint.** Validate real submission, error display, and persisted data through the connected application.

These are illustrative boundaries, not mandatory layers for every feature. A small feature may need only one increment. Tests using stubs prove only the isolated behavior; integration increments require real connected boundaries or remain unverified.

## Execution rule

Build one increment, validate it, and advance only after it passes. Corrections to that increment are revalidated before advancing. After all increments pass, perform final application validation, including complete user journeys and the local handoff.
