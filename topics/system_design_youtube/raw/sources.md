# Source Pack: YouTube-like System Design

Use these sources as grounding and inspiration. Do not copy their structure, prose, diagrams, or design wholesale.

The article should distinguish:
- public facts from sources
- inferred design choices for a YouTube-like system
- interview-level simplifications

## Primary public grounding sources

### Google Global Cache / CDN

- Introduction to Google Global Cache
  - URL: https://support.google.com/interconnect/answer/9058809\?hl\=en
  - Use for: edge caching / CDN grounding.
  - Look for: what GGC is, what it means for ISPs to serve Google content from inside their own networks.
  - Source note: Google says GGC allows ISPs to serve certain Google content from within their own networks.

### Vitess / metadata database scaling

- Vitess History
  - URL: https://vitess.io/docs/23.0/overview/history/
  - Use for: public grounding on YouTube-era MySQL scalability.
  - Look for: why Vitess was created, YouTube MySQL scaling challenges.

- What is Vitess?
  - URL: https://vitess.io/docs/24.0/overview/whatisvitess/
  - Use for: SQL vs NoSQL tradeoff discussion.
  - Look for: MySQL compatibility, sharding, query routing, connection pooling, and why scalable SQL can be viable.

### Video processing / transcoding

- YouTube Blog: Reimagining video infrastructure to empower YouTube
  - URL: https://blog.youtube/inside-youtube/new-era-video-infrastructure/
  - Use for: public grounding on YouTube video infrastructure and VCU.
  - Look for: transcoding, video infrastructure, quality/efficiency motivation.

- Google Research: Warehouse-Scale Video Acceleration: Co-design and Deployment in the Wild
  - URL: https://research.google/pubs/warehouse-scale-video-acceleration-co-design-and-deployment-in-the-wild/
  - Use for: deeper grounding on warehouse-scale transcoding and accelerator tradeoffs.
  - Look for: video processing as a warehouse-scale workload, accelerator design, deployment, throughput/cost/efficiency tradeoffs.

## Optional coverage/checklist references

These may be used only as coverage checklists, not as source prose or structure:

- Alex Xu system design material
- Grokking the System Design Interview
- common YouTube system-design interview questions
- cloud provider architecture docs for generic building blocks such as object storage, queues, CDN, stream processing, search, and NoSQL databases

## Source-use rules

- Do not claim to describe YouTube's actual internal architecture unless a public source supports the claim.
- For inferred choices, use phrasing such as:
  - "A YouTube-like system could..."
  - "One plausible design is..."
  - "For an interview design, we can choose..."
- Use sources to ground constraints and real-world examples.
- Design from first principles for the article.
- Do not copy diagrams or prose from any source.
