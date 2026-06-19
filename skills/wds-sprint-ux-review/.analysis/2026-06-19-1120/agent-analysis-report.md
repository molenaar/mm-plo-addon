# Analysis Report: wds-sprint-ux-review

Generated: 2026-06-19T11:20:00 · Schema: 2

**Grade: Good**

> Good: determinism split is clean, persona is investment, one high (missing-doc guard) and three medium findings to address.

Freya's persona, output contract, and script/judgment split are the agent's clear strengths — the determinism lens found nothing and the leanness lens found one low-severity prose trim. The main opportunity is defensive guards: DESIGN.md or EXPERIENCE.md absent at activation causes silent failure or hallucination, and ScheduleWakeup unavailability stops the loop with no signal. Secondary: a Step 3 parallelization claim is inaccurate (git command listed alongside file reads), and the wds-loop-exploration.md normative reference is never actually loaded.

| Severity | Count |
| --- | --- |
| Critical | 0 |
| High | 3 |
| Medium | 4 |
| Low | 7 |

## Themes

### 1. Missing input guards

- Root cause: No existence checks before consuming reference docs or calling environment tools — absent files or unavailable ScheduleWakeup fail silently or stop the loop invisibly.
- Fix: Add guards at the top of Step 3 (check DESIGN.md and EXPERIENCE.md exist, emit WARN and skip DR if absent) and at the end of Step 5 (ScheduleWakeup fallback note if unavailable). Add cold-start diff_range guard in Step 2.
- Findings:
  - `enhancement-1` Missing DESIGN.md or EXPERIENCE.md causes silent failure or hallucination — `SKILL.md — Step 3: Load reference context`
  - `enhancement-3` ScheduleWakeup assumed available — no fallback — `SKILL.md — Step 5`
  - `enhancement-4` Cold-start diff_range errors on repos with fewer than 3 commits — `SKILL.md — Step 1 defaults / Step 2`

### 2. Inaccurate Step 3 parallelization

- Root cause: git diff is a shell command, not a file read — listing it in the 'Read in parallel' block is structurally incorrect and will confuse the executing model.
- Fix: Split Step 3: run git diff first (separate Bash call), then read DESIGN.md and EXPERIENCE.md in parallel.
- Findings:
  - `architecture-1` git diff command listed alongside file reads in 'Read in parallel' block — `SKILL.md — Step 3`

### 3. Dangling normative reference

- Root cause: wds-loop-exploration.md is cited as the signal authority in the Overview but is never loaded in any activation step — the inline definitions in SKILL.md and design-fidelity-review.md are complete, making the reference misleading.
- Fix: Remove the reference sentence from the Overview, letting the inline signal definitions stand as canonical.
- Findings:
  - `agent-cohesion-2` wds-loop-exploration.md referenced but never loaded — `SKILL.md — Overview`

### 4. Minor surface polish

- Root cause: Several low-effort cleanups that individually cost little but collectively reduce friction for future maintainers and first-timers.
- Fix: Trim Signal 4 negative-scope prose; add {project-root} prefix to scan_paths; annotate signal-3 table split; add persistent_facts default; add stdout confirmation on Step 5; add missing-key fallback note to Step 1.
- Findings:
  - `leanness-1` Signal 4 negative-scope prose is prescriptive teaching — `references/design-fidelity-review.md — Signal 4`
  - `customization-1` Missing persistent_facts default glob — `customize.toml`
  - `customization-2` scan_paths is a bare relative path without {project-root} prefix — `customize.toml`
  - `agent-cohesion-1` Capability table obscures signal-3 split — `SKILL.md — Capabilities table`
  - `enhancement-5` Headless output path not discoverable by callers — `SKILL.md — Step 5`
  - `enhancement-6` Step 1 fallback doesn't document missing-key behavior — `SKILL.md — Step 1`

## Strengths

- Freya's persona is precise and distinctive — voice, finding format, and communication style are investment and were treated as such throughout all lenses.
- Determinism split is exemplary — scan-signals.py correctly owns all deterministic work (hex drift, @reference check, new page detection) with 12 passing unit tests; design-fidelity-review.md correctly owns all judgment signals.
- Customize.toml surface is correctly scoped: [agent] metadata block present, [workflow] scalars named by purpose, no forbidden mechanisms.
- Output contract is clear and durable: one timestamped append per activation, a defined clean-pass format, advisory-only posture.

## Recommendations

1. Add missing-doc guard in Step 3: check {workflow.design_doc} and {workflow.experience_doc} exist before loading; if either is absent, append a WARN line to wds-status.md and skip Step 4. (resolves: enhancement-1)
2. Fix Step 3 structure: move git diff to its own Bash call before the parallel file reads, so 'Read in parallel' refers only to actual file reads. (resolves: architecture-1)
3. Remove the wds-loop-exploration.md normative reference sentence from the Overview — the inline definitions are complete and the reference implies an authority that is never consulted. (resolves: agent-cohesion-2)
4. Add ScheduleWakeup fallback note to Step 5: if unavailable, emit a reminder line to wds-status.md so the loop failure is observable. (resolves: enhancement-3)
5. Add persistent_facts default glob to customize.toml and prefix scan_paths with {project-root}/. (resolves: customization-1, customization-2)
6. Annotate capability table signal-3 split as 3a/3b; trim Signal 4 negative-scope prose; add cold-start diff_range guard; add Step 1 missing-key fallback note; add stdout path confirmation to Step 5. (resolves: agent-cohesion-1, leanness-1, enhancement-4, enhancement-6, enhancement-5)

## Agent Profile

- Name: Freya
- Title: UX Design Reviewer
- Type: stateless
- Mission: Scan git diffs against DESIGN.md and EXPERIENCE.md every 40 minutes, catch design fidelity drift before it calcifies, and append a timestamped advisory finding to wds-status.md.

## Capabilities

- **Deterministic scan (SC)** (script) — scan-signals.py — hex drift, missing @reference, new pages detection across .astro/.ts/.js/.css
- **Design fidelity review (DR)** (prompt) — design-fidelity-review.md — House integration, missing Sally dossiers, protagonist journey drift, prototype trigger

## Per-Lens Verdicts

- **leanness**: Lean. Activation steps qualify under the operational-cost exception; persona is untouched. One low finding on Signal 4 negative-scope prose.
- **architecture**: Mostly sound. One inaccuracy: git diff command listed as a parallel read alongside file reads — it is a shell invocation and cannot batch with file reads.
- **determinism**: Clean. The script/judgment split is correct and well-enforced — scan-signals.py owns all deterministic work, design-fidelity-review.md owns all judgment.
- **customization**: Clean structure. Two findings: missing persistent_facts default glob (medium), bare relative scan_paths without {project-root} prefix (low).
- **enhancement**: Six findings. One high: no guard for absent DESIGN.md/EXPERIENCE.md. Two medium: large-diff ceiling undefined, ScheduleWakeup availability assumed.
- **agent-cohesion**: Coherent. Two minor findings: signal-3 split not legible from the capabilities table alone; wds-loop-exploration.md referenced but never loaded.

## Experience

- **Normal 40-min pass** — Resolve config → run scan-signals.py → load DESIGN.md + EXPERIENCE.md + diff → run DR capability → append finding → ScheduleWakeup
- **Clean pass (no changes)** — scan JSON returns no_changes:true → skip Step 4 → append clean-pass line → ScheduleWakeup
- **First run on fresh repo** — HEAD~3 may not exist → git diff errors → currently undefined behavior
- Headless: No explicit headless path — output goes to wds-status.md regardless; stdout confirmation of output path is absent

## Findings

### High (3)

#### enhancement-1 — Missing DESIGN.md or EXPERIENCE.md causes silent failure or hallucination

- Lens: enhancement
- Location: `SKILL.md — Step 3: Load reference context`
- Evidence: Step 3 reads {workflow.design_doc} and {workflow.experience_doc} with no existence guard. If either is absent the DR capability runs against empty context and may emit spurious 'None detected' results.
- Recommendation: Check both files exist before Step 3. If either is absent, append a WARN line to wds-status.md and skip Step 4: '[TIMESTAMP] FREYA — WARN. {doc} not found at {path}. UX review skipped this pass.'

#### lint-1 — .memlog.md at skill root flagged by path-standards scanner

- Lens: lint
- Location: `.memlog.md`
- Evidence: Scanner expects only SKILL.md at root; .memlog.md is a builder process artifact placed here per build-process.md convention ({target-agent-path}/.memlog.md). Known false positive.
- Recommendation: No action — this is a builder artifact placed by convention. The scanner does not distinguish builder artifacts from progressive-disclosure content.

#### lint-2 — uv not found on PATH — ruff linting skipped

- Lens: lint
- Location: `scripts/scan-signals.py`
- Evidence: uv is not installed in this environment; ruff could not run. No lint issues were reported for the lines that were checked.
- Recommendation: Install uv to enable ruff. No code changes needed.

### Medium (4)

#### architecture-1 — git diff command listed alongside file reads in 'Read in parallel' block

- Lens: architecture
- Location: `SKILL.md — Step 3`
- Evidence: git diff is a shell invocation and cannot be issued in the same parallel batch as file reads. Listing it in the 'Read in parallel' block is structurally inaccurate.
- Recommendation: Split Step 3: run git diff as a separate Bash call first, then read DESIGN.md and EXPERIENCE.md in parallel.

#### customization-1 — Missing persistent_facts default glob

- Lens: customization
- Location: `customize.toml`
- Evidence: No persistent_facts entry is present. The BMad default glob file:{project-root}/**/project-context.md is absent, so Freya activates with no ambient project context.
- Recommendation: Add persistent_facts = ["file:{project-root}/**/project-context.md"] to customize.toml.

#### enhancement-2 — Large-diff behavior undefined — no file-count ceiling

- Lens: enhancement
- Location: `SKILL.md — Step 3 / Step 4`
- Evidence: Step 3 loads the raw diff with no size guard. A diff touching 50+ files (dependency upgrade, generated assets) will push excessive tokens into Step 4 and may produce noise findings.
- Recommendation: Add a file-count heuristic: if diff touches more than ~30 files, note the cap in the finding header. The deterministic scan already filters by path; the judgment scan should mirror that discipline.

#### enhancement-3 — ScheduleWakeup assumed available — no fallback

- Lens: enhancement
- Location: `SKILL.md — Step 5`
- Evidence: Step 5 calls ScheduleWakeup unconditionally. If unavailable (some CI environments, remote agents), the loop stops self-scheduling silently.
- Recommendation: Add fallback note: if ScheduleWakeup is unavailable, append '[TIMESTAMP] FREYA — NOTE. Self-schedule unavailable; re-invoke manually with /loop 40m /wds-sprint-ux-review.'

### Low (7)

#### agent-cohesion-2 — wds-loop-exploration.md referenced but never loaded

- Lens: agent-cohesion
- Location: `SKILL.md — Overview`
- Evidence: The Overview cites docs/wds-loop-exploration.md as the signal authority but no activation step reads it. The inline definitions in SKILL.md and design-fidelity-review.md are complete, making the reference misleading.
- Recommendation: Remove the reference sentence and let the inline signal definitions stand as canonical.

#### customization-2 — scan_paths is a bare relative path without {project-root} prefix

- Lens: customization
- Location: `customize.toml`
- Evidence: scan_paths = "src/" resolves relative to the working directory. All other scalars use {project-root}/. Silently wrong if invoked from a non-root directory.
- Recommendation: Change to scan_paths = "{project-root}/src/" and update the script invocation and fallback git command. Or document that invocation must be from project root.

#### leanness-1 — Signal 4 negative-scope prose is prescriptive teaching

- Lens: leanness
- Location: `references/design-fidelity-review.md — Signal 4`
- Evidence: 'Static cards, text blocks, and simple display components do not warrant dossiers; use judgment. The bar is whether...' — the counter-example list unpacks judgment the model applies correctly from the positive criterion alone.
- Recommendation: Cut the two explanatory sentences; keep only the bar sentence: 'Bar: would a developer need a spec to implement the interaction correctly?'
- Proposed smallest: **Signal 4 — Missing Sally dossier**: When the diff introduces or substantially changes a non-trivial interactive `.astro` or `.ts` component in `src/components/` — state machines, multi-step flows, complex transitions, anything Sally would need to wireframe — check whether a corresponding file exists in `{workflow.component_dossiers}`. Flag if absent. Bar: would a developer need a spec to implement the interaction correctly?
- Predicted delta: ~1 token saved on inference noise; eliminates anchoring risk from the counter-example list without changing true-positive recall.

#### agent-cohesion-1 — Capability table obscures signal-3 split

- Lens: agent-cohesion
- Location: `SKILL.md — Capabilities table`
- Evidence: Signal 3 appears in both SC and DR rows without indicating they are two halves — 'new-page detection' and 'House integration' — so the table implies duplication rather than a deliberate split.
- Recommendation: Annotate as 3a (new-page file detection) in SC and 3b (House nav integration) in DR.

#### enhancement-4 — Cold-start diff_range errors on repos with fewer than 3 commits

- Lens: enhancement
- Location: `SKILL.md — Step 1 defaults / Step 2`
- Evidence: HEAD~3 does not exist on a repo with fewer than 3 commits. git diff HEAD~3..HEAD will error on first run of a new project.
- Recommendation: Guard: if git rev-list --count HEAD < 3, fall back to git diff $(git rev-list --max-parents=0 HEAD)..HEAD.

#### enhancement-5 — Headless output path not discoverable by callers

- Lens: enhancement
- Location: `SKILL.md — Step 5`
- Evidence: When called from automation, the caller has no machine-readable confirmation of where the finding was appended — the status_file path is resolved at runtime from customize.toml and never echoed.
- Recommendation: Emit one stdout line at end of Step 5: 'FREYA: finding appended to {resolved_status_file_path}'. Does not pollute wds-status.md.

#### enhancement-6 — Step 1 fallback doesn't document missing-key behavior

- Lens: enhancement
- Location: `SKILL.md — Step 1`
- Evidence: The fallback says 'read customize.toml directly' but doesn't instruct Freya what to do if a key is absent. An absent key leaves the variable as an unresolved template string.
- Recommendation: Add one sentence: 'If a key is absent from customize.toml, use the default from the table above.'
