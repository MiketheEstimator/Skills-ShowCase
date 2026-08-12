# EXP-002R26 — 3x vs Confirmed 2x Intervention Amplitude

## Status
RUNNING after EXP-002R25 support.

## Hypothesis
The R25 gain may continue with stronger linear interventions. Tripling the benchmark's original setpoints may improve causal signal beyond the confirmed 2x policy without increasing terminal harm.

## Frozen comparison
Use benchmark-v2, uniform DAG prior, TAU2=4, width-1 controller, budget 15, identical candidate roles/targets and RNG namespaces. Control is the confirmed R25 policy with proposed setpoints multiplied by 2. Treatment multiplies original setpoints by 3. Target costs remain unchanged. Both policies score their own amplitude-adjusted actions with the same EIG simulator.

## Screen
Fresh paired seeds 65701-65712. Promote only if treatment-minus-2x-control mean edge-error delta <= -0.10, mean Brier delta <= +0.005, and <=2/12 worlds worsen by >0.50. If passed, confirm on seeds 65801-65824 with mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier <= +0.005, and <=3/24 large harms.

If 3x fails, retain 2x as the supported amplitude policy and redirect to generalization testing rather than trying arbitrary larger amplitudes.