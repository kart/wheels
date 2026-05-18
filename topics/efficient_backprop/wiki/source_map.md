# Source Map: Efficient BackProp

## Topic

- Topic id: `efficient_backprop`
- Title: `Efficient BackProp`
- Article shape: `paper_deep_dive`
- Audience profile: `beginner_technical`

## Primary Source

| Source id | Path | Type | Status | Notes |
|---|---|---|---|---|
| `paper_01` | `topics/efficient_backprop/raw/papers/efficient_backprop.pdf` | PDF chapter/paper | readable with local extraction | 44-page PDF, originally published in Orr and Muller, *Neural Networks: Tricks of the Trade*, Springer, 1998. |

## Generated Extraction Artifacts

These are generated source-evidence artifacts under `wiki/source_assets/**`, not section media.

| Artifact | Path | Purpose |
|---|---|---|
| Layout-preserving text | `topics/efficient_backprop/wiki/source_assets/extracted/efficient_backprop_layout.txt` | Main text extraction with page breaks and approximate formula/figure placement. |
| Plain text | `topics/efficient_backprop/wiki/source_assets/extracted/efficient_backprop_plain.txt` | Search-friendly text extraction. |
| Rendered pages | `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_001.png` through `efficient_backprop_page_044.png` | Visual evidence for formulas, figures, captions, and extraction verification. |

## Source Structure

The PDF text extraction identifies these main sections:

| Paper section | Topic | Source coverage notes |
|---|---|---|
| Abstract | Purpose and claims | The chapter analyzes backprop convergence, practical tricks, and the practical limits of classical second-order methods. |
| 1 Introduction | Why backprop can feel like art | Frames training as a set of critical but problem-dependent choices, with heuristics and theory as guidance rather than a foolproof recipe. |
| 2 Learning and Generalization | Learning machine, training cost, test error, bias/variance | Introduces the learning-machine diagram, mean squared error, empirical risk minimization, and the distinction between minimization and generalization. |
| 3 Standard Backpropagation | Modular backprop and classical multilayer equations | Defines modules, Jacobians, chain-rule backward recurrence, matrix/sigmoid layers, and gradient descent. |
| 4 A Few Practical Tricks | Stochastic learning, shuffling, input normalization, sigmoid choice, target values, learning rates, RBFs | This is a core practical section and must be covered deeply. |
| 5 Convergence of Gradient Descent | Quadratic intuition, eigenvalues, conditioning, examples, transformations | Explains why learning rates and input transformations matter through curvature and Hessian geometry. |
| 6 Classical second order optimization methods | Newton, conjugate gradient, quasi-Newton, Gauss-Newton, Levenberg-Marquardt | Explains benefits and limits of classical second-order optimization for neural nets. |
| 7 Tricks to compute the Hessian information | Finite differences, diagonal estimates, backpropagating second derivatives | Covers ways to approximate useful Hessian information without explicitly forming the full Hessian. |
| 8 Analysis of the Hessian in multi-layer networks | Hessian spectra and layered curvature | Uses eigenvalue spectrum figures to explain curvature spread and why conditioning is hard in multilayer networks. |
| 9 Applying Second Order Methods to Multilayer Networks | Stochastic diagonal Levenberg-Marquardt and principal eigenvalue/vector estimation | Presents practical approximate second-order methods and learning-rate prediction. |
| 10 Discussion and Conclusion | Recommended training workflow and caveats | Summarizes recommended practices and states that classical second-order methods are impractical in almost all useful cases. |

## Required Deep-Dive Coverage

Later planning and authoring should not collapse this source into a short summary. The paper/chapter is long and foundational. The final article should preserve a deep walkthrough of:

- training/generalization distinction
- standard backpropagation and what changes during training
- stochastic versus batch learning
- input centering, scaling, and decorrelation
- target scaling
- sigmoid saturation and activation choice
- weight initialization
- learning-rate selection and adaptation
- curvature, Hessian, eigenvalues, and conditioning
- first-order versus second-order optimization
- why classical second-order methods are often impractical for large neural networks
- diagonal/implicit Hessian approximations
- which recommendations are historical versus still useful today

## Source Fidelity Notes

- The PDF text extraction is mostly readable but has OCR/encoding artifacts such as broken ligatures and malformed characters.
- Equations are partially readable in text, but formula fidelity must be checked against rendered page images before final prose.
- Figures are visible in rendered pages. Later reader-facing visuals should generally be simplified teaching redraws rather than raw screenshots.
- Historical/current interpretation must be clearly labeled as interpretation. The source itself is a 1998 chapter/paper; later modern ML practice is outside the provided source unless separately sourced or marked as contextual interpretation.
