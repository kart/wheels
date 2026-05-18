# Efficient BackProp Wiki

## Bootstrap Status

This wiki compiles source-grounded understanding for `efficient_backprop` before any section planning or reader-facing prose is created.

Generated bootstrap artifacts:

- `wiki/source_map.md`
- `wiki/source_summary.md`
- `wiki/concepts.md`
- `wiki/formulas_and_notation.md`
- `wiki/historical_vs_current.md`
- `wiki/foundation_stack.md`
- `wiki/glossary.md`
- `wiki/open_questions.md`
- `wiki/source_assets/**`
- `wiki_preview/index.html`

## Source

Primary source:

- Yann LeCun, Leon Bottou, Genevieve B. Orr, and Klaus-Robert Muller, "Efficient BackProp", originally published in Orr and Muller, *Neural Networks: Tricks of the Trade*, Springer, 1998.
- Local file: `topics/efficient_backprop/raw/papers/efficient_backprop.pdf`

## Reader And Article Shape

- Audience: `beginner_technical`
- Article shape: `paper_deep_dive`

The final article must be a deep paper/chapter walkthrough, not a short summary. The source is long and foundational, so later section planning should include explicit background sections before formula-heavy mechanics.

## Core Source Thesis

The paper says backpropagation is simple and efficient in principle, but often hard to make work well in practice. It then explains practical "tricks" through optimization geometry:

- preprocess inputs so gradients are less biased and the error surface is better conditioned
- choose activation functions and target values that avoid saturation
- initialize weights so units operate in useful regimes
- choose learning rates with curvature in mind
- prefer stochastic learning for many large redundant classification datasets
- understand why full second-order methods are usually impractical for large networks
- use partial or implicit curvature information when it gives practical benefit

## Planning Implications

Later section planning should consume `wiki/foundation_stack.md` first. Recommended early background sections:

1. What changes during training: parameters, loss, gradients, and backpropagation.
2. Loss geometry: learning rates, curvature, conditioning, Hessian/eigenvalue intuition.
3. Practical training hygiene: normalization, scaling, saturation, initialization.

Only after that should the article walk through the paper's sections in detail.

## Source Asset Evidence

Rendered source pages:

- `wiki/source_assets/pages/efficient_backprop_page_001.png` through `efficient_backprop_page_044.png`

Text extraction:

- `wiki/source_assets/extracted/efficient_backprop_layout.txt`
- `wiki/source_assets/extracted/efficient_backprop_plain.txt`

Important audit files:

- `wiki/source_assets/formulas.md`
- `wiki/source_assets/figures.md`
- `wiki/source_assets/tables.md`
- `wiki/source_assets/visual_audit.md`

## Critical Caveat

Historical/current relevance is not directly established by the 1998 source. `wiki/historical_vs_current.md` includes bootstrap interpretation for later planning, but final article claims about modern practice should either be clearly framed as interpretation or grounded in additional sources if the user adds them.
