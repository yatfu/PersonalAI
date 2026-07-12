# Orchestrator — &lt;workflowName&gt;

Not an agent itself — the control-flow spec other agents/scripts run against.

## Sequence

1. `agents/<agentA>.md` — input → output
2. `agents/<agentB>.md` — input → output
3. ...

## Handoff contract

What exact fields/shape pass from one stage to the next. Be concrete enough that any agent (or script) reading only this file knows what it will receive and must produce.

```
<agentA> output → <agentB> input:
  - field: description
```

## Loops / retries

Does any stage send work backward (e.g. validation failing research)? Under what condition, and how many times before escalating to the human instead of looping forever?

## Stopping condition

What marks the run complete.

## Output location

Where the orchestrator writes the final result: `outputs/<workflowName>/<runIdentifier>/`
