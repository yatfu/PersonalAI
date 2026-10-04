---
name: gstack-ui
description: Design, implement, or review gstack application interfaces using concrete Tailwind CSS patterns, responsive layouts, accessible controls, and contracted UI states.
---

# Design application interfaces

## Inputs

Read `brief.md`, relevant `architecture.md` and `contracts.md` sections, the current increment, and existing UI components when available. Use [tailwindPatterns.md](references/tailwindPatterns.md) for setup and implementation examples; use the [theme CSS](assets/uiTheme.css) as an adaptable starting point.

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

## Ownership and handoff

- Architect records the UI specification in `architecture.md`: affected routes/components, responsive layouts, tokens, Tailwind setup, state behavior, and verification checks. Reference contracts rather than duplicating their rules.
- Frontend implements the specification in the current increment, coordinating through its assigned communication paths. Styling setup and connecting UI behavior may be separate increments; preserve the one-goal rule and validate each.
- Validator uses this skill to review the rendered interface and records the authoritative verdict through `gstack-validate`.
- Planner may use the skill to refine interface requirements. Shared skill access does not transfer ownership or permit code changes outside the assigned role.
- Return affected IDs, file references, decisions, checks, and limitations. Route scope questions to planner and contract/design changes to architect.
