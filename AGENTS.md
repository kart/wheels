# Wheels — Agent Instructions

## Project Goal

Wheels turns raw learning resources into structured understanding and publishable explanations.

The workflow is:

raw sources → generated plan → compiled wiki → lesson + visuals → HTML preview → reviewer audit → fixer loop → publish pack

## Core Folders

- raw/ contains human-provided source material. Do not overwrite raw files.
- wiki/ contains LLM-compiled understanding.
- outputs/ contains lessons, visuals, code, previews, and publish drafts.
- reviews/ contains reviewer reports and fix logs.

## Explanation Quality Bar

The target reader is smart but may be new to the topic.

Assume:
- undergraduate-level technical maturity
- math may be weak
- coding skill is novice to beginner
- examples, intuition, and visuals are essential

Every lesson should:
- build up concepts gradually
- start with motivation before mechanics
- use intuition before equations
- use examples before abstraction
- use visuals wherever they reduce cognitive load
- avoid long walls of text
- avoid shallow summaries
- avoid unexplained equations
- explain code before showing code
- use well-commented educational code if code is included

## Visual Quality Bar

Visuals are first-class teaching artifacts.

Good visuals:
- explain a mechanism, contrast, flow, or structure
- are placed near the relevant text
- have clear captions
- use accurate labels, arrows, axes, and numbers
- are simple but correct

Bad visuals:
- are decorative but not educational
- contradict the text
- use wrong numbers or misleading charts
- have unclear arrows, labels, or captions

## Source Fidelity Rules

- Stay grounded in provided sources.
- Clearly separate source claims from interpretation.
- Do not invent claims.
- Do not overclaim historical importance.
- If unsure, say so.
- If PDF reading is insufficient, ask for extracted text or figures.

## Reviewer Rule

The reviewer must not edit lesson, wiki, output, visual, or raw files.

The reviewer only writes review reports.

## Fixer Rule

The fixer must validate reviewer comments before applying them.

Do not blindly apply reviewer feedback.

## Article Shapes

Every topic should choose an article shape in topic.yaml.

Available article shapes live in:

templates/article_shapes.md

Supported shapes:
- paper_deep_dive
- system_design_deep_dive
- algorithm_walkthrough

The selected article shape should guide:
- outputs/lesson.md
- outputs/preview.html
- outputs/publish/blog.md

## Audience Profiles

Reusable audience profiles live in:

prompts/audience_profiles.md

The topic.yaml should choose an audience profile.

The selected audience profile should guide:
- explanation depth
- pacing
- amount of math
- code style
- visual density

## Preview vs Publish

outputs/preview.html should be a reader-facing local preview of the eventual blog, not an internal artifact dashboard.

Internal/debug information should go in:
- wiki_preview/
- reviews/
- outputs/audit_preview.html if needed

## Jekyll Publish Contract

outputs/publish/blog.md should be copy-pasteable into karthik.dev/_posts/.

It should include Jekyll front matter:

---
layout: default
title: "..."
excerpt: "..."
category: "..."
---

For paper posts, it should also include:
- short italic series/context intro
- paper citation blockquote
- beginner-friendly sections
- image references using the configured asset_base_path
- math where useful
- code where useful
- caveats
- recap
- next-up section

Do not actually publish anything.

## Teaching Depth Contract

Generated content must help a smart beginner understand the topic from first principles.

Do not merely summarize. Build understanding.

Every major explanation should answer:

1. What problem are we solving?
2. What did people do before?
3. What is the bottleneck or confusion?
4. What is the new idea?
5. What are the inputs?
6. What are the outputs?
7. What parameters, state, data structures, or system components exist?
8. What changes during training, execution, or operation?
9. Why does the mechanism work?
10. What are the caveats?

## Prerequisite Ladder Rule

Before using a concept, either explain it or explicitly mark it as assumed.

For math-heavy topics:
- introduce symbols before formulas
- explain intuition before equations
- provide a tiny numerical example after nontrivial formulas
- do not assume softmax, dot product, cosine similarity, loss functions, matrix multiplication, or gradients unless the topic.yaml says they are assumed

For coding-heavy topics:
- explain the idea before code
- use beginner-friendly comments
- avoid clever code when clear code is better

## No Black Boxes Rule

Avoid phrases like:
- "the model learns"
- "the vectors are trained"
- "the system scales"
- "the algorithm is faster"

unless you explain what is changing and why.

Examples:
- If a model learns, explain what parameters are updated.
- If a system scales, explain what bottleneck was reduced.
- If an algorithm is faster, explain what work was avoided.
- If a vector representation is trained, explain the training signal and update intuition.

## Formula Rule

Every important formula should be followed by:
- what each symbol means
- a plain-English reading
- a small numerical example when useful
- the reason the formula matters

## Visual Rule

Each visual must teach one specific idea.

Rules:
- One visual should have one caption.
- Do not duplicate the same caption both inside the image and below it.
- Do not include long prose inside the image if the article already explains it.
- Visuals must be placed near the relevant text.
- Diagrams must have correct arrows, labels, directions, axes, and caveats.
- Qualitative charts must be labeled as qualitative.
- Do not invent exact numeric charts unless the numbers are sourced.

## Reader-Facing Preview Rule

outputs/preview.html should read like the final blog draft.

It should not look like an internal artifact dashboard.

Internal/debug material should either be omitted or moved to a collapsed Build Notes section at the bottom.

## Real-World Grounding Rule

For every deep-dive topic, include a practical workflow section when relevant.

Examples:
- For papers: how someone would train/use/deploy the idea in practice.
- For system design: how one real request flows through the system.
- For algorithms: how the pattern appears in related problems.

## Paper Deep-Dive Rule

For paper_deep_dive topics, the final blog must not collapse the paper into a high-level overview.

It must include either:
1. a section-by-section walkthrough of the source paper, or
2. an explicitly justified adapted structure that still covers every major paper section deeply.

The article should preserve paper fidelity while filling in missing intuition for the reader.
