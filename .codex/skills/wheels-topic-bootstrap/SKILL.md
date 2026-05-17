---
name: wheels-topic-bootstrap
description: Bootstrap a Wheels topic from TOPIC_DIR/topic.yaml and raw sources through plan.yaml, wiki compilation, and replan, stopping before section authoring.
---

# wheels-topic-bootstrap

Use this skill when starting or restarting the first half of a Wheels topic: topic setup, startup planning, source-grounded wiki compilation, and post-wiki replanning. Stop before drafting section prose.

This skill wraps the existing `scripts/wheels_prompt.py` workflow. Do not edit `scripts/wheels_prompt.py` unless a small compatibility bug blocks the workflow.

## Scope

This skill owns:

- inspecting an existing `<TOPIC_DIR>/topic.yaml`
- helping create `<TOPIC_DIR>/topic.yaml` when it is missing
- generating `<TOPIC_DIR>/plan.yaml` through the startup prompt
- running wiki/source phases from `<TOPIC_DIR>/plan.yaml`
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
- `<TOPIC_DIR>/topic.yaml` if present
- `<TOPIC_DIR>/plan.yaml` if present
- `<TOPIC_DIR>/wiki/**` if present

For regression awareness, if `TOPIC_ID` is `word2vec`, treat `<TOPIC_DIR>` as the v1 demo fixture. Do not rewrite its final article unless explicitly asked. Do not modify `<TOPIC_DIR>/outputs/**` or `<TOPIC_DIR>/reviews/**` unless explicitly asked.

## Bootstrap Write Scope

Bootstrap may update only:

- `<TOPIC_DIR>/topic.yaml`, if creating or strengthening topic intent
- `<TOPIC_DIR>/plan.yaml`
- `<TOPIC_DIR>/wiki/**`
- `<TOPIC_DIR>/wiki_preview/**`
- `<TOPIC_DIR>/.wheels_state.json` as needed

Bootstrap must not update:

- `<TOPIC_DIR>/raw/**`
- `<TOPIC_DIR>/sections/**`
- `<TOPIC_DIR>/outputs/**`
- `<TOPIC_DIR>/reviews/**`
- `<TOPIC_DIR>/outputs/preview.html`
- `<TOPIC_DIR>/outputs/publish/blog.md`

## Topic YAML Handling

If `<TOPIC_DIR>/topic.yaml` exists:

1. Read it.
2. Check that it includes, or has a clear equivalent for:
   - `id`
   - `title`
   - `goal`
   - `available_sources`
   - `audience_profile`
   - `article_shape`
   - `publish_target`
   - source ownership rules
3. Check that `article_shape` is one of:
   - `paper_deep_dive`
   - `system_design_deep_dive`
   - `algorithm_walkthrough`
4. Check that every listed source path is under `<TOPIC_DIR>/raw/**`.
5. Do not modify `<TOPIC_DIR>/raw/**`.

If `<TOPIC_DIR>/topic.yaml` is missing:

1. Create `<TOPIC_DIR>/topic.yaml` only after gathering the minimum topic metadata from the user or existing files.
2. Use `templates/article_shapes.md` and `prompts/audience_profiles.md` for valid values.
3. Prefer conservative defaults:
   - `audience_profile: beginner_technical`
   - `article_shape: paper_deep_dive` only if the primary source is a paper
4. Include `source_policy.raw_is_human_owned: true` and `source_policy.do_not_overwrite_raw: true`.
5. Do not invent source files.

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
4. Do not generate `<TOPIC_DIR>/wiki/**`, lesson prose, visuals, `<TOPIC_DIR>/outputs/preview.html`, `<TOPIC_DIR>/reviews/**`, or publish files during startup planning.
5. Do not generate section prose, code, `<TOPIC_DIR>/outputs/preview.html`, or `<TOPIC_DIR>/outputs/publish/blog.md`.

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
- Do not generate lesson prose.
- Do not generate visuals.
- Do not generate code.
- Do not generate `<TOPIC_DIR>/outputs/preview.html`.
- Do not generate `<TOPIC_DIR>/outputs/publish/blog.md`.
- Do not modify `<TOPIC_DIR>/raw/**`.
- Preserve source fidelity notes and useful strategy sections.

After replan, verify that `<TOPIC_DIR>/plan.yaml` contains section-planning metadata only. It must not contain generated section prose, visual asset contents, code, `<TOPIC_DIR>/outputs/preview.html` content, or `<TOPIC_DIR>/outputs/publish/blog.md` content.

## Required Replan Shape

The revised `<TOPIC_DIR>/plan.yaml` must split future reader-facing work into explicit sections that can be approved by the reader before prose generation.

Require all future section/content phases to include:

- stable `id`
- reader-facing `section_title`
- `reader_question` or `reader_goal`
- source coverage from `<TOPIC_DIR>/wiki/**` and/or `<TOPIC_DIR>/raw/**` source references
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
- the replanned reader-facing sections from `<TOPIC_DIR>/plan.yaml`
- any source extraction caveats
- a clear statement that section prose has not been generated

Then stop and ask the reader to approve or revise the section plan before any section prose is written.

## Safety Rules

- Never modify files under `<TOPIC_DIR>/raw/**`.
- Never delete existing files under `<TOPIC_DIR>/outputs/**`.
- Never rewrite an existing final article as part of bootstrap.
- Do not continue into section prose generation.
- Stop before generating section prose, visuals, code, `<TOPIC_DIR>/outputs/preview.html`, or `<TOPIC_DIR>/outputs/publish/blog.md`.
- Reviewer behavior belongs to reviewer skills; this skill may inspect `<TOPIC_DIR>/reviews/**` only as prior context.
- If PDF reading is insufficient, ask for extracted text or figures rather than inventing claims.
