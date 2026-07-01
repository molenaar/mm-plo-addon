# mm-plo-addon

A [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) addon, built with [BMad Builder](https://bmad-builder-docs.bmad-method.org/), that adds tracker-first parallel sprint orchestration to a BMad project.

**What it gives you:** two skills. `mm-plo-orchestrator` reads your `sprint-status.yaml` tracker and dispatches dev, review, QA, and retrospective lanes in parallel — stories advance independently instead of one at a time. `mm-ux-orchestrator` runs alongside it as an advisory UX fidelity loop, delegating to Sally (`bmad-agent-ux-designer`) with an optional deterministic scan when a WDS design system is present.

**Why use it:** once John has planned epics and stories, this turns execution from "wait for story 1 to finish before starting story 2" into several stories moving through dev → review → QA at once, with John — and optionally a UX reviewer — watching progress in their own loops.

## What’s inside

- `skills/mm-plo-orchestrator/` — tracker-first sprint orchestration (Amelia executes stories across parallel lanes)
- `skills/mm-ux-orchestrator/` — UX orchestration loop (Freya delegates to Sally via `bmad-agent-ux-designer`; WDS deterministic scan activates automatically when DESIGN.md is present)
- `.claude-plugin/marketplace.json` — standalone distribution manifest at repo root

## Lanes run in parallel, not sequentially

`mm-plo-orchestrator` doesn't work through stories one at a time. Each round, it reads `docs/operations/lane-map.yaml` alongside `sprint-status.yaml` to see which stories can start *now* versus which are waiting on one specific dependency. A populated lane map looks something like this:

```yaml
lanes:
  - id: 1-1-user-authentication
    depends_on: []
  - id: 1-2-account-management
    depends_on: []
  - id: 1-3-password-reset
    depends_on: ["1-1-user-authentication"]
  - id: 1-4-session-persistence
    depends_on: ["1-1-user-authentication"]
```

`1-1` and `1-2` start immediately — neither depends on anything. `1-3` and `1-4` only wait on `1-1`, specifically — not on `1-2`, and not on each other. The moment `1-1` clears review, both can start, independently, in the same round. Dependencies gate individual stories, not the round as a whole — that's the entire model.

(This repo's own `docs/operations/lane-map.yaml` ships empty — it's a template. A real project populates it once epics and stories exist.)

## Tutorial

New to this addon? [docs/tutorial.md](docs/tutorial.md) walks through installing it and running a full sprint round — three terminals, scoping a round with John, and why stories advance in parallel rather than one at a time.

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
/bmad-agent-dev
/goal ROUND closure line shows done: X/X and retros: X/X with churn: none
/mm-plo-orchestrator --headless
```

Amelia runs parallel rounds — dev, review, QA, and retrospective lanes — until all stories and epics are done. Each round ends with a closure line you and the `/goal` evaluator can both read.

**Terminal 2 — John monitors progress**

```
/bmad-agent-pm
/loop 20m /bmad-sprint-status
```

John wakes up every 20 minutes, reads the tracker, and gives a PM-level status report. He flags risks, blockers, and whether the sprint is on track — a richer check than the goal evaluator alone.

**Terminal 3 (optional) — Freya orchestrates UX review**

Requires `bmad-agent-ux-designer` (Sally) installed.

```
/bmad-agent-ux-designer
/loop 40m /mm-ux-orchestrator
```

Freya wakes up every 40 minutes and delegates to Sally for design judgment (House integration, missing dossiers, protagonist journey drift, prototype candidates). On WDS projects (DESIGN.md present), she also runs a deterministic scan first (hex drift, missing `@reference`, new pages) and passes the results to Sally. Findings append to `_bmad-output/planning-artifacts/ux-status.md` for review in BMAD Viewer. Pure advisory; never blocks stories from reaching `done`.

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
- **Terminal 3 (if running)**: Freya's design fidelity findings in `ux-status.md`

Your only job mid-sprint is to unblock what neither Amelia nor John can resolve alone.

## Install

Install from this repository with the BMad installer:

```bash
npx bmad-method install --custom-source https://github.com/molenaar/mm-plo-addon --tools claude-code --yes
```

Then run `mm-plo-orchestrator` and use `setup` or `configure` to register config and help entries.

## Update

If you already have a previous version of this addon installed in a project, run the same command with `--action update`:

```bash
npx bmad-method install --custom-source https://github.com/molenaar/mm-plo-addon --tools claude-code --yes --action update
```

## Development

This section is only relevant if you are modifying or building this addon itself — not for regular use. The addon is built and validated using [BMad Builder](https://github.com/bmad-code-org/bmad-builder), which provides the build toolchain for this repo. To keep both BMad Builder and the addon's own skills in sync inside this repo:

```bash
npx bmad-method install --custom-source https://github.com/bmad-code-org/bmad-builder,https://github.com/molenaar/mm-plo-addon --tools claude-code --yes --action update
```

The difference from the Update command above is the additional `https://github.com/bmad-code-org/bmad-builder` source — that pulls in the builder tools needed to work on the addon. You do not need this when using the addon in a project.

## License

MIT
