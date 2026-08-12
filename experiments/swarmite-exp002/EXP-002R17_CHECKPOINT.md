# EXP-002R17 Checkpoint

Status: RUNNING

## Completed this worker event
- Re-read persistent queue and worker protocol.
- Resumed EXP-002R17 before any PENDING item.
- Re-verified frozen training design: seeds 64001-64024; lambda grid {0, .25, .50, .75, 1.0}; lambda=0 matched control; selection constrained by mean Brier delta <= +0.005; no validation inspection before training selection is persisted.
- Committed `swarmite_exp002_r17.py`, a reproducible runner importing the frozen benchmark-v2 engine and applying the exact tempered generator-informed prior from the protocol.
- Runner emits per-world arm metrics and paired deltas for every lambda and applies the preregistered training selection rule.

## Execution state
No training world is counted complete in this checkpoint. The current ChatGPT execution sandbox cannot directly materialize the GitHub connector's source file into its Python runtime, and outbound raw-GitHub access from the runtime is unavailable. Fabricating or manually approximating benchmark execution would violate the reproducibility invariant.

## Exact resume action
Execute `swarmite_exp002_r17.py` against the committed `swarmite_benchmark_v2.py` for all training seeds 64001-64024 in one source-consistent environment. Persist raw rows and training summary atomically, freeze selected lambda, then and only then execute validation seeds 64101-64112 if allowed by the protocol. Do not inspect validation results before the training selection artifact exists.

Runner commit: `91f2e0574d80dc1807bb42f9e6962a8df9e0baa8`.
