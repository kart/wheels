# wheels-topic-bootstrap

Use this skill when starting or restarting the first half of a Wheels topic: topic setup, startup planning, source-grounded wiki compilation, and post-wiki replanning. Stop before drafting section prose.

This skill wraps the existing `scripts/wheels_prompt.py` workflow. Do not edit `scripts/wheels_prompt.py` unless a small compatibility bug blocks the workflow.

## Scope

This skill owns:

- inspecting an existing `topics/<topic>/topic.yaml`
- helping create `topics/<topic>/topic.yaml` when it is missing
- generating `topics/<topic>/plan.yaml` through the startup prompt
- running wiki/source phases from `plan.yaml`
- marking completed wiki phases in `.wheels_state.json`
- invoking post-wiki replanning
- requiring the revised plan to split future prose work into reader-approved sections

This skill does not own:

- writing final lesson prose
- generating section prose
- generating visuals
- generating code
- generating `outputs/preview.html`
- generating final publish drafts
- generating `outputs/publish/blog.md`
- editing files under `raw/`
- deleting existing outputs

## Proposed Wheels Skill Architecture

Create the Wheels workflow as separate Codex skills so each phase has a clear stopping point:

1. `wheels-topic-bootstrap/SKILL.md`
   - Setup through compiled wiki and post-wiki replan.
   - Stops with a sectioned plan awaiting reader approval.

2. `wheels-section-planner/SKILL.md`
   - Converts the replanned `plan.yaml` into explicit reader-approved section contracts.
   - Owns section boundaries, prerequisites, source coverage, visual intent, and acceptance criteria.

3. `wheels-section-author/SKILL.md`
   - Generates exactly one approved section at a time.
   - Updates `outputs/lesson.md`, `outputs/visual_plan.md`, relevant assets/code, and `outputs/preview.html`.
   - Stops after that section.

4. `wheels-section-reviewer/SKILL.md`
   - Performs a section-level reviewer pass.
   - Writes only `reviews/<phase_id>_review.md`.
   - Does not edit lesson, wiki, output, visual, code, or raw files.

5. `wheels-section-fixer/SKILL.md`
   - Validates section reviewer findings.
   - Applies accepted fixes only.
   - Writes `reviews/<phase_id>_fix_log.md`.

6. `wheels-final-audit/SKILL.md`
   - Runs whole-article review after all sections are drafted and fixed.
   - Checks source fidelity, teaching depth, visual correctness, code correctness, and preview quality.

7. `wheels-publish-pack/SKILL.md`
   - Creates the final copy-pasteable publish pack only after review/fix completion.
   - Owns `outputs/publish/` and Jekyll front matter requirements.

Only this first skill is implemented now.

## Required Inputs

Ask for or infer:

- `topic_id`, matching `topics/<topic_id>/`
- whether the topic folder already exists
- raw source availability under `topics/<topic_id>/raw/`

Before editing anything, inspect:

- `README.md`
- `AGENTS.md`
- `scripts/wheels_prompt.py`
- `templates/article_shapes.md`
- `prompts/audience_profiles.md` if present
- `topics/<topic_id>/topic.yaml` if present
- `topics/<topic_id>/plan.yaml` if present
- `topics/<topic_id>/wiki/` if present

For regression awareness, treat `topics/word2vec` as the v1 demo fixture. Do not rewrite its final article unless explicitly asked.

## Topic YAML Handling

If `topics/<topic_id>/topic.yaml` exists:

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
4. Check that every listed source path is under `topics/<topic_id>/raw/`.
5. Do not modify `raw/`.

If `topics/<topic_id>/topic.yaml` is missing:

1. Create `topics/<topic_id>/topic.yaml` only after gathering the minimum topic metadata from the user or existing files.
2. Use `templates/article_shapes.md` and `prompts/audience_profiles.md` for valid values.
3. Prefer conservative defaults:
   - `audience_profile: beginner_technical`
   - `article_shape: paper_deep_dive` only if the primary source is a paper
4. Include `source_policy.raw_is_human_owned: true` and `source_policy.do_not_overwrite_raw: true`.
5. Do not invent source files.

## Startup Plan Workflow

If `topics/<topic_id>/plan.yaml` is missing or the user explicitly asks to restart planning:

1. Run:

   ```bash
   .venv/bin/python scripts/wheels_prompt.py --topic <topic_id> --startup
   ```

   If `.venv/bin/python` is unavailable, use:

   ```bash
   python scripts/wheels_prompt.py --topic <topic_id> --startup
   ```

2. Use the printed prompt as the authoritative startup task.
3. Create only `topics/<topic_id>/plan.yaml`.
4. Do not generate wiki, lesson, visuals, preview, reviews, or publish files during startup planning.
5. Do not generate section prose, code, `outputs/preview.html`, or `outputs/publish/blog.md`.

After creating or finding `plan.yaml`, run:

```bash
.venv/bin/python scripts/wheels_prompt.py --topic <topic_id> --status
```

Use `python` instead of `.venv/bin/python` only if the venv command is unavailable.

## Wiki Phase Loop

Run only phases needed to compile the wiki. Use the existing phase prompts rather than inventing phase instructions.

Loop:

1. Run:

   ```bash
   .venv/bin/python scripts/wheels_prompt.py --topic <topic_id> --next
   ```

2. Read the emitted phase prompt.
3. If the next phase is a wiki/source/extraction/compiled-wiki phase, execute exactly that phase.
4. Do not run later lesson, prose, visual, preview, review, fix, or publish phases.
5. Do not generate section prose, visuals, code, `outputs/preview.html`, or `outputs/publish/blog.md`.
6. When the phase completion checks are satisfied, run:

   ```bash
   .venv/bin/python scripts/wheels_prompt.py --topic <topic_id> --mark-done
   ```

7. Repeat until the wiki is compiled.

Stop the wiki loop when:

- required wiki files from the plan exist, and
- the next phase is replan, outline, lesson, content, visual, preview, review, fix, or publish.

If the startup plan did not include an explicit replan phase after the wiki, still invoke the replan workflow below.

## Post-Wiki Replan Workflow

After wiki generation, run:

```bash
.venv/bin/python scripts/wheels_prompt.py --topic <topic_id> --replan
```

Use the printed prompt as the authoritative replan task.

Replan rules:

- Modify only `topics/<topic_id>/plan.yaml`.
- Preserve completed phase ids.
- Do not rename or delete completed phase ids.
- Do not generate lesson prose.
- Do not generate visuals.
- Do not generate code.
- Do not generate `outputs/preview.html`.
- Do not generate `outputs/publish/blog.md`.
- Do not modify `raw/`.
- Preserve source fidelity notes and useful strategy sections.

## Required Replan Shape

The revised `plan.yaml` must split future reader-facing work into explicit sections that can be approved by the reader before prose generation.

Require all future section/content phases to include:

- stable `id`
- reader-facing `section_title`
- `reader_question` or `reader_goal`
- source coverage from `wiki/` and/or raw source references
- prerequisite concepts to introduce first
- concepts this section is allowed to teach
- visuals/code expected for this section, if any
- outputs to update
- section-level reviewer report path
- section-level fix log path
- explicit instruction to stop and wait for approval before the next section

For `paper_deep_dive`, require either:

- section-by-section paper coverage, or
- an explicitly justified adapted structure that still covers every major paper section deeply.

The replan must not collapse a paper into a high-level overview.

## Reader Approval Gate

End this skill by presenting:

- the proposed skill architecture
- the topic status
- the wiki files created or already present
- the replanned reader-facing sections from `plan.yaml`
- any source extraction caveats
- a clear statement that section prose has not been generated

Then stop and ask the reader to approve or revise the section plan before any section prose is written.

## Safety Rules

- Never modify files under `raw/`.
- Never delete existing outputs.
- Never rewrite an existing final article as part of bootstrap.
- Do not continue into section prose generation.
- Stop before generating section prose, visuals, code, `outputs/preview.html`, or `outputs/publish/blog.md`.
- Reviewer behavior belongs to reviewer skills; this skill may inspect reviewer reports only as prior context.
- If PDF reading is insufficient, ask for extracted text or figures rather than inventing claims.
