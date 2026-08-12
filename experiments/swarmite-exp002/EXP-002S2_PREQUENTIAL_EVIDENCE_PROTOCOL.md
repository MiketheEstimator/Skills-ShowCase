# EXP-002S2 — Prequential Predictive Family Evidence

## Status
RUNNING after protocol freeze.

## Hypothesis
R21-R24 and S1 show that closed-form family marginal likelihood remains fragile under materially different coefficient and residual-scale priors. A prequential predictive-evidence score based on sequential out-of-sample prediction can reduce prior-volume sensitivity while preserving causal family discrimination.

## Frozen design
Keep benchmark-v2 world generator, uniform DAG prior, width-1 proposal portfolio, intervention budget 15, proposal RNG, real-environment RNG, and candidate count unchanged. Control remains the committed fixed-noise TAU2=4 benchmark.

Treatment replaces each family marginal-likelihood term with deterministic prequential log predictive evidence. For each node/family, order eligible rows by their existing deterministic acquisition order. Use the first 10 eligible rows as a warm-start fit under the benchmark TAU2=4 Gaussian regression model. Score every subsequent eligible row by one-step posterior predictive log density, updating the family posterior after each scored row. Interventional rows targeting the child node remain excluded exactly as in the benchmark. The resulting cumulative prequential score is used as the family score for DAG posterior construction. Posterior predictive simulation for EIG uses the corresponding current sequential Gaussian family posterior.

No ground-truth information may affect family scoring or action selection.

## Mechanics gate
Fresh seeds 66001-66004 only. Verify exact 29,281-DAG support, finite predictive scores/posteriors, deterministic replay, spend <=15, and row-order invariance to any metadata not used by the benchmark acquisition order. Persist executable lineage and gate before efficacy exposure.

## Prospective screen
Fresh seeds 66011-66022. Pass only if treatment-minus-control mean terminal edge-error delta <= -0.10, mean Brier delta <= +0.005, and <=2/12 worlds worsen by >0.50.

If passed, confirm on 66101-66124 with mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier delta <= +0.005, and <=3/24 large harms.

This is a model-selection evidence change, not another graph-prior, coefficient-prior, or residual-scale retry.