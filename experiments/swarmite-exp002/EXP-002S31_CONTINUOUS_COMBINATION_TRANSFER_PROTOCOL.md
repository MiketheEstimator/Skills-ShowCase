# EXP-002S31 — Continuous Science-Posterior Combination Transfer Stress

## Status
Protocol frozen before any S31 world is executed.

## Objective
Test the exact S30 terminal architecture without retuning on previously unseen mechanism/noise families. The S30 temperature is frozen at `T=5.0`; planning remains the exact baseline controller.

## Hypothesis
ADEQ-weighted continuous mixing between the baseline and S23 robust terminal posteriors will preserve low harm in-distribution and deliver net structural improvement across novel model shifts that were not present in S30 training, validation, or confirmation.

## Frozen terminal rule
For every world:
1. Generate interventions using only the baseline posterior/controller.
2. Compute terminal baseline posterior `p0`.
3. Compute frozen S23 robust posterior `pr`.
4. Compute direct 5-fold predictive adequacy `ADEQ = robust_cv_logscore - baseline_cv_logscore` using the exact S29 scoring mechanics on that world's observed terminal dataset.
5. Set `alpha = sigmoid(ADEQ / 5.0)`.
6. Return `pmix = (1-alpha)*p0 + alpha*pr` as the treatment science posterior.

No threshold, temperature, class prior, feature, or other parameter may be changed.

## Stress regimes
Regime is assigned only by seed modulo 4 for simulation/evaluation and is never visible to the terminal rule.

1. `linear_gaussian_anchor` — exact benchmark-v2 environment.
2. `sin_gaussian` — structural contribution uses `sin(parent)` with Gaussian N(0,1) noise.
3. `asinh_t7` — structural contribution uses `asinh(parent)` with Student-t7 noise scaled to unit variance.
4. `leakyrelu_contaminated` — structural contribution uses leaky-ReLU(parent), slope 0.2 for negative values, with 90% N(0,1) / 10% N(0,3^2) contamination, rescaled to unit marginal variance.

World DAG generation, coefficient magnitudes, intervention costs, budget, proposals, EIG simulations, and RNG namespace discipline remain benchmark-v2 except for the explicitly frozen environment mechanism/noise functions.

## Worlds
- Mechanics gate: seeds 71700-71703, one per regime. These are excluded from efficacy pooling.
- Held-out transfer confirmation: seeds 71800-71895 (96 worlds, 24 per regime).
- No S31 training or tuning stage exists.

## Mechanics gate
All four mechanics worlds must satisfy:
- exact 29,281-DAG support;
- spend <=15;
- baseline posterior reconstruction error <=1e-10;
- baseline, robust, and mixed posteriors finite and normalized;
- ADEQ finite;
- action trace generated only by the baseline planner.

Failure blocks efficacy interpretation.

## Transfer success criteria
S31 supports transfer only if all hold on the 96 confirmation worlds:
1. overall mean mixed edge delta <= -0.10;
2. paired bootstrap 95% upper bound <0;
3. overall mean mixed Brier delta <= +0.005;
4. <=8/96 worlds worsen by >0.50 edge-error units;
5. linear-Gaussian anchor mean mixed edge delta <= +0.05 and Brier <= +0.005;
6. each unseen regime has mean mixed edge delta <0;
7. at least two of three unseen regimes have bootstrap 95% upper bound <0;
8. each unseen regime mean Brier delta <= +0.010.

## Interpretation and redirect
If supported, promote ADEQ-weighted continuous terminal posterior combination as the current reference science architecture and move to scale/generalization tests (larger graph/hypothesis spaces).

If falsified, do not retune T or add hard gates. Diagnose the failing unseen regime and whether the missing capability is mechanism representation, noise representation, or posterior model-set coverage before expanding the model set.
