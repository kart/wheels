# Wiki Index

Topic: `system_design_youtube`

Article shape: `system_design_deep_dive`

Audience: `system_design_interview_l5_plus`

## Purpose

This wiki is the internal source-grounded understanding layer for a YouTube-like video platform system design. It is not final article prose. Later section planning should use it to create small, reader-approved article sections.

## Source Boundary

Public sources ground only a few real-world facts:

- Google Global Cache shows that Google serves some content from ISP-hosted caches and reports typical cacheable-traffic hit rates for GGC.
- Vitess public docs show one YouTube-era path for scaling MySQL: primary/replica, more replicas, sharding, and proxy-based routing.
- YouTube/Google sources show that video transcoding is expensive at scale and that YouTube built VCU acceleration with reported 20-33x efficiency improvements over a prior optimized baseline.

Everything else in the article should be labeled as a plausible design for a YouTube-like platform, not actual YouTube internals.

## Wiki Files

- `source_map.md`: raw files, public URLs, source claims, and source-use boundaries.
- `requirements_and_scope.md`: product scope, user journeys, requirements, non-goals, and section planning notes.
- `capacity_and_constraints.md`: interview-scale assumptions, workload shape, bottlenecks, and estimate caveats.
- `apis_and_entities.md`: APIs, core entities, schemas, storage domains, and SQL/NoSQL tradeoffs.
- `architecture_notes.md`: upload, transcoding, playback, CDN/cache, search, feed, engagement, counters, and moderation notes.
- `operations_and_failure_modes.md`: SLOs, observability, failure modes, degradation, multi-region, and cost controls.
- `glossary.md`: definitions and prerequisite ladder.
- `open_questions.md`: source caveats, claims to qualify, and future source gaps.

## Recommended Reader-Facing Section Flow

1. What are we building, and what are we not claiming?
2. Requirements, APIs, and scale.
3. Data model and storage choices.
4. Upload and transcoding pipeline.
5. Playback, CDN, and edge caching.
6. Search, recommendations, and engagement.
7. Reliability, observability, and cost.
8. Final architecture and interview recap.

## Planning Notes

Later section phases should include diagrams heavily:

- Journey map for upload and watch.
- Entity/data model diagram.
- Upload/transcoding sequence.
- Playback cache-hit/cache-miss sequence.
- Search/recommendation update flow.
- Counter aggregation pipeline.
- Final architecture diagram.
- Failure-mode and SLO tables.

No section prose has been generated during bootstrap.
