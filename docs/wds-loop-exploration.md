# WDS Loop — Exploration Notes

> Status: draft exploration — evaluate with Marcel before building anything
> Date: 2026-06-19
> Context: PLO headless + /loop 20m /bmad-sprint-status active

---

## Why this matters

PLO's goal is convergent: all stories done, all gates green. It doesn't care whether
the shipped UI matches EXPERIENCE.md's "House" model or uses `#3b82f6` where it should
use `bg-primary`. A sprint can reach `done: 62/62` while every protagonist journey in
EXPERIENCE.md is broken and "The House" is still a corridor of identical white doors.

WDS needs its own loop — orthogonal to PLO, not subordinate to it.

---

## What we learned from the Stop hook failure

The README describes wiring John as a Stop hook so he evaluates every round closure.
This was horrible in practice: Stop fires after **every AI response**, not after every
round. A single PLO session producing 20 responses triggers John 20 times — mostly on
mechanical messages that carry no signal. Token burn is extreme, output is noise.

**Lesson: trigger on human-meaningful events, not on AI response boundaries.**

The right triggers for a WDS loop are:
- A round close (PLO emits a structured closure line)
- A story reaching `done` in the tracker
- A fixed wall-clock interval (Freya wakes up and scans regardless)

None of these are Stop hooks.

---

## What a WDS loop would actually check

Freya reads:
- `git diff HEAD~3..HEAD -- app/src/` — what actually changed in the UI this round
- `DESIGN.md` — token taxonomy, canon themes, `{theme.<name>.<token>}` paths
- `EXPERIENCE.md` — "The House" nav model, named protagonist journeys (Alex etc.)
- `docs/ux/components/*` — Sally's component dossiers (wireframes, state specs)
- `app/src/styles/themes/*.css` — shipped tokens (source of truth per DESIGN.md §1)

Freya outputs findings to `_bmad-output/planning-artifacts/wds-status.md` — one
timestamped entry per run. John reads this in his 20-min loop and decides if action
is needed.

### Signal types Freya would detect

**1. Hardcoded color drift**
Components using hex values or raw CSS vars instead of Tailwind token classes.
`grep -rn "#[0-9a-f]\{3,6\}\|var(--color" app/src/components/` catches this.
This is a lint signal — mechanically detectable, no LLM needed for the check itself.

**2. Missing @reference in scoped styles**
Components with `<style>` blocks using `@apply` with custom tokens (like `bg-primary`)
without `@reference "../../styles/global.css"` — exactly the CI failure we just fixed.
A pre-commit linter could catch this. But Freya flags it in her advisory if she sees it.

**3. New route not integrated into "The House"**
EXPERIENCE.md Chapter 1 describes the nav model — the House — as the answer to "where
am I, what matters, where do I go next?" If a new top-level page appears in
`app/src/pages/` without a corresponding EXPERIENCE.md section or nav integration,
Freya flags it: "new door added, no floor indicator."

**4. Missing Sally dossier for complex UI**
If a story implements a non-trivial interactive component and there's no corresponding
`docs/ux/components/<component>.md`, Freya flags: "wireframe/dossier missing."
Simple components (static cards, text) don't need dossiers. Judgement call — Freya is
LLM-powered, so she can make this call.

**5. Protagonist journey drift**
EXPERIENCE.md names protagonist journeys (Alex, etc.). If a round's diffs change the
flow a protagonist would take — different auth redirect, removed shortcut, changed
copy on a key decision screen — Freya flags it as a journey check.

**6. Prototype trigger signal**
If Freya sees a complex UX interaction in the diffs that:
  - Has no preceding wireframe/dossier
  - Has no EXPERIENCE.md reference
  - Is in a new pattern not previously implemented
She emits: "Prototype candidate: [component]. Recommend Sally dossier + human review
before Amelia proceeds."

This is the highest-value signal — recognizing when development has outrun the design
intent and human exploration is needed before the feature calcifies.

---

## Proposed architecture

### Option A: Freya as a timed parallel loop (simplest)

```
Terminal 3:
/loop 40m /wds-sprint-ux-review
```

Freya runs every 40 minutes. She scans recent diffs, checks design fidelity,
appends a timestamped finding to `wds-status.md`. John reads it at his 20-min
mark. No blocking, pure advisory. Marcel reviews `wds-status.md` in BMAD Viewer.

Advantages: trivial to set up, no PLO coupling, same pattern as John's loop.
Disadvantage: not event-driven — might wake up when nothing changed.

### Option B: WDS with its own convergence goal

```
Terminal 3:
/goal WDS: DESIGN.md v1 complete + EXPERIENCE.md Chapter 2 approved
/wds-loop --headless
```

Freya + Saga work toward a WDS-specific goal: design documentation complete,
Chapter 2 resolved, no open UX questions. Parallel to PLO, different success
condition. WDS terminates when its own goal is met.

This maps cleanly onto the "goals and loops" paradigm: two loops, two goals,
both running, one is implementation convergence, one is design/UX convergence.

Advantages: clean goal model, terminates naturally, explicit convergence condition.
Disadvantage: requires more scaffolding in mm-plo-addon.

### Option C: WDS as a PLO advisory lane (light integration)

Add to PLO's lane dispatch: after Dev completes a story, before CR, a brief
WDS advisory check runs. Freya scans the story's diff, emits a one-paragraph
advisory. CR reads the advisory; if it's flagged, adds UX notes to the review.

Advantages: integrated into existing flow, UX input at the right moment.
Disadvantage: slightly slows PLO. Must be lightweight (30s scan, not a full design review).

### Recommended path

**Start with Option A** — timed loop, no coupling, proves the value. If Freya's
findings are consistently useful, evolve to Option B for WDS-goal convergence.
Option C can be a PLO lane-map entry if the advisory proves consistently non-trivial.

---

## What would go into mm-plo-addon

```
mm-plo-addon/
  skills/
    wds-loop/
      SKILL.md          — skill definition + activation steps
      customize.toml    — wds_scan_paths, wds_status_file, agent (Freya)
  docs/
    wds-loop-exploration.md   ← this file
    wds-loop-design.md        ← write after Marcel approves direction
```

The `wds-loop` skill would:
1. Load DESIGN.md + EXPERIENCE.md
2. Run `git diff HEAD~3..HEAD -- app/src/` 
3. Scan for the signal types above
4. Append a structured finding to `wds-status.md`
5. Call ScheduleWakeup for the next interval

Freya's persona (from `wds-agent-freya-ux` skill) carries through.

---

## Open questions to resolve with Marcel

1. **Advisory vs. gating**: should WDS ever block a story from reaching `done`,
   or is it always advisory? Strong opinion: advisory only. Don't slow PLO.

2. **Who acts on WDS findings**: John reads them in his 20-min loop and creates
   stories if needed? Or does Freya create a story directly in the tracker?

3. **WDS goal vs. PLO goal**: should they share a terminal (same headless session)
   or always be separate? Separate seems safer — different cadences, different contexts.

4. **Prototype workflow**: when Freya emits a prototype signal, what's the flow?
   Sally gets activated? Or Marcel reviews and decides manually?

5. **EXPERIENCE.md Chapter 2**: WDS loop has a natural relationship to the open
   Chapter 2 questions (blocked per `WDS-CONVERGENCE-STATUS.md`). Should the WDS loop
   actively drive Chapter 2 completion, or observe-only?

6. **The lint angle**: some WDS checks (hardcoded hex colors, missing `@reference`)
   are mechanical enough for a CI lint step, not a WDS loop. Worth separating
   automated lint from Freya's judgment-based advisory?

---

## Connection to the OpenAI goals/loops framing

The interesting design insight: loops and goals work best when each loop has a
*single coherent concern* and a *clear termination condition*.

PLO: concern = implementation completeness, goal = `done: X/X, churn: none`
WDS: concern = design fidelity, goal = `DESIGN.md + EXPERIENCE.md fully realized`
John: concern = PM-level risk, goal = ongoing (never terminates, runs the whole sprint)

Three loops, three concerns, one human (Marcel) watching all three. The human's job
is not execution — it's inter-loop judgment when one loop's finding should influence
another's behavior.

That's meaningfully different from the Stop hook approach: that was one loop trying
to evaluate another loop's internal state at every step. Loops should be loosely coupled
through *files and artifacts*, not through *response-level hooks*.
