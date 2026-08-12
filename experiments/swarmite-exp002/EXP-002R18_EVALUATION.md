# EXP-002R18 Evaluation

## Disposition
COMPLETE_FALSIFIED_AT_SCREEN.

On fresh paired seeds 64301-64312, the hierarchical Beta-Binomial sparsity prior produced mean treatment-minus-control edge-error delta +0.008308, mean Brier delta +0.009064, 8 wins / 4 losses, 2/12 harms >0.50, and net MAP delta -2.

The preregistered screen required mean edge-error delta <= -0.10, mean Brier delta <= +0.005, and no more than 2/12 harms >0.50. The first two conditions failed, so confirmation was not opened.

The result narrows the mechanism: allowing latent world density improves directional consistency relative to the fixed R17 prior, but rare prior-misspecification failures still dominate mean terminal quality and calibration.

## Successor rationale
Test robust Bayesian contamination rather than stronger/weaker shrinkage. An explicit mixture prior that retains a uniform-prior floor can preserve hierarchical sparsity information while bounding the influence of a misspecified sparsity component.