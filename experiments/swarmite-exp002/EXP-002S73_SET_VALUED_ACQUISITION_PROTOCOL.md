# EXP-002S73 — Set-Valued Empirical Acquisition Utility Diagnostic

## Hypothesis
The S70-S72 failures may reflect a mismatch between marginal response calibration and the planner's actual decision objective. Even when predictive response intervals are miscalibrated, the empirical posterior-predictive *family of structural outcomes* induced by an intervention may still contain useful information about acquisition value.

## Mechanism
Do not calibrate response means, variances, or intervals. For each candidate intervention target and setpoint, draw a frozen empirical family of posterior-predictive outcomes from the current posterior. Update the structural posterior separately for every draw and compute the empirical distribution of immediate edge-marginal displacement from the current posterior. Define a set-valued acquisition score as a conservative upper-tail summary of that structural displacement distribution, normalized by intervention cost.

This is materially different from S67 static response disagreement, S68 mean branch VOI, and S70-S72 response calibration: S73 preserves the empirical distribution of *structural posterior changes* and scores its upper quantile rather than collapsing simulated responses to a scalar mean or calibrated response interval.

## Frozen design
- Baseline planner/control: frozen EIG target selection.
- Candidate: empirical 75th percentile of branch structural edge displacement per intervention cost.
- Branches: 32 posterior-predictive draws per target/setpoint, pooled across setpoints.
- Mechanics: 2 fresh worlds per regime.
- Diagnostic: 64 fresh worlds per regime (128 total), disjoint seed namespace.
- Realized acquisition value: same matched one-step intervention value/cost definition used by S66-S68.
- Ground truth is scoring-only and never enters candidate score construction.

## Metrics
1. AUC for positive realized acquisition value.
2. Spearman correlation of candidate score with realized value.
3. Candidate vs frozen EIG mean realized value/cost.
4. Paired candidate-minus-EIG value/cost overall and by regime.
5. Fraction of worlds candidate beats EIG.

## Preregistered disposition
SUPPORTED if AUC >= 0.60, Spearman >= 0.10, candidate mean value/cost >= EIG, and each regime paired difference >= -0.02.
WEAK if AUC >= 0.56 but support criteria fail.
Otherwise FALSIFIED.

## Successor logic
- SUPPORTED: freeze the score and run a prospective resource-matched planner policy test without retuning.
- WEAK: test distributional risk/ambiguity utility using the same empirical structural families, without changing branch generation.
- FALSIFIED: abandon posterior-predictive branch summaries as acquisition utilities and redirect toward direct intervention-response model learning from accumulated observed intervention data.
