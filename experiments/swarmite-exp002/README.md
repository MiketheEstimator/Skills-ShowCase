# SWARMITE Experiment 002 — Exact Bayesian Adaptive Causal Discovery

This experiment uses an exact Bayesian posterior over all 29,281 DAGs on five nodes to test experiment-design policies under controlled causal ground truth.

## Most important correction
The first pass used a fixed number of interventions while rewarding information gain per cost. That was an invalid comparison because expensive policies could buy more evidence. The benchmark was corrected to a fixed total cost budget of 15.

## Current result
The original discretized contextual bandit does not outperform strong fixed designers.

A continuous LinUCB meta-controller improved substantially and learned a mixed strategy dominated by INFOGAIN, CHEAPEST, and FALSIFY. On 24 held-out hard worlds:

| Policy | Edge F1 | Info / Cost | Exact MAP |
|---|---:|---:|---:|
| INFOGAIN | 0.9870 | 0.4200 | 83.3% |
| LinUCB | 0.9851 | 0.4147 | 87.5% |
| WEAKTIE | 0.9780 | 0.4040 | 87.5% |
| RIVAL | 0.9704 | 0.4105 | 83.3% |
| RANDOM | 0.9497 | 0.3863 | 83.3% |

Paired bootstrap intervals between LinUCB and INFOGAIN span zero on all primary measures. There is no justified claim of superiority yet.

## Established findings
1. Equal resource budgets are required when reward is normalized by resource cost.
2. Exact-DAG identification and useful edge-structure recovery are separate scientific objectives.
3. Coarse discretized epistemic fingerprints lose too much state information.
4. Continuous contextual selection is viable but has not yet beaten the strongest static Bayesian design heuristic.
5. The next controller should evaluate proposals, not merely designers.

## Next loop
Every designer proposes an intervention in parallel. A proposal-level value model ranks the five concrete interventions using continuous epistemic features. That controller is then compared against myopic INFOGAIN and a 2-step Bayesian search under exactly matched cost.
