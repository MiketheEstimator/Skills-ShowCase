# EXP-002R3 — Powered Breadth Replication on Frozen Benchmark v2

## Objective
Resolve whether width-2 proposal breadth improves terminal causal recovery on the separately versioned, reproducible benchmark-v2 engine established by EXP-002R2.

## Frozen engine
Use `swarmite_benchmark_v2.py` at Git blob SHA `339e622169411861592d9c0e5abd4beadc6f2ac7` and `EXP-002R2_BENCHMARK_V2_MANIFEST.json` without scientific parameter changes.

## Design
Run 48 fresh paired worlds, seeds 5000 through 5047 inclusive. Compare strict nested width-1 vs width-2 portfolios at identical intervention-cost budget 15. World, observational, proposal, planner, and environment RNG namespaces remain isolated exactly as in benchmark v2.

## Primary metric
Paired terminal posterior expected edge error, width-2 minus width-1.

## Secondary metrics
Exact MAP recovery, true-DAG posterior mass, posterior entropy, edge-marginal Brier score, intervention count, spend, posterior-predictive simulation count, and compute ratio.

## Success / falsification
Breadth improvement is supported only if the paired bootstrap 95% CI for mean edge-error delta lies entirely below zero. It is falsified for this benchmark if the interval lies entirely above zero. Otherwise the effect is unresolved at n=48. MAP/Brier gains are secondary and cannot override an unresolved or adverse primary metric.

## Persistence
Persist every completed world with world seed, SCM parameters, RNG ledger, arm traces, terminal metrics, spend, and frozen engine/manifest identity. Checkpoint after completed world batches; never regenerate or pool a world under changed mechanics.

## Successor rule
If supported, enqueue a separately labeled soft-intervention transfer replication using benchmark v2. If falsified or unresolved, diagnose heterogeneity before any transfer claim; do not tune proposal roles from the test worlds.
