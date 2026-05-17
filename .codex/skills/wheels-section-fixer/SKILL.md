---
name: wheels-section-fixer
description: Fix exactly one reviewed Wheels section by validating review findings and user comments before applying section-local changes.
---

# wheels-section-fixer

Use this skill after `wheels-section-reviewer` has reviewed one authored section. This is a section-local fixer skill, not a full-topic fixer.

This skill fixes exactly one reviewed Wheels section. It must validate review findings and user comments before applying changes. It must not blindly apply reviewer suggestions. It must not approve the section. It must not move to the next section.

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
- verify against the actual section artifacts
- decide whether the finding is valid

4. Apply only accepted fixes.

Possible fixes may include:

- improving explanation depth
- adding missing prerequisite explanation
- correcting unsupported claims
- improving toy-to-real bridge
- fixing broken preview rendering
- fixing visual captions or layout
- improving code comments or shape clarity
- correcting small code/media issues
- updating `<SECTION_DIR>/source_notes.md` with caveats or source anchors

5. Code/media rule:

- Modify code/media only when the review or user comments justify it.
- Keep changes section-local.
- Do not introduce large new demos unless explicitly justified.
- If generated code exists and needs verification, run only section-local checks when safe and practical.
- If code checks are run, they must be section-local.
- Code checks must not write outside `<SECTION_DIR>/**`.
- If a code check would write outside `<SECTION_DIR>/**`, stop or record it as deferred in `<SECTION_DIR>/fix_log.md`.
- Do not run expensive, destructive, networked, or ambiguous checks without explicit user approval.
- If code execution is risky, expensive, or ambiguous, record the check as deferred in `<SECTION_DIR>/fix_log.md`.

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
