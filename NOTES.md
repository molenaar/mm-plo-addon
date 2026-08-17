# Notes

Working notes for changes made outside the normal PR flow — picked up and
formalized (tests, docs, versioning, release) when you're back in this repo.

---

## 2026-08-17 (9) — tmux-menu.sh: resynced from project-scaffold (the real source of truth)

**Trigger:** After hand-editing `mm-plo-addon`'s copy in entry (8), learned
`~/project-scaffold` is the actual canonical source this tooling gets
copied from into each project — and it (along with `the-one-dca-system`'s
copy) already had a more complete `show_info()` (a "Notifying Marcel
directly" Teams/PushNotification section neither other copy had) and a
nicer `printf`-table menu format than the plain `echo` version hand-written
in entry (8).

**Fix:** Applied entry (8)'s same content changes (drop options 8–11,
fix stale PLO/PM/UX descriptions, add the two ping examples) directly onto
`project-scaffold/tmux-menu.sh` instead of maintaining independent
hand-written copies — inserted the two examples into its *existing*
cross-session-messaging writeup rather than duplicating the mechanism
explanation. Then replaced `mm-plo-addon/tmux-menu.sh` with a straight
copy of the fixed `project-scaffold` version (`bash -n` clean, byte-
identical) rather than hand-reconciling two independently-edited copies.

Not part of the addon module either way (untracked, outside `skills/`) —
no rebuild/validate needed. `project-scaffold`'s tree was clean before
this edit (fully committed); this change is uncommitted there too, same
as everything else this session.

---

## 2026-08-17 (8) — Updated tmux-menu.sh: dropped obsolete options, added ping examples

**Trigger:** Asked to bring `tmux-menu.sh` (untracked, copied in from a
sibling project's tooling — its header still said "for the-one-dca-system")
in line with today's changes, plus add worked examples of the
cross-session ping mechanism `mm-plo-orchestrator`'s Cross-Session
Coordination section documents.

**Fixes:**

1. Removed menu options 8–11 (UX Orchestrator loop, WDS party-mode, WDS
   Saga, WDS Freya) and their `SESSION_*`/`*_BOOTSTRAP_PROMPT` variables —
   all obsolete per entries (3)–(5) above (mm-ux-orchestrator removed
   entirely; WDS itself deprecated upstream). Kept options 1–7 as
   directed.
2. Option 7 (PLO)'s description dropped the stale "[Amelia: PLO dispatch,
   John as Stop hook evaluator]" bracket — replaced with what's actually
   true now: dispatches `bmad-build-auto` per lane, self-continues until
   nothing's ready.
3. Option 6 (UX)'s bootstrap prompt and description reworded — no longer
   references a "PLO handoff" concept tied to the removed skill; now
   describes Sally as ask-directly-no-loop, expecting PLO to ping her
   mid-round.
4. `PM_BOOTSTRAP_PROMPT` dropped the same stale "John evaluates round
   closure automatically" Stop-hook reference — reworded to match entry
   (7)'s actual behavior (PLO self-continues, stops when nothing's ready,
   that's the cue to talk to John).
5. `show_info()` gained two new sections: the general "Cross-session
   agent messaging" mechanism writeup (same content this addon's sibling
   project already had proven out, adapted — dropped the Teams/
   PushNotification bits since those are that project's own tooling, not
   part of this addon), and two concrete worked examples matching what
   was asked for:
   - PLO finds a technical issue mid-round → pings Mary to analyze →
     Winston (architecture) + Sally (UX) assess in parallel → John plans
     and dispatches a story → PLO picks it up next round.
   - Human discusses a UX issue with Sally → Sally pings Winston for
     technical impact → pings John to plan/dispatch → John pings PLO so
     it doesn't wait for its next tracker read.

`bash -n` clean. Not part of the module (untracked, outside `skills/`) —
no rebuild/validate needed for this file.

---

## 2026-08-17 (7) — Made multi-round self-continuation explicit; dropped /goal and John's loop

**Trigger:** Reviewing the just-trimmed "Advanced: John as goal evaluator"
section (entry (6)) surfaced the same question about the rest of the
hands-off setup: is `/goal` (mechanical Haiku pattern-match on the closure
line, used to auto-reinvoke PLO round after round) still needed, and is
John's `/loop 20m /bmad-sprint-planning` still needed either, once its own
justification ("richer than the goal evaluator alone") no longer applies?
User's actual practice: PLO already keeps going through rounds by itself
until the tracker has nothing left, at which point the user asks John
directly what to dispatch next — not on a timer, and not gated by a
mechanical goal string.

**Findings/fixes:**

1. `mm-plo-orchestrator/SKILL.md` was actually silent on whether one
   invocation self-continues across rounds — Stage 5 closes one round and
   emits the closure line "so the goal evaluator can read it," implying an
   *external* mechanism was needed to keep going. That was the gap `/goal`
   was patching. Made it explicit instead: added a "Continuing across
   rounds" note after Stage 5 — go back to Stage 1 automatically after
   closing a round; only Stage 2's "nothing active" case (or a QA
   gate/churn stall) stops it. This is what actually makes `--headless`
   hands-off across a whole batch, with zero external loop machinery.
2. Dropped `/goal` from README's Terminal 1 example — redundant now that
   self-continuation is the documented behavior, not an emergent one.
   `--headless` itself is unaffected and still does exactly what it always
   did (skip interactive prompting, return structured JSON).
3. Dropped John's `/loop 20m /bmad-sprint-planning` — same reasoning as
   the UX loop cut (entry (4)): a timer that fires whether or not there's
   anything new to report, in a terminal that might be busy with something
   else, when the actually useful moment to check with John is exactly
   when PLO stops (nothing active) — a natural pause point, not a clock.
   Terminal 2 is now just "load `/bmad-agent-pm`, ask him when you want a
   read."
4. Following from that: restructured the tutorial's terminal setup from
   the fixed "Terminal 1 / Terminal 2" framing to the user's actual
   practice — five terminals (PLO, John, Mary, Winston, Sally), none
   looping, only PLO's terminal strictly required for running rounds. The
   rest are kept open for ad hoc consultation and Cross-Session
   Coordination pings, not because round-execution mechanically needs
   them. README's Terminal 2 section gained a short pointer to the same
   fuller picture without fully restructuring its own numbered layout.
5. Tutorial steps 6–7 reworded to match: "the round closes" → "each round,
   and when it stops," describing multi-round continuation as the default
   and framing a stop as a cue to consult John, not a per-round checkpoint.
   Removed the now-fully-redundant "Going hands-off (optional)" section
   entirely (its content was exactly `/goal`, already cut above).

Rebuilt; installed copy matches source exactly.

---

## 2026-08-17 (6) — Moved the deferred goal-evaluator section out of README (KISS)

**Problem:** `README.md` carried a ~35-line "Advanced: John as the goal
evaluator" section — explicitly marked *"currently not working... no
solution exists for this yet... do not configure this in active
projects"* — sitting in the primary onboarding doc every new reader
scrolls past. Dead weight for a feature nobody can turn on, same class of
cut as everything else today.

**Fix:** Trimmed README to one line pointing here. Full detail preserved
below for whoever picks the idea back up later — the point of moving it,
not deleting it, is that the failure mode itself is worth keeping:

> By default `/goal` uses a small fast model (Haiku) to check the closure
> line — mechanical pattern matching. For a richer check, the idea was to
> wire John as a custom [prompt-based Stop
> hook](https://code.claude.com/docs/en/hooks-guide#prompt-based-hooks) in
> the project's `.claude/settings.json`, so he evaluates whether acceptance
> criteria are *genuinely* met (he wrote them) instead of just technically
> passing:
>
> ```json
> {
>   "hooks": {
>     "Stop": [{
>       "matcher": "^ROUND \\d+ \\|",
>       "hooks": [{
>         "type": "prompt",
>         "prompt": "<paste workflow.goal_evaluator_prompt from customize.toml>"
>       }]
>     }]
>   }
> }
> ```
>
> The `matcher` is critical — `^ROUND \\d+ \\|` matches only the
> standardized closure line Stage 5 emits (`ROUND 3 | done: 4/6 | ...`).
> Without it the hook fires on every response in every session, including
> John's own PM session and any session that reads a `round-summary.md`
> file. With this in place, the idea was to drop `/goal` from Terminal 1
> and just run `/mm-plo-orchestrator --headless` — John would wake up
> after every round automatically, apply PM-level judgment, and keep PLO
> running until satisfied.
>
> **Why it's deferred:** the prompt-based Stop hook fires *inside John's
> own PM terminal session* (Terminal 2) when it stops, but that session
> never terminates cleanly as a result — it causes an endless loop. No
> workaround found yet. If Claude Code's hooks model changes (e.g. a way
> to scope a Stop hook to a different session than the one it fires in),
> revisit this.

---

## 2026-08-17 (5) — Removed mm-ux-orchestrator entirely; addon is PLO-only again

**Trigger:** Immediately after the on-demand rework (entry below), asked
whether the skill is still useful at all — established the user's actual
workflow never uses it: they run WDS's own `wds-agent-freya-ux` live in
its own terminal (tmux option 11) during ongoing projects, and separately
confirmed a general aversion to self-scheduling loops in principle ("a
loop is annoying when an agent is busy and it can't be stopped by the
agent" — not specific to this skill). Once both the design-judgment half
*and* the loop mechanism were off the table, decided to remove the skill
rather than keep a stripped-down remainder — options 9/10/11 (WDS
partymode/Saga/Freya) in the tmux menu are obsolete too, alongside it.

**Fix:** `mm-plo-addon` is single-skill again (`mm-plo-orchestrator` only).

1. Deleted `skills/mm-ux-orchestrator/` and `skills/mplo-setup/` entirely.
2. Reverted the module to the **standalone self-registering** pattern —
   correct per `create-module.md` for a single-skill module (the
   dedicated-`-setup`-skill pattern from entry (2) below was only correct
   while there were two skills to register). Wrote `assets/module.yaml`
   and `assets/module-help.csv` back into `mm-plo-orchestrator/assets/`,
   ran `scaffold-standalone-module.py` to restore `assets/module-setup.md`
   and the merge scripts, and reverted `SKILL.md`'s Step 0 to
   self-registration.
   - Caught and fixed a bug in that scaffold script: with `--marketplace-
     dir` pointing at the repo root (not the skill's own parent, since the
     skill lives nested under `skills/`), it wrote `"skills": ["./mm-plo-
     orchestrator"]` into `marketplace.json` — dropping the `skills/`
     path segment. Fixed by hand to `"./skills/mm-plo-orchestrator"`,
     matching the actual repo layout.
3. `README.md` and `docs/tutorial.md`: removed all `mm-ux-orchestrator`/
   Sally/UX-terminal content — "two skills" → one, "three terminals" →
   two, Terminal 3 section gone, Install/Update instructions reverted to
   `mm-plo-orchestrator setup`/`configure`. Kept the Cross-Session
   Coordination pointer (PLO can still ping *whatever* UX persona terminal
   the user happens to be running, unrelated to whether this addon ships
   one). Also swept three stale "Amelia" references in README left over
   from the `bmad-build-auto` dispatch fix (entry (1) below) that hadn't
   been caught yet — PLO doesn't route through her anymore, so "Amelia
   advances lanes" reads wrong now.

Re-validated: clean pass, standalone module detected correctly, 0
findings. Rebuilt; installed copy matches source exactly.

---

## 2026-08-17 (4) — Retired the self-scheduling loop; mm-ux-orchestrator is now on-demand only

**Trigger:** After the Freya→Sally rework (entry below), asked whether
`mm-ux-orchestrator` is still useful at all, since the user's actual
workflow never runs `/loop 40m /mm-ux-orchestrator` — they run WDS's own
`wds-agent-freya-ux` live in its own terminal during ongoing projects, and
ask PLO to ping that session (or John) when something needs discussing.
Established: the *design-judgment* half of this skill (signals 3b–6) is
genuinely redundant with that live practice — a human discussing it with
Sally beats a scripted advisory block. The *deterministic scan* half
(`scan-signals.py`: hex drift, missing `@reference`, new pages) isn't —
mechanical diff-checking a live conversation doesn't replace, and it's
independent of the `wds` module (works off this addon's own `DESIGN.md`
convention), so it isn't going obsolete alongside WDS's deprecation either.

**Decision (user):** drop the self-scheduling loop machinery entirely, on
principle beyond just this skill — "a loop is annoying when an agent is
busy and it can't be stopped by the agent." Keep the check, make it strictly
on-demand: ask for one when one is wanted (a human, or PLO pinging the UX
session mid-round), never autonomous.

**Implementation:** `mm-ux-orchestrator/SKILL.md` — removed the `ScheduleWakeup`
call and its "self-schedule unavailable" fallback note from the former
Step 6 (now just "Write finding," no "and schedule next run"). Step 2's
"skip the greet/menu, this is an unattended loop activation" line reworded
to "one-shot check invocation." Frontmatter description reworded from loop
framing ("Use when running /loop /mm-ux-orchestrator or /loop 40m
/mm-ux-orchestrator") to ad hoc framing ("invoke when a check is wanted...
Not a self-scheduling loop"). Cascaded into `mplo-setup/assets/module.yaml`
and `module-help.csv` (renamed the `UX` row from "Run UX Orchestration
Loop" to "Run UX Drift Check"), `README.md`'s intro paragraph, skill
listing, and Terminal 3 section (no longer a standing loop terminal — just
ask Sally for a check in whichever terminal she's already running), and
`docs/tutorial.md`'s equivalent table row and prose.

Re-validated: clean pass, 0 findings. Rebuilt; installed copy matches
source exactly.

---

## 2026-08-17 (3) — Retired the separate "Freya" persona; mm-ux-orchestrator now runs as Sally directly

**Trigger:** While testing the mplo update in `courseware-schedule`
(entry below), the installer's WDS deprecation notice led to checking that
project's `wds` module — which ships its own agent, `wds-agent-freya-ux`
("Freya — WDS Designer"), unrelated to this addon's `mm-ux-orchestrator`
persona (also named Freya). In a project with both `mplo` and `wds`
installed, "talk to Freya" was genuinely ambiguous between two different
personas with different jobs.

**Decision (user):** don't just rename to dodge the collision — retire the
separate coordinator persona entirely. The loop should run *as* Sally
(`bmad-agent-ux-designer`) directly, not as a different character who then
delegates to her. User confirmed the skill's trigger name/invocation
(`/mm-ux-orchestrator`, `/loop 40m /mm-ux-orchestrator`) stays unchanged —
only the persona it adopts changes.

**Implementation:**
1. `mm-ux-orchestrator/customize.toml` — removed the hardcoded `[agent]`
   block (name Freya, icon 🔍, etc.) entirely. Kept `[workflow]` unchanged.
2. `mm-ux-orchestrator/SKILL.md` — rewritten: a new Step 2 resolves Sally's
   own `[agent]` block dynamically via
   `resolve_customization.py --skill {path to bmad-agent-ux-designer} --key agent`
   (same merge mechanism any BMad agent uses for its own customization,
   just pointed at a sibling skill's directory instead of its own). Every
   persona-identity reference in the doc (finding-block headers, sign-offs,
   `ScheduleWakeup` reason) now uses `{agent.name}`/`{agent.icon}` resolved
   at runtime instead of a hardcoded "FREYA".
3. Also fixed, same trip: the old design invoked `bmad-agent-ux-designer`
   via the **Skill tool** for design judgment (old Step 4, "Delegate to
   Sally") — that re-triggers her full interactive activation (greet,
   render menu, wait for input), the exact same anti-pattern already fixed
   for PLO/Amelia earlier today. New Step 5 applies the judgment inline,
   under the resolved persona, with no nested persona-adoption call.
4. Cascaded into `mplo-setup/assets/module.yaml` (removed the `agents:`
   roster entry — this skill no longer declares its own agent identity)
   and `module-help.csv` (reworded the `UX` row's description).
5. `README.md` and `docs/tutorial.md` Terminal 3 sections updated: no
   longer need to load `/bmad-agent-ux-designer` in the terminal before
   `/loop 40m /mm-ux-orchestrator` — the loop resolves her identity itself.
   (This also retroactively explains why the old two-step terminal
   sequence never actually connected: the terminal's own persona-load was
   never consumed by Freya's internal, separate Skill-tool call to Sally —
   two disconnected Sally-adoptions were happening either way.)
6. Also swept `docs/tutorial.md`'s Terminal 1/2 rows and a stale
   "lanes the orchestrator dispatches" paragraph that still described
   `bmad-agent-dev`/`bmad-code-review`/`bmad-qa-generate-e2e-tests` as a
   fixed three-lane chain — same staleness class as the README fixes from
   entry (1) below, just missed on the first pass since tutorial.md wasn't
   re-read then.

Re-validated (`bmad-module-builder` Validate Module): clean pass, 0
findings. Rebuilt via `scripts/rebuild-module.sh`; diffed installed vs.
source for all three touched files — exact match.

---

## 2026-08-17 (2) — Re-scaffolded mplo as a proper multi-skill module

**Problem:** Ran `bmad-module-builder`'s Validate Module against `mplo`
after the SKILL.md edits earlier today (see entry below). It failed when
pointed at `skills/` — no dedicated `*-setup` skill, and the module was
using the *standalone self-registering* pattern (`module.yaml`/
`module-help.csv`/`module-setup.md` embedded in
`mm-plo-orchestrator/assets/`). That pattern is only correct for
genuinely single-skill modules per current `create-module.md` convention
("if multiple skills detected... generate a dedicated `-setup` skill").
This addon has had two skills (`mm-plo-orchestrator` +
`mm-ux-orchestrator`) for a while — the standalone pattern predates
`mm-ux-orchestrator`'s addition and was never migrated. Concretely, this
meant `mm-ux-orchestrator` had zero help-catalog entries and no place in
the module's own roster — discoverable only by direct invocation, not via
`bmad-help` or the module menu.

**Fix:** Re-scaffolded per the official
[distribute-your-module](https://bmad-builder-docs.bmad-method.org/how-to/distribute-your-module/#single-module-repository)
layout, at the user's explicit direction after they linked it:

1. `scaffold-setup-skill.py` generated `skills/mplo-setup/` — module
   identity, both skills' capabilities (`OR` for sprint rounds, new `UX`
   for the UX loop), and an `agents:` roster entry for Freya
   (`mm-ux-orchestrator` has an `[agent]` block in its `customize.toml`;
   `mm-plo-orchestrator` is workflow-only, no roster entry).
2. Removed the superseded standalone files from
   `mm-plo-orchestrator/assets/` and `/scripts/` (both now-empty dirs
   removed).
3. `mm-plo-orchestrator/SKILL.md` Step 0 no longer self-registers — it
   points users to `mplo-setup` instead.
4. `module_version` bumped `1.3.0` → `1.4.0` in the new `module.yaml`,
   matching what the installed manifest and `marketplace.json` already
   tracked (a version-drift finding from the first validation pass).
5. `.claude-plugin/marketplace.json`'s `skills` array and `README.md`'s
   install instructions updated to reference `mplo-setup`.

Re-ran validation: clean pass, 0 findings, both skills registered. Full
report: `skills/reports/module-validation-mplo-2026-08-17.md`. Verified via
`scripts/rebuild-module.sh` (see below) that `.claude/skills/mplo-setup`
installs correctly and the old registration files are gone from the
installed copy too.

**Also found and fixed while rebuilding:** `scripts/rebuild-module.sh`
(added earlier today) was silently no-op-ing — `--custom-source .`
(relative path) fails to resolve (`Not a valid Git URL or local path`),
so the installer fell back to a stale cached copy instead of reading
today's source edits. Fixed by resolving to an absolute path before
passing it. Confirmed with a diff: installed and source `SKILL.md` now
match exactly.

**Committed this session:** nothing — working tree only, per this repo's
usual practice of leaving hand-edited-outside-PR-flow changes uncommitted
for review.

---

## 2026-08-17 (1) — Reconciled mm-plo-orchestrator with BMad 6.11.0's build overhaul

**Problem:** Hadn't touched this addon in a while; BMad's core update
(6.8.0 → 6.11.0) changed the implementation phase drastically.
`bmad-dev-story`/`bmad-quick-dev`/`bmad-create-story` are now deprecated
shims; `bmad-build` (interactive) and `bmad-build-auto` (unattended) are
canonical, and both bake an adversarial review (Blind Hunter, Edge Case
Hunter, Verification Gap Reviewer, +1) directly into the workflow —
`bmad-code-review` is a separate, standalone skill reusing the same engine,
not a step `bmad-build` calls into. Quinn and Paige are gone from BMad
upstream (Quinn's QA role folded into the build/review loop; Paige is on
hiatus) — confirmed neither name was ever referenced in this addon's own
skills, so no cleanup needed there.

**Root issue found:** `mm-plo-orchestrator`'s Dispatch stage still pointed
implementation lanes at `bmad-agent-dev` (the Amelia persona). Her own menu
(`bmad-agent-dev/customize.toml`) routes to the *interactive* `bmad-build`,
which halts at checkpoints waiting for a human — but a dispatched lane has
none. Every round would have stalled mid-lane. Confirmed via `sprint-status.
yaml` from a sibling project (`the-one-dca-system`) that PLO's only real
input is the tracker, and that UX findings (`ux-status.md`) reach PLO only
by John translating them into tracker stories/AC holds — never read by PLO
directly. An earlier attempt at this session to have PLO scan `ux-status.md`
itself for a matching "drift flag" protocol was invented, not verified, and
was reverted once checked against real tracker data.

**Fixes applied**, all in `skills/mm-plo-orchestrator/SKILL.md` and
`skills/mm-ux-orchestrator/SKILL.md`:

1. Dispatch now targets `bmad-build-auto` directly (bypassing the Amelia
   persona), in its folder+id mode — passing `{spec_folder}`/`story_id` from
   the tracker, and reading `stories.yaml`'s `spec_checkpoint`/
   `done_checkpoint`/`invoke_dev_with` fields rather than deciding checkpoint
   behavior itself.
2. `bmad-code-review` is no longer a standing "review lane" — `bmad-build-
   auto` already runs the equivalent review inline and reports
   `followup_review_recommended`; Collect & Gate now dispatches
   `bmad-code-review` only when that flag is `true`.
3. `bmad-sprint-status` (deprecated, emits a notice every call) replaced
   with `bmad-sprint-planning` in headless `status` intent, in both Read
   Tracker and the tracker-refresh dispatch bullet.
4. Added a Cross-Session Coordination section (`ListAgents`/`SendMessage`
   between live Claude Code sessions, human-in-the-loop by design) and a
   Drift Flags convention in `mm-ux-orchestrator` for John to translate a
   contract-drift finding into tracker state.
5. `README.md`'s suggested 2-terminal setup updated to match: Terminal 1 no
   longer loads `/bmad-agent-dev` first (PLO dispatches `bmad-build-auto`
   directly now), Terminal 2's `/bmad-sprint-status` → `/bmad-sprint-
   planning`.

New doc: `docs/build-integration.md` — full diagram (verified against the
actual installed `bmad-build-auto` step files and the official BMad Build
diagram, not the docs site's prose summary, which had the triage categories
slightly wrong) and explanation of why the orchestrator layer is still
needed post-6.11.0.

**Open, not resolved this session:**
- `bmad-agent-ux-designer` (Sally)'s own menu wasn't checked for the same
  interactive-default trap Amelia's had — user doesn't work with Sally
  directly enough for this to matter right now.
- Point #1 from the kickoff discussion (agents forgetting to check
  `lane-map.yaml`, defaulting to `sprint-status.yaml` only) — not addressed.
- The official BMad Build diagram shows `DEFER → deferred_work.md` (a file);
  the installed `step-04-review.md` writes defers into the spec's own
  `deferred:` frontmatter instead. Flagged in `docs/build-integration.md`,
  not reconciled — possibly still in flux upstream.

Working tree only — not committed, not pushed, not run through this repo's
own verification pass.

---

## 2026-07-11 — Manual verification lane for repos with no test infra

**Problem:** Running `mm-plo-orchestrator` headlessly against `flow-platform`
(Epic 10, stories 10-1 and 10-3), Stage 3's dispatch table only had one QA
skill: `bmad-qa-generate-e2e-tests`. That repo has no e2e/automated test
infrastructure at all. Dispatching the skill anyway would have meant standing
up a whole test framework mid-round as a side effect of one story's QA pass —
clearly out of scope. Skipping the QA gate silently would have been worse
(both stories stayed at `review` status specifically *because* no QA gate had
run — see the round's `closure-notes.md` in `flow-platform/_bmad-output/
orchestration/mm-plo-orchestrator-flow-platform-2026-07-11/`). Neither option
was in the skill's own vocabulary — it just didn't model "QA without test
infra" as a lane type.

**Solution applied (uncommitted, this repo):** Edited
`skills/mm-plo-orchestrator/SKILL.md`, Stage 3 ("Dispatch"). Diff:

```diff
 - `bmad-agent-dev` for implementation lanes
 - `bmad-code-review` for review lanes
-- `bmad-qa-generate-e2e-tests` for test lanes
+- `bmad-qa-generate-e2e-tests` for test lanes, **only when e2e/automated test infrastructure already exists in the target repo**
 - `bmad-retrospective` for retrospective lanes (pass: epic name, completed story list, round summaries for that epic)
 - `bmad-sprint-status` when the tracker needs to be refreshed
 
+**No test infrastructure yet:** if a story needs a QA lane but the repo has no e2e/automated test infrastructure, do not stand one up mid-round as a side effect of one story's QA pass, and do not silently skip the gate either. Dispatch a **manual verification lane** instead — no upstream skill; derive a short verification checklist from the story's acceptance criteria (or its dev-round evidence, if that's the only spec context available) and either execute it directly (e.g. exercise the endpoint/flow against a local dev stack) or hand it to the user as an explicit next step. Record the result the same way as any other lane (pass/needs-fix/blocked + evidence), and surface the missing test infrastructure itself as a backlog candidate for John/the user to decide on — it is a gap to flag, not a decision this skill makes unilaterally.
+
 Dispatch independent lanes in parallel when dependencies allow. Do not copy core lane logic into this skill; orchestrate it.
```

Working tree only — not committed, not pushed, not run through this repo's
own verification.

**Follow-up (for Marcel, next time in this repo):**
1. Run the full BMad module verification pass on this change before it ships
   (whatever that normally covers here — eval-runner, `bmad-customize`
   consistency check, etc.; I haven't run any of it from the `flow-platform`
   session).
2. Decide whether Stage 4 ("Collect & Gate") and the Stage 5 "Status
   write-back" rule need matching language — right now they say generically
   "QA gate" / "passed the QA gate," which already reads fine against a
   manual-verification result, but worth a second look once the Stage 3
   wording is final.
3. Consider whether the manual-verification-lane checklist format should be
   specified more concretely (right now it's "derive a short checklist from
   the story's ACs" — loose by design, but may want a template once a couple
   of real rounds have used it).
4. Once verified, sync into `flow-platform`'s installed copy
   (`.claude/skills/mm-plo-orchestrator/SKILL.md` — currently byte-identical
   to this repo's pre-change version) via whatever the normal install/update
   path is.
5. Related, smaller finding from the same session: this repo's own
   `docs/operations/lane-map.yaml` ships empty (documented as intentional —
   "a real project populates it once epics and stories exist"). No action
   needed here; `flow-platform`'s copy was populated directly in that repo.
