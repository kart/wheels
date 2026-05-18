# Section Planning

This directory contains planning metadata for `topics/system_design_youtube`.

These files are contracts for later section authoring. They are not article prose, code, diagrams, rendered media, previews, reviews, or publish artifacts.

## Files

- `section_plan.yaml` gives the full section order, source strategy, prerequisite ramp, media strategy, and approval policy.
- `<section_id>/section.yaml` gives the source anchors, learning goal, dependencies, visual/code plan, system-design decisions, review checks, and user approval gate for one section.

## Workflow

Later skills should consume exactly one `<section_id>/section.yaml` at a time. The authoring skill should draft only that section, update the relevant output files, run the section review/fix loop, and stop.

The user must approve the completed section before the next section begins.
