# Visual Audit: Efficient BackProp

## Scope

Audited source:

- `paper_01`: `topics/efficient_backprop/raw/papers/efficient_backprop.pdf`

The PDF has 44 pages. All pages were rendered as source-evidence images under:

```text
topics/efficient_backprop/wiki/source_assets/pages/
```

Rendered file pattern:

```text
efficient_backprop_page_001.png
...
efficient_backprop_page_044.png
```

Text extraction artifacts:

- `topics/efficient_backprop/wiki/source_assets/extracted/efficient_backprop_layout.txt`
- `topics/efficient_backprop/wiki/source_assets/extracted/efficient_backprop_plain.txt`

## Extraction Quality

- Text extraction is broadly usable for section headings, prose, captions, and many equations.
- The source uses older PDF encoding; extracted text has artifacts such as broken ligatures, missing minus signs in some places, malformed accents, and spacing issues inside formulas.
- Formula text must be treated as uncertain until checked against the rendered page image.
- Figure captions are mostly recoverable from text extraction, but rendered pages should be inspected before final prose or visual redraws.

## Important Visual Evidence

The source contains a large number of figures that are central to teaching:

- Figure 1: gradient-based learning machine.
- Figures 2-3: linearly dependent inputs and input transformation.
- Figure 4: recommended versus not-recommended sigmoid shapes.
- Figure 5: convergence flow and learning-rate adaptation intuition.
- Figures 6-8: gradient descent, constant-error lines, Hessian eigenvectors/eigenvalues, and conditioning.
- Figures 9-14: toy linear/multilayer network examples and learning trajectories.
- Figures 15-17: Newton and conjugate-gradient geometry.
- Figure 18: backpropagating diagonal Hessian for sigmoids and RBFs.
- Figures 19-21: Hessian spectra and layer-wise second derivative intuition.
- Figures 22-26: stochastic diagonal Levenberg-Marquardt and principal eigenvalue/learning-rate prediction experiments.

## Recommended Treatment

- Do not use raw page screenshots as reader-facing visuals by default.
- Use rendered pages as evidence for source fidelity.
- Later section authors should create simplified code-generated teaching visuals for:
  - one-parameter and two-parameter loss landscapes
  - stable versus unstable learning rates
  - well-conditioned versus ill-conditioned contours
  - input centering/scaling/decorrelation
  - activation saturation
  - first-order versus second-order step geometry
  - diagonal versus full Hessian intuition
- If a later section refers to exact numeric values from Figures 19-26, the values should be visually checked from the rendered page image and marked as source-derived.

## Manual Spot-Check Needed Later

Before final article prose, manually inspect rendered page evidence for:

- Equations 1-16 for backpropagation, input normalization, target scaling, and weight initialization.
- Equations 20-39 for gradient descent, Taylor/quadratic approximation, Hessian/eigenvalue conditions, and optimal learning rates.
- Equations 40-47 for Newton, conjugate gradient, BFGS, Gauss-Newton, and Levenberg-Marquardt.
- Equations 48-64 for Hessian approximations and eigenvalue/vector estimation.
- Captions and axes in Figures 6-8, 11-13, 19-26, because these visuals carry training-geometry and convergence claims.

## Caveats

- No OCR was run. Text extraction plus rendered page images were sufficient for bootstrap-level source mapping.
- The extracted formulas in `efficient_backprop_layout.txt` should be considered approximate, not authoritative.
- Rendered pages are source evidence only. They are not section visuals and should not be copied into final outputs without an explicit teaching reason.
