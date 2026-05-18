# Glossary

This glossary is a short reference. It is not a substitute for `foundation_stack.md`.

## Activation Saturation

A unit is saturated when its activation is in a flat tail where changing the input barely changes the output. Saturation makes derivatives small and slows gradient-based learning.

## Backpropagation

An efficient chain-rule procedure for computing derivatives of the cost with respect to every parameter in a layered model.

## Batch Learning

Training mode where a full training-set gradient is computed before each parameter update.

## Condition Number

In this paper's optimization discussion, roughly the ratio between largest and smallest Hessian eigenvalues. Large condition numbers mean some directions are much steeper than others, making scalar learning-rate gradient descent slow.

## Curvature

How quickly the gradient changes as parameters move. In one dimension it is a second derivative; in many dimensions it is represented locally by the Hessian.

## Decorrelation

Transforming inputs so different input coordinates are less statistically coupled. The paper connects decorrelation to making the Hessian closer to diagonal in simple cases.

## Eigenvalue

For the Hessian, an eigenvalue measures curvature along a corresponding eigenvector direction.

## Eigenvector

For the Hessian, a principal direction of the local loss surface.

## Fan-In

The number of inputs feeding into a unit. The paper's initialization rule scales random weight standard deviation as `1 / sqrt(fan-in)` under its assumptions.

## Gradient

The vector of first derivatives of the cost with respect to parameters. It points in the direction of steepest local increase; gradient descent moves against it.

## Hessian

The matrix of second derivatives of the cost with respect to parameters. It describes local curvature.

## Learning Rate

The step-size multiplier used to convert a gradient or search direction into a parameter update.

## Levenberg-Marquardt

A curvature-aware method related to Gauss-Newton that adds damping to avoid unstable steps when curvature estimates are small or ill-conditioned.

## Mean Squared Error

A cost function based on the squared difference between desired and predicted output.

## Momentum

A training heuristic that adds a fraction of the previous update to the current update, often damping high-curvature oscillations and helping movement along flatter directions.

## Newton Method

A second-order method that uses the inverse Hessian to rescale/rotate the gradient. Attractive for local quadratics, but full Hessian storage/inversion is usually impractical for large networks.

## Stochastic Learning

Training mode where each update uses one example or a small noisy sample instead of the full training set.

## Target Scaling

Choosing numerical target values for supervised outputs. In this paper, target scaling is tied to avoiding sigmoid saturation.
