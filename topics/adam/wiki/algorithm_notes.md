# Algorithm Notes

## Problem Setup

Adam minimizes a stochastic objective. At step `t`, the optimizer sees a gradient `g_t` from a stochastic realization `f_t(theta)`, often a minibatch loss. The update uses only first-order information: gradients with respect to parameters.

## Inputs

- `alpha`: base stepsize.
- `beta_1`: exponential decay rate for the first-moment estimate.
- `beta_2`: exponential decay rate for the second raw moment estimate.
- `epsilon`: small denominator stabilizer.
- `theta_0`: initial parameter vector.
- `f(theta)`: stochastic objective.

## State

- `t`: timestep.
- `m_t`: moving average of gradients. This remembers direction.
- `v_t`: moving average of squared gradients. This remembers scale/variability per coordinate.
- `theta_t`: current parameter vector.

## Core Update

At each step:

1. Compute a stochastic gradient `g_t`.
2. Update direction memory: `m_t = beta_1 m_{t-1} + (1 - beta_1) g_t`.
3. Update squared-gradient memory: `v_t = beta_2 v_{t-1} + (1 - beta_2) g_t^2`.
4. Correct early-time bias:
   - `m_hat_t = m_t / (1 - beta_1^t)`
   - `v_hat_t = v_t / (1 - beta_2^t)`
5. Update parameters:
   - `theta_t = theta_{t-1} - alpha m_hat_t / (sqrt(v_hat_t) + epsilon)`

All vector operations are elementwise.

## Beginner Numerical Example To Use Later

For one coordinate, suppose:

- `alpha = 0.001`
- `beta_1 = 0.9`
- `beta_2 = 0.999`
- `epsilon` is tiny
- first observed gradient is `g_1 = 2`

Then:

- `m_1 = 0.9 * 0 + 0.1 * 2 = 0.2`
- `v_1 = 0.999 * 0 + 0.001 * 4 = 0.004`
- `m_hat_1 = 0.2 / 0.1 = 2`
- `v_hat_1 = 0.004 / 0.001 = 4`
- update amount is about `0.001 * 2 / sqrt(4) = 0.001`

This example shows why bias correction matters: without correction, `m_1` and `v_1` are not on the same scale as the observed gradient statistics.

## Why The Denominator Is Useful

If a coordinate repeatedly has large squared gradients, `v_hat_t` grows for that coordinate. Dividing by `sqrt(v_hat_t)` reduces the step there. If another coordinate has smaller squared gradients, it can receive a relatively larger effective step. This is the adaptive per-parameter learning-rate idea.

## Scale Invariance Claim

The paper states that rescaling gradients by a constant scales the first moment and second-moment square root in matching ways, so the ratio approximately cancels the scale. This claim should be taught carefully:

- It applies to the update ratio before `epsilon` dominates.
- It is diagonal/per-coordinate rescaling behavior, not arbitrary rotation or full matrix invariance.

## Relationship To Other Optimizers

Paper-grounded interpretation:

- SGD uses the current gradient directly.
- Momentum smooths directions by accumulating gradient history.
- AdaGrad accumulates squared-gradient information and is useful for sparse gradients, but its accumulated denominator can keep growing.
- RMSProp uses an exponential moving average of squared gradients for non-stationary settings.
- Adam combines a momentum-like first moment, an RMSProp-like second raw moment, and explicit bias correction.

## Implementation Caveats

- The paper gives a clearer pseudocode and a more efficient order. Teach the clear version first.
- Do not claim the default hyperparameters are universally optimal; the paper says they worked well for tested machine-learning problems.
- The algorithm stores two additional vectors the same size as parameters.
