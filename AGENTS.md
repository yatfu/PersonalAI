# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

# Project Context

this workspace is used as a tool for me to:
  increase productivity and automate my workflows
  speed up learning and research
  learn about AI workflow and agent development

# Communication Style
Unless explanation is the goal, answers will be short as possible while losing as little detail as possible.

# Rules
All outputs in english should prioritize clarity.
# File Naming Rules
Lowercase file names
use camelCase format
use descriptive names
avoid special characters
# Folder Structure
/workflows contains multi-agent workflow definitions (orchestrator + per-agent specs), one folder per workflow — see workflows/README.md
/outputs Contains completed work and deliverables
/resources contains reference material, source documents, examples, and research
/drafts contains work in progress and temporary files
/weeklyUpdates contains all outputs i tell you to do on a weekly basis

# Agent Behavior
Do not take actions outside the explicit scope of the user's prompt. If completing the request appears to require work beyond that scope, stop and ask for authorization before proceeding.

Before starting any task you should:
  understand the objective well
  ask questions if there is uncertainty
  create a plan
  execute step by step
  review the output
  improve the output based on review

## Project status

The repository includes a buildless interview study webpage in `outputs/interviewGuide/dist`. `guideData.js` holds the study content, `app.js` handles interactions and browser-local progress, and `styles.css` handles layout. See `outputs/interviewGuide/readme.md` for usage.

No build or lint step is required for this page. Check JavaScript with `node --check outputs/interviewGuide/dist/app.js` and `node --check outputs/interviewGuide/dist/guideData.js`. There is no automated test suite or single-test command; manually verify search, expandable panels, practice progress persistence, and printing.

When code is added to this project, update this file with:
- Build, lint, and test commands (including how to run a single test)
- The high-level architecture and structure once one exists
