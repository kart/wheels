# Open Questions And Caveats

## Source Access

- No PDFs were present under `raw/`, so no PDF extraction or rich source-asset audit was required.
- The Google Research page exposes an abstract and metadata. The full ACM paper was not added under `raw/`, so later sections should not claim details beyond the accessible abstract unless the paper is supplied.
- Public pages support several real-world facts about Google/YouTube systems, but they do not disclose full internal architecture.

## Claims That Must Stay Qualified

- CDN/cache design should be framed as a plausible design for a YouTube-like platform, with Google Global Cache used only as public grounding for edge caching concepts.
- Metadata storage should explain Vitess as public evidence that sharded SQL can scale, not as proof of the current YouTube schema or database layout.
- Transcoding pipeline design should be framed as a plausible architecture. Public sources support that YouTube uses custom VCU acceleration and warehouse-scale video processing, but not the exact queue, scheduler, or worker topology.
- Recommendation/feed serving should be high-level unless additional sources are added. Avoid inventing exact ranking models or feature weights.
- Abuse/moderation should be described as hooks and workflows, not as a full policy or ML enforcement system.

## Design Assumptions To Make Explicit Later

- Traffic and storage estimates will be article assumptions for interview practice, not sourced measurements unless tied to a public source.
- API examples and schemas are teaching artifacts.
- Consistency choices should be domain-specific: strong enough for ownership/security/publication state, looser for counters and analytics.
- Multi-region design depth should appear as selective L6+ extensions rather than splitting every section into level-specific versions.

## Reader Confusions To Prevent

- "CDN" is not just a cache; it changes the request path, cost profile, failure modes, and origin load.
- "Transcoding" is not upload storage; it creates playable renditions and manifests after the original upload is durably stored.
- "SQL versus NoSQL" is not a binary scale/no-scale decision. Sharded SQL and NoSQL solve different operational and query-model problems.
- "Recommendations" should not consume the whole article; for this topic, it is one subsystem inside a broader video platform design.
- "View count" is not a simple synchronous increment at high scale; counters need buffering, deduplication/abuse controls, and delayed aggregation.

## Possible Future Source Additions

- Full text of the warehouse-scale video acceleration paper for deeper VCU details.
- Public docs about adaptive bitrate streaming formats if the article needs more playback detail.
- Public cloud docs for generic object storage, queues, stream processing, search indexing, and CDN behavior, if the user wants broader infrastructure grounding.
