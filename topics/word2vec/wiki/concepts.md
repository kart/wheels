# Concepts: Word2Vec

This file compiles beginner-readable concept notes for the Word2Vec topic. It is grounded in `raw/papers/word2vec.pdf` through `wiki/source_summary.md`.

Use two labels consistently in later lesson work:

- **Paper claim:** A claim made by the Mikolov et al. paper.
- **Teaching interpretation:** A beginner-friendly explanation or analogy derived from the paper, not a direct claim by the paper.

## Vocabulary and Atomic Word IDs

**Paper claim:** The paper says many NLP systems treated words as atomic units, represented as indices in a vocabulary, with no built-in notion of similarity between words.

**Teaching interpretation:** A vocabulary index is like assigning every word a locker number. The number helps you find the word, but it does not tell you that `cat` is closer in meaning to `dog` than to `engine`.

**Beginner example:**

| Word | Atomic ID |
| --- | --- |
| cat | 17 |
| dog | 42 |
| car | 203 |
| engine | 204 |

The IDs can identify words, but the model has no direct reason to treat `cat` and `dog` as related.

**Lesson caution:** Do not imply atomic representations are useless. The paper explicitly notes that simple models have advantages: simplicity, robustness, and the ability to train on huge data.

## One-Hot Encoding

**Paper claim:** In the paper's feedforward NNLM discussion, previous words are encoded with `1-of-V` coding, where `V` is vocabulary size.

**Teaching interpretation:** One-hot encoding is a common way to represent a vocabulary index as a vector. If there are `V` words, the vector has `V` slots. A word turns on exactly one slot and leaves all others at zero.

**Beginner example:**

For a tiny vocabulary `[cat, dog, car, engine]`:

| Word | One-hot vector |
| --- | --- |
| cat | `[1, 0, 0, 0]` |
| dog | `[0, 1, 0, 0]` |
| car | `[0, 0, 1, 0]` |
| engine | `[0, 0, 0, 1]` |

This is useful for identity, but it does not encode similarity. Every pair of different words is equally different in this representation.

## Continuous Dense Word Vectors

**Paper claim:** The paper proposes architectures for computing continuous vector representations of words from very large datasets.

**Teaching interpretation:** A dense word vector is a short list of learned numbers. Instead of one active slot and thousands or millions of zeros, each word has many coordinates that can shift during training. Words that behave similarly in text can end up with vectors that point in similar directions or sit near each other.

**Beginner example:**

These numbers are illustrative, not from the paper:

| Word | Tiny dense vector |
| --- | --- |
| cat | `[0.7, 0.2, -0.1]` |
| dog | `[0.6, 0.3, -0.2]` |
| car | `[-0.4, 0.8, 0.5]` |
| engine | `[-0.5, 0.7, 0.6]` |

The model can now represent graded relationships because vectors can be close, far, or point in similar directions.

**Lesson caution:** The paper usually says "word vectors," "continuous vector representations," and "distributed representations." The word "embedding" is a later/common teaching term and should be introduced as explanatory interpretation.

## Distributed Representations

**Paper claim:** The paper identifies distributed representations of words as a successful concept and cites prior work. It does not claim that Word2Vec invented distributed word representations.

**Teaching interpretation:** "Distributed" means the information about a word is spread across many vector dimensions instead of stored in one slot. No single coordinate needs to mean "animal" or "country"; the pattern across coordinates is what matters.

**Why this matters for beginners:** It helps explain why vector similarity can emerge without a hand-written dictionary of meanings.

## Language Modeling Versus Representation Learning

**Paper claim:** The paper discusses neural network language models, but its new architectures focus on learning word vectors efficiently. It directly extends earlier work where vectors are learned first and can then be used in a neural language model.

**Teaching interpretation:** A language model tries to predict words well. Word2Vec uses prediction tasks as a training signal, but the final prize in this paper is the learned word vectors.

**Beginner distinction:**

- Language modeling question: "What word probably comes next?"
- Word representation question: "After training on many prediction tasks, what useful vector did each word learn?"

## Context Windows

**Paper claim:** CBOW uses surrounding words, including future words, to predict the current middle word. Skip-gram predicts words within a range before and after the current word. The paper uses `C = 10` in the Skip-gram experiments.

**Teaching interpretation:** A context window is a small neighborhood around a word in a sentence.

**Beginner example:**

Sentence: `the quick brown fox jumps over the lazy dog`

If the center word is `fox` and the window size is 2:

- Context before: `quick`, `brown`
- Center: `fox`
- Context after: `jumps`, `over`

This small local neighborhood becomes a training example.

## Projection Layer

**Paper claim:** The paper describes projection layers in neural language models and the proposed architectures. For CBOW, the projection layer is shared for all words and context vectors are averaged because all words are projected into the same position.

**Teaching interpretation:** The projection layer is the lookup step. Given a word ID, the model retrieves that word's current dense vector.

**Beginner mental model:** Think of a table with one row per word. Training changes the numbers in the rows.

## CBOW

**Exact term:** Continuous Bag-of-Words Model

**Paper claim:** CBOW predicts the current word based on surrounding context. In the paper's best setting for the described task, the input used four future and four history words, and the training criterion was to classify the current middle word correctly.

**Teaching interpretation:** CBOW is a fill-in-the-blank game:

`the quick ___ fox`

Given the surrounding words, the model tries to predict the missing center word.

**Prediction direction to preserve:**

`context words -> current/middle word`

**Important properties from the paper:**

- The non-linear hidden layer from the feedforward NNLM is removed.
- Context vectors are averaged or summed in the shared projection.
- Word order in the history does not affect the projection.
- Future words can be used as context.

**Equation to preserve:**

`Q = N x D + D x log2(V)`

Where:

- `N`: number of context words
- `D`: vector dimensionality
- `V`: vocabulary size
- `Q`: model-specific training cost per example

**Lesson caution:** Do not describe CBOW as predicting context words. That is Skip-gram.

## Skip-gram

**Exact term:** Continuous Skip-gram Model

**Paper claim:** Skip-gram uses each current word as input and predicts words within a certain range before and after it. Increasing the range can improve vector quality but increases computational complexity. More distant words are sampled less often because they are usually less related.

**Teaching interpretation:** Skip-gram is the reverse prediction game:

Given `brown`, try to predict nearby words such as `quick` and `fox`.

**Prediction direction to preserve:**

`current/center word -> surrounding context words`

**Equation to preserve:**

`Q = C x (D + D x log2(V))`

Where:

- `C`: maximum context distance
- `D`: vector dimensionality
- `V`: vocabulary size
- `Q`: model-specific training cost per example

**Lesson caution:** Do not describe Skip-gram as averaging context to predict the center word. That is CBOW.

## Log-linear Classifier

**Paper claim:** The paper calls CBOW and Skip-gram new log-linear models and describes CBOW as a log-linear classifier in the setting with history and future words.

**Teaching interpretation:** For this lesson, a log-linear classifier can be explained as a simpler prediction model without the extra non-linear hidden layer used in heavier neural language models.

**Beginner framing:** The model still learns by making predictions and adjusting weights, but it avoids a costly middle computation layer. That design choice is central to the paper's speed story.

## Hierarchical Softmax and Huffman Trees

**Paper claim:** The paper uses hierarchical softmax where the vocabulary is represented as a Huffman binary tree. Frequent words receive shorter binary codes. This reduces the number of output units evaluated, compared with scoring every word in the vocabulary.

**Teaching interpretation:** Instead of asking "Which one of a million words is the answer?" all at once, hierarchical softmax turns prediction into a sequence of smaller left/right decisions down a tree.

**Beginner example:**

If the target word is `the`, a frequent word, it might be reachable by a short path. A rare word might require a longer path.

**Caution:** The paper notes this speedup is especially important for architectures without hidden layers because they depend heavily on efficient softmax normalization.

## Training Complexity

**Paper claim:** The paper defines training complexity as proportional to:

`O = E x T x Q`

Where:

- `E`: training epochs
- `T`: number of words in the training set
- `Q`: architecture-specific work per training example

**Teaching interpretation:** Total training work grows when you:

- make more passes over the data,
- use more training words,
- or use a model that does more work per word.

**Beginner example:** If a model is twice as expensive per word, training on the same corpus takes roughly twice the work. If the corpus is twice as large, that also roughly doubles work.

## Cosine Similarity

**Paper claim:** In analogy evaluation, after computing a target vector expression, the paper searches for the closest word vector using cosine distance and discards the input question words.

**Teaching interpretation:** Cosine similarity compares vector direction. Two words can be similar if their vectors point in similar directions, even if their raw coordinate sizes differ.

**Beginner framing:** If vectors are arrows, cosine similarity asks whether two arrows point the same way.

## Analogy and Vector Offset Questions

**Paper claim:** The paper evaluates whether word vectors preserve syntactic and semantic regularities through vector arithmetic. Example: compute `vector("biggest") - vector("big") + vector("small")`, then search for the closest vector. The expected result is `smallest`.

**Teaching interpretation:** Some learned relationships act like reusable arrows in vector space. If `big -> biggest` is one arrow, applying a similar arrow to `small` may land near `smallest`.

**Beginner example:**

`Paris - France + Italy` should land near `Rome` in a good vector space.

**Caution:** This is statistical and imperfect. It is not symbolic logic. The paper's own examples would score only about 60% under the exact-match metric described in Table 8.

## Semantic Versus Syntactic Regularities

**Paper claim:** The paper's test set contains five semantic question types and nine syntactic question types, with 8,869 semantic and 10,675 syntactic questions.

**Teaching interpretation:**

- Semantic relationships are about meaning or world relationships: country-capital, city-state, currency.
- Syntactic relationships are about grammar or word form: comparative, superlative, plural, past tense.

**Examples from the paper's categories:**

- Semantic: `Athens : Greece :: Oslo : Norway`
- Syntactic: `great : greater :: tough : tougher`

## Exact-Match Accuracy

**Paper claim:** A question is marked correct only if the closest computed vector exactly matches the expected answer. Synonyms count as mistakes.

**Teaching interpretation:** The metric is strict. A model can produce a reasonable nearby answer and still be scored wrong if it is not the exact target word.

**Why this matters:** It prevents the lesson from overstating or understating results. The numbers are useful, but they are tied to a specific exact-match test.

## Terms and Symbols for the Final Lesson

Use these consistently:

| Symbol or term | Meaning |
| --- | --- |
| `V` | Vocabulary size |
| `D` | Word vector dimensionality |
| `N` | Number of previous or context words, depending on architecture discussion |
| `H` | Hidden layer size |
| `E` | Number of training epochs |
| `T` | Number of training words |
| `Q` | Model-specific training cost per example |
| `C` | Maximum Skip-gram context distance |
| CBOW | Continuous Bag-of-Words; predicts current word from context |
| Skip-gram | Predicts surrounding words from current word |
| NNLM | Neural network language model |
| RNNLM | Recurrent neural network language model |

