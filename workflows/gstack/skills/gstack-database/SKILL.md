---
name: gstack-database
description: Design, implement, or review gstack data models, schemas, migrations, constraints, indexes, queries, transactions, persistence adapters, and test fixtures.
---

# Database design and implementation

## Inputs and modes

Read `brief.md`, relevant architecture and technical contracts, planner's responsibilities and handoff paths, and existing schemas, migrations, queries, and persistence interfaces. During implementation, identify the current increment and read [shared implementation rules](../references/implementation.md) before contributing.

- **Design:** Architect records storage decisions and migration/setup strategy in `architecture.md`, with precise data and interface rules in `contracts.md`. Propose required team or communication changes to planner; do not modify application code or data.
- **Implement:** Database changes assigned persistence structures, adapters, fixtures, and tests for the current increment. Follow the entry gate, acceptance-test-first procedure, correction limits, and handoffs in the shared rules.
- **Review:** Validator checks schema, migration, query, and integrity evidence through `gstack-validate`. Inspecting a schema or seeing a mock call does not prove working persistence.

## Database design

- Use the chosen engine and existing driver or ORM conventions. Define entities, identifiers, types, defaults, required fields, relationships, ownership, and uniqueness using the actual persistence model. Do not add a new database or ORM just to fit this skill.
- Distinguish application validation from storage-enforced integrity. Specify constraints and deletion/update behavior where required; reference technical C-IDs rather than duplicating the data model in handoff messages.
- Define persistence operations, returned shapes, error behavior, and transaction boundaries needed by consumers. Backend owns business rules and server authorization; database implements assigned storage constraints and database access policies where the architecture requires them.
- Specify migrations/backfills for existing data, compatibility with current callers, and recovery behavior. Identify prerequisites and any destructive operations before implementation. Choose indexes from actual access patterns and required performance outcomes rather than adding speculative indexes.

## Database implementation

- Write assigned schema, migration, query, and persistence tests before implementing behavior. Use compatible libraries and concrete AC-IDs; validate against a designated test database or storage environment when real persistence is required.
- Implement contracted schemas, migrations, indexes, queries, and adapters. Use the selected client's parameterization for values; do not construct queries from untrusted string fragments. Preserve returned shapes expected by consumers.
- Enforce assigned uniqueness, relationship, ownership, and data-integrity rules at the available storage boundary. Coordinate atomic multi-write operations and failure behavior with backend; use transactions where the contracted outcome requires them and the engine supports them.
- Expose agreed persistence interfaces and exchange artifacts through planner H-IDs. Consumers are often backend, but follow the actual architecture. Do not independently change server APIs, business rules, or frontend behavior.
- Apply and test migrations in the designated test environment. Check both a fresh setup and existing-data transition when relevant. Do not perform unapproved destructive operations against live or user data; report required authorization or unavailable prerequisites as blockers.
- Provide schema/setup commands, placeholder connection configuration, fixtures, and supported recovery instructions. Keep fixture data deterministic and isolated; clean up test-owned data without deleting unrelated records.

## Verification and handoff

- Observe stored/read values, defaults, constraints, updates, deletion behavior, and ownership isolation where contracted. Test invalid writes and transaction failure/rollback behavior required by acceptance criteria.
- For migration goals, verify representative existing records survive the transition with expected shapes. For index/performance goals, record the relevant query-plan or timing evidence against the planned outcome; a successful schema build alone is insufficient.
- Use real persistence for integration evidence. Doubles may support earlier isolated increments, but cannot establish migrations, constraints, transaction behavior, or durability. Coordinate connected tests and fixtures with the assigned consumer role.
- Report changed schemas/migrations/queries, test cases/commands, AC/C/H IDs, test-environment prerequisites, compatibility/recovery notes, checks, and blockers to the owner using [shared implementation rules](../references/implementation.md).
- Architect owns technical design changes; planner owns scope and assignments; validator owns authoritative gate verdicts. Shared skill access does not transfer these responsibilities.
