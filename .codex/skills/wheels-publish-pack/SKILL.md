---
name: wheels-publish-pack
description: Assemble the final publish package for one Wheels topic after all sections are approved and final audit marks it ready.
---

# wheels-publish-pack

Use this skill after all sections have been individually approved and `wheels-final-audit` has marked the topic ready for publish-pack assembly.

This is a final assembly skill. It must not author new section content. It must not rewrite unapproved sections. It must not run section author, reviewer, fixer, or final-audit behavior.

## Required User Input

This skill requires:

- `TOPIC_ID`

Derived path:

- `TOPIC_DIR` = `topics/<TOPIC_ID>`

All topic-specific paths must be scoped through `TOPIC_DIR`.

Use scoped paths like:

- `<TOPIC_DIR>/topic.yaml`
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
- remove section-local duplication where appropriate
- preserve source fidelity
- preserve toy-to-real bridges
- preserve mechanism-first explanations
- avoid adding new unsupported claims
- avoid introducing new major content not present in approved sections
- include valid Jekyll front matter if `<TOPIC_DIR>/topic.yaml` requests Jekyll output
- use web-safe asset paths according to `<TOPIC_DIR>/topic.yaml`
- not include internal authoring_notes, review notes, fix logs, or section state metadata

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
- source section
- current repo path
- intended publish destination path
- whether the asset needs copying to a blog/static-site location
- any known caveats

### 4. Create Final Source Notes

Create or update `<TOPIC_DIR>/outputs/publish/source_notes.md`.

It should consolidate section source notes:

- source used
- sections supported
- key claims supported
- simplifications or interpretations
- toy-to-real caveats

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
