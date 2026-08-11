# EXP-002R — Canonical Benchmark Reconstruction and Regression Certification

## Objective
Restore a reproducible executable EXP-002 benchmark without fabricating historical implementation details, then certify it before any powered continuation of EXP-002J4.

## Hypothesis
The durable protocol and result invariants are sufficient to reconstruct a canonical five-node exact-DAG benchmark whose behavior is consistent with prior controls and whose RNG/state serialization supports exact continuation.

## Fixed invariants
- Five labeled observed variables.
- Linear-Gaussian SCM baseline.
- Exact hypothesis space of 29,281 DAGs.
- Designers: INFOGAIN, FALSIFY, CHEAPEST, RIVAL, WEAKTIE.
- Same total intervention-cost budget across compared policies.
- Primary terminal metric: posterior expected edge error.
- Secondary metrics include true-DAG mass, MAP recovery, entropy, calibration, intervention count/spend, and compute.
- Strict nested breadth: width-2 contains the identical width-1 base proposal swarm plus one independent extra swarm.
- Independent RNG streams for world generation, proposal generation, planner simulation, and environment outcomes.

## Reconstruction stages
1. Build deterministic DAG enumeration and verify cardinality = 29,281.
2. Specify canonical SCM parameter generator and observational/interventional likelihood.
3. Implement exact posterior update and metrics.
4. Implement the five designers and action-cost semantics.
5. Implement width-1/width-2 nested proposal generation with RNG isolation.
6. Add atomic per-world JSONL checkpointing with seed/state lineage.
7. Run internal invariants and self-consistency tests.
8. Regression-certify against historical result artifacts without fitting parameters to those outputs.

## Regression certification
Use historical artifacts as external controls, not tuning targets. At minimum compare reconstructed benchmark behavior with:
- EXP-002M2_BREADTH_N48_RESULT.json
- EXP-002F_RNG_ISOLATED_RESULT.json
- EXP-002J_J2_CORRECTED_NESTED_BREADTH_RESULT.json

Certification outcome categories:
- CERTIFIED: implementation invariants pass and historical directional/scale behavior is compatible without post-hoc tuning.
- PARTIALLY_CERTIFIED: core engine passes but one or more historical behaviors cannot be verified because seeds/state were not persisted.
- FAILED_RECONSTRUCTION: material incompatibility indicates unresolved implementation ambiguity.

## Success criterion
Only CERTIFIED permits EXP-002J4 to return to RUNNING at world 13. PARTIALLY_CERTIFIED may run a fresh, separately labeled J4 replication from world 1, but may not pool with the historical n=12 screen.

## Anti-overfitting rule
Do not alter model parameters, proposal heuristics, costs, or RNG mapping merely to reproduce historical aggregate values. Any such change must be independently justified by protocol evidence.
