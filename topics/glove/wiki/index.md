# GloVe Wiki

This wiki is the source-grounded understanding layer for `topics/glove`. It is not the final lesson and should not be published directly.

## Primary Source

- `raw/papers/glove.pdf`
- "GloVe: Global Vectors for Word Representation"
- Jeffrey Pennington, Richard Socher, Christopher D. Manning

## Files

- `source_map.md`: inventory of paper sections, figures, tables, equations, experiments, and extraction caveats.
- `paper_walkthrough.md`: source-grounded section-by-section notes.
- `concepts.md`: beginner-facing prerequisite concepts and intuition.
- `mechanism_notes.md`: derivation and objective notes with symbols and toy examples.
- `experiments_and_results.md`: evaluation setup, reported results, model analysis, runtime, and comparison caveats.
- `teaching_plan_notes.md`: likely reader confusions, visual opportunities, and section-planning guidance.
- `glossary.md`: symbols and terms.
- `open_questions.md`: extraction caveats and non-overclaim rules.

## Core Source Claims

- GloVe is presented as a global log-bilinear regression model for word representations.
- The model is motivated from ratios of co-occurrence probabilities, not only from raw co-occurrence probabilities.
- The paper positions GloVe between global matrix factorization methods and local context-window prediction methods.
- The objective trains on nonzero word-word co-occurrence counts with a weighting function.
- In the paper's experiments, GloVe performs strongly on word analogy, word similarity, and named entity recognition tasks.

## Key Teaching Interpretation

The shortest beginner path is:

1. Words can be represented by the contexts they appear in.
2. Raw co-occurrence counts are noisy because common words appear with many words.
3. Ratios compare two target words against the same context word and can reveal a contrast.
4. GloVe asks vectors to encode those contrasts through dot products and vector differences.
5. Training adjusts word vectors, context vectors, and biases so predicted log co-occurrence counts match observed log counts, with weighting to reduce the influence of extremely rare and extremely frequent pairs.

## Do Not Overstate

- Treat the results as the paper's reported 2014 experimental findings.
- Do not claim analogy benchmarks prove semantic understanding.
- Do not claim GloVe universally beats every later word embedding method.
- Do not reproduce exact chart curves unless manually verified.
