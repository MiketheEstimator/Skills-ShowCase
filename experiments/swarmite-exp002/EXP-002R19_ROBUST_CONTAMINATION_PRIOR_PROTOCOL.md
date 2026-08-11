# EXP-002R19 — Robust Contamination Sparsity Prior

## Hypothesis
R18's rare catastrophic harms arise from prior misspecification. A coherent 50/50 mixture prior between the uniform DAG prior and the R18 hierarchical sparsity prior will retain useful sparsity information while bounding misspecification damage.

## Frozen treatment
Benchmark-v2 width-1 portfolio controller. Control: uniform DAG prior. Treatment: prior weight for DAG g is 0.5*U(g)+0.5*H(g), where U is uniform over the 29,281 DAGs and H is the normalized R18 Beta-Binomial DAG-size prior with Beta(1.75,3.25) latent edge probability. All intervention budgets, proposal mechanics, EIG simulations, and RNG namespaces remain matched.

## Screen
Fresh paired seeds 64501-64512. Pass only if mean edge-error delta <= -0.10, mean Brier delta <= +0.005, and <=2/12 worlds worsen by >0.50. If passed, confirm on seeds 64601-64624 with mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, Brier <= +0.005, and <=3/24 harms >0.50.

Ground truth is evaluation-only.