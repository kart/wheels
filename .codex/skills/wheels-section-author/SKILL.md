---
name: wheels-section-author
description: Author exactly one planned Wheels section from section-local planning files, producing only section-local draft, preview, source notes, and optional teaching assets.
---

# wheels-section-author

Use this skill after `wheels-section-planner` has created section planning files. This is a section-local authoring skill, not a full-topic authoring skill.

This skill authors exactly one planned Wheels section. Never author more than one section in one skill run.

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
- `<TOPIC_DIR>/plan.yaml`
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
- `<SECTION_DIR>/state.yaml`

Do not use naked topic-specific paths like `topic.yaml`, `plan.yaml`, `wiki/**`, `outputs/**`, `reviews/**`, or `.wheels_state.json` unless the text explicitly says "inside TOPIC_DIR".

If `TOPIC_ID` or `SECTION_ID` is missing or ambiguous, stop and ask for it. Never mix files from multiple topics. Never author more than one section in one skill run.

## Preflight Validation

Before authoring, verify these exist:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/wiki/**`
- `<TOPIC_DIR>/sections/section_plan.yaml`
- `<SECTION_DIR>/section.yaml`

If any are missing:

- stop
- explain which input is missing
- do not create authoring files
- do not create prose, media, code, `<SECTION_DIR>/preview.html`, or `<SECTION_DIR>/blog_fragment.md`

During preflight, read `<SECTION_DIR>/section.yaml`. If the `section_id` inside `<SECTION_DIR>/section.yaml` does not match the requested `SECTION_ID`, stop and do not create or modify authoring artifacts.

During preflight, if `<SECTION_DIR>/state.yaml` exists and says `approved_by_user: true`, stop. Do not revise an approved section unless the user explicitly asks to revise it.

Before authoring, inspect `depends_on_sections` from `<SECTION_DIR>/section.yaml` if present. For each dependency, check `<TOPIC_DIR>/sections/<dependency_section_id>/state.yaml`. If any dependency is missing or is not `approved_by_user: true`, stop, explain which dependency is not approved, and do not author the requested section.

## Inputs To Read

When the skill is actually used, read:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/wiki/**`
- `<TOPIC_DIR>/sections/section_plan.yaml`
- `<SECTION_DIR>/section.yaml`
- `AGENTS.md`
- `templates/article_shapes.md`
- `prompts/audience_profiles.md`
- relevant source anchors from `<TOPIC_DIR>/wiki/**`

Read `<SECTION_DIR>/section.yaml` first.

## Allowed Writes

When the skill is actually used, write only section-local artifacts:

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
- `<SECTION_DIR>/state.yaml`

Before writing or updating section-local artifacts, inspect existing `<SECTION_DIR>` files if present. Update only intentionally. Do not delete existing section files unless explicitly asked.

## Forbidden Writes

- Do not modify `<TOPIC_DIR>/raw/**`.
- Do not modify `<TOPIC_DIR>/plan.yaml`.
- Do not modify `<TOPIC_DIR>/.wheels_state.json`.
- Do not modify `<TOPIC_DIR>/outputs/**`.
- Do not modify `<TOPIC_DIR>/reviews/**`.
- Do not modify other sections under `<TOPIC_DIR>/sections/<other_section_id>/**`.
- Do not modify any files outside the Allowed Writes list.
- Allowed writes are exhaustive; no other files may be created or modified.
- Explicit v1 fixture exception: do not modify `topics/word2vec/outputs/**` or `topics/word2vec/reviews/**` unless the user explicitly asks. This hard-coded fixture guard is intentional and does not replace `TOPIC_DIR` scoping for active topic work.
- Do not assemble final `<TOPIC_DIR>/outputs/publish/blog.md`.
- Do not assemble final `<TOPIC_DIR>/outputs/preview.html` for the full topic.

## Authoring Notes First

Before writing polished prose, create `<SECTION_DIR>/authoring_notes.md`.

`<SECTION_DIR>/authoring_notes.md` must include:

- what question this section answers
- what the reader should understand by the end
- source anchors and claims used
- prerequisite concepts needed
- expected reader confusions
- concrete teaching mechanism selected
- why this mechanism fits this section
- whether code is useful
- whether media is useful
- what toy/scaled-down demo will be used, if any
- what the toy/demo demonstrates
- what the toy/demo omits
- toy-to-real bridge
- section-local structure before prose

## Mechanism-First Teaching

Use mechanism-first teaching.

The mechanism may be:

- runnable code
- pseudocode
- worked numerical example
- visual trace
- architecture diagram
- state machine
- sequence diagram
- table
- simulation
- no mechanism, with explicit reason

## Code Rule

Plan and generate code only when it naturally clarifies the section. Do not force code.

If code is generated, it must be section-local under `<SECTION_DIR>/code/**`. It should be small, readable, educational, and connected directly to the prose.

## Media Rule

Generate media only when it clarifies the section.

If media is generated, it must be section-local under `<SECTION_DIR>/visuals/**`, `<SECTION_DIR>/manim/**`, or `<SECTION_DIR>/manim_media/**`. Media must have a clear teaching purpose and must not be decorative filler.

## Prose Rule

Write `<SECTION_DIR>/draft.md` as the canonical section draft.

Write `<SECTION_DIR>/blog_fragment.md` as the publishable fragment for this section only.

Do not write full-topic `blog.md`. Do not jump ahead to later sections. Do not summarize future sections except with brief forward pointers when needed.

## Preview Rule

Create `<SECTION_DIR>/preview.html` as a reader-facing preview for this section only.

It should render the section draft, visuals, code snippets, and captions in context. It should not include internal planning notes unless clearly collapsed or omitted.

Do not create or modify `<TOPIC_DIR>/outputs/preview.html`.

## Source Notes

Create or update `<SECTION_DIR>/source_notes.md` with:

- source anchors used
- claims supported by each source
- assumptions or simplifications
- toy-to-real caveats

## State

Create or update `<SECTION_DIR>/state.yaml` with:

```yaml
status: authored
approved_by_user: false
needs_review: true
```

Do not mark the section approved.

## Stop Condition

After authoring exactly this one section, stop.

Tell the user:

- which files were created or updated
- that they should review `<SECTION_DIR>/preview.html`
- that the next step is section review
- that no later section will be authored until this section is reviewed, fixed, and explicitly approved

Do not run reviewer/fixer behavior inside this skill.

## Quality Bar

- Do not produce shallow summaries.
- Explain motivation before mechanism.
- Use examples before abstraction.
- Introduce equations only after intuition.
- Define inputs, outputs, parameters/state, and what changes during execution/training.
- Use toy-to-real bridges wherever applicable.
- Preserve source fidelity.
- Keep the section understandable to an undergraduate-level technical reader.
- Make it useful to the actual learner, who may be experienced in computer science but is building systematic AI foundations.

## Creativity Policy

Be creatively ambitious inside the current section, but stay inside the section contract.

You may creatively choose:

- the clearest teaching mechanism
- examples, analogies, and toy demos
- visual, Manim, and diagram concepts
- small explanatory code
- section structure and narrative flow
- toy-to-real bridge framing

You must not creatively invent:

- unsupported source claims
- results not present in `<TOPIC_DIR>/wiki/**` or source anchors
- fake citations
- production details not grounded in sources or clearly marked as interpretation
- content from future sections
- changes to other sections or topic-level outputs

Prefer memorable explanations over generic summaries.
Prefer concrete mechanisms over abstract prose.
Prefer a surprising but accurate toy example over a bland overview.

Preserve all existing guardrails:

- one section only
- `TOPIC_DIR` and `SECTION_DIR` scoping
- no `<TOPIC_DIR>/raw/**` modification
- no `<TOPIC_DIR>/outputs/**` modification
- no `<TOPIC_DIR>/reviews/**` modification
- no final blog/preview assembly
- no approval by Codex
- no reviewer/fixer behavior
