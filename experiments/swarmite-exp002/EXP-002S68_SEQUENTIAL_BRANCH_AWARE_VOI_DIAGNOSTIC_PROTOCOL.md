# EXP-002S68 — Sequential Branch-Aware Value-of-Information Diagnostic

## Hypothesis
The S67 failure arose because a static scalar summary of posterior-response dispersion discards the sequential decision value contained in distinct possible intervention outcomes. A truth-free two-stage lookahead score that preserves outcome branches will align better with realized acquisition value than static response disagreement and the frozen one-step EIG target.

## Frozen controls
- Benchmark mechanics, budget 15, S30/S46 terminal inference, intervention costs, and seed/regime construction remain unchanged.
- Google Drive is read-only and is not used for writes.
- S67 static disagreement and frozen baseline EIG are matched controls.
- Ground truth is used only after target scoring to measure realized acquisition value.

## Candidate representation
For every candidate first intervention target and setpoint {-2,+2}, draw posterior-predictive outcome branches from the frozen current posterior. For each branch, update the posterior and calculate the best available second-step EIG-per-cost across targets. Candidate score is immediate expected posterior entropy reduction per first-step cost plus the branch-probability-weighted best downstream EIG-per-cost. No truth labels enter this score.

## Prospective design
- Mechanics: 2 fresh worlds per regime.
- Diagnostic: 64 fresh worlds per regime (128 total), disjoint from S67.
- 8 posterior-predictive branches per setpoint/target.
- Compare candidate target with frozen EIG target using the same realized acquisition-value oracle used only for scoring in S66/S67.

## Success criteria
`BRANCH_VOI_ALIGNED` requires: positive-value AUC >= 0.60; Spearman(score, realized value) >= 0.10; mean realized value/cost >= frozen EIG; and no regime paired difference below -0.02.

AUC >= 0.56 without full qualification is `BRANCH_VOI_WEAK`. Otherwise `BRANCH_VOI_FALSIFIED`.

## Scientific redirects
- ALIGNED: freeze a resource-matched sequential planner policy test without terminal-inference changes.
- WEAK: preserve explicit branches but move from expected-value scalarization to risk-sensitive/set-valued branch utility.
- FALSIFIED: abandon posterior-derived scalar acquisition surrogates and diagnose intervention-response model misspecification/calibration directly.

No threshold, temperature, cap, S62/S65 localization, S67 disagreement-weight, or residual-likelihood retuning is permitted in this experiment.