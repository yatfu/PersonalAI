# Increment plan template

The architect writes `increments.md` in the application's output folder using this template. Every increment has exactly one goal: a feature, component, setup capability, or connection between existing pieces. If two goals can be completed and evaluated separately, split them. Multiple files or layers may change to achieve one goal.

Integration is explicit work: connecting a form to an endpoint or an endpoint to persistence is its own increment when built separately. A component can pass its scoped checks before integration, but that does not establish that the complete user journey works.

## Template

```markdown
# Increments — <application or feature>

## Plan

| ID | One goal | Owner | Depends on | Acceptance / contract IDs |
|---|---|---|---|---|
| I-1 | <one observable outcome> | <selected role; planner confirms> | <IDs or none> | <AC / C IDs or supporting prerequisite> |

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
- Acceptance tests: <AC IDs → test files/cases, library, fixtures, and evidence scope>
- Required checks: <automated test command and supplemental manual check → expected outcome>
- Check prerequisites: <tools, services, configuration, and fixtures needed>
- Regression checks: <previous behavior at risk, or none with reason>
- Evidence limits: <what these checks do not establish yet>
- Execution evidence: <I-1 in validationState.json; related validation.md sections>

## Execution record

- Machine record: validationState.json
- Gate instructions: workflows/gstack/validationGate.md
```

Architect defines goals, dependencies, and checks, and creates `validationState.json` using [validationGate.md](validationGate.md). Planner confirms assignments. Increment owner reports building/ready progress in `handoff.md`; validator records machine verdicts (`pending`, `passed`, `failed`, `blocked`), attempt history, and correction counts through the gate. Keep narrative findings in `validation.md`. The JSON record is authoritative; do not duplicate live statuses or counts in this planning document.

## State and evidence rules

- Before starting or correcting an increment, run the gate's read-only `check --increment` command and stop on any nonzero exit. All earlier increments need fresh passing evidence.
- After each increment, validator reviews assertions and handoffs, then runs `validate --through <ID> --reviewed`. This rechecks the earlier prefix before recording the current verdict. Only a passing run permits progression.
- Planner/architect update plans when scope, assignments, or contracts change. Gate fingerprints invalidate old evidence automatically; preserve history and counts when updating JSON definitions. Revalidate before advancing. Only validator can grant a fresh pass.
- Each increment needs at least one observable goal-specific check and its prerequisites. A build check alone is insufficient for a goal whose behavior requires runtime verification.
- The gate numbers attempts and saves source/planning fingerprints, command results, and immutable log references. Validator links those attempts from `validation.md`; preserve history when resuming.
- Revalidation without implementation or planning corrections does not consume a correction pass. Corrections required after a failed recheck do consume one. Follow the orchestrator's limits.

## Example decomposition

1. **I-1: Persist a task record.** Validate data constraints and storage behavior directly.
2. **I-2: Implement the task creation endpoint.** Validate its input, permissions, and output using a clearly identified test double for persistence.
3. **I-3: Connect the endpoint to real persistence.** Validate requests against a test database and verify saved records.
4. **I-4: Build the task entry form.** Validate form interactions using a clearly identified stub submission handler.
5. **I-5: Connect the form to the endpoint.** Validate real submission, error display, and persisted data through the connected application.

These are illustrative boundaries, not mandatory layers for every feature. A small feature may need only one increment. Tests using stubs prove only the isolated behavior; integration increments require real connected boundaries or remain unverified.

## Acceptance-test matrix

Use [acceptanceTestTemplate.md](acceptanceTestTemplate.md) to map every planner criterion to automated tests, test writers, and the increment that verifies its complete behavior. Builders write assigned tests before implementation; validator independently runs them after every increment.

## Execution rule

Build one increment, validate it, and advance only after it passes. Corrections to that increment are revalidated before advancing. After all increments pass, perform final application validation, including complete user journeys and the local handoff.
