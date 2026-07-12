# &lt;workflowName&gt;

One paragraph: what this workflow produces and why it exists.

## When to run it

What triggers a run — a request, a schedule, an event.

## Inputs

What the caller needs to supply to start a run (e.g. a topic, a URL, constraints).

## Output

What gets produced and where it lands: `outputs/<workflowName>/<runIdentifier>/...`

## Agents

| Agent | Role |
|---|---|
| `agents/<agentName>.md` | one-line role summary |

See [orchestrator.md](orchestrator.md) for the sequence and handoff contract between them.
