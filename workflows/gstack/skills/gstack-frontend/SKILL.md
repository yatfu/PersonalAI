---
name: gstack-frontend
description: Design, implement, or review gstack frontend routes, components, client state, server connections, and accessible interfaces with Tailwind styling defaults.
---

# Frontend design and implementation

## Inputs

Read `brief.md`, relevant `architecture.md` and `contracts.md` sections, the current increment when implementing, and existing UI components when available. Use [tailwindPatterns.md](references/tailwindPatterns.md) for setup and implementation examples; use the [theme CSS](assets/uiTheme.css) as an adaptable starting point.

## Use the appropriate mode

- **Design:** Architect specifies routes, components, client/server boundaries, interaction states, and UI details in `architecture.md`, referencing technical C-IDs and communication H-IDs. Planner may refine user requirements. Do not modify application code in design mode.
- **Implement:** Frontend reads and follows [shared implementation rules](../references/implementation.md) before contributing to the current increment. These cover entry gates, acceptance tests before behavior, contracts, handoffs, and corrections.
- **Review:** Validator checks the actual interface and test evidence using `gstack-validate`. Skill access does not grant another role's output ownership or a validation pass.

## Styling default

- Use Tailwind CSS for new gstack interfaces unless the user specifies another approach. The examples target Tailwind v4; verify the installed version and framework integration before applying them.
- For an existing application, reuse its styling system unless a change is requested. If it already uses Tailwind, reuse its version, tokens, and components; adding a feature does not imply upgrading or migrating styling.
- Use utilities for layout and component styles. Keep custom CSS for theme tokens, base rules, or behavior that utilities cannot express clearly. Reuse repeated patterns through framework components.

## Procedure

1. Map each affected page or component to a user goal and its acceptance or contract IDs. Identify the primary action, navigation, content order, and required UI states.
2. Define a small set of semantic colors, spacing, typography, borders, and focus styles. Adapt the supplied CSS to the application's identity; it is a starter, not a required visual theme.
3. Specify layouts at narrow and wide widths with concrete classes, such as `grid grid-cols-1 gap-6 lg:grid-cols-2`. Define overflow behavior for tables, code, and long content. Start with unprefixed mobile styles, then add breakpoint overrides.
4. Use semantic elements and visible labels. Specify keyboard focus, error associations, disabled and pending behavior, and status announcements. Use an established accessible component for complex interactions when available; styling does not implement keyboard or focus behavior.
5. Define loading, empty, success, error, and disabled states where the contract requires them. Tailwind classes change presentation; frontend must implement the actual state and event logic in the designated increment.
6. Verify the production build generates the needed classes. Use complete class strings rather than interpolated fragments. Check narrow/wide layouts, keyboard operation, focus visibility, contrast, and required states in the rendered interface. Record unrun checks explicitly.

## Frontend implementation

- Preserve the selected framework and existing route/component conventions. Use the architecture to decide what renders on the server and what needs client state; server business logic and authorization remain backend responsibilities.
- Implement navigation, forms, client state, and required loading/empty/success/error behavior. Prevent duplicate submissions and preserve user input on failure according to the contract. Apply optimistic updates only when contracted reconciliation and failure behavior are defined.
- Connect UI to the contracted endpoint, action, or local interface in its designated integration increment. Use exact input/output shapes and error codes; missing fields or incompatible responses return to architect rather than being silently guessed.
- Reuse shared types or schemas when available. Client validation improves feedback but does not replace backend validation or access controls. Never put server secrets in client code or public configuration.
- Write assigned component/interaction tests and connected browser journeys using the chosen libraries. Include planner AC-IDs, narrow/wide layouts, keyboard operation, required states, and real boundaries where the criterion needs them. Isolated UI tests cannot establish persistence or server permissions.

## Ownership and handoff

- Architect records the UI specification in `architecture.md`: affected routes/components, responsive layouts, tokens, Tailwind setup, state behavior, and verification checks. Reference contracts rather than duplicating their rules.
- Frontend implements the specification in the current increment, coordinating through its assigned communication paths. Styling setup and connecting UI behavior may be separate increments; preserve the one-goal rule and validate each.
- Validator uses this skill to review the rendered interface and records the authoritative verdict through `gstack-validate`.
- Planner may use the skill to refine interface requirements. Shared skill access does not transfer ownership or permit code changes outside the assigned role.
- Return affected IDs, file references, decisions, checks, and limitations. Route scope questions to planner and contract/design changes to architect.
