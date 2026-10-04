# AGENTS.md

This file provides project guidance to Codex and other coding agents working in this repository.

# Project Context

this workspace is used as a tool for me to:
  increase productivity and create automated workflows
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

# Agent Behavior
Before starting any task you should:
  understand the objective well
  ask questions if there is uncertainty
  create a plan
  execute step by step
  review the output
  improve the output based on review

## Project status

This repository contains Markdown workflow specifications under `workflows/`, standalone HTML tools and generated deliverables under `outputs/`, and shared reference material under `resources/`. There is no repository-wide build system, package manifest, or test suite. Generated applications may have their own commands under their application directories.

When the project structure or development commands change, update this file with:
- Build, lint, and test commands (including how to run a single test)
- The high-level architecture and structure once one exists
