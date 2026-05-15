# Word2Vec Publish Asset Manifest

Publish target:

- Site repo: `~/karthik.dev`
- Post destination: `~/karthik.dev/_posts/`
- Image destination: `~/karthik.dev/assets/images/`
- Blog image base path: `/assets/images`
- Filename prefix: `word2vec-`

## Publish Drafts

| File | Purpose |
| --- | --- |
| `blog.md` | Jekyll-ready blog post with front matter. |
| `twitter_thread.md` | Concise Twitter/X thread pointing to the full article. |
| `youtube_script.md` | Draft narration outline for a beginner-friendly video. |
| `source_notes.md` | Source fidelity notes and caveats. |
| `asset_manifest.md` | This publication asset inventory. |
| `README.md` | Publish pack overview and local checks. |

## Visual Assets

| Source file | Publish asset | Destination in karthik.dev | Referenced in blog section |
| --- | --- | --- | --- |
| `../visuals/one_hot_vs_dense.svg` | `assets/word2vec-one-hot-vs-dense.svg` | `assets/images/word2vec-one-hot-vs-dense.svg` | The Problem Before the Paper |
| `../visuals/context_window.svg` | `assets/word2vec-context-window.svg` | `assets/images/word2vec-context-window.svg` | A Tiny Example |
| `../visuals/cbow_flow.svg` | `assets/word2vec-cbow-flow.svg` | `assets/images/word2vec-cbow-flow.svg` | CBOW |
| `../visuals/skipgram_flow.svg` | `assets/word2vec-skipgram-flow.svg` | `assets/images/word2vec-skipgram-flow.svg` | Skip-gram |
| `../visuals/complexity_comparison.svg` | `assets/word2vec-complexity-comparison.svg` | `assets/images/word2vec-complexity-comparison.svg` | Why the Paper Cares So Much About Speed |
| `../visuals/hierarchical_softmax_tree.svg` | `assets/word2vec-hierarchical-softmax-tree.svg` | `assets/images/word2vec-hierarchical-softmax-tree.svg` | Why the Paper Cares So Much About Speed |
| `../visuals/analogy_vector_offset.svg` | `assets/word2vec-analogy-vector-offset.svg` | `assets/images/word2vec-analogy-vector-offset.svg` | How the Paper Tests the Vectors |
| `../visuals/evaluation_pipeline.svg` | `assets/word2vec-evaluation-pipeline.svg` | `assets/images/word2vec-evaluation-pipeline.svg` | How the Paper Tests the Vectors |

## Code Assets

The final blog includes small excerpts rather than linking to local code files.

| Source file | Publication use |
| --- | --- |
| `../code/toy_context_pairs.py` | Source for the CBOW/Skip-gram training-example snippet and sample output. |
| `../code/analogy_demo.py` | Source for the analogy-vector mechanics snippet. |

## Local Preview

| File | Purpose |
| --- | --- |
| `../preview.html` | Reader-facing local HTML preview using local copies of the publish assets. |

## Notes

- Do not publish directly without final editorial review.
- Keep all image filenames prefixed with `word2vec-` to avoid collisions in `~/karthik.dev/assets/images/`.
- The visual assets are educational redraws, not copied paper diagrams.
- The complexity visual is qualitative, not an exact numeric chart.

