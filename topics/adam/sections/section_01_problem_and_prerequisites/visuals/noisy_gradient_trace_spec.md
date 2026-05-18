# Visual Spec: noisy_gradient_trace

## Teaching Purpose

Show why Adam-style optimizers keep state when training uses noisy stochastic gradients.

## Exact Concept

The visual contrasts two one-parameter training sketches:

- Left: an SGD-style update reacts to the latest noisy mini-batch gradient/update, so the path can wobble.
- Right: an Adam-style update uses running estimates. `m_t` tracks recent gradient direction and `v_t` tracks recent squared-gradient scale. The current step is shaped by this state.

## Visual Marks

- Pale gold curve: qualitative loss shape for a one-parameter toy problem.
- Gold circle: lower-loss region, not a measured optimum.
- Blue polyline and arrows: direct update steps that react to recent noisy hints.
- Green curve and arrow: current step shaped by running estimates.
- Right callout: recent noisy gradients and their Adam-style summaries.
- Axis labels: loss and parameter value theta.

## What The Visual Must Not Imply

- It must not imply Adam knows the direct path to the optimum.
- It must not imply this is a measured Adam trajectory.
- It must not imply the toy one-parameter sketch captures full high-dimensional Adam behavior.
- It must not present exact experimental values or source-paper measurements.

## Source Assets Used

No figure, formula, or table source asset is directly redrawn. The visual is conceptual and is grounded in the section's source anchors about stochastic gradients, noisy/high-dimensional optimization, and Adam's running first- and second-moment estimates.

## Conceptual Or Source-Derived

Conceptual teaching sketch. Not source-derived from a paper figure.

## Caption

A conceptual sketch of the motivation: a single mini-batch gradient can be useful and still wobble, while Adam-style optimizers keep running estimates of recent direction and squared-gradient scale. The symbols `m_t` and `v_t` are introduced later; this is not a measured result from the paper.

## Review Checklist

- Rendered SVG and PNG exist.
- Python source is the source of truth.
- No clipped text.
- No text outside the canvas.
- No oversized arrows.
- No overlapping labels.
- No floating, unanchored noisy-gradient arrows.
- The right panel does not imply Adam magically knows the optimum.
- Caption clearly says the visual is conceptual and not a measured Adam-paper result.
