---
name: design-fidelity-review
description: Freya's judgment review for signals 3-6 against DESIGN.md and EXPERIENCE.md
code: DR
added: 2026-06-19
type: prompt
---

The outcome is one advisory finding block covering the four judgment signals. The consumer is `wds-status.md` — a file John reads in his 20-minute loop and Marcel reviews in BMAD Viewer. Every finding must be specific enough that a reader who was not in this session can act on it: name the file, quote or cite the relevant EXPERIENCE.md section, name the protagonist affected. Vague observations are not findings.

You have in scope: the scan JSON from `scan-signals.py` (signals 1–2 resolved; signal 3 new-page list present), the raw git diff for `{workflow.scan_paths}`, `{workflow.design_doc}`, `{workflow.experience_doc}`, and the component dossier folder at `{workflow.component_dossiers}`.

**Signal 3 — New route not in "The House"**: For each `.astro` file in the scan JSON's `new_pages` list (new files in `src/pages/`), check `{workflow.experience_doc}` for a corresponding nav section, route entry, or House floor reference. Flag any file that has none. Name the file and the missing EXPERIENCE.md anchor.

**Signal 4 — Missing Sally dossier**: When the diff introduces or substantially changes a non-trivial interactive `.astro` or `.ts` component in `src/components/` — state machines, multi-step flows, complex transitions, anything Sally would need to wireframe — check whether a corresponding file exists in `{workflow.component_dossiers}`. Flag if absent. Bar: would a developer need a spec to implement the interaction correctly?

**Signal 5 — Protagonist journey drift**: If the diff alters auth redirects, navigation shortcuts, copy on key decision screens, or flow transitions that a named protagonist would traverse, flag it. Name the protagonist, cite the EXPERIENCE.md journey section, and describe the specific change. Read the diff carefully — this signal fires on behavioural changes to existing flows, not new components.

**Signal 6 — Prototype trigger**: If the diff introduces a complex UX interaction that has no preceding dossier, no EXPERIENCE.md reference, and no established pattern in the codebase, emit: "Prototype candidate: [component name]. Recommend Sally dossier + human review before Amelia proceeds." This is the highest-priority finding in the block and should appear first when it fires.

Produce findings only for signals that actually fired. For each signal with nothing to report, emit "None detected." Do not invent findings to fill the format.
