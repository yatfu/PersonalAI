# Application contract template

A contract defines the behavior shared by the UI, backend, and persistence layer. The architect fills this template into `contracts.md` in the application's output folder. The builder implements it; the validator checks it against the brief and actual behavior.

## Sizing and ownership

- For a small feature, one operation and a few rules may be enough. For a larger feature, repeat the operation section for each affected boundary.
- Describe only affected behavior. Reference existing types, schemas, and interfaces by file path and symbol where possible; avoid duplicating their definitions. Record intended changes explicitly.
- Use the application's actual mechanism: HTTP endpoints, server actions, events, or local calls. Do not introduce an API layer just to fill this template.
- Mark irrelevant sections `Not applicable` with a short reason. Label unresolved decisions `Blocking` or `Non-blocking`; only dependent implementation waits for a blocking decision.
- The architect owns contract decisions. The builder may choose internal implementation details that preserve the contract. Changes to externally observable behavior return to the architect; changes to required behavior also return to the planner. Update documents before implementing the affected change. Routine compatible decisions do not need user approval.

## Template

```markdown
# Contracts — <application or feature>

## Scope

- Source brief and acceptance criteria: <path; IDs such as AC-1>
- Existing contracts preserved: <paths and symbols, or none>
- Assumptions and unresolved decisions: <decision, blocking status, affected operation>

## Data

| Entity / field | Type | Required / default | Rules |
|---|---|---|---|
| <field> | <type> | <required or default> | <constraints> |

- Relationships and ownership: <foreign keys, access boundaries>
- Persistence: <storage, when writes occur, durability expectations>
- Existing data: <migration/backfill behavior, or not applicable>

## Operation C-1 — <name>

- Acceptance criteria: <AC IDs>
- Caller and boundary: <UI → server, server → external service, etc.>
- Interface: <method/path, action signature, event name, or existing symbol>
- Authentication and authorization: <who can invoke it and access affected data>
- Input: <exact fields, types, required/optional values, and validation>
- Success: <response shape, status/result, and side effects>
- Failure: <trigger → status/error code and shape; retry behavior if relevant>
- Example: <valid input and expected output; representative invalid input>
- UI behavior: <trigger; loading, success, empty, and error states as applicable>
- Verification: <observable success and failure checks tied to AC IDs>

## Compatibility and integrations

- Compatibility: <existing callers or data affected; intended preservation/change>
- External dependencies: <interface/configuration references; unavailable-service behavior>

## Required verification

| Criterion / contract | Check | Expected result |
|---|---|---|
| <AC-1 / C-1> | <test, command, or manual journey> | <observable outcome> |

## Decision log

- <decision and reason; affected contract IDs; superseded behavior if any>
```

## Example — creating a task

Illustrative choices for an authenticated HTTP application; these defaults are not requirements for every app.

- **AC-1:** A signed-in user creates a task and sees it after refreshing.
- **Data:** `id` is a server-generated UUID; `title` is a trimmed string of 1–120 characters; `completed` defaults to `false`; `ownerId` comes from the authenticated session; `createdAt` is a server-generated UTC timestamp.
- **C-1 interface:** `POST /api/tasks`, JSON input `{ "title": "Buy milk" }`.
- **Success:** Return `201` with `{ "task": { "id": "<uuid>", "title": "Buy milk", "completed": false, "createdAt": "<UTC timestamp>" } }` after the database write succeeds. The task belongs to the signed-in user.
- **Failure:** Missing/blank/overlong title returns `400` with `{ "error": { "code": "INVALID_TITLE", "message": "Title must contain 1–120 characters." } }`. Missing session returns `401` with the same error envelope and code `UNAUTHENTICATED`. A failed database write returns `500` with code `SAVE_FAILED` and a generic message.
- **UI:** Disable submission while pending. On success, display the returned task and clear the form. On failure, retain the title and show the error; do not display a successfully saved task.
- **Checks:** Create and refresh to confirm persistence; submit a blank title and confirm no write; attempt creation without a session; verify one user cannot retrieve another user's tasks through the existing list contract.

This contract gives all layers the same answers: what to send, what to store, what to return, and what the user should see.
