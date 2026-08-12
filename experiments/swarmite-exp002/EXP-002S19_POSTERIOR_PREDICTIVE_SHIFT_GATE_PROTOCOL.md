# EXP-002S19 — Posterior-Predictive Residual Shift Gate

Status: RUNNING after protocol freeze.

## Rationale
S17 and S18 retain strong structural gains but fail calibration under combined nonlinear mechanism and heavy-tailed noise shift. S18 showed that posterior-to-posterior disagreement geometry alone is insufficient. The next mechanism therefore adds an observable data-fit signal rather than another posterior threshold tweak.

## Frozen architecture
Keep the exact S17 compound-shift environment, baseline Gaussian planning posterior/controller, frozen S5 nonlocal science posterior, intervention budget, RNG semantics, and strict planning/science separation. No science or shift-detection quantity may influence action selection.

For each completed world compute:
- `D_sum`: total absolute edge-marginal disagreement between science and planning posteriors.
- `PPC_tail`: posterior-predictive tail mismatch. Using the planning posterior's terminal MAP DAG, fit its Gaussian family regressions on all rows where the child is not intervened. Standardize residuals by the fitted Gaussian predictive scale and compute the maximum across nodes of `abs(mean(z^4)-3)` after clipping |z| at 8 for numerical stability.
- `PPC_nonlinear`: nonlinear lack-of-fit. For the same residuals, compute the maximum absolute correlation between residual and `tanh(linear_predictor)` across nodes, treating undefined correlations as zero.

These are observable terminal diagnostics; ground truth is used only for across-world gate selection/evaluation.

## Training
Fresh seeds 69601-69624. Candidate gate form: promote when `D_sum <= a`, `PPC_tail <= t`, and `PPC_nonlinear <= n`.

Grid:
- a in {1.00, 1.25, 1.50, 2.00, 3.00}
- t in {0.50, 1.00, 2.00, 4.00, 8.00}
- n in {0.10, 0.20, 0.30, 0.45, 0.60}

Qualify a candidate only if coverage >=0.50, promoted mean edge delta <= -0.10, promoted mean Brier delta <= +0.005, and <=2 promoted worlds have edge harm >0.50. Select highest coverage; tie-break by lower Brier, lower edge delta, then stricter `(a,t,n)` lexicographically. Persist the full training grid and selected gate before validation exposure.

## Validation
Fresh seeds 69701-69724. Pass only if coverage >=0.50, promoted mean edge delta <= -0.10, promoted mean Brier delta <= +0.005, <=2 large harms, and exact planning-trace identity.

## Held-out confirmation
Only if validation passes: seeds 69801-69848. Promotion requires coverage >=0.50, promoted mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, promoted mean Brier delta <= +0.005, <=4 large harms, and exact planning-trace identity.

## Redirect rule
If this residual-aware detector fails validation, stop adding hand-engineered abstention thresholds and redirect to explicit model-class uncertainty / mixture-of-world-model terminal inference while retaining the planning/science separation invariant.