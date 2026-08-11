# EXP-002R24 — Frozen-Design g-Prior

## Status
RUNNING after R23 falsification.

## Hypothesis
R23's treatment recomputed the g-prior from the evolving post-intervention design, making the prior data-dependent at every step. Freezing the g-prior covariance from the initial observational design before any intervention restores sequential coherence and may retain dimension-aware coefficient regularization without the R23 instability.

## Frozen treatment
Benchmark-v2, uniform DAG prior, width-1 controller, budget 15. Control remains the committed TAU2=4 model. Treatment constructs, once from the initial 30 observational rows, a family-specific Zellner prior covariance with g=30 for non-intercept coefficients and intercept variance 4, stabilized with X'X+1e-6 I. These prior precision matrices and normalizers are then held fixed for every subsequent likelihood update and posterior-predictive calculation. No intervention data may alter the prior itself.

## Mechanics gate
Seeds 65301-65304 only. Require finite scores/posteriors, exact 29,281 DAG support, deterministic replay, spend <=15, and byte-identical frozen prior matrices before/after the trajectory. Mechanics worlds are never efficacy data.

## Prospective screen
Fresh seeds 65311-65322. Pass if mean edge-error delta <= -0.10, mean Brier delta <= +0.005, and <=2/12 harms >0.50. If passed, confirm on 65401-65424 with mean edge delta <= -0.10, bootstrap 95% upper bound <0, Brier <= +0.005, and <=3/24 large harms.

Ground truth is evaluation-only.