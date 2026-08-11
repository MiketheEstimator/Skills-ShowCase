# EXP-002R27 — Nonlinear Transfer of Confirmed 2x Amplitude

## Status
RUNNING after R25 support and R26 non-promotion.

## Hypothesis
The confirmed 2x amplitude benefit may depend on correctly specified linear SCMs. Stronger interventions could remain beneficial under moderate nonlinear structural equations by increasing causal signal, or could fail because large setpoints amplify model misspecification. This experiment tests that uncertainty directly.

## Fresh nonlinear transfer benchmark
Retain benchmark-v2 DAG generation, node costs, observational sample count, budget 15, and Gaussian exogenous noise. For each true edge, deterministically assign one effect family from {linear, tanh, centered-quadratic} using an isolated `r27-effect-type` RNG namespace. Edge coefficient magnitudes/signs remain those from benchmark-v2. Contributions are: linear `w*x`; tanh `1.5*w*tanh(x)`; centered-quadratic `0.5*w*(x*x-1)`. Structural equations sum parent contributions plus N(0,1) noise. Interventions remain perfect do-setpoints.

## Inference intentionally unchanged
Both policies continue using the committed linear-Gaussian benchmark-v2 Bayesian inference and EIG model. This is a transfer/misspecification test, not a nonlinear-aware estimator test.

## Comparison
Control uses original 1x setpoints. Treatment is the confirmed R25 2x amplitude policy. Candidate roles/targets, intervention-cost budget, and planner simulation counts remain otherwise matched. Real-environment RNG uses isolated R27 namespaces.

## Screen
Fresh seeds 65901-65912. Pass if mean treatment-minus-control edge-error delta <= -0.10, mean Brier delta <= +0.005, and <=2/12 harms >0.50. If passed, confirm on 66001-66024 requiring mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier <= +0.005, and <=3/24 large harms.

Ground truth is evaluation-only.