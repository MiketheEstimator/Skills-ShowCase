# EXP-002R23 — Design-Adaptive g-Prior for Family Likelihoods

## Status
RUNNING after R22 mechanism diagnosis.

## Hypothesis
R22 showed that simply reducing isotropic coefficient-prior variance weakens the marginal-likelihood complexity penalty and drives dense-graph overfit. A design-adaptive Gaussian g-prior can regularize coefficient scale relative to the observed design while preserving a dimension-aware evidence penalty, avoiding the R21 failure mechanism.

## Frozen scientific design
Keep benchmark-v2, uniform DAG prior, width-1 proposal portfolio, budget 15, proposal RNG, real-environment RNG, and EIG simulation count unchanged. Control is the committed TAU2=4 family model. Treatment uses a Zellner-style prior on non-intercept regression coefficients with covariance g*(X'X)^-1 using g=30 (approximately the observational sample size); the intercept retains the benchmark prior variance 4. Use a numerically stabilized X'X + 1e-6 I when required. The same treatment family model must be used for marginal likelihood and posterior predictive simulation.

## Mechanics gate
Before prospective scoring, execute seeds 65101-65104 only as mechanics/invariant worlds. Verify finite family scores/posteriors, exact 29,281 DAG support, intervention spend <=15, deterministic replay, and no ground-truth access in action selection. These mechanics worlds are never pooled into efficacy results.

## Prospective screen after mechanics gate
Fresh seeds 65111-65122. Pass if mean treatment-minus-control terminal edge-error delta <= -0.10, mean Brier delta <= +0.005, and <=2/12 worlds worsen by >0.50. If passed, confirm on 65201-65224 with mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier <= +0.005, and <=3/24 large harms.

No R17-R22 efficacy worlds may be reused.