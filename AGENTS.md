# AGENTS.md

This file provides project guidance to Codex and other coding agents working in this repository.

## Project context

Use this workspace to:

- Increase productivity and create automated workflows.
- Speed up learning and research.
- Learn about AI workflows and agent development.

## Communication

- Keep answers as short as possible while preserving detail, unless explanation is the goal.
- Prioritize clarity in all English output.

## File naming

- Use descriptive names.
- Use camelCase with a lowercase initial letter.
- Avoid special characters.

## Folder structure

| Directory | Purpose |
|---|---|
| `workflows/` | Multi-agent workflow definitions: an orchestrator and individual agent specifications, with one folder per workflow. See [workflows/README.md](workflows/README.md). |
| `outputs/` | Completed work and deliverables. |
| `resources/` | Reference material, source documents, examples, and research. |
| `workflows/gstack/skills/` | Shared gstack procedures, linked from `.agents/skills/` for Codex discovery. |
| `workflows/gstack/scripts/` | Workflow automation, including the increment validation gate and its behavioral tests. |

## Agent behavior

For each task:

1. Understand the objective before starting.
2. Ask questions if there is uncertainty.
3. Create a plan.
4. Execute step by step.
5. Review the output.
6. Improve the output based on the review.

## Commits and GitHub

- After each completed logical change, use the `git-commits` skill to create a separate commit, unless the user explicitly requests otherwise.
- Inspect the diff and run appropriate checks before committing. Preserve unrelated changes and existing staged work.
- Push the completed commits to this repository's configured GitHub upstream. This is standing authorization for routine commits and pushes; do not request confirmation again unless execution permissions require it.
- Do not force-push or rewrite history. If committing or pushing fails, report the failure and preserve the work.

## Project status

This repository contains Markdown workflow specifications under `workflows/`, standalone HTML tools and generated deliverables under `outputs/`, and shared reference material under `resources/`. There is no repository-wide build system, package manifest, or test suite. Generated applications may have their own commands under their application directories.

The gstack gate uses Python 3.8+ and the standard library. Run its tests with `python3 -m unittest discover -s workflows/gstack/scripts/tests -p 'test*.py'`; run one case with `python3 -m unittest discover -s workflows/gstack/scripts/tests -p 'test*.py' -k test_order_and_read_only_checks`. See [workflows/gstack/validationGate.md](workflows/gstack/validationGate.md) for application validation commands.

When the project structure or development commands change, update this file with:

- Build, lint, and test commands, including how to run a single test.
- The high-level architecture and project structure once established.
