# mm-plo-addon

Private BMad addon for tracker-first sprint orchestration.

## What’s inside

- `skills/mm-plo-orchestrator/` — tracker-first sprint orchestration (Amelia executes stories across parallel lanes)
- `skills/wds-sprint-ux-review/` — design fidelity auditor (Freya monitors UX convergence against DESIGN.md and EXPERIENCE.md)
- `.claude-plugin/marketplace.json` — standalone distribution manifest at repo root

## Recommended: BMAD Viewer for VS Code

The **[BMAD Viewer](https://marketplace.visualstudio.com/items?itemName=rdudiver.bmad-viewer-vscode)** is essential for keeping the human in the loop while the orchestrator runs.

- **Kanban dashboard** — reads directly from `sprint-status.yaml` so you see story status updates in real time as Amelia advances lanes
- **Round summaries** — search and browse all `.md` files in `_bmad-output` rendered as HTML, including every `round-summary.md` the orchestrator produces
- **Human gate** — review the kanban after John populates epics and before handing off to Amelia; if the board looks wrong, fix it before setting a `/goal`

Install it from the VS Code marketplace before running your first sprint.

## Suggested Sprint Setup: Two Terminals + Viewer

Set and forget. Open two Claude Code terminals and the BMAD Viewer, then step back and watch.

**Terminal 1 — Amelia executes the sprint**

After John finishes planning and you've reviewed the kanban:

```
/goal ROUND closure line shows done: X/X and retros: X/X with churn: none
/mm-plo-orchestrator --headless
```

Amelia runs parallel rounds — dev, review, QA, and retrospective lanes — until all stories and epics are done. Each round ends with a closure line you and the `/goal` evaluator can both read.

**Terminal 2 — John monitors progress**

```
/loop 20m /bmad-sprint-status
```

John wakes up every 20 minutes, reads the tracker, and gives a PM-level status report. He flags risks, blockers, and whether the sprint is on track — a richer check than the goal evaluator alone.

**Terminal 3 (optional) — Freya audits design fidelity**

```
/loop 40m /wds-sprint-ux-review
```

Freya wakes up every 40 minutes and scans recent code changes against your design system. She detects hardcoded colors, missing component dossiers, protagonist journey drift, and prototype candidates — design signals that matter independent of PLO's implementation progress. Her findings append to `_bmad-output/planning-artifacts/wds-status.md` for you to review in the BMAD Viewer. Pure advisory; never blocks stories from reaching `done`.

**Advanced: John as the goal evaluator — deferred until further notice**

> **This feature is currently not working and has been deferred.** The prompt-based Stop hook causes an endless loop in John's PM terminal — the hook fires inside John's own session, which never terminates cleanly. No solution exists for this yet. The section below is kept for reference only; do not configure this in active projects.

<details>
<summary>Reference (not for use)</summary>

By default `/goal` uses a small fast model (Haiku) to check the closure line — mechanical pattern matching. For a richer check, wire John as a custom [prompt-based Stop hook](https://code.claude.com/docs/en/hooks-guide#prompt-based-hooks) in your project's `.claude/settings.json`. John evaluates whether acceptance criteria are *genuinely* met, not just technically passing — because he wrote them.

```json
{
  "hooks": {
    "Stop": [{
      "matcher": "^ROUND \\d+ \\|",
      "hooks": [{
        "type": "prompt",
        "prompt": "<paste workflow.goal_evaluator_prompt from customize.toml>"
      }]
    }]
  }
}
```

The `matcher` is critical. `^ROUND \\d+ \\|` matches only the standardized closure line emitted by Stage 5 (`ROUND 3 | done: 4/6 | ...`). Without it the hook fires on every response in every session — including John's PM sessions and any session that reads a round-summary.md file — creating an unintended loop.

With this in place, drop `/goal` from Terminal 1 and just run:

```
/mm-plo-orchestrator --headless
```

John wakes up after every round automatically, applies PM-level judgment, and keeps Amelia running until he is satisfied.

</details>

**You — watch and unblock**

- **BMAD Viewer**: kanban updates as stories advance, round summaries and WDS design findings available in the search panel
- **Terminal 1**: closure lines show round-by-round progress; `churn: detected` or `churn: rate-limit` means action needed
- **Terminal 2**: John's 20-minute reports surface anything the automation missed
- **Terminal 3 (if running)**: Freya's design fidelity findings in `wds-status.md`

Your only job mid-sprint is to unblock what neither Amelia nor John can resolve alone.

## Install

Install from this repository with the BMad installer:

```bash
npx bmad-method install --custom-source https://github.com/molenaar/mm-plo-addon --tools claude-code --yes
```

Then run `mm-plo-orchestrator` and use `setup` or `configure` to register config and help entries.

## Development

This repo's local `_bmad` install and `.claude/skills` toolchain track [BMad Builder](https://github.com/bmad-code-org/bmad-builder) for building and validating `mm-plo-orchestrator`. To refresh the toolchain to the latest BMad Builder release alongside this addon's own skills:

```bash
npx bmad-method install --custom-source https://github.com/bmad-code-org/bmad-builder,https://github.com/molenaar/mm-plo-addon --tools claude-code --yes --action update
```

## License

MIT
