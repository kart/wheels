# Visual Plan: Word2Vec

## Phase Status

Status: generated for phase 04.

This plan documents the visual assets created for `outputs/lesson.md`. The visuals prioritize correctness and educational clarity over decoration.

Source grounding:

- `wiki/source_summary.md`
- `wiki/concepts.md`
- `wiki/architecture_notes.md`
- `wiki/results_notes.md`
- `outputs/lesson.md`
- `raw/papers/word2vec.pdf`

Inspection notes:

- Figure 1 was inspected through the readable PDF text extraction. Its caption states that CBOW predicts the current word based on context and Skip-gram predicts surrounding words given the current word. The architecture visuals preserve that direction.
- Relevant tables were inspected through extracted text before creating the qualitative comparison and evaluation visuals. No exact numeric chart was generated except labels copied from sourced lesson/wiki content.
- Phase 06 integrated these visual assets into `outputs/preview.html`. The preview should be rechecked after any future visual, lesson, or code changes.

## Visual Assets

| ID | Path | Status | Lesson placement | Purpose | Caption |
| --- | --- | --- | --- | --- | --- |
| `one_hot_vs_dense` | `outputs/visuals/one_hot_vs_dense.svg` | generated | Section 1, after the one-hot table | Contrast sparse identity-only vectors with dense learned vectors. | One-hot vectors identify words with separate slots. Dense word vectors can represent graded relationships learned from context. |
| `context_window` | `outputs/visuals/context_window.svg` | generated | Section 2, beside the sentence example | Show center word, context words, and window size. | A context window turns ordinary text into training examples: one center word and nearby context words. |
| `cbow_flow` | `outputs/visuals/cbow_flow.svg` | generated | Section 3, near the CBOW prediction-direction line | Redraw CBOW architecture with correct prediction direction. | CBOW uses surrounding context words to predict the current word. Direction must not be reversed. |
| `skipgram_flow` | `outputs/visuals/skipgram_flow.svg` | generated | Section 4, near the Skip-gram prediction-direction line | Redraw Skip-gram architecture with correct prediction direction. | Skip-gram uses one current word to predict several surrounding words. Direction must not be reversed. |
| `hierarchical_softmax_tree` | `outputs/visuals/hierarchical_softmax_tree.svg` | generated | Section 5, after the vocabulary-size bottleneck explanation | Explain hierarchical softmax as a path through a binary tree. | Hierarchical softmax turns a large vocabulary prediction into a path through a binary tree. |
| `complexity_comparison` | `outputs/visuals/complexity_comparison.svg` | generated | Section 5, after the speed/scaling explanation | Qualitatively compare where model training cost comes from. | Qualitative comparison of the paper's efficiency story; this is not an exact numeric chart. |
| `analogy_vector_offset` | `outputs/visuals/analogy_vector_offset.svg` | generated | Section 6, beside analogy examples | Explain vector offset intuition for analogy-style evaluation. | Analogy questions test whether relationship directions in vector space can transfer from one word pair to another. |
| `evaluation_pipeline` | `outputs/visuals/evaluation_pipeline.svg` | generated | Section 6, after exact-match scoring explanation | Show the analogy evaluation pipeline from question to score. | Evaluation pipeline: analogy question, vector expression, nearest-neighbor search, exact-match score. |

## Correctness Checks

CBOW:

- Visual path: `outputs/visuals/cbow_flow.svg`
- Source grounding: Figure 1 caption and `wiki/architecture_notes.md`
- Direction shown: context words `w(t-2)`, `w(t-1)`, `w(t+1)`, `w(t+2)` flow into shared projection/sum and then to output `w(t)`.
- Status: generated

Skip-gram:

- Visual path: `outputs/visuals/skipgram_flow.svg`
- Source grounding: Figure 1 caption and `wiki/architecture_notes.md`
- Direction shown: current word `w(t)` flows through projection and then outward to context predictions `w(t-2)`, `w(t-1)`, `w(t+1)`, `w(t+2)`.
- Status: generated

Complexity comparison:

- Visual path: `outputs/visuals/complexity_comparison.svg`
- Type: qualitative chart
- Numeric caution: bar lengths are explanatory only and are labeled as qualitative. The visual does not invent exact numeric values.
- Source grounding: paper complexity discussion summarized in `wiki/architecture_notes.md`.
- Status: generated

Analogy visuals:

- Visual paths: `outputs/visuals/analogy_vector_offset.svg`, `outputs/visuals/evaluation_pipeline.svg`
- Source grounding: paper analogy examples and exact-match evaluation summarized in `wiki/results_notes.md`.
- Caution included: analogy geometry is illustrative and not actual paper vector coordinates.
- Status: generated

## Needs Review

All visuals are generated, but these items should be reviewed in the later reviewer phase:

- Confirm that text remains readable in browser previews at common desktop and mobile widths.
- Confirm that the CBOW and Skip-gram arrows remain unambiguous after HTML scaling.
- Confirm that qualitative visuals are not mistaken for exact paper measurements.
- Confirm that the illustrative dense-vector and analogy coordinates are understood as illustrative, not paper data.
