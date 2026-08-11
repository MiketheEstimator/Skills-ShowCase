# EXP-002R10 — Orthogonal Intervention Action-Space Test

## Motivation
EXP-002R9 found that the normal width-2 portfolio produced only 4.5 unique intervention actions on average from 10 role-labeled candidates at decision 0. Edge-centric reward replacement did not solve terminal alignment. This suggests the proposal portfolio may be semantically redundant even when role labels differ.

## Hypothesis
At matched candidate count and planner simulations, replacing role-derived duplicate proposals with an orthogonalized set of 10 unique interventions will improve terminal edge recovery.

## Treatment action set
At every decision, treatment proposes exactly the 10 unique hard interventions `(target, setpoint)` formed by all 5 variables crossed with setpoints `{-2,+2}`. Role label is `ORTHOGONAL`. Candidates exceeding remaining intervention budget are filtered exactly as in the control.

## Control
Frozen benchmark-v2 width-2 portfolio: two swarms × five roles, with duplicates retained exactly as currently implemented.

## Matched resources
- Same fresh paired worlds and initial observational data.
- Same intervention budget 15.
- Same 3 posterior-predictive EIG simulations per affordable candidate.
- Candidate count is 10 before affordability filtering in both arms.
- Planner simulation counts are tracked exactly; affordability may create small path-dependent total differences.
- Environment RNG remains keyed by world seed, step, target, and setpoint.

## Primary metric
Paired terminal edge-error difference: orthogonal action space minus frozen width-2 control. Lower is better.

## Secondary metrics
MAP recovery, Brier score, true-DAG mass, entropy, intervention count, planner simulations, unique candidate actions per step, and selected target diversity.

## Initial screen
12 fixed fresh worlds, seeds 57001 through 57012.

## Success / falsification
Promote only if treatment lowers mean paired edge error, wins at least 7 of 12 worlds, and does not materially increase planner simulations. A null/adverse result falsifies simple action-space orthogonalization and redirects toward posterior-model calibration or multi-step utility rather than further proposal diversification retries.