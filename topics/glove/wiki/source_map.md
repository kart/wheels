# GloVe Source Map

## Source Inventory

- Topic: `glove`
- Primary source: `topics/glove/raw/papers/glove.pdf`
- Paper title: "GloVe: Global Vectors for Word Representation"
- Authors: Jeffrey Pennington, Richard Socher, Christopher D. Manning
- PDF metadata: 12 pages, created by TeX/pdfTeX, not encrypted
- Text extraction status: usable with `pdftotext -layout`
- Article shape: `paper_deep_dive`
- Audience profile: `beginner_technical`

## Paper-Level Claim Boundary

Claims below are source-grounded notes from the paper unless marked as "teaching interpretation."

The paper presents GloVe as a global log-bilinear regression model for unsupervised word representation learning. It argues that useful linear structure in word vectors can be motivated from ratios of word-word co-occurrence probabilities, and it trains on nonzero entries of a word-word co-occurrence matrix. The abstract reports 75% on a word analogy task and says the model also outperforms related models on similarity tasks and named entity recognition.

## Section Map

### Abstract

Source coverage:
- States the problem: recent word-vector methods capture semantic and syntactic regularities, but the origin of those regularities had remained opaque.
- Frames GloVe as combining advantages of global matrix factorization and local context-window methods.
- Claims efficient use of corpus statistics by training on nonzero co-occurrence matrix entries.
- Reports 75% performance on a word analogy task and stronger performance on similarity and NER tasks.

Later teaching needs:
- Explain "nonzero co-occurrence entries" before using it.
- Avoid presenting 75% as timeless state of the art; it is the paper's reported result.

### 1 Introduction

Source coverage:
- Motivates semantic vector space models for applications such as information retrieval, document classification, question answering, NER, and parsing.
- Contrasts pairwise distance/angle evaluation with analogy evaluation.
- Uses the analogy idea that "king - queen = man - woman" should hold as a vector relationship.
- Identifies two model families:
  - global matrix factorization methods such as LSA
  - local context-window methods such as skip-gram
- States the paper's diagnosis:
  - LSA-like methods use global statistics but do poorly on analogies.
  - Skip-gram-like methods can do well on analogies but do not operate directly on global co-occurrence counts.
- States the proposed direction: a weighted least-squares model over global word-word co-occurrence counts.

Later teaching needs:
- Start with a concrete word-context example before analogies.
- Explain that analogies are an evaluation probe, not proof of human-like understanding.

### 2 Related Work

Source coverage:
- Matrix factorization methods:
  - LSA uses term-document matrices.
  - HAL and similar methods use term-term matrices.
  - Frequent function words can dominate raw co-occurrence similarity.
  - COALS, PPMI, and HPCA are discussed as transformations or normalizations of co-occurrence statistics.
- Shallow window-based methods:
  - Neural language model lineage from Bengio et al.
  - Collobert and Weston decouple word-vector training from downstream tasks.
  - Skip-gram and CBOW use simple single-layer architectures with inner products.
  - vLBL and ivLBL are related log-bilinear models.
  - Skip-gram and ivLBL predict context from word; CBOW and vLBL predict word from context.
  - The paper argues window-based methods scan local windows and do not directly exploit repeated global co-occurrence counts.

Later teaching needs:
- Explain "global" as reusing aggregate counts.
- Explain "local window" as repeated examples from sliding windows.
- Avoid implying the paper proves all count-based methods always beat all prediction-based methods.

### 3 The GloVe Model

Source coverage:
- Defines the word-word co-occurrence matrix `X`.
- Defines `X_ij` as the number of times word `j` occurs in the context of word `i`.
- Defines `X_i = sum_k X_ik`.
- Defines `P_ij = P(j | i) = X_ij / X_i`.
- Uses the ice/steam example to argue that ratios of co-occurrence probabilities isolate meaning-relevant contrasts better than raw probabilities.
- Proposes a model family where a function `F` encodes the ratio `P_ik / P_jk`.
- Narrows the model using vector differences, a dot product, a homomorphism choice that leads to exponentiation, and symmetry between word and context roles.
- Arrives at:
  - `w_i^T wtilde_k + b_i + btilde_k = log(X_ik)`
- Notes that log zero is undefined and motivates a weighted least-squares objective over observed counts:
  - `J = sum_{i,j=1}^V f(X_ij) (w_i^T wtilde_j + b_i + btilde_j - log X_ij)^2`
- Defines desirable properties of the weighting function:
  - zero weight at zero
  - non-decreasing so rare co-occurrences are not overweighted
  - capped or relatively small for large counts so frequent pairs are not overweighted
- Uses:
  - `f(x) = (x / x_max)^alpha` if `x < x_max`
  - `f(x) = 1` otherwise
- Reports `x_max = 100` and `alpha = 3/4` for experiments.

Figures/tables:
- Table 1: ice/steam co-occurrence probabilities and ratios for `solid`, `gas`, `water`, `fashion`.
- Figure 1: weighting function `f` with `alpha = 3/4`.

Later teaching needs:
- This is the conceptual center of the article.
- Explain every symbol before formula use.
- Use a tiny numerical example for a single loss term.
- Show why biases absorb row/context frequency effects.

### 3.1 Relationship to Other Models

Source coverage:
- Starts from a softmax model `Q_ij` for the probability that word `j` appears in context of word `i`.
- Groups local-window training terms by co-occurrence pair to express an implied global objective.
- Discusses cross-entropy as one distance measure between empirical and model distributions.
- Critiques cross-entropy/softmax normalization for long-tailed distributions and computational cost.
- Motivates an unnormalized least-squares objective that becomes equivalent to the GloVe-style cost function when generalized with a weighting function.

Later teaching needs:
- Treat this as optional deepening unless the section plan needs full paper-section fidelity.
- Explain that the paper is connecting window-based objectives to count objectives, not simply dismissing window methods.

### 3.2 Complexity of the Model

Source coverage:
- Complexity depends on the number of nonzero entries in `X`.
- Worst case is no worse than `O(|V|^2)`.
- The paper argues the nonzero count is much smaller in practice.
- Uses a rank-frequency style assumption and harmonic-number expansion.
- Reports observed modeling of `X_ij` with exponent `alpha = 1.25` for corpora studied.
- Concludes complexity is much better than the worst case and somewhat better than online window-based methods scaling like `O(|C|)`.

Later teaching needs:
- For beginner readers, this can be simplified to "train only where a pair was observed," with the asymptotic argument as a caveat box.
- Do not overemphasize the zeta-function derivation unless needed.

### 4 Experiments

Source coverage:
- Evaluates on:
  - word analogy task from Mikolov et al.
  - word similarity tasks described in Luong et al.
  - CoNLL-2003 shared NER benchmark

### 4.1 Evaluation Methods

Source coverage:
- Word analogies:
  - Dataset has 19,544 questions.
  - Split into semantic and syntactic subsets.
  - Example semantic form: "Athens is to Greece as Berlin is to ?"
  - Example syntactic form: "dance is to dancing as fly is to ?"
  - Answer found by nearest vector to `w_b - w_a + w_c` by cosine similarity.
- Word similarity:
  - Evaluates on WordSim-353, MC, RG, SCWS, and RW.
  - Uses Spearman rank correlation between vector-derived similarity and human judgments.
- Named entity recognition:
  - Uses CoNLL-2003 English benchmark and tests on CoNLL-03, ACE, and MUC7.
  - Adds 50-dimensional vectors for each word in a five-word context as continuous features in a CRF setup.

Figures/tables:
- Table 2: word analogy accuracy by model, vector dimension, corpus size, semantic, syntactic, overall.
- Table 3: Spearman rank correlation on word similarity tasks.
- Table 4: F1 score on NER tasks.

Later teaching needs:
- Explain each benchmark type by what it asks the vector space to do.
- Keep benchmark caveats visible.

### 4.2 Corpora and Training Details

Source coverage:
- Trains on five corpora:
  - Wikipedia 2010, 1B tokens
  - Wikipedia 2014, 1.6B tokens
  - Gigaword 5, 4.3B tokens
  - Gigaword 5 + Wikipedia 2014, 6B tokens
  - Common Crawl, 42B tokens
- Mentions an additional 840B-token web corpus for scalability but says results are not directly comparable because the vocabulary was not lowercased.
- Tokenizes and lowercases with Stanford tokenizer.
- Builds a 400,000-word vocabulary, except Common Crawl uses about 2 million words.
- Uses distance weighting in the co-occurrence matrix so pairs `d` words apart contribute `1/d`.
- Sets `x_max = 100`, `alpha = 3/4`.
- Trains with AdaGrad, stochastic sampling of nonzero `X` entries, initial learning rate 0.05.
- Runs 50 iterations for vectors smaller than 300 dimensions and 100 otherwise.
- Default context is 10 words left and right.
- Produces two vector sets, `W` and `Wtilde`, and uses `W + Wtilde` as final word vectors.

Later teaching needs:
- Explain what changes during training: word vectors, context vectors, and biases are adjusted to reduce weighted squared error on observed co-occurrence pairs.

### 4.3 Results

Source coverage:
- Table 2 reports GloVe outperforming listed baselines on word analogies, including 75.0 overall for 300-dimensional vectors trained on 42B tokens.
- The paper notes its word2vec-tool results are stronger than many previously published results due to choices such as negative sampling, number of negative samples, and corpus.
- Table 3 reports GloVe outperforming listed models on most word similarity datasets and outperforming CBOW vectors trained on a larger 100B-word news corpus while using a corpus less than half the size.
- Table 4 reports NER results where GloVe has the highest values in Dev, ACE, and MUC7; HPCA is slightly higher on the CoNLL test set.

Later teaching needs:
- Say "in the paper's experimental setup" for result comparisons.
- Avoid flattening all tasks into one score.

### 4.4 Model Analysis: Vector Length and Context Size

Source coverage:
- Figure 2 studies analogy accuracy by vector dimension and window size/type.
- Reports diminishing returns above about 200 dimensions.
- Reports syntactic performance is better for small and asymmetric context windows.
- Reports semantic information is more often non-local and better captured with larger windows.

Later teaching needs:
- Explain symmetric versus asymmetric context windows.
- Use a qualitative summary rather than recreating exact plotted curves unless visually verified.

### 4.5 Model Analysis: Corpus Size

Source coverage:
- Figure 3 studies analogy accuracy for 300-dimensional vectors across corpora.
- Syntactic subtask improves monotonically with corpus size.
- Semantic subtask does not; smaller Wikipedia corpora can beat larger Gigaword corpora.
- Paper suggests this may be due to city/country analogies and Wikipedia's coverage of locations, plus Wikipedia updates versus fixed news repositories.

Later teaching needs:
- Emphasize that more data is not automatically better for every benchmark.

### 4.6 Model Analysis: Run-time

Source coverage:
- Runtime is split between populating `X` and training.
- On a dual 2.1GHz Intel Xeon E5-2658 machine:
  - populating `X` with 10-word symmetric context, 400,000 vocabulary, and 6B-token corpus takes about 85 minutes on a single thread
  - one training iteration for 300-dimensional vectors using all 32 cores takes 14 minutes

Later teaching needs:
- Separate preprocessing cost from training cost.

### 4.7 Model Analysis: Comparison with word2vec

Source coverage:
- Notes that rigorous quantitative comparison with word2vec is complicated by many sensitive parameters.
- Controls vector length, context window, corpus, and vocabulary size.
- Varies training iterations for GloVe and negative samples for word2vec as a training-time comparison.
- Figure 4 compares GloVe with CBOW and skip-gram on overall analogy accuracy as a function of training time.
- Reports GloVe consistently outperforms word2vec under the controlled setup, achieves better results faster, and has the best results irrespective of speed.
- Notes word2vec performance can decrease beyond about 10 negative samples, with a proposed explanation about negative sampling approximation quality.

Later teaching needs:
- Keep the paper's own caveat about comparison difficulty.
- Do not generalize this 2014 comparison to all later embedding methods.

### 5 Conclusion

Source coverage:
- Restates the count-based versus prediction-based question.
- Argues both model classes probe underlying co-occurrence statistics.
- Claims count-based methods can be efficient at capturing global statistics.
- Presents GloVe as using count-data benefits while capturing linear substructures seen in prediction-based methods.
- Concludes GloVe outperforms other models on analogy, similarity, and NER tasks in the paper's setup.

Later teaching needs:
- Close with "what the paper gave us" and "what it does not prove."

## Tables and Figures

- Table 1: co-occurrence probabilities and ratios for `ice` and `steam` with context words `solid`, `gas`, `water`, and `fashion`.
- Figure 1: weighting function `f` with `alpha = 3/4`.
- Table 2: word analogy accuracy comparison across models and corpora.
- Figure 2: analogy accuracy as function of vector dimension and window size/type.
- Table 3: word similarity task Spearman correlations.
- Table 4: NER F1 scores.
- Figure 3: analogy accuracy across corpora.
- Figure 4: GloVe versus CBOW/skip-gram analogy accuracy as function of training time.

## Equation Inventory

- Eq. 1: general function of two target word vectors and a context vector equals `P_ik / P_jk`.
- Eq. 2: restricts dependence to target-vector difference and context vector.
- Eq. 3: uses a dot product so vector arguments produce a scalar relation.
- Eq. 4-6: imposes a homomorphism leading to the exponential/log form.
- Eq. 7: log-count bilinear relation with word and context biases.
- Eq. 8: GloVe weighted least-squares objective.
- Eq. 9: weighting function with cutoff `x_max` and exponent `alpha`.
- Eq. 10-16: relationship to softmax/window-based objectives and an unnormalized least-squares form.
- Eq. 17-22: complexity argument based on rank-frequency assumptions and nonzero co-occurrence entries.

## Evaluation Artifacts

- Analogy benchmark: 19,544 questions, semantic and syntactic subsets.
- Similarity benchmarks: WordSim-353, MC, RG, SCWS, RW.
- NER benchmark: CoNLL-2003 English with CoNLL, ACE, and MUC7 test settings.
- Main corpora: Wikipedia 2010, Wikipedia 2014, Gigaword 5, Gigaword 5 + Wikipedia 2014, Common Crawl.

## Extraction Caveats

- `pdftotext -layout` preserves enough text for source compilation but flattens two-column layout.
- Equations are readable but some superscripts/subscripts and tildes need manual checking against the PDF.
- Figures are not image-extracted by `pdfimages -list`, likely because they are vector drawings/charts; later visuals should be recreated as teaching diagrams, not copied.
- Exact chart curves in Figures 2-4 should not be reproduced numerically unless manually traced or tabular values are available.
- Table 2 appears partially adjacent to surrounding text in extraction and should be checked visually before using exact rows in publish prose.
