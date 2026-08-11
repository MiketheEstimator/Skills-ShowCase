# EXP-002R Provenance Audit

## Question
Can the historical EXP-002 executable benchmark be recovered from GitHub sufficiently to resume the historical EXP-002J4 screen exactly?

## Repository-history findings

- The initial EXP-002 exact-results commit added only `experiments/swarmite-exp002/README.md`.
- The immediately following protocol commit added only `experiments/swarmite-exp002/EXPERIMENT_PROTOCOL.md`.
- The recursive repository tree at that early protocol commit shows the EXP-002 directory containing only those two Markdown files. No Python runner, notebook, seed ledger, serialized worlds, or executable causal engine was committed with the benchmark.
- Later EXP-002 commits predominantly persist protocols, aggregate result JSON, checkpoints, and interpretation artifacts. Repository search and current-directory inspection likewise did not recover an exact historical runner.

## Independently recovered invariant

The original README states that the corrected benchmark used a fixed total intervention-cost budget of **15**. This is stronger provenance than the provisional canonical-v1 reconstruction assumption of budget 10 and is incorporated prospectively into the successor benchmark specification.

## Consequence

The historical J4 n=12 checkpoint cannot be continued at world 13 with exact experimental identity from repository state. Required missing identity includes the original SCM parameter generator, initial-data generator, action/cost semantics, likelihood implementation, designer proposal/tie-breaking mechanics, and historical per-world RNG mapping/state.

A clean untuned reconstruction can test whether durable invariants are sufficient to recreate compatible behavior, but failure of such a regression must not be repaired by fitting parameters to historical aggregate outputs.

## EXP-002R result

Canonical v1 passed exact-DAG enumeration/state-consistency checks but failed the behavioral breadth regression: on its first eight matched worlds, width-2 minus width-1 mean edge error was +0.2581, opposite the supported historical EXP-002M2 effect of -0.0987. Canonical v1 is therefore `FAILED_RECONSTRUCTION`.

## Scientific disposition

1. Preserve historical results as historical evidence.
2. Keep historical EXP-002J4 blocked from pooled continuation.
3. Do not tune a reconstruction until it reproduces historical aggregates.
4. Start a separately versioned fresh benchmark with all mechanics, seeds, raw rows, and checkpoints persisted before outcomes are inspected.
5. Re-establish the breadth baseline prospectively on that benchmark before testing soft-intervention transfer.
