# Experiments Notes

## Experiment Families

The paper reports empirical comparisons across:

- L2-regularized multi-class logistic regression on MNIST.
- Logistic regression with bag-of-words features on IMDB movie reviews.
- Multilayer fully connected neural networks on MNIST with and without dropout.
- A CIFAR-10 convolutional neural network.
- A variational autoencoder experiment studying bias correction.

## Figure 1: Logistic Regression

Source claims:

- The MNIST logistic regression setting is convex.
- The IMDB bag-of-words feature setup is sparse.
- The paper reports Adam as similar or favorable compared with other optimizers in these training curves.

Teaching use:

- MNIST logistic regression can illustrate dense gradients.
- IMDB bag-of-words can illustrate sparse features and why adaptive per-coordinate scaling helps.

## Figure 2: Multilayer Networks

Source claims:

- The paper compares training of multilayer neural networks on MNIST with and without dropout.
- Adam is reported as showing better convergence than other methods in the shown results.

Teaching use:

- Use dropout/noisy objectives to connect back to stochastic gradient noise.

## Figure 3: CIFAR-10 ConvNet

Source claims:

- The CIFAR-10 experiment uses a `c64-c64-c128-1000` architecture.
- The paper notes that despite a scale difference early in training, Adam and SGD eventually converge considerably faster than AdaGrad for CNNs in the shown setting.

Teaching use:

- This figure is a good place to avoid overclaiming. The paper's own discussion is nuanced.

## Figure 4: Bias Correction

Source claims:

- The figure compares bias-corrected Adam with a variant lacking bias correction.
- The experiment varies `beta_1`, `beta_2`, and learning rate for a variational autoencoder.
- Values of `beta_2` close to 1 lead to instabilities without bias correction in the shown setting.

Teaching use:

- Figure 4 can support the cold-start memory explanation.
- Later visuals should probably redraw a simplified qualitative matrix, not copy the paper figure.

## Caveats

- The curves are not structured numeric tables.
- Exact values should not be invented.
- Experiments support "worked well in these tested settings," not "universally best optimizer."
