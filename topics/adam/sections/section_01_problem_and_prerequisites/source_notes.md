# Source Notes

## Source Anchors Used

- `topics/adam/wiki/paper_walkthrough.md`
  - Adam is introduced for first-order gradient-based stochastic optimization.
  - The paper focuses on high-dimensional parameter spaces.
  - Stochastic objectives arise from minibatches and other noise sources such as dropout.
  - The paper positions Adam as combining useful ideas associated with AdaGrad and RMSProp.
- `topics/adam/wiki/glossary.md`
  - Used for definitions of parameter vector, objective, gradient, stochastic gradient, sparse gradient, and first-order method.
- `topics/adam/wiki/source_map.md`
  - Used for source inventory and page evidence mapping.
- `topics/adam/wiki/index.md`
  - Used for source-fidelity warnings and the broad statement that Adam is a stateful update rule.

## Source Assets Used

- `topics/adam/wiki/source_assets/pages/paper_01_page_01.png`
  - Evidence for abstract and introduction claims.
- `topics/adam/wiki/source_assets/pages/paper_01_page_05.png`
  - Evidence for related-work context.

No formula, figure, or table assets are used directly in this section.

## Claims And Support

- Claim: Adam is an optimizer for stochastic objectives using first-order gradients.
  - Supported by `paper_walkthrough.md` abstract and introduction notes.
- Claim: Stochastic gradients can arise from mini-batches and other noise sources.
  - Supported by `paper_walkthrough.md` Section 1 notes.
- Claim: The paper positions Adam relative to AdaGrad and RMSProp.
  - Supported by `paper_walkthrough.md` introduction and related-work notes.
- Claim: Adam should be introduced as stateful optimizer behavior, not a model architecture change.
  - Supported by `wiki/index.md` teaching interpretation and `glossary.md`.

## Assumptions And Simplifications

- The one-parameter knob example is a teaching simplification. It is not a paper experiment.
- The noisy-gradient visual is qualitative and should not be read as a measured optimization trajectory.
- The optimizer comparison table intentionally stays high level; mechanics for Adam, AdaGrad, RMSProp, and momentum are deferred.

## Visual Verification Caveats

No formula or chart values are quoted. The generated SVG is section-local and qualitative. Paper page screenshots are evidence only.

## Toy-To-Real Caveats

The toy example has one parameter and a hand-written sequence of mini-batch hints. Real training uses high-dimensional parameter vectors, gradients computed by the model/training objective, and update rules applied elementwise across many coordinates.
