# EXP-002R29 — Soft-Intervention Transfer of Confirmed 2x Amplitude

## Status
RUNNING after R28.

## Hypothesis
The confirmed 2x amplitude policy may retain or increase its advantage when interventions are imperfect because stronger requested setpoints can preserve realized separation under partial compliance. Conversely, the unchanged perfect-do inference model may make stronger interventions more harmful under intervention misspecification.

## Fresh transfer benchmark
Use benchmark-v2 linear SCMs and all original DAG/weight generation. Actual target interventions have fixed efficacy alpha=0.8: on a targeted node, realized value is `alpha*setpoint + (1-alpha)*(parent_linear_contribution + epsilon)` with epsilon~N(0,1). Untargeted nodes follow the original structural equations. Observational data are unchanged. Both inference policies intentionally continue treating targeted rows as perfect do-interventions, so this is a misspecification transfer test.

## Comparison
Control uses original 1x setpoints. Treatment uses the confirmed R25 2x amplitudes. Same budget, proposal roles, target costs, EIG simulation counts, and isolated RNG namespaces.

## Screen
Fresh paired seeds 66101-66112. Pass if mean edge-error delta <= -0.10, mean Brier delta <= +0.005, and <=2/12 harms >0.50. If passed, confirm on 66201-66224 requiring mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier <= +0.005, and <=3/24 large harms.

Ground truth is evaluation-only.