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
- `content.json` — validated learning content and viz data, per module
- `resource.html` — the rendered site: one section per module, with visualizations where the content supplies data for one

## Agents

| Agent | Role |
|---|---|
| [`agents/researchAgent.md`](agents/researchAgent.md) | Maps the topic: subtopics, dependencies, key concepts, common pitfalls |
| [`agents/researchValidator.md`](agents/researchValidator.md) | Checks the *research* for accuracy, gaps, and bad sequencing before anything is built on top of it |
| [`agents/curriculumPlanner.md`](agents/curriculumPlanner.md) | Turns validated research into ordered modules with objectives and milestones |
| [`agents/contentBuilder.md`](agents/contentBuilder.md) | Writes the actual learning content as `content.json` — no HTML, no visualizations |
| [`agents/contentValidator.md`](agents/contentValidator.md) | Checks the *content* is sufficient to actually learn each topic/key concept from — separate gate from researchValidator, later in the pipeline, on different material |
| [`agents/siteGenerator.md`](agents/siteGenerator.md) | Renders validated content into the site and its visualizations — presentation only, doesn't write or judge content |

See [orchestrator.md](orchestrator.md) for the sequence, both retry loops, and the handoff contract between stages.

## Status

Run once end-to-end on `topic: Next.js` (2026-07-13/14) — see `outputs/topicTrainer/nextjs/`. Both retry loops fired for real: researchValidator rejected the first research draft (version mislabeling + a missing Metadata/SEO subtopic), approved on revision 1; contentValidator approved content.json on the first pass with one trivial tag fix applied directly. No contentBuilder retry loop has been exercised yet — worth watching the first time it triggers.

**2026-07-14 revision (token efficiency):** that first run spent a lot of tokens re-stating full content in chat between agents instead of leaving it on disk. `orchestrator.md` and every agent spec were revised to: (1) require file-first handoffs — each agent writes its output file directly and returns only a short status summary, never the full content restated; (2) require patch-in-place resubmissions on a validator rejection, instead of full regeneration; (3) mark `curriculumPlanner`, `contentBuilder`, `contentValidator`, and `siteGenerator` as no-web-search roles (only `researchAgent`/`researchValidator` should hit the web); (4) scope `researchValidator`'s independent re-verification to flagged/fast-moving claims rather than blanket re-checking everything; (5) give `researchAgent` an explicit size cap (~2,500–4,000 words, ~12–18 subtopics, 2-3 sentences per keyConcept) — completeness of coverage is still required, the cap is on verbosity per item, not on what must be included. Not yet re-run against these revised specs — worth comparing token totals on the next topic.
