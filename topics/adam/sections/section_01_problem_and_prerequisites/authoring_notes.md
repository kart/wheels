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

The paper page screenshots are used only as source evidence. They are not embedded in the reader-facing preview. The section-local visual is a code-generated simplified teaching sketch inspired by the paper's motivation, not a reproduction of a paper figure.

Visual source of truth:

- Spec: `visuals/noisy_gradient_trace_spec.md`
- Python source: `visuals/noisy_gradient_trace.py`
- Rendered outputs: `visuals/noisy_gradient_trace.svg`, `visuals/noisy_gradient_trace.png`

## Prerequisite / Intuition Ramp

### Audience-Aware Judgment

This is the first section, so it should not assume the reader already understands optimization vocabulary. It may use central terms early only when they are immediately grounded in plain English.

### Terms Introduced

- Parameters: adjustable model numbers, introduced as knobs.
- Loss/objective: one number measuring how wrong the model is; lower is better.
- Training: repeatedly changing parameters to reduce loss.
- Gradient: a local hint for how parameters should move.
- Mini-batch: a smaller sample of examples used to get a cheaper hint.
- Stochastic gradient: a gradient from a sampled/noisy training situation.
- SGD: a rule that follows the latest noisy hint.
- Optimizer: a rule for deciding how to change parameters after seeing a gradient.
- State: running summaries remembered across steps.

### Ramp Order

1. Start with parameters as adjustable knobs.
2. Define loss/objective as a single wrongness score.
3. Define training as repeatedly changing knobs to lower that score.
4. Define gradient as a local hint.
5. Explain why full-dataset gradients can be expensive.
6. Introduce mini-batches as cheaper but noisier hints.
7. Introduce SGD as following the latest noisy hint.
8. Introduce Adam as a stateful optimizer that remembers recent hints.

### Notation Introduction

Only after the plain-English ramp:

- `theta`: all parameters collected together.
- `f(theta)`: the objective/loss at a parameter setting.
- `f_t(theta)`: the sampled/noisy objective at timestep `t`.
- `m_t` and `v_t`: named only as future Adam state symbols in the visual caption; formal mechanics are deferred.

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

The visual contrasts raw noisy nudges with an Adam-style state-shaped step. This fits the section because the goal is motivation, not yet the Adam equations.

## Code Use

No reader-facing lesson code is useful in this section. The visual is generated from section-local Python source so the technical diagram is reproducible and reviewable.

## Media Use

Use the rendered `visuals/noisy_gradient_trace.svg` near the toy example. `visuals/noisy_gradient_trace.py` is the source of truth and also renders `visuals/noisy_gradient_trace.png`. The visual teaches one idea: noisy gradients motivate optimizer memory.

## Toy Demo

Toy setup: one parameter is being nudged toward a lower-loss region. Each mini-batch gives a gradient hint, but the hint wobbles.

Demonstrates: a single gradient can be locally useful but noisy; repeated direct use of noisy hints can zigzag.

Omits: many parameters, per-coordinate scaling, Adam's exact `m_t` and `v_t` state, and paper-scale experiments.

## Toy-To-Real Bridge

The same problem becomes more serious in high-dimensional models: different parameters can receive gradients at different scales, sparse features may update only occasionally, and minibatches or dropout can make the current gradient noisy. The paper frames Adam as a first-order method for exactly this high-dimensional stochastic setting.

## Section-Local Structure Before Prose

1. Start with a concrete knobs/loss/training mental model.
2. Define gradient as a local hint.
3. Explain mini-batches as cheaper but noisier hints.
4. Introduce SGD as following the latest noisy hint.
5. Introduce Adam as a stateful optimizer that remembers recent hints.
6. Use the one-parameter noisy-hint toy example.
7. Bridge to high-dimensional and sparse/noisy settings.
8. Briefly position SGD, momentum, AdaGrad, RMSProp, and Adam without teaching their mechanics yet.
9. End by preparing the reader for Algorithm 1.
