# Source Map

## Topic

- `topic_id`: `adam`
- `title`: Adam
- `article_shape`: `paper_deep_dive`
- `audience_profile`: `beginner_technical`

## Raw Sources

| Source | Type | Status | Notes |
|---|---:|---|---|
| `raw/papers/adam.pdf` | PDF paper | readable with local extraction | 15-page ICLR 2015 paper, "Adam: A Method for Stochastic Optimization" by Diederik P. Kingma and Jimmy Lei Ba. |

## Generated Source Evidence

- Extracted text: `wiki/source_assets/extracted/adam_pdftotext_layout.txt`
- Rendered pages: `wiki/source_assets/pages/paper_01_page_01.png` through `wiki/source_assets/pages/paper_01_page_15.png`
- Parser caveat: `pdftotext` and `pdftoppm` reported a recoverable xref reconstruction warning. Text and rendered pages were produced, but formulas and plots should be visually checked against page screenshots before final prose.

## Paper Page Map

| PDF page | Evidence image | Main content |
|---:|---|---|
| 1 | `wiki/source_assets/pages/paper_01_page_01.png` | Abstract and Section 1 introduction. |
| 2 | `wiki/source_assets/pages/paper_01_page_02.png` | Algorithm 1 and Section 2 algorithm setup. |
| 3 | `wiki/source_assets/pages/paper_01_page_03.png` | Adam update-rule properties and Section 3 bias correction start. |
| 4 | `wiki/source_assets/pages/paper_01_page_04.png` | Bias-correction derivation and Section 4 convergence analysis. |
| 5 | `wiki/source_assets/pages/paper_01_page_05.png` | Theorem 4.1, related work, and start of experiments. |
| 6 | `wiki/source_assets/pages/paper_01_page_06.png` | Logistic regression experiments and Figure 1. |
| 7 | `wiki/source_assets/pages/paper_01_page_07.png` | Multilayer neural network and convolutional network experiments, Figures 2 and 3. |
| 8 | `wiki/source_assets/pages/paper_01_page_08.png` | Bias-correction experiment, Figure 4, and AdaMax setup. |
| 9 | `wiki/source_assets/pages/paper_01_page_09.png` | Algorithm 2 AdaMax and infinity-norm derivation. |
| 10 | `wiki/source_assets/pages/paper_01_page_10.png` | Temporal averaging, conclusion, acknowledgements, and start of references. |
| 11 | `wiki/source_assets/pages/paper_01_page_11.png` | References. |
| 12 | `wiki/source_assets/pages/paper_01_page_12.png` | Appendix convergence proof definitions and lemmas. |
| 13 | `wiki/source_assets/pages/paper_01_page_13.png` | Appendix Lemma 10.4 proof. |
| 14 | `wiki/source_assets/pages/paper_01_page_14.png` | Appendix Theorem 10.5 proof. |
| 15 | `wiki/source_assets/pages/paper_01_page_15.png` | Appendix proof conclusion. |

## Source Claims To Preserve

- Adam is a first-order gradient-based stochastic optimization algorithm based on adaptive estimates of lower-order moments.
- The algorithm keeps exponential moving averages of gradients and squared gradients, then applies bias correction for zero initialization.
- The paper positions Adam as combining strengths associated with AdaGrad for sparse gradients and RMSProp for non-stationary objectives.
- The paper analyzes regret in an online convex optimization setting and reports empirical comparisons on logistic regression, multilayer networks, convolutional networks, and a variational autoencoder bias-correction study.
- AdaMax is presented as an infinity-norm variant of Adam.

## Extraction Caveats

- Mathematical layout in the extracted text is imperfect: hats, square roots, subscripts, and fractions require visual verification.
- The experiment figures are available as full-page screenshots, but exact plotted values were not extracted as structured data.
- No OCR was used. The text layer is sufficient for prose notes, while formulas and charts need screenshot spot checks during section planning/authoring.
