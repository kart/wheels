# Publish Pack Prompt

The publish pack is the reader-facing final package.

It should be created only after the lesson, visuals, code, preview, reviewer audit, and fixer loop are complete.

## Required outputs

Create or update:

- outputs/publish/blog.md
- outputs/publish/asset_manifest.md
- outputs/publish/source_notes.md
- outputs/publish/twitter_thread.md
- outputs/publish/youtube_script.md
- outputs/publish/README.md

## blog.md requirements

blog.md must be Jekyll-ready.

It must include front matter:

---
layout: default
title: "..."
excerpt: "..."
category: "..."
---

The body should follow the selected article_shape from topic.yaml and templates/article_shapes.md.

For paper_deep_dive posts:
- start with why the paper/topic matters
- explain the problem before the solution
- use tiny examples early
- introduce intuition before math
- place visuals near the relevant explanation
- include code only after explaining the idea
- separate paper claims from interpretation
- include caveats and misconceptions
- end with recap and what comes next

For paper_deep_dive posts, do not turn the article into only a summary.
The final blog must teach the paper deeply, including the mechanism, examples, and section-by-section source coverage.


## Asset rules

Use publish_target.asset_base_path from topic.yaml for image links.

Example:

![CBOW diagram](/assets/images/word2vec/cbow_flow.svg)

asset_manifest.md should list:
- source file in outputs/visuals/
- destination path in karthik.dev
- where it is referenced in blog.md

## Do not

- Do not modify raw/.
- Do not create unsupported claims.
- Do not include internal reviewer/debug notes in blog.md.
- Do not actually publish anything.


## Deep-Dive Publish Requirements

Do not compress the reviewed lesson into a short overview.

For paper_deep_dive posts:
- Preserve the deep-dive structure.
- Include prerequisite intuition before the paper's mechanisms.
- Include section-by-section paper coverage or a justified adapted walkthrough.
- Explain what is being trained, updated, stored, computed, or optimized.
- Include numerical examples after important formulas where useful.
- Include a practical workflow section explaining how the idea would be used in reality.
- Keep visuals near the relevant explanation.
- Avoid duplicate captions.

The final blog.md should feel like a reader-facing teaching article, not a summary of generated artifacts.
