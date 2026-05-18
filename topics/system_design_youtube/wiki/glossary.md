# Glossary

## Adaptive Bitrate Streaming

A playback approach where the player switches between different quality levels based on network and device conditions. The server prepares multiple renditions of the same video.

## Cache Hit

A request is served by a cache because the requested item is already there. In video systems, cache hits reduce latency and origin load.

## Cache Miss

A request cannot be served by the cache, so the system fetches from an upstream cache, origin service, or object storage.

## CDN

A content delivery network places content closer to users. For video playback, the CDN usually serves chunks and thumbnails, not application metadata.

## Consistency

The rule for when different readers see the same state. Stronger consistency is useful for privacy and ownership; eventual consistency is often acceptable for counters and analytics.

## Edge Cache

A cache near users, often inside or near ISP networks. Google Global Cache is a public Google example for certain Google content.

## Idempotency

Retrying the same operation has the same effect as doing it once. Upload completion and processing job creation should be idempotent.

## Manifest

A file or response that tells the video player which renditions/chunks are available and where to fetch them.

## Metadata

Small structured data about videos, users, channels, comments, and state. Metadata is separate from large media blobs.

## Object Storage

Durable storage for large blobs such as original videos, transcoded chunks, thumbnails, and manifests.

## Origin

The upstream source of content when an edge cache misses. In a video design, origin can be backed by object storage and origin services.

## Queue

A durable buffer between services. Upload completion can enqueue processing so the user request does not wait for transcoding.

## Read Replica

A database copy used to scale reads or improve availability. It does not solve every write-scaling problem.

## Rendition

One generated version of a video, such as 1080p VP9 or 480p H.264.

## Sharding

Splitting data across multiple database partitions. It increases capacity but forces careful routing, key choice, and operational tooling.

## SLO

Service Level Objective: a concrete target such as "99.9% of manifest requests complete under X ms."

## Transcoding

Converting/compressing an uploaded video into formats, resolutions, and bitrates suitable for playback on different devices and networks.

## VTGate / VTTablet

Vitess components. VTGate routes MySQL-protocol queries to the right shards; VTTablet runs alongside MySQL instances and manages query/connection/replication behavior.

## Watch Event

An event emitted when a user watches video. It can feed counters, analytics, recommendations, and abuse systems.
