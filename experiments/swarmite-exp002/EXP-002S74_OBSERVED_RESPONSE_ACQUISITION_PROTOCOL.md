# EXP-002S74 — Observed Intervention-Response Acquisition Model Diagnostic

## Hypothesis
Acquisition value is better predicted from **already observed intervention-response transitions** than from posterior-predictive branch summaries. A truth-free model using accumulated empirical intervention responses can identify which next target yields structural information beyond frozen EIG.

## Why this is the next experiment
S67, S68, and S73 falsified increasingly rich posterior-predictive acquisition summaries; S70-S72 also failed to repair the predictive response distribution by calibration. S74 moves upstream to empirical transitions already present in the acquired dataset and does not reuse those failed score families.

## Frozen design
- Mechanics: 2 fresh worlds/regime.
- Training: 64 fresh worlds/regime.
- Held-out diagnostic: 64 fresh worlds/regime, disjoint from training.
- Baseline planner/state, intervention budget, S30 terminal inference, and EIG control remain frozen.
- For each candidate intervention target, construct truth-free features from the accumulated data: target intervention count/fraction; candidate-column observational/interventional mean and variance contrasts; absolute standardized mean shift; and aggregate response-vector mean/variance displacement between rows where that target was intervened and non-target rows. Missing empirical target histories are encoded explicitly and shrunk to neutral features.
- Fit a regularized linear acquisition-value model on training worlds only. Standardization and coefficients are frozen before held-out evaluation.
- Ground truth is used only to compute realized acquisition value labels and held-out scoring.

## Primary metrics
1. AUC for positive realized acquisition value.
2. Spearman correlation between predicted and realized acquisition value.
3. Mean realized value/cost of the model-selected target versus frozen EIG.
4. Fraction of matched worlds in which model selection beats EIG.
5. Regime-specific paired value/cost differences.

## Frozen disposition
SUPPORTED if held-out AUC >= 0.60, Spearman >= 0.15, model mean value/cost >= EIG, and neither regime paired difference < -0.02.
WEAK if AUC >= 0.56 or Spearman >= 0.10 without satisfying support.
FALSIFIED otherwise.

## Successor logic
- SUPPORTED: freeze the model and run a resource-matched prospective planner policy test.
- WEAK: test set-valued empirical transition histories / uncertainty-aware empirical acquisition, without coefficient retuning.
- FALSIFIED: abandon scalar acquisition prediction from both posterior-predictive and simple empirical-transition summaries; move to direct intervention-response representation learning / target-conditional transition geometry.
