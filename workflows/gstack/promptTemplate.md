# Feature prompt template

Use the short template for focused changes and the expanded template for larger features. Fill only the fields that matter; delete unused fields. Describe the intended behavior rather than guessing implementation details. File paths, screenshots, and examples help when available.

These prompts guide an AI session through the gstack specifications; there is no automated runner. For an existing application, supply its source directory as `applicationPath`. The workflow updates that directory directly.

## Short template — focused feature or fix

```text
In [application path], implement [feature or fix].
Follow workflows/gstack/orchestrator.md, using one goal per increment and
validation before advancing. A small change can be a single increment.

Current behavior: [what happens now, if relevant]
Desired behavior: [what should happen, including the trigger and result]
Done when: [observable acceptance criteria]
Constraints: [anything that must be preserved or followed]

Inspect the existing implementation and follow its conventions. Make the
change, run appropriate checks, and summarize the result and any limitations.
```

### Example

```text
In outputs/gstack/taskManager/app, add a status filter to the task list.
Follow workflows/gstack/orchestrator.md; this change can be one increment.

Desired behavior: users can choose All, Open, or Completed. Default to All.
Changing the filter should update the list without reloading the page.
Done when: the filter works with mixed statuses and an empty result shows
"No tasks match this filter."
Constraints: preserve the existing task creation and completion behavior.

Inspect the existing implementation and follow its conventions. Implement
the change, verify the filter behavior, and summarize the result.
```

## Expanded template — broad or complex feature

```text
Implement [feature name] in [existing application path / new application name].
Use the gstack workflow specifications in workflows/gstack/ as guidance.

Goal
[Who needs this feature, what problem it solves, and the intended outcome.]

Context
[Relevant existing behavior, files, data, interfaces, or reference examples.]
[For a new application: describe the application and its intended users.]

User journeys
1. [Starting state → user action → expected result.]
2. [Another essential journey, if needed.]

Scope
Required: [behaviors that must be delivered.]
Deferred: [related capabilities to leave for later, if relevant.]

Acceptance criteria
1. [A concrete result that can be observed or tested.]
2. [Persistence, failure, or permission behavior where relevant.]
3. [Interface behavior where relevant.]

Data and integrations
[What must be stored, where data comes from, external services, and what
configuration is available. Leave credentials out of this prompt.]

Interface expectations
[Pages, navigation, interactions, responsive behavior, accessibility,
or a reference design. State when the existing design should be followed.]

Technical constraints
[Required stack, compatibility, performance needs, or existing contracts.
If undecided, ask the architect to choose and explain a suitable approach.
New applications default to Tailwind CSS for styling; existing applications
keep their styling system unless a change is requested.]

Execution
Inspect the application and relevant instructions first. For a broad feature,
document scope and assumptions before building. Have planner select required
frontend, backend, and database agents and define their communication contract.
Have architect define technical interfaces and increments; planner confirms
role assignments before implementation.
Implement one goal per increment: a feature, component, or integration
connection. Use the increment gate before implementation and after every increment or
correction; advance only after fresh validation passes. Verify complete journeys during final validation.
Update documentation when setup or behavior changes.

Resolve routine details using the existing application and reasonable
judgment. Ask targeted questions when missing information materially changes
the scope, data model, permissions, or essential behavior. Continue independent
work while waiting. Treat unrun checks as unverified.

Deliver
[Expected code, documentation, migration, or other artifacts.]
Summarize what changed, checks and outcomes, and remaining limitations.
```

## Optional instructions

Append only what suits the task:

- **Explore before implementation:** "Inspect the current application and recommend an approach. Return a plan; wait for my instruction before implementing."
- **Plan and implement:** "Create a brief plan, then proceed with implementation without a separate approval step."
- **Broad idea:** "Help define the smallest complete version that achieves the goal. Record assumptions and defer optional features."
- **Exact specification:** "Follow the supplied acceptance criteria. Flag conflicts before changing the specified behavior."
- **Visual change:** "Follow the existing design and verify the affected layouts at mobile and desktop sizes."
- **Data change:** "Include migrations and describe how existing records will be handled."

## Choosing the level of detail

For a small change, the application location, desired behavior, and one or two acceptance criteria are usually enough. For larger features, add user journeys, boundaries, data requirements, and important constraints. If you are unsure of the size, describe the outcome and let the workflow assess the work after inspecting the application.
