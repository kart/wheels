# Figure Audit: Efficient BackProp

Rendered page images are source evidence. Later reader-facing visuals should usually be simplified teaching redraws, not raw page screenshots.

## Figure Inventory

| Figure | Page | What it shows | Recommended treatment |
|---|---:|---|---|
| Fig. 1 | 2 | Gradient-based learning machine: input, parameters, model, output, desired output, error/cost. | Redraw simplified as teaching diagram. |
| Fig. 2 | 9 | Linearly dependent inputs and lines of constant error. | Redraw simplified when explaining redundant/correlated inputs. |
| Fig. 3 | 10 | Input transformation sequence: mean cancellation, KL expansion, covariance equalization. | Redraw simplified flow. |
| Fig. 4 | 11 | Standard logistic versus recommended symmetric scaled tanh. | Code-generate activation curves. |
| Fig. 5 | 16 | Convergence flow and average flow near final stage of learning. | Explain in text or redraw only if section uses learning-rate adaptation. |
| Fig. 6 | 17 | Gradient descent behavior for different learning rates. | Redraw as a central teaching visual. |
| Fig. 7 | 19 | Lines of constant error and Hessian eigenvectors. | Redraw with contours and axes. |
| Fig. 8 | 19 | Input spread and Hessian eigenvalue/eigenvector intuition for LMS. | Redraw or combine with Fig. 7 teaching visual. |
| Fig. 9 | 21 | Simple linear network. | Redraw only if using the linear toy example. |
| Fig. 10 | 21 | Two Gaussian classes. | Redraw if using the paper's toy data example. |
| Fig. 11 | 22 | Batch learning trajectories and error curves for different learning rates. | Redraw simplified or cite qualitatively. |
| Fig. 12 | 23 | Stochastic learning trajectory and error curve. | Redraw simplified to contrast batch/stochastic. |
| Fig. 13 | 23 | Multilayer stochastic trajectory/errors. | Cite qualitatively unless needed for detailed walkthrough. |
| Fig. 14 | 24 | Minimal multilayer network. | Redraw if using this example. |
| Fig. 15 | 26 | Newton algorithm as whitening/local coordinate transform. | Redraw simplified for second-order section. |
| Fig. 16 | 27 | Conjugate-gradient direction idea. | Redraw if explaining conjugate gradient geometry. |
| Fig. 17 | 27 | Conjugate directions in 2D error surface. | Redraw if explaining conjugacy. |
| Fig. 18 | 31 | Backpropagating diagonal Hessian for sigmoids and RBFs. | Use as source evidence; redraw only if covering Hessian backprop deeply. |
| Fig. 19 | 33 | Eigenvalue spectrum in a 4-layer shared-weight network. | Use qualitative chart or cite; exact values require spot-check. |
| Fig. 20 | 34 | Histogram-like eigenvalue spectrum with "big killers". | Use qualitative chart; exact values require spot-check. |
| Fig. 21 | 34 | Layer-wise second derivative scale sketch. | Redraw simplified if explaining layer learning-rate differences. |
| Fig. 22 | 36 | Stochastic diagonal LM with smaller learning rates. | Cite qualitatively or redraw if comparing algorithms. |
| Fig. 23 | 37 | Stochastic diagonal LM with larger learning rates and more fluctuations. | Cite qualitatively or redraw if comparing algorithms. |
| Fig. 24 | 39 | Online principal eigenvalue estimate over pattern presentations. | Cite qualitatively; exact values require spot-check. |
| Fig. 25 | 40 | MSE versus ratio of learning rate to predicted optimal rate for fully connected network. | Cite qualitatively; exact values require spot-check. |
| Fig. 26 | 41 | MSE versus ratio of learning rate to predicted optimal rate for shared-weight network. | Cite qualitatively; exact values require spot-check. |

## High-Priority Teaching Visuals For Later Sections

1. Gradient descent learning-rate outcomes, based on Fig. 6.
2. Well-conditioned versus ill-conditioned loss contours, based on Figs. 7-8.
3. Input transformation pipeline, based on Figs. 2-3.
4. Logistic versus symmetric tanh saturation, based on Fig. 4.
5. Newton as whitening/local preconditioning, based on Fig. 15.
6. Full Hessian versus diagonal/implicit curvature information, based on sections 7-9.

## Verification Notes

- Figure captions are extracted well enough for planning but should be checked visually.
- Axes and numeric values in Figures 19-26 should not be quoted exactly without rendered-page inspection.
- Conceptual redraws should be labeled as conceptual or source-inspired, not exact reproductions, unless values are visually verified.
