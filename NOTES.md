# Notes

Working notes for changes made outside the normal PR flow — picked up and
formalized (tests, docs, versioning, release) when you're back in this repo.

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
