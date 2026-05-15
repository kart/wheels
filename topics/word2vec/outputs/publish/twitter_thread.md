# Twitter/X Thread Draft: Word2Vec

1. Word2Vec is easier to understand if you start with the problem: word IDs identify words, but they do not encode similarity.

`cat = 17` and `dog = 42` tells us nothing about why those words are related.

2. The core trick: learn word vectors by solving prediction problems over nearby words in text.

The useful output is the learned vector table, not the guesses themselves.

3. CBOW predicts the current word from surrounding words:

`context -> current word`

Example: `the quick ___ fox` should predict `brown`.

4. Skip-gram goes the other direction:

`current word -> context`

Example: given `brown`, predict nearby words like `quick` and `fox`.

5. The Word2Vec paper cares a lot about speed.

The goal is not just to learn vectors, but to learn useful high-dimensional vectors from billions of words.

6. The efficiency move: remove expensive hidden-layer machinery from earlier neural language models and train simpler log-linear models at much larger scale.

7. The paper evaluates vectors with analogy-style questions:

`Paris - France + Italy -> Rome`

This is tested with cosine nearest-neighbor search and exact-match scoring.

8. Important caveat: vector arithmetic is an empirical regularity, not proof of symbolic reasoning or human-like understanding.

9. Result pattern from the paper: CBOW is strong on syntactic relationships in the reported comparison; Skip-gram is especially strong on semantic relationships.

10. Full article: a beginner-friendly deep dive with diagrams, tiny examples, code snippets, results, caveats, and misconceptions.

