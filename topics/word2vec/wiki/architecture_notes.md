# Architecture Notes: Word2Vec

This file compares the model architectures discussed in the paper in beginner-readable terms. It is grounded in `wiki/source_summary.md` and the primary source PDF.

Use these labels in later lesson work:

- **Paper claim:** What the paper states or reports.
- **Teaching interpretation:** A simplified explanation meant to help beginners.

## Why Architecture Matters in This Paper

**Paper claim:** The paper compares architectures by computational complexity, defined as the number of parameters that need to be accessed to fully train the model. The goal is to maximize accuracy while minimizing computational complexity.

**Teaching interpretation:** The authors are asking: how much useful word-vector quality can we get per unit of training work?

This matters because the paper's goal is not just to train word vectors. It is to train high-quality vectors from billions of words and very large vocabularies.

## Total Training Cost

**Paper claim:** The paper defines total training complexity as:

`O = E x T x Q`

Where:

- `E` is the number of training epochs.
- `T` is the number of words in the training set.
- `Q` is the architecture-specific training cost per example.

**Teaching interpretation:** Training work comes from three knobs:

- How many times we pass over the text.
- How much text we use.
- How expensive the model is for each word or context.

The paper tries to reduce `Q`, so larger `T` and larger vectors become practical.

## Feedforward Neural Net Language Model

**Exact term in paper:** Feedforward Neural Net Language Model, or NNLM

### Structure

**Paper claim:** The feedforward NNLM has input, projection, hidden, and output layers. The input uses `N` previous words encoded with `1-of-V` coding. The projection layer has size `N x D`, and the hidden layer has size `H`.

**Teaching interpretation:** This model looks at a fixed number of previous words, converts them into dense vectors, pushes those through a hidden layer, and predicts a probability distribution over the vocabulary.

### Cost

**Paper claim:** The per-example complexity is:

`Q = N x D + N x D x H + H x V`

The paper says the `H x V` term is dominating before output optimizations. With hierarchical softmax, much of the remaining complexity comes from `N x D x H`.

### Beginner explanation

The old model is powerful but expensive for two reasons:

- It has a dense hidden layer computation.
- It may need to score many possible output words.

The proposed Word2Vec architectures are easier to understand if this is the contrast: remove expensive hidden-layer machinery and train useful vectors with simpler prediction tasks.

## Recurrent Neural Net Language Model

**Exact term in paper:** Recurrent Neural Net Language Model, or RNNLM

### Structure

**Paper claim:** The RNNLM has input, hidden, and output layers. A recurrent matrix connects the hidden layer to itself through time-delayed connections, allowing the model to carry information from the past.

**Teaching interpretation:** An RNNLM has a memory-like hidden state. Instead of only looking at a fixed window of previous words, it updates a state as it reads a sequence.

### Cost

**Paper claim:** The per-example complexity is:

`Q = H x H + H x V`

With hierarchical softmax, `H x V` can be reduced to `H x log2(V)`, leaving `H x H` as much of the complexity.

### Beginner explanation

The RNNLM can model sequence patterns, but maintaining and updating a hidden state is expensive. The Word2Vec paper does not try to teach RNNs; it uses RNNLMs as one comparison point for word-vector quality and training cost.

## Parallel Training with DistBelief

**Paper claim:** The authors implemented several models in DistBelief. They trained multiple replicas in parallel and synchronized gradient updates through centralized parameter servers. They used mini-batch asynchronous gradient descent with Adagrad.

**Teaching interpretation:** The paper is partly an engineering scaling paper. It asks how to learn vectors when the text corpus and vocabulary are very large, and it uses distributed infrastructure for large experiments.

**Lesson guidance:** Mention this after the reader understands why the architecture is cheaper. Do not make distributed systems the main thread.

## New Log-linear Models

**Paper claim:** The paper proposes two new architectures that try to minimize computational complexity. The main observation is that much complexity in earlier neural models comes from the non-linear hidden layer.

**Teaching interpretation:** The authors simplify the model: keep the prediction task that teaches useful word vectors, but remove a costly hidden layer. This is the central architecture move.

## CBOW Architecture

**Exact term in paper:** Continuous Bag-of-Words Model

### Prediction direction

**Paper claim:** CBOW predicts the current word based on context.

**Must preserve:** `context words -> current/middle word`

### Architecture

**Paper claim:** CBOW is similar to the feedforward NNLM, but the non-linear hidden layer is removed. The projection layer is shared for all words. All context words are projected into the same position, so their vectors are averaged. Word order in the history does not influence the projection. The paper also uses future words.

**Teaching interpretation:** CBOW takes several nearby words, blends their vectors into one context clue, and asks: what word probably belongs in the middle?

### Training target

**Paper claim:** The paper reports best performance on its task with four future and four history words as input, where the criterion is to classify the current middle word correctly.

### Cost

**Paper claim:** CBOW training complexity is:

`Q = N x D + D x log2(V)`

Where:

- `N`: number of context words
- `D`: vector dimensionality
- `V`: vocabulary size

### Beginner example

Sentence fragment:

`the quick ___ fox`

CBOW uses words like `the`, `quick`, and `fox` as clues and tries to predict the missing word.

### What to emphasize in the lesson

- CBOW is fast because it removes the non-linear hidden layer.
- It ignores word order in the bag-of-words projection.
- It predicts one center word from multiple context words.

## Skip-gram Architecture

**Exact term in paper:** Continuous Skip-gram Model

### Prediction direction

**Paper claim:** Skip-gram predicts surrounding words given the current word.

**Must preserve:** `current/center word -> surrounding context words`

### Architecture

**Paper claim:** Skip-gram uses each current word as input to a log-linear classifier with a continuous projection layer, and predicts words within a certain range before and after the current word.

**Teaching interpretation:** Skip-gram takes one word and asks: what nearby words should this word help predict?

### Window size and sampling

**Paper claim:** Increasing the prediction range improves vector quality but increases computational complexity. More distant words are sampled less often because they are usually less related to the current word. The paper uses `C = 10` in later experiments.

### Cost

**Paper claim:** Skip-gram training complexity is:

`Q = C x (D + D x log2(V))`

Where:

- `C`: maximum distance of context words
- `D`: vector dimensionality
- `V`: vocabulary size

### Beginner example

Sentence fragment:

`the quick brown fox`

If the center word is `brown`, Skip-gram may train on predictions like:

- `brown -> quick`
- `brown -> fox`
- `brown -> the`, if the window includes it

### What to emphasize in the lesson

- Skip-gram predicts multiple context words from one center word.
- Wider windows can help but cost more.
- The paper's results show Skip-gram is especially strong on semantic analogy questions in key comparisons.

## Figure 1 Architecture Summary

**Paper claim:** Figure 1 compares the two new model architectures. Its caption states that CBOW predicts the current word from context and Skip-gram predicts surrounding words from the current word.

**Redraw guidance for later visual phase:**

- CBOW side:
  - Inputs: `w(t-2)`, `w(t-1)`, `w(t+1)`, `w(t+2)`
  - Projection: shared lookup plus sum/average
  - Output: `w(t)`
- Skip-gram side:
  - Input: `w(t)`
  - Projection: current word vector
  - Outputs: `w(t-2)`, `w(t-1)`, `w(t+1)`, `w(t+2)`

**Caveat:** Figure 1 needs visual inspection before final redraw. Text extraction captured structure but not exact layout.

## Architecture Comparison Table

| Architecture | Main prediction target | Key expensive part | Paper role |
| --- | --- | --- | --- |
| Feedforward NNLM | Next/current word from previous words | Hidden layer and vocabulary output | Prior model comparison |
| RNNLM | Next word using recurrent hidden state | Recurrent hidden computation and vocabulary output | Prior model comparison |
| CBOW | Current word from context | Much cheaper; no non-linear hidden layer | Proposed model |
| Skip-gram | Surrounding words from current word | Repeated predictions over context range | Proposed model |

## Equations to Carry Forward

Use these exact formulas in later lesson work, with beginner explanation before or immediately after each one:

| Equation | Formula | Teaching use |
| --- | --- | --- |
| (1) | `O = E x T x Q` | Total training cost story |
| (2) | `Q = N x D + N x D x H + H x V` | Why feedforward NNLM is expensive |
| (3) | `Q = H x H + H x V` | Why RNNLM is expensive |
| (4) | `Q = N x D + D x log2(V)` | Why CBOW is cheaper |
| (5) | `Q = C x (D + D x log2(V))` | Why Skip-gram cost grows with context range |

## Common Architecture Mistakes to Avoid

- Do not say CBOW predicts surrounding words. It predicts the current/middle word from context.
- Do not say Skip-gram averages context vectors. Skip-gram predicts context words from the current word.
- Do not teach hierarchical softmax as the main invention. It is an efficiency technique used in the models.
- Do not claim that removing the hidden layer always improves modeling power. The paper frames the simpler models as potentially less precise but much more scalable.
- Do not over-teach NNLM or RNNLM internals. They are supporting contrast, not the core beginner topic.

