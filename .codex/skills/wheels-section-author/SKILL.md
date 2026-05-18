---
name: wheels-section-author
description: Author exactly one planned Wheels section from section-local planning files, producing only section-local draft, preview, source notes, and optional teaching assets.
---

# wheels-section-author

Use this skill after `wheels-section-planner` has created section planning files. This is a section-local authoring skill, not a full-topic authoring skill.

This skill authors exactly one planned Wheels section. Never author more than one section in one skill run.

Ownership boundaries:

- `scripts/init_topic.py` owns deterministic `<TOPIC_DIR>/topic.yaml` creation.
- `wheels-topic-bootstrap` owns `<TOPIC_DIR>/plan.yaml` and `<TOPIC_DIR>/wiki/**`.
- `wheels-section-planner` owns `<TOPIC_DIR>/sections/section_plan.yaml` and `<SECTION_DIR>/section.yaml`.

The section author may read those files, but must treat them as read-only inputs.

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
- `<TOPIC_DIR>/plan.yaml`
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
- `<SECTION_DIR>/state.yaml`

Do not use naked topic-specific paths like `topic.yaml`, `plan.yaml`, `wiki/**`, `outputs/**`, `reviews/**`, or `.wheels_state.json` unless the text explicitly says "inside TOPIC_DIR".

If `TOPIC_ID` or `SECTION_ID` is missing or ambiguous, stop and ask for it. Never mix files from multiple topics. Never author more than one section in one skill run.

## Preflight Validation

Before authoring, verify these exist:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/plan.yaml`
- `<TOPIC_DIR>/wiki/**`
- `<TOPIC_DIR>/wiki/foundation_stack.md` if present
- `<TOPIC_DIR>/sections/section_plan.yaml`
- `<SECTION_DIR>/section.yaml`

If any are missing:

- stop
- explain which input is missing
- do not create authoring files
- do not create prose, media, code, `<SECTION_DIR>/preview.html`, or `<SECTION_DIR>/blog_fragment.md`

Validate that `<TOPIC_DIR>/topic.yaml` includes these deterministic fields created by `scripts/init_topic.py`:

- `id`
- `title`
- `audience_profile`
- `article_shape`
- `workflow`
- `publish_target`
- `raw_resource_policy`
- `quality_contract`
- `section_planning_preferences`

If any required `<TOPIC_DIR>/topic.yaml` field is missing:

- stop
- report the missing fields
- do not auto-repair `<TOPIC_DIR>/topic.yaml`
- do not create or update authoring artifacts

During preflight, read `<SECTION_DIR>/section.yaml`. If the `section_id` inside `<SECTION_DIR>/section.yaml` does not match the requested `SECTION_ID`, stop and do not create or modify authoring artifacts.

If `<SECTION_DIR>/section.yaml` is incomplete or wrong, stop and report that section planning should be revised. Do not modify `<SECTION_DIR>/section.yaml` unless the user explicitly asks for a section-plan revision.

During preflight, if `<SECTION_DIR>/state.yaml` exists and says `approved_by_user: true`, stop. Do not revise an approved section unless the user explicitly asks to revise it.

Before authoring, inspect `depends_on_sections` from `<SECTION_DIR>/section.yaml` if present. For each dependency, check `<TOPIC_DIR>/sections/<dependency_section_id>/state.yaml`. If any dependency is missing or is not `approved_by_user: true`, stop, explain which dependency is not approved, and do not author the requested section.

## Inputs To Read

When the skill is actually used, read:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/plan.yaml`
- `<TOPIC_DIR>/wiki/**`
- `<TOPIC_DIR>/sections/section_plan.yaml`
- `<SECTION_DIR>/section.yaml`
- `<TOPIC_DIR>/.wheels_state.json` if present
- `AGENTS.md`
- `templates/article_shapes.md`
- `prompts/audience_profiles.md`
- relevant source anchors from `<TOPIC_DIR>/wiki/**`
- relevant source asset audit files under `<TOPIC_DIR>/wiki/source_assets/**` when `<SECTION_DIR>/section.yaml` contains `source_assets` or `visual_verification_required`
- evidence image paths referenced in `<SECTION_DIR>/section.yaml`, such as `<TOPIC_DIR>/wiki/source_assets/pages/**` or `<TOPIC_DIR>/wiki/source_assets/extracted/**`

Read `<SECTION_DIR>/section.yaml` first.

If `<TOPIC_DIR>/wiki/foundation_stack.md` exists, inspect it after reading `<SECTION_DIR>/section.yaml`, especially when `<SECTION_DIR>/section.yaml` contains `foundation_role` or `foundation_stack_refs`. Treat the foundation stack as read-only planning/source-grounding support. Do not use it as final prose directly and do not dump it into the section.

When `<SECTION_DIR>/section.yaml` contains `source_assets` or `visual_verification_required`, inspect the relevant files from:

- `<TOPIC_DIR>/wiki/source_assets/index.yaml`
- `<TOPIC_DIR>/wiki/source_assets/formulas.md`
- `<TOPIC_DIR>/wiki/source_assets/figures.md`
- `<TOPIC_DIR>/wiki/source_assets/tables.md`
- `<TOPIC_DIR>/wiki/source_assets/visual_audit.md`
- evidence image paths referenced in `<SECTION_DIR>/section.yaml`

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

- Do not modify `<TOPIC_DIR>/topic.yaml`.
- Do not modify `<TOPIC_DIR>/wiki/**`.
- Do not modify `<TOPIC_DIR>/wiki/source_assets/**`.
- Do not modify `<TOPIC_DIR>/raw/**`.
- Do not modify `<TOPIC_DIR>/plan.yaml`.
- Do not modify `<TOPIC_DIR>/.wheels_state.json`.
- Do not modify `<TOPIC_DIR>/sections/section_plan.yaml`.
- Do not modify `<SECTION_DIR>/section.yaml` unless the user explicitly asks for a section-plan revision.
- Do not modify `<TOPIC_DIR>/outputs/**`.
- Do not modify `<TOPIC_DIR>/reviews/**`.
- Do not modify other sections under `<TOPIC_DIR>/sections/<other_section_id>/**`.
- Do not modify any files outside the Allowed Writes list.
- Allowed writes are exhaustive; no other files may be created or modified.
- Explicit v1 fixture exception: do not modify `topics/word2vec/outputs/**` or `topics/word2vec/reviews/**` unless the user explicitly asks. This hard-coded fixture guard is intentional and does not replace `TOPIC_DIR` scoping for active topic work.
- Do not assemble final `<TOPIC_DIR>/outputs/publish/blog.md`.
- Do not assemble final `<TOPIC_DIR>/outputs/preview.html` for the full topic.

The section author must not enrich, repair, strengthen, or update `<TOPIC_DIR>/topic.yaml`. It must not add source-derived or section-derived fields to `<TOPIC_DIR>/topic.yaml`, including:

- `goal`
- `available_sources`
- `source_policy`
- `must_explain`
- paper-specific learning goals
- system-design-specific learning goals
- algorithm-specific learning goals
- source-derived claims
- discovered source inventory
- section plan metadata

## Source Asset Handling

When `<SECTION_DIR>/section.yaml` maps source assets to the section, consume those assets as read-only source evidence.

Use:

- `<TOPIC_DIR>/wiki/source_assets/formulas.md` to explain equations accurately
- `<TOPIC_DIR>/wiki/source_assets/figures.md` to understand paper figures, charts, and diagrams
- `<TOPIC_DIR>/wiki/source_assets/tables.md` to understand tables
- `<TOPIC_DIR>/wiki/source_assets/visual_audit.md` to respect caveats and verification needs
- page or extracted evidence images as source evidence, not as section visuals by default

Do not modify:

- `<TOPIC_DIR>/wiki/source_assets/**`
- `<TOPIC_DIR>/wiki/**`
- `<SECTION_DIR>/section.yaml`

Do not copy raw evidence images into the section by default. If a source asset inspires a teaching visual, create a simplified section-local visual under `<SECTION_DIR>/visuals/**` and document the transformation in `<SECTION_DIR>/authoring_notes.md` and `<SECTION_DIR>/source_notes.md`.

## Foundation / Background Use

Read `foundation_role` and `foundation_stack_refs` from `<SECTION_DIR>/section.yaml` when present.

Authoring behavior:

- If the section is a background/foundation section, write it as a real learning scaffold, not a shallow glossary.
- If the section is a bridge section, connect the prerequisite intuition to the first core topic mechanism.
- If the section is a core-topic section, introduce only the prerequisite intuition needed for that section and rely on prior approved sections where appropriate.
- Do not dump the entire `<TOPIC_DIR>/wiki/foundation_stack.md` into every section.
- Do not use `<TOPIC_DIR>/wiki/foundation_stack.md` as final prose directly.
- Convert foundation stack material into section-specific teaching.
- Avoid over-explaining concepts already established in prior approved sections.
- Avoid starting too abstractly.
- Technical terms may be introduced early when immediately grounded in plain English.

For background sections, use this teaching style:

- what this concept is
- why the reader needs it
- intuition-first explanation
- tiny example
- why it matters for the main topic
- enough-understanding check

For core sections, keep the ramp concise and local.

Article-shape behavior:

- For `paper_deep_dive`, use the foundation stack to introduce math and notation before paper equations. Include "what you do not need yet" when it prevents overlearning irrelevant background.
- For `system_design_deep_dive`, use the foundation stack to introduce system-design primitives before using them in architecture decisions. For `system_design_interview_l5_plus`, keep the main explanation strong L5 and use selective L6+ callouts.
- For `algorithm_walkthrough`, use the foundation stack to introduce data structures, complexity, and pattern intuition before optimized implementation.

### Formula Handling Rule

If the section depends on a formula asset:

- explain the intuition before the equation
- define every symbol used
- include a small worked example when useful
- explicitly state any simplification
- if `visual_verification_needed` is `true`, do not pretend the formula is fully verified
- either visually verify the evidence image if practical or mark the relevant prose as needing verification in `<SECTION_DIR>/authoring_notes.md`

### Figure And Table Handling Rule

If the section depends on figure or table assets:

- do not blindly copy dense paper visuals into the section
- decide whether to:
  - explain in text
  - redraw a simplified teaching visual under `<SECTION_DIR>/visuals/**`
  - use the original evidence image only as a reference
  - skip it with reason
- do not quote exact table or chart values unless they are marked reliable or visually verified
- if exact values are uncertain, describe the qualitative trend instead

## Authoring Notes First

Before writing polished prose, create `<SECTION_DIR>/authoring_notes.md`.

`<SECTION_DIR>/authoring_notes.md` must include:

- what question this section answers
- what the reader should understand by the end
- a `Prerequisite / Intuition Ramp` section
- source anchors and claims used
- source assets used, if any
- prerequisite concepts needed
- concepts assumed from prior approved sections
- terms and notation this section will introduce
- the concrete mental model and tiny example used before notation
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

`<SECTION_DIR>/authoring_notes.md` must also include a `Foundation / Background Use` section with:

- foundation_stack.md sections consulted
- prerequisites introduced in this section
- prerequisites assumed from prior approved sections
- intuition built before notation
- concepts deliberately deferred
- why the section does or does not need a foundation ramp

When source assets exist for the section, `<SECTION_DIR>/authoring_notes.md` must include a `Source Assets Used` section listing:

- formulas used
- figures used
- tables used
- page evidence used
- visual verification items
- which assets were used only as source evidence
- which assets were transformed into section teaching visuals

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

Use the repo virtual environment for Python instructions and commands:

- prefer `.venv/bin/python`
- do not use system Python
- do not install packages from inside the skill unless the user explicitly asks

## Media Rule

Generate media only when it clarifies the section.

If media is generated, it must be section-local under `<SECTION_DIR>/visuals/**`, `<SECTION_DIR>/manim/**`, or `<SECTION_DIR>/manim_media/**`. Media must have a clear teaching purpose and must not be decorative filler.

If media is based on source assets, it must be a section-local teaching artifact unless there is a clear reason to embed original evidence. Preserve source fidelity, but prefer simplified explanatory visuals over dense paper screenshots.

For `article_shape: system_design_deep_dive` and especially `audience_profile: system_design_interview_l5_plus`, prefer architecture, sequence, data-flow, pipeline, cache-flow, data-model, or state diagrams. Mermaid or Graphviz may be better than matplotlib for architecture and sequence diagrams. Diagrams must show meaningful boundaries and data/control flow, not generic boxes. Captions should explain the design decision the diagram supports.

## Code-Generated Technical Visuals Policy

For technical teaching visuals, prefer code-generated visuals when feasible.

This applies especially to visuals involving plots, curves, loss landscapes, optimizer trajectories, gradient updates, vector geometry, matrices, attention maps, probability distributions, algorithm traces, state-machine-like flows, system diagrams with structured layout, charts derived from source assets, and simplified redraws of paper figures or tables.

The preferred artifact pattern is:

```text
<SECTION_DIR>/visuals/<visual_id>_spec.md
<SECTION_DIR>/visuals/<visual_id>.py
<SECTION_DIR>/visuals/<visual_id>.svg
<SECTION_DIR>/visuals/<visual_id>.png
```

The Python file is the source of truth. The SVG/PNG files are rendered outputs.

When creating a technical visual:

1. First write `<SECTION_DIR>/visuals/<visual_id>_spec.md`.
2. Prefer writing Python source at `<SECTION_DIR>/visuals/<visual_id>.py`.
3. Render both `<SECTION_DIR>/visuals/<visual_id>.svg` and `<SECTION_DIR>/visuals/<visual_id>.png`.
4. Use `.venv/bin/python` to run the visual script.
5. Use deterministic visual generation.

The visual spec must include:

- teaching purpose
- exact concept being shown
- what each visual mark means
- what the visual must not imply
- source assets used, if any
- whether the visual is conceptual or source-derived
- caption
- review checklist

Deterministic visual generation means:

- no uncontrolled randomness
- set an explicit seed if randomness is useful
- fixed figure size
- explicit axis limits where appropriate
- explicit margins/layout
- readable font sizes
- no clipped text
- no text outside canvas
- no hidden labels
- no overlapping labels
- no oversized arrows
- no decorative-only visuals
- clear caption
- visual meaning matches section prose

If using matplotlib:

- use matplotlib, not seaborn
- avoid unnecessary styling
- use clear labels and annotations
- prefer simple, high-contrast layouts
- avoid crowded legends
- save SVG and PNG
- use `bbox_inches` only carefully; ensure it does not crop labels
- consider `constrained_layout` or explicit `subplots_adjust`
- close figures after saving

If a visual is based on a source asset:

- do not blindly reproduce the paper visual
- create a simplified teaching redraw when appropriate
- document the transformation in `<SECTION_DIR>/authoring_notes.md` and `<SECTION_DIR>/source_notes.md`
- preserve source meaning
- do not quote exact values unless reliable or visually verified

`<SECTION_DIR>/preview.html` should use the rendered SVG or PNG. It should not embed the Python source. It should include a caption explaining whether the image is conceptual or source-derived.

Keep visual source local to the section. Do not write visuals under `<TOPIC_DIR>/outputs/**` during authoring.

Hand-authored SVG is allowed only when:

- the visual is simple
- code generation would add unnecessary complexity
- the reviewer can still inspect rendered output
- the author documents why `hand_svg` was chosen in `<SECTION_DIR>/authoring_notes.md`

Avoid:

- freehand complex SVG as the default
- AI-generated images for technical diagrams requiring accuracy
- decorative graphics that do not teach a mechanism
- raw paper screenshots as reader-facing visuals unless there is a clear teaching reason
- copying dense paper figures directly when a simplified teaching redraw would be clearer

## Prose Rule

Write `<SECTION_DIR>/draft.md` as the canonical section draft.

Write `<SECTION_DIR>/blog_fragment.md` as the publishable fragment for this section only.

Before writing prose, list in `<SECTION_DIR>/authoring_notes.md` the terms and notation the section will introduce.

Start prose with the simplest concrete mental model that gives the reader an object to think about. Do not overload the opening with stacked abstractions.

For notation, formulas, algorithms, paper-specific terms, and expert vocabulary, prefer this order:

```text
concrete object -> plain-English intuition -> tiny example -> notation -> paper terminology -> formula/algorithm
```

This is a preferred teaching flow, not a rigid template that every paragraph must follow.

Avoid this order:

```text
notation -> formula -> terminology -> explanation
```

Technical terms may be introduced early if they are immediately grounded in plain English, especially when the term is central to the section. The issue is not using technical terms; the issue is using them as if the reader already understands them.

Good: "Adam is an optimizer: a rule that decides how to change model parameters after seeing a gradient."

Bad: "Adam is a first-order stochastic optimizer for scalar objectives over high-dimensional parameter spaces."

For each technical term introduced, decide whether it needs a plain-English definition, a tiny example, a later formal definition, or can rely on prior approved sections. Make this judgment based on `audience_profile`, `prerequisite_concepts`, `depends_on_sections`, terms already introduced in prior approved sections, the section learning goal, and the section's position in the article.

Prefer "term + plain-English grounding" over avoiding the term entirely. Keep the ramp concise; do not create a glossary dump. Avoid defining every possible term if it distracts from the section's learning goal.

Keep the prerequisite/intuition ramp concise but real. Do not add filler.

For background/foundation sections, do not stop at definitions. Build intuition with examples and enough-understanding checks. For core sections, avoid re-teaching the whole foundation stack; include only the local ramp needed to understand the current mechanism.

Do not write full-topic `blog.md`. Do not jump ahead to later sections. Do not summarize future sections except with brief forward pointers when needed.

### System Design Deep Dive Authoring

For `article_shape: system_design_deep_dive` and/or `audience_profile: system_design_interview_l5_plus`, author sections as design reasoning, not generic architecture prose.

The main explanation should be a strong L5 path. Add L6+ callouts only when they add senior-level depth. Keep those callouts concise and clearly marked with labels such as:

- "L6+ extension:"
- "Senior-level tradeoff:"
- "Where a stronger answer goes deeper:"

Do not repeat the whole section separately for L5, L6, and L7. Avoid padding. Do not add L6+ callouts when they are filler.

Each relevant section should include:

- requirements or constraints before architecture
- concrete API examples when applicable
- concrete data model examples when applicable
- explicit SQL vs NoSQL tradeoffs when storage is central
- step-by-step workflows
- sync vs async boundary explanations
- consistency model discussion when relevant
- failure modes and mitigations
- observability/metrics when operationally relevant
- capacity or bottleneck reasoning when relevant
- clear separation of public facts vs inferred design choices
- diagrams that clarify architecture, sequence, data flow, pipelines, state, or data models

Wording policy:

- Do not claim a real company or system does something internally unless supported by a public source in `<TOPIC_DIR>/wiki/**`.
- For inferred choices, use phrasing such as "a YouTube-like system could..." or "one plausible design is...".
- Use public sources as grounding, not as text to copy.
- Do not lift prose, diagrams, or structure from Alex Xu, Grokking, or similar interview-prep sources.

Useful L6+ callout topics include multi-region architecture, consistency boundaries, capacity modeling, operational maturity, cost controls, incident handling, data evolution, platform abstractions, organizational/ownership tradeoffs, abuse/moderation implications, observability and SLOs, and migration/evolution strategy.

## Preview Rule

Create `<SECTION_DIR>/preview.html` as a reader-facing preview for this section only.

It should render the section draft, visuals, code snippets, and captions in context. It should not include internal planning notes unless clearly collapsed or omitted.

If the section creates simplified visuals based on source assets, include the simplified section visual in `<SECTION_DIR>/preview.html`.

Do not expose raw evidence page screenshots in the reader-facing preview unless there is a clear teaching reason. If a paper figure or table is referenced but not reproduced, mention it in prose rather than embedding raw evidence by default.

Do not create or modify `<TOPIC_DIR>/outputs/preview.html`.

## Source Notes

Create or update `<SECTION_DIR>/source_notes.md` with:

- source anchors used
- source assets used
- claims supported by each source
- assumptions or simplifications
- visual verification caveats
- which source assets were used only as evidence and which were transformed into section-local teaching visuals
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
- results not present in `<TOPIC_DIR>/wiki/**`, `<TOPIC_DIR>/wiki/source_assets/**`, or source anchors
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
