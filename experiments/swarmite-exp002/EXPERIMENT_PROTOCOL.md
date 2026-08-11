# Experiment 002 Protocol

## Hypothesis
A learned experiment-selection policy can achieve greater information gain per unit cost on held-out causal worlds than static experiment-design heuristics.

## Ground truth
Five-variable linear Gaussian structural causal models. Ground-truth DAG is hidden from policies and visible only to the evaluator.

## Belief state
Exact posterior over all 29,281 DAGs on five labeled nodes.

## Designers
- INFOGAIN
- FALSIFY
- CHEAPEST
- RIVAL
- WEAKTIE

## Controls
- RANDOM
- each fixed designer
- discretized contextual bandit
- continuous LinUCB controller

## Resource control
All policies receive the same total intervention-cost budget, not the same number of experiments.

## Metrics
- posterior entropy reduction per cost
- exact true-DAG posterior mass
- exact MAP recovery
- edge precision / recall / F1
- Brier calibration
- posterior expected edge error
- interventions and total cost

## Success criterion
A learned controller must outperform the strongest static control on a held-out set with paired uncertainty intervals that exclude zero on the pre-registered primary metric.

## Current outcome
Unresolved. LinUCB is competitive but not significantly superior to static INFOGAIN.
