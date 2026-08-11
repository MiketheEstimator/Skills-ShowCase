# EXP-002S16R — Fresh Reproducible Noise-Shift Transfer Recovery

Status: RUNNING after protocol and executable freeze.

## Why this recovery exists
EXP-002S16 became nonpoolable after conflicting same-seed results were produced without a common source-addressed noise kernel. S16R repeats the scientific question only with fresh worlds and an executable frozen before efficacy exposure.

## Frozen executable
Use `experiments/swarmite-exp002/swarmite_exp002_s16_noise.py`, committed as `128325fbbc5e243cac54299f4a97bdf122682fdc` before any S16R seed is executed.

The environment uses the benchmark-v2 linear DAG/coefficient generator and standardized Student-t(df=3) structural noise. For every environment row, exactly five independent t innovations are drawn as one vector from the environment RNG before topological traversal, then divided by sqrt(3); an intervened node consumes its already-drawn innovation without using it. Observation and intervention RNG namespaces remain the benchmark-v2 `('v2','obs',seed)` and `('v2','env',seed,step,target,setpoint)` namespaces.

Planning remains the original Gaussian benchmark-v2 posterior and portfolio controller. Terminal science inference remains the frozen S5 nonlocal posterior. Structural promotion uses the previously selected S15 disagreement threshold D <= 1.50. No retuning.

## Fresh worlds
Mechanics: 68901-68904.
Screen: 68911-68922.
Confirmation if screen passes: 69001-69024.

## Mechanics gate
Require deterministic replay, exactly 29,281 DAGs, finite normalized planning/science posteriors, spend <=15, and exact planning-trace identity by construction.

## Screen criteria
Coverage >=0.50; promoted mean edge delta <= -0.10; promoted mean Brier delta <= +0.005; <=2 promoted edge harms >0.50; exact planning-trace identity.

## Confirmation criteria
Coverage >=0.50; promoted mean edge delta <= -0.10; paired bootstrap 95% upper bound <0; promoted mean Brier delta <= +0.005; <=3 promoted edge harms >0.50; exact planning-trace identity.

A null or adverse result is a valid completed falsification. No S16 historical world may be pooled into S16R.