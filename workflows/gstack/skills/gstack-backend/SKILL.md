---
name: gstack-backend
description: Design, implement, or review gstack server behavior, APIs or actions, authentication, authorization, business logic, and service or persistence connections.
---

# Backend design and implementation

## Inputs and modes

Read `brief.md`, relevant architecture and technical contracts, planner's role boundaries and handoff paths, and existing server interfaces. During implementation, identify the current increment and read [shared implementation rules](../references/implementation.md) before contributing.

- **Design:** Architect records server structure and integration decisions in `architecture.md`, with precise behavior in `contracts.md`. Propose required role or communication changes to planner; do not change application code.
- **Implement:** Backend changes only assigned server behavior, tests, and integration files within the current increment. Follow the entry gate, acceptance-test-first procedure, correction limits, and handoffs in the shared rules.
- **Review:** Validator uses this guidance to assess server behavior and evidence through `gstack-validate`; it does not modify code or grant a pass merely by inspecting a contract.

## Backend design

- Use the selected framework and existing conventions. Describe the actual boundary: endpoint, server action, event consumer, or service call. Do not introduce an HTTP API or extra service layer just to fit a template.
- For each affected operation, specify trusted identity, permitted users/resources, input rules, success and error shapes, side effects, and observable acceptance checks. Reference C-IDs rather than copying competing definitions into architecture or messages.
- Separate transport concerns from business rules where the application's structure supports it. Identify database-owned queries/adapters and the backend code that consumes them; record corresponding planner H-IDs.
- Define external-service configuration and unavailable-service behavior. Record timeouts, safe retry conditions, and duplicate-request handling when required by the operation. Coordinate atomicity and transaction requirements with database; do not assume separate writes succeed together.

## Backend implementation

- Write assigned behavioral tests before implementation using libraries appropriate to the chosen stack. Include AC-IDs in cases and use the actual public server boundary for API/action criteria. Pure business-rule tests are supporting evidence when a criterion also requires permissions, transport behavior, or persistence.
- Validate input at server boundaries and use only validated fields. Derive user identity and ownership from trusted server context; authorize each affected resource or action. Client validation and caller-provided owner IDs are not authorization.
- Implement business rules and contracted error/result behavior. Return success only after the required side effect completes. Distinguish invalid input, missing identity, forbidden access, missing resources, and dependency failures according to the contract; do not invent error codes.
- Consume agreed persistence interfaces. Database owns schemas, migrations, queries, and adapters; backend owns the business decisions and the designated server-to-persistence connection. Request interface changes through architect and exchange artifacts through planner's handoff contract.
- Connect real services or persistence in assigned integration increments. Keep test doubles explicit until integration is required; do not silently replace unavailable required services with a success stub.
- Keep server configuration private, provide placeholder environment examples, and log actionable failures without exposing credentials or sensitive payloads. Apply retry or idempotency behavior only when it preserves the contracted operation.

## Verification and handoff

- Cover contracted valid/invalid input, required authentication and resource permissions, relevant success/failure responses, and side effects. Include ownership isolation and duplicate/failure behavior when required by planner's criteria.
- Integration evidence must observe the real required boundary, such as a request followed by reading the saved record from the designated test database. A mock receiving a write call does not prove persistence. Coordinate fixtures with database and response/error behavior with frontend.
- Report server files, test cases/commands, AC/C/H IDs, environment/service prerequisites, checks, limitations, and blockers to the increment owner. Use [shared implementation rules](../references/implementation.md) for aggregate handoff and validator return.
- Architect owns technical design changes; planner owns scope and assignments; validator owns authoritative gate verdicts. These rules apply even though every agent can access this skill.
