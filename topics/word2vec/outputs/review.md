# Phase 05 Code Demo Notes

## Included

- `outputs/code/toy_context_pairs.py`
  - Purpose: show how a toy sentence becomes CBOW and Skip-gram training examples.
  - Dependency status: Python standard library only.
  - Lesson fit: supports the context-window, CBOW, and Skip-gram sections.

- `outputs/code/analogy_demo.py`
  - Purpose: show cosine similarity and analogy-style vector arithmetic with hand-made vectors.
  - Dependency status: Python standard library only.
  - Lesson fit: supports the analogy evaluation section without pretending to train real Word2Vec vectors.

## Skipped

- `outputs/code/tiny_skipgram_training.py`
  - Status: skipped.
  - Rationale: a tiny trainer would either require more implementation detail than this beginner lesson needs or risk suggesting that a toy corpus can reproduce the paper's large-scale behavior. The current lesson is better served by separating the two ideas: generating prediction examples and evaluating vectors with cosine similarity.

## Cautions for Later Review

- Do not present hand-made vectors as paper vectors.
- Do not imply these scripts reproduce the paper's reported accuracy.
- Keep code blocks near the relevant lesson explanations and introduce the intuition before showing code.
