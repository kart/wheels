# Source Map

Topic: `system_design_youtube`

This topic is a source-grounded but mostly first-principles system design article. The sources provide public facts and realism anchors. The final design must not claim to be YouTube's actual internal architecture unless a public source directly supports the claim.

## Raw Files

### `raw/brief.md`

Type: topic brief and acceptance criteria.

Use for:

- Product scope: upload, watch, browse metadata, search, likes/dislikes, comments, subscriptions, recommendations/feed suggestions, view counts, and engagement signals.
- Required design areas: requirements, capacity, APIs, entities, upload, transcoding, metadata storage, object storage, SQL versus NoSQL, playback, CDN, search, recommendations, engagement, counters, moderation, reliability, observability, cost, and design evolution.
- Framing rule: use phrases such as "a YouTube-like system could..." and "one plausible design is..." when discussing inferred architecture.

Source status: local, readable.

### `raw/sources.md`

Type: source pack with public grounding URLs and source-use rules.

Use for:

- Public grounding on Google Global Cache.
- Public grounding on YouTube-era MySQL scaling and Vitess.
- Public grounding on video transcoding and warehouse-scale video acceleration.
- Source-use constraints: do not copy interview-prep prose, structure, or diagrams; use optional interview sources only as coverage checklists.

Source status: local, readable.

## Public Grounding Sources

### Google Global Cache introduction

URL: <https://support.google.com/interconnect/answer/9058809?hl=en>

Public facts available from the source:

- Google Global Cache allows ISPs to serve some Google content from inside their own networks.
- The stated benefit is less congestion inside ISP networks and less traffic on peering/transit links.
- Google describes GGC as transparent to users.
- The source says typically 70-90% of cacheable traffic can be served from GGC, with cache hit rates varying by operator consumption patterns.
- Google says GGC has multiple levels of redundancy and serves users from the best available data location during temporary outages.

How to use:

- Ground the edge caching/CDN section.
- Explain why video systems push popular content close to viewers.
- Use the 70-90% figure only as a Google-stated GGC claim, not as a generic guarantee for every video platform.

Do not infer:

- Exact YouTube cache placement, eviction algorithms, routing policy, cache topology, or internal CDN control-plane details.

### Vitess history

URL: <https://vitess.io/docs/23.0/overview/history/>

Public facts available from the source:

- Vitess was created in 2010 to solve MySQL scalability challenges faced by YouTube.
- The documented progression was primary database for writes, replica for reads, more replicas for high read-only traffic, then sharding when write traffic became too high or data became too large for one MySQL instance.
- Before Vitess, the application layer had to identify the right shard before database operations.
- Vitess introduced a proxy between application and database to route and manage database interactions.
- The source says YouTube scaled its user base by more than 50x since then and Vitess continued as a scaling platform.

How to use:

- Ground the metadata storage section.
- Explain why "just use MySQL" evolves into read replicas, sharding, and routing/proxy layers.
- Discuss SQL versus NoSQL without pretending SQL stops being viable at scale.

Do not infer:

- Current YouTube metadata schema, shard keys, table layout, or exact traffic distribution.

### What is Vitess

URL: <https://vitess.io/docs/24.0/overview/whatisvitess/>

Public facts available from the source:

- Vitess is an open-source database clustering system for horizontally scaling MySQL.
- It distributes data across MySQL instances through sharding while presenting a unified database interface.
- VTGate accepts MySQL-protocol connections and routes queries to the right shards.
- VTTablet runs alongside each MySQL instance and manages queries, connections, and replication.
- A topology service such as etcd, ZooKeeper, or Consul maintains cluster state.
- Vitess addresses scaling beyond a single server, cluster management, and database protection.
- Vitess features include connection pooling, query rewriting/sanitization, query blocking/killing, monitoring, topology management, and sharding.
- The source contrasts Vitess with NoSQL by noting SQL semantics, transactions, existing MySQL tooling, and indexing support.

How to use:

- Ground the SQL versus NoSQL tradeoff section.
- Explain a plausible "scalable SQL metadata tier" pattern for video metadata, channel metadata, subscriptions, and some engagement data.
- Use VTGate/VTTablet as an example of proxy-based sharded SQL architecture.

Do not infer:

- That a YouTube-like design must use Vitess, or that every data domain should use SQL.

### YouTube Blog: Reimagining video infrastructure

URL: <https://blog.youtube/inside-youtube/new-era-video-infrastructure/>

Public facts available from the source:

- YouTube states that videos are uploaded in one format but consumed on different devices and resolutions.
- The source explains transcoding as compressing videos so the service sends the smallest amount of data to a chosen device with high quality.
- It says transcoding is costly and slow on CPUs, especially as uploaded volume grows.
- YouTube created a custom chip and software coordination system for transcoding, called the Video (trans)Coding Unit (VCU).
- The source reports up to 20-33x compute-efficiency improvement versus its previous optimized CPU-based system.
- It says more than 500 hours of video content on average are uploaded every minute.
- It says higher-quality video and more efficient codecs such as VP9 motivated more efficient/scalable infrastructure, and VP9 used 5x more compute resources to encode than H.264 in the cited comparison.

How to use:

- Ground the upload and transcoding pipeline.
- Explain why transcoding is an asynchronous pipeline rather than a synchronous API request.
- Explain the cost/performance tradeoff between better compression and more encode compute.

Do not infer:

- Exact VCU scheduling, fleet size, codec ladder policy, queue structure, or failure-handling internals.

### Google Research: Warehouse-Scale Video Acceleration

URL: <https://research.google/pubs/warehouse-scale-video-acceleration-co-design-and-deployment-in-the-wild/>

Public facts available from the source:

- The abstract says video sharing accounts for the majority of internet traffic.
- It frames video processing as important for video sharing, conferencing, AR/VR, cloud gaming, and IoT video.
- It describes a warehouse-scale video transcoding accelerator using a video coding unit (VCU).
- It discusses hardware design, data-center-scale tradeoffs, and co-design with distributed software systems.
- It reports 20-33x improved efficiency over a prior well-tuned non-accelerated baseline.
- It says the design helps adapt to changing bottlenecks, improves failure management, and enables new workload capabilities.

How to use:

- Deepen the transcoding and operations discussion.
- Support the claim that video processing is a warehouse-scale workload and not merely an application feature.
- Use accelerator discussion as an L6+ extension about hardware/software co-design and cost efficiency.

Do not infer:

- Full paper details not present in the accessible abstract unless the paper PDF/text is later added to raw/.

## Optional Coverage References

The raw source pack names Alex Xu, Grokking, common YouTube interview prompts, and cloud provider architecture docs as optional coverage checklists only. They should not be copied, paraphrased, or used as primary source prose or structure.

## Inferred Design Space

The final article may propose a plausible YouTube-like architecture with the following explicitly labeled as design choices, not public facts:

- API shapes for uploads, video metadata, comments, likes, subscriptions, search, and feed.
- Metadata schemas and shard keys.
- Object storage layout and video rendition naming.
- Queue topics and worker pools for transcoding.
- Search index update pipeline.
- Recommendation candidate generation and ranking flow at a high level.
- Counter aggregation and analytics pipeline.
- Abuse/moderation hooks.
- Multi-region strategy, disaster recovery, and degradation modes.
- Observability dashboards, SLOs, and operational runbooks.

## Source-Fidelity Rules For Later Sections

- Use "public source says" for the facts above.
- Use "a YouTube-like system could" or "one plausible interview design is" for architecture choices not directly sourced.
- Do not present exact YouTube internals unless a public source directly supports the claim.
- Do not use the GGC cache-hit figure as a generic CDN guarantee.
- Do not use the VCU efficiency figure as a generic transcoding speedup.
- Do not imply Vitess is the only correct metadata database answer.
