# Operations And Failure Modes

## Reliability Priorities

The watch path should usually have the highest availability target because it is the dominant user-facing read path. Upload and processing can often tolerate more delay, as long as the system is honest about state and does not lose data.

Candidate SLOs:

- Video page metadata latency.
- Playback manifest latency.
- Playback startup time.
- Playback error rate.
- Upload session creation success.
- Upload completion durability.
- Time from upload completion to first playable rendition.
- Transcoding backlog age.
- Search indexing freshness.
- Comment/engagement write success.

## Observability

Metrics:

- API QPS, latency, error rate by endpoint.
- Upload throughput and failure reasons.
- Object storage read/write errors.
- Queue depth and oldest message age.
- Transcoding job duration by codec/resolution.
- Rendition failure rate.
- CDN cache hit ratio and origin egress.
- Manifest request errors.
- Search indexing lag.
- Counter aggregation lag.
- Comment moderation queue size.

Logs:

- Request IDs across upload, processing, playback, and storage.
- State transition logs for video publication.
- Worker failure and retry logs.

Traces:

- Upload complete to processing enqueue.
- Playback request to manifest generation.
- Metadata read path with cache/database spans.

## Failure Modes

| Failure | User impact | Design response |
| --- | --- | --- |
| Upload interrupted | Creator upload stalls or fails | Resumable upload session and retryable chunks |
| Upload complete called twice | Duplicate processing jobs | Idempotency key and video state check |
| Transcoding backlog grows | New videos take longer to publish | Priority queues, backlog alerts, limited rendition policy |
| One rendition fails | Some quality levels missing | Publish available renditions or mark failed depending on policy |
| Metadata database shard hot | Video page latency rises | Cache, split hot data, avoid hot counters in primary row |
| CDN cache miss storm | Origin overload | Origin shielding, request collapsing, pre-warming for expected viral content |
| Search index lag | New/updated videos not searchable immediately | Expose eventual consistency, monitor lag, replay events |
| Counter pipeline delayed | View/like counts stale | Eventual count display and reconciliation |
| Comment spam surge | Poor content quality or abuse | Rate limits, moderation queues, trust signals |
| Region outage | Playback/upload degraded | Failover strategy, regional routing, clear degradation policy |

## Degradation Strategies

- Serve cached metadata when the primary metadata read path is degraded.
- Continue playback for cached/public videos even if engagement writes lag.
- Accept uploads but delay processing when transcoding is saturated.
- Temporarily generate fewer renditions during processing backlog.
- Disable or simplify recommendations while preserving search/subscriptions.
- Show stale counters rather than blocking watch pages.

## Consistency Boundaries

Stronger consistency needed:

- Ownership and authorization.
- Video privacy and deletion.
- Publication state transitions.
- User action idempotency for likes/subscriptions.

Eventual consistency acceptable:

- View counts.
- Aggregate likes/dislikes.
- Search index freshness.
- Recommendation features.
- Analytics dashboards.

## Multi-Region Notes

Main L5 path:

- Start with regional primary metadata, replicated object storage, CDN edge delivery, and async pipelines.

L6+ extension:

- Discuss active-active metadata only after identifying conflict boundaries.
- Privacy/deletion and publication state should not rely on vague eventual consistency.
- Regional cache/object placement affects egress cost, latency, and recovery behavior.
- Cross-region replay of event streams requires idempotent consumers.

## Cost Controls

Major cost domains:

- Original and derived video storage.
- Transcoding compute or accelerators.
- CDN egress and cache miss origin egress.
- Metadata database replicas/shards.
- Search index storage and query capacity.
- Event stream and analytics storage.

Cost-aware design choices:

- Rendition ladder policy based on popularity and device demand.
- Retain originals and derived files according to product/legal needs.
- Use edge caching for popular chunks.
- Avoid synchronous per-view database writes.
- Batch and aggregate events.
- Tune search and recommendation freshness by product value.

## Review Risks For Later Prose

- Overclaiming exact YouTube internals.
- Treating L6+ as more components instead of clearer tradeoffs.
- Hand-waving "scales horizontally" without naming the bottleneck removed.
- Omitting state transitions in upload/transcoding.
- Not explaining what happens when queues back up.
- Using exact-looking numbers without labeling assumptions.
