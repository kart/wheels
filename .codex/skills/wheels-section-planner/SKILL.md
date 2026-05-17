---
name: wheels-section-planner
description: Convert a bootstrapped Wheels <TOPIC_DIR>/wiki/** into a section-by-section learning plan for user review before any section authoring begins.
---

# wheels-section-planner

Use this skill after `wheels-topic-bootstrap` has completed. This skill converts `<TOPIC_DIR>/wiki/**` into a section-by-section learning plan that the user can review before any section authoring begins.

This skill plans the learning/content sequence only. It must not author content, generate prose, generate media, generate code, create or modify previews, or create or modify publish artifacts.

## Topic Resolution

This skill requires an active topic id.

Use this convention everywhere:

- `TOPIC_ID` = the topic id provided by the user
- `TOPIC_DIR` = `topics/<TOPIC_ID>`

All topic-specific files must be referenced through `TOPIC_DIR`:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/plan.yaml`
- `<TOPIC_DIR>/wiki/**`
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

## Inputs To Inspect

Before creating section planning files, inspect:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/plan.yaml`
- `<TOPIC_DIR>/wiki/**`
- `<TOPIC_DIR>/wiki/source_map.md` if present
- `<TOPIC_DIR>/wiki/glossary.md` if present
- `<TOPIC_DIR>/wiki/open_questions.md` if present
- `AGENTS.md`
- `templates/article_shapes.md`
- `prompts/audience_profiles.md`
- `prompts/reviewer.md` if useful

## Write Scope

This skill may create directories and files only under:

- `<TOPIC_DIR>/sections/**`

If `<TOPIC_DIR>/sections/**` already exists, inspect it first. Update only planning files intentionally. Do not delete existing section planning unless explicitly asked.

Files under `<TOPIC_DIR>/sections/**` must contain planning metadata only. They must not contain draft prose, code bodies, SVG/diagram markup, rendered HTML, or publish Markdown.

Expected output files:

- `<TOPIC_DIR>/sections/README.md`
- `<TOPIC_DIR>/sections/section_plan.yaml`
- `<TOPIC_DIR>/sections/<section_id>/section.yaml` for each planned section

This skill must not modify:

- `scripts/wheels_prompt.py`
- `<TOPIC_DIR>/raw/**`
- `<TOPIC_DIR>/outputs/**`
- `<TOPIC_DIR>/reviews/**`
- `<TOPIC_DIR>/outputs/preview.html`
- `<TOPIC_DIR>/outputs/publish/blog.md`

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
mechanism_strategy:
media_strategy:
code_strategy:
toy_to_real_strategy:
user_review_policy:
  mode: section_by_section
  must_wait_for_approval: true
status: planned
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
prerequisite_concepts:
depends_on_sections:
authoring_order_notes:
key_questions_to_answer:
core_mechanism:
  type: runnable_code | pseudocode | worked_example | visual_trace | architecture_diagram | state_machine | sequence_diagram | table | simulation | none_with_reason
  why_this_mechanism:
media_needed:
  - type:
    purpose:
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

Use stable, readable `section_id` values such as `section_01_motivation` or `section_04_core_mechanism`.

## Required README

Create `<TOPIC_DIR>/sections/README.md` explaining:

- what `<TOPIC_DIR>/sections/**` is
- how section planning works
- how later skills should consume each `<TOPIC_DIR>/sections/<section_id>/section.yaml`
- that the user must approve one section before moving to the next

## Planning Principles

- Mechanism-first, not prose-first.
- Plan code when it can naturally clarify the concept; do not generate code in this skill.
- Code should not be forced when a diagram, worked example, state machine, or table teaches better.
- Every major section should identify a concrete teaching mechanism.
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

For `article_shape: system_design_deep_dive`, plan sections in this general order:

- concrete user journey
- requirements and constraints
- back-of-the-envelope scale
- APIs/entities
- high-level architecture
- data model
- deep dives into hard parts
- failure modes
- observability/operations
- tradeoffs and final design

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
