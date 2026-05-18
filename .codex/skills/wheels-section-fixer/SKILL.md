---
name: wheels-section-fixer
description: Fix exactly one reviewed Wheels section by validating review findings and user comments before applying section-local changes.
---

# wheels-section-fixer

Use this skill after `wheels-section-reviewer` has reviewed one authored section. This is a section-local fixer skill, not a full-topic fixer.

This skill fixes exactly one reviewed Wheels section. It must validate review findings and user comments before applying changes. It must not blindly apply reviewer suggestions. It must not approve the section. It must not move to the next section.

## Tooling Policy

For Python instructions, examples, or validation commands, prefer `.venv/bin/python`. Do not use system Python. Do not install packages from inside the skill unless the user explicitly asks. If dependencies are missing, note that the user may install them with commands such as `.venv/bin/python -m pip install matplotlib numpy pillow cairosvg playwright pymupdf` and `.venv/bin/python -m playwright install chromium`.

## Required User Inputs

This skill requires:

- `TOPIC_ID`
- `SECTION_ID`
- user comments, if provided

Derived paths:

- `TOPIC_DIR` = `topics/<TOPIC_ID>`
- `SECTION_DIR` = `<TOPIC_DIR>/sections/<SECTION_ID>`

All topic-specific paths must be scoped through `TOPIC_DIR` or `SECTION_DIR`.

Use scoped paths like:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/wiki/**`
- `<TOPIC_DIR>/wiki/source_assets/**`
- `<TOPIC_DIR>/sections/section_plan.yaml`
- `<SECTION_DIR>/section.yaml`
- `<SECTION_DIR>/authoring_notes.md`
- `<SECTION_DIR>/draft.md`
- `<SECTION_DIR>/blog_fragment.md`
- `<SECTION_DIR>/preview.html`
- `<SECTION_DIR>/media_plan.md`
- `<SECTION_DIR>/visuals/**`
- `<SECTION_DIR>/code/**`
- `<SECTION_DIR>/manim/**`
- `<SECTION_DIR>/manim_media/**`
- `<SECTION_DIR>/source_notes.md`
- `<SECTION_DIR>/review.md`
- `<SECTION_DIR>/fix_log.md`
- `<SECTION_DIR>/state.yaml`

Do not use naked topic-specific paths like `topic.yaml`, `plan.yaml`, `wiki/**`, `outputs/**`, `reviews/**`, or `.wheels_state.json` unless the text explicitly says "inside TOPIC_DIR".

If `TOPIC_ID` or `SECTION_ID` is missing or ambiguous, stop and ask for it. Never mix files from multiple topics. Never fix more than one section in one skill run.

## Preflight Validation

Before fixing, verify these exist:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/wiki/**`
- `<TOPIC_DIR>/sections/section_plan.yaml`
- `<SECTION_DIR>/section.yaml`
- `<SECTION_DIR>/draft.md`
- `<SECTION_DIR>/blog_fragment.md`
- `<SECTION_DIR>/preview.html`
- `<SECTION_DIR>/review.md`
- `<SECTION_DIR>/state.yaml`

If any required input is missing:

- stop
- explain which input is missing
- do not modify any files

## Section And State Checks

Read `<SECTION_DIR>/section.yaml`. If `section_id` inside `<SECTION_DIR>/section.yaml` does not match requested `SECTION_ID`, stop.

Read `<SECTION_DIR>/state.yaml`. If `approved_by_user: true`, stop unless the user explicitly asks to revise an approved section.

Before fixing, require both:

- `<SECTION_DIR>/review.md` exists
- `<SECTION_DIR>/state.yaml` has `reviewed: true`

If either condition is false:

- stop
- explain the inconsistent or missing review state
- ask the user to run `wheels-section-reviewer` first
- do not modify any files

Only allow override if the user explicitly asks to fix without a completed review.

If `<SECTION_DIR>/state.yaml` has `needs_fix: false` and there are no user comments requesting changes, stop and report that no fix is needed. Do not modify any files.

## Existing-File Safety

- Inspect existing section-local files before updating.
- Update intentionally.
- Do not delete existing section files unless explicitly asked.
- If `<SECTION_DIR>/fix_log.md` already exists, append or update intentionally.
- Do not erase prior fix history unless explicitly asked.

## Allowed Writes

- `<SECTION_DIR>/draft.md`
- `<SECTION_DIR>/blog_fragment.md`
- `<SECTION_DIR>/preview.html`
- `<SECTION_DIR>/media_plan.md`
- `<SECTION_DIR>/visuals/**`
- `<SECTION_DIR>/code/**`
- `<SECTION_DIR>/manim/**`
- `<SECTION_DIR>/manim_media/**`
- `<SECTION_DIR>/source_notes.md`
- `<SECTION_DIR>/fix_log.md`
- `<SECTION_DIR>/state.yaml`

## Forbidden Writes

- Do not modify `<TOPIC_DIR>/wiki/**`.
- Do not modify `<TOPIC_DIR>/wiki/source_assets/**`.
- Do not modify `<TOPIC_DIR>/raw/**`.
- Do not modify `<TOPIC_DIR>/outputs/**`.
- Do not modify `<TOPIC_DIR>/reviews/**`.
- Do not modify `<TOPIC_DIR>/plan.yaml`.
- Do not modify `<TOPIC_DIR>/.wheels_state.json`.
- Do not modify `<TOPIC_DIR>/sections/section_plan.yaml`.
- Do not modify other sections under `<TOPIC_DIR>/sections/<other_section_id>/**`.
- Do not modify `<SECTION_DIR>/section.yaml` unless explicitly asked.
- Do not modify `<SECTION_DIR>/review.md`.
- `<SECTION_DIR>/review.md` is an input to this skill, not an output.
- Do not assemble final `<TOPIC_DIR>/outputs/publish/blog.md`.
- Do not assemble final `<TOPIC_DIR>/outputs/preview.html`.
- Do not modify any files outside the Allowed Writes list.
- Allowed writes are exhaustive; no other files may be created or modified.

Explicit v1 fixture exception: do not modify `topics/word2vec/outputs/**` or `topics/word2vec/reviews/**` unless the user explicitly asks. This hard-coded fixture guard is intentional and does not replace `TOPIC_DIR` scoping for active topic work.

## Fixing Behavior

1. Read `<SECTION_DIR>/review.md` and user comments.

2. Create or update `<SECTION_DIR>/fix_log.md` before applying final changes.

`<SECTION_DIR>/fix_log.md` must track:

- each reviewer finding
- each user comment
- decision: `accepted` | `rejected` | `deferred`
- reason for decision
- files changed if accepted
- remaining open issues

3. Validate every finding.

Do not blindly apply reviewer suggestions. For each finding:

- verify against `<SECTION_DIR>/section.yaml`
- verify against `<TOPIC_DIR>/wiki/**` and source anchors
- verify against `<TOPIC_DIR>/wiki/source_assets/**` when the finding or section contract involves formulas, figures, tables, charts, diagrams, page evidence, `source_assets`, or `visual_verification_required`
- verify against the actual section artifacts
- decide whether the finding is valid

When `<SECTION_DIR>/section.yaml` contains `source_assets` or `visual_verification_required`, or when `<SECTION_DIR>/review.md` mentions source asset, formula, figure, or table issues, inspect:

- `<TOPIC_DIR>/wiki/source_assets/index.yaml`
- `<TOPIC_DIR>/wiki/source_assets/formulas.md`
- `<TOPIC_DIR>/wiki/source_assets/figures.md`
- `<TOPIC_DIR>/wiki/source_assets/tables.md`
- `<TOPIC_DIR>/wiki/source_assets/visual_audit.md`
- evidence image paths referenced in `<SECTION_DIR>/section.yaml`
- `<SECTION_DIR>/authoring_notes.md`
- `<SECTION_DIR>/source_notes.md` if present
- `<SECTION_DIR>/review.md`

Treat `<TOPIC_DIR>/wiki/source_assets/**`, `<TOPIC_DIR>/wiki/**`, `<SECTION_DIR>/section.yaml`, and `<SECTION_DIR>/review.md` as read-only inputs.

4. Apply only accepted fixes.

Possible fixes may include:

- improving explanation depth
- adding missing prerequisite explanation
- adding or repairing a prerequisite/intuition ramp before technical notation or terminology
- correcting unsupported claims
- improving toy-to-real bridge
- fixing broken preview rendering
- fixing visual captions or layout
- improving code comments or shape clarity
- correcting small code/media issues
- updating `<SECTION_DIR>/source_notes.md` with caveats or source anchors
- correcting source-asset-related formula, figure, table, chart, or visual-verification issues in section-local artifacts

If accepted reviewer findings or user comments identify source-asset-related issues, update only section-local artifacts allowed by this skill:

- `<SECTION_DIR>/draft.md`
- `<SECTION_DIR>/blog_fragment.md`
- `<SECTION_DIR>/preview.html`
- `<SECTION_DIR>/media_plan.md`
- `<SECTION_DIR>/visuals/**`
- `<SECTION_DIR>/code/**`
- `<SECTION_DIR>/manim/**`
- `<SECTION_DIR>/manim_media/**`
- `<SECTION_DIR>/source_notes.md`
- `<SECTION_DIR>/fix_log.md`
- `<SECTION_DIR>/state.yaml`

### Formula Fixes

If a formula issue is accepted:

- correct the formula explanation in section prose
- define missing symbols
- add or improve intuition before the equation
- add or improve a worked example when useful
- add caveats if `visual_verification_needed` is `true`
- do not pretend uncertainty is resolved unless evidence was visually checked
- record the fix decision in `<SECTION_DIR>/fix_log.md`

### Prerequisite / Intuition Ramp Fixes

If a reviewer or user flags missing prerequisite intuition, revise the opening/ramp before polishing wording.

When fixing prerequisite-ramp issues:

- fix missing intuition by adding the smallest useful explanation, not by adding a long generic primer
- prefer local surgical fixes: one concrete analogy, one short definition, one tiny example, or a sentence connecting the term to prior sections
- add a concrete mental model before notation when the audience needs it
- add a tiny example when it helps anchor the concept
- ground central technical terms in plain English when first used, unless prior approved sections already established them
- introduce notation after the reader has an intuitive object for it when the notation is new or likely confusing
- prefer concrete object -> plain-English intuition -> tiny example -> notation -> paper terminology -> formula/algorithm as a teaching flow, not a rigid template
- avoid notation -> formula -> terminology -> explanation
- do not overcorrect by bloating the section with definitions unrelated to the learning goal
- do not bury the main idea under a glossary dump
- preserve flow, section scope, and the section's learning goal
- preserve section scope and do not drift into later sections
- update `<SECTION_DIR>/authoring_notes.md` only if the fix changes the planned ramp or introduced terms
- update `<SECTION_DIR>/source_notes.md` if new or clarified claims are added
- record accepted/rejected/deferred ramp fixes in `<SECTION_DIR>/fix_log.md`

### Figure And Table Fixes

If a figure/table issue is accepted:

- correct qualitative interpretation
- remove or soften exact values if not reliable or visually verified
- improve captions
- replace misleading simplified visuals
- create or update section-local teaching visuals if useful
- do not copy raw evidence screenshots into preview by default
- record the fix decision in `<SECTION_DIR>/fix_log.md`

### Visual Verification Handling

If a reviewer says manual visual verification is required:

- do not silently mark it resolved unless the evidence image was actually inspected
- either fix based on inspection, or record the issue as deferred in `<SECTION_DIR>/fix_log.md`
- if deferred, keep `needs_fix: true` unless the issue is non-blocking

5. Code/media rule:

- Modify code/media only when the review or user comments justify it.
- Keep changes section-local.
- Do not introduce large new demos unless explicitly justified.
- Use `.venv/bin/python` for Python code or visual-generation checks. Do not use system Python.
- Do not install packages from inside the skill unless the user explicitly asks.
- If generated code exists and needs verification, run only section-local checks when safe and practical.
- If code checks are run, they must be section-local.
- Code checks must not write outside `<SECTION_DIR>/**`.
- If a code check would write outside `<SECTION_DIR>/**`, stop or record it as deferred in `<SECTION_DIR>/fix_log.md`.
- Do not run expensive, destructive, networked, or ambiguous checks without explicit user approval.
- If code execution is risky, expensive, or ambiguous, record the check as deferred in `<SECTION_DIR>/fix_log.md`.

### Code-Generated Visual Fixes

For technical teaching visuals, prefer fixing the visual source code/spec and regenerating rendered outputs.

The preferred artifact pattern is:

```text
<SECTION_DIR>/visuals/<visual_id>_spec.md
<SECTION_DIR>/visuals/<visual_id>.py
<SECTION_DIR>/visuals/<visual_id>.svg
<SECTION_DIR>/visuals/<visual_id>.png
```

The Python file is the source of truth. The SVG/PNG files are rendered outputs.

When fixing visual issues:

- prefer editing the visual source code/spec and regenerating rendered outputs
- do not manually patch rendered SVG unless the visual is trivial and no source exists
- if a hand-authored SVG exists and needs substantial revision, consider replacing it with code-generated visual artifacts
- use `.venv/bin/python` when running visual scripts
- keep all visual source and outputs section-local under `<SECTION_DIR>/visuals/**`
- do not modify `<TOPIC_DIR>/wiki/source_assets/**`, `<TOPIC_DIR>/wiki/**`, `<TOPIC_DIR>/raw/**`, `<TOPIC_DIR>/outputs/**`, or other sections

When fixing code-generated visuals:

1. update the spec if the teaching intent changed
2. update the Python source
3. regenerate SVG and PNG
4. update `<SECTION_DIR>/preview.html` if needed
5. update `<SECTION_DIR>/source_notes.md` if source-derived
6. record all decisions in `<SECTION_DIR>/fix_log.md`

If a reviewer flags visual clipping/overflow:

- fix layout in source code
- rerender
- verify rendered output if tooling permits

If a reviewer flags misleading visual implication:

- change the visual design, not just the caption
- update prose/caption as needed

6. Preview rule:

- Regenerate or update `<SECTION_DIR>/preview.html` when prose, code, media, captions, or layout changes affect the section preview.
- Preview must remain section-local.
- Do not generate full-topic preview.

7. Blog fragment rule:

- Update `<SECTION_DIR>/blog_fragment.md` if the publishable section fragment changes.
- Do not generate full-topic `<TOPIC_DIR>/outputs/publish/blog.md`.

8. Source notes:

- Update `<SECTION_DIR>/source_notes.md` if fixes add, remove, or clarify claims.

## State Update

Update `<SECTION_DIR>/state.yaml` while preserving existing fields.

Preserve all existing fields in `<SECTION_DIR>/state.yaml` unless explicitly listed below.

Do not change `approved_by_user`.

Do not change unrelated fields.

Only add or update:

- `fixed`
- `needs_review`
- `needs_fix`
- `last_fix`

Do not set `approved_by_user: true`. Only the user can approve a section.

## Stop Condition

After fixing exactly this one section, stop.

Tell the user:

- which files were changed
- which findings were accepted/rejected/deferred
- whether another review is recommended
- that the user should inspect `<SECTION_DIR>/preview.html`
- that no later section will be authored until this section is explicitly approved

Do not approve the section. Do not run reviewer behavior inside this skill. This fixer may read `<SECTION_DIR>/review.md`, but it must not create a new review or perform reviewer-skill behavior. Do not move to the next section.

## Quality Bar

- Fixes should improve understanding, not merely polish wording.
- Preserve source fidelity.
- Preserve mechanism-first teaching.
- Preserve toy-to-real bridges.
- Keep the section undergraduate-readable.
- Keep artifacts section-local and reviewable.

## Creativity Policy

You may creatively improve clarity, examples, diagrams, code comments, toy demos, and toy-to-real bridges when fixing accepted issues.

Creative fixes are allowed only when they directly address:

- accepted reviewer findings
- accepted user comments
- clear section-local correctness or clarity gaps

You must not:

- broaden the section beyond its approved scope
- introduce new unsupported claims
- invent source results, citations, benchmarks, or production details
- rewrite unrelated parts of the section just for style
- change other sections
- change topic-level outputs
- approve the section on behalf of the user

Any new claim must be grounded in `<TOPIC_DIR>/wiki/**`, section source notes, or clearly marked as interpretation.

Any new source-asset-related claim must be grounded in `<TOPIC_DIR>/wiki/source_assets/**`, section source notes, or clearly marked as interpretation.

Prefer fixes that improve understanding, not merely polish wording.

Preserve all existing guardrails:

- one section only
- validate findings before applying changes
- track accepted/rejected/deferred findings in `fix_log.md`
- section-local writes only
- no `<TOPIC_DIR>/raw/**` modification
- no `<TOPIC_DIR>/outputs/**` modification
- no `<TOPIC_DIR>/reviews/**` modification
- no final blog/preview assembly
- no section approval by Codex
- no reviewer behavior
- no moving to the next section
