# Validation V3 — Matched-Seed and Transfer Tests

## Objective
Determine whether the v0.2 novelty/exploration policy truly dominates static information-gain, and whether any advantage transfers to a harder causal-world family.

## Matched-seed original-family test
2,000 matched hidden worlds, 10 variables, 20-intervention budget. Bootstrap 95% confidence intervals are paired novelty minus information-gain.

| Metric | Mean difference | 95% CI | Interpretation |
|---|---:|---:|---|
| Graph recovery | +0.0230 | [+0.0221, +0.0239] | Novelty reliably improves recovery |
| Information / cost | -0.00379 | [-0.01049, +0.00291] | No reliable efficiency difference |
| Experiments used | -0.948 | [-1.046, -0.850] | Novelty reliably stops about one intervention earlier |

## Harder transfer family
The transfer environment uses 14 variables, denser graphs, heterogeneous intervention costs, weaker causal signal, and higher observation noise.

| Policy | Graph recovery | Info / cost | Experiments |
|---|---:|---:|---:|
| Random | 82.28% | 1.070 | 25.0 |
| Information gain | 90.06% | 1.659 | 25.0 |
| Falsification | 86.48% | 1.679 | 25.0 |
| Cheapest | 85.69% | 1.691 | 25.0 |
| Novelty | **93.37%** | 1.601 | 25.0 |

Paired novelty minus information-gain on 1,000 transfer worlds:

- Graph recovery: +0.03305, 95% CI [+0.03084, +0.03536]
- Information / cost: -0.05796, 95% CI [-0.06382, -0.05184]

## Conclusion
There is no globally dominant fixed experiment-design role. Novelty/exploration improves causal recovery, but on the harder transfer family it pays a measurable efficiency cost. This falsifies the simple hypothesis that one learned role should replace all others.

## Experiment-design implication
The controller should learn a state-dependent or phase-dependent policy schedule instead of selecting one global role. The next experiment therefore searches hybrid schedules and evaluates them on independent held-out worlds.
