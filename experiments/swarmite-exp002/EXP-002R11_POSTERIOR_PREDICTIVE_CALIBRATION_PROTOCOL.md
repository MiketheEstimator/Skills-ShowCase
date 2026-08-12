# EXP-002R11 — Posterior-Predictive Intervention Calibration Audit

## Motivation
EXP-002R6, R9, and R10 each changed a different component of decision quality without producing better terminal edge recovery: estimator-budget allocation, utility definition, and proposal diversity. This leaves the planner's posterior-predictive world model itself as a leading failure mechanism.

## Hypothesis
The frozen benchmark-v2 posterior predictive is materially miscalibrated for intervention outcomes in ways that distort expected-information rankings even when the graph posterior is internally coherent.

## Design
Use 12 fresh fixed worlds, seeds 58001 through 58012. For each world, construct the normal observational posterior from 30 passive samples. Evaluate the 10 unique hard interventions formed by all 5 targets crossed with setpoints {-2,+2}. For every intervention, generate 50 real-environment outcome rows using evaluation-only RNG namespaces and 50 posterior-predictive rows from the frozen inferred model. Ground truth remains unavailable to proposal or predictive generation and is used only to label evaluation outcomes.

## Primary calibration diagnostics
For each non-intervened variable and intervention action, compare posterior-predictive versus real-environment outcome distributions using mean error, variance ratio, empirical 90% interval coverage, and energy-distance-style sample discrepancy. Aggregate per action and per world.

## Decision relevance
Independently compute the frozen 30-simulation DAG-entropy EIG ranking for the same interventions. Test whether actions with larger predictive calibration error are more likely to be misranked relative to realized one-step posterior improvement and terminal forced-action recovery from the R7-style continuation audit.

## Success criterion
Support posterior-predictive miscalibration as a decision failure mechanism only if calibration error is materially nonzero across worlds and positively associated with EIG ranking error / terminal regret. If calibration is good or unrelated to decision failure, falsify this mechanism and redirect toward genuinely multi-step value-of-information planning.

## Checkpoint discipline
Persist each world atomically. The fixed seeds and evaluation sample counts are frozen before execution.