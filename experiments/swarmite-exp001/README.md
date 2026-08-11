# SWARMITE Experiment 001 — Adaptive Causal Discovery

A computational pilot for testing whether a looped scientific controller can learn to design better interventions over repeated hidden causal worlds.

## Hypothesis
A controller that learns experiment-design preferences from realized information gain per unit cost will improve experiment efficiency on unseen causal systems relative to random selection and strong static heuristics.

## Scientific loop
1. Generate a hidden directed acyclic causal graph.
2. Initialize uncertain beliefs about candidate edges.
3. Select an experiment-design role: information gain, falsification, cheapest discriminating test, or novelty/exploration.
4. Select an intervention.
5. Run the intervention against simulator ground truth.
6. Update beliefs from noisy evidence.
7. Score information gain per cost.
8. Update the meta-policy.
9. Repeat until stop condition or budget.
10. Freeze the learned policy and evaluate on held-out worlds.

## Pilot 0.1
The first adaptive update rule did **not** beat static information gain. This was treated as a failed design, not a success.

## Pilot 0.2 redesign
Replaced runaway direct weights with an exploration-aware UCB meta-controller and separated training worlds from held-out evaluation worlds.

On the initial deterministic pilot (150 train / 100 held-out worlds, 10 variables, 20 intervention budget), the learned controller selected the novelty/exploration role. Held-out results:

| Policy | Graph recovery | Info/cost | Experiments |
|---|---:|---:|---:|
| Random | 91.24% | 0.949 | 19.82 |
| Information gain | 95.00% | 1.665 | 16.60 |
| Falsification | 94.82% | 1.603 | 18.02 |
| Cheapest | 94.84% | 1.627 | 17.63 |
| Learned/frozen novelty | **97.18%** | **1.670** | **15.41** |

These are pilot results from a simplified simulator, not evidence that the architecture generalizes beyond this world family.

## Next experiment
- matched seeded worlds across every policy
- confidence intervals and bootstrap comparison
- validation split separate from final test
- calibration score
- role ablations
- Think Harder operator-selection layer
- persistent experience ledger
- multi-agent blind replication / falsification
