# Formulas And Notation

This file records important notation and formulas for planning. Formula transcription from PDF text extraction is approximate; final article prose should verify against rendered page evidence in `wiki/source_assets/pages/**`.

## Core Symbols

| Symbol | Meaning | Source context |
|---|---|---|
| `Z_p` | p-th input pattern | Learning machine, section 2 |
| `D_p` | desired output for pattern `p` | Learning machine, section 2 |
| `W` | all adjustable parameters | Learning machine and optimization sections |
| `M(Z_p; W)` | model output for input `Z_p` and parameters `W` | Learning machine, section 2 |
| `E_p` | cost/error for pattern `p` | Learning machine, section 2 |
| `E_train(W)` | average training cost over examples | Learning machine, section 2 |
| `X_n` | output vector of module/layer `n` | Backprop, section 3 |
| `W_n` | parameters of module/layer `n` | Backprop, section 3 |
| `Y_n` | weighted input/preactivation vector at layer `n` | Classical multilayer network, section 3 |
| `F` or `f` | activation function | Classical multilayer network, section 3 |
| `eta` | learning rate | Gradient descent and later optimizer sections |
| `H` | Hessian matrix of second derivatives | Convergence and second-order sections |
| `lambda_i` | Hessian eigenvalue | Curvature/conditioning sections |
| `lambda_max` | largest Hessian eigenvalue | Learning-rate stability |
| `kappa` | condition number, approximately `lambda_max / lambda_min` | Conditioning |

## Mean Squared Error

Source idea:

```text
E_p = 1/2 (D_p - M(Z_p; W))^2
E_train = average of E_p over training examples
```

Plain-English reading:

For each training example, compare the desired output with the model's output, square the difference, and average across examples.

Why it matters:

The paper's later Gauss-Newton and Levenberg-Marquardt discussion depends on mean-squared-error structure.

## Modular Backpropagation

Source idea:

```text
X_n = F_n(W_n, X_{n-1})
```

If the derivative of the cost with respect to `X_n` is known, the chain rule gives derivatives with respect to `W_n` and `X_{n-1}` using Jacobians of `F_n`.

Plain-English reading:

A layer transforms its input into an output. Backprop asks: if changing this layer's output changes the loss, how much did this layer's weights and inputs contribute?

Why it matters:

This explains backprop as systematic chain-rule bookkeeping, not magic.

## Classical Layer Equations

Source formulas:

```text
Y_n = W_n X_{n-1}
X_n = F(Y_n)
```

Plain-English reading:

A layer first computes weighted sums, then applies a nonlinear activation to each weighted sum.

Why it matters:

Most later training tricks affect either the scale of `X`, the scale of `Y`, the derivative of `F`, or the scale of `W`.

## Gradient Descent Update

Source idea:

```text
W(t+1) = W(t) - eta * dE/dW
```

The extracted PDF has sign/spacing artifacts, but the intended gradient-descent form is a move opposite the gradient.

Plain-English reading:

At each step, move parameters in the direction that most quickly lowers the cost locally, with step size controlled by `eta`.

Why it matters:

Nearly every paper trick changes either the gradient direction, the step size, or the shape of the surface that the gradient sees.

## Stochastic Update

Source idea:

```text
W(t+1) = W(t) - eta * dE_t/dW
```

Plain-English reading:

Instead of averaging every example before moving, use one example's gradient estimate and update immediately.

Why it matters:

This is central to the paper's distinction between large redundant classification datasets and smaller batch-friendly problems.

## Input Covariance

Source formula:

```text
C_i = (1/P) * sum_p (z_i^p)^2
```

assuming inputs have been centered.

Plain-English reading:

For input coordinate `i`, measure the average squared size of that coordinate across training examples.

Why it matters:

The paper recommends scaling input variables so covariances are about the same, often around 1 for the recommended sigmoid setup.

## Recommended Sigmoid

Source formula:

```text
f(x) = 1.7159 * tanh((2/3) * x)
```

Plain-English reading:

Use a symmetric squashing function scaled so its useful operating region works well with normalized inputs.

Why it matters:

The paper coordinates activation choice with input normalization, target values, and initialization.

## Weight Initialization Scale

Source idea:

```text
sigma_w = m^{-1/2}
```

where `m` is fan-in.

Plain-English reading:

If a unit receives more inputs, make each incoming random weight smaller so the total weighted sum stays at a useful scale.

Why it matters:

This prevents units from starting heavily saturated or too weakly activated, assuming normalized inputs and the paper's recommended sigmoid.

## One-Dimensional Curvature And Optimal Learning Rate

Source idea:

For a local quadratic in one dimension:

```text
eta_opt = 1 / curvature
eta_max = 2 * eta_opt
```

Plain-English reading:

If the valley is steep, use a smaller step. If it is shallow, a larger step is safe. More than twice the one-step rate overshoots and diverges in the quadratic idealization.

Why it matters:

This is the simplest bridge from learning rate to curvature.

## Hessian

Source formula:

```text
H_ij = d^2 E / (dW_i dW_j)
```

Plain-English reading:

The Hessian records how the gradient itself changes when parameters move.

Why it matters:

Its eigenvalues and eigenvectors describe the local shape of the loss surface.

## Multi-Dimensional Learning-Rate Stability

Source idea:

```text
eta < 2 / lambda_max
eta_opt approximately 1 / lambda_max for scalar-rate gradient descent
condition number kappa = lambda_max / lambda_min
```

Plain-English reading:

The largest curvature direction sets the maximum safe scalar learning rate. If other directions are much flatter, that safe rate can be painfully slow there.

Why it matters:

This explains zigzagging, slow convergence, normalization, decorrelation, and per-weight learning rates.

## Linear Network Hessian And Input Covariance

Source idea:

For least mean squares with a linear network:

```text
H = (1/P) * sum_p x_p x_p^T
```

Plain-English reading:

In this simple case, the loss curvature is the same object as the input covariance matrix.

Why it matters:

This is the paper's clearest mathematical reason why preprocessing inputs changes optimization geometry.

## Newton Step

Source idea:

```text
Delta w = - eta * H^{-1} * gradient
```

Plain-English reading:

Instead of stepping directly downhill, rescale and rotate the step by inverse curvature so the local valley becomes more spherical.

Why it matters:

This explains both the attraction and impracticality of second-order methods.

## Diagonal Levenberg-Marquardt Learning Rate

Source idea:

```text
eta_ki = epsilon / (running_diagonal_second_derivative_ki + mu)
```

Plain-English reading:

Give each parameter a learning rate inversely related to its estimated local curvature, with damping `mu` to avoid huge rates in flat regions.

Why it matters:

This is the paper's practical compromise: use some curvature information without storing or inverting the full Hessian.

## Principal Eigenvalue Learning-Rate Estimate

Source idea:

Estimate the largest Hessian eigenvalue using Hessian-vector products or gradient perturbations, then set:

```text
eta_opt approximately 1 / largest_eigenvalue_estimate
```

Plain-English reading:

Find the steepest local direction and choose a learning rate that is safe at that scale.

Why it matters:

The paper uses this to motivate automatic learning-rate prediction in Figures 24-26.
