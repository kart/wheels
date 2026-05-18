---
name: wheels-topic-bootstrap
description: Bootstrap a Wheels topic from TOPIC_DIR/topic.yaml and raw sources through plan.yaml, wiki compilation, and replan, stopping before section authoring.
---

# wheels-topic-bootstrap

Use this skill when starting or restarting the first half of a Wheels topic: topic setup, startup planning, source-grounded wiki compilation, and post-wiki replanning. Stop before drafting section prose.

This skill wraps the existing `scripts/wheels_prompt.py` workflow. Do not edit `scripts/wheels_prompt.py` unless a small compatibility bug blocks the workflow.

## Scope

This skill owns:

- validating an existing `<TOPIC_DIR>/topic.yaml` as read-only configuration
- generating `<TOPIC_DIR>/plan.yaml` through the startup prompt
- running wiki/source phases from `<TOPIC_DIR>/plan.yaml`
- generating rich PDF source audit files under `<TOPIC_DIR>/wiki/source_assets/**` when PDF sources exist
- generating `<TOPIC_DIR>/wiki/foundation_stack.md` as a source-grounded background/prerequisite planning artifact
- marking completed wiki phases in `<TOPIC_DIR>/.wheels_state.json`
- invoking post-wiki replanning
- requiring the revised plan to split future prose work into reader-approved sections

This skill does not own:

- writing final lesson prose
- generating section prose
- generating visuals
- generating code
- generating `<TOPIC_DIR>/outputs/preview.html`
- generating final publish drafts
- generating `<TOPIC_DIR>/outputs/publish/blog.md`
- creating, repairing, strengthening, enriching, or updating `<TOPIC_DIR>/topic.yaml`
- adding source-derived or paper-specific fields to `<TOPIC_DIR>/topic.yaml`
- editing files under `<TOPIC_DIR>/raw/**`
- deleting existing files under `<TOPIC_DIR>/outputs/**`

## Proposed Wheels Skill Architecture

Create the Wheels workflow as separate Codex skills so each phase has a clear stopping point:

1. `wheels-topic-bootstrap/SKILL.md`
   - Setup through compiled wiki and post-wiki replan.
   - Stops with a sectioned plan awaiting reader approval.

2. `wheels-section-planner/SKILL.md`
   - Converts the replanned `<TOPIC_DIR>/plan.yaml` into explicit reader-approved section contracts.
   - Owns section boundaries, prerequisites, source coverage, visual intent, and acceptance criteria.

3. `wheels-section-author/SKILL.md`
   - Generates exactly one approved section at a time.
   - Updates `<TOPIC_DIR>/outputs/lesson.md`, `<TOPIC_DIR>/outputs/visual_plan.md`, relevant assets/code, and `<TOPIC_DIR>/outputs/preview.html`.
   - Stops after that section.

4. `wheels-section-reviewer/SKILL.md`
   - Performs a section-level reviewer pass.
   - Writes only `<TOPIC_DIR>/reviews/<phase_id>_review.md`.
   - Does not edit `<TOPIC_DIR>/outputs/**`, `<TOPIC_DIR>/wiki/**`, visual/code artifacts, or `<TOPIC_DIR>/raw/**`.

5. `wheels-section-fixer/SKILL.md`
   - Validates section reviewer findings.
   - Applies accepted fixes only.
   - Writes `<TOPIC_DIR>/reviews/<phase_id>_fix_log.md`.

6. `wheels-final-audit/SKILL.md`
   - Runs whole-article review after all sections are drafted and fixed.
   - Checks source fidelity, teaching depth, visual correctness, code correctness, and preview quality.

7. `wheels-publish-pack/SKILL.md`
   - Creates the final copy-pasteable publish pack only after review/fix completion.
   - Owns `<TOPIC_DIR>/outputs/publish/**` and Jekyll front matter requirements.

Only this first skill is implemented now.

## Required Inputs

Use this topic path convention throughout the skill run:

- `TOPIC_ID` = the topic id provided by the user
- `TOPIC_DIR` = `topics/<TOPIC_ID>`

Never mix files from multiple topics in one skill run. If `TOPIC_ID` is missing or ambiguous, stop and ask for the topic id.

Ask for or infer:

- `TOPIC_ID`, matching `TOPIC_DIR`
- whether the topic folder already exists
- raw source availability under `<TOPIC_DIR>/raw/**`

Before editing anything, inspect:

- `README.md`
- `AGENTS.md`
- `scripts/wheels_prompt.py`
- `templates/article_shapes.md`
- `prompts/audience_profiles.md` if present
- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/plan.yaml` if present
- `<TOPIC_DIR>/wiki/**` if present
- `<TOPIC_DIR>/wiki/source_assets/**` if present

For regression awareness, if `TOPIC_ID` is `word2vec`, treat `<TOPIC_DIR>` as the v1 demo fixture. Do not rewrite its final article unless explicitly asked. Do not modify `<TOPIC_DIR>/outputs/**` or `<TOPIC_DIR>/reviews/**` unless explicitly asked.

## Bootstrap Write Scope

Bootstrap may update only:

- `<TOPIC_DIR>/plan.yaml`
- `<TOPIC_DIR>/wiki/**`
- `<TOPIC_DIR>/wiki/source_assets/index.yaml`
- `<TOPIC_DIR>/wiki/source_assets/formulas.md`
- `<TOPIC_DIR>/wiki/source_assets/figures.md`
- `<TOPIC_DIR>/wiki/source_assets/tables.md`
- `<TOPIC_DIR>/wiki/source_assets/visual_audit.md`
- `<TOPIC_DIR>/wiki/source_assets/pages/**`
- `<TOPIC_DIR>/wiki/source_assets/extracted/**`
- `<TOPIC_DIR>/wiki/foundation_stack.md`
- `<TOPIC_DIR>/wiki_preview/**`
- `<TOPIC_DIR>/.wheels_state.json` as needed

Bootstrap must not update:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/raw/**`
- `<TOPIC_DIR>/sections/**`
- `<TOPIC_DIR>/outputs/**`
- `<TOPIC_DIR>/reviews/**`
- `<TOPIC_DIR>/outputs/preview.html`
- `<TOPIC_DIR>/outputs/publish/blog.md`

`<TOPIC_DIR>/wiki/source_assets/**` files are generated wiki artifacts. Rendering PDF pages into `<TOPIC_DIR>/wiki/source_assets/pages/**` is source evidence generation, not section media generation.

## Topic YAML Handling

`scripts/init_topic.py` owns deterministic `<TOPIC_DIR>/topic.yaml` creation. Bootstrap treats `<TOPIC_DIR>/topic.yaml` as read-only configuration.

Required behavior:

1. Validate that `<TOPIC_DIR>/topic.yaml` exists.
2. Validate that it includes these deterministic fields created by `scripts/init_topic.py`:
   - `id`
   - `title`
   - `audience_profile`
   - `article_shape`
   - `workflow`
   - `publish_target`
   - `raw_resource_policy`
   - `quality_contract`
   - `section_planning_preferences`
3. If any required field is missing:
   - stop
   - report the missing field
   - tell the user to rerun `scripts/init_topic.py` or fix `<TOPIC_DIR>/topic.yaml` manually
   - do not auto-repair `<TOPIC_DIR>/topic.yaml`
4. Check that `article_shape` is one of:
   - `paper_deep_dive`
   - `system_design_deep_dive`
   - `algorithm_walkthrough`
   - `general_concept_deep_dive`
5. Do not modify `<TOPIC_DIR>/topic.yaml`.
6. Do not add source-derived or paper-specific fields to `<TOPIC_DIR>/topic.yaml`, including:
   - `goal`
   - `available_sources`
   - `source_policy`
   - `must_explain`
   - paper-specific learning goals
   - source-derived claims
   - discovered source inventory
7. Do not modify `<TOPIC_DIR>/raw/**`.

If source inventory or source grounding is needed, write it under:

- `<TOPIC_DIR>/wiki/source_map.md`
- `<TOPIC_DIR>/wiki/source_summary.md`
- another appropriate `<TOPIC_DIR>/wiki/**` file

## Foundation Stack Generation

During bootstrap, after source extraction/wiki compilation and before post-wiki replanning, create or update:

```text
<TOPIC_DIR>/wiki/foundation_stack.md
```

`foundation_stack.md` is a first-class generated wiki artifact. It is source-grounding and planning support for later section planning and authoring. It is not final article prose, not section authoring, not a publish output, and not permission to create `<TOPIC_DIR>/sections/**`, `<TOPIC_DIR>/outputs/**`, or `<TOPIC_DIR>/reviews/**`.

Build the foundation stack from:

- `<TOPIC_DIR>/topic.yaml` `article_shape`
- `<TOPIC_DIR>/topic.yaml` `audience_profile`
- `<TOPIC_DIR>/raw/**` source material
- compiled `<TOPIC_DIR>/wiki/**`
- available source asset audits under `<TOPIC_DIR>/wiki/source_assets/**`

Required structure for `<TOPIC_DIR>/wiki/foundation_stack.md`:

1. Topic and target audience
2. Goal of the foundation stack
3. Big picture of the topic
4. Prerequisite stack
5. Detailed prerequisite sections
6. For each prerequisite:
   - what the reader needs to know
   - intuition-first explanation
   - small example, analogy, or tiny worked case
   - why it matters for this topic
   - what enough understanding means
   - optional learn-more links when available
7. Best learning order
8. Final prerequisite checklist
9. Core mental model in one paragraph
10. Open foundation gaps or uncertainties

Quality bar:

- Do not create a shallow glossary.
- Do not merely list terms.
- Explain intuition before notation or jargon.
- Use concrete examples, analogies, or tiny worked cases.
- Explicitly say what the reader does not need to know yet when that prevents overlearning irrelevant background.
- Be deep enough that section planning can decide whether the article needs one or more background sections before the core topic.
- Clearly separate source-backed claims from bootstrap interpretation or inferred learning needs.

Article-shape guidance:

- For `paper_deep_dive`, include mathematical, conceptual, notation, and paper-specific prerequisite ladders. Include historical/contextual prerequisites only when useful. Do not require reading unrelated original papers unless truly necessary. Explain what can be skipped or deferred on a first pass.
- For `system_design_deep_dive`, include foundations such as requirements thinking, capacity estimation, API design, data modeling, SQL vs NoSQL, blob/object storage vs metadata storage, caching/CDN, queues and async workflows, stream processing, consistency, indexing/search, counters/analytics, failure modes, observability/SLOs, cost/performance tradeoffs, and evolution from simple to scaled design. For `audience_profile: system_design_interview_l5_plus`, make the main path support strong L5, identify selective L6+ depth where useful, do not create separate L5/L6/L7 prerequisite guides, and distinguish public facts from inferred design knowledge.
- For `algorithm_walkthrough`, include data structure prerequisites, complexity-analysis prerequisites, proof/intuition prerequisites when relevant, common pattern prerequisites, and edge-case thinking.
- For `general_concept_deep_dive`, infer the needed foundation stack from the topic and sources and make the prerequisite ladder explicit.

Guardrails:

- Do not modify `<TOPIC_DIR>/topic.yaml`.
- Do not modify `<TOPIC_DIR>/raw/**`.
- Do not create or modify `<TOPIC_DIR>/sections/**`.
- Do not create or modify `<TOPIC_DIR>/outputs/**`.
- Do not create or modify `<TOPIC_DIR>/reviews/**`.
- Do not write final article prose.
- Do not create section visuals/code/media.

## Rich PDF Source Audit

If `<TOPIC_DIR>/raw/**` contains one or more PDF sources, bootstrap should create or update a generated rich source asset audit under:

- `<TOPIC_DIR>/wiki/source_assets/index.yaml`
- `<TOPIC_DIR>/wiki/source_assets/formulas.md`
- `<TOPIC_DIR>/wiki/source_assets/figures.md`
- `<TOPIC_DIR>/wiki/source_assets/tables.md`
- `<TOPIC_DIR>/wiki/source_assets/visual_audit.md`
- `<TOPIC_DIR>/wiki/source_assets/pages/**`
- `<TOPIC_DIR>/wiki/source_assets/extracted/**`

This audit belongs in bootstrap because section planning and section authoring should know what formulas, figures, charts, tables, captions, and visually important pages exist before content generation begins.

The audit must preserve all existing ownership boundaries:

- Do not modify `<TOPIC_DIR>/topic.yaml`.
- Do not modify `<TOPIC_DIR>/raw/**`.
- Do not modify `<TOPIC_DIR>/sections/**`.
- Do not modify `<TOPIC_DIR>/outputs/**`.
- Do not modify `<TOPIC_DIR>/reviews/**`.

### What To Inspect

For each PDF under `<TOPIC_DIR>/raw/**`, inspect for:

- formulas
- equations
- figures
- charts
- diagrams
- tables
- captions
- pages where text extraction may be insufficient

Use available local tooling only. Do not modify project dependencies unless explicitly asked.

Prefer PDF text extraction plus rendered page images as the baseline. Do not use OCR by default. Use OCR only as a last resort when text extraction fails and the needed information is visible only in the rendered page image. If OCR is used, mark the extracted text as uncertain and set `visual_verification_needed: true` for the related asset.

If rendering or extraction tools are unavailable:

- still create the applicable `<TOPIC_DIR>/wiki/source_assets/**` notes
- record the limitation in `<TOPIC_DIR>/wiki/source_assets/visual_audit.md`
- mark relevant items as `visual_verification_needed: true`

### Page Rendering Rule

For short PDFs, roughly 30 pages or fewer, render all pages to:

```text
<TOPIC_DIR>/wiki/source_assets/pages/
```

Use deterministic names such as:

```text
paper_01_page_001.png
paper_01_page_002.png
```

For longer PDFs, bootstrap may render only candidate pages containing formulas, figures, tables, charts, diagrams, or captions. Explain the selection in:

```text
<TOPIC_DIR>/wiki/source_assets/visual_audit.md
```

Full-page screenshots are the baseline source of visual evidence.

### Extraction And Cropping Rule

If local tooling can extract or crop embedded figures/tables reliably, bootstrap may write extracted assets under:

```text
<TOPIC_DIR>/wiki/source_assets/extracted/
```

Cropped extraction is optional. Do not block the audit on cropped extraction if full-page screenshots exist.

### Formula Audit File

Create or update:

```text
<TOPIC_DIR>/wiki/source_assets/formulas.md
```

For every important formula or equation, include:

- `formula_id`
- source PDF path
- page number
- paper section if known
- nearby text/caption if useful
- normalized formula if confidently extracted
- symbol definitions
- intuition
- why it matters
- likely sections that will need it
- visual evidence image path
- `visual_verification_needed: true | false`

If formula extraction is uncertain, mark `visual_verification_needed: true` instead of guessing.

### Figure Audit File

Create or update:

```text
<TOPIC_DIR>/wiki/source_assets/figures.md
```

For every important figure/chart/diagram, include:

- `figure_id`
- source PDF path
- page number
- caption if available
- what it appears to show
- why it matters
- recommended treatment:
  - `use_original`
  - `redraw_simplified`
  - `explain_in_text`
  - `skip`
- visual evidence image path
- `visual_verification_needed: true | false`

### Table Audit File

Create or update:

```text
<TOPIC_DIR>/wiki/source_assets/tables.md
```

For every important table, include:

- `table_id`
- source PDF path
- page number
- caption if available
- what it appears to show
- whether exact values were reliably extracted
- whether to treat it qualitatively or quantitatively
- visual evidence image path
- `visual_verification_needed: true | false`

### Source Asset Index

Create or update:

```text
<TOPIC_DIR>/wiki/source_assets/index.yaml
```

It should include:

- `topic_id`
- list of PDF sources inspected
- list of source assets discovered
- asset id
- asset type: `formula | figure | table | page | chart | diagram`
- source PDF path
- page number
- evidence image path
- related wiki note file
- `visual_verification_needed`
- suggested section ids if known
- open verification items

### Visual Audit

Create or update:

```text
<TOPIC_DIR>/wiki/source_assets/visual_audit.md
```

It should summarize:

- which PDFs were inspected
- which pages were rendered
- which formulas/tables/figures need visual verification
- any extraction limitations
- any pages that should be manually spot-checked before final prose

### Section Planning Integration

Bootstrap itself must not create `<TOPIC_DIR>/sections/**`.

However, bootstrap should leave guidance in the plan/wiki notes that `wheels-section-planner` should later consume:

- `<TOPIC_DIR>/wiki/source_assets/index.yaml`
- `<TOPIC_DIR>/wiki/source_assets/formulas.md`
- `<TOPIC_DIR>/wiki/source_assets/figures.md`
- `<TOPIC_DIR>/wiki/source_assets/tables.md`
- `<TOPIC_DIR>/wiki/source_assets/visual_audit.md`

### Already-Bootstrapped Topics

For an already bootstrapped topic such as `TOPIC_ID=glove`, it is acceptable to run bootstrap again only to add or refresh:

- `<TOPIC_DIR>/wiki/source_assets/**`

When doing so, bootstrap must not modify:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/sections/**`
- `<TOPIC_DIR>/outputs/**`
- `<TOPIC_DIR>/reviews/**`

## Startup Plan Workflow

For every `wheels_prompt.py` command, prefer:

```bash
.venv/bin/python scripts/wheels_prompt.py ...
```

Use `python` only if the venv command is unavailable.

When invoking `wheels_prompt.py`, capture and read stdout. Treat the emitted prompt as the next phase specification. Codex may execute the emitted phase only if it is within bootstrap scope. If the emitted prompt conflicts with this skill's guardrails, `AGENTS.md`, or the user's explicit instructions, stop and report the conflict instead of proceeding.

If `<TOPIC_DIR>/plan.yaml` is missing or the user explicitly asks to restart planning:

1. Run:

   ```bash
   .venv/bin/python scripts/wheels_prompt.py --topic <TOPIC_ID> --startup
   ```

   If `.venv/bin/python` is unavailable, use:

   ```bash
   python scripts/wheels_prompt.py --topic <TOPIC_ID> --startup
   ```

2. Use the printed prompt as the authoritative startup task.
3. Create only `<TOPIC_DIR>/plan.yaml`.
4. Do not modify `<TOPIC_DIR>/topic.yaml`.
5. Do not generate `<TOPIC_DIR>/wiki/**`, lesson prose, visuals, `<TOPIC_DIR>/outputs/preview.html`, `<TOPIC_DIR>/reviews/**`, or publish files during startup planning.
6. Do not generate section prose, code, `<TOPIC_DIR>/outputs/preview.html`, or `<TOPIC_DIR>/outputs/publish/blog.md`.

After creating or finding `<TOPIC_DIR>/plan.yaml`, run:

```bash
.venv/bin/python scripts/wheels_prompt.py --topic <TOPIC_ID> --status
```

## Wiki Phase Loop

Run only phases needed to compile the wiki. Use the existing phase prompts rather than inventing phase instructions.

Guardrail: `wheels_prompt.py --next` mutates `<TOPIC_DIR>/.wheels_state.json` by setting `last_prompted_phase`. If `--next` emits a phase that bootstrap must not run, do not mark that phase done.

Loop:

1. Run:

   ```bash
   .venv/bin/python scripts/wheels_prompt.py --topic <TOPIC_ID> --next
   ```

2. Read the emitted phase prompt.
3. If the next phase is a wiki/source/extraction/compiled-wiki phase, execute exactly that phase.
   - If raw sources are discovered, use them only to generate `<TOPIC_DIR>/plan.yaml`, `<TOPIC_DIR>/wiki/**`, `<TOPIC_DIR>/wiki_preview/**`, and `<TOPIC_DIR>/.wheels_state.json` as needed.
   - Write source inventory, source grounding, and source summaries under `<TOPIC_DIR>/wiki/**`, not `<TOPIC_DIR>/topic.yaml`.
   - If PDF sources exist, create or update the rich PDF source audit under `<TOPIC_DIR>/wiki/source_assets/**` as part of source/wiki compilation.
4. If `--next` emits a non-wiki / non-source-extraction / non-compiled-wiki phase, stop immediately.
5. Do not execute that phase.
6. Do not run `--mark-done` for that phase.
7. Report that bootstrap has reached the pre-section boundary.
8. Do not run later lesson, prose, visual, preview, review, fix, or publish phases.
9. Do not generate section prose, visuals, code, `<TOPIC_DIR>/outputs/preview.html`, or `<TOPIC_DIR>/outputs/publish/blog.md`.
10. When the phase completion checks are satisfied, run:

   ```bash
   .venv/bin/python scripts/wheels_prompt.py --topic <TOPIC_ID> --mark-done
   ```

11. Repeat until the wiki is compiled.

Stop the wiki loop when:

- required `<TOPIC_DIR>/wiki/**` files from `<TOPIC_DIR>/plan.yaml` exist, and
- required `<TOPIC_DIR>/wiki/source_assets/**` audit files exist when `<TOPIC_DIR>/raw/**` contains PDF sources, and
- `<TOPIC_DIR>/wiki/foundation_stack.md` has been created or refreshed, and
- the next phase is replan, outline, lesson, content, visual, preview, review, fix, or publish.

If the startup plan did not include an explicit replan phase after `<TOPIC_DIR>/wiki/**` is compiled, still invoke the replan workflow below.

## Post-Wiki Replan Workflow

After wiki generation, run:

```bash
.venv/bin/python scripts/wheels_prompt.py --topic <TOPIC_ID> --replan
```

Use the printed prompt as the authoritative replan task.

Replan rules:

- Modify only `<TOPIC_DIR>/plan.yaml`.
- Preserve completed phase ids.
- Do not rename or delete completed phase ids.
- Do not modify `<TOPIC_DIR>/topic.yaml`.
- Do not generate lesson prose.
- Do not generate visuals.
- Do not generate code.
- Do not generate `<TOPIC_DIR>/outputs/preview.html`.
- Do not generate `<TOPIC_DIR>/outputs/publish/blog.md`.
- Do not modify `<TOPIC_DIR>/raw/**`.
- Preserve source fidelity notes and useful strategy sections.
- Preserve and reference `<TOPIC_DIR>/wiki/source_assets/**` audit guidance when PDF source assets exist.
- Preserve and reference `<TOPIC_DIR>/wiki/foundation_stack.md` as planning support for background sections, prerequisite ladders, notation strategy, and intuition strategy.

After replan, verify that `<TOPIC_DIR>/plan.yaml` contains section-planning metadata only. It must not contain generated section prose, visual asset contents, code, `<TOPIC_DIR>/outputs/preview.html` content, or `<TOPIC_DIR>/outputs/publish/blog.md` content.

References to `<TOPIC_DIR>/wiki/source_assets/pages/**` or `<TOPIC_DIR>/wiki/source_assets/extracted/**` are allowed in plan metadata as source evidence references. They must not be treated as generated section visuals.

## Required Replan Shape

The revised `<TOPIC_DIR>/plan.yaml` must split future reader-facing work into explicit sections that can be approved by the reader before prose generation.

Require all future section/content phases to include:

- stable `id`
- reader-facing `section_title`
- `reader_question` or `reader_goal`
- source coverage from `<TOPIC_DIR>/wiki/**` and/or `<TOPIC_DIR>/raw/**` source references
- source asset coverage from `<TOPIC_DIR>/wiki/source_assets/**` when PDFs exist
- foundation/background coverage from `<TOPIC_DIR>/wiki/foundation_stack.md`
- prerequisite concepts to introduce first
- concepts this section is allowed to teach
- visuals/code expected for this section, if any
- scoped output paths to update later, written as `<TOPIC_DIR>/outputs/**`
- section-level reviewer report path, written as `<TOPIC_DIR>/reviews/<phase_id>_review.md`
- section-level fix log path, written as `<TOPIC_DIR>/reviews/<phase_id>_fix_log.md`
- explicit instruction to stop and wait for approval before the next section

For `paper_deep_dive`, require either:

- section-by-section paper coverage, or
- an explicitly justified adapted structure that still covers every major paper section deeply.

The replan must not collapse a paper into a high-level overview.

## Reader Approval Gate

End this skill by presenting:

- the proposed skill architecture
- the topic status
- the `<TOPIC_DIR>/wiki/**` files created or already present
- the `<TOPIC_DIR>/wiki/source_assets/**` files created or already present, if PDFs were audited
- whether `<TOPIC_DIR>/wiki/foundation_stack.md` was created or refreshed
- the replanned reader-facing sections from `<TOPIC_DIR>/plan.yaml`
- any source extraction caveats
- any rich PDF visual audit caveats
- a clear statement that section prose has not been generated

Then stop and ask the reader to approve or revise the section plan before any section prose is written.

## Safety Rules

- Never modify files under `<TOPIC_DIR>/raw/**`.
- Never modify `<TOPIC_DIR>/topic.yaml`.
- Never delete existing files under `<TOPIC_DIR>/outputs/**`.
- Never rewrite an existing final article as part of bootstrap.
- Do not continue into section prose generation.
- Stop before generating section prose, visuals, code, `<TOPIC_DIR>/outputs/preview.html`, or `<TOPIC_DIR>/outputs/publish/blog.md`.
- Bootstrap stops after source extraction/source map, compiled wiki, `<TOPIC_DIR>/wiki/foundation_stack.md`, and post-wiki replan; it stops before `<TOPIC_DIR>/sections/**`, section prose, section visuals/code, `<TOPIC_DIR>/outputs/**`, `<TOPIC_DIR>/reviews/**`, and publish artifacts.
- Rendering PDF pages into `<TOPIC_DIR>/wiki/source_assets/pages/**` is allowed source evidence generation when PDF sources exist; do not place those files under `<TOPIC_DIR>/outputs/**`.
- Reviewer behavior belongs to reviewer skills; this skill may inspect `<TOPIC_DIR>/reviews/**` only as prior context.
- If PDF reading is insufficient, ask for extracted text or figures rather than inventing claims.
