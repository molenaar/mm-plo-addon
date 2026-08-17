# mm-plo-addon

A [BMad Method](https://github.com/bmad-code-org/BMAD-METHOD) addon, built with [BMad Builder](https://bmad-builder-docs.bmad-method.org/), that adds tracker-first parallel sprint orchestration to a BMad project.

**What it gives you:** `mm-plo-orchestrator` reads your `sprint-status.yaml` tracker and dispatches dev, review, QA, and retrospective lanes in parallel — stories advance independently instead of one at a time.

**Why use it:** once John has planned epics and stories, this turns execution from "wait for story 1 to finish before starting story 2" into several stories moving through dev → review → QA at once, with John watching progress in his own loop.

## What’s inside

- `skills/mm-plo-orchestrator/` — tracker-first sprint orchestration (dispatches `bmad-build-auto` per story across parallel lanes; see [docs/build-integration.md](docs/build-integration.md))
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

New to this addon? [docs/tutorial.md](docs/tutorial.md) walks through installing it and running a full sprint round — two terminals, scoping a round with John, and why stories advance in parallel rather than one at a time.

## Recommended: BMAD Viewer for VS Code

The **[BMAD Viewer](https://marketplace.visualstudio.com/items?itemName=rdudiver.bmad-viewer-vscode)** is essential for keeping the human in the loop while the orchestrator runs.

- **Kanban dashboard** — reads directly from `sprint-status.yaml` so you see story status updates in real time as PLO advances lanes
- **Round summaries** — search and browse all `.md` files in `_bmad-output` rendered as HTML, including every `round-summary.md` the orchestrator produces
- **Human gate** — review the kanban after John populates epics and before handing off to PLO; if the board looks wrong, fix it before setting a `/goal`

Install it from the VS Code marketplace before running your first sprint.

## Suggested Sprint Setup: Two Terminals + Viewer

Set and forget. Open two Claude Code terminals and the BMAD Viewer, then step back and watch.

**Terminal 1 — PLO executes the sprint**

After John finishes planning and you've reviewed the kanban:

```
/mm-plo-orchestrator --headless
```

PLO dispatches `bmad-build-auto` directly per lane (not through Amelia's persona — her menu routes to the interactive `bmad-build`, which would stall waiting for a human that isn't there) and runs parallel rounds — dev, review, QA, and retrospective lanes — continuing round after round by itself until the tracker runs out of eligible lanes, at which point it stops and surfaces why. No `/goal` or external loop needed; the tracker itself is what paces it. Each round ends with a closure line so you can follow progress. See [docs/build-integration.md](docs/build-integration.md) for how this fits together with upstream BMad's own build workflow.

**Terminal 2 — John, on demand**

```
/bmad-agent-pm
```

No loop — ask John for a status/risk read whenever you want one. The natural moment is right when PLO stops with nothing active (see Terminal 1): that's when there's actually something new for him to weigh in on, not an arbitrary timer.

Real projects typically keep more of the team available the same way — Mary (`bmad-agent-analyst`), Winston (`bmad-agent-architect`), and a UX designer (e.g. `bmad-agent-ux-designer`), each in their own terminal, none looping, all on demand. PLO can also ping any of them directly mid-round when a lane is blocked on something in their lane — see Cross-Session Coordination in `mm-plo-orchestrator`'s `SKILL.md`.

*(John as a Stop-hook goal evaluator was attempted and deferred — a prompt-based hook caused an endless loop in his own terminal. See `NOTES.md` if you want to pick that idea back up.)*

**You — watch and unblock**

- **BMAD Viewer**: kanban updates as stories advance, round summaries available in the search panel
- **Terminal 1**: closure lines show round-by-round progress; a stop with nothing active is your cue to check with John; `churn: detected` or `churn: rate-limit` means action needed sooner

Your only job mid-sprint is to unblock what neither PLO nor John can resolve alone.

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
