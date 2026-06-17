# mm-plo-addon

Private BMad addon for tracker-first sprint orchestration.

## What’s inside

- `skills/mm-plo-orchestrator/` — reusable workflow skill
- `.claude-plugin/marketplace.json` — standalone distribution manifest at repo root

## Recommended: BMAD Viewer for VS Code

The **[BMAD Viewer](https://marketplace.visualstudio.com/items?itemName=rdudiver.bmad-viewer-vscode)** is essential for keeping the human in the loop while the orchestrator runs.

- **Kanban dashboard** — reads directly from `sprint-status.yaml` so you see story status updates in real time as Amelia advances lanes
- **Round summaries** — search and browse all `.md` files in `_bmad-output` rendered as HTML, including every `round-summary.md` the orchestrator produces
- **Human gate** — review the kanban after John populates epics and before handing off to Amelia; if the board looks wrong, fix it before setting a `/goal`

Install it from the VS Code marketplace before running your first sprint.

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
