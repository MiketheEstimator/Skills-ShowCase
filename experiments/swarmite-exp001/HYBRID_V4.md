# Hybrid Policy Search V4

## Question
Can a phase-dependent experiment-design schedule outperform either pure novelty or pure information-gain under a constrained multi-objective objective?

## Selection rule
On validation worlds, maximize graph recovery subject to retaining at least 99% of the best observed information-per-cost, then minimize experiment count. Evaluate the selected schedule on independent held-out worlds.

## Original causal family
The selector chose pure novelty (equivalent to an information→novelty schedule with switch at step 0).

Held-out result: 97.18% recovery, 1.657 info/cost, 15.67 experiments.

Interpretation: in the original family, the novelty policy remains on the Pareto frontier and no phase switch justified itself.

## Harder transfer family
The selector chose:

`NOVELTY for steps 1–18 → INFORMATION GAIN for steps 19–25`

Held-out result: 90.81% recovery, 1.638 info/cost, 25 experiments.

Matched held-out baselines on the same transfer seeds:

| Policy | Recovery | Info/cost | Experiments |
|---|---:|---:|---:|
| Information gain | 90.13% | 1.644 | 25 |
| Novelty | 93.49% | 1.582 | 25 |
| Hybrid 18→7 | 90.81% | 1.638 | 25 |

## Interpretation
The hybrid does not dominate both fixed policies. It occupies a compromise point: substantially recovers the efficiency of information-gain while retaining some recovery advantage. This is evidence for a Pareto frontier, not evidence for a universal schedule.

## Established finding
The experiment-design problem is multi-objective. A single scalar 'best policy' is under-specified unless the controller is given an explicit utility, constraint, or scientific priority such as maximum recovery, minimum cost, fastest falsification, or calibrated uncertainty.

## Next experiment
Replace fixed-role and fixed-phase schedules with a state-dependent controller whose state includes uncertainty, disagreement, remaining budget, intervention novelty, recent information gain, and prediction error. Evaluate policies against explicit utility profiles rather than one global reward.
