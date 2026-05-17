# GloVe Open Questions and Caveats

## Extraction Caveats

- The PDF text is readable, but the source is two-column academic layout. Some passages appear side-by-side in extracted text.
- Equations need visual cross-checking before final prose, especially superscripts, subscripts, tildes, and summation limits.
- Figures 1-4 are chart/vector content. Do not invent exact plotted values from the images.
- Table 2 needs visual cross-checking before exact row-by-row use because extraction interleaves it with nearby text.

## Claims Not To Overstate

- The paper's 75% analogy result is a reported result in its experimental setup, not a universal property of GloVe.
- "GloVe outperforms word2vec" should be stated as the paper's controlled 2014 comparison, with the paper's own caveat that rigorous comparison is complicated by many parameters.
- The paper argues that count-based and prediction-based methods both probe co-occurrence statistics; it does not prove that all count-based methods are always better.
- Analogy performance should not be framed as proof that vectors understand language.
- The complexity analysis relies on assumptions about co-occurrence distributions and observed corpora; present the practical intuition before the asymptotic derivation.

## Visual Verification Needed Later

- Figure 1: confirm shape and labels of the weighting function before recreating a simplified teaching version.
- Figure 2: use only qualitative claims unless exact plotted values are manually extracted.
- Figure 3: use only qualitative claims unless exact plotted values are manually extracted.
- Figure 4: use only qualitative claims unless exact plotted values are manually extracted.
- Tables 1, 3, and 4 are readable enough for source notes, but final publish text should still check exact numbers against the PDF.

## Teaching Risks

- Readers may not know what a co-occurrence matrix is; introduce it before `X_ij`.
- Readers may not know conditional probability; introduce `P(j | i)` with a tiny count example.
- Readers may not know dot products; explain them as a compatibility score before using the formula.
- Readers may not know least squares; explain it as "make the predicted number close to the observed number, with bigger penalties for bigger mistakes."
- Readers may not know why logs appear; explain count ranges and multiplicative ratios before log equations.
- Readers may confuse word vectors and context vectors; keep their roles explicit until the final `W + Wtilde` note.

## Minimum Additional Extraction Needed

- No additional OCR is needed for the main text.
- Manual PDF spot checks are needed before final authoring for equations, Table 2, and chart labels.
