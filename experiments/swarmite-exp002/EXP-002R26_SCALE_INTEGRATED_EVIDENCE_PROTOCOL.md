# EXP-002R26 — Scale-Integrated Family Evidence Recovery

## Status
RUNNING after protocol freeze.

## Recovery rationale
EXP-002R25 was blocked before efficacy exposure because its intended runner namespace collided with a pre-existing unrelated executable. R26 recovers the same scientific question under a clean, unique lineage without reusing any R25 mechanics or efficacy worlds.

## Hypothesis
The dense-graph distortions seen in R21-R24 may arise from fixed residual variance in the family evidence model. Integrating residual-scale uncertainty with exact conjugate Normal-Inverse-Gamma evidence and Student-t posterior predictive scoring may improve terminal structural recovery.

## Frozen treatment
Keep benchmark-v2, uniform DAG prior, width-1 proposal portfolio, intervention budget 15, proposal RNG, real-environment RNG, and three predictive planner simulations per candidate unchanged. Control is the committed TAU2=4 fixed-noise benchmark.

Treatment uses beta | sigma^2 ~ Normal(0, sigma^2 * 4 I), including intercept, and sigma^2 ~ Inverse-Gamma(a0=3,b0=2), prior mean 1. Use exact NIG marginal likelihood and exact Student-t posterior predictive simulation/scoring.

## Mechanics gate
Fresh mechanics-only seeds 65501-65504. Verify finite family evidence and predictive scales, posterior normalization over exactly 29,281 DAGs, deterministic replay, spend <=15, and no ground-truth access during action selection. Persist executable and mechanics gate before efficacy exposure.

## Prospective screen
Fresh seeds 65511-65522. Pass only if treatment-minus-control mean terminal edge-error delta <= -0.10, mean Brier delta <= +0.005, and <=2/12 worlds worsen by >0.50.

If screen passes, confirm on 65601-65624 with mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier delta <= +0.005, and <=3/24 large harms.

Persist posterior expected graph size as a secondary terminal diagnostic only. No R17-R25 efficacy worlds may be reused.