---
name: wheels-section-planner
description: Convert a bootstrapped Wheels <TOPIC_DIR>/wiki/** into a section-by-section learning plan for user review before any section authoring begins.
---

# wheels-section-planner

Use this skill after `wheels-topic-bootstrap` has completed. This skill converts `<TOPIC_DIR>/wiki/**` into a section-by-section learning plan that the user can review before any section authoring begins.

This skill plans the learning/content sequence only. It must not author content, generate prose, generate media, generate code, create or modify previews, or create or modify publish artifacts.

`scripts/init_topic.py` owns deterministic `<TOPIC_DIR>/topic.yaml` creation. This skill may read `<TOPIC_DIR>/topic.yaml`, but must treat it as read-only configuration.

## Tooling Policy

For any future Python instructions, examples, or optional validation commands, prefer `.venv/bin/python`. Do not use system Python. Do not install packages from inside the skill unless the user explicitly asks. If dependencies are missing, note that the user may install them with commands such as `.venv/bin/python -m pip install matplotlib numpy pillow cairosvg playwright pymupdf` and `.venv/bin/python -m playwright install chromium`.

## Topic Resolution

This skill requires an active topic id.

Use this convention everywhere:

- `TOPIC_ID` = the topic id provided by the user
- `TOPIC_DIR` = `topics/<TOPIC_ID>`

All topic-specific files must be referenced through `TOPIC_DIR`:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/plan.yaml`
- `<TOPIC_DIR>/wiki/**`
- `<TOPIC_DIR>/wiki/source_assets/**`
- `<TOPIC_DIR>/wiki_preview/**`
- `<TOPIC_DIR>/sections/**`
- `<TOPIC_DIR>/outputs/**`
- `<TOPIC_DIR>/reviews/**`
- `<TOPIC_DIR>/.wheels_state.json`

Do not use naked topic-specific references like `topic.yaml`, `plan.yaml`, `wiki/**`, `outputs/**`, `reviews/**`, or `.wheels_state.json` unless the text explicitly says "inside TOPIC_DIR".

If `TOPIC_ID` is missing or ambiguous, stop and ask for the topic id. Never mix files from multiple topics in one skill run.

## Preflight Validation

Before planning, verify these required bootstrap inputs exist:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/plan.yaml`
- `<TOPIC_DIR>/wiki/**`

If any required bootstrap input is missing:

- stop before creating `<TOPIC_DIR>/sections/**`
- tell the user to run `wheels-topic-bootstrap` first
- do not create `<TOPIC_DIR>/sections/section_plan.yaml`
- do not create `<TOPIC_DIR>/sections/<section_id>/section.yaml` files

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
- do not create or update `<TOPIC_DIR>/sections/**`

If `<TOPIC_DIR>/wiki/**` is missing or incomplete, stop and tell the user to run `wheels-topic-bootstrap` first. Do not create `<TOPIC_DIR>/sections/**` from raw sources alone.

## Inputs To Inspect

Before creating section planning files, inspect:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/plan.yaml`
- `<TOPIC_DIR>/wiki/**`
- `<TOPIC_DIR>/wiki/source_map.md` if present
- `<TOPIC_DIR>/wiki/source_summary.md` if present
- `<TOPIC_DIR>/wiki/glossary.md` if present
- `<TOPIC_DIR>/wiki/open_questions.md` if present
- `<TOPIC_DIR>/wiki/source_assets/index.yaml` if present
- `<TOPIC_DIR>/wiki/source_assets/formulas.md` if present
- `<TOPIC_DIR>/wiki/source_assets/figures.md` if present
- `<TOPIC_DIR>/wiki/source_assets/tables.md` if present
- `<TOPIC_DIR>/wiki/source_assets/visual_audit.md` if present
- `AGENTS.md`
- `templates/article_shapes.md`
- `prompts/audience_profiles.md`
- `prompts/reviewer.md` if useful

## Write Scope

This skill owns only section planning artifacts:

- `<TOPIC_DIR>/sections/README.md`
- `<TOPIC_DIR>/sections/section_plan.yaml`
- `<TOPIC_DIR>/sections/<section_id>/section.yaml`

If `<TOPIC_DIR>/sections/**` already exists, inspect it first. Update only planning files intentionally. Do not delete existing section planning unless explicitly asked.

Files under `<TOPIC_DIR>/sections/**` must contain planning metadata only. They must not contain draft prose, code bodies, SVG/diagram markup, rendered HTML, or publish Markdown.

Expected output files:

- `<TOPIC_DIR>/sections/README.md`
- `<TOPIC_DIR>/sections/section_plan.yaml`
- `<TOPIC_DIR>/sections/<section_id>/section.yaml` for each planned section

This skill must not modify:

- `scripts/wheels_prompt.py`
- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/raw/**`
- `<TOPIC_DIR>/wiki/**`
- `<TOPIC_DIR>/wiki/source_assets/**`
- `<TOPIC_DIR>/plan.yaml`
- `<TOPIC_DIR>/.wheels_state.json`
- `<TOPIC_DIR>/outputs/**`
- `<TOPIC_DIR>/reviews/**`
- `<TOPIC_DIR>/outputs/preview.html`
- `<TOPIC_DIR>/outputs/publish/blog.md`

This skill must not enrich, repair, strengthen, or update `<TOPIC_DIR>/topic.yaml`. It must not add source-derived or topic-specific fields to `<TOPIC_DIR>/topic.yaml`, including:

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

If `TOPIC_ID` is `word2vec`, treat `<TOPIC_DIR>` as the v1 demo fixture. Do not modify `<TOPIC_DIR>/outputs/**` or `<TOPIC_DIR>/reviews/**` unless explicitly asked.

## Purpose

The section plan should break the topic into reviewable learning units.

Each section should be small enough that the user can:

- read a generated preview produced later by an authoring skill
- ask clarifying questions
- request fixes
- approve it
- then move to the next section

The section planner must not author content. It only plans the learning/content sequence.

## Source Asset Audit Integration

If `<TOPIC_DIR>/wiki/source_assets/**` exists, treat it as read-only source evidence created by bootstrap. Use it to decide which formulas, figures, charts, diagrams, tables, or page screenshots matter for each planned section.

When source assets are present:

- inspect `<TOPIC_DIR>/wiki/source_assets/index.yaml`
- inspect `<TOPIC_DIR>/wiki/source_assets/formulas.md`
- inspect `<TOPIC_DIR>/wiki/source_assets/figures.md`
- inspect `<TOPIC_DIR>/wiki/source_assets/tables.md`
- inspect `<TOPIC_DIR>/wiki/source_assets/visual_audit.md`
- map relevant source assets to the appropriate `<TOPIC_DIR>/sections/<section_id>/section.yaml`
- include open visual verification items in `<TOPIC_DIR>/sections/section_plan.yaml`
- do not copy source asset files
- do not render new pages
- do not crop images
- do not create media, code, prose, previews, or publish files
- do not modify `<TOPIC_DIR>/wiki/source_assets/**`

If no `<TOPIC_DIR>/wiki/source_assets/**` directory exists:

- set `source_assets_available: false` in `<TOPIC_DIR>/sections/section_plan.yaml`
- do not fail solely because source assets are absent
- do fail and tell the user to rerun `wheels-topic-bootstrap` only if the topic clearly depends on formula/table/figure evidence and the wiki is not sufficient for source-grounded section planning

Source asset mappings are planning metadata only. They should point to existing evidence paths and planned section usage; they must not generate section visuals.

## Code-Generated Technical Visuals Policy

For technical teaching visuals, prefer code-generated visuals when feasible.

This applies especially to visuals involving plots, curves, loss landscapes, optimizer trajectories, gradient updates, vector geometry, matrices, attention maps, probability distributions, algorithm traces, state-machine-like flows, system diagrams with structured layout, charts derived from source assets, and simplified redraws of paper figures or tables.

The preferred artifact pattern for later authoring is:

```text
<SECTION_DIR>/visuals/<visual_id>_spec.md
<SECTION_DIR>/visuals/<visual_id>.py
<SECTION_DIR>/visuals/<visual_id>.svg
<SECTION_DIR>/visuals/<visual_id>.png
```

The Python file is the source of truth. The SVG/PNG files are rendered outputs.

Planner behavior:

- For technical visuals, default `preferred_generation_method` to `code_generated` unless there is a strong reason not to.
- For plots, trajectories, curves, matrices, optimizer/gradient illustrations, and conceptual technical diagrams, prefer `suggested_tool: matplotlib`.
- For graph/flow diagrams, use Graphviz or Mermaid only when already available and clearly better for the diagram.
- Use Manim only when animation or step-by-step math transformation is specifically useful.
- Use `hand_svg` only for very simple diagrams where code would add unnecessary complexity, and explain why in planning metadata.
- Avoid AI-generated images for technical diagrams requiring accuracy.
- Avoid decorative-only visuals.
- Avoid raw paper screenshots as reader-facing visuals unless there is a clear teaching reason.
- For formula/figure/table source assets, plan simplified teaching redraws as code-generated visuals when appropriate.
- Do not generate visual code, SVG, PNG, media, or previews in this planner. Planning metadata only.

## Required Top-Level Plan

Create `<TOPIC_DIR>/sections/section_plan.yaml` with at least:

```yaml
topic_id:
topic_dir:
article_shape:
audience_profile:
planning_inputs:
section_order:
  - section_id:
    title:
    reason_for_position:
authoring_order_notes:
section_dependencies:
global_prerequisite_ladder:
source_coverage_strategy:
source_asset_strategy:
  source_assets_available: true | false
  important_assets:
    - asset_id:
      type:
      likely_section:
      visual_verification_needed:
  open_visual_verification_items:
    - item:
mechanism_strategy:
media_strategy:
code_strategy:
toy_to_real_strategy:
prerequisite_ramp_strategy:
  default_order: "concrete object -> plain-English intuition -> tiny example -> notation -> paper terminology -> formula/algorithm"
  audience_constraints:
  section_1_assumptions:
user_review_policy:
  mode: section_by_section
  must_wait_for_approval: true
status: planned
```

System design fields are optional and conditional. They should not be emitted for non-system-design sections unless explicitly relevant.

For `article_shape: system_design_deep_dive`, `audience_profile: system_design_interview_l5_plus`, or explicitly system-design sections, add relevant top-level planning fields such as:

```yaml
system_design_strategy:
  applies: true | false
  main_path_level: strong_l5
  l6_plus_policy: selective_only
  requirements_strategy:
  capacity_strategy:
  api_strategy:
  data_model_strategy:
  workflow_strategy:
  reliability_strategy:
  observability_strategy:
```

## Required Section Files

Create one `<TOPIC_DIR>/sections/<section_id>/section.yaml` for each planned section. Each file must include at least:

```yaml
section_id:
title:
status: planned
learning_goal:
reader_outcome:
source_anchors:
  - source:
    relevant_claims:
source_assets:
  formulas:
    - asset_id:
      reason:
      evidence_image:
      visual_verification_needed:
  figures:
    - asset_id:
      reason:
      evidence_image:
      recommended_treatment:
      visual_verification_needed:
  tables:
    - asset_id:
      reason:
      evidence_image:
      qualitative_or_quantitative:
      visual_verification_needed:
  pages:
    - asset_id:
      reason:
      evidence_image:
visual_verification_required:
  - asset_id:
    reason:
prerequisite_concepts:
prerequisite_ladder:
  assumed_concepts:
  concepts_introduced_here:
  concrete_mental_model:
  tiny_example:
terms_that_must_be_introduced_before_use:
term_introduction_strategy:
  immediate_plain_english:
  tiny_example_needed:
  already_established_in:
  can_be_used_lightly:
  defer_formal_definition_until:
notation_introduction_order:
intuition_before_notation_notes:
depends_on_sections:
authoring_order_notes:
key_questions_to_answer:
core_mechanism:
  type: runnable_code | pseudocode | worked_example | visual_trace | architecture_diagram | state_machine | sequence_diagram | table | simulation | none_with_reason
  why_this_mechanism:
media_needed:
  - type:
    purpose:
    preferred_generation_method: code_generated | hand_svg | manim | mermaid | none
    suggested_tool: matplotlib | graphviz | manim | mermaid | plain_svg | none
    visual_source_expected: true | false
    rendered_outputs_expected:
      - svg
      - png
    source_assets_used:
      - asset_id:
    review_requirements:
      - rendered_visual_check
      - no_clipping
      - no_misleading_implication
      - caption_matches_visual
code_needed:
  required: true | false
  why:
  artifact_type:
toy_or_scaled_down_demo:
  description:
  what_it_demonstrates:
  what_it_omits:
toy_to_real_bridge:
expected_reader_confusions:
section_specific_review_checks:
completion_criteria:
user_review_gate:
  required: true
  instruction: "Stop after this section is authored/reviewed/fixed and wait for user approval before continuing."
```

System design fields are optional and conditional. Include the following fields only when `article_shape` is `system_design_deep_dive`, `audience_profile` is `system_design_interview_l5_plus`, or the section is explicitly a system-design section. For non-system-design topics, do not include these fields unless directly relevant; do not pollute `paper_deep_dive`, `algorithm_walkthrough`, or `general_concept_deep_dive` section files with empty system-design fields.

```yaml
design_questions:
  - question:
requirements_covered:
  functional:
  non_functional:
design_decisions:
  - decision:
    options_considered:
    chosen_option:
    reason:
    tradeoffs:
    l6_plus_extension:
apis_to_design:
  - name:
    purpose:
    request_shape:
    response_shape:
    consistency_expectation:
    failure_cases:
data_model:
  entities:
  storage_choice:
  sql_vs_nosql_reasoning:
  indexes:
  partitioning_key:
  consistency_model:
  l6_plus_extension:
workflows:
  - name:
    steps:
    sync_or_async:
    failure_modes:
    retry_idempotency_notes:
diagrams_needed:
  - type: architecture | sequence | data_model | state_machine | pipeline | cache_flow
    purpose:
    preferred_generation_method: code_generated | mermaid | graphviz | hand_svg
    suggested_tool:
scale_and_capacity:
  assumptions:
  bottlenecks:
  scaling_strategy:
  l6_plus_extension:
failure_modes:
  - failure:
    mitigation:
    detection:
    l6_plus_extension:
observability:
  metrics:
  logs:
  traces:
  alerts:
  slos:
source_grounding:
  known_public_facts:
  inferred_design_choices:
  sources_to_consult:
l6_plus_callouts:
  - topic:
    why_it_matters:
    where_to_include:
```

Use stable, readable `section_id` values such as `section_01_motivation` or `section_04_core_mechanism`.

## Required README

Create `<TOPIC_DIR>/sections/README.md` explaining:

- what `<TOPIC_DIR>/sections/**` is
- how section planning works
- how later skills should consume each `<TOPIC_DIR>/sections/<section_id>/section.yaml`
- that the user must approve one section before moving to the next

## Planning Principles

- Mechanism-first, not prose-first.
- Prerequisite-ramp first, then mechanism. Before a section introduces notation, formulas, algorithms, paper-specific terms, or expert vocabulary, it must build the minimum beginner mental model needed to understand them.
- Prefer this teaching order: concrete object -> plain-English intuition -> tiny example -> notation -> paper terminology -> formula/algorithm. This is a preferred teaching flow, not a rigid template that every paragraph must follow.
- Avoid this teaching order: notation -> formula -> terminology -> explanation.
- Each planned section should identify concepts it assumes and concepts it must introduce.
- Each section should list terms that must be introduced before use and the order in which notation should be introduced.
- `terms_that_must_be_introduced_before_use` should not mean every technical word. It should mean terms that are central, likely confusing, or not already established.
- Use `term_introduction_strategy` to decide, based on `audience_profile`, `prerequisite_concepts`, `depends_on_sections`, terms already introduced in prior approved sections, section learning goal, and section position, which terms need immediate plain-English grounding, a tiny example, a later formal definition, or no extra explanation.
- For `beginner_technical` audiences, section 1 must not assume domain-specific machinery unless it is explicitly listed as a prerequisite.
- Plan code when it can naturally clarify the concept; do not generate code in this skill.
- Code should not be forced when a diagram, worked example, state machine, or table teaches better.
- Every major section should identify a concrete teaching mechanism.
- Every planned technical visual should specify whether visual source is expected, what tool should generate it, which rendered outputs are expected, and what rendered review checks are required.
- For technical visuals, prefer code-generated visuals with deterministic generation and rendered SVG/PNG outputs.
- Every major section should map relevant source assets from `<TOPIC_DIR>/wiki/source_assets/**` when that audit exists.
- Every section should include a toy-to-real bridge when applicable.
- Every section should have explicit expected reader confusions.
- Every section should have completion criteria.
- Every section should have a user review gate.
- Keep section scope small enough for one author-review-fix-approval loop.

`media_needed` and `code_needed` are planning fields only. They must not result in generated media, code, diagrams, Manim, SVG, rendered HTML, `<TOPIC_DIR>/outputs/preview.html`, or `<TOPIC_DIR>/outputs/publish/blog.md` during this skill.

## Article-Shape Rules

### Research Paper Deep Dive

For `article_shape: paper_deep_dive` or research paper topics:

- Preserve the paper's intellectual order where useful.
- Add prerequisite sections before the paper walkthrough if needed.
- Do not merely mirror paper headings mechanically.
- Each section should answer a learning question.
- Include source anchors to paper sections, equations, figures, or claims when available.
- Separate motivation/problem, prior work, core idea, mechanism, training/execution workflow, experiments/results, limitations, real-world relevance, and what came next.
- Plan code when it clarifies a mechanism; do not generate code in this skill.
- Use worked examples or diagrams when code would be distracting.
- Include a toy-to-real bridge wherever the paper's real setup is too large to reproduce.

### System Design Deep Dive

For `article_shape: system_design_deep_dive`, plan a serious system design deep dive, not a generic interview-prep outline. When `audience_profile: system_design_interview_l5_plus` is present, the main path should be useful to a strong L5 candidate and selective L6+ callouts should deepen only the decisions where senior-level reasoning materially helps.

Plan sections that cover, when applicable:

- problem framing and product scope
- functional requirements
- non-functional requirements
- capacity and traffic estimates
- core entities
- API design
- high-level architecture
- upload/write path
- read/playback path
- async workflows
- data model
- SQL vs NoSQL tradeoffs
- blob/object storage vs metadata storage
- partitioning/sharding strategy
- indexing/search strategy
- caching/CDN strategy
- eventing/queues/stream processing
- consistency choices
- id generation
- counters/analytics
- recommendations/feed path, when applicable
- abuse/moderation hooks, when applicable
- reliability and failure modes
- observability/metrics/SLOs
- security/privacy basics
- cost/performance tradeoffs
- evolution from simple design to real-world scale

For each relevant section, include system design planning fields in `<SECTION_DIR>/section.yaml` from the template above. Use them to capture design questions, requirements covered, design decisions, APIs, data model, workflows, diagrams, scale/capacity, failure modes, observability, source grounding, and selective L6+ callouts.

Planner behavior:

- Aim the default path at strong L5.
- Ensure every major section teaches design reasoning, not just components.
- Plan L6+ callouts selectively; do not require every section to have one.
- Add an L6+ callout only when it meaningfully deepens the design.
- Do not create separate L5/L6/L7 versions of each section.
- Avoid bloated repeated level-specific answers.
- Use clearly marked callout labels such as "L6+ extension:", "Senior-level tradeoff:", or "Where a stronger answer goes deeper:".
- Candidate L6+ topics include multi-region architecture, consistency boundaries, capacity modeling, operational maturity, cost controls, incident handling, data evolution, platform abstractions, organizational/ownership tradeoffs, abuse/moderation implications, observability and SLOs, and migration/evolution strategy.

Mechanisms may be architecture diagrams, sequence diagrams, tables, simulations, or pseudocode. Code is optional and should only be required when it clarifies an algorithm, simulation, or data structure. Always include a toy-to-real bridge for scale assumptions.

### Algorithm Walkthrough

For `article_shape: algorithm_walkthrough`, plan sections in this order:

- problem in plain English
- examples and constraints
- brute force
- why brute force is wasteful
- key insight
- visual dry run
- implementation
- complexity
- edge cases
- pattern and similar problems

Plan code as usually required; do not generate code in this skill. The mechanism should usually be a dry run plus runnable code.

### General Concept Deep Dive

For `article_shape: general_concept_deep_dive` or unknown shape:

- Plan around learning questions.
- Use prerequisite ladder first.
- Then motivation, mechanism, concrete examples, caveats, applications, and recap.
- Pick the best mechanism per section instead of forcing code.

## Stop Condition

After creating:

- `<TOPIC_DIR>/sections/README.md`
- `<TOPIC_DIR>/sections/section_plan.yaml`
- `<TOPIC_DIR>/sections/<section_id>/section.yaml` files

stop.

Present a concise section plan summary to the user and stop. Wait for explicit user approval before any section authoring begins.

After creating planning files, the skill may summarize the section plan in the assistant response only. It must not create a new summary file outside `<TOPIC_DIR>/sections/**`.

Do not author the first section. Do not generate section prose. Do not generate images, Manim, diagrams, code, `<TOPIC_DIR>/outputs/preview.html`, or `<TOPIC_DIR>/outputs/publish/blog.md`.
