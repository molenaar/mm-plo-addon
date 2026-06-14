# mm-plo-addon

Private BMad addon for tracker-first sprint orchestration.

## What’s inside

- `skills/mm-plo-orchestrator/` — reusable workflow skill
- `.claude-plugin/marketplace.json` — standalone distribution manifest at repo root

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
