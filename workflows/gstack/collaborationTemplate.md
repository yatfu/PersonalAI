# Agent communication contract

Planner writes `collaboration.md` in the application document directory. This contract selects the implementation team, assigns ownership, and defines how agents exchange work. Architect supplies technical details in `contracts.md`; communication entries reference those details rather than inventing or duplicating them.

## Selection rules

- Select **frontend** for interface, client state, frontend routes, or frontend integration changes.
- Select **backend** for server behavior, authentication, authorization, business logic, APIs, or service integration changes.
- Select **database** for schemas, migrations, indexes, persistence adapters, queries, or data-integrity changes.
- Select only roles needed for changed behavior. Reading or reusing an existing API or schema does not automatically require its implementation agent.
- Base assignments on responsibility rather than folder names. For example, a server-rendered page can belong to frontend while authorization belongs to backend.
- Record who must communicate and why. Only selected implementation roles participate in implementation handoffs. A task involving one role may need no such handoff.

## Template

```markdown
# Collaboration — <application or feature>

## Implementation team

| Agent | Required? | Reason | Owned responsibilities / files |
|---|---|---|---|
| frontend | <yes/no> | <affected behavior or reason to omit> | <scope; exact files when known> |
| backend | <yes/no> | <affected behavior or reason to omit> | <scope; exact files when known> |
| database | <yes/no> | <affected behavior or reason to omit> | <scope; exact files when known> |

## Communication paths

| Handoff ID | Sender → receiver | Purpose | Technical contract IDs | Used by increments |
|---|---|---|---|---|
| H-1 | <selected role → selected role> | <specific dependency> | <C IDs or pending architect definition> | <I IDs once planned> |

## H-1 — <handoff name>

- Trigger: <when the sender requests or delivers something>
- Required artifact: <source file/symbol, schema, or document section>
- Payload requirements: <which fields of the common message format are needed>
- Acceptance: <what the receiver checks before acknowledging the handoff>
- Blocking conditions: <missing or incompatible information that prevents use>
- Change handling: <affected consumers; who must be notified>

## Increment assignments

| Increment | One goal | Owner | Collaborators | Handoff IDs | Shared-file owner |
|---|---|---|---|---|---|
| I-1 | <goal from increments.md> | <one selected role> | <selected roles or none> | <H IDs or none> | <owner for any shared file> |

## Decisions and unresolved questions

- <decision, reason, affected roles/IDs, and blocking status>
```

## Common message format

Use `communications.md` in the same document directory as an append-only log. Each message has:

| Field | Required content |
|---|---|
| `messageId` | Unique stable ID, such as M-1. |
| `incrementId` | Current increment, or `planning` before implementation. |
| `handoffId` | H-ID from `collaboration.md`. |
| `from` / `to` | Selected sender and receiver roles. |
| `kind` | `request`, `ready`, `acknowledged`, `blocked`, or `changeRequest`. |
| `summary` | Short description of the request, delivery, or issue. |
| `artifactRefs` | Relevant paths and symbols/sections, plus commit or revision reference when available. |
| `contractIds` | Relevant C-IDs, or an explicit note that architect must define them. |
| `replyTo` | Earlier message ID, or `none` for a new thread. |
| `nextAction` | Responsible role and required action, or `none`. |

The sender → receiver path identifies the delivery direction. Requests, acknowledgements, blockers, and change requests may travel in either direction between those two roles; deliveries use the declared direction.

Write artifacts first, then log references and a short summary. A receiver appends its acknowledgement after checking the delivery; it does not edit the sender's message. Acknowledgement confirms a usable handoff, not a validation pass. Record blocked or incompatible deliveries explicitly.

## Integration and changes

- Frontend normally owns connecting UI to backend; backend normally owns connecting server behavior to persistence. Planner can choose a different selected owner and record why.
- Every increment has exactly one owner, even when several roles contribute to its single goal. Independent goals must be separate increments.
- Shared files have one writer for the current increment. Execute contributions sequentially by default; other roles propose changes to the assigned writer.
- Planner confirms assignments after architect drafts increments. Keep owner, collaborators, and handoff IDs consistent in `collaboration.md` and `increments.md`.
- Team or communication changes return to planner; technical contract changes return to architect. Update affected plans and invalidate obsolete validation evidence before proceeding.

## Examples

- **Change button styling:** frontend only; no implementation-agent handoff is needed.
- **Add UI to an existing endpoint:** frontend only if the existing endpoint already satisfies the feature. Select backend if its behavior must change.
- **Create a persisted form submission:** frontend, backend, and database. Define frontend ↔ backend communication for request/response behavior and backend ↔ database communication for persistence. No direct frontend ↔ database path is needed unless the architecture actually uses one.
- **Add an index without changing callers:** database only; verify existing query behavior and the index's effect.
