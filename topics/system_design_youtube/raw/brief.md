# System Design Brief: YouTube-like Video Platform

## Goal

Design a YouTube-like video platform as a serious system design deep dive.

The article should be useful for system design interview preparation, with the main path aimed at a strong L5 candidate and selective L6+ callouts where senior-level depth matters.

## Audience

Audience profile:

system_design_interview_l5_plus

Meaning:

- Main flow should be understandable and useful for a strong L5 candidate.
- Include clearly marked L6+ extensions only when they add meaningful design depth.
- Do not write separate L5/L6/L7 versions of every section.
- Avoid shallow interview-prep answers.

## Product Scope

Design a platform where users can:

- upload videos
- watch videos
- browse video metadata
- search videos
- like/dislike videos
- comment on videos
- subscribe to channels
- receive recommendations/feed suggestions
- see view counts and engagement signals

## Main Design Areas To Cover

The final deep dive should cover:

- requirements and non-goals
- capacity and traffic assumptions
- APIs
- core entities
- upload workflow
- video processing/transcoding pipeline
- metadata storage
- blob/object/video storage
- SQL vs NoSQL tradeoffs
- playback workflow
- CDN and edge caching
- search indexing
- recommendations/feed serving at a high level
- comments, likes, subscriptions
- counters and analytics
- abuse/moderation hooks
- reliability and failure modes
- observability and SLOs
- cost/performance tradeoffs
- evolution from simple design to scaled design

## Important Framing

Do not claim to describe YouTube's actual internal architecture unless supported by public sources.

Use phrasing such as:

- "A YouTube-like system could..."
- "One plausible design is..."
- "A public source says..."
- "An inferred design choice is..."

## Non-Goals

Do not:

- copy Alex Xu, Grokking, or any interview-prep source
- produce a generic boxes-and-arrows answer
- skip database modeling
- skip API design
- skip failure modes
- skip SQL vs NoSQL reasoning
- claim exact YouTube internals without public evidence
- make every section separately discuss L5, L6, and L7

## Desired Output Style

The article should include:

- architecture diagrams
- sequence/workflow diagrams
- API examples
- data model examples
- design-decision tables
- failure-mode tables
- capacity estimates
- L6+ callouts where meaningful
- clear separation of public facts and inferred design choices
