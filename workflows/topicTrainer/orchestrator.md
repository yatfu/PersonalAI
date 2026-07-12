# Orchestrator — topicTrainer

Not an agent itself — the control-flow spec that runs the four agents in order and writes the final result.

## Sequence

1. **researchAgent** — `topic` (+ `focus` if given) → research brief
2. **validationAgent** — research brief → validation verdict (approved, or issues to fix)
   - if not approved: send the specific issues back to **researchAgent**, which revises and resubmits (see Loops below)
3. **curriculumPlanner** — approved research brief → curriculum (ordered modules, objectives, milestones)
4. **resourceBuilder** — curriculum + the approved research brief + `currentLevel` → single self-contained HTML learning page

## Handoff contract

```
researchAgent → validationAgent:
  - researchedAt: the date this research was run, plus the recency of sources it draws on
  - topicMap: list of subtopics with a short description each
  - dependencies: which subtopics require which others first
  - keyConcepts: per subtopic, the concepts a learner must come away with
  - pitfalls: common misconceptions/mistakes worth calling out
  - sources: what was consulted, with links where applicable
  - openQuestions: anything the research agent is unsure about

validationAgent → researchAgent (only on rejection):
  - issues: specific, actionable list — "X is outdated", "dependency order is wrong: A needs B first", "missing: ...", "missing/stale researchedAt: ..."

validationAgent → curriculumPlanner (only on approval):
  - the research brief, unchanged, plus a short note on anything borderline that was approved anyway

curriculumPlanner → resourceBuilder:
  - modules: ordered list, each with a name, objective, the subtopics it covers, and relative weight/depth
  - milestones: checkpoints — "after module N, you should be able to ..."
  - the approved research brief, carried forward unchanged — resourceBuilder needs keyConcepts/pitfalls/sources as the substance for each module's content, not just the curriculum's headings

resourceBuilder → orchestrator:
  - resource.html — a single self-contained HTML page, one accordion section per module, with visualizations where they aid understanding
  - a flag if any module's underlying research was too thin to write real content for (rather than a padded/generic section)
```

## Loops / retries

If **validationAgent** rejects the research brief, it goes back to **researchAgent** with the specific issue list. Maximum **2** revision passes. If still not approved after that, stop and surface the unresolved issues to the user rather than looping indefinitely or forcing an approval.

## Stopping condition

Run is complete when `resourceBuilder` produces `resource.html` (or flags modules whose research was too thin to write real content for).

## Output location

`outputs/topicTrainer/<topicSlug>/` — write `research.md` (final approved version), `curriculum.md`, and `resource.html`. `<topicSlug>` = the topic in camelCase, e.g. topic "Async Rust" → `asyncRust`.
