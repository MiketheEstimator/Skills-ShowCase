# EXP-002J4 Reproducibility Blocker

## Status
BLOCKED_EXECUTION_REPRODUCIBILITY

## Trigger
The queue requested exact resumption of EXP-002J4 from paired world 13 after a completed 12-world soft-intervention screen.

## Audit result
The repository contains the EXP-002 protocols, result JSONs, and checkpoints, but no executable EXP-002 benchmark runner or persisted per-world seed/state ledger capable of reproducing the exact 29,281-DAG inference engine and corrected nested width-1/width-2 controller used to generate the prior results.

The durable J4 checkpoint gives the aggregate n=12 result and states that execution should resume atomically from paired world 13, but it does not contain the actual 12 completed world seeds, canonical world generator, proposal RNG mapping, posterior likelihood implementation, action-cost function, or per-pair serialized state.

## Why execution was not guessed
WORKER_PROTOCOL requires matched resources, paired-world comparisons, preserved negative results, and checkpoint resumption. Generating worlds 13-48 with a newly invented engine would make the powered result non-comparable to the n=12 screen and could create a false scientific conclusion.

## Recovery successor
Enqueue EXP-002R: Canonical benchmark reconstruction and regression certification.

EXP-002R must reconstruct a runnable benchmark only from durable invariants, then certify it against historical controls before it is allowed to resume J4. Minimum certification targets:

1. Enumerate exactly 29,281 DAGs on five labeled nodes.
2. Reproduce the five named designers and matched intervention-cost budget semantics documented in EXPERIMENT_PROTOCOL.md.
3. Implement strict nested proposal breadth: width-2 = exact width-1 base swarm + one independent extra swarm.
4. RNG-isolate world generation, proposal generation, planner simulation, and environment outcomes.
5. Persist every paired world seed and row atomically.
6. Regression-test the reconstructed engine against at least three historical aggregate controls (EXP-002M2, EXP-002F, and one transfer result). The reconstruction is certified only if differences are explainable by Monte Carlo uncertainty or if historical seed/state can be recovered.
7. If regression certification fails, do not resume J4; continue diagnosing engine ambiguity instead of tuning toward the historical numbers.

## Scientific interpretation
No new scientific conclusion about imperfect interventions is supported by this blocker. The existing 12-world J4 screen remains directionally favorable but unresolved and should not be upgraded, downgraded, or pooled with results from a non-certified engine.
