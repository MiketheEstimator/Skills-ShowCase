# EXP-002S9 — Dual-Posterior Transfer Under Effect-Size Shift

## Status
RUNNING after protocol freeze.

## Hypothesis
S8 is supported in benchmark-v2, but its structural posterior encodes a nonzero-effect gap centered near magnitude 0.65. The architecture should be considered robust only if its inference gain survives plausible effect-size distribution shift without changing the planning policy.

## Frozen transfer worlds
Use the benchmark-v2 DAG topology generator and all observation/intervention mechanics unchanged, but replace nonzero coefficient magnitudes with Uniform(0.15,0.90), preserving random signs. This introduces genuinely weaker causal effects that overlap the near-zero region absent from the training benchmark while keeping graph density, noise, costs, budget, and interventions comparable.

Control uses committed benchmark-v2 planning and inference on the shifted worlds. Treatment uses the exact S8 dual-posterior architecture without retuning: baseline posterior controls every action; the frozen S5 nonlocal structural posterior is terminal output only. Action traces must remain identical by construction.

## Mechanics gate
Fresh seeds 67001-67004. Verify shifted-world construction, exact 29,281-DAG inference support, deterministic replay, spend <=15, and treatment/control trace identity.

## Prospective screen
Fresh seeds 67011-67022. Transfer is supported at screen only if mean edge delta <= -0.10, mean Brier delta <= +0.005, <=2/12 worlds worsen by >0.50, and all action traces are identical.

If passed, confirm on 67101-67124 with mean edge delta <= -0.10, paired bootstrap 95% upper bound <0, mean Brier delta <= +0.005, <=3/24 large harms, and exact trace identity.

If falsified, do not retune on the same worlds. Redirect to an adaptive or mixture structural posterior using fresh training/validation/test partitions.