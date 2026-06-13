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

## License

MIT
