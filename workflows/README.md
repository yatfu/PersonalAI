# Workflows

Definitions for repeatable multi-agent workflows. This folder holds **how a workflow runs** — orchestration logic and agent specs. It does not hold results; those go to `/outputs/<workflowName>/...` (see below).

## Convention

Each workflow gets its own folder:

```
workflows/
  <workflowName>/
    README.md          — what it does, when to run it, what it needs, where results land
    orchestrator.md     — sequence, handoff contract between agents, retry/loop rules, output location
    agents/
      <agentName>.md     — one file per agent: role, inputs, outputs, instructions
```

`_template/` is a blank copy of this shape — copy it to start a new workflow rather than building the structure by hand.

## Why split it this way

- **orchestrator.md is not an agent** — it's the spec for the control flow (who runs after whom, what gets passed forward, when to loop back or stop). Whether you end up running it as a Claude Code session, a script, or an n8n flow, the contract stays the same and only needs writing once.
- **agents/ stays flat and swappable** — each agent file is self-contained (role, inputs, outputs, instructions), so an agent can be reused across workflows or replaced without touching the others.
- **Results live in `/outputs`, not here** — a workflow definition doesn't change when you run it; a run's output should. Running `topicTrainer` on a topic writes to `outputs/topicTrainer/<topicSlug>/`, keeping the definition and its outputs from tangling together as more workflows and more runs pile up.
- **Reference material a workflow depends on goes in `/resources`** — e.g. a style guide, a glossary, source docs — linked to from the relevant agent file rather than duplicated.

## Starting a new workflow

1. Copy `_template/` to `workflows/<newWorkflowName>/`.
2. Fill in `README.md`, `orchestrator.md`, and one file per agent under `agents/`.
3. Add a line for it below.

## Current workflows

- **[gstack](gstack/README.md)** — foundation for generating full stack applications, from scope and architecture through implementation, validation, and local handoff.
- **[topicTrainer](topicTrainer/README.md)** — give it a topic, it researches, validates, builds a curriculum, and produces a single accordion-style HTML page to learn it from.
