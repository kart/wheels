# YouTube Script Draft: Word2Vec

Working title: "Word2Vec Explained: CBOW, Skip-gram, and Why Prediction Learns Meaning"

## Opening

Today we are going to explain Word2Vec from the ground up.

The point is not to memorize architecture names first. The point is to understand the problem the paper is solving.

Many NLP systems used words as atomic IDs. A system might know that `cat` is word 17 and `dog` is word 42, but those numbers do not say that cats and dogs are more related than cats and engines.

Show visual: `assets/word2vec-one-hot-vs-dense.svg`

## Tiny Example

Use the sentence:

`the quick brown fox jumps over the lazy dog`

Pick a center word: `fox`.

With a context window of 2, the nearby words are `quick`, `brown`, `jumps`, and `over`.

Word2Vec turns text into many small prediction problems. As the model improves at prediction, it learns word vectors as parameters.

Show visual: `assets/word2vec-context-window.svg`

## CBOW

CBOW means Continuous Bag-of-Words.

Its direction is:

`context words -> current word`

So if the sentence is:

`the quick ___ fox`

CBOW uses the surrounding words as clues and predicts the missing middle word.

Show visual: `assets/word2vec-cbow-flow.svg`

Say clearly: do not reverse this direction. CBOW guesses the center from the context.

## Skip-gram

Skip-gram does the opposite.

Its direction is:

`current word -> surrounding context words`

Given `brown`, it tries to predict nearby words like `quick`, `fox`, and maybe `the`, depending on the window.

Show visual: `assets/word2vec-skipgram-flow.svg`

Say clearly: Skip-gram starts from the current word and predicts outward.

## Code Moment

Show a short excerpt from `../code/toy_context_pairs.py`.

Frame it carefully:

This script does not train Word2Vec. It only prints the training examples that CBOW and Skip-gram would use.

Mention that output uses labels like `the@0` and `the@6` so repeated words are not confusing.

## Why Speed Matters

The paper is really about scalable word vectors.

It wants useful vectors from huge datasets, not just a nice demo on a small corpus.

The paper writes total training cost as:

`O = E x T x Q`

Where:

- `E` is epochs
- `T` is training words
- `Q` is work per training example

The Word2Vec architectures try to shrink `Q`.

Show visual: `assets/word2vec-complexity-comparison.svg`

Then explain hierarchical softmax:

Instead of scoring every word in the vocabulary, the model follows a path through a binary tree.

Show visual: `assets/word2vec-hierarchical-softmax-tree.svg`

## Evaluation

The paper does not only ask whether similar words are close together.

It asks whether relationships behave consistently.

Example:

`big : biggest :: small : ?`

The vector operation is:

`vector("biggest") - vector("big") + vector("small")`

Expected answer:

`smallest`

Then the semantic example:

`Paris - France + Italy -> Rome`

Show visual: `assets/word2vec-analogy-vector-offset.svg`

Then show the pipeline:

question, vector expression, nearest-neighbor search, exact-match score.

Show visual: `assets/word2vec-evaluation-pipeline.svg`

Important spoken caveat: this is not symbolic reasoning. It is an empirical pattern in learned vectors.

## Results

Keep this concise.

The paper reports a Semantic-Syntactic Word Relationship test set with 8,869 semantic and 10,675 syntactic questions.

In one architecture comparison:

- CBOW is strong on syntactic questions.
- Skip-gram is much stronger on semantic questions.

The larger result story is that simpler architectures can train useful high-dimensional vectors at much lower computational cost than the heavier neural language models compared in the paper.

## Misconceptions

Address these quickly:

- Word2Vec does not store dictionary definitions.
- CBOW and Skip-gram do not predict in the same direction.
- Analogy arithmetic is not guaranteed logic.
- Word2Vec did not invent distributed word representations.

## Closing

The takeaway:

Word2Vec learns word geometry from local prediction.

CBOW:

`context -> current word`

Skip-gram:

`current word -> context`

And the paper's real power is the combination of useful vectors and scalable training.

