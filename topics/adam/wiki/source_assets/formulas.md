# Formula Audit

## F01 - Adam Moment Updates

- `formula_id`: `F01_adam_moment_updates`
- Source PDF: `raw/papers/adam.pdf`
- Page: 2
- Paper section: Algorithm 1 / Section 2
- Visual evidence: `wiki/source_assets/pages/paper_01_page_02.png`
- Normalized formula:
  - `g_t = grad_theta f_t(theta_{t-1})`
  - `m_t = beta_1 m_{t-1} + (1 - beta_1) g_t`
  - `v_t = beta_2 v_{t-1} + (1 - beta_2) g_t^2`
  - `m_hat_t = m_t / (1 - beta_1^t)`
  - `v_hat_t = v_t / (1 - beta_2^t)`
  - `theta_t = theta_{t-1} - alpha m_hat_t / (sqrt(v_hat_t) + epsilon)`
- Symbol definitions: `theta` is the parameter vector; `g_t` is the stochastic gradient; `m_t` is the first-moment moving average; `v_t` is the second raw moment moving average; `alpha` is the stepsize; `beta_1` and `beta_2` are decay rates; `epsilon` is a small stabilizer.
- Intuition: Adam stores a smoothed direction and a smoothed squared-gradient scale, then updates each parameter by direction divided by scale.
- Why it matters: This is the central mechanism every reader-facing section must preserve.
- Likely sections: Adam update loop; toy implementation; caveats.
- `visual_verification_needed`: false

## F02 - Efficient Computation Order

- `formula_id`: `F02_efficient_order`
- Source PDF: `raw/papers/adam.pdf`
- Page: 2
- Paper section: Section 2
- Visual evidence: `wiki/source_assets/pages/paper_01_page_02.png`
- Normalized formula: `alpha_t = alpha * sqrt(1 - beta_2^t) / (1 - beta_1^t)`, followed by `theta_t = theta_{t-1} - alpha_t m_t / (sqrt(v_t) + epsilon_hat)`.
- Symbol definitions: Same symbols as F01; `alpha_t` folds bias correction into the learning-rate multiplier.
- Intuition: The clearer pseudocode computes corrected moments explicitly; the efficient version moves the correction factors into a scalar multiplier.
- Why it matters: Useful caveat for implementation, but not the first teaching path.
- Likely sections: Adam update loop; practical implementation notes.
- `visual_verification_needed`: true

## F03 - Effective Step Size Bounds

- `formula_id`: `F03_effective_step_bounds`
- Source PDF: `raw/papers/adam.pdf`
- Page: 3
- Paper section: Section 2.1
- Visual evidence: `wiki/source_assets/pages/paper_01_page_03.png`
- Normalized formula: `Delta_t = alpha * m_hat_t / sqrt(v_hat_t)`, with paper-stated upper-bound cases depending on `(1 - beta_1)` and `sqrt(1 - beta_2)`.
- Symbol definitions: `Delta_t` is the effective parameter-space step before `epsilon`; `m_hat_t` and `v_hat_t` are bias-corrected moment estimates.
- Intuition: Dividing by the square root of the second moment prevents large updates when recent squared gradients are large.
- Why it matters: Supports the paper's claim that Adam's step magnitudes are approximately bounded by `alpha` in common settings.
- Likely sections: Why the update works; caveats about hyperparameters.
- `visual_verification_needed`: true

## F04 - Bias-Correction Expansion

- `formula_id`: `F04_bias_correction_expansion`
- Source PDF: `raw/papers/adam.pdf`
- Pages: 3-4
- Paper section: Section 3
- Visual evidence: `wiki/source_assets/pages/paper_01_page_03.png`, `wiki/source_assets/pages/paper_01_page_04.png`
- Normalized formula:
  - `v_t = (1 - beta_2) sum_{i=1}^{t} beta_2^{t-i} g_i^2`
  - `E[v_t] = E[g_t^2] * (1 - beta_2^t) + zeta`
- Symbol definitions: `v_t` is the second raw moment moving average; `g_i` are gradients; `zeta` accounts for non-stationarity in the gradient distribution.
- Intuition: Starting the moving average at zero omits the missing early history, so the estimate is too small by a factor near `1 - beta_2^t`.
- Why it matters: Explains why Adam divides by `1 - beta^t` and why the correction is most important early.
- Likely sections: Bias correction section; worked numerical example.
- `visual_verification_needed`: true

## F05 - Regret Definition

- `formula_id`: `F05_regret_definition`
- Source PDF: `raw/papers/adam.pdf`
- Page: 4
- Paper section: Section 4
- Visual evidence: `wiki/source_assets/pages/paper_01_page_04.png`
- Normalized formula: `R(T) = sum_{t=1}^{T} [f_t(theta_t) - f_t(theta*)]`, where `theta* = arg min_{theta in X} sum_{t=1}^{T} f_t(theta)`.
- Symbol definitions: `R(T)` is regret; `theta_t` is the online prediction at time `t`; `theta*` is the best fixed parameter in hindsight.
- Intuition: Regret asks how much worse the online sequence was than the best single fixed choice after seeing all functions.
- Why it matters: Frames the theorem's scope; it is not a blanket proof that Adam wins on every neural-network objective.
- Likely sections: Theory and caveats.
- `visual_verification_needed`: false

## F06 - Theorem 4.1 Regret Bound

- `formula_id`: `F06_theorem_4_1`
- Source PDF: `raw/papers/adam.pdf`
- Page: 5
- Paper section: Section 4
- Visual evidence: `wiki/source_assets/pages/paper_01_page_05.png`
- Normalized formula: Long regret upper bound implying `O(sqrt(T))` regret under stated assumptions.
- Symbol definitions: Requires bounded gradients, bounded distance between generated parameters, decaying `alpha_t`, and decaying first-moment coefficient `beta_{1,t}`.
- Intuition: Under online convex assumptions, average regret goes to zero as `T` grows.
- Why it matters: Must be presented with assumptions and limits; beginner prose should not overgeneralize it to deep learning nonconvex training.
- Likely sections: Theory and caveats.
- `visual_verification_needed`: true

## F07 - AdaMax Infinity-Norm Recurrence

- `formula_id`: `F07_adamax_recurrence`
- Source PDF: `raw/papers/adam.pdf`
- Pages: 8-9
- Paper section: Section 7.1
- Visual evidence: `wiki/source_assets/pages/paper_01_page_08.png`, `wiki/source_assets/pages/paper_01_page_09.png`
- Normalized formula:
  - `u_t = max(beta_2 u_{t-1}, |g_t|)`
  - `theta_t = theta_{t-1} - (alpha / (1 - beta_1^t)) m_t / u_t`
- Symbol definitions: `u_t` is the exponentially weighted infinity norm; `m_t` is the first-moment estimate.
- Intuition: AdaMax replaces the second-moment denominator with a decayed maximum of absolute gradients.
- Why it matters: Covers the paper's variant without making it the main path.
- Likely sections: Variant/caveat section.
- `visual_verification_needed`: true

## F08 - Temporal Averaging

- `formula_id`: `F08_temporal_averaging`
- Source PDF: `raw/papers/adam.pdf`
- Page: 10
- Paper section: Section 7.2
- Visual evidence: `wiki/source_assets/pages/paper_01_page_10.png`
- Normalized formula: `theta_bar_t = beta_2 theta_bar_{t-1} + (1 - beta_2) theta_t`, with bias-corrected `theta_hat_t = theta_bar_t / (1 - beta_2^t)`.
- Symbol definitions: `theta_bar_t` is an exponential average of parameter vectors.
- Intuition: The same moving-average and bias-correction idea can smooth parameters over time.
- Why it matters: Minor extension; include only if space allows.
- Likely sections: What came next / paper variants.
- `visual_verification_needed`: true
