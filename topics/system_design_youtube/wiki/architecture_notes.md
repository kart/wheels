# Architecture Notes

## High-Level Components

- API gateway / edge API.
- Auth and authorization service.
- Upload service.
- Object storage for originals and derived media.
- Metadata service and metadata database.
- Processing queue.
- Transcoding workers.
- Thumbnail and manifest generation.
- Playback service.
- CDN/edge cache.
- Search indexing pipeline and search service.
- Feed/recommendation service.
- Engagement services for likes, comments, subscriptions.
- Event stream for watch/engagement/analytics.
- Counter aggregation.
- Moderation and abuse review hooks.
- Observability stack.

## Upload Pipeline

Plausible flow:

1. Client creates upload session.
2. Upload service creates video row in `UPLOADING` or `DRAFT` state.
3. Client uploads bytes to object storage through a resumable path.
4. Client completes upload session.
5. Upload service verifies checksum/object presence.
6. Upload service emits `VideoUploaded` event.
7. Processing queue fans work to validation, media inspection, transcoding, thumbnailing, and manifest generation.
8. Metadata transitions through `PROCESSING`, `READY`, `PUBLISHED`, or `FAILED`.

Key design choices:

- Make upload idempotent with session IDs and object checksums.
- Store the original before processing.
- Keep processing asynchronous.
- Separate user-visible upload state from internal job state.

Failure cases:

- Client disconnects mid-upload.
- Duplicate completion request.
- Object exists but checksum fails.
- Transcoding worker crashes.
- One rendition fails while others succeed.
- Moderation blocks publication.

## Transcoding Pipeline

Public grounding:

- YouTube's blog states that uploaded videos must be prepared for different devices and resolutions.
- It describes transcoding as compressing video for efficient delivery at high quality.
- It says transcoding is costly and slow on CPUs and that YouTube built VCU acceleration.
- Google Research describes warehouse-scale video transcoding acceleration and reports 20-33x efficiency over a prior baseline.

Plausible design:

- Job planner creates rendition jobs based on input properties, product policy, and codec ladder.
- Queue partitions jobs by priority, codec, resolution, or resource class.
- Workers write outputs to object storage.
- Manifest generator publishes a manifest only after required renditions are ready.
- Optional policy: publish low-resolution rendition first, add higher-quality renditions later.

Teaching point:

- Better codecs can reduce delivery cost but increase processing cost. The platform optimizes the whole system, not just one service.

## Playback Pipeline

Plausible flow:

1. Video page requests metadata.
2. Playback service checks video visibility, readiness, region, and policy.
3. Playback service returns manifest URL and metadata.
4. Player requests chunks.
5. CDN/edge cache serves chunks on hit.
6. On miss, cache fetches from origin or origin shield backed by object storage.
7. Player emits watch events asynchronously.

Public grounding:

- Google Global Cache docs support the concept of serving certain Google content from inside ISP networks and reducing external traffic.

Design choices:

- Keep media bytes off metadata services.
- Cache chunks and thumbnails aggressively.
- Use signed URLs or tokenized manifests if access control matters.
- Handle cache miss storms for newly viral videos.

## Search Indexing

Plausible flow:

1. Metadata update or publish event enters event stream.
2. Indexing worker enriches the document.
3. Search index stores searchable fields.
4. Query service retrieves candidates and applies filters such as visibility, region, language, and safety.

Tradeoffs:

- Search index is fast but eventually consistent.
- Primary metadata database remains source of truth.
- Deletes and privacy changes require careful propagation and possibly tombstones.

## Recommendations And Feed

Scope for this article:

- High-level candidate generation and ranking, not full ML model design.

Plausible flow:

1. Watch/like/subscription events enter stream.
2. Feature pipelines aggregate recent user/video/channel signals.
3. Candidate generators use subscriptions, similar videos, trending items, search history, or collaborative signals.
4. Ranker orders candidates.
5. Feed service applies filters and returns items.

Teaching caveat:

- Do not invent exact features or model architecture. Keep this section focused on system boundaries and freshness/latency tradeoffs.

## Engagement, Comments, And Subscriptions

Likes/dislikes:

- Store user action for idempotency and toggling.
- Aggregate counts asynchronously.
- Provide actor read-your-write behavior.

Comments:

- Write path needs moderation hooks and spam controls.
- Read path needs pagination, ranking/sorting, and caching.

Subscriptions:

- Store subscriber-channel relationships.
- Feed fanout can be pull-based, push-based, or hybrid.

Counters:

- Watch events should be buffered and deduplicated.
- Aggregate counts may lag.
- Hot videos need partitioned counters or time-bucketed aggregation.

## Moderation Hooks

Possible hooks:

- Pre-publication media scan.
- Metadata/text checks.
- Comment spam detection.
- User/channel trust signals.
- Manual review queues for flagged content.

Design caveat:

- This article should describe where moderation fits in the architecture, not make policy claims.

## Visual Opportunities

- Upload sequence diagram.
- Transcoding job DAG.
- Playback hit/miss flow.
- Metadata/search index update flow.
- Counter aggregation pipeline.
- Final architecture map with public-fact callouts.
