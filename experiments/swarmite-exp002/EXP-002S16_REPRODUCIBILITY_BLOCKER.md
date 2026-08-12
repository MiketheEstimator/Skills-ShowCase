# EXP-002S16 Reproducibility Blocker

## Disposition
`BLOCKED_EXECUTION_REPRODUCIBILITY`

The queue still identified S16 as RUNNING at protocol freeze, but a confirmation artifact had already been committed at 2026-08-11T14:14:50Z without a persisted executable runner or mechanics/screen lineage. During recovery, a newly committed explicit runner (`swarmite_exp002_s16_noise.py`) reproduced the protocol mechanics but generated materially different outcomes on the same confirmation seeds. The two result sets therefore cannot be pooled or treated as interchangeable.

The likely source is under-specified Student-t noise execution semantics/RNG consumption (for example drawing a vector of innovations before topological traversal versus drawing innovations inline). Because the protocol freezes the distribution but not the exact executable noise kernel, the historical confirmation result is not source-addressable enough to resolve the discrepancy after exposure.

## Preserved evidence
- Historical confirmation artifact remains untouched: `EXP-002S16_CONFIRMATION_RESULT.json`.
- Recovery runner remains committed: `swarmite_exp002_s16_noise.py`.
- Recovery mechanics and screen traces remain preserved as diagnostic, nonpoolable artifacts.

## Scientific action
Do not select between conflicting S16 outcomes post hoc. Recover prospectively as EXP-002S16R using fresh seeds and an exact committed executable kernel before any efficacy worlds are exposed. This is an execution-integrity failure, not a scientific falsification of the S15 gate.