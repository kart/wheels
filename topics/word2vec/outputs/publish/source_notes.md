# Word2Vec Source Notes

Primary source:

- Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean, "Efficient Estimation of Word Representations in Vector Space"
- Project source file: `../../raw/papers/word2vec.pdf`
- arXiv version shown in the source summary: `arXiv:1301.3781v3 [cs.CL] 7 Sep 2013`

Reviewed supporting artifacts:

- `../../wiki/source_summary.md`
- `../../wiki/concepts.md`
- `../../wiki/architecture_notes.md`
- `../../wiki/results_notes.md`
- `../lesson.md`
- `../visual_plan.md`
- `../../reviews/reviewer_report.md`
- `../../reviews/fix_log.md`

## Claims Preserved in the Blog

- The paper proposes Continuous Bag-of-Words and Continuous Skip-gram architectures.
- CBOW predicts the current word from surrounding context.
- Skip-gram predicts surrounding context words from the current word.
- The paper emphasizes computational efficiency so high-dimensional vectors can be trained from very large corpora.
- The paper evaluates vectors with semantic and syntactic relationship questions using vector arithmetic and cosine nearest-neighbor search.
- The evaluation uses strict exact-match scoring; synonyms can count as mistakes.
- The paper situates itself in prior work on continuous and distributed word representations. The blog should not imply Word2Vec invented word vectors.

## Caveats to Preserve

- Analogy arithmetic is an empirical regularity, not symbolic reasoning.
- Toy code demos are educational only; they do not reproduce the paper's training setup or results.
- Visuals are educational redraws and simplifications, not copied paper figures.
- `word2vec-complexity-comparison.svg` is qualitative, not an exact numeric chart.
- Dense-vector maps and analogy coordinates are illustrative, not paper data.
- Training-time comparisons should be described carefully because the paper notes CPU-core counts were estimates from shared datacenter resources.

## PDF Extraction Caveat

The source summary reports that local `pdftotext` extraction was usable for the 12-page PDF. Figure 1 and Tables 1-8 were readable enough for lesson and visual planning, but exact table formatting or any future numeric chart should be checked visually against the PDF before publication.

## Result Claims Used

- Semantic-Syntactic Word Relationship test set: 8,869 semantic questions and 10,675 syntactic questions.
- Architecture comparison used in the post:

| Architecture | Semantic | Syntactic |
| --- | ---: | ---: |
| RNNLM | 9 | 36 |
| NNLM | 23 | 53 |
| CBOW | 24 | 64 |
| Skip-gram | 55 | 59 |

Interpretation used in the post: in this comparison, CBOW is strongest on syntactic questions, while Skip-gram is much stronger on semantic questions.

