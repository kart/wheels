# Experiments and Results Notes

## Evaluation Methods

### Word Analogies

Source claims:
- The analogy task has 19,544 questions.
- It has semantic and syntactic subsets.
- The model answers `a is to b as c is to ?` by finding the word vector closest to `w_b - w_a + w_c` using cosine similarity.

Teaching interpretation:
- This evaluates whether relationships are represented as directions in vector space.
- It does not prove that the model understands the words.

### Word Similarity

Source claims:
- Datasets: WordSim-353, MC, RG, SCWS, RW.
- The paper computes vector similarity and compares ranking with human judgments using Spearman rank correlation.

Teaching interpretation:
- Similarity tasks test pairwise closeness, which is different from analogy structure.

### Named Entity Recognition

Source claims:
- Uses CoNLL-2003 English benchmark.
- Tests include CoNLL-03, ACE, and MUC7.
- Adds 50-dimensional word-vector features to a CRF with discrete features.

Teaching interpretation:
- NER is downstream evidence: vectors are useful as features in another model.

## Corpora and Training Details

Source claims:
- Corpora:
  - Wikipedia 2010: 1B tokens
  - Wikipedia 2014: 1.6B tokens
  - Gigaword 5: 4.3B tokens
  - Gigaword 5 + Wikipedia 2014: 6B tokens
  - Common Crawl: 42B tokens
- Additional 840B-token corpus is mentioned for scalability but not directly comparable.
- Vocabulary is usually 400,000 words; Common Crawl uses about 2 million.
- Context window defaults to ten words left and ten words right.
- Distance weighting contributes `1/d` for words `d` positions apart.
- Hyperparameters:
  - `x_max = 100`
  - `alpha = 3/4`
  - AdaGrad
  - initial learning rate `0.05`
  - 50 iterations for vectors under 300 dimensions
  - 100 iterations otherwise
- Final vectors use `W + Wtilde`.

## Main Result Claims

Source claims:
- Table 2: GloVe is strong on word analogies and reports 75.0 overall accuracy for 300-dimensional vectors trained on 42B tokens.
- Table 3: GloVe performs strongly across word similarity datasets.
- Table 4: GloVe has the top reported values for Dev, ACE, and MUC7 NER settings; HPCA is slightly better on the CoNLL test set.

Important caveat:
- Results should be phrased as "in the paper's setup" or "the paper reports."

## Model Analysis

### Vector Length and Context Size

Source claims:
- Diminishing returns appear above about 200 dimensions.
- Smaller/asymmetric windows help syntactic analogy performance.
- Larger windows help semantic information more often because semantic cues may be less local.

Teaching interpretation:
- Syntax often depends on nearby word order.
- Semantics can depend on broader topical context.

### Corpus Size

Source claims:
- Syntactic analogy performance improves monotonically with corpus size in Figure 3.
- Semantic analogy performance does not.
- The paper suggests Wikipedia's coverage of locations and updates may help city/country analogies.

Teaching interpretation:
- Dataset composition and corpus composition interact.

### Runtime

Source claims:
- Building the co-occurrence matrix and training are separate costs.
- For a 6B-token corpus, 400,000 vocabulary, and 10-word symmetric context:
  - building `X` takes about 85 minutes on one thread of the specified machine
  - one 300-dimensional training iteration takes 14 minutes on 32 cores

Teaching interpretation:
- GloVe's "global" approach pays a preprocessing cost to build `X`, then trains from compacted counts.

### Comparison with word2vec

Source claims:
- The paper explicitly says a rigorous quantitative comparison is complicated by many sensitive parameters.
- It controls vector length, context window size, corpus, and vocabulary size.
- It uses training time as the comparison axis by varying GloVe iterations and word2vec negative samples.
- In Figure 4, GloVe outperforms CBOW and skip-gram under the paper's controlled setup.

Teaching interpretation:
- The fair claim is not "GloVe always beats word2vec." The fair claim is "under this controlled setup in the paper, GloVe performed better and reached strong results faster."

## Tables and Figures Usage Guidance

- Table 1 can be converted into a simplified teaching table because the values are visible and central to the mechanism.
- Figure 1 can be recreated qualitatively to explain weighting.
- Figures 2-4 should be summarized qualitatively unless exact chart values are manually extracted.
- Tables 2-4 can be quoted selectively after visual cross-checking.
