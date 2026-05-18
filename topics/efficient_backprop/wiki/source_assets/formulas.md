# Formula Audit: Efficient BackProp

Formula extraction from the PDF is approximate. Use rendered evidence pages for final verification.

## `formula_learning_machine_mse`

- Source: `paper_01`
- Page: 2
- Related paper section: 2, Learning and Generalization
- Formula: mean squared error per example and average training cost.
- Symbols:
  - `D_p`: desired output
  - `M(Z_p; W)`: model output
  - `E_p`: per-example error
  - `E_train`: average training error
- Intuition: measure the squared gap between desired and predicted output, then average across examples.
- Why it matters: sets the cost function that later optimization tries to minimize.
- Likely sections: motivation, training setup.
- Evidence image: `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_002.png`
- `visual_verification_needed`: true

## `formula_backprop_01_10`

- Source: `paper_01`
- Pages: 3-4
- Related paper section: 3, Standard Backpropagation
- Formula group: modular backprop recurrence, matrix/sigmoid layer equations, scalar/matrix backprop equations, gradient descent update.
- Symbols:
  - `X_n`: layer/module output
  - `W_n`: layer/module parameters
  - `Y_n`: weighted sums/preactivations
  - `F` or `f`: activation function
  - `E_p`: per-example cost
  - `eta`: learning rate
- Intuition: derivatives flow backward through modules using the chain rule; gradients with respect to weights are then used by an optimizer.
- Why it matters: this is the paper's formal backprop foundation.
- Likely sections: foundation training loop, standard backprop walkthrough.
- Evidence images:
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_003.png`
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_004.png`
- `visual_verification_needed`: true

## `formula_input_covariance_13`

- Source: `paper_01`
- Page: 8
- Related paper section: 4.3, Normalizing the Inputs
- Formula: input covariance/average squared component after centering.
- Symbols:
  - `P`: number of training examples
  - `z_i^p`: component `i` of training example `p`
  - `C_i`: covariance/spread of input variable `i`
- Intuition: measure how large each input coordinate tends to be.
- Why it matters: the paper recommends scaling inputs so covariances are comparable.
- Evidence image: `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_008.png`
- `visual_verification_needed`: true

## `formula_recommended_sigmoid`

- Source: `paper_01`
- Page: 10-11
- Related paper section: 4.4, The Sigmoid
- Formula: `f(x) = 1.7159 tanh((2/3)x)`.
- Intuition: a symmetric activation scaled to work well with normalized inputs.
- Why it matters: coordinates activation output scale with input preprocessing and target values.
- Evidence images:
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_010.png`
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_011.png`
- `visual_verification_needed`: true

## `formula_weight_initialization_14_16`

- Source: `paper_01`
- Page: 13
- Related paper section: 4.6, Initializing the weights
- Formula group: weighted-sum standard deviation and random-weight scale `sigma_w = m^{-1/2}`.
- Symbols:
  - `m`: fan-in, number of inputs to a unit
  - `sigma_w`: standard deviation of random weights
  - `sigma_y`: standard deviation of weighted input to sigmoid
- Intuition: shrink individual weights when a unit has many inputs so the sum remains in a useful activation range.
- Why it matters: initialization controls early activation saturation and gradient scale.
- Evidence image: `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_013.png`
- `visual_verification_needed`: true

## `formula_learning_rate_adaptation_17_19`

- Source: `paper_01`
- Pages: 13-15
- Related paper section: 4.7, Choosing Learning Rates
- Formula group: adaptive learning-rate rules using a leaky average of gradients.
- Intuition: use an averaged gradient signal to estimate distance to minimum and anneal the learning rate near the minimum.
- Why it matters: bridges stochastic learning-rate adaptation to Hessian/eigenvector intuition.
- Evidence images:
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_013.png`
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_014.png`
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_015.png`
- `visual_verification_needed`: true

## `formula_curvature_20_39`

- Source: `paper_01`
- Pages: 16-20
- Related paper section: 5.1, A Little Theory
- Formula group: one-dimensional gradient descent, Taylor expansion, optimal learning rate, Hessian definition, quadratic approximation, eigendecomposition, convergence condition.
- Key meanings:
  - `eta_opt`: one-step optimal learning rate for local quadratic in one dimension
  - `eta_max`: maximum non-divergent learning rate in one-dimensional quadratic case
  - `H`: Hessian curvature matrix
  - `lambda_max`: largest Hessian eigenvalue
  - condition number: eigenvalue spread controlling convergence speed
- Intuition: learning rate is safe only relative to curvature; in many dimensions, the steepest direction limits the global rate.
- Why it matters: this is the mathematical backbone for normalization, conditioning, and second-order methods.
- Evidence images:
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_016.png`
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_017.png`
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_018.png`
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_019.png`
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_020.png`
- `visual_verification_needed`: true

## `formula_second_order_40_47`

- Source: `paper_01`
- Pages: 25-29
- Related paper section: 6, Classical second order optimization methods
- Formula group: Newton update, conjugate-gradient direction rules, BFGS inverse-Hessian estimate update, Gauss-Newton and Levenberg-Marquardt updates.
- Intuition: use curvature or curvature approximations to choose better-shaped steps than raw gradient descent.
- Why it matters: shows why second-order methods are attractive and why full versions are expensive or limited.
- Evidence images:
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_025.png`
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_026.png`
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_027.png`
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_028.png`
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_029.png`
- `visual_verification_needed`: true

## `formula_hessian_48_64`

- Source: `paper_01`
- Pages: 30-38
- Related paper sections: 7 and 9
- Formula group: square-Jacobian approximation, backpropagating diagonal Hessian terms, Hessian-vector products, stochastic diagonal Levenberg-Marquardt rates, principal eigenvalue/vector estimates.
- Intuition: compute useful curvature approximations without explicitly storing or inverting the full Hessian.
- Why it matters: this is the paper's practical route from second-order theory to scalable training tricks.
- Evidence images:
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_030.png`
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_031.png`
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_032.png`
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_035.png`
  - `topics/efficient_backprop/wiki/source_assets/pages/efficient_backprop_page_038.png`
- `visual_verification_needed`: true
