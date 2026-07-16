# Orchestrator — topicTrainer

Not an agent itself — the control-flow spec that runs the six agents in order and writes the final result.

## Execution conventions

These apply to every stage below — they exist because the first full run burned far more tokens than the actual content required, mostly from re-stating content in chat instead of leaving it on disk.

1. **File-first handoff.** Every agent writes its designated output directly to its file in `outputs/topicTrainer/<topicSlug>/` and returns only a short status summary in its final message (what it produced, key decisions, anything flagged) — never the full content restated in chat. The next agent **reads the file itself**; it is never pasted the previous stage's full output.
2. **Patch, don't regenerate.** On a rejection (either loop), the validator's issues must reference the specific field/section/module at fault. The resubmitting agent edits its existing file **in place** to address those items — it does not regenerate the whole document from scratch. It returns a short "what changed" note, not the restated document.
3. **Tool scope is not uniform.** Only **researchAgent** and **researchValidator** should need WebSearch/WebFetch — they're the only stages dealing with facts that can be wrong or stale. **curriculumPlanner**, **contentBuilder**, **contentValidator**, and **siteGenerator** work entirely from files already on disk (the research brief, the curriculum, the content) and should not need to search the web at all.

## Sequence

1. **researchAgent** — `topic` (+ `focus` if given) → writes `research.md`
2. **researchValidator** — reads `research.md` → validation verdict (approved, or issues to fix)
   - if not approved: issues go back to **researchAgent**, which patches `research.md` in place and resubmits (see Loops below)
3. **curriculumPlanner** — reads approved `research.md` → writes `curriculum.md`
4. **contentBuilder** — reads `curriculum.md` + `research.md` → writes `content.json` (topics, explanations, key concepts, viz data — no HTML)
5. **contentValidator** — reads `content.json` (+ `curriculum.md` + `research.md` for cross-reference) → sufficiency verdict (sufficient, or gaps to fill)
   - if insufficient: issues go back to **contentBuilder**, which patches `content.json` in place and resubmits (see Loops below)
6. **siteGenerator** — reads approved `content.json` → writes `resource.html`, with visualizations rendered from any `vizData`

## Handoff contract

Every row below is a file on disk, not a chat payload — the "contract" is the file's schema, not something re-typed between agents.

```
research.md (written by researchAgent, read by researchValidator):
  - researchedAt: date researched, plus recency of sources drawn on
  - topicMap: subtopics with a short description each
  - dependencies: which subtopics require which others first
  - keyConcepts: per subtopic, the concepts a learner must come away with
  - pitfalls: common misconceptions/mistakes worth calling out
  - sources: what was consulted, with links where applicable
  - openQuestions: anything the research agent is unsure about

researchValidator's verdict (returned in chat, not written to a file — it's small):
  - approved: true/false
  - issues (only if rejected): specific, actionable, referencing the exact field/subtopic in research.md
  - notes: anything borderline, approved anyway

  - on rejection: researchAgent patches research.md in place per the issues list, does not regenerate it
  - on approval: curriculumPlanner reads research.md directly

curriculum.md (written by curriculumPlanner, read by contentBuilder):
  - modules: ordered list, each with a name, objective, the subtopics it covers, relative weight/depth
  - milestones: checkpoints — "after module N, you should be able to ..."

content.json (written by contentBuilder, read by contentValidator and siteGenerator):
  - modules: per module — name, objective, sections (subtopic, explanation, keyConceptsCovered, pitfallsCovered), milestoneNote where applicable, optional vizData (type + raw data, not a rendering)
  - sources: carried from research.md, for citation on the site
  - a flag if any module's underlying research was too thin to write real content for

contentValidator's verdict (returned in chat, not written to a file):
  - sufficient: true/false
  - issues (only if insufficient): specific, actionable, referencing the exact module/section in content.json
  - notes: anything borderline, approved anyway

  - on rejection: contentBuilder patches content.json in place per the issues list, does not regenerate modules that weren't flagged
  - on approval: siteGenerator reads content.json directly

resource.html (written by siteGenerator):
  - a single self-contained HTML page, one section per module rendered from content.json, visualizations rendered from any vizData, milestones flagged in place, sources cited
  - a flag (in its chat summary, not the file) if any vizData couldn't be meaningfully rendered
```

## Loops / retries

- If **researchValidator** rejects `research.md`, issues go back to **researchAgent**, which patches the file in place. Maximum **2** revision passes.
- If **contentValidator** finds `content.json` insufficient, issues go back to **contentBuilder**, which patches the file in place. Maximum **2** revision passes.
- In either case, if still unresolved after 2 passes, stop and surface the issues to the user rather than looping indefinitely or forcing an approval.

## Stopping condition

Run is complete when `siteGenerator` produces `resource.html` (or a validator's issues remain unresolved after 2 revision passes).

## Output location

`outputs/topicTrainer/<topicSlug>/` — `research.md`, `curriculum.md`, `content.json`, and `resource.html`, each written directly by the agent responsible for it (not re-written by the orchestrator after the fact). `<topicSlug>` = the topic in camelCase, e.g. topic "Async Rust" → `asyncRust`.
