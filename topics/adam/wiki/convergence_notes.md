# Convergence Notes

## Source Scope

The paper analyzes Adam using online convex optimization. The setup is an arbitrary sequence of convex cost functions `f_1, ..., f_T`. At each time, the algorithm predicts parameters and then evaluates them on the current function.

This is not the same as a full guarantee for nonconvex deep neural network training.

## Regret

The paper defines regret as:

`R(T) = sum_{t=1}^{T} [f_t(theta_t) - f_t(theta*)]`

where `theta*` is the best fixed parameter in hindsight over the feasible set.

Plain-English reading:

- The algorithm makes a sequence of choices.
- After all `T` rounds, compare those choices to the best single choice you could have made if you knew the whole sequence.
- Regret is the extra cumulative loss from not knowing the future.

## Theorem 4.1

Source claim:

- Under bounded gradients, bounded parameter distances, specific decay conditions, and `beta_1 / sqrt(beta_2) < 1`, Adam achieves an `O(sqrt(T))` regret-style guarantee.
- The paper says the result is comparable to best known bounds for the online convex setting.
- Average regret converges to zero under the theorem's assumptions.

Important assumptions to preserve:

- Functions are convex in the analysis.
- Gradients are bounded.
- Distances between generated parameters are bounded.
- The learning rate decays like `alpha_t = alpha / sqrt(t)`.
- The first-moment coefficient decays exponentially in the theorem statement.

## Appendix Proof Map

- Definition 10.1: convexity.
- Lemma 10.2: convex functions can be lower bounded by tangent hyperplanes.
- Lemma 10.3: bounds a sum involving per-coordinate gradients.
- Lemma 10.4: bounds accumulated corrected moment terms.
- Theorem 10.5: proof of the regret bound.

## Teaching Guidance

The future article should explain:

- why regret is a useful theoretical lens,
- why convex assumptions simplify analysis,
- how this differs from practical deep-learning behavior,
- what the paper can claim from experiments versus theory.

Avoid:

- "Adam is proven to converge on neural networks."
- "The theorem proves Adam is always faster."
- Long proof algebra unless the section is explicitly framed as optional.
