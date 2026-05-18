# APIs And Entities

## API Boundary Notes

API examples in the final article should be teaching artifacts. They are not sourced YouTube APIs.

Good API sections should explain:

- Who calls the API.
- What durable state changes.
- Whether the response means "accepted", "processed", or "published".
- What errors/retries mean.
- Which operations can be eventually consistent.

## Candidate APIs

### Upload Session

```http
POST /v1/upload-sessions
```

Request fields:

- `channel_id`
- `filename`
- `content_type`
- `content_length`
- `checksum`
- `visibility`

Response fields:

- `upload_session_id`
- `upload_url`
- `expires_at`
- `video_id`

Teaching point: create metadata and upload intent before bytes are fully uploaded.

### Complete Upload

```http
POST /v1/upload-sessions/{upload_session_id}/complete
```

Response fields:

- `video_id`
- `processing_state`

Teaching point: completion should enqueue processing and return "processing", not pretend all playback renditions are ready.

### Video Metadata

```http
GET /v1/videos/{video_id}
PATCH /v1/videos/{video_id}
```

Teaching point: metadata reads are latency-sensitive and often cached; metadata writes need authorization and publication-state checks.

### Playback Manifest

```http
GET /v1/videos/{video_id}/playback
```

Response fields:

- `manifest_url`
- `available_renditions`
- `license_or_access_policy` if needed

Teaching point: the API returns control metadata; the player then fetches media chunks through CDN paths.

### Engagement

```http
POST /v1/videos/{video_id}/likes
DELETE /v1/videos/{video_id}/likes
POST /v1/videos/{video_id}/comments
GET /v1/videos/{video_id}/comments
```

Teaching point: user-visible action state may need read-your-write behavior for the actor, while aggregate counts can lag.

### Subscriptions And Feed

```http
POST /v1/channels/{channel_id}/subscriptions
GET /v1/me/feed
GET /v1/search?q=...
```

Teaching point: feed and search can be served from specialized indexes rather than scanning primary metadata storage.

## Core Entities

### User

- `user_id`
- authentication and profile state
- abuse/trust signals

### Channel

- `channel_id`
- owner `user_id`
- display metadata
- subscriber count summary

### Video

- `video_id`
- `channel_id`
- title, description, tags
- visibility
- upload state
- processing state
- publication timestamps
- source object pointer
- active manifest pointer

### Rendition

- `rendition_id`
- `video_id`
- codec
- resolution
- bitrate
- object path
- processing status

### Manifest

- `manifest_id`
- `video_id`
- rendition list
- version
- object path

### Engagement

- like/dislike action by user/video
- comment
- subscription
- watch event
- aggregated counters

## Storage Domains

### Metadata Store

Good fit for:

- users, channels, videos, publication state, ownership, basic engagement action state.

Possible implementation:

- Sharded SQL, potentially with a Vitess-like proxy architecture.

Source grounding:

- Vitess public docs show that YouTube-era MySQL scaling led from replicas to sharding and proxy-based query routing.
- Vitess docs describe VTGate, VTTablet, topology service, connection pooling, query rewriting, and sharding.

Tradeoff:

- SQL helps with relationships, transactions, indexes, and operational familiarity.
- Sharding adds operational and query complexity.

### Object Storage

Good fit for:

- original uploads, transcoded chunks, thumbnails, manifests.

Tradeoff:

- Cheap durable bytes and high throughput.
- Not suitable for rich metadata queries.

### Search Index

Good fit for:

- text search by title, description, channel, tags, language, and freshness.

Tradeoff:

- Fast retrieval but asynchronously updated.
- Needs reindexing and consistency caveats.

### Analytics/Event Stream

Good fit for:

- watch events, view counts, recommendation signals, abuse signals, operational events.

Tradeoff:

- High write volume and delayed aggregation.
- Requires deduplication and late-event handling.

## SQL Versus NoSQL Teaching Points

Avoid the shallow answer "NoSQL because scale." Better framing:

- Use SQL where relationships, constraints, transactions, and indexes matter.
- Use sharding/proxy patterns when a single SQL instance becomes the bottleneck.
- Use NoSQL/wide-column/key-value stores where access patterns are simple, write volume is extreme, and flexible horizontal partitioning matters.
- Use search indexes for search, not as the source of truth.
- Use event streams/analytics stores for counters and signals, not as the canonical metadata store.

## Candidate Shard Keys

- `video_id` for video metadata and renditions.
- `channel_id` for channel-owned video listings.
- `user_id` for subscriptions and user action state.
- Time buckets plus `video_id` for watch events and counters.

Teaching caveat: shard keys encode access patterns. A key that balances writes may make common reads expensive.
