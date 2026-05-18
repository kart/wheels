# Historical Versus Still-Useful Recommendations

This file separates source claims from bootstrap interpretation. The source is from 1998. It does not itself prove what is current practice in 2026. Treat modern relevance notes as planning interpretation unless later supported with additional sources.

## Source-Era Context

The paper discusses classical feed-forward neural networks, sigmoid/tanh activations, mean squared error, stochastic gradient, conjugate gradient, BFGS, Gauss-Newton, Levenberg-Marquardt, and Hessian approximations. It predates many later defaults such as ReLU-family activations, batch normalization, Adam-style adaptive optimizers becoming common defaults, and deep-learning-scale GPU training practice.

## Recommendations That Are Source Claims

The paper explicitly recommends or argues:

- shuffle examples
- center input variables by subtracting the mean
- normalize input variables to standard deviation around 1
- decorrelate input variables if possible
- prefer symmetric sigmoids over standard logistic sigmoid
- choose target values within the sigmoid range rather than at asymptotes
- initialize weights with mean zero and standard deviation about `1 / sqrt(fan-in)` under the paper's assumptions
- use larger learning rates in lower layers than higher layers in many architectures
- use stochastic gradient with careful tuning for large redundant classification datasets
- use conjugate gradient for smaller datasets or regression-like tasks where accurate real-valued outputs matter
- regard classical full second-order methods as impractical in almost all useful large-network cases

## Durable Principles

These ideas remain broadly useful as training intuition:

- preprocessing changes optimization geometry
- centering reduces biased update directions
- scaling inputs changes effective curvature
- decorrelation can reduce parameter coupling
- activation saturation blocks gradients
- target scale can induce or avoid output saturation
- initialization scale controls early activation and gradient regimes
- learning-rate stability depends on curvature
- a single scalar learning rate is limited by the steepest direction
- full Hessians are expensive, but curvature approximations can be useful

## Historically Specific Details

These should be explained as historical/source-era recommendations, not universal modern rules:

- the specific scaled tanh activation as the recommended default
- the target-value recommendation tied to the scaled sigmoid's maximum second derivative
- mean squared error as the common classification cost in the source's framing
- the exact stochastic diagonal Levenberg-Marquardt recommendation and the paper's three-times-faster rule of thumb
- conjugate gradient as a preferred option for some smaller/regression problems in the source-era optimizer landscape
- layerwise learning-rate heuristics tied to sigmoid-era multilayer architectures

## Modern Interpretation To Handle Carefully

If later article sections discuss modern deep learning, phrase cautiously:

- Modern neural networks often use activation functions and normalization layers that change the saturation and centering story, but the underlying gradient-flow intuition remains useful.
- Modern initialization schemes can be viewed as descendants of the same variance-control idea, but exact formulas differ by activation and architecture.
- Adaptive optimizers and normalization layers do not remove the need to understand scale, curvature, and conditioning.
- Full Hessian methods remain expensive at large scale, but modern second-order, quasi-second-order, and preconditioning ideas continue to appear in specialized forms.

Do not claim these modern points as source claims unless additional sources are added.

## Planning Guidance

The final article should include a "historical versus still useful" section after the paper walkthrough or near the recap. It should:

- respect the paper's 1998 context
- avoid ridiculing old recommendations
- explain which ideas were tied to sigmoid networks and which are general optimization principles
- avoid pretending the paper anticipated every modern method
- use "the source argues" for source claims and "a modern reader can reinterpret this as" for interpretation
