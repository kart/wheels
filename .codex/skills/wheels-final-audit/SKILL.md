---
name: wheels-final-audit
description: Perform an audit-only full-topic review after all planned Wheels sections are authored, reviewed, fixed, and explicitly approved.
---

# wheels-final-audit

Use this skill after all planned sections have been individually authored, reviewed, fixed, and explicitly approved by the user.

This is an audit-only skill. It must not edit section content. It must not apply fixes. It must not generate the publish pack. It must not assemble the final blog or final preview.

## Tooling Policy

For Python instructions, examples, or validation commands, prefer `.venv/bin/python`. Do not use system Python. Do not install packages from inside the skill unless the user explicitly asks. If dependencies are missing, note that the user may install them with commands such as `.venv/bin/python -m pip install matplotlib numpy pillow cairosvg playwright pymupdf` and `.venv/bin/python -m playwright install chromium`.

## Required User Input

This skill requires:

- `TOPIC_ID`

Derived path:

- `TOPIC_DIR` = `topics/<TOPIC_ID>`

All topic-specific paths must be scoped through `TOPIC_DIR`.

Use scoped paths like:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/plan.yaml`
- `<TOPIC_DIR>/wiki/**`
- `<TOPIC_DIR>/wiki/source_assets/**`
- `<TOPIC_DIR>/sections/section_plan.yaml`
- `<TOPIC_DIR>/sections/<section_id>/section.yaml`
- `<TOPIC_DIR>/sections/<section_id>/state.yaml`
- `<TOPIC_DIR>/sections/<section_id>/draft.md`
- `<TOPIC_DIR>/sections/<section_id>/blog_fragment.md`
- `<TOPIC_DIR>/sections/<section_id>/preview.html`
- `<TOPIC_DIR>/sections/<section_id>/source_notes.md`
- `<TOPIC_DIR>/sections/<section_id>/review.md`
- `<TOPIC_DIR>/sections/<section_id>/fix_log.md`
- `<TOPIC_DIR>/reviews/final_audit.md`
- `<TOPIC_DIR>/reviews/final_audit_state.yaml`

Do not use naked topic-specific paths like `topic.yaml`, `plan.yaml`, `wiki/**`, `outputs/**`, `reviews/**`, `sections/**`, or `.wheels_state.json` unless the text explicitly says "inside TOPIC_DIR".

If `TOPIC_ID` is missing or ambiguous, stop and ask for it. Never mix files from multiple topics. Never audit more than one topic in one skill run.

## Preflight Validation

Before auditing, verify these exist:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/wiki/**`
- `<TOPIC_DIR>/sections/section_plan.yaml`

Then inspect `<TOPIC_DIR>/sections/section_plan.yaml` to identify expected sections.

For every expected section, verify:

- `<TOPIC_DIR>/sections/<section_id>/section.yaml` exists
- `<TOPIC_DIR>/sections/<section_id>/state.yaml` exists
- `<TOPIC_DIR>/sections/<section_id>/draft.md` exists
- `<TOPIC_DIR>/sections/<section_id>/blog_fragment.md` exists
- `<TOPIC_DIR>/sections/<section_id>/preview.html` exists
- `<TOPIC_DIR>/sections/<section_id>/source_notes.md` exists
- `<TOPIC_DIR>/sections/<section_id>/review.md` exists
- whether `<TOPIC_DIR>/sections/<section_id>/fix_log.md` exists
- `<TOPIC_DIR>/sections/<section_id>/state.yaml` has `approved_by_user: true`

`<TOPIC_DIR>/sections/<section_id>/fix_log.md` is conditional:

- If the section passed review without fixes, missing `<TOPIC_DIR>/sections/<section_id>/fix_log.md` may be acceptable.
- If `<TOPIC_DIR>/sections/<section_id>/state.yaml` indicates `fixed: true`, `needs_fix` was previously true, or `<TOPIC_DIR>/sections/<section_id>/review.md` contained blocking issues, then missing `<TOPIC_DIR>/sections/<section_id>/fix_log.md` should be reported as a gap.
- The final audit should report the fix-log status in the Section Completeness Matrix.

If any required section artifact is missing:

- continue the audit only far enough to report missing artifacts
- mark the final audit verdict as `blocked`
- do not create publish artifacts
- do not modify section files

If any section is not `approved_by_user: true`:

- mark the final audit verdict as `blocked`
- identify the unapproved section
- do not proceed to publish-pack readiness

## Allowed Writes

- `<TOPIC_DIR>/reviews/final_audit.md`
- `<TOPIC_DIR>/reviews/final_audit_state.yaml`
- May create `<TOPIC_DIR>/reviews/` only if needed to write:
  - `<TOPIC_DIR>/reviews/final_audit.md`
  - `<TOPIC_DIR>/reviews/final_audit_state.yaml`

Do not create any other files under `<TOPIC_DIR>/reviews/**`.

## Forbidden Writes

- Do not modify `<TOPIC_DIR>/raw/**`.
- Do not modify `<TOPIC_DIR>/outputs/**`.
- Do not modify `<TOPIC_DIR>/wiki/**`.
- Do not modify `<TOPIC_DIR>/wiki/source_assets/**`.
- Do not modify `<TOPIC_DIR>/plan.yaml`.
- Do not modify `<TOPIC_DIR>/.wheels_state.json`.
- Do not modify `<TOPIC_DIR>/sections/**`.
- Do not modify any section draft, blog fragment, preview, code, media, source notes, review, fix log, or state file.
- Do not assemble final `<TOPIC_DIR>/outputs/publish/blog.md`.
- Do not assemble final `<TOPIC_DIR>/outputs/preview.html`.
- Do not create social posts.
- Do not create publish-pack files.
- Do not modify `topics/word2vec/outputs/**`.
- Do not modify `topics/word2vec/reviews/**` unless explicitly asked.
- Do not modify any files outside the Allowed Writes list.
- Allowed writes are exhaustive; no other files may be created or modified.

## Existing Audit Safety

- If `<TOPIC_DIR>/reviews/final_audit.md` or `<TOPIC_DIR>/reviews/final_audit_state.yaml` already exists, inspect it first.
- Update intentionally.
- Do not delete prior audit history unless explicitly asked.

## Audit Behavior

Review the full topic across all approved sections.

If `<TOPIC_DIR>/wiki/source_assets/**` exists, inspect:

- `<TOPIC_DIR>/wiki/source_assets/index.yaml`
- `<TOPIC_DIR>/wiki/source_assets/formulas.md`
- `<TOPIC_DIR>/wiki/source_assets/figures.md`
- `<TOPIC_DIR>/wiki/source_assets/tables.md`
- `<TOPIC_DIR>/wiki/source_assets/visual_audit.md`

Treat all source asset files as read-only. Use them to audit whether source evidence was mapped, used, reviewed, fixed, deferred, or documented appropriately across sections.

## Audit Checks

### Section Approval And Completeness

- Are all sections from `<TOPIC_DIR>/sections/section_plan.yaml` present?
- Are all required section artifacts present?
- Are all sections `approved_by_user: true`?
- Are dependencies between sections satisfied?

### Narrative Flow

- Does the topic read in a coherent learning order?
- Does each section naturally lead to the next?
- Are transitions missing or abrupt?
- Are there unnecessary jumps in difficulty?

### Prerequisite Ladder

- Are prerequisite concepts introduced before they are used?
- Are terms consistent across sections?
- Are any important foundations missing?
- Are there sections that assume knowledge not yet taught?

### Source Fidelity And Coverage

- Are major source claims covered?
- Are important paper/system/source sections omitted?
- Are claims grounded in `<TOPIC_DIR>/wiki/**` and section source notes?
- Are interpretations clearly separated from source-backed claims?
- Are limitations and caveats represented honestly?

### Source Asset And Visual Evidence Handling

- Do section.yaml files reference relevant source assets where appropriate?
- Were important formula assets covered by some section?
- Were important figure/table/chart assets either used, explicitly skipped, or noted as not relevant?
- Are `visual_verification_required` items resolved, deferred, or clearly documented?
- Did any section quote exact chart/table values that were not marked reliable or visually verified?
- Did any section transform paper figures/tables into simplified teaching visuals, and if so, was the transformation reviewed?
- Are source-asset caveats carried through `<SECTION_DIR>/review.md`, `<SECTION_DIR>/fix_log.md`, `<SECTION_DIR>/source_notes.md`, or section prose?
- Are any rich PDF visual audit caveats still blocking publish readiness?

### Redundancy And Contradiction

- Are explanations duplicated across sections?
- Do sections contradict each other?
- Are definitions inconsistent?
- Are examples reused in a confusing way?

### Mechanism Quality

- Does every major concept have an appropriate concrete teaching mechanism?
- Are mechanisms consistent with the section plan?
- Are code, worked examples, diagrams, traces, simulations, or tables used where useful?
- Are any sections too abstract or too prose-only?

### Toy-To-Real Bridge

- Does each relevant section explain what the toy/scaled-down demo demonstrates?
- Does each relevant section explain what the toy version omits?
- Does the full topic bridge cleanly from learning artifact to real-world usage?

### Code And Media Consistency

- Are section-local code paths consistent?
- Are image/media paths likely to work during publish-pack assembly?
- Are captions consistent?
- Are visuals non-duplicative and useful?
- Are there known occlusion, readability, ambiguity, or correctness issues?
- Are important technical visuals backed by specs and source code when feasible?
- Are rendered SVG/PNG files present for code-generated visuals?
- Were central visuals reviewed after rendering?
- Do any approved sections still have incomplete rendered visual review?
- Are visual source files section-local?
- Are captions clear about conceptual vs source-derived visuals?
- Are simplified redraws faithful to source assets?
- Are there unresolved clipping/overflow/occlusion issues?
- Are there broken image paths in section previews?
- Are generated visuals suitable for publish-pack assembly?

### Preview And Publish Readiness

- Do section previews appear reader-facing?
- Are there broken markdown, math, HTML, code block, image, or asset path issues?
- Are blog fragments likely to assemble cleanly?
- Are there front matter concerns that should be handled by publish-pack?
- If a visual verification item is blocking and unresolved, the verdict must be `blocked` or `needs_cross_section_fixes` and `ready_for_publish_pack` must be `false`.
- If visual verification items are non-blocking caveats, list them in `<TOPIC_DIR>/reviews/final_audit.md`; publish-pack may proceed only if the caveats do not affect correctness of the final article.
- If a central visual has not passed rendered review, the final audit should block publish readiness and set `ready_for_publish_pack: false`.
- If an important technical visual lacks a spec/source code without a documented reason, report it as a consistency gap. Treat it as blocking when it affects reviewability or correctness.

### Audience Fit

- Is the combined topic understandable to an undergraduate-level technical reader?
- Does it remain useful to an experienced CS learner building AI/system foundations?
- Is the content deep enough, or does it collapse into summary?

## Output

Create or update `<TOPIC_DIR>/reviews/final_audit.md` with this structure:

```markdown
# Final Audit: <TOPIC_ID>

## Summary Verdict
One of:
- publish_ready
- publish_ready_with_minor_notes
- needs_cross_section_fixes
- blocked

## Blocking Issues
List issues that must be resolved before publish-pack assembly.

## Cross-Section Improvements
List recommended improvements that affect multiple sections.

## Section Completeness Matrix
For each section:
- section_id
- approved_by_user status
- required artifacts present/missing
- fix_log status
- notes

## Narrative Flow Notes
Assess ordering, transitions, and difficulty progression.

## Prerequisite / Terminology Notes
Assess definitions, prerequisite ladder, and consistency.

## Source Fidelity / Coverage Notes
Assess source grounding and major coverage gaps.

## Source Asset / Visual Evidence Notes
Include:
- important formulas/figures/tables/pages audited
- source assets covered by sections
- source assets missing section coverage
- unresolved visual verification items
- manual spot-checks still needed
- whether publish-pack may proceed safely

## Mechanism / Code / Media Notes
Assess teaching mechanisms, toy demos, visuals, code, and toy-to-real bridges.

## Publish-Pack Readiness Notes
List what the publish-pack skill should watch for.

## Recommended Next Action
One of:
- proceed_to_publish_pack
- run_section_fixer_for_specific_sections
- revise_section_plan
- block_until_missing_artifacts_are_created
```

## State Update

Create or update `<TOPIC_DIR>/reviews/final_audit_state.yaml` with:

```yaml
topic_id:
audited: true
verdict:
ready_for_publish_pack: true | false
blocking_sections:
last_audit: <short timestamp or simple marker>
```

Do not modify section states. Do not set any section `approved_by_user`. Do not create publish artifacts.

## Stop Condition

After writing `<TOPIC_DIR>/reviews/final_audit.md` and `<TOPIC_DIR>/reviews/final_audit_state.yaml`, stop.

Tell the user:

- final audit file created
- summary verdict
- whether the next step is publish-pack or section-level fixes

Do not run section reviewer behavior inside this skill. Do not run section fixer behavior inside this skill. Do not run publish-pack behavior inside this skill. This skill may only audit and write the two allowed final audit files. Do not apply fixes. Do not modify sections.

## Quality Bar

- Audit should be strict but actionable.
- Prefer specific file/section references.
- Separate blocking issues from polish.
- Protect source fidelity.
- Protect section-by-section learning quality.
- Protect toy-to-real bridge quality.
- Protect final publish readiness.
