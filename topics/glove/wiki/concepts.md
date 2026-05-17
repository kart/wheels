# Concepts for Teaching GloVe

## Distributional Meaning

Source grounding:
- The paper assumes word occurrence statistics are the primary information source for unsupervised word-vector learning.

Beginner explanation:
- A word's meaning can be approximated by the company it keeps. If two words appear near similar context words, they may have related meanings or grammatical roles.

Common confusion:
- Similar contexts do not guarantee identical meanings. `ice` and `steam` both appear with `water`, but they contrast on `solid` and `gas`.

## Context Window

Source grounding:
- The paper constructs co-occurrence counts from context windows and usually uses ten words left and ten words right.
- It also discusses symmetric and asymmetric context windows.

Beginner explanation:
- Pick a target word in a corpus. Words nearby are counted as its context. A symmetric window looks both left and right. An asymmetric window can look only to one side.

## Co-occurrence Matrix

Source grounding:
- The paper defines `X` as the word-word co-occurrence matrix.
- `X_ij` is the number of times word `j` appears in the context of word `i`.

Beginner explanation:
- Imagine a large table. Rows are target words, columns are context words, and each cell stores how often that pair was observed.

Tiny example:

If `ice` has context counts:

| context | count |
| --- | ---: |
| solid | 19 |
| gas | 7 |
| water | 300 |

Then the row for `ice` contains those counts in the corresponding columns.

## Conditional Probability

Source grounding:
- The paper defines `P_ij = P(j | i) = X_ij / X_i`.

Beginner explanation:
- `P(j | i)` means: among all context positions around word `i`, what fraction were word `j`?

Tiny example:
- If `ice` has 10,000 total context counts and `solid` appears 19 times around it, then `P(solid | ice) = 19 / 10000 = 0.0019`.

## Probability Ratios

Source grounding:
- Table 1 compares `P(k | ice) / P(k | steam)` for context words.
- The paper argues ratios highlight meaning-relevant contrasts better than raw probabilities.

Beginner explanation:
- A ratio asks, "Is this context word more characteristic of `ice` or of `steam`?"
- A ratio near 1 means the context word does not distinguish the targets.
- A large ratio favors the first target.
- A small ratio favors the second target.

## Word Vectors and Context Vectors

Source grounding:
- The paper uses word vectors `w` and separate context vectors `wtilde`.
- It later uses `W + Wtilde` as final word vectors.

Beginner explanation:
- During training, each word has a vector for when it is the target and another vector for when it appears as context.
- These are both adjustable lists of numbers.
- After training, the paper combines them by adding the two vectors for each word.

## Dot Product

Source grounding:
- The paper uses `w_i^T wtilde_j` in the model.

Beginner explanation:
- A dot product turns two vectors into one score. In GloVe, that score is part of the model's prediction for how strongly a target word and context word co-occur.

Tiny example:
- If `w_i = [2, 1]` and `wtilde_j = [3, 4]`, then the dot product is `2*3 + 1*4 = 10`.

## Bias Terms

Source grounding:
- The paper adds `b_i` and `btilde_j` to restore symmetry and absorb frequency-related terms.

Beginner explanation:
- Some words are common in many contexts. Biases give the model a way to account for broad frequency effects instead of forcing every frequency pattern into the vector dimensions.

## Log Counts

Source grounding:
- The model targets `log(X_ij)` for nonzero counts.

Beginner explanation:
- Counts can span huge ranges. Logs compress them and turn multiplicative relationships into additive ones, which fits vector differences and dot products more naturally.

## Weighted Least Squares

Source grounding:
- GloVe minimizes a weighted squared error between predicted log counts and observed log counts.

Beginner explanation:
- For each observed word-context pair, the model predicts a number. The training penalty is large when the prediction is far from the target log count.
- The weight decides how much that pair should matter.

Tiny example:
- Suppose a pair has target `log(X_ij) = 3.0`.
- The current model predicts `2.4`.
- The error is `2.4 - 3.0 = -0.6`.
- The squared error is `0.36`.
- If the weight is `0.5`, the weighted contribution is `0.18`.

## Weighting Function

Source grounding:
- The paper defines `f(x)` with cutoff `x_max` and exponent `alpha`.
- It uses `x_max = 100` and `alpha = 3/4`.

Beginner explanation:
- Very rare pairs can be noisy.
- Very frequent pairs can dominate.
- The weighting function gives small counts a smaller voice, increases their influence as counts become more reliable, and caps the influence of very frequent pairs.

## Analogy Evaluation

Source grounding:
- The paper uses questions like `a is to b as c is to ?`.
- It answers with the vector closest to `w_b - w_a + w_c` by cosine similarity.

Beginner explanation:
- This benchmark checks whether a relationship appears as a reusable direction in vector space.

Caveat:
- It is a benchmark for vector structure, not a full test of language understanding.
