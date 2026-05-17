# Paper Walkthrough Notes

## Abstract

Source claims:
- The paper says recent word-vector methods can capture fine-grained semantic and syntactic regularities through vector arithmetic, but the source of those regularities was unclear.
- It proposes a global log-bilinear regression model.
- It says the model combines strengths of global matrix factorization and local context-window methods.
- It trains on nonzero elements of a word-word co-occurrence matrix.
- It reports 75% on a word analogy task and stronger performance than related models on similarity tasks and NER.

Teaching interpretation:
- The abstract sets up a mechanism question: why should arithmetic on word vectors work at all?
- The final article should make the model feel like a response to that question, not just a new objective function.

## 1 Introduction

Source claims:
- Semantic vector-space models represent each word with a real-valued vector.
- Such vectors can support information retrieval, document classification, question answering, NER, and parsing.
- Traditional intrinsic evaluation often looks at distance or angle between word-vector pairs.
- Mikolov et al.'s analogy evaluation probes finer vector-space structure through vector differences.
- The paper gives the example `king - queen = man - woman`.
- The introduction identifies two major families:
  - global matrix factorization, such as LSA
  - local context-window methods, such as skip-gram
- The paper's stated critique:
  - LSA-like methods use global statistics but underperform on analogies.
  - Skip-gram-like methods can do better on analogies but do not directly operate on global co-occurrence counts.
- The proposed model is a weighted least-squares model over global word-word co-occurrence counts.

Teaching interpretation:
- A beginner needs "global" and "local" anchored in a corpus example.
- The analogy example should be introduced as an evaluation signal for vector-space structure, not as proof of meaning.

## 2 Related Work

Source claims:
- Matrix factorization methods have roots in LSA.
- LSA uses term-document matrices.
- HAL uses term-term matrices, where rows and columns correspond to words and entries are context co-occurrence counts.
- Frequent words can dominate raw co-occurrence similarity without contributing much semantic relatedness.
- COALS, PPMI, and HPCA are discussed as transformations that address raw-count problems.
- Shallow window-based methods learn word representations through local prediction tasks.
- The paper connects Bengio et al., Collobert and Weston, skip-gram, CBOW, vLBL, and ivLBL.
- Skip-gram and ivLBL predict context from word; CBOW and vLBL predict word from context.
- The paper argues window-based models do not directly use aggregate co-occurrence counts and therefore do not exploit repeated statistics as efficiently.

Teaching interpretation:
- The useful contrast is not "old bad, new good." It is:
  - count methods see the whole count table but may not shape vectors well for analogies
  - window prediction methods shape vectors well but process many repeated local examples
  - GloVe tries to preserve both global counts and linear vector structure

## 3 The GloVe Model

Source claims:
- All unsupervised word-vector methods ultimately rely on word occurrence statistics.
- The paper defines:
  - `X`: word-word co-occurrence matrix
  - `X_ij`: number of times word `j` appears in the context of word `i`
  - `X_i = sum_k X_ik`: total context occurrences for word `i`
  - `P_ij = P(j | i) = X_ij / X_i`
- The paper uses `ice` and `steam` to show that ratios of probabilities can distinguish relevant context words better than raw probabilities.
- For `solid`, `P(solid | ice) / P(solid | steam)` is large.
- For `gas`, the ratio is small.
- For `water` and `fashion`, the ratio is close to one.
- The paper argues the appropriate starting point should be ratios of co-occurrence probabilities.
- The most general first model uses a function `F(w_i, w_j, wtilde_k) = P_ik / P_jk`.
- The paper then imposes desiderata:
  - encode the ratio in vector differences
  - use a dot product to keep the scalar/vector relationship simple
  - preserve symmetry between word and context roles
- These choices lead to a log-count relationship with biases:
  - `w_i^T wtilde_k + b_i + btilde_k = log(X_ik)`
- Because log zero is undefined and rare co-occurrences are noisy, the final objective is weighted:
  - `J = sum f(X_ij) (w_i^T wtilde_j + b_i + btilde_j - log X_ij)^2`
- The weighting function should:
  - give zero weight to zero counts
  - not overweight rare co-occurrences
  - not overweight very frequent co-occurrences
- The paper uses `x_max = 100` and `alpha = 3/4`.

Teaching interpretation:
- The derivation can be taught as a series of constraints:
  - "What should vectors preserve?"
  - "How can a vector difference become a scalar comparison?"
  - "Why do logs turn ratios into differences?"
  - "Why do biases absorb broad frequency effects?"
  - "Why should rare pairs count less?"

## 3.1 Relationship to Other Models

Source claims:
- The paper starts from a softmax probability `Q_ij` for context word `j` given word `i`.
- It writes the objective for skip-gram/ivLBL-like methods as the sum of log probabilities over corpus windows.
- By grouping identical word-context pairs, the paper rewrites the objective in terms of the co-occurrence matrix `X`.
- It interprets the grouped objective as a weighted sum of cross-entropies.
- It criticizes cross-entropy and softmax normalization as potentially costly or undesirable for long-tailed distributions.
- It then motivates a least-squares objective on unnormalized log quantities, leading to an objective equivalent to the GloVe cost.

Teaching interpretation:
- This section is a bridge: the paper is saying local-window objectives also imply global co-occurrence statistics when grouped.
- It is useful for explaining why GloVe is not a totally separate universe from prediction models.

## 3.2 Complexity

Source claims:
- GloVe's cost depends on the number of nonzero elements in `X`.
- It scales no worse than `O(|V|^2)`, but the paper argues this worst case is loose.
- The paper assumes word co-occurrences follow a power-law-like pattern and derives a tighter practical relation to corpus size.
- For the corpora studied, the paper observes an exponent near `1.25` and concludes the number of nonzero co-occurrences grows like `O(|C|^0.8)`.
- The paper concludes this is better than the worst case and somewhat better than online window methods that scale like `O(|C|)`.

Teaching interpretation:
- The main beginner takeaway: GloVe does not train on every possible word pair. It trains where the co-occurrence count is nonzero.
- The asymptotic details can be a small sidebar.

## 4 Experiments

Source claims:
- The paper evaluates on word analogies, word similarity datasets, and NER.

## 4.1 Evaluation Methods

Source claims:
- The analogy dataset contains 19,544 questions.
- It has semantic and syntactic subsets.
- The model answers `a is to b as c is to ?` by finding `d` closest to `w_b - w_a + w_c` under cosine similarity.
- Similarity evaluations include WordSim-353, MC, RG, SCWS, and RW.
- Similarity is scored with Spearman rank correlation against human judgments.
- NER uses CoNLL-2003 English and tests on CoNLL-03, ACE, and MUC7.
- The NER setup adds 50-dimensional word vectors as continuous features to a CRF with discrete features.

Teaching interpretation:
- Each evaluation probes a different behavior:
  - analogy: vector offset structure
  - similarity: pairwise similarity alignment with human judgments
  - NER: downstream feature usefulness

## 4.2 Corpora and Training Details

Source claims:
- Corpora include 1B-token Wikipedia 2010, 1.6B-token Wikipedia 2014, 4.3B-token Gigaword 5, 6B-token Gigaword 5 + Wikipedia 2014, and 42B-token Common Crawl.
- The paper mentions an 840B-token web corpus for scalability but says it is not directly comparable.
- It uses Stanford tokenizer, lowercasing, and a 400,000-word vocabulary for most corpora.
- Common Crawl uses about 2 million words.
- Context-window co-occurrences are distance-weighted by `1/d`.
- Experiments use `x_max = 100`, `alpha = 3/4`, AdaGrad, stochastic sampling of nonzero entries, and learning rate 0.05.
- Default context is 10 words to the left and right.
- Final vectors use `W + Wtilde`.

Teaching interpretation:
- Training changes the entries of `W`, `Wtilde`, and the bias terms.
- The observed counts `X_ij` do not change during training; they are the fixed target signal.

## 4.3 Results

Source claims:
- On analogy tasks, GloVe performs better than listed baselines in Table 2, with 75.0 overall for 300-dimensional vectors on 42B tokens.
- The paper states its word2vec-tool results are stronger than some previously published results due to choices such as negative sampling, number of negative samples, and corpus.
- On similarity tasks, Table 3 reports GloVe strong across the listed datasets.
- On NER, Table 4 reports GloVe leading Dev, ACE, and MUC7, while HPCA is slightly higher on the CoNLL test set.

Teaching interpretation:
- The final article should not overfit the narrative to a single table.
- Results should be framed as evidence across intrinsic and downstream tasks.

## 4.4 Vector Length and Context Size

Source claims:
- Figure 2 reports diminishing returns above roughly 200 dimensions.
- Syntactic performance is better with small and asymmetric windows.
- Semantic information is more often non-local and benefits from larger windows.

Teaching interpretation:
- This is a good place to explain why word order and nearby words matter more for syntax.

## 4.5 Corpus Size

Source claims:
- Figure 3 reports syntactic analogy performance improving monotonically with corpus size.
- Semantic analogy performance does not follow the same monotonic pattern.
- The paper suggests Wikipedia may help location-based analogies because it covers many places and is updated.

Teaching interpretation:
- More data can help, but corpus composition matters.

## 4.6 Runtime

Source claims:
- Runtime has two parts: building `X` and training.
- For 6B tokens, 400,000 vocabulary, 10-word symmetric context:
  - building `X` takes about 85 minutes on one thread on the specified machine
  - one 300-dimensional training iteration takes 14 minutes using all 32 cores

Teaching interpretation:
- Distinguish preprocessing from optimization.

## 4.7 Comparison with word2vec

Source claims:
- The paper says rigorous comparison is complicated by parameter sensitivity.
- It controls vector length, context window size, corpus, and vocabulary size.
- It compares GloVe training iterations against CBOW/skip-gram negative samples as a training-time proxy.
- Figure 4 reports GloVe outperforming word2vec under those controlled settings.
- The paper says word2vec performance can decrease beyond about 10 negative samples.

Teaching interpretation:
- Keep the caveat in the same paragraph as the comparison.

## 5 Conclusion

Source claims:
- The paper returns to whether word representations are better learned from count-based or prediction-based methods.
- It argues both classes probe corpus co-occurrence statistics.
- It says count-based methods can be efficient at capturing global statistics.
- It presents GloVe as combining count-data benefits with linear substructures common in prediction-based methods.
- It concludes GloVe outperforms other models on analogy, similarity, and NER in the paper's experiments.

Teaching interpretation:
- The final section should recap mechanism, not just results.
