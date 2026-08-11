# EXP-002S17 — Fixed Disagreement Gate Under Latent Residual Confounding

## Status
RUNNING after protocol freeze.

## Hypothesis
S15-S16 show that the frozen D<=1.50 disagreement gate transfers across nonlinear mechanisms and heavy-tailed noise. A harder unresolved shift is causal insufficiency: correlated residual variation from an unobserved common factor. The fixed gate should abstain when baseline and science posteriors become dangerously inconsistent and preserve calibrated structural gains on promoted worlds.

## Frozen worlds
Use benchmark-v2 DAGs, linear directed mechanisms, coefficient generator, interventions, costs, observation count, and budget. For each world choose one deterministic pair of distinct observed nodes from an isolated RNG namespace. At each sample draw a latent standard-normal factor L. For the selected pair, nonintervened structural noise is `sqrt(1-rho^2)*epsilon + rho*L` with rho=0.60; all other nodes use independent N(0,1) noise. Interventions override the targeted node exactly. Ground-truth scoring remains only the observed directed DAG; the latent factor is intentionally omitted from the inference model.

## Frozen architecture
Planning remains benchmark-v2 Gaussian planning. Terminal science inference remains frozen S10/S5 nonlocal. Use the fixed S15 gate D<=1.50 with no retuning; otherwise abstain as model-shift-sensitive.

## Mechanics
Seeds 68901-68904. Require deterministic latent-pair replay, exact 29,281 DAG support, finite normalized posteriors, spend<=15, and identical traces.

## Screen
Seeds 68911-68922. Pass if coverage>=0.50, promoted mean edge delta<=-0.10, promoted mean Brier delta<=+0.005, <=2 promoted large harms, and trace identity.

## Confirmation
If screen passes, seeds 69001-69024. Require coverage>=0.50, promoted mean edge delta<=-0.10, bootstrap 95% upper bound<0, promoted mean Brier delta<=+0.005, <=3 promoted large harms, and trace identity.

## Redirect
If falsified, treat latent confounding as outside the fixed-gate robustness envelope and redirect toward an explicit residual-dependence detector or latent-variable science model rather than retuning D on exposed worlds.