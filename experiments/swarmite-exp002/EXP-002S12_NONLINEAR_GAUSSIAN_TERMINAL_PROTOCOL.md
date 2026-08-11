# EXP-002S12 — Nonlinear Gaussian Terminal Inference

## Status
RUNNING after protocol freeze.

## Hypothesis
S10 showed that planning/inference separation retains structural benefit under nonlinear mechanism shift but violates the Brier guardrail. The exploratory S11 diagnostic showed that simply combining the correct `tanh(parent)` feature map with the S5 nonlocal coefficient prior is structurally harmful. Therefore the active uncertainty is whether the calibration failure comes from model-form misspecification or from the nonlocal coefficient prior under nonlinear features.

## Frozen treatment
Use exactly the S10 nonlinear worlds and baseline planning posterior. Planning actions and environmental observations are generated exactly as in S10. Terminal treatment inference alone uses the same Gaussian linear-family evidence calculation as benchmark v2, except every candidate parent column is replaced by `tanh(x_parent)` before fitting. Coefficient prior remains the original zero-mean Gaussian with TAU2=4.0; no nonlocal prior, sparsity penalty, retuning, or planning feedback is allowed.

## Controls
Primary control: original benchmark-v2 linear Gaussian terminal posterior on the identical nonlinear data and trace. Secondary comparator: frozen S10 linear nonlocal terminal posterior on the same data. All three receive identical observations by construction.

## Mechanics gate
Fresh seeds 67601-67604. Require exact 29,281 DAG support, normalized finite terminal posterior, spend <=15, and identical planning trace for every comparator.

## Prospective screen
Fresh seeds 67611-67622. Pass only if treatment vs primary baseline has mean edge delta <= -0.10, mean Brier delta <= 0.000, <=2/12 worlds worsen edge error by >0.50, and every trace is identical. Also report treatment deltas vs S10 but do not use them to rescue a failed primary screen.

## Confirmation
Only if screen passes, run fresh seeds 67701-67724. Promotion requires treatment vs primary baseline mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier delta <=0.000, <=3/24 large harms, and exact trace identity.

## Falsification redirect
If this exact nonlinear Gaussian science posterior fails, conclude that correct mechanism-form representation alone is insufficient. Redirect toward model averaging or a mixture science posterior that can hedge linear/nonlinear structural families without altering planning.