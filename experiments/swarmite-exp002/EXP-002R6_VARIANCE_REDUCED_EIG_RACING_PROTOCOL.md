# EXP-002R6 — Compute-Matched Variance-Reduced EIG Racing

## Motivation
EXP-002R5 found that the deployed 3-simulation EIG judge is extremely noisy and that extra-swarm winners exhibit greater positive selection optimism than base-swarm winners. This suggests width-2 may waste its larger proposal set by maximizing Monte-Carlo noise.

## Hypothesis
At identical width-2 proposal breadth, intervention budget, and per-decision planner-simulation budget, a two-stage racing estimator will improve terminal scientific recovery relative to the frozen 3-simulation-per-candidate width-2 baseline by reducing winner's-curse selection error.

## Mechanism
For every decision, generate the exact same width-2 candidate set. Control uses 3 posterior-predictive simulations per affordable candidate. Treatment uses 2 simulations per candidate, ranks candidates, then allocates the remaining simulation budget equal to the control's total simulations for that decision across the top two candidates using an independent `v2|racing-refine` RNG namespace. The treatment selects using the pooled stage-1 plus refinement estimate. When fewer than two candidates are affordable, allocate the full remaining budget to the sole candidate.

## Matched controls
- Same fresh paired worlds.
- Same observational data and intervention budget 15.
- Same width-2 proposals and proposal RNG.
- Same environment RNG keyed by selected action.
- Same total planner simulations per decision as the width-2 control, up to integer allocation residue; any residue is deterministically assigned to the top-ranked candidate.
- Track actual planner simulations exactly.

## Primary metric
Paired terminal edge-error difference: racing minus baseline. Lower is better.

## Secondary metrics
MAP recovery, Brier score, posterior entropy, true-DAG mass, intervention spend, number of decisions, planner simulations, and action divergence.

## Initial screen
12 fresh worlds. No parameters are tuned from outcomes.

## Success / falsification
Promote only if racing has lower mean paired edge error without materially higher planner simulations and the improvement is accompanied by reduced selection instability/action divergence consistent with the mechanism. A null or adverse screen falsifies this specific racing allocation and redirects toward horizon/credit mismatch rather than retrying equivalent estimator-budget reallocations.