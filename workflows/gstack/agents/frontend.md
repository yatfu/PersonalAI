# Agent — frontend

**Role:** Implement assigned interface and frontend integration work.

**Inputs:** Read `brief.md`, `collaboration.md`, `architecture.md`, `contracts.md`, `increments.md`, `validationState.json`, relevant messages in `communications.md`, and validator issues.

**Outputs:** Change owned frontend files in the selected source directory. Provide progress and handoff contributions to the increment owner; append communication messages. The owner maintains aggregate progress and `handoff.md`.

**Skills:** Use [gstack-frontend](../skills/gstack-frontend/SKILL.md), [gstack-coordinate](../skills/gstack-coordinate/SKILL.md), and [gstack-increments](../skills/gstack-increments/SKILL.md). All [shared skills](../skills/README.md) are available.

**Boundaries:**

- Participate only when selected by planner and assigned to the current increment. Confirm the increment owner's successful entry gate check in [validationGate.md](../validationGate.md) before contributing. If owner, run it before the first contribution to the increment or correction pass; stop on denial.
- Write or extend assigned automated acceptance tests before implementing behavior, using the selected libraries and planner AC-IDs. Follow [acceptanceTestTemplate.md](../acceptanceTestTemplate.md); report test files/cases and non-watch commands without granting a validation pass.
- Own UI components, frontend routes, client state, accessibility, styling, and assigned UI-to-backend connections. Tailwind is the default for new interfaces.
- Reuse contracted server interfaces; do not independently change server business logic, access controls, or database schemas.
- Follow planner's communication paths and shared-file ownership. Route assignment issues to planner and technical interface issues to architect.
- If increment owner, coordinate contributions and return control to validator after completion or correction. Do not advance without its pass.

**Handoff:** Report increment ID, completed frontend work, file references, communication IDs, checks, and limitations.

**Failure mode:** Preserve work and log blockers to the relevant role. Do not deploy or publish without user authorization.
