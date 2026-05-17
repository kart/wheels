---
name: wheels-section-reviewer
description: Review exactly one authored Wheels section and write section-local review findings only, without applying fixes.
---

# wheels-section-reviewer

Use this skill after `wheels-section-author` has authored one section. This is a section-local review skill, not a full-topic review skill.

This skill reviews exactly one authored Wheels section. It must write review findings only. It must not apply fixes.

## Required User Inputs

This skill requires:

- `TOPIC_ID`
- `SECTION_ID`

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
- `<SECTION_DIR>/state.yaml`

Do not use naked topic-specific paths like `topic.yaml`, `plan.yaml`, `wiki/**`, `outputs/**`, `reviews/**`, or `.wheels_state.json` unless the text explicitly says "inside TOPIC_DIR".

If `TOPIC_ID` or `SECTION_ID` is missing or ambiguous, stop and ask for it. Never mix files from multiple topics. Never review more than one section in one skill run.

## Preflight Validation

Before reviewing, verify these exist:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/wiki/**`
- `<TOPIC_DIR>/sections/section_plan.yaml`
- `<SECTION_DIR>/section.yaml`
- `<SECTION_DIR>/draft.md`
- `<SECTION_DIR>/blog_fragment.md`
- `<SECTION_DIR>/preview.html`
- `<SECTION_DIR>/state.yaml`

If any required input is missing:

- stop
- explain which input is missing
- do not create `<SECTION_DIR>/review.md`
- do not modify any files

## Section And State Checks

Read `<SECTION_DIR>/section.yaml`. If `section_id` inside `<SECTION_DIR>/section.yaml` does not match requested `SECTION_ID`, stop.

Read `<SECTION_DIR>/state.yaml`. If `status` is not `authored`, stop unless the user explicitly asks to review a non-authored section.

If `approved_by_user: true`, stop unless the user explicitly asks to re-review an approved section.

## Allowed Writes

- `<SECTION_DIR>/review.md`
- `<SECTION_DIR>/state.yaml` only to record review status

If `<SECTION_DIR>/review.md` already exists, inspect it first. Update it intentionally. Do not delete prior review history unless explicitly asked.

## Forbidden Writes

- Do not modify `<SECTION_DIR>/draft.md`.
- Do not modify `<SECTION_DIR>/blog_fragment.md`.
- Do not modify `<SECTION_DIR>/preview.html`.
- Do not modify `<SECTION_DIR>/authoring_notes.md`.
- Do not modify `<SECTION_DIR>/source_notes.md`.
- Do not modify `<SECTION_DIR>/visuals/**`.
- Do not modify `<SECTION_DIR>/code/**`.
- Do not modify `<SECTION_DIR>/manim/**`.
- Do not modify `<SECTION_DIR>/manim_media/**`.
- Do not modify `<TOPIC_DIR>/raw/**`.
- Do not modify `<TOPIC_DIR>/outputs/**`.
- Do not modify `<TOPIC_DIR>/reviews/**`.
- Do not modify `<TOPIC_DIR>/plan.yaml`.
- Do not modify `<TOPIC_DIR>/.wheels_state.json`.
- Do not modify other sections under `<TOPIC_DIR>/sections/<other_section_id>/**`.
- Do not assemble final `<TOPIC_DIR>/outputs/publish/blog.md`.
- Do not assemble final `<TOPIC_DIR>/outputs/preview.html`.
- Do not modify any files outside the Allowed Writes list.
- Allowed writes are exhaustive; no other files may be created or modified.

Explicit v1 fixture exception: do not modify `topics/word2vec/outputs/**` or `topics/word2vec/reviews/**` unless the user explicitly asks. This hard-coded fixture guard is intentional and does not replace `TOPIC_DIR` scoping for active topic work.

## Review Scope

Review exactly this section's artifacts:

- `<SECTION_DIR>/section.yaml`
- `<SECTION_DIR>/authoring_notes.md`
- `<SECTION_DIR>/draft.md`
- `<SECTION_DIR>/blog_fragment.md`
- `<SECTION_DIR>/preview.html`
- `<SECTION_DIR>/media_plan.md` if present
- `<SECTION_DIR>/visuals/**` if present
- `<SECTION_DIR>/code/**` if present
- `<SECTION_DIR>/manim/**` if present
- `<SECTION_DIR>/source_notes.md` if present
- relevant `<TOPIC_DIR>/wiki/**` source anchors

Do not review unrelated sections in this skill run. Use a separate run with a different `SECTION_ID` for another section.

## Review Checks

### Source Fidelity

- Are claims grounded in `<TOPIC_DIR>/wiki/**` and source anchors?
- Are paper/system/source claims represented accurately?
- Are unsupported claims clearly marked as interpretation?
- Are simplifications disclosed?

### Learning Goal Fit

- Does the section satisfy `<SECTION_DIR>/section.yaml` learning_goal?
- Does it answer the key questions?
- Does it match the intended audience?
- Does it stay within this section's scope?

### Prerequisite Handling

- Are prerequisite concepts introduced before use?
- Are undefined terms avoided?
- Are equations introduced only after intuition?
- Are formula symbols defined?
- Are formulas paired with numerical or concrete examples when useful?

### Mechanism Clarity

- Is the chosen teaching mechanism appropriate?
- Does the mechanism explain inputs, outputs, moving parts, and state?
- Does it show what changes during execution/training when applicable?
- Is the toy/scaled-down demo clear?
- Is the toy-to-real bridge explicit and honest?

### Prose Quality

- Is the explanation deep rather than a shallow summary?
- Does it explain motivation before mechanism?
- Does it use examples before abstraction?
- Are transitions clear?
- Does it avoid jumping ahead into later sections?

### Code Review, If Code Exists

- Does code run or appear runnable?
- Is code small and educational?
- Is code directly connected to the prose?
- Are comments useful but not noisy?
- Are input/output shapes or data structures clear?
- Are limitations of toy code explained?

Do not execute or modify code while reviewing. If code execution is needed to verify correctness, report it as a recommended check unless the user explicitly asks to run it.

### Media Review, If Media Exists

- Does every visual/media artifact teach one clear idea?
- Are labels readable?
- Are there occlusion issues?
- Are there duplicated captions or labels?
- Are diagrams technically correct?
- Are captions accurate?
- Is any media decorative filler rather than teaching support?

### Preview Review

- Does `<SECTION_DIR>/preview.html` render as a reader-facing section preview?
- Are visuals/code/captions shown in context?
- Are internal notes omitted or clearly separated?
- Are there broken paths, broken math, broken markdown, or bad layout issues?

### Blog Fragment Review

- Is `<SECTION_DIR>/blog_fragment.md` publishable as a section fragment?
- Does it avoid full-topic front matter unless explicitly required?
- Does it not duplicate future/final assembly concerns?

### Approval Readiness

- Is this section ready for user reading?
- What blocks approval?
- What can be improved later but does not block approval?

## Output

Create `<SECTION_DIR>/review.md` with this structure:

```markdown
# Review: <SECTION_ID>

## Summary Verdict
One of:
- pass
- pass_with_minor_edits
- needs_revision
- blocked

## Blocking Issues
List issues that must be fixed before user approval.

## Non-Blocking Improvements
List helpful but optional improvements.

## Source Fidelity Notes
State whether claims are grounded, unsupported, or simplified.

## Learning Goal Coverage
State whether the section meets its learning goal and key questions.

## Mechanism / Code / Media Notes
Review the concrete teaching mechanism, code, visuals, Manim, or diagrams.

## Preview / Rendering Notes
Review `<SECTION_DIR>/preview.html`.

## Recommended Fixes
Give exact, actionable fixes with file references.

Recommended fixes are review findings only. Do not apply recommended fixes in this skill.

## Approval Recommendation
State whether the user should read now, request fixes first, or block the section.
```

## State Update

When updating `<SECTION_DIR>/state.yaml`, preserve all existing fields.

Only add or update:

- `reviewed`
- `needs_fix`
- `last_review`

Do not change:

- `status`
- `approved_by_user`
- `needs_review`
- unrelated fields

Update `<SECTION_DIR>/state.yaml` only to record:

```yaml
reviewed: true
needs_fix: true | false
last_review: <short timestamp or simple marker>
```

Do not set `approved_by_user: true`. Only the user can approve a section.

## Stop Condition

After writing `<SECTION_DIR>/review.md` and updating review status in `<SECTION_DIR>/state.yaml`, stop.

Tell the user:

- review file created
- summary verdict
- whether the next step is fixer or user read-through

Do not apply fixes. Do not run section-fixer behavior. Do not move to the next section.
