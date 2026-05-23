---
name: wheels-section-reviewer
description: Review exactly one authored Wheels section and write section-local review findings only, without applying fixes.
---

# wheels-section-reviewer

Use this skill after `wheels-section-author` has authored one section. This is a section-local review skill, not a full-topic review skill.

This skill reviews exactly one authored Wheels section. It must write review findings only. It must not apply fixes.

## Tooling Policy

For Python instructions, examples, or validation commands, prefer `.venv/bin/python`. Do not use system Python. Do not install packages from inside the skill unless the user explicitly asks. If dependencies are missing, note that the user may install them with commands such as `.venv/bin/python -m pip install matplotlib numpy pillow cairosvg playwright pymupdf` and `.venv/bin/python -m playwright install chromium`.

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
- Do not modify `<TOPIC_DIR>/wiki/**`.
- Do not modify `<TOPIC_DIR>/wiki/source_assets/**`.
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
- `<TOPIC_DIR>/wiki/foundation_stack.md` if present
- relevant `<TOPIC_DIR>/wiki/source_assets/**` files if `<SECTION_DIR>/section.yaml` contains `source_assets` or `visual_verification_required`

Do not review unrelated sections in this skill run. Use a separate run with a different `SECTION_ID` for another section.

When `<SECTION_DIR>/section.yaml` contains `source_assets` or `visual_verification_required`, inspect:

- `<TOPIC_DIR>/wiki/source_assets/index.yaml`
- `<TOPIC_DIR>/wiki/source_assets/formulas.md`
- `<TOPIC_DIR>/wiki/source_assets/figures.md`
- `<TOPIC_DIR>/wiki/source_assets/tables.md`
- `<TOPIC_DIR>/wiki/source_assets/visual_audit.md`
- evidence image paths referenced in `<SECTION_DIR>/section.yaml`
- the `Source Assets Used` section in `<SECTION_DIR>/authoring_notes.md`
- `<SECTION_DIR>/source_notes.md` if present

Treat all source asset files and section authoring artifacts as read-only while reviewing.

If `<TOPIC_DIR>/wiki/foundation_stack.md` exists, inspect it when reviewing the section's `foundation_role`, `foundation_stack_refs`, prerequisite ramp, or background depth. Treat it as read-only planning/source-grounding support, not as required final prose.

## Review Checks

### Source Fidelity

- Are claims grounded in `<TOPIC_DIR>/wiki/**` and source anchors?
- Are paper/system/source claims represented accurately?
- Are unsupported claims clearly marked as interpretation?
- Are simplifications disclosed?

### Source Asset / Formula / Figure / Table Review

- Did the section use the assets mapped in `<SECTION_DIR>/section.yaml`?
- Were any relevant mapped assets ignored without explanation?
- Were formulas transcribed or normalized accurately?
- Were symbols defined?
- Was intuition explained before equations?
- Were `visual_verification_needed` caveats respected?
- Were uncertain formulas, tables, or charts treated cautiously?
- Were exact table/chart values quoted only if reliable or visually verified?
- Were dense paper figures copied blindly, or were simplified teaching visuals created when appropriate?
- If simplified visuals were created, are they faithful to the source asset?
- Are raw evidence screenshots exposed in `<SECTION_DIR>/preview.html` only when there is a clear teaching reason?
- Are source-asset caveats recorded in `<SECTION_DIR>/authoring_notes.md` or `<SECTION_DIR>/source_notes.md`?

### Learning Goal Fit

- Does the section satisfy `<SECTION_DIR>/section.yaml` learning_goal?
- Does it answer the key questions?
- Does it match the intended audience?
- Does it stay within this section's scope?

### System Design Deep Dive Review

For `article_shape: system_design_deep_dive` sections, check:

- Are requirements clear?
- Are assumptions explicit?
- Are APIs concrete enough?
- Is the data model plausible?
- Are SQL/NoSQL choices justified?
- Are storage choices separated between metadata and blobs/object storage where relevant?
- Are workflows complete and ordered?
- Are async boundaries clear?
- Are consistency choices stated?
- Are retry/idempotency concerns addressed where needed?
- Are failure modes included?
- Are bottlenecks and scaling paths discussed?
- Are observability/metrics/SLOs included where relevant?
- Are public facts separated from inferred design choices?
- Are diagrams readable, accurate, and not generic filler?
- Does the section avoid copying interview-prep sources?
- Does it teach design reasoning, not just list components?

For `audience_profile: system_design_interview_l5_plus`, additionally check:

- Does the main path remain coherent for L5?
- Are L6+ callouts selective and meaningful?
- Are L6+ callouts too verbose or too frequent?
- Are senior-level topics included where they genuinely matter?
- Does the section avoid separate repetitive L5/L6/L7 answers?

If a system design section is generic, component-list-only, or lacks design reasoning, mark `needs_fix: true`.

### Prerequisite Handling

- Are prerequisite concepts introduced before use?
- Are technical terms introduced with enough context for the declared audience?
- Are equations introduced only after intuition?
- Are formula symbols defined?
- Are formulas paired with numerical or concrete examples when useful?

### Prerequisite / Intuition Ramp Review

- Does `<SECTION_DIR>/authoring_notes.md` include a `Prerequisite / Intuition Ramp` section?
- Does the section build the minimum beginner mental model before introducing notation, formulas, algorithms, paper-specific terms, or expert vocabulary?
- Does the prose generally prefer concrete object -> plain-English intuition -> tiny example -> notation -> paper terminology -> formula/algorithm, without treating that sequence as a rigid paragraph-by-paragraph template?
- Does the section avoid notation -> formula -> terminology -> explanation?
- Does the section assume the concept it is supposed to teach?
- Are technical terms introduced with enough context for the declared audience?
- Are multiple abstractions stacked before any concrete mental model?
- Does the section explain central terms when first used?
- Does the section over-explain already-established terms?
- Does the section bury the main idea under too many definitions?
- Did the author make a reasonable audience-aware judgment based on `audience_profile`, prerequisites, dependencies, prior approved sections, section learning goal, and section position?
- Do not require every technical term to be defined from scratch if prior approved sections establish it.
- Are the first few paragraphs accessible to the declared audience?
- For beginner-oriented audiences, does the section avoid assuming domain-specific machinery unless explicitly listed as prerequisite?
- If the section starts too abstractly for the audience, set `needs_fix: true`.
- Do not treat a missing intuition ramp as optional polish when it blocks beginner comprehension.

### Foundation / Background Review

- Did the section use `<TOPIC_DIR>/wiki/foundation_stack.md` appropriately when present?
- Does `<SECTION_DIR>/authoring_notes.md` include `Foundation / Background Use`?
- Was the section's `foundation_role` satisfied?
- If this is a background section, is it deep and intuitive rather than a glossary?
- If this is a core section, does it rely on prior approved foundation sections correctly?
- Does the section introduce prerequisites before using them?
- Does it avoid assuming the concepts it is supposed to teach?
- Does it avoid dumping too much background that distracts from the section goal?
- Does it preserve the intended audience level?
- Are enough-understanding checks or equivalent reader outcomes present when useful?
- Are deferred concepts clearly deferred rather than silently ignored?
- For paper topics, are math/notation prerequisites introduced before formulas?
- For system-design topics, are requirements, capacity, API, and data-model primitives introduced before major architecture decisions?
- For algorithm topics, are data structures and complexity ideas introduced before optimized mechanics?
- If the section starts too abstractly for the audience, set `needs_fix: true`.
- If a background section is shallow, glossary-like, or fails to build intuition, set `needs_fix: true`.
- If a core section duplicates too much foundation material unnecessarily, set `needs_fix: true` when it blocks flow, otherwise list it as a non-blocking improvement.

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

- If the section contains any reader-facing visual artifact, inspect the rendered visual output when local tooling makes that possible.
- Reader-facing visual artifacts include `<SECTION_DIR>/visuals/**`, `<SECTION_DIR>/manim_media/**`, SVG files, PNG/JPG/WebP files, charts, diagrams, and `<SECTION_DIR>/preview.html` with embedded visuals.
- Do not rely only on source text for SVG files. Inspect the rendered SVG when possible.
- For code-generated visuals, review both the visual source/spec and rendered output. Inspect `<SECTION_DIR>/visuals/<visual_id>_spec.md`, `<SECTION_DIR>/visuals/<visual_id>.py`, `<SECTION_DIR>/visuals/<visual_id>.svg`, `<SECTION_DIR>/visuals/<visual_id>.png`, and `<SECTION_DIR>/preview.html` when present.
- Treat the Python visual source as the source of truth and SVG/PNG files as rendered outputs.
- Use available local tools for rendered checks when possible: `.venv/bin/python`, Pillow for image dimension/basic checks, CairoSVG for SVG-to-PNG rendering if installed, and Playwright/Chromium for `<SECTION_DIR>/preview.html` screenshots if installed.
- Do not use system Python for visual checks. Prefer `.venv/bin/python`.
- Do not install packages during review unless the user explicitly asks.
- For rendered SVGs and other rendered visuals, check for clipped text, text running outside the canvas, overlap, occlusion, unreadable labels, poor visual hierarchy, oversized arrows or marks, ambiguous arrows or labels, misleading visual implications, and inconsistencies between the caption and the image meaning.
- Does the rendered visual match the visual spec?
- Does every visual/media artifact teach one clear idea?
- Are labels readable?
- Are arrows/marks too large?
- Are arrows/labels ambiguous?
- Are there occlusion issues?
- Are there duplicated captions or labels?
- Are diagrams technically correct?
- Are captions accurate?
- Is any media decorative filler rather than teaching support?
- If visuals are derived from source assets, do they preserve the source meaning?
- Do simplified visuals introduce any misleading claims?
- Do captions clearly distinguish original source evidence from teaching redraws?
- If a visual is conceptual, is it clearly labeled as conceptual?
- Are exact values avoided unless verified?
- Does `<SECTION_DIR>/preview.html` render the visual in context?
- If rendered visual inspection is not possible with available local tooling, state that explicitly in `<SECTION_DIR>/review.md` and treat visual review as incomplete.
- If rendered visual inspection cannot be performed, do not mark a central visual as approval-ready. Set `needs_fix: true` if the visual is central to the learning mechanism.
- If rendered inspection finds clipping, overflow, overlap, occlusion, unreadable labels, misleading implication, or caption mismatch, mark it as a review finding and set `needs_fix: true` when the visual appears in `<SECTION_DIR>/preview.html` or is central to the section.

### Preview Review

- Open or render `<SECTION_DIR>/preview.html` when local browser or screenshot tooling is available.
- If browser/screenshot rendering is not available, inspect the HTML, linked image paths, image dimensions, and layout constraints, but mark rendered preview review as incomplete.
- Does `<SECTION_DIR>/preview.html` render as a reader-facing section preview?
- Are visuals/code/captions shown in context?
- Are internal notes omitted or clearly separated?
- Are there broken paths, broken math, broken markdown, or bad layout issues?
- If the section contains reader-facing formulas, does `<SECTION_DIR>/preview.html` include MathJax or equivalent math rendering support, matching the `~/karthik.dev` MathJax v3 SVG setup closely enough for local preview fidelity?
- Are important formulas rendered as math rather than left as plain fenced code blocks, unless the block is intentionally literal code or a non-math trace?

### Blog Fragment Review

- Is `<SECTION_DIR>/blog_fragment.md` publishable as a section fragment?
- Does it avoid full-topic front matter unless explicitly required?
- Does it not duplicate future/final assembly concerns?

### Approval Readiness

- Is this section ready for user reading?
- What blocks approval?
- What can be improved later but does not block approval?
- If the section contains important reader-facing visuals and rendered visual inspection was not performed, do not mark the section fully approval-ready.
- If an uninspected important visual is central to the section's learning mechanism, set `needs_fix: true` and state that visual review is incomplete.
- If an uninspected visual is not central to the section's learning mechanism, list incomplete rendered visual review as a caveat.
- If rendered visual inspection finds clipping, text running outside the canvas, overlap, occlusion, unreadable labels, misleading visual implications, or caption/image mismatch in a reader-facing visual, mark this as a review finding.
- If that visual is central to the section's learning mechanism or appears in `<SECTION_DIR>/preview.html`, set `needs_fix: true`.
- Do not mark the section approval-ready until the visual issue is fixed or explicitly deferred by the user.
- Do not set `approved_by_user: true`; only the user can approve a section.

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

## Source Asset / Formula / Figure / Table Notes
State:
- assets reviewed
- formula accuracy issues
- figure/table interpretation issues
- visual verification caveats
- whether source evidence was transformed faithfully into teaching artifacts
- whether any manual spot-check is required

## Foundation / Background Notes
State:
- foundation_stack.md consulted or not present
- whether the section's foundation_role was satisfied
- missing prerequisite intuition
- over-explained or duplicated background
- deferred concepts
- whether the section is ready for the target audience

## Learning Goal Coverage
State whether the section meets its learning goal and key questions.

## Mechanism / Code / Media Notes
Review the concrete teaching mechanism, code, visuals, Manim, or diagrams.
Explicitly state:
- whether rendered visual inspection was performed
- which visual files were inspected
- whether clipping, overlap, occlusion, unreadable labels, visual hierarchy problems, oversized marks, ambiguous arrows/labels, misleading implications, or caption/image mismatches were found
- whether visual review is complete or incomplete

## Preview / Rendering Notes
Review `<SECTION_DIR>/preview.html`.
Explicitly state:
- whether `<SECTION_DIR>/preview.html` was opened or rendered
- which preview rendering method or local tooling was used, if any
- whether embedded visuals rendered in context
- whether clipping, overlap, occlusion, bad layout, broken paths, or unreadable visual labels were found
- whether rendered preview review is complete or incomplete

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
