# Authoring Notes

## Section Question

Why is plain stochastic gradient descent not enough for noisy, high-dimensional training?

## Reader Outcome

By the end of this section, the reader should be able to explain:

- what an objective/loss function is,
- what a parameter vector is,
- what a gradient says,
- why a stochastic gradient is a noisy hint,
- why an optimizer might keep state across steps.

## Source Anchors And Claims Used

- `topics/adam/wiki/paper_walkthrough.md`
  - The paper focuses on high-dimensional stochastic optimization using first-order gradients.
  - Stochasticity can come from minibatches or other noise sources such as dropout.
  - Adam is positioned between AdaGrad and RMSProp: sparse-gradient usefulness from AdaGrad and online/non-stationary usefulness from RMSProp.
- `topics/adam/wiki/glossary.md`
  - Definitions for `theta`, `f(theta)`, `f_t(theta)`, gradient, stochastic gradient, sparse gradient, and first-order method.
- `topics/adam/wiki/source_map.md`
  - Confirms page 1 contains abstract/introduction and page 5 contains related work.

## Source Assets Used

### Formulas Used

None.

### Figures Used

None.

### Tables Used

None.

### Page Evidence Used

- `topics/adam/wiki/source_assets/pages/paper_01_page_01.png`: abstract and introduction evidence.
- `topics/adam/wiki/source_assets/pages/paper_01_page_05.png`: related-work context evidence.

### Visual Verification Items

No section-specific visual verification is required. The source PDF extraction warning is noted in `topics/adam/wiki/source_assets/visual_audit.md`, but this section does not quote formulas or chart values.

### Evidence Versus Teaching Visuals

The paper page screenshots are used only as source evidence. They are not embedded in the reader-facing preview. The section-local visual `visuals/noisy_gradient_trace.svg` is a simplified teaching sketch inspired by the paper's motivation, not a reproduction of a paper figure.

## Prerequisites

- objective/loss function
- parameter vector
- gradient
- stochastic gradient/minibatch
- sparse gradient

## Expected Reader Confusions

- Thinking stochastic means random for no reason rather than sampled or minibatch-based.
- Thinking Adam changes the model architecture rather than the parameter update rule.
- Treating AdaGrad and RMSProp as concepts that must be mastered now rather than motivation for Adam's design.

## Teaching Mechanism

Mechanism: visual trace.

The visual contrasts raw noisy nudges with a smoother stateful path. This fits the section because the goal is motivation, not yet the Adam equations.

## Code Use

No code is useful in this section. Code will be clearer in the next section after the Adam update loop exists.

## Media Use

Use `visuals/noisy_gradient_trace.svg` near the toy example. It teaches one idea: noisy gradients motivate optimizer memory.

## Toy Demo

Toy setup: one parameter is being nudged toward a lower-loss region. Each mini-batch gives a gradient hint, but the hint wobbles.

Demonstrates: a single gradient can be locally useful but noisy; repeated direct use of noisy hints can zigzag.

Omits: many parameters, per-coordinate scaling, Adam's exact `m_t` and `v_t` state, and paper-scale experiments.

## Toy-To-Real Bridge

The same problem becomes more serious in high-dimensional models: different parameters can receive gradients at different scales, sparse features may update only occasionally, and minibatches or dropout can make the current gradient noisy. The paper frames Adam as a first-order method for exactly this high-dimensional stochastic setting.

## Section-Local Structure Before Prose

1. Start with the training-loop problem: repeated parameter nudges.
2. Define objective, parameters, gradient, stochastic gradient.
3. Use the one-parameter noisy-hint toy example.
4. Bridge to high-dimensional and sparse/noisy settings.
5. Introduce the design pressure behind stateful optimizers.
6. Briefly position SGD, momentum, AdaGrad, RMSProp, and Adam without teaching their mechanics yet.
7. End by preparing the reader for Algorithm 1.
