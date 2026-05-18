# Requirements And Scope

## Product Goal

Design a YouTube-like platform where creators upload videos and viewers discover, watch, search, react to, comment on, and subscribe to video content.

This is an interview-oriented design, not a claim about YouTube's exact internals.

## Concrete User Journeys

### Creator Upload Journey

1. Creator authenticates.
2. Creator requests an upload session.
3. Client uploads the original video, ideally resumably, to an ingest endpoint or object-storage-backed upload path.
4. Metadata is created in a draft or processing state.
5. A durable message starts asynchronous processing.
6. Workers validate the file, inspect media properties, transcode into playable renditions, generate thumbnails, and build manifests.
7. The video moves to published or failed-review state.
8. Search, feed, subscription, and notification systems receive update events.

Key teaching point: upload completion is not the same as video availability. The system should acknowledge durable receipt before all derived video formats exist.

### Viewer Playback Journey

1. Viewer opens a video page or feed item.
2. API fetches video metadata, creator metadata, engagement summary, comments preview, and watch authorization.
3. Playback service returns a manifest pointing to available renditions.
4. Player fetches video chunks from CDN/edge cache if available.
5. Cache misses go toward origin/object storage or an origin shield.
6. Watch events flow asynchronously into counters, recommendations, analytics, and abuse systems.

Key teaching point: the read path is dominated by playback media traffic, while metadata calls are smaller but latency-sensitive.

## Functional Requirements

- Upload videos.
- Process videos into device/network-appropriate playable versions.
- Store originals and generated renditions.
- Publish and browse video metadata.
- Watch videos with adaptive playback.
- Search videos.
- Like/dislike videos.
- Comment on videos.
- Subscribe to channels.
- Provide feed/recommendation suggestions at a high level.
- Track views and engagement signals.
- Support abuse/moderation hooks.

## Nonfunctional Requirements

- Low-latency playback startup for popular videos.
- High availability for watch path.
- Durable upload storage.
- Eventual completion for transcoding.
- Backpressure when processing falls behind.
- Cost-aware storage and transcoding.
- Scalable metadata reads.
- Safe publication state transitions.
- Observable pipelines and user-facing SLOs.

## Non-Goals

- Exact YouTube internal architecture.
- Full recommendation model design.
- Full content moderation policy or classifier design.
- Copying an interview-prep source's structure, prose, or diagrams.
- Exact numeric capacity claims unless labeled as assumptions or sourced facts.

## Requirements Table For Later Article

| Area | Requirement | Why it matters | Likely design mechanism |
| --- | --- | --- | --- |
| Upload | Accept large files reliably | Network interruptions are common | Resumable upload, object storage, upload session state |
| Processing | Create playable renditions | Devices and bandwidth differ | Async queue, transcoding workers, manifests |
| Playback | Serve video chunks near viewers | Video traffic is heavy | CDN/edge cache, origin storage |
| Metadata | Fast page/feed reads | UI depends on metadata before playback | Indexed metadata store, cache |
| Engagement | Likes/comments/views | Product feedback and ranking signals | Write APIs, event streams, aggregation |
| Search | Find videos by text/metadata | Discovery path | Search index and async indexing |
| Feed | Suggest videos | Engagement path | Candidate generation, ranking service at high level |
| Safety | Avoid publishing unsafe content | Platform risk | Moderation hooks before/after publish |

## Section Planning Notes

Prerequisites to explain before using them:

- CDN and cache hit/miss.
- Object storage versus metadata database.
- Queue and asynchronous worker.
- Transcoding and adaptive bitrate.
- Sharding, replica, and consistency.
- SLO, metric, alert, and degradation.

Expected reader confusions:

- Why video upload is not handled like a small image upload.
- Why metadata storage and video blob storage are separate.
- Why view counts are eventually consistent.
- Why "NoSQL for scale" is too shallow.
- Why recommendations are a subsystem, not the whole design.
