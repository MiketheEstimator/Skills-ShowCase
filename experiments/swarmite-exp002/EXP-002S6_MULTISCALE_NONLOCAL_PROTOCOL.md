# EXP-002S6 — Multiscale Nonlocal Included-Effect Prior

## Status
RUNNING after protocol freeze.

## Hypothesis
S5's nonlocal effect prior improved mean edge recovery but violated the large-harm guardrail because its narrow slab concentrated included effects near magnitude 0.65 while the frozen generator spans 0.4-0.9. A multiscale nonlocal slab can preserve low density near zero while reducing effect-size misspecification and catastrophic harms.

## Frozen treatment
Retain all benchmark-v2 mechanics and the S5 structural-evidence-only intervention. Replace each included-edge coefficient prior with an equal six-component mixture centered at ±0.45, ±0.65, and ±0.85, each Gaussian component having standard deviation 0.08. Intercept prior remains N(0,4). For k parents, integrate exactly over all 6^k coefficient-component assignments with equal weights. No realized ground truth may enter scoring.

Posterior-predictive EIG continues to use the benchmark full-data Gaussian family posterior so only structural family evidence changes.

## Mechanics gate
Fresh seeds 66601-66604. Verify exact DAG support, finite normalized posteriors, deterministic replay, spend <=15, and exact component enumeration.

## Prospective screen
Fresh seeds 66611-66622. Pass only if mean treatment-minus-control edge delta <= -0.10, mean Brier delta <= +0.005, and <=2/12 worlds have edge delta > +0.50.

If passed, confirm on 66701-66724 with mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier delta <= +0.005, and <=3/24 large harms.

S5 screen and confirmation worlds are excluded from S6 efficacy testing.