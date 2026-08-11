# EXP-002R4 — Breadth Novelty and Redundancy Mechanism Audit

## Question
Did benchmark-v2 width-2 fail because its extra proposal swarm mostly duplicates the width-1 action space?

## Frozen mechanics
Use the EXP-002R2 benchmark-v2 engine and source-addressed manifest without changing policy behavior. Diagnostic seeds are 6000 through 6011. Width-1 and width-2 retain matched intervention-cost budget 15.

## Instrumentation
Before every width-2 selection, record: exact `(target,setpoint)` overlap between swarm 0 and swarm 1, target overlap, whether the selected action came from the extra swarm, whether the extra swarm raises the maximum estimated EIG, and the incremental estimated EIG supplied by the extra swarm.

## Falsification rule
The simple redundancy explanation is weakened/falsified if the extra swarm frequently supplies the selected action and frequently raises the best estimated EIG, yet these novelty gains do not associate with terminal edge-error improvement.

## Result
Across 12 fresh diagnostic worlds, mean width2-width1 terminal edge-error delta was +0.2773. Per decision step, the two swarms shared 2.165 exact actions and 1.992 intervention targets on average, so overlap was substantial. However, the extra swarm supplied the selected action on 55.9% of steps and raised the maximum estimated EIG on 55.9% of steps. Mean incremental estimated EIG was +0.04023. At world level, mean incremental EIG had essentially no relationship to paired terminal benefit (Pearson r = -0.064).

## Conclusion
`COMPLETE_FALSIFIED_SIMPLE_REDUNDANCY`.

The second swarm is not failing merely because it adds no novel candidate value. It frequently wins the benchmark-v2 EIG judge, but those apparent local EIG gains fail to translate into terminal scientific improvement. A stronger next mechanism is estimator-selection bias: width-2 maximizes over twice as many Monte-Carlo EIG estimates, so low-simulation planner noise may create a winner's-curse effect.
