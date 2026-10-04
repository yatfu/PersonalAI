# Acceptance criteria and test coverage

## Planner creates the criteria

Planner explicitly writes this section in `brief.md` before technical design or implementation. Translate user requirements into observable outcomes; do not assume builders will invent the acceptance criteria. Include required failure, permission, and persistence behavior. Keep IDs stable when revising scope and record removed criteria explicitly.

```markdown
## Acceptance criteria

| ID | Given / preconditions | When / action | Then / expected result |
|---|---|---|---|
| AC-1 | A signed-in user has entered a valid task title | They submit the form and refresh | The saved task is displayed and belongs to that user |
| AC-2 | The task title is blank | The user submits | An error is shown and no task is stored |
```

Use plain `AC-<positive integer>` IDs in the first column. Architect and builders reference these IDs; only planner can change the required outcomes. Ambiguous or missing criteria return to planner before dependent work.

## Architect maps criteria to tests

Include an acceptance-test matrix in `increments.md`. Every planner criterion must have automated behavioral coverage, an assigned test writer, and an increment where the criterion will be fully verified. A criterion may span several increments; isolated tests are supporting evidence until its complete behavior is tested.

```markdown
| Criterion | Test writer | Test file / case | Library | Verification increment | Evidence scope |
|---|---|---|---|---|---|
| AC-1 | frontend, with backend/database fixtures | tests/taskCreation.spec.ts / create and refresh | Playwright | I-5 | Integrated UI, API, and test database |
| AC-2 | backend; frontend covers the error display | tests/taskValidation.test.ts / reject blank title | Vitest | I-2, I-5 | Server behavior first, then connected UI |
```

Select compatible libraries for the actual stack and preserve suitable existing tools. Examples: [Vitest](https://vitest.dev/guide/) for JavaScript/TypeScript behavior, [Playwright](https://playwright.dev/docs/test-assertions) for browser journeys, and [pytest](https://docs.pytest.org/en/stable/) for Python. These are examples, not required technologies. Record versions, configuration, fixtures, test-database setup, and non-watch commands.

## Builders write tests before implementation

- Each assigned implementation role creates or extends its current increment's acceptance tests before implementing its behavior. Reuse relevant existing tests. Test writing belongs to that increment's one goal; do not implement future increments to satisfy their tests early.
- Put AC IDs in test names and map concrete test files/cases to criteria. Test observable outcomes through the appropriate public boundary, including relevant failure paths. A build, type check, snapshot alone, or assertion about a mock call does not establish an acceptance criterion.
- Frontend owns interface and assigned browser integration tests; backend owns server behavior and assigned persistence-integration tests; database owns schema, migration, query, and integrity tests. Respect the planner's ownership assignments for shared fixtures and files.
- Run the new tests before implementation and record the expected behavioral failure when practical. A missing dependency or broken test setup is a blocker, not proof of a useful failing test.
- Use isolated doubles only where the increment explicitly allows them. Tests for a connected journey must use the required real boundaries and designated test environment.
- Keep commands finite and non-interactive. Required suites must fail on failed tests and must not treat skipped, todo, or zero collected acceptance tests as passing coverage. Manual checks can supplement automated tests, not replace required criterion coverage.

## Validator checks the coverage

Validator reviews assertions against planner's outcomes, verifies that mapped cases actually run, and independently executes the required suites. Builders' self-checks cannot grant a pass. Validate current increment behavior and prior regressions after every increment; future criteria remain pending. Final validation must execute automated coverage for every criterion, including complete user journeys, and record remaining manual checks and limitations.
