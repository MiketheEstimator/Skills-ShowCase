# EXP-002S4 — Blocked Cross-Validated Predictive Family Evidence

## Status
RUNNING after protocol freeze.

## Hypothesis
S2 failed because its unscored 10-row warm-start gave larger parent sets free fitting capacity, producing a systematic dense-graph bias. A genuinely held-out predictive family score in which every eligible row is scored out of sample can preserve predictive discrimination without the warm-start density pathology.

## Frozen design
Keep benchmark-v2 world generator, uniform DAG prior, width-1 proposal portfolio, intervention budget 15, proposal RNG, real-environment RNG, candidate count, coefficient prior TAU2=4, and known residual variance 1 unchanged. Control is the committed benchmark-v2 fixed-noise marginal-likelihood arm.

Treatment changes only family model-selection evidence. For each child/family, eligible rows remain those whose intervention target is not the child. Partition eligible rows deterministically by acquisition-order index modulo 5. For each fold, fit the benchmark Gaussian regression posterior on the other four folds starting from the same TAU2=4 prior, then sum one-step posterior-predictive log densities for rows in the held-out fold without updating on those held-out outcomes. Sum all five held-out fold scores to obtain the family score used for DAG posterior construction. Every eligible row is therefore scored exactly once out of sample and no row is granted as an unscored warm-start.

For posterior-predictive EIG simulation, use the ordinary full-data Gaussian family posterior under TAU2=4; only DAG family evidence changes. No ground truth may affect scoring or action selection.

## Mechanics gate
Fresh seeds 66201-66204. Verify exact 29,281-DAG support, finite normalized posteriors, deterministic replay, spend <=15, exactly-once held-out scoring for every eligible row, and deterministic acquisition-order fold assignment. Persist runner and gate before efficacy exposure.

## Prospective screen
Fresh seeds 66211-66222. Pass only if treatment-minus-control mean terminal edge-error delta <= -0.10, mean Brier delta <= +0.005, and <=2/12 worlds worsen by >0.50.

If passed, confirm on fresh seeds 66301-66324. Promotion requires mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier delta <= +0.005, and <=3/24 large harms.

## Scientific distinction
This is not another graph prior, coefficient prior, residual-scale model, or warm-start prequential retry. It changes the evidence estimator to deterministic held-out predictive scoring specifically to test the density mechanism supported by S3.