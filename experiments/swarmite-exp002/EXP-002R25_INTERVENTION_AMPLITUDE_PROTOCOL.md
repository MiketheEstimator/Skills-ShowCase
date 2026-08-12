# EXP-002R25 — Higher-Amplitude Interventions

## Hypothesis
Many prior/search modifications failed while the benchmark's action cost is independent of setpoint magnitude. In the linear-Gaussian SCM, larger do-intervention magnitudes should increase descendant signal-to-noise and causal identifiability per intervention-cost unit without requiring a different posterior model.

## Frozen treatment
Benchmark-v2, uniform DAG prior, TAU2=4, width-1 controller, budget 15, same candidate roles/targets and RNG namespaces. Control uses committed setpoints. Treatment multiplies every proposed setpoint by 2 before EIG scoring and environment execution: ±2 proposals become ±4 and ±1 proposals become ±2. Target costs are unchanged. Candidate target identities are otherwise identical to control at a given posterior state. Compute is tracked separately.

## Screen
Fresh paired seeds 65501-65512. Pass if mean terminal edge-error delta <= -0.10, mean Brier delta <= +0.005, and <=2/12 worlds worsen by >0.50. If passed, confirm on 65601-65624 requiring mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier <= +0.005, and <=3/24 large harms.

Ground truth is evaluation-only.