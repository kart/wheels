# Word2Vec: Learning Word Meaning from Nearby Words

## Draft Status

This is a structured lesson draft, not the final prose-heavy lesson. It is designed for an undergraduate beginner audience and should be expanded after visual assets and optional code demos are created.

Source labels used throughout:

- **Paper claim:** A claim grounded in Mikolov et al., "Efficient Estimation of Word Representations in Vector Space."
- **Teaching interpretation:** A beginner-friendly explanation or analogy derived from the paper.
- **Visual placeholder:** A planned teaching visual to create in a later phase.
- **Code note:** A planned optional demo to create in a later phase.

## Learning Goals

By the end, the reader should be able to:

- Explain why treating words as isolated IDs loses useful similarity information.
- Describe the basic idea of learning word vectors from context prediction.
- Distinguish CBOW from Skip-gram without reversing their prediction directions.
- Explain why the paper emphasizes computational cost.
- Interpret analogy-style evaluation without overclaiming what vector arithmetic proves.
- Read the main result story at a high level without needing to parse every table in the paper.

## 1. Why Word2Vec Was Needed

### Motivation Before Mechanics

Start with a tiny vocabulary:

| Word | ID |
| --- | ---: |
| cat | 17 |
| dog | 42 |
| car | 203 |
| engine | 204 |

If a system only sees these as IDs, it can tell that `cat` and `dog` are different words. It cannot directly tell that they are more related to each other than `cat` and `engine`.

**Paper claim:** The paper says many NLP systems treated words as atomic units, represented as indices in a vocabulary, with no notion of similarity between words.

**Teaching interpretation:** A word ID is like a locker number. It helps retrieve the word, but the number itself does not explain the word.

### One-Hot Vectors Are Identity, Not Similarity

For a tiny vocabulary `[cat, dog, car, engine]`:

| Word | One-hot vector |
| --- | --- |
| cat | `[1, 0, 0, 0]` |
| dog | `[0, 1, 0, 0]` |
| car | `[0, 0, 1, 0]` |
| engine | `[0, 0, 0, 1]` |

This is useful for representing identity, but every different word looks equally different.

**Paper claim:** In the paper's NNLM background, previous words are encoded with `1-of-V` coding, where `V` is vocabulary size.

**Teaching interpretation:** One-hot vectors are a clean starting point, but they leave similarity for the model to discover elsewhere.

**Visual placeholder: `outputs/visuals/one_hot_vs_dense.svg`**

Caption draft: "One-hot vectors identify words with separate slots. Dense word vectors can place related words closer together."

Placement note: Put this visual immediately after the one-hot table.

## 2. The Core Trick: Learn Vectors by Predicting Nearby Words

### The Prediction Game

Use a small sentence:

`the quick brown fox jumps over the lazy dog`

Pick a center word:

`the quick brown [fox] jumps over the lazy dog`

With a context window of 2:

- Before: `quick`, `brown`
- Center: `fox`
- After: `jumps`, `over`

The key idea is not to manually tell the model that `fox` is an animal. Instead, train a model on many small prediction tasks built from nearby words. The vectors are learned as the model gets better at these tasks.

**Paper claim:** The paper proposes architectures for computing continuous word vector representations from very large datasets.

**Teaching interpretation:** Word2Vec turns raw text into many little guessing games. The model's learned word-vector table is the useful artifact.

**Visual placeholder: `outputs/visuals/context_window.svg`**

Caption draft: "A context window turns ordinary text into training examples: one center word and nearby context words."

Placement note: Put this visual beside the sentence example.

**Code note: `outputs/code/toy_context_pairs.py`**

Planned purpose: Generate CBOW and Skip-gram training pairs from a few tokenized toy sentences. Explain the idea before showing code.

## 3. CBOW: Guess the Word from Its Neighbors

### Beginner Example First

Imagine this fill-in-the-blank:

`the quick ___ fox`

CBOW uses nearby context words as clues and predicts the missing current word.

**Paper claim:** CBOW predicts the current word based on surrounding context. The paper reports a setting with four future and four history words as input, predicting the current middle word.

**Teaching interpretation:** CBOW is a "guess the middle word" game.

### Prediction Direction

Preserve this exactly:

`context words -> current/middle word`

Example training target:

- Input clues: `the`, `quick`, `fox`
- Target: `brown`

### What Happens Inside

Beginner-level mechanics:

1. Look up a vector for each context word.
2. Combine those vectors, roughly by averaging or summing.
3. Use the combined context clue to predict the center word.
4. Update the word vectors so future guesses improve.

**Paper claim:** CBOW removes the non-linear hidden layer from the feedforward NNLM. It shares the projection layer for all words, and context vectors are averaged because all words are projected into the same position.

**Teaching interpretation:** The model trades some complexity for speed: it uses a simple blended clue rather than a heavier hidden-layer computation.

**Visual placeholder: `outputs/visuals/cbow_flow.svg`**

Caption draft: "CBOW uses surrounding context words to predict the current word."

Placement note: Put this diagram next to the prediction-direction line. It must show context words flowing into the middle-word prediction.

### Equation Later, After the Intuition

Once the reader understands the prediction game, introduce the cost formula:

`Q = N x D + D x log2(V)`

Plain-English reading:

- `N`: how many context words are used
- `D`: how long each word vector is
- `V`: vocabulary size
- `Q`: work per training example

**Paper claim:** This is the paper's CBOW training-complexity expression with hierarchical softmax.

**Teaching interpretation:** The important beginner point is that CBOW avoids an expensive hidden layer, so each training example can be cheaper.

## 4. Skip-gram: Guess the Neighbors from the Word

### Beginner Example First

Use the same sentence:

`the quick brown fox jumps over the lazy dog`

If the center word is `brown`, Skip-gram trains on predictions like:

- `brown -> quick`
- `brown -> fox`
- `brown -> the`, if the window includes it

**Paper claim:** Skip-gram uses each current word as input and predicts words within a range before and after it.

**Teaching interpretation:** Skip-gram is a "given this word, guess nearby words" game.

### Prediction Direction

Preserve this exactly:

`current/center word -> surrounding context words`

This is the opposite direction from CBOW.

### Window Size and Distance

If the model tries to predict more surrounding words, it gets more training signals, but it also does more work.

**Paper claim:** The paper says increasing the range can improve vector quality but increases computational complexity. More distant words are sampled less often because they are usually less related to the current word. The paper uses `C = 10` in the experiments described.

**Teaching interpretation:** Nearby words are usually stronger clues than faraway words, so the model pays more attention to close neighbors.

**Visual placeholder: `outputs/visuals/skipgram_flow.svg`**

Caption draft: "Skip-gram uses one current word to predict several surrounding words."

Placement note: Put this diagram immediately after the prediction-direction line. It must show center word flowing outward to context predictions.

### Equation Later, After the Intuition

Skip-gram cost:

`Q = C x (D + D x log2(V))`

Plain-English reading:

- `C`: maximum context distance
- `D`: vector length
- `V`: vocabulary size
- The `C x` part reminds us that Skip-gram can make multiple predictions around each center word.

**Paper claim:** This is the paper's Skip-gram training-complexity expression.

**Teaching interpretation:** Wider context windows may improve learned vectors, but the model pays for those extra predictions.

## 5. Why the Paper Cares So Much About Speed

### The Scaling Problem

The paper is not just asking, "Can we learn word vectors?" It is asking whether we can learn good vectors from billions of words and very large vocabularies.

**Paper claim:** The paper's main goal is to learn high-quality word vectors from huge datasets, with billions of words and millions of vocabulary items.

**Teaching interpretation:** If each training example is expensive, huge text collections become hard to use. If each example is cheap, the model can learn from much more text.

### Older Neural Language Models as Contrast

Keep this section compact. It should explain why CBOW and Skip-gram are simpler, not turn into a full NNLM/RNNLM lesson.

**Paper claim:** The paper discusses feedforward NNLM and RNNLM architectures as prior neural language models. It identifies expensive hidden-layer and vocabulary-output computations in those models.

**Teaching interpretation:** Older neural language models can be more expressive, but they do more work per training example. Word2Vec's proposed models remove the non-linear hidden layer to make large-scale vector learning practical.

### Total Cost Formula

Introduce the paper's general training-cost formula:

`O = E x T x Q`

Plain-English reading:

- `E`: number of passes over the data
- `T`: number of training words
- `Q`: work per training example

If `Q` is smaller, the model can afford larger `T` or larger vectors.

**Paper claim:** The paper defines model training complexity as proportional to `O = E x T x Q`.

**Teaching interpretation:** Word2Vec's design focuses on shrinking the per-example work so huge corpora become usable.

### Hierarchical Softmax

Prediction over a huge vocabulary is expensive if the model scores every possible word.

**Paper claim:** The paper uses hierarchical softmax with a Huffman binary tree, giving frequent words shorter binary codes and reducing the number of output units that need to be evaluated.

**Teaching interpretation:** Instead of choosing from every word at once, the model walks a tree of smaller decisions.

**Visual placeholder: `outputs/visuals/hierarchical_softmax_tree.svg`**

Caption draft: "Hierarchical softmax turns a large vocabulary prediction into a path through a tree."

Placement note: Put this visual after the vocabulary-size bottleneck explanation.

**Visual placeholder: `outputs/visuals/complexity_comparison.svg`**

Caption draft: "The paper's efficiency story: older neural language models spend substantial work in hidden-layer and output computations; CBOW and Skip-gram remove the non-linear hidden layer."

Placement note: Use a qualitative chart, not a misleading exact numeric chart.

## 6. How Do We Know the Vectors Are Good?

### Beyond Nearest Neighbors

It is easy to show that a word such as `France` is near other country words. The paper asks for a harder test: can the vectors capture relationships?

**Paper claim:** The paper argues that nearest-neighbor examples are not enough and evaluates syntactic and semantic word relationships.

**Teaching interpretation:** The test is not only "which words are close?" but "do similar relationships point in similar directions?"

### Analogy-Style Evaluation

Start with a grammar-like example:

`big : biggest :: small : ?`

The paper's vector operation:

`vector("biggest") - vector("big") + vector("small")`

Expected answer: `smallest`

Then use a semantic example:

`Paris - France + Italy -> Rome`

**Paper claim:** The paper uses vector addition/subtraction and then searches for the closest vector using cosine distance, discarding the input question words.

**Teaching interpretation:** Some learned relationships behave like reusable arrows in vector space.

Important caution:

This is not symbolic logic. It is an empirical pattern in learned vectors.

**Visual placeholder: `outputs/visuals/analogy_vector_offset.svg`**

Caption draft: "Analogy questions test whether relationship directions in vector space can transfer from one word pair to another."

Placement note: Put this visual beside the analogy examples.

**Visual placeholder: `outputs/visuals/evaluation_pipeline.svg`**

Caption draft: "Evaluation pipeline: analogy question, vector expression, nearest-neighbor search, exact-match score."

Placement note: Put this after explaining exact-match scoring.

### Exact-Match Scoring

**Paper claim:** A question is counted correct only when the closest vector exactly matches the expected answer. Synonyms are counted as mistakes.

**Teaching interpretation:** This makes the metric strict. A model can give a plausible answer and still lose the point.

## 7. What the Results Say

### Keep the Result Story Small

This section should summarize the paper's main result pattern without reproducing every table.

**Paper claim:** The Semantic-Syntactic Word Relationship test set contains 8,869 semantic and 10,675 syntactic questions.

**Teaching interpretation:** The evaluation separates meaning-like relationships from grammar-like relationships.

### Architecture Comparison

Use Table 3 as the cleanest beginner-facing comparison:

| Architecture | Semantic | Syntactic |
| --- | ---: | ---: |
| RNNLM | 9 | 36 |
| NNLM | 23 | 53 |
| CBOW | 24 | 64 |
| Skip-gram | 55 | 59 |

**Paper claim:** In this comparison, CBOW performs better than NNLM on syntactic tasks and about the same on semantic tasks; Skip-gram is slightly worse than CBOW on syntactic tasks but much better on semantic tasks.

**Teaching interpretation:** CBOW is especially strong on syntax here, while Skip-gram is especially strong on semantic relationships.

### Data, Dimension, and Compute Tradeoff

**Paper claim:** The paper reports that using more training data and higher-dimensional word vectors generally improves accuracy, but with diminishing improvements; the authors argue data size and vector dimensionality should be increased together.

**Teaching interpretation:** Bigger is not automatically better in isolation. More data, larger vectors, and training time are a three-way tradeoff.

### Large-Scale Training

Selected result from Table 6:

| Model | Dimensionality | Training words | Total accuracy | Training time |
| --- | ---: | ---: | ---: | --- |
| NNLM | 100 | 6B | 50.8 | 14 days x 180 CPU cores |
| CBOW | 1000 | 6B | 63.7 | 2 days x 140 CPU cores |
| Skip-gram | 1000 | 6B | 65.6 | 2.5 days x 125 CPU cores |

**Paper claim:** CPU-core counts are estimates because datacenter machines were shared with production tasks.

**Teaching interpretation:** The table supports the paper's scaling story, but the training-time comparison should be described carefully rather than as a perfectly controlled benchmark.

### Optional Secondary Result

**Paper claim:** On the Microsoft Sentence Completion Challenge, Skip-gram alone scores 48.0, while Skip-gram combined with RNNLMs scores 58.9, which the paper reports as state of the art at the time.

**Teaching interpretation:** Skip-gram vectors can provide useful complementary information, even when they are not best alone on a task.

## 8. What to Take Away

### Core Takeaways

- Word2Vec learns useful dense word vectors from local context prediction.
- CBOW predicts the current word from surrounding context.
- Skip-gram predicts surrounding words from the current word.
- The paper's architecture choices are motivated by scale: cheaper training makes very large corpora usable.
- Analogy arithmetic is an empirical evaluation pattern, not proof that vectors understand language like people do.
- The paper is part of a longer history of continuous and distributed word representations; it should not be framed as inventing word vectors.

### Final Caution Box

**Paper claim:** The paper reports strong results for CBOW and Skip-gram on its syntactic and semantic regularity tests.

**Teaching interpretation:** The lesson should treat those results as evidence that simple context-prediction objectives can produce useful word geometry, while keeping the claims tied to the paper's datasets, metrics, and time.

## Visual Placeholder Checklist

These visuals are referenced in the draft and should be created in the visual phase:

| Placeholder | Purpose | Nearby section |
| --- | --- | --- |
| `outputs/visuals/one_hot_vs_dense.svg` | Contrast identity-only vectors with dense similarity-friendly vectors | Section 1 |
| `outputs/visuals/context_window.svg` | Explain center word and context words | Section 2 |
| `outputs/visuals/cbow_flow.svg` | Show CBOW prediction direction | Section 3 |
| `outputs/visuals/skipgram_flow.svg` | Show Skip-gram prediction direction | Section 4 |
| `outputs/visuals/hierarchical_softmax_tree.svg` | Explain vocabulary prediction as tree path | Section 5 |
| `outputs/visuals/complexity_comparison.svg` | Qualitatively compare architecture costs | Section 5 |
| `outputs/visuals/analogy_vector_offset.svg` | Show vector relationship offsets | Section 6 |
| `outputs/visuals/evaluation_pipeline.svg` | Show analogy scoring pipeline | Section 6 |

## Code Demo Placement Notes

These are notes only; no code is generated in this phase.

| Demo | Placement | Teaching purpose |
| --- | --- | --- |
| `outputs/code/toy_context_pairs.py` | After Section 2 or before CBOW/Skip-gram sections | Show how context windows become training examples |
| `outputs/code/tiny_skipgram_training.py` | Optional after Section 4 | Show vectors as learned parameters on toy data, with clear caveat that toy data will not reproduce paper results |
| `outputs/code/analogy_demo.py` | After Section 6 | Demonstrate cosine similarity and vector arithmetic separately from training |

## Expansion Notes for the Final Lesson

- Expand each section with short paragraphs, not long blocks.
- Keep examples before equations.
- Keep CBOW and Skip-gram diagrams close to the prediction-direction text.
- Verify Figure 1 and Tables 1-8 visually before final diagrams or result charts.
- Use "paper claim" labels for factual claims tied to the source and "teaching interpretation" labels for analogies.
- Avoid saying Word2Vec invented word vectors or that vector arithmetic is guaranteed reasoning.
