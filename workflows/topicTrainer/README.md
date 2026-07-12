# topicTrainer

Give it a topic, it produces a validated, ordered curriculum and a single-page HTML learning resource covering it.

## When to run it

Whenever you want a structured learning path for a topic, instead of researching and sequencing it yourself.

## Inputs

- `topic` (required) — what to learn
- `currentLevel` (optional) — beginner/some background/etc., defaults to beginner
- `focus` (optional) — e.g. "practical/build-oriented" vs "theory-first"

## Output

`outputs/topicTrainer/<topicSlug>/`
- `research.md` — validated research brief
- `curriculum.md` — ordered modules with objectives and milestones
- `resource.html` — a single self-contained page: one accordion section per module, with visualizations where they help

## Agents

| Agent | Role |
|---|---|
| [`agents/researchAgent.md`](agents/researchAgent.md) | Maps the topic: subtopics, dependencies, key concepts, common pitfalls |
| [`agents/validationAgent.md`](agents/validationAgent.md) | Checks the research for accuracy, gaps, and bad sequencing before anything is built on top of it |
| [`agents/curriculumPlanner.md`](agents/curriculumPlanner.md) | Turns validated research into ordered modules with objectives and milestones |
| [`agents/resourceBuilder.md`](agents/resourceBuilder.md) | Turns the curriculum + research into a single accordion-style HTML page to actually learn from |

See [orchestrator.md](orchestrator.md) for the sequence, the validation retry loop, and the handoff contract between stages.

## Status

Scaffolded — agent roles and the orchestration contract are defined; prompts haven't been battle-tested on a real topic yet. Expect to tighten each agent's instructions after the first couple of runs.
