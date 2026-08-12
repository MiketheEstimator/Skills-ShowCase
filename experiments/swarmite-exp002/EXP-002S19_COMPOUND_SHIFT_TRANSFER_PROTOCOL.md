# EXP-002S19 — Fixed Disagreement Gate Under Compound Model Shift

## Status
RUNNING after protocol freeze.

## Hypothesis
The frozen S15 disagreement gate D<=1.50 has now transferred independently to nonlinear mechanisms, standardized heavy-tailed noise, and latent residual confounding. A stronger test is whether the same architecture works when all three shifts occur simultaneously without retuning.

## Frozen worlds
Use benchmark-v2 DAG topology and coefficients. Replace linear parent effects with `tanh(parent)*W`, replace Gaussian structural noise with standardized Student-t(df=3) noise, and add one deterministic latent residual factor to a deterministic pair of observed nodes using rho=0.60 while keeping each pair-node residual variance normalized. Interventions override the target node exactly. Costs, budget, and observation count remain unchanged.

## Frozen architecture
Planning remains the original benchmark-v2 Gaussian planner. Terminal science inference remains the frozen S10/S5 nonlocal posterior. Promote structural output only when the frozen S15 disagreement score D<=1.50; otherwise return ABSTAIN_MODEL_SHIFT. No retuning or extra gate is permitted.

## Mechanics
Seeds 69701-69704. Require deterministic replay, exact 29,281 DAG support, finite normalized posteriors, spend<=15, and trace identity.

## Screen
Seeds 69711-69722. Pass if coverage>=0.50, promoted mean edge delta<=-0.10, promoted mean Brier delta<=+0.005, <=2 promoted large harms, and trace identity.

## Confirmation
If screen passes, seeds 69801-69824. Require coverage>=0.50, promoted mean edge delta<=-0.10, bootstrap 95% upper bound<0, promoted mean Brier delta<=+0.005, <=3 promoted large harms, and trace identity.

## Redirect
If falsified, conclude independent-shift robustness does not compose and redirect toward a multi-signal model-shift gate or a structural ensemble rather than retuning D on exposed compound worlds.