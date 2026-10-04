# Shared gstack skills

Agents own responsibilities and outputs. Skills provide reusable procedures. Every gstack agent can access every skill.

| Skill | Procedure | Usual owner |
|---|---|---|
| [gstack-plan](gstack-plan/SKILL.md) | Scope, journeys, acceptance criteria | Planner |
| [gstack-design](gstack-design/SKILL.md) | Architecture and stack selection | Architect |
| [gstack-ui](gstack-ui/SKILL.md) | UI design and concrete Tailwind styling | Architect, builder, validator |
| [gstack-contracts](gstack-contracts/SKILL.md) | Data and interface contracts | Architect |
| [gstack-increments](gstack-increments/SKILL.md) | One-goal plans and progress | Architect, builder, validator |
| [gstack-build](gstack-build/SKILL.md) | Implement one increment | Builder |
| [gstack-validate](gstack-validate/SKILL.md) | Evidence and validation | Validator |

## Using a skill

Read the selected `SKILL.md`, supply the relevant files and context, and follow its procedure. Load referenced templates only when needed. These are instructions for an AI session or runner; a name alone does not execute a call.

Repository `.agents/skills/` discovery links point to these folders, keeping one maintained copy. Codex can discover them or receive explicit requests such as `$gstack-contracts`. Other runners can load the files directly.

## Ownership

Shared access does not change stage order or authority. The builder may inspect contracts or run self-checks. The architect owns contract changes; the validator owns verdicts that permit advancement. The validator may use build guidance to diagnose defects but does not modify application code.

Agent files define inputs, outputs, boundaries, and escalation rules. Skill files describe procedures. The [orchestrator](../orchestrator.md) retains sequence, gates, and retries. Skill outputs go into the application's output folder, never into skill definitions.
