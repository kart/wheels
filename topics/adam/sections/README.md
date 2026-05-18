# Adam Section Plan

This directory contains planning metadata for the `adam` topic. It is the handoff between the bootstrapped wiki and later section-by-section authoring.

Files here are not lesson prose. They define what each future authoring pass is allowed to teach, which source notes and source assets it must use, what teaching mechanism should carry the section, and what the reviewer should check.

## Files

- `section_plan.yaml`: global section order, dependency ladder, source strategy, media/code strategy, and open verification items.
- `<section_id>/section.yaml`: one section contract for a future author/reviewer/fixer loop.

## How Later Skills Should Use This

For each section, the authoring skill should read:

1. `topics/adam/topic.yaml`
2. `topics/adam/plan.yaml`
3. `topics/adam/sections/section_plan.yaml`
4. the relevant `topics/adam/sections/<section_id>/section.yaml`
5. the source anchors and source assets listed in that section file

The author should update only the scoped output paths for that section, then stop. The reviewer writes only that section's review report. The fixer validates reviewer findings before applying accepted fixes and writing the section fix log.

The user must approve one authored/reviewed/fixed section before the next section begins.
