# GloVe Glossary

- `AdaGrad`: optimization method used by the paper to update model parameters during training.
- `analogy task`: benchmark where the model answers questions of the form `a is to b as c is to ?`.
- `asymmetric context window`: context window that looks only to one side of the target word.
- `bias`: extra scalar parameter for a target or context word that helps account for broad frequency effects.
- `CBOW`: continuous bag-of-words model; predicts a word from its context.
- `co-occurrence`: event where a word appears within another word's context window.
- `co-occurrence matrix`: table `X` whose entry `X_ij` stores how often context word `j` appears near target word `i`.
- `context vector`: vector `wtilde_j` for a word when it is used in the context role.
- `context window`: span of nearby words counted around a target word.
- `cosine similarity`: measure of vector direction similarity used by the paper for analogy answers.
- `dot product`: operation turning two vectors into one scalar score; in GloVe it contributes to the predicted log co-occurrence count.
- `GloVe`: Global Vectors; the paper's global log-bilinear regression model for word representation.
- `global statistics`: aggregate counts collected over the corpus, rather than individual local windows considered one at a time.
- `HPCA`: Hellinger PCA, a matrix-factorization-related baseline discussed in the paper.
- `LSA`: latent semantic analysis, a matrix factorization method using term-document matrices.
- `NER`: named entity recognition, a task of identifying entities such as persons, locations, and organizations.
- `nonzero entry`: a co-occurrence matrix cell with count greater than zero.
- `PPMI`: positive pointwise mutual information, a co-occurrence transformation discussed in related work.
- `semantic analogy`: analogy involving meaning-like relations, often people or places in the paper's examples.
- `skip-gram`: local context-window model that predicts context from a word.
- `softmax`: normalized exponential function used in prediction models to produce probabilities over vocabulary items.
- `Spearman rank correlation`: rank-based correlation used to compare model similarity scores with human similarity judgments.
- `symmetric context window`: context window that looks both left and right of the target word.
- `syntactic analogy`: analogy involving grammatical form, such as tense or adjective form.
- `term-document matrix`: matrix whose rows are words/terms and columns are documents.
- `term-term matrix`: matrix whose rows and columns are both words/terms.
- `weighted least squares`: objective that penalizes squared prediction errors, with each error multiplied by a weight.
- `word vector`: vector `w_i` for a word when it is used in the target role.
- `x_max`: cutoff in the GloVe weighting function, set to 100 in the paper's experiments.
- `alpha`: exponent in the GloVe weighting function, set to 3/4 in the paper's experiments.

## Symbol Glossary

- `V`: vocabulary size.
- `C`: corpus; `|C|` is corpus size.
- `X`: word-word co-occurrence matrix.
- `X_ij`: count of word `j` appearing in the context of word `i`.
- `X_i`: sum of co-occurrence counts in row `i`, `sum_k X_ik`.
- `P_ij`: conditional probability `P(j | i) = X_ij / X_i`.
- `w_i`: target-word vector for word `i`.
- `w_j`: target-word vector for word `j`.
- `wtilde_k`: context-word vector for word `k`.
- `b_i`: target-word bias.
- `btilde_j`: context-word bias.
- `F`: function used in the derivation to connect vectors to probability ratios.
- `f(x)`: weighting function applied to co-occurrence count `x`.
- `J`: objective/cost function minimized during training.
