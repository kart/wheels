---
name: wheels-publish-pack
description: Assemble the final publish package for one Wheels topic after all sections are approved and final audit marks it ready.
---

# wheels-publish-pack

Use this skill after all sections have been individually approved and `wheels-final-audit` has marked the topic ready for publish-pack assembly.

This is a final assembly skill. It must not author new section content. It must not rewrite unapproved sections. It must not run section author, reviewer, fixer, or final-audit behavior.

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
- `<TOPIC_DIR>/wiki/foundation_stack.md` if present
- `<TOPIC_DIR>/sections/section_plan.yaml`
- `<TOPIC_DIR>/sections/<section_id>/section.yaml`
- `<TOPIC_DIR>/sections/<section_id>/state.yaml`
- `<TOPIC_DIR>/sections/<section_id>/blog_fragment.md`
- `<TOPIC_DIR>/sections/<section_id>/preview.html`
- `<TOPIC_DIR>/sections/<section_id>/source_notes.md`
- `<TOPIC_DIR>/sections/<section_id>/visuals/**`
- `<TOPIC_DIR>/sections/<section_id>/code/**`
- `<TOPIC_DIR>/sections/<section_id>/manim_media/**`
- `<TOPIC_DIR>/reviews/final_audit.md`
- `<TOPIC_DIR>/reviews/final_audit_state.yaml`
- `<TOPIC_DIR>/outputs/publish/blog.md`
- `<TOPIC_DIR>/outputs/publish/twitter_thread.md`
- `<TOPIC_DIR>/outputs/publish/linkedin_post.md`
- `<TOPIC_DIR>/outputs/publish/youtube_script.md`
- `<TOPIC_DIR>/outputs/publish/asset_manifest.md`
- `<TOPIC_DIR>/outputs/publish/source_notes.md`
- `<TOPIC_DIR>/outputs/publish/README.md`
- `<TOPIC_DIR>/outputs/preview.html`

Do not use naked topic-specific paths like `topic.yaml`, `plan.yaml`, `wiki/**`, `sections/**`, `outputs/**`, `reviews/**`, or `.wheels_state.json` unless the text explicitly says "inside TOPIC_DIR".

If `TOPIC_ID` is missing or ambiguous, stop and ask for it. Never mix files from multiple topics. Never assemble more than one topic in one skill run.

## Preflight Validation

Before assembling the publish pack, verify these exist:

- `<TOPIC_DIR>/topic.yaml`
- `<TOPIC_DIR>/sections/section_plan.yaml`
- `<TOPIC_DIR>/reviews/final_audit.md`
- `<TOPIC_DIR>/reviews/final_audit_state.yaml`

Read `<TOPIC_DIR>/reviews/final_audit_state.yaml`.

If `<TOPIC_DIR>/reviews/final_audit_state.yaml` contains `topic_id`, verify it matches `TOPIC_ID`. If it does not match `TOPIC_ID`, stop. Do not create or modify publish files.

If `ready_for_publish_pack` is not `true`:

- stop
- explain that final audit has not cleared the topic for publish-pack assembly
- do not create or modify publish files

Read `<TOPIC_DIR>/sections/section_plan.yaml` to determine section order.

Validate that section IDs in the section order are unique. If duplicate section IDs exist, stop, report the duplicates, and do not create or modify publish files.

For every section in the section plan, verify:

- `<TOPIC_DIR>/sections/<section_id>/section.yaml` exists
- `<TOPIC_DIR>/sections/<section_id>/state.yaml` exists
- `<TOPIC_DIR>/sections/<section_id>/blog_fragment.md` exists
- `<TOPIC_DIR>/sections/<section_id>/preview.html` exists
- `<TOPIC_DIR>/sections/<section_id>/source_notes.md` exists
- `<TOPIC_DIR>/sections/<section_id>/state.yaml` has `approved_by_user: true`

If any section preview is missing:

- stop
- explain which section preview is missing
- do not create or modify publish files

If any section is missing required files or is not approved:

- stop
- explain what is missing or unapproved
- do not create or modify publish files

## Allowed Writes

- `<TOPIC_DIR>/outputs/preview.html`
- `<TOPIC_DIR>/outputs/publish/blog.md`
- `<TOPIC_DIR>/outputs/publish/twitter_thread.md`
- `<TOPIC_DIR>/outputs/publish/linkedin_post.md`
- `<TOPIC_DIR>/outputs/publish/youtube_script.md`
- `<TOPIC_DIR>/outputs/publish/asset_manifest.md`
- `<TOPIC_DIR>/outputs/publish/source_notes.md`
- `<TOPIC_DIR>/outputs/publish/README.md`

May create:

- `<TOPIC_DIR>/outputs/`
- `<TOPIC_DIR>/outputs/publish/`

only if needed to write the allowed publish files.

## Forbidden Writes

- Do not modify `<TOPIC_DIR>/raw/**`.
- Do not modify `<TOPIC_DIR>/wiki/**`.
- Do not modify `<TOPIC_DIR>/plan.yaml`.
- Do not modify `<TOPIC_DIR>/.wheels_state.json`.
- Do not modify `<TOPIC_DIR>/sections/**`.
- Do not modify `<TOPIC_DIR>/reviews/**`.
- Do not modify section drafts, blog fragments, previews, code, media, source notes, review files, fix logs, state files, or section.yaml files.
- Do not modify `topics/word2vec/outputs/**` or `topics/word2vec/reviews/**` unless explicitly asked.
- Do not copy files to any external blog repo, static-site repo, Jekyll repo, GitHub Pages repo, or publishing destination.
- Do not modify any external blog/static-site repository.
- Do not commit changes to any external repository.
- Do not publish externally.
- Do not run deployment commands.
- Do not push to GitHub or any remote.
- If publishing requires copying assets outside `<TOPIC_DIR>`, record copy instructions only in `<TOPIC_DIR>/outputs/publish/README.md`.
- Do not modify any files outside the Allowed Writes list.
- Allowed writes are exhaustive; no other files may be created or modified.

## Existing Publish-Pack Safety

- If any allowed publish file already exists, inspect it first.
- Update intentionally.
- Do not delete prior publish-pack history unless explicitly asked.
- If overwriting a publish artifact, preserve useful metadata or note the overwrite in `<TOPIC_DIR>/outputs/publish/README.md`.

## Publish Behavior

### 1. Assemble Final Blog

Create or update `<TOPIC_DIR>/outputs/publish/blog.md`.

Use approved `<TOPIC_DIR>/sections/<section_id>/blog_fragment.md` files in section-plan order.

The final blog should:

- be coherent as a single article or long-form lesson
- preserve section order
- preserve approved foundation/background sections and prerequisite explanations that were authored section-by-section
- remove section-local duplication where appropriate
- preserve source fidelity
- preserve toy-to-real bridges
- preserve mechanism-first explanations
- avoid adding new unsupported claims
- avoid introducing new major content not present in approved sections
- include a short "Prerequisites / Background" section only if approved section content contains one
- include valid Jekyll front matter if `<TOPIC_DIR>/topic.yaml` requests Jekyll output
- use web-safe asset paths according to `<TOPIC_DIR>/topic.yaml`
- not include internal authoring_notes, review notes, fix logs, or section state metadata
- not publish `<TOPIC_DIR>/wiki/foundation_stack.md` directly as an internal artifact unless explicitly requested
- not include internal foundation planning notes or section state metadata

For `article_shape: system_design_deep_dive`, preserve approved system design teaching artifacts and caveats:

- architecture diagrams
- API examples
- schema/data model examples
- workflow diagrams
- design-decision tables
- capacity assumptions
- failure-mode tables
- L6+ callouts
- source/caveat notes distinguishing public facts from inferred design choices

For `article_shape: system_design_deep_dive`, preserve approved background around system-design primitives, but do not include internal planning scaffolding.

For `article_shape: paper_deep_dive`, preserve approved math, notation, and concept background, but do not publish raw wiki notes.

Do not publish external repos or deployment artifacts.

### 2. Create Final Preview

Create or update `<TOPIC_DIR>/outputs/preview.html`.

The final preview should:

- be reader-facing
- render the assembled blog content
- include visuals/code/captions in context
- avoid internal planning/debug artifacts
- use paths that work locally where possible
- surface obvious broken image/code references if they cannot be resolved

### 3. Create Asset Manifest

Create or update `<TOPIC_DIR>/outputs/publish/asset_manifest.md`.

It should list:

- every visual/media/code asset referenced by the final blog
- internal planning sources when useful, including `<TOPIC_DIR>/wiki/foundation_stack.md` as an internal source not published directly
- source section
- current repo path
- intended publish destination path
- whether the asset needs copying to a blog/static-site location
- any known caveats
- for each visual: `section_id`, `visual_id`, rendered asset path, source code path if present, spec path if present, whether the visual is conceptual or source-derived, source assets used if any, and whether rendered review passed

When assembling publish artifacts:

- include rendered visual outputs, not visual source code, in the final article by default
- preserve visual captions
- preserve conceptual/source-derived caveats
- ensure `asset_manifest.md` records visual source files and rendered outputs
- ensure `README.md` notes any non-published visual source files
- do not publish Python visual source code unless explicitly requested
- do not copy assets to external repos
- do not run deployment

### 4. Create Final Source Notes

Create or update `<TOPIC_DIR>/outputs/publish/source_notes.md`.

It should consolidate section source notes:

- source used
- sections supported
- key claims supported
- simplifications or interpretations
- toy-to-real caveats
- for system design topics, public facts vs inferred design choices and any approved caveats about plausible architecture decisions

### 5. Create Social Variants

Create or update:

- `<TOPIC_DIR>/outputs/publish/twitter_thread.md`
- `<TOPIC_DIR>/outputs/publish/linkedin_post.md`
- `<TOPIC_DIR>/outputs/publish/youtube_script.md`

Rules:

- Social variants must be derived only from approved section fragments and the assembled final blog.
- Social variants must be derived from approved section content.
- Do not add unsupported claims.
- Do not introduce new examples, claims, conclusions, comparisons, anecdotes, or recommendations that are not present in approved section fragments or the final blog.
- If a social post needs an idea not present in the approved material, note it as a suggested future addition instead of adding it.
- Twitter/X thread should be concise and sequential.
- LinkedIn post should be professional and reflective.
- YouTube script should be optional in spirit but still created if the skill asks for it; it can say when the topic may not yet need a video.
- Each social artifact should point back to the core article idea.

### 6. Create Publish README

Create or update `<TOPIC_DIR>/outputs/publish/README.md`.

It should explain:

- what files are in the publish pack
- what the user should inspect before publishing
- where assets should be copied
- that `<TOPIC_DIR>/wiki/foundation_stack.md`, if present, was an internal planning/source-grounding artifact rather than a publish artifact
- any known caveats from final audit
- suggested publishing order

## Skill Separation

- Do not run section-author behavior inside this skill.
- Do not run section-reviewer behavior inside this skill.
- Do not run section-fixer behavior inside this skill.
- Do not run final-audit behavior inside this skill.
- If assembly reveals a major issue, report it and stop or note it in `<TOPIC_DIR>/outputs/publish/README.md`; do not fix section-local source content.

## State

Do not modify section states. Do not approve sections. Do not modify `<TOPIC_DIR>/reviews/final_audit_state.yaml`. Only the user decides when to publish.

## Stop Condition

After creating or updating the allowed publish files, stop.

Tell the user:

- publish pack files created or updated
- whether final preview was created
- what to inspect before publishing
- any blocking issues discovered during assembly

## Quality Bar

- Final blog should feel like a coherent human-readable article, not stitched fragments.
- Preserve the approved learning sequence.
- Preserve source fidelity.
- Preserve mechanism-first teaching.
- Preserve toy-to-real bridges.
- Avoid shallow summaries.
- Avoid unsupported claims.
- Keep the final output understandable to an undergraduate-level technical reader while still useful to an experienced CS learner.

## Creativity Policy

You may creatively adapt approved content for final blog, preview, Twitter/X, LinkedIn, and YouTube formats.

You may creatively improve:

- transitions between approved sections
- headings and subheadings
- article framing
- social post hooks
- thread sequencing
- LinkedIn tone
- YouTube narration structure
- reader-facing polish

You must not introduce new examples, claims, conclusions, comparisons, anecdotes, recommendations, benchmarks, or source interpretations that are not already present in approved section fragments or the assembled final blog.

Format creatively; do not invent substantively.

If a stronger idea, example, or claim would improve the publish pack but is not present in the approved material:

- do not add it directly
- record it as a suggested future addition in `<TOPIC_DIR>/outputs/publish/README.md`

Preserve all existing guardrails:

- assemble one topic only
- require final audit readiness
- require all sections `approved_by_user: true`
- do not modify `<TOPIC_DIR>/sections/**`
- do not modify `<TOPIC_DIR>/reviews/**`
- do not modify `<TOPIC_DIR>/raw/**`
- do not modify `<TOPIC_DIR>/wiki/**`
- do not modify `<TOPIC_DIR>/plan.yaml`
- do not modify `<TOPIC_DIR>/.wheels_state.json`
- do not publish externally
- do not copy files to external blog/static-site repos
- do not run deployment commands
