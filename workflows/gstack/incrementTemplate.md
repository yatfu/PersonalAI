# Increment plan template

The architect writes `increments.md` in the application's output folder using this template. Every increment has exactly one goal: a feature, component, setup capability, or connection between existing pieces. If two goals can be completed and evaluated separately, split them. Multiple files or layers may change to achieve one goal.

Integration is explicit work: connecting a form to an endpoint or an endpoint to persistence is its own increment when built separately. A component can pass its scoped checks before integration, but that does not establish that the complete user journey works.

## Template

```markdown
# Increments — <application or feature>

## Plan
| ID | One goal | Depends on | Acceptance / contract IDs | Status |
|---|---|---|---|---|
| I-1 | <one observable outcome> | <IDs or none> | <AC / C IDs or supporting prerequisite> | pending |

## I-1 — <name>
- Goal: <one outcome>
- Included: <work needed for that outcome>
- Excluded: <adjacent work reserved for other increments>
- Dependencies: <previous increments that must pass>
- Contract references: <C IDs or not applicable with reason>
- Required checks: <command/test/manual check → expected outcome>
- Regression checks: <previous behavior at risk, or none with reason>
- Evidence limits: <what these checks do not establish yet>

## Execution state
- Current increment: <ID or none>
- Final validation: <pending / passed / failed / blocked>
```

Statuses: `pending`, `building`, `validating`, `passed`, `failed`, `blocked`. The architect defines goals, dependencies, and checks. The builder updates implementation progress. The validator owns validation verdicts. Keep failed attempts and evidence in `validation.md`; do not erase them when an increment later passes.

## Example decomposition

1. **I-1: Persist a task record.** Validate data constraints and storage behavior directly.
2. **I-2: Implement the task creation endpoint.** Validate its input, permissions, and output using a clearly identified test double for persistence.
3. **I-3: Connect the endpoint to real persistence.** Validate requests against a test database and verify saved records.
4. **I-4: Build the task entry form.** Validate form interactions using a clearly identified stub submission handler.
5. **I-5: Connect the form to the endpoint.** Validate real submission, error display, and persisted data through the connected application.

These are illustrative boundaries, not mandatory layers for every feature. A small feature may need only one increment. Tests using stubs prove only the isolated behavior; integration increments require real connected boundaries or remain unverified.

## Execution rule

Build one increment, validate it, and advance only after it passes. Corrections to that increment are revalidated before advancing. After all increments pass, perform final application validation, including complete user journeys and the local handoff.
