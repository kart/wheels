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
