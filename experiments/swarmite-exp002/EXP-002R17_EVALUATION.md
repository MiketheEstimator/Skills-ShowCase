# EXP-002R17 Evaluation

## Disposition
COMPLETE_FALSIFIED_ON_VALIDATION.

The frozen training grid selected lambda=1.0 from seeds 64001-64024. That selection was durably persisted before validation.

On the preregistered validation seeds 64101-64112, lambda=1.0 versus lambda=0 produced mean terminal edge-error delta +0.405388, mean Brier delta +0.027320, 5 wins / 7 losses, 5/12 worlds with edge-error harm >0.50, and net MAP delta -5.

The preregistered validation gate required mean edge-error delta <= -0.10, mean Brier delta <= +0.005, and no more than 2/12 harms >0.50. All three conditions failed. Held-out seeds 64201-64224 therefore remain uninspected.

## Interpretation
The training benefit did not generalize. Fixed global shrinkage toward the generator's marginal edge probability is unsafe across worlds and appears vulnerable to density mismatch/heterogeneity. A diagnostic-only correlation between true edge count and validation edge harm was positive (~0.45), but true density is ground truth and cannot be used for policy gating.

## Successor
Test a materially different inference mechanism: a hierarchical Beta-Binomial DAG sparsity prior that treats per-world edge density as latent rather than forcing a fixed p=0.35 penalty. This preserves generator-informed regularization while allowing density uncertainty without ground-truth leakage.