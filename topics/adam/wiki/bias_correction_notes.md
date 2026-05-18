# Bias Correction Notes

## Source Claim

Adam initializes `m_0 = 0` and `v_0 = 0`. Because both moving averages start from zero, early estimates are biased toward zero. The paper corrects this by dividing by:

- `1 - beta_1^t` for the first moment,
- `1 - beta_2^t` for the second raw moment.

## Moving Average Expansion

For the second raw moment:

`v_t = beta_2 v_{t-1} + (1 - beta_2) g_t^2`

Expanding the recurrence gives:

`v_t = (1 - beta_2) sum_{i=1}^{t} beta_2^{t-i} g_i^2`

If the gradient distribution is stationary, the expected value is scaled by `1 - beta_2^t`. The paper includes a `zeta` term for non-stationarity.

## Tiny Example

Suppose the squared gradient is always `4` and `beta_2 = 0.999`.

At `t = 1`:

- Raw moving average: `v_1 = 0.001 * 4 = 0.004`.
- Correction factor: `1 - 0.999^1 = 0.001`.
- Corrected value: `v_hat_1 = 0.004 / 0.001 = 4`.

Without correction, the denominator would use `sqrt(0.004)`, much smaller than `sqrt(4)`. That can make the early parameter step too large, especially when the first-moment estimate is also interacting with decay rates.

## Why Sparse Gradients Make This Important

The paper notes that sparse gradients need averaging over many gradients for a reliable second-moment estimate. That pushes `beta_2` close to 1. But when `beta_2` is close to 1, `1 - beta_2^t` is tiny early on, so the uncorrected `v_t` is especially biased toward zero.

## Teaching Guidance

Use bias correction as a concrete case of "the optimizer's memory has a cold start." Avoid saying the vector "learns" unless the text says exactly what is updated: the moving-average state changes from previous state plus a weighted new gradient.

## Caveats

- The clean expectation derivation is exact under stationarity; `zeta` handles non-stationarity.
- The paper's Figure 4 supports the practical importance of bias correction, but exact values should not be quoted without visual extraction.
