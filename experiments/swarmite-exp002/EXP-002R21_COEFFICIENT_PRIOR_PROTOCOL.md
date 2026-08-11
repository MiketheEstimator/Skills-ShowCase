# EXP-002R21 — Generator-Scale Coefficient Prior

## Hypothesis
The benchmark likelihood uses a Gaussian coefficient prior variance TAU2=4, much broader than the generator's nonzero coefficient magnitudes (0.4-0.9). Excess coefficient flexibility may weaken marginal-likelihood discrimination and encourage unstable graph evidence. A fixed coefficient prior variance of 0.5, chosen from generator scale before observing R21 worlds, may improve terminal structure recovery without directly imposing graph sparsity.

## Frozen treatment
Benchmark-v2 width-1 portfolio controller and uniform DAG prior. Control is committed TAU2=4. Treatment uses identical mechanics except Bayesian linear family models use coefficient/intercept prior variance TAU2=0.5 in both marginal likelihood and posterior predictive variance. Budget, proposals, EIG simulations, and RNG namespaces remain matched.

## Screen
Fresh paired seeds 64901-64912. Pass if mean terminal edge-error delta <= -0.10, mean Brier delta <= +0.005, and <=2/12 worlds worsen by >0.50. If passed, confirm on 65001-65024 with mean edge delta <= -0.10, bootstrap 95% upper bound <0, mean Brier <= +0.005, and <=3/24 large harms.

Ground truth is evaluation-only.