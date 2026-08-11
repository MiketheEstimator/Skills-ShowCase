# EXP-002R18 — Hierarchical Sparsity Prior

## Status
RUNNING after R17 validation falsification.

## Hypothesis
R17 failed because a fixed global sparsity penalty cannot accommodate world-to-world density heterogeneity. Treating edge probability as a latent per-world quantity under a Beta prior centered on the generator rate can preserve useful sparsity information while reducing catastrophic over-shrinkage.

## Frozen treatment
Use benchmark-v2, width-1 portfolio controller, budget 15, and all existing RNG namespaces unchanged. Control is the committed uniform DAG prior. Treatment replaces the uniform prior with a Beta-Binomial DAG-size prior obtained by integrating a latent edge probability p over Beta(a=1.75,b=3.25), mean 0.35 and concentration 5: log prior(k) proportional to log B(k+a,10-k+b)-log B(a,b), where k is DAG edge count. No ground-truth information is used by the controller.

## Screen
Fresh paired seeds 64301-64312. Promotion to a 24-world confirmation requires mean treatment-minus-control terminal edge-error delta <= -0.10, mean Brier delta <= +0.005, and no more than 2/12 worlds worsening by >0.50 edge-error units. Otherwise treat as completed falsification and redirect.

## Confirmation if screen passes
Fresh seeds 64401-64424. Promotion requires mean edge-error delta <= -0.10, paired bootstrap 95% upper bound < 0, mean Brier delta <= +0.005, and no more than 3/24 worlds worsening by >0.50.

## Scientific controls
Matched intervention budget, proposal generation, EIG simulations, environment RNG, and observational data. R16/R17 seeds are excluded. Ground truth is used only for terminal evaluation.
