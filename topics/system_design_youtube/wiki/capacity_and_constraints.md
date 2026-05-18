# Capacity And Constraints

## Source-Grounded Scale Anchors

Public sources provide only a few hard anchors:

- YouTube's blog says more than 500 hours of video are uploaded per minute on average.
- The same blog says videos are uploaded in one format but consumed across devices and resolutions, requiring transcoding.
- Google Global Cache documentation says GGC can serve certain Google content from ISP networks and that typically 70-90% of cacheable traffic can be served from GGC, varying by operator.
- Google Research's abstract says video sharing accounts for the majority of internet traffic.

These facts justify a design where media storage, transcoding, and edge delivery dominate scale and cost.

## Interview Assumptions

Later article sections can choose round numbers for teaching. They must be labeled as assumptions.

Example assumption set:

- 100 million daily active users.
- 10 million daily uploads.
- Average uploaded video length: 5 minutes.
- Average original upload size: 500 MB.
- Average generated storage multiplier: 2x to 5x depending on renditions/codecs and retention.
- Watch:write ratio is heavily read-dominated.
- Popular videos are highly skewed: a small fraction of videos drives a large fraction of media traffic.

These are not sourced YouTube measurements. They are a capacity-modeling scaffold.

## Workload Shape

### Upload Path

- Large request bodies.
- Lower QPS than watch path, but high bandwidth and storage impact.
- Requires durability before background processing.
- Burstiness from events, creator behavior, and network retries.
- Processing can lag if queues back up.

### Transcoding Path

- CPU/GPU/accelerator-intensive.
- Queue-based.
- Multiple outputs per input: resolutions, bitrates, codecs, thumbnails, manifests.
- More efficient codecs can reduce network/storage cost but increase encode compute.
- Public YouTube sources ground this tradeoff: VP9 can be more compute-intensive to encode than H.264, and YouTube built VCU acceleration for efficiency.

### Playback Path

- Extremely read-heavy.
- Bandwidth-dominant.
- Tail latency and startup time matter.
- Edge cache hit rate changes origin load and cost.
- Hot videos require cache and load-shedding strategies.

### Metadata Path

- Smaller payloads than media, but high QPS.
- Needs indexing, caching, and scalable storage.
- Some writes need stronger consistency: ownership, publication state, privacy, deletion.
- Some signals tolerate delay: view counts, analytics, recommendation feedback.

## Back-Of-The-Envelope Model

For a teaching example:

```text
daily_upload_storage = uploads_per_day * average_original_size
derived_storage = daily_upload_storage * rendition_multiplier
retained_storage = (daily_upload_storage + derived_storage) * retention_days
```

Plain English:

- First estimate the durable original uploads.
- Then add generated renditions and thumbnails.
- Then multiply by retention.

Example with assumptions:

```text
10M uploads/day * 500 MB = 5 PB/day of originals
5 PB/day * 3x derived multiplier = 15 PB/day derived
20 PB/day total new stored bytes before retention policy and compression details
```

This example is intentionally rough and should be labeled as capacity practice, not a source claim.

## Bottlenecks To Teach

- Upload bandwidth and durable ingest.
- Transcoding backlog and compute efficiency.
- Object storage throughput.
- CDN hit rate and origin egress.
- Metadata read QPS.
- Hot rows or partitions for popular videos and counters.
- Search indexing freshness.
- Recommendation feature pipeline lag.
- Abuse/moderation latency before publication.

## L6+ Extensions

- Capacity model should connect cost domains: storage cost, transcode compute, CDN/origin egress, metadata database cost, search index cost, analytics stream cost.
- Regionality matters: storage replication, cache placement, and data residency can conflict with cost.
- Backpressure is a product decision: allow upload but delay publish, reduce rendition set temporarily, or prioritize popular/creator-tier content.
- Multi-region active-active is not automatically best; publication state, ownership, and deletion flows may need strong coordination.
