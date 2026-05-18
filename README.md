# Wheels

Wheels turns raw learning resources into structured understanding and publishable explanations.

The workflow is:

```text
raw sources -> plan -> compiled wiki -> lesson + visuals + code -> HTML preview -> review -> fixes -> publish pack
```

The project is designed for deep technical teaching, not shallow summaries. A Wheels topic should help a smart beginner understand an idea from first principles while staying grounded in the provided source material.

## Repository Layout

```text
.
├── AGENTS.md                  # Global quality rules and workflow contracts
├── prompts/                   # Reusable phase/review/publish guidance
├── scripts/                   # Local helper scripts
├── templates/                 # Article shape definitions
└── topics/
    └── <topic>/
        ├── topic.yaml         # Topic config, audience, article shape, publish target
        ├── plan.yaml          # Topic execution plan
        ├── raw/               # Human-provided sources. Do not overwrite.
        ├── wiki/              # Compiled source-grounded understanding
        ├── wiki_preview/      # Local browsable wiki preview
        ├── outputs/           # Lesson, visuals, code, preview, publish pack
        └── reviews/           # Reviewer reports and fix logs
```

## Core Contracts

The current project rules live in [AGENTS.md](AGENTS.md). The most important ones:

- `raw/` is human-owned source material. Do not modify it.
- Stay grounded in provided sources.
- Build intuition before equations.
- Use examples before abstraction.
- Explain code before showing code.
- Do not say something “learns”, “trains”, “scales”, or “optimizes” without explaining what changes and why.
- Every important formula needs symbol definitions, plain-English meaning, and a small numerical example when useful.
- Visuals are teaching artifacts, not decoration.
- `outputs/preview.html` should read like the final blog, not an internal dashboard.
- `outputs/publish/blog.md` should be copy-pasteable into `karthik.dev/_posts/`.

## Topic Configuration

Every topic starts with `topics/<topic>/topic.yaml`.

Important fields:

- `id`: stable topic id, matching the folder name.
- `title`: reader-facing title.
- `available_sources`: raw source files to use.
- `audience_profile`: selected profile from [prompts/audience_profiles.md](prompts/audience_profiles.md).
- `article_shape`: selected shape from [templates/article_shapes.md](templates/article_shapes.md).
- `publish_target`: final blog format, category, asset path, and filename prefix.
- `must_explain`: topic-specific concepts that the final article must teach.
- `publish_repair_focus`: known repair priorities for final publish output.

Example topic:

```text
topics/word2vec/
```

## Article Shapes

Article shapes define the reader journey for final lessons and blog posts.

Current shapes are defined in [templates/article_shapes.md](templates/article_shapes.md):

- `paper_deep_dive`
- `system_design_deep_dive`
- `algorithm_walkthrough`

For a `paper_deep_dive`, the final blog must be a real paper walkthrough. It should cover prior work, bottlenecks, mechanisms, experiments, limitations, misconceptions, and practical workflow. It should not collapse the paper into a short overview.

## Audience Profiles

Audience profiles are defined in [prompts/audience_profiles.md](prompts/audience_profiles.md).

Supported profiles:

- `beginner_technical`
- `system_design_interview_l5_plus`

The current default profile used by Word2Vec is `beginner_technical`:

- undergraduate-level technical maturity
- math may be weak
- coding skill may be novice
- examples, visuals, and gradual buildup are essential

Use `system_design_interview_l5_plus` for system design interview content where the main path should be useful to a strong L5 candidate and clearly marked L6+ callouts should deepen the answer only where they add meaningful design depth.

## Workflow

### 1. Add Raw Sources

Create a topic folder:

```text
topics/<topic>/
```

Add:

```text
topics/<topic>/topic.yaml
topics/<topic>/raw/
```

Do not overwrite or edit files under `raw/` during generation phases.

### 2. Create `plan.yaml`

Generate a topic execution plan from `topic.yaml` and `raw/`.

The plan should decide:

- wiki structure
- lesson structure
- concepts needing intuition
- concepts needing examples
- visuals
- code demos
- preview strategy
- review strategy
- fix strategy
- execution phases

The normalized plan should include machine-readable `execution_phases`.

### 3. Build the Source Map and Wiki

The wiki is the internal compiled understanding layer. It should separate source claims from teaching interpretation.

Typical files:

```text
wiki/source_summary.md
wiki/concepts.md
wiki/architecture_notes.md
wiki/results_notes.md
```

Use the wiki to preserve fidelity before writing the reader-facing lesson.

### 4. Build a Wiki Preview

Use the helper script:

```bash
python scripts/build_wiki_preview.py --topic word2vec
```

Output:

```text
topics/word2vec/wiki_preview/index.html
```

If the `markdown` Python package is missing:

```bash
pip install markdown
```

### 5. Draft Lesson, Visuals, and Code

Typical outputs:

```text
outputs/lesson.md
outputs/visual_plan.md
outputs/visuals/*.svg
outputs/code/*.py
```

Rules:

- Keep lesson structure modular.
- Place visuals near the explanations they support.
- Keep visuals simple but correct.
- Use code only where it improves understanding.
- Toy code must be clearly labeled as educational and not a reproduction of paper-scale results.

### 6. Build Reader-Facing Preview

Output:

```text
outputs/preview.html
```

This should read like the final blog draft. It should not expose internal planning notes, reviewer notes, or artifact checklists except in a collapsed build-notes section if needed.

### 7. Reviewer Audit

The reviewer writes only:

```text
reviews/reviewer_report.md
```

The reviewer must not edit lesson, wiki, output, visual, code, or raw files.

Review priorities are defined in [prompts/reviewer.md](prompts/reviewer.md):

- source fidelity
- technical correctness
- visual correctness
- code correctness
- explanation quality
- rendered preview quality
- deep-dive completeness

### 8. Fixer Loop

The fixer validates reviewer findings before applying changes.

Output:

```text
reviews/fix_log.md
```

Do not blindly apply reviewer feedback. Mark findings accepted, rejected, or modified with rationale.

### 9. Publish Pack

Final publish materials live under:

```text
outputs/publish/
```

Required files:

```text
outputs/publish/blog.md
outputs/publish/twitter_thread.md
outputs/publish/youtube_script.md
outputs/publish/source_notes.md
outputs/publish/asset_manifest.md
outputs/publish/README.md
outputs/publish/assets/
```

For Jekyll publishing, `blog.md` must include front matter:

```yaml
---
layout: default
title: "..."
excerpt: "..."
category: "..."
---
```

Image links in the final blog should use the configured `publish_target.asset_base_path`, for example:

```markdown
<img src="/assets/images/word2vec-cbow-flow.svg" alt="CBOW architecture flow">
```

Use topic-specific filename prefixes, such as `word2vec-`, to avoid collisions.

## Jekyll Handoff

For `karthik.dev`, posts and image assets are copied manually.

Example:

```bash
mkdir -p ~/karthik.dev/_posts
mkdir -p ~/karthik.dev/assets/images

cp topics/word2vec/outputs/publish/blog.md ~/karthik.dev/_posts/2026-05-14-word2vec.md
cp topics/word2vec/outputs/publish/assets/word2vec-* ~/karthik.dev/assets/images/

cd ~/karthik.dev
/Users/kart/.rbenv/shims/bundle exec jekyll serve
```

The `karthik.dev` home page may need a manual `index.md` entry if the landing page is curated rather than generated from `site.posts`.

The site layout also needs Markdown article styles for tables, blockquotes, figures, and code blocks. Wheels’ `preview.html` includes local preview CSS, but that CSS is not automatically transferred into Jekyll.

## Manim Animations

Some topics may include experimental Manim animations:

```text
outputs/manim/
outputs/manim_media/
```

Use the repo virtual environment explicitly:

```bash
.venv/bin/manim -ql --media_dir topics/word2vec/outputs/manim_media \
  topics/word2vec/outputs/manim/word2vec_scenes.py OneHotVsDenseScene
```

Do not use system Python, system pip, or bare `manim` when working in this repo. Prefer:

```bash
.venv/bin/python
.venv/bin/pip
.venv/bin/manim
```

If Manim rendering fails because of system dependencies such as `ffmpeg`, Cairo, or Pango, document the issue instead of retrying repeatedly.

## Helper Scripts

### `scripts/build_wiki_preview.py`

Builds a browsable local HTML wiki from all Markdown files under a topic’s `wiki/` folder.

```bash
python scripts/build_wiki_preview.py --topic word2vec
```

### `scripts/wheels_prompt.py`

Generates phase prompts for topic workflows. It expects topic folders and normalized `plan.yaml` files. Use it to keep repeated phase instructions consistent.

## Quality Checklist

Before calling a topic publish-ready, verify:

- `raw/` is unchanged.
- Source claims and teaching interpretation are not blurred.
- Prerequisites are introduced before use.
- Important formulas include definitions, intuition, and numerical examples where useful.
- No major mechanism is hidden behind phrases like “the model learns.”
- Visuals teach one specific idea each.
- Captions are not duplicated inside and outside visuals.
- Code demos are beginner-friendly and clearly scoped.
- `outputs/preview.html` is reader-facing.
- `outputs/publish/blog.md` is Jekyll-ready.
- Reviewer findings have been validated and recorded in `reviews/fix_log.md`.

## Current Example Topic

The `word2vec` topic demonstrates the full workflow:

```text
topics/word2vec/
```

It includes:

- source map and compiled wiki
- lesson draft
- SVG visual assets
- toy Python demos
- reader-facing preview
- reviewer report and fix log
- publish pack for `karthik.dev`
- experimental Manim scenes

Use it as the reference implementation for future topics.
