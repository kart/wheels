# Mechanism Notes

## The Problem the Model Is Solving

Source claim:
- The paper wants a word-vector model that uses global corpus co-occurrence statistics while producing vector spaces with useful linear substructure.

Teaching interpretation:
- The training signal is not a human label. It is the co-occurrence table extracted from text.
- The model changes vectors and biases until their scores match observed log co-occurrence counts.

## Notation

- `V`: vocabulary size.
- `X`: word-word co-occurrence matrix.
- `X_ij`: count of context word `j` near target word `i`.
- `X_i`: total number of context-word counts around target word `i`, `sum_k X_ik`.
- `P_ij`: conditional probability `P(j | i) = X_ij / X_i`.
- `w_i`: target-word vector for word `i`.
- `wtilde_j`: context-word vector for word `j`.
- `b_i`: target-word bias.
- `btilde_j`: context-word bias.
- `f(X_ij)`: weighting function for a count.
- `J`: total training objective to minimize.

## Why Ratios

Source claim:
- The paper argues that `P_ik / P_jk` is better than raw probabilities for isolating what distinguishes two words.

Plain-English reading:
- Compare two target words, `i` and `j`, against the same probe context `k`.
- If the ratio is high, `k` is more characteristic of `i`.
- If the ratio is low, `k` is more characteristic of `j`.
- If the ratio is near 1, `k` does not distinguish them.

Tiny example:
- Suppose `P(solid | ice) = 0.0019`.
- Suppose `P(solid | steam) = 0.00022`.
- The ratio is about `0.0019 / 0.00022 = 8.6`.
- So `solid` is much more diagnostic for `ice` than for `steam`.

## From Ratios to Vector Differences

Source claim:
- The paper wants a function `F` that maps word vectors to the probability ratio.

Teaching interpretation:
- If analogies are represented by vector offsets, then the difference between two word vectors should carry information about what distinguishes them.
- That is why the paper moves from `F(w_i, w_j, wtilde_k)` to a function involving `w_i - w_j`.

## Why Dot Products

Source claim:
- The right-hand side of the ratio equation is a scalar, while the model arguments are vectors.
- The paper uses a dot product to produce a scalar.

Plain-English reading:
- The dot product scores how compatible a target-word difference is with a context word.

## Why Logs Appear

Source claim:
- With the chosen homomorphism, `F = exp`, leading to a log relation:
  - `w_i^T wtilde_k = log(P_ik) = log(X_ik) - log(X_i)`

Teaching interpretation:
- Ratios multiply and divide.
- Vector differences add and subtract.
- Logs turn multiplication/division into addition/subtraction, making the algebra fit vector-space operations.

## Why Biases Appear

Source claim:
- `log(X_i)` is independent of context word `k`, so it can be absorbed into a bias for target word `i`.
- A context bias restores symmetry.

Plain-English reading:
- Biases let the model handle broad word-frequency effects separately from the semantic/syntactic dimensions in the vectors.

## The Core Matching Equation

Source claim:
- The paper reaches:

```text
w_i^T wtilde_j + b_i + btilde_j = log(X_ij)
```

Symbols:
- `w_i^T wtilde_j`: compatibility score between target word `i` and context word `j`.
- `b_i`: target-word bias.
- `btilde_j`: context-word bias.
- `log(X_ij)`: compressed observed co-occurrence count.

Plain-English reading:
- The model should predict the log count of a word-context pair from their vectors and biases.

## The Training Objective

Source claim:
- The GloVe objective is:

```text
J = sum_{i,j=1}^V f(X_ij) (w_i^T wtilde_j + b_i + btilde_j - log X_ij)^2
```

Plain-English reading:
- For every observed word-context pair, compare the model's predicted log count to the true log count.
- Square the error so larger misses hurt more.
- Multiply by a weight so not every pair matters equally.
- Add all weighted errors.

What changes during training:
- `w_i`
- `wtilde_j`
- `b_i`
- `btilde_j`

What does not change during training:
- the corpus
- the co-occurrence counts `X_ij`
- the target log counts

Tiny one-term example:
- Observed count: `X_ij = 20`
- Target: `log(20) ~= 3.00`
- Current dot-plus-bias prediction: `2.50`
- Error: `2.50 - 3.00 = -0.50`
- Squared error: `0.25`
- If `f(20) ~= 0.30`, this pair contributes about `0.075` to `J`.

## Weighting Function

Source claim:
- The paper uses:

```text
f(x) = (x / x_max)^alpha, if x < x_max
f(x) = 1, otherwise
```

with `x_max = 100` and `alpha = 3/4` in experiments.

Plain-English reading:
- Below the cutoff, larger counts get more trust.
- At and above the cutoff, counts stop gaining extra influence.

Tiny example with `x_max = 100`, `alpha = 3/4`:
- Count `1`: weight `1 / 100` to the `3/4` power, about `0.032`.
- Count `10`: weight `10 / 100` to the `3/4` power, about `0.178`.
- Count `100`: weight `1`.
- Count `1000`: capped at `1`.

## Training Workflow

Source-grounded steps:
1. Tokenize and lowercase the corpus.
2. Choose a vocabulary.
3. Slide a context window across the corpus.
4. Build a word-word co-occurrence matrix `X`, with distance weighting `1/d`.
5. Initialize word vectors, context vectors, and biases.
6. Sample nonzero entries of `X`.
7. Use AdaGrad to adjust parameters and reduce the weighted squared error.
8. Use `W + Wtilde` as final vectors.

Teaching caveat:
- This workflow is paper-scale. A toy code demo should only illustrate the mechanics on a tiny corpus.
