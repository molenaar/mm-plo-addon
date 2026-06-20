# Analysis Report: skills/mm-ux-orchestrator

Generated: 2026-06-20T07:29:00Z · Schema: 2

**Grade: Good**

> Well-structured stateless orchestration skill with two fixable runtime gaps (Sally fallback, missing directory guard) and one orphan reference file; the rich Freya persona was treated as investment throughout.

mm-ux-orchestrator is a clean, purposeful stateless skill with the right shape: Freya coordinates, Sally judges, WDS scan is correctly gated on DESIGN.md presence. Two medium gaps exist at the edges of dependency resolution — no fallback when Sally is unavailable, and no directory creation guard before the status file write. Five scanner highs are all environmental or archival noise (old analysis artifacts, missing uv, misclassified memlog) and do not reflect on the skill's source files.

| Severity | Count |
| --- | --- |
| Critical | 0 |
| High | 5 |
| Medium | 5 |
| Low | 7 |

## Themes

### 1. Delegation resilience

- Root cause: Freya delegates to Sally and writes to a file path — both dependencies can fail silently with no recovery path defined.
- Fix: Add two guards: (1) in Step 4, if bmad-agent-ux-designer is unavailable, append a WARN line and include only signals 1–3a from scan results; (2) in Step 5, run a Bash mkdir -p on the status_file parent directory before writing.
- Findings:
  - `enhancement-1` Step 5 does not create parent directory before writing status_file — `SKILL.md:Step 5`
  - `enhancement-2` No fallback when bmad-agent-ux-designer (Sally) is unavailable — `SKILL.md:Step 4`
  - `cohesion-1` Sally unavailability creates a dead-end in the end-to-end journey — `SKILL.md:Step 4`

### 2. Orphan content

- Root cause: Two items in the skill tree carry no live reference: prompt-quality-canon.md is not loaded by any step, and the capabilities table restates step content already in scope.
- Fix: Remove prompt-quality-canon.md from the skill (or add a load instruction in design-fidelity-review.md); collapse the capabilities table to a two-column summary that adds only the When column.
- Findings:
  - `architecture-2` prompt-quality-canon.md is an orphan reference — not loaded by any step — `references/prompt-quality-canon.md`
  - `leanness-1` Capabilities table restates step content; only 'When' column adds new information — `SKILL.md:Capabilities`
  - `cohesion-2` Capabilities table redundancy — aligns with leanness-1 — `SKILL.md:Capabilities`

### 3. Minor mechanics

- Root cause: Three small wiring decisions that would improve reliability or efficiency with minimal change: Step 3 reads could be parallelised, WDS mode detection could be a Bash test, and the fidelity brief path could be user-configurable.
- Fix: In Step 3, issue git diff and read experience_doc in one parallel call. Rewrite 'Check whether {workflow.design_doc} exists' as a Bash call: 'Run: test -f {workflow.design_doc}'. Optionally lift design-fidelity-review.md path to {workflow.fidelity_brief} in customize.toml.
- Findings:
  - `architecture-1` Step 3 sequential reads are parallelisable — `SKILL.md:Step 3`
  - `determinism-1` WDS mode detection is a file-existence check done by the model — `SKILL.md:Step 2`
  - `customization-1` design-fidelity-review.md path is hardcoded in Step 4 — `SKILL.md:Step 4, customize.toml`

## Strengths

- WDS mode detection logic is clean and non-invasive — a single file presence check gates the optional scan without complicating the non-WDS path.
- Freya's persona is precise and load-bearing: the 'no editorializing, no noise when nothing happened' character directly shapes the clean-pass line and the finding template, and was treated as investment throughout the analysis.
- The capability split between SC (script, deterministic, WDS-gated) and DR (external skill, always-on) is architecturally sound and will hold as both capabilities evolve independently.
- Fallback paths are thorough for tooling failures: uv fallback, git rev-list guard for shallow repos, ScheduleWakeup fallback note — the skill degrades gracefully when the environment is thin.
- design-fidelity-review.md is well-scoped: it tells Sally exactly what to do when wds_mode is false (skip signals 1-2, focus on 3-6 from diff alone).

## Recommendations

1. Add Sally unavailability guard to Step 4: 'If bmad-agent-ux-designer is unavailable or returns no output, skip signals 3b–6 and append WARN to the finding block: [TIMESTAMP] FREYA — WARN. bmad-agent-ux-designer unavailable; design judgment signals 3–6 skipped this pass.' (resolves: enhancement-2, cohesion-1)
2. Add directory creation to Step 5: before the file write, run 'mkdir -p $(dirname {workflow.status_file})' or equivalent Bash call so the write does not fail on a fresh project without _bmad-output/planning-artifacts/. (resolves: enhancement-1)
3. Remove skills/mm-ux-orchestrator/references/prompt-quality-canon.md — it is not loaded by any step in SKILL.md or design-fidelity-review.md. If Sally should use it, add a load instruction in design-fidelity-review.md. (resolves: architecture-2)
4. In Step 3, merge the git diff call and the experience_doc read into one parallel block: 'Run in parallel: (a) git diff {workflow.diff_range} -- {workflow.scan_paths}; (b) read {workflow.experience_doc} if it exists.' (resolves: architecture-1)

## Agent Profile

- Name: Freya
- Title: UX Orchestrator
- Type: stateless
- Mission: Timed UX orchestration loop: delegate to Sally for design judgment every 40 minutes, optionally running WDS deterministic scan first, and append one advisory finding to ux-status.md.

## Capabilities

- **SC — Deterministic scan** (script) — scan-signals.py detects hex drift, missing @reference, new pages — runs only in WDS mode (DESIGN.md present)
- **DR — Design judgment** (external skill) — bmad-agent-ux-designer (Sally) covers signals 3b–6 using design-fidelity-review.md as her briefing — runs always

## Per-Lens Verdicts

- **leanness**: Lean for a multi-mode orchestration skill; two low-grade ceremony lines in Step 4 and capabilities table, no ceremony in the capability prompts themselves.
- **architecture**: Sound topology and activation flow; one orphan reference file (prompt-quality-canon.md not referenced in SKILL.md), one missed parallelisation in Step 3.
- **determinism**: Scripts handle plumbing correctly; one low-grade determinism leak where the model checks file existence rather than a Bash call.
- **customization**: Well-surfaced workflow scalars, sole config mechanism, persistent_facts wired; one low opportunity to lift the fidelity brief path.
- **enhancement**: Two medium runtime gaps: Sally unavailability has no fallback, and Step 5 does not ensure the parent directory exists before writing.
- **agent-cohesion**: Persona and capabilities cohere well; the coordinator-delegates-to-specialist shape is authentic to Freya's character. Primary gap is the missing Sally fallback, which leaves the end-to-end journey with a dead-end.

## Experience

- **WDS project loop (happy path)** — Loop fires → config resolved → DESIGN.md found → scan-signals.py runs → git diff + EXPERIENCE.md read → Sally invoked → finding assembled → appended to ux-status.md → ScheduleWakeup called
- **Non-WDS project loop** — Loop fires → config resolved → DESIGN.md absent → scan JSON set to wds_mode:false → git diff + EXPERIENCE.md (if present) read → Sally invoked → finding assembled with signals 1-2 marked 'WDS mode not active' → appended → ScheduleWakeup called
- **Clean pass (no changes)** — Loop fires → scan-signals.py returns no_changes:true → clean-pass line appended → ScheduleWakeup called
- Headless: Self-scheduling via ScheduleWakeup; stdout confirmation line provides machine-readable signal for headless callers; graceful fallback note when ScheduleWakeup unavailable.

## Findings

### High (5)

#### lint-1 — Prompt file at skill root: .memlog.md

- Lens: lint
- Location: `.memlog.md`
- Evidence: Scanner flagged .memlog.md as capability content at skill root. This is the builder's process log placed here per bmb spec — a scanner false positive, not a skill authoring defect.
- Recommendation: No action needed; .memlog.md is the builder's trace file and its placement is correct per bmb convention.

#### lint-2 — Absolute path in .analysis/2026-06-19-1120/findings.json

- Lens: lint
- Location: `.analysis/2026-06-19-1120/findings.json:9`
- Evidence: Absolute machine path in standards.canon field of a prior analysis report. Archival artifact from previous analysis run, not a source file.
- Recommendation: No action needed on the skill itself; this is an old report file. The builder's render script should emit relative or placeholder paths in the standards block.

#### lint-3 — Absolute path in .analysis/2026-06-19-1120/findings.json (principles)

- Lens: lint
- Location: `.analysis/2026-06-19-1120/findings.json:10`
- Evidence: Absolute machine path in standards.principles. Same archival artifact as lint-2.
- Recommendation: No action needed. See lint-2.

#### lint-4 — Absolute path in .analysis/2026-06-19-1120/findings.json (scripts)

- Lens: lint
- Location: `.analysis/2026-06-19-1120/findings.json:11`
- Evidence: Absolute machine path in standards.scripts. Same archival artifact as lint-2.
- Recommendation: No action needed. See lint-2.

#### lint-5 — uv not found on PATH — cannot run ruff for Python linting

- Lens: lint
- Location: `scripts/scan-signals.py`
- Evidence: Scanner could not run ruff because uv is not installed in this environment. The Python in scan-signals.py was not linted.
- Recommendation: Install uv in the development environment to enable Python linting. Not a skill defect.

### Medium (5)

#### architecture-1 — Step 3 sequential reads are parallelisable

- Lens: architecture
- Location: `SKILL.md:Step 3`
- Evidence: 'First, run: git diff... then read {workflow.experience_doc}'. The git diff call and the experience_doc read are independent — neither consumes the other's output.
- Recommendation: Rewrite Step 3 opening as: 'Run in parallel: (a) git diff {workflow.diff_range} -- {workflow.scan_paths} and capture the raw diff; (b) read {workflow.experience_doc} if it exists.' This matches the parallelisation pattern already present elsewhere in the skill.

#### architecture-2 — prompt-quality-canon.md is an orphan reference — not loaded by any step

- Lens: architecture
- Location: `references/prompt-quality-canon.md`
- Evidence: The file exists in references/ but SKILL.md and design-fidelity-review.md contain no instruction to load it. It was bundled from the previous version but the current architecture delegates all judgment to Sally, who has no explicit instruction to use it either.
- Recommendation: Remove references/prompt-quality-canon.md from the skill, or add a load instruction to design-fidelity-review.md if Sally should hold the quality bar while reviewing ('Load references/prompt-quality-canon.md to calibrate finding severity').

#### enhancement-1 — Step 5 does not create parent directory before writing status_file

- Lens: enhancement
- Location: `SKILL.md:Step 5`
- Evidence: 'Ensure {workflow.status_file} exists (create with a # UX Status header if absent).' This handles a missing file but not a missing parent directory. On a fresh project where _bmad-output/planning-artifacts/ has never been created, the write will fail silently with no error in the finding.
- Recommendation: Add before the file write: 'Run: mkdir -p $(dirname {workflow.status_file})' or equivalent Bash call to ensure the directory chain exists. This is the same pattern the PLO orchestrator uses for _bmad-output writes.

#### enhancement-2 — No fallback when bmad-agent-ux-designer (Sally) is unavailable

- Lens: enhancement
- Location: `SKILL.md:Step 4`
- Evidence: Step 4 unconditionally invokes bmad-agent-ux-designer with no guard for the case where the skill is not installed or returns no output. On a project where only mm-ux-orchestrator is installed (Sally absent), the step fails and Freya produces no finding.
- Recommendation: Add after the Sally invocation: 'If bmad-agent-ux-designer is unavailable or returns no output, skip signals 3b–6 and append to the finding: [TIMESTAMP] FREYA — WARN. bmad-agent-ux-designer unavailable; design judgment signals 3–6 skipped this pass. Signals 1–3a from deterministic scan only.' This degrades gracefully rather than silently failing.

#### cohesion-1 — Sally unavailability creates a dead-end in the end-to-end journey

- Lens: agent-cohesion
- Location: `SKILL.md:Step 4`
- Evidence: Freya's identity is 'UX orchestration coordinator' — she coordinates the scan and Sally's judgment. If Sally is absent, Freya has no path to produce a finding, contradicting the coordinator persona (a coordinator who cannot coordinate when one party is missing is not resilient). Aligns with enhancement-2.
- Recommendation: Same fix as enhancement-2: add the Sally unavailability guard with a graceful WARN fallback. The fix aligns the 'resilient coordinator' implied by Freya's persona with her actual runtime behavior.

### Low (7)

#### leanness-1 — Capabilities table restates step content; only 'When' column adds new information

- Lens: leanness
- Location: `SKILL.md:Capabilities`
- Evidence: The capabilities table lists Code, Capability, Signal types, How, When. The Code, Capability, Signal types, and How columns repeat what Steps 2 and 4 already state inline. Only the 'When' column (WDS mode only vs Always) is novel.
- Recommendation: Collapse the table to two columns (Capability | When) or fold the 'When' distinction into a single inline sentence at the end of each step. Saves ~4 lines with no information loss.

#### leanness-2 — Ceremony sentence in Step 4

- Lens: leanness
- Location: `SKILL.md:Step 4`
- Evidence: 'Sally returns a finding block covering signals 3b–6. Collect her output; it feeds the finding assembled in Step 5.' The second sentence ('Collect her output; it feeds...') is self-evident from the structure.
- Recommendation: Cut the second sentence. 'Sally returns a finding block covering signals 3b–6.' is the complete and sufficient statement.

#### architecture-3 — Freya reads EXPERIENCE.md then passes its contents to Sally — mild read-before-delegate

- Lens: architecture
- Location: `SKILL.md:Step 3, Step 4`
- Evidence: Step 3 reads experience_doc into Freya's context; Step 4 passes those contents to Sally. For small files this is acceptable, but for large EXPERIENCE.md files this bloats Freya's context unnecessarily.
- Recommendation: Low priority. If EXPERIENCE.md files grow large, consider passing the path and letting Sally read it directly inside her invocation. For now, the current pattern is acceptable.

#### determinism-1 — WDS mode detection is a file-existence check done by the model

- Lens: determinism
- Location: `SKILL.md:Step 2`
- Evidence: 'Check whether {workflow.design_doc} exists' is a deterministic file-existence test assigned to the model in prose rather than as a Bash call.
- Recommendation: Rewrite as an explicit Bash call: 'Run: test -f {workflow.design_doc} && echo wds_mode=active || echo wds_mode=inactive'. This is unambiguous and does not cost prompt tokens for a yes/no question.

#### customization-1 — design-fidelity-review.md path is hardcoded in Step 4

- Lens: customization
- Location: `SKILL.md:Step 4, customize.toml`
- Evidence: 'The briefing from references/design-fidelity-review.md' is hardcoded. An org that wants to supply its own UX judgment brief cannot override it.
- Recommendation: Low opportunity. Add 'fidelity_brief = "{skill-root}/references/design-fidelity-review.md"' to customize.toml [workflow] and reference '{workflow.fidelity_brief}' in Step 4. Only worthwhile if orgs are expected to swap the brief.

#### enhancement-3 — Finding template shows 'active | not active' inline — ambiguous for first-time readers

- Lens: enhancement
- Location: `SKILL.md:Persona/Communication style`
- Evidence: The WDS mode row in the template reads '**WDS mode**: active | not active' — the pipe means 'one of these', but the template only shows one combined row rather than two distinct examples.
- Recommendation: Minor polish. Either add a note '(one of: active, not active)' or show a two-block example in the persona section: one for WDS mode active, one for non-WDS. Low value unless the skill will be used by people unfamiliar with the format.

#### cohesion-2 — Capabilities table redundancy — aligns with leanness-1

- Lens: agent-cohesion
- Location: `SKILL.md:Capabilities`
- Evidence: Same observation as leanness-1: the table restates step content with only the 'When' column adding new information.
- Recommendation: See leanness-1. Collapsing the table to two columns or inline notes keeps the 'When' distinction without the full restatement.
