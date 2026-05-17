# Teaching Plan Notes

## Reader Prerequisite Ladder

Before the final article uses the GloVe objective, it should introduce:

1. Corpus and token.
2. Context window.
3. Co-occurrence count.
4. Co-occurrence matrix.
5. Conditional probability.
6. Ratio.
7. Vector.
8. Dot product.
9. Bias term.
10. Log count.
11. Squared error.
12. Weighting function.

## Likely Reader Confusions

- "Global" may sound like the model sees the whole corpus at once. Clarify that the corpus is summarized into co-occurrence counts.
- "Local window" may sound less statistical. Clarify that window methods also accumulate learning signals from many contexts.
- `X_ij` and `P_ij` can blur together. Keep count and probability examples separate.
- Word vectors and context vectors can look redundant. Explain target role versus context role.
- The weighting function can look arbitrary. Explain the problem it solves before its formula.
- Analogies can be overinterpreted. Keep benchmark meaning modest.
- `W + Wtilde` can seem like a trick. Explain it as combining two trained views of each word.

## Visual Opportunities

- Corpus to windows to co-occurrence matrix:
  - One short sentence with a highlighted target word and neighboring context words.
  - A small matrix showing counts.
- Ice/steam ratio table:
  - Use the source's `solid`, `gas`, `water`, and `fashion` contrast.
  - Caption: ratios separate discriminative contexts from shared or irrelevant contexts.
- Objective anatomy:
  - Show observed count, log target, vector dot product plus biases, error, square, and weight.
- Weighting function:
  - Qualitative curve: rare counts low weight, medium counts rising, high counts capped.
- Training workflow:
  - Corpus -> co-occurrence matrix -> sampled nonzero pair -> parameter update -> final vectors.
- Evaluation map:
  - Analogy, similarity, and NER as three different probes.

## Toy-to-Real Bridges

- Toy corpus:
  - "ice is solid water"
  - "steam is hot gas"
  - "water can be ice"
- Use it only to show mechanics, not to produce meaningful embeddings.
- Real paper-scale bridge:
  - The paper uses billions of tokens and hundreds of thousands to millions of vocabulary entries.

## Section Planning Recommendation

Use an adapted paper-deep-dive structure. It should preserve every major paper section but teach prerequisites before the densest derivation.

Recommended future sections:

1. Why word-vector arithmetic needed an explanation.
2. The older choices: global counts and local windows.
3. The ice/steam ratio insight.
4. Deriving the GloVe objective.
5. What training actually changes.
6. How the paper evaluates GloVe.
7. Model analysis: dimensions, windows, corpora, runtime, word2vec comparison.
8. What the paper proves, what it does not prove, and how GloVe is used.

## Acceptance Criteria for Later Prose

- Every formula has symbols, plain-English reading, and at least one tiny example where useful.
- Every visual has one teaching purpose and one caption.
- Every result claim is tied to "the paper reports" or "in this setup."
- No section says "the model learns" without naming the parameters that change.
- No exact chart values are invented from figures.
