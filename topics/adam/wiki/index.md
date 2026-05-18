# Adam Wiki

This wiki compiles source-grounded understanding for the `adam` topic. It is not reader-facing lesson prose.

## Source

- Primary source: `raw/papers/adam.pdf`
- Extracted text: `wiki/source_assets/extracted/adam_pdftotext_layout.txt`
- Visual evidence: `wiki/source_assets/pages/paper_01_page_01.png` through `paper_01_page_15.png`

## Wiki Files

- `source_map.md`: source inventory, page map, extraction caveats.
- `paper_walkthrough.md`: section-by-section paper notes.
- `algorithm_notes.md`: Adam mechanism, update equations, state, hyperparameters, and properties.
- `bias_correction_notes.md`: why zero-initialized moment estimates need correction.
- `convergence_notes.md`: regret framing, assumptions, theorem scope, appendix proof map.
- `experiments_notes.md`: reported experiments and what they can/cannot support.
- `glossary.md`: prerequisite terms and symbols.
- `open_questions.md`: caveats and verification items for section planning.
- `source_assets/`: generated source evidence and formula/figure/table audits.

## Core Source Summary

The Adam paper introduces an adaptive first-order stochastic optimizer. It keeps two exponentially decayed statistics per parameter: a first-moment estimate of gradients and a second raw moment estimate of squared gradients. Because these estimates start at zero, the paper corrects early-time bias by dividing by `1 - beta_1^t` and `1 - beta_2^t`. The final update moves parameters in the direction of the corrected first moment scaled by the square root of the corrected second moment plus `epsilon`.

The paper motivates Adam as combining useful traits associated with AdaGrad and RMSProp: handling sparse gradients and non-stationary/noisy objectives. It also presents update-rule properties, an online-convex regret analysis, empirical comparisons, AdaMax, and temporal averaging.

## Teaching Interpretation

For a beginner, Adam should be taught as a stateful update rule rather than as a magic optimizer. The future article should make explicit:

- what the parameters are,
- what a stochastic gradient is,
- why raw SGD can be noisy or poorly scaled,
- what changes in `m_t` and `v_t` at every step,
- why zero initialization biases early estimates,
- how division by `sqrt(v_hat_t)` changes each coordinate's step size,
- where the paper's theory applies and where it does not.

## Source Fidelity Warnings

- Do not imply the paper proves Adam always outperforms other optimizers.
- Do not describe the regret theorem as a general nonconvex deep-learning guarantee.
- Treat experiment curves qualitatively unless exact plot values are manually extracted.
- Verify formula layout in screenshots before final prose.
