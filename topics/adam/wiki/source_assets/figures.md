# Figure Audit

## G01 - Algorithm 1 Pseudocode

- `figure_id`: `G01_algorithm_1`
- Source PDF: `raw/papers/adam.pdf`
- Page: 2
- Caption: Algorithm 1, Adam for stochastic optimization.
- What it appears to show: Required inputs, initialized state, gradient computation, moment updates, bias correction, and parameter update.
- Why it matters: Primary mechanism source.
- Recommended treatment: `redraw_simplified`
- Visual evidence: `wiki/source_assets/pages/paper_01_page_02.png`
- `visual_verification_needed`: false

## G02 - Figure 1 Logistic Regression

- `figure_id`: `G02_figure_1_logistic_regression`
- Source PDF: `raw/papers/adam.pdf`
- Page: 6
- Caption: Logistic regression training negative log likelihood on MNIST images and IMDB movie reviews with bag-of-words features.
- What it appears to show: Training curves comparing Adam with other optimizers on dense and sparse logistic-regression settings.
- Why it matters: Supports the paper's empirical comparison claims, especially sparse-feature discussion.
- Recommended treatment: `explain_in_text`
- Visual evidence: `wiki/source_assets/pages/paper_01_page_06.png`
- `visual_verification_needed`: true

## G03 - Figure 2 Multilayer Neural Networks

- `figure_id`: `G03_figure_2_mlp`
- Source PDF: `raw/papers/adam.pdf`
- Page: 7
- Caption: Training of multilayer neural networks on MNIST images with and without dropout.
- What it appears to show: Training-cost curves for optimizer comparisons under dense gradients and dropout noise.
- Why it matters: Part of empirical section coverage.
- Recommended treatment: `explain_in_text`
- Visual evidence: `wiki/source_assets/pages/paper_01_page_07.png`
- `visual_verification_needed`: true

## G04 - Figure 3 CIFAR-10 ConvNet

- `figure_id`: `G04_figure_3_cifar10`
- Source PDF: `raw/papers/adam.pdf`
- Page: 7
- Caption: Convolutional neural network training cost on CIFAR-10, including first three epochs and 45 epochs.
- What it appears to show: Adam, AdaGrad, and SGD comparisons; the paper notes Adam and SGD eventually converge faster than AdaGrad in the CNN setting.
- Why it matters: Prevents overclaiming that Adam dominates every run.
- Recommended treatment: `explain_in_text`
- Visual evidence: `wiki/source_assets/pages/paper_01_page_07.png`
- `visual_verification_needed`: true

## G05 - Figure 4 Bias-Correction Terms

- `figure_id`: `G05_figure_4_bias_correction`
- Source PDF: `raw/papers/adam.pdf`
- Page: 8
- Caption: Effect of bias-correction terms versus no bias correction terms after processing one million minibatches.
- What it appears to show: Sensitivity over `beta_1`, `beta_2`, and learning rate choices; instability without bias correction for `beta_2` close to 1.
- Why it matters: Direct evidence for the bias-correction explanation.
- Recommended treatment: `redraw_simplified`
- Visual evidence: `wiki/source_assets/pages/paper_01_page_08.png`
- `visual_verification_needed`: true

## G06 - Algorithm 2 AdaMax

- `figure_id`: `G06_algorithm_2_adamax`
- Source PDF: `raw/papers/adam.pdf`
- Page: 9
- Caption: Algorithm 2, AdaMax variant based on the infinity norm.
- What it appears to show: AdaMax inputs, state, infinity-norm update, and parameter update.
- Why it matters: Required for source-complete paper walkthrough, but secondary to Adam.
- Recommended treatment: `explain_in_text`
- Visual evidence: `wiki/source_assets/pages/paper_01_page_09.png`
- `visual_verification_needed`: true
