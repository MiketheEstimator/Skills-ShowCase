# EXP-002R2 — Fresh Benchmark v2 Preregistration and Calibration

## Objective
Create a new, fully reproducible five-node exact-DAG benchmark rather than attempting to impersonate the unrecoverable historical EXP-002 implementation. Establish its own strong-control baseline before any new transfer claim.

## Hypothesis
A protocol-grounded benchmark using genuine posterior-predictive experiment scoring, matched intervention-cost budget, strict nested proposal breadth, and isolated/persisted RNG state can produce a stable prospective comparison whose results are exactly resumable across worker runs.

## Independence from historical aggregate outcomes
Historical aggregates are evidence about the old benchmark, not tuning targets. Parameters in benchmark v2 are frozen prospectively. The only imported historical implementation invariant recovered independently from the original protocol/README is total intervention-cost budget = 15. No proposal coefficient, likelihood hyperparameter, world distribution, or RNG mapping may be adjusted merely to make width-2 win or reproduce an old numerical effect.

## Fixed benchmark-v2 mechanics
- Five labeled observed variables.
- Exact posterior support over all 29,281 DAGs.
- Linear-Gaussian SCM baseline with benchmark-v2 generator/version explicitly serialized.
- Total intervention-cost budget = 15 per arm.
- Ground truth hidden from proposal policies.
- Separate deterministic RNG streams for world generation, observational data, proposal generation, posterior-predictive simulation, and real intervention outcomes.
- Every world receives a persisted seed ledger and all frozen SCM parameters before policy evaluation.
- Width-2 is strictly nested: it contains the exact width-1 proposal swarm plus one independently seeded additional swarm.

## Material mechanism change from failed canonical v1
Canonical v1 ranked interventions with a heuristic edge-uncertainty proxy. Benchmark v2 must instead score epistemic proposals using genuine posterior-predictive expected information value: simulate possible intervention outcomes from the current posterior predictive distribution, update the exact DAG posterior, and estimate expected posterior entropy reduction per intervention cost. Other designers must be defined algorithmically and deterministically from current belief state, with tie-breaking keyed only to proposal RNG.

## Controls
At minimum:
- INFOGAIN fixed designer.
- CHEAPEST fixed designer.
- RANDOM matched-budget controller.
- Width-1 five-designer proposal portfolio.
- Width-2 nested ten-proposal portfolio.

## Primary metric
Paired terminal posterior expected edge error, width-2 minus width-1.

## Secondary metrics
- true-DAG posterior mass
- exact MAP recovery
- posterior entropy
- Brier calibration of edge marginals
- intervention count and realized spend
- posterior-predictive simulations and wall-clock compute

## Calibration stages
1. Implement and unit-test exact posterior, interventions, costs, proposal generation, and EIG scoring.
2. Persist a deterministic benchmark-v2 manifest including source hash, all hyperparameters, and RNG namespace map.
3. Run 4 paired mechanics worlds solely for invariant checking. Bugs may be fixed; scientific parameters may not be tuned from outcome direction.
4. Freeze code/manifest.
5. Run a fresh 12-world breadth screen.
6. If the primary interval/direction is unstable, extend according to a preregistered rule rather than changing mechanics.
7. Only after a stable baseline exists may a separately labeled soft-intervention transfer experiment be enqueued.

## Success criteria
EXP-002R2 completes when benchmark v2 is reproducibly executable, its mechanics tests pass, source/state lineage is persisted, and a prospective baseline result is recorded without tuning to historical results. Width-2 is not required to win. A null or adverse breadth result is a valid completion and redirects later experiments.

## Persistence requirement
Each completed world must be written atomically with world seed, SCM parameters, observational seed, proposal/planner/environment seed namespaces, arm traces, terminal posterior metrics, spend, and engine source/manifest hash. A watchdog must be able to resume at the next uncommitted world without regenerating prior state.
