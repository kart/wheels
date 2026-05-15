# Results Notes: Word2Vec

This file compiles the paper's evaluation setup, tables, examples, and result cautions for later lesson writing. It is grounded in `wiki/source_summary.md` and the primary source PDF.

Use these labels consistently:

- **Paper claim:** What the paper states or reports.
- **Teaching interpretation:** A beginner-friendly explanation based on the paper.

## What the Paper Tries to Measure

**Paper claim:** The paper evaluates word vectors using syntactic and semantic word relationship tasks, not just nearest-neighbor examples.

**Teaching interpretation:** Nearest neighbors can show that `France` is near `Italy`, but that is a weak test. The paper wants to know whether relationships between pairs of words are also organized in vector space.

## Analogy-Style Evaluation

**Paper claim:** The paper represents a relationship by subtracting and adding word vectors, then searches for the closest word vector using cosine distance. Input question words are discarded during the search.

**Example from the paper's explanation:**

`vector("biggest") - vector("big") + vector("small")`

Expected answer: `smallest`

**Teaching interpretation:** The test asks whether a relationship acts like a reusable direction in vector space. If the model learned a "comparative or superlative direction," applying it to another word may land near the correct form.

**Lesson caution:** Vector arithmetic should be presented as an empirical pattern, not symbolic reasoning.

## Semantic-Syntactic Word Relationship Test Set

**Paper claim:** The paper introduces a comprehensive test set with five semantic relationship types and nine syntactic relationship types.

Reported question counts:

- Semantic: 8,869 questions
- Syntactic: 10,675 questions

**Paper claim:** Questions were created by manually building lists of related word pairs, then connecting pairs to form questions. The test set includes only single-token words, so multi-word entities like "New York" are excluded.

**Paper claim:** A model is correct only if the closest vector exactly matches the expected word. Synonyms count as mistakes.

**Teaching interpretation:** The score is strict. A plausible answer can still be wrong under this metric if it is not exactly the target word.

## Table 1: Question Categories

**Paper claim:** Table 1 gives examples of five semantic and nine syntactic categories.

Categories shown:

| Type | Category examples |
| --- | --- |
| Semantic | common capital city, all capital cities, currency, city-in-state, man-woman |
| Syntactic | adjective to adverb, opposite, comparative, superlative, present participle, nationality adjective, past tense, plural nouns, plural verbs |

**Teaching interpretation:** These categories let the paper test both meaning-like relationships and grammar-like relationships.

**Visual/table caution:** Table 1 is readable from extraction, but exact examples should be checked against the PDF before final reproduction.

## Table 2: Data Size and Vector Dimensionality

**Paper claim:** The authors train CBOW on subsets of Google News data with vocabulary restricted to the 30,000 most frequent words for this experiment.

Variables:

- Vector dimensionality: 50, 100, 300, 600
- Training words: 24M, 49M, 98M, 196M, 391M, 783M

**Paper claim:** Accuracy generally improves as training words and vector dimensionality increase, but with diminishing improvements after some point.

Notable extracted value:

- 600-dimensional CBOW vectors trained on 783M words reach 50.4 accuracy on this restricted-vocabulary subset.

**Teaching interpretation:** Bigger vectors help, and more data helps, but neither knob is magic by itself. The paper argues they should be increased together under a compute budget.

**Equation connection:** From Equation (4), the paper notes that doubling training data produces about the same computational-complexity increase as doubling vector size.

## Table 3: Architecture Comparison

**Paper claim:** Table 3 compares RNNLM, NNLM, CBOW, and Skip-gram using the same data and 640-dimensional vectors. It reports semantic and syntactic accuracy on the paper's test set, plus a syntactic MSR word relatedness test.

Extracted values:

| Architecture | Semantic | Syntactic | MSR syntactic test |
| --- | ---: | ---: | ---: |
| RNNLM | 9 | 36 | 35 |
| NNLM | 23 | 53 | 47 |
| CBOW | 24 | 64 | 61 |
| Skip-gram | 55 | 59 | 56 |

**Paper claim:** CBOW performs better than NNLM on syntactic tasks and about the same on semantic tasks. Skip-gram is slightly worse than CBOW on syntactic tasks but much better on semantic tasks.

**Teaching interpretation:** This is the cleanest table for explaining the architecture tradeoff. CBOW is very strong on syntax here; Skip-gram shines on semantic relationships.

## Table 4: Public Vectors and Authors' Models

**Paper claim:** Table 4 compares publicly available word vectors with vectors from the authors' models on the full Semantic-Syntactic Word Relationship test set.

Selected extracted values:

| Model | Dimensionality | Training words | Semantic | Syntactic | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Our NNLM | 100 | 6B | 34.2 | 64.5 | 50.8 |
| CBOW | 300 | 783M | 15.5 | 53.1 | 36.1 |
| Skip-gram | 300 | 783M | 50.0 | 55.9 | 53.3 |

**Teaching interpretation:** The table supports the paper's claim that the simpler architectures are competitive and efficient. Skip-gram with less data than the 6B-word NNLM has the best total among these selected rows.

**Lesson caution:** Do not overload beginners with all rows from Table 4 unless needed. A compact comparison is enough.

## Table 5: One Epoch Versus Three Epochs

**Paper claim:** Training a model on twice as much data for one epoch gives comparable or better results than iterating over the same data for three epochs in the reported cases.

Selected extracted values:

| Model | Dimensionality | Training words | Total accuracy | Training time |
| --- | ---: | ---: | ---: | --- |
| 3 epoch CBOW | 300 | 783M | 36.1 | 1 day |
| 1 epoch CBOW | 300 | 1.6B | 36.1 | 0.6 days |
| 3 epoch Skip-gram | 300 | 783M | 53.3 | 3 days |
| 1 epoch Skip-gram | 300 | 1.6B | 53.8 | 2 days |
| 1 epoch Skip-gram | 600 | 783M | 55.5 | 2.5 days |

**Teaching interpretation:** For this paper's setup, fresh data can be more valuable than repeated passes over the same data.

## Table 6: Large-Scale Parallel Training

**Paper claim:** Table 6 reports DistBelief distributed training results on Google News 6B data using 50 to 100 model replicas and Adagrad.

Extracted values:

| Model | Dimensionality | Training words | Semantic | Syntactic | Total | Training time |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| NNLM | 100 | 6B | 34.2 | 64.5 | 50.8 | 14 days x 180 CPU cores |
| CBOW | 1000 | 6B | 57.3 | 68.9 | 63.7 | 2 days x 140 CPU cores |
| Skip-gram | 1000 | 6B | 66.1 | 65.1 | 65.6 | 2.5 days x 125 CPU cores |

**Paper claim:** CPU-core counts are estimates because datacenter machines were shared with production tasks.

**Teaching interpretation:** This table is the strongest support for the paper's scaling story: simpler models can train high-dimensional vectors much faster than the NNLM comparison while achieving better total accuracy on the reported task.

**Lesson caution:** The training-time comparison is not a clean single-machine benchmark. The paper itself warns that CPU usage fluctuated.

## Table 7: Microsoft Sentence Completion Challenge

**Paper claim:** The Microsoft Sentence Completion Challenge has 1,040 sentences with one missing word and five candidate choices.

**Paper claim:** Skip-gram alone scores 48.0 accuracy. Combining Skip-gram scores with RNNLMs gives 58.9 accuracy, which the paper reports as a new state-of-the-art result at the time.

Extracted values:

| Architecture | Accuracy |
| --- | ---: |
| 4-gram | 39 |
| Average LSA similarity | 49 |
| Log-bilinear model | 54.8 |
| RNNLMs | 55.4 |
| Skip-gram | 48.0 |
| Skip-gram + RNNLMs | 58.9 |

**Teaching interpretation:** Skip-gram is not best alone on this task, but it provides complementary information when combined with RNNLMs.

**Lesson guidance:** Treat this as a secondary result, not the main storyline.

## Table 8: Learned Relationship Examples

**Paper claim:** Table 8 shows word-pair relationship examples using Skip-gram vectors trained on 783M words with 300 dimensions.

**Paper claim:** The relationship is formed by subtracting two vectors and adding another. The text gives `Paris - France + Italy = Rome`.

Selected examples from Table 8:

| Relationship | Example outputs |
| --- | --- |
| France - Paris | Italy: Rome; Japan: Tokyo |
| big - bigger | cold: colder; quick: quicker |
| Miami - Florida | Baltimore: Maryland; Dallas: Texas |
| Einstein - scientist | Mozart: violinist; Picasso: painter |
| Microsoft - Windows | Google: Android; Apple: iPhone |

**Paper claim:** The table's examples would score only about 60% under the paper's exact-match accuracy metric. Averaging ten examples instead of one to form the relationship vector improved the best models by about 10 percentage points absolute.

**Teaching interpretation:** The examples are memorable, but they should not be used as proof that the model understands facts in a human sense. They show that repeated textual patterns can create useful geometry.

## Overall Result Story

**Paper claim:** The paper reports that high-quality word vectors can be trained with simple architectures compared with feedforward and recurrent neural network language models.

**Paper claim:** Lower computational complexity makes it possible to compute accurate high-dimensional vectors from much larger datasets.

**Teaching interpretation:** The paper's story has two halves:

1. A learning trick: train vectors by predicting words from local context.
2. An efficiency trick: simplify the architecture so it can scale to much more text.

## What the Results Do Not Prove

Do not overclaim these points in later artifacts:

- The results do not prove that vectors understand meaning like humans.
- The results do not prove that analogy arithmetic always works.
- The results do not prove that Word2Vec invented word vectors or distributed representations.
- The results do not make CBOW or Skip-gram universally best for every NLP task.
- The "one trillion words" statement in the conclusion is a forward-looking expectation, not a completed experiment in the paper.

## Exact Result Claims Worth Preserving

- The paper's test set has 8,869 semantic and 10,675 syntactic questions.
- CBOW predicts the current word from context; Skip-gram predicts context words from the current word.
- Table 3: CBOW achieves 64 syntactic accuracy, while Skip-gram achieves 55 semantic accuracy in the 640-dimensional architecture comparison.
- Table 4: Skip-gram with 300 dimensions and 783M words reports total 53.3, higher than the selected authors' NNLM row at total 50.8.
- Table 6: 1000-dimensional CBOW and Skip-gram trained on 6B words report total 63.7 and 65.6 respectively, compared with NNLM total 50.8.
- Table 7: Skip-gram alone is 48.0 on sentence completion, but Skip-gram plus RNNLMs is 58.9.

## Visual Recommendations for Later Phases

No visuals are created in this phase, but the results should later be visualized carefully:

- Use a compact architecture comparison chart from Table 3.
- Use a data-versus-dimension heatmap or small matrix from Table 2 only after verifying table values against the PDF.
- Use a restrained summary chart for Table 6 to show the scale/training-time tradeoff.
- Use an analogy pipeline diagram: relationship pair -> vector expression -> nearest-neighbor search -> exact-match scoring.

