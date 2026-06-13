---
name: mm-plo-orchestrator
description: Orchestrates tracker-first sprint rounds. Use when user says "orchestrate a sprint round", "run the sprint tracker", or "coordinate lane dispatch".
---

# mm-plo-orchestrator

## Overview

This skill orchestrates deterministic, tracker-first sprint rounds by reading the sprint tracker as the source of truth, selecting active lanes from configurable inputs, dispatching upstream BMAD skills in parallel, and closing the round with QA gating and updated tracker state. Act as a sprint orchestration lead. Use when the user wants interactive or `--headless` coordination of sprint lanes. Produces a workspace folder containing `round-summary.md`, `lane-bundles.md`, `dispatch-block.md`, `closure-notes.md`, and `tracker-state.yaml`.

## Conventions

- Bare paths (e.g. `references/guide.md`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory (where `customize.toml` lives).
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{workflow.*}` resolves to the merged workflow customization values.

## On Activation

### Step 0: Handle Standalone Registration

If the user passes `setup`, `configure`, or `install`, or the module is not yet registered in `{project-root}/_bmad/config.yaml`, load `assets/module-setup.md` and complete registration before proceeding.

### Step 1: Resolve the Workflow Block

Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow`

If the script fails, resolve the `workflow` block yourself by reading these three files in base → team → user order and applying structural merge rules: `{skill-root}/customize.toml`, `{project-root}/_bmad/custom/{skill-name}.toml`, `{project-root}/_bmad/custom/{skill-name}.user.toml`.

### Step 2: Load Config

Load config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` if present. Prefer configured values for `{user_name}`, `{communication_language}`, and `{document_output_language}` when available. Resolve `{workflow.output_dir}`, `{workflow.output_folder_name}`, `{workflow.sprint_tracker_path}`, `{workflow.prompt_catalog_path}`, and `{workflow.lane_map_path}`. Treat `{workflow.prompt_catalog_path}` as the repo-owned operations directory and `{workflow.lane_map_path}` as the concrete lane map file inside it.

### Step 3: Establish the Workspace

Set `{round_workspace}` = `{workflow.output_dir}/{workflow.output_folder_name}`. Create it if missing. If `references/.decision-log.md` exists, resume from it. Treat any existing `tracker-state.yaml` as the last known round state, but re-read the tracker before making new decisions.

### Step 4: Load Persistent Facts

Treat entries from `{workflow.persistent_facts}` as foundational context for the whole run. The tracker is the source of truth; do not infer lane progress from conversation alone.

## Stages

| # | Stage | Purpose |
|---|-------|---------|
| 1 | Read Tracker | Confirm current round state from the tracker and `bmad-sprint-status` |
| 2 | Choose Lanes | Select active lanes from the lane map and prompt catalog |
| 3 | Dispatch | Fan out the right BMAD skills in parallel |
| 4 | Collect & Gate | Gather returns, apply QA/review gates, detect churn |
| 5 | Close Round | Write workspace files and update tracker state |

### 1. Read Tracker

Use `bmad-sprint-status` in `mode=data` as the canonical pulse for counts, risks, and the next recommended workflow. Reconcile that output against the tracker and any saved round state. Surface missing tracker, stale state, no active lanes, or contradictory state explicitly instead of guessing.

### 2. Choose Lanes

Derive the active lanes from the tracker, lane map, and prompt catalog. Preserve deterministic ordering: active lanes first, then review lanes, then ready lanes, then backlog only when the lane map explicitly allows a fresh dispatch. If nothing is active, write a blocked round summary and stop.

### 3. Dispatch

Build one dispatch bundle per lane with the lane objective, required inputs, dependencies, stop conditions, and the BMAD skill to invoke. Use these upstream skills as authoritative dependencies:

- `bmad-agent-dev` for implementation lanes
- `bmad-code-review` for review lanes
- `bmad-qa-generate-e2e-tests` for test lanes
- `bmad-sprint-status` when the tracker needs to be refreshed

Dispatch independent lanes in parallel when dependencies allow. Do not copy core lane logic into this skill; orchestrate it.

### 4. Collect & Gate

Collect all returns, compare them to the lane contract, and decide whether the round can close. QA gate failures override a green implementation lane. If the round shows repeated no-advance churn, surface the stall and narrow the next dispatch instead of looping.

### 5. Close Round

Write `round-summary.md`, `lane-bundles.md`, `dispatch-block.md`, `closure-notes.md`, and `tracker-state.yaml` into the workspace. Update the tracker only after the gate passes. Keep `references/.decision-log.md` current so the round can resume cleanly later.

## Headless Mode

When `--headless` is set, skip interactive prompting and return structured JSON with `status`, `round`, `active_lanes`, `workspace`, `outputs`, and `blocked_reason` when applicable.

## Constraints

- The tracker is the source of truth.
- Missing tracker, stale round state, no active lanes, repeated churn, and QA gate failures are explicit outcomes.
- The skill is orchestration only; upstream BMAD skills remain authoritative for their own logic.
- Paths stay configurable so the workflow works in other repos, not just `mm-plo-addon`.
