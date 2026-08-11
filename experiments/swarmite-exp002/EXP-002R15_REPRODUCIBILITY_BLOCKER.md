# EXP-002R15 Reproducibility Blocker

## Disposition
`BLOCKED_EXECUTION_REPRODUCIBILITY`

The queue checkpoint stated that no R15 prospective worlds had completed, but the repository already contained three atomic artifacts for seeds 61001-61003. Those artifacts encode shortlist/action selections and planner-simulation counts that cannot be regenerated from the committed `swarmite_benchmark_v2.py` plus the frozen R15 protocol alone.

The exact R15 execution kernel, RNG namespaces, terminal-rollout implementation, and continuation-state update mechanics were not committed. A reconstruction attempt using only the committed benchmark/protocol failed regression against the persisted worlds, including shortlist/action differences. Therefore seeds 61001-61003 are preserved as historical evidence but are permanently nonpoolable with any new R15 observations.

No scientific claim about the R15 cost-tier hypothesis is inferred from this execution failure. Recovery proceeds as EXP-002R15R on fresh seeds with a committed source-addressed runner and explicit RNG namespaces before prospective execution.