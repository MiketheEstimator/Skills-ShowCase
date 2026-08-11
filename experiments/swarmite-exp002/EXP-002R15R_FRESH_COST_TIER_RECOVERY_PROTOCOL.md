# EXP-002R15R — Reproducible Cost-Tier Recovery

## Status
Protocol frozen before prospective seeds 62001-62012.

## Purpose
Recover the scientifically unresolved R15 cost-tier hypothesis after its execution lineage failed reproducibility. Historical R15 seeds 61001-61003 are permanently nonpoolable.

## Frozen mechanics
Use committed `swarmite_benchmark_v2.py` and `swarmite_exp002_r15r.py`. Start from 30 passive observations. Audit the same ten fixed interventions (five targets x {-2,+2}) with 30 posterior-predictive EIG simulations per action. Form the top-3 shortlist. Only candidates whose target intervention cost is no greater than the one-step argmax target cost are eligible for terminal rescoring. Rescore each eligible action with four full remaining-budget posterior-predictive rollouts using the frozen width-1 continuation controller. Simulated histories refit the family models after every synthetic intervention. Terminal utility is negative summed edge-marginal uncertainty. Treatment chooses the best eligible terminal score; control chooses one-step EIG argmax.

Real arms use common-random-number namespaces keyed by seed, step, target and setpoint. Therefore if control and treatment select the same first action, their entire real trajectory and terminal metrics are exactly identical. Planner RNG is independent from environment RNG.

## Seeds
62001-62012, with no reuse of historical R15 observations.

## Endpoints
Primary: paired terminal edge error, treatment minus control. Secondary: Brier, true-DAG mass, MAP recovery, override rate, harmful overrides >0.10 edge-error units, and selection compute relative to the 300-simulation one-step audit.

## Promotion criteria
Promote only if all hold: mean paired edge-error delta <= -0.10; no more than 2/12 worlds worsen by >0.10; mean Brier delta <= +0.005; mean selection-compute ratio <=10x. Otherwise falsify the cost-tier gate and redirect away from selective terminal-rescoring mechanisms.

## Checkpoint discipline
Each completed seed is an atomic result. The runner and RNG namespaces are committed before results are interpreted.