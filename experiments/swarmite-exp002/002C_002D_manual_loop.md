# SWARMITE Experiment 002C–002D Manual Loop

## 002C — Counterfactual Credit Assignment Pilot

Question: does leave-one-out marginal terminal credit improve experiment-policy learning relative to immediate information-gain reward or naive terminal credit?

Exact Bayesian hypothesis space: all 29,281 DAGs on five labeled nodes. Small pilot only (6 training worlds / 10 held-out worlds) under matched total intervention cost.

### Results

| Credit scheme | Mean expected edge error ↓ | Mean posterior entropy ↓ |
|---|---:|---:|
| Immediate IG/cost | 1.8145 | 3.8173 |
| Naive terminal equal credit | **1.5841** | 3.6679 |
| Leave-one-out marginal credit | 1.6207 | **3.6284** |

Leave-one-out credit changed preference toward INFO/RIVAL, but did not clearly dominate. Interaction effects between experiments remain unassigned; marginal contribution estimated by removing one experiment from a completed trajectory is noisy and path-dependent.

## 002D — Proposal-Level Value Pilot

Question: does ranking the concrete experiments proposed in parallel by all designers outperform selecting a designer identity?

Training labels used privileged simulator-only one-step structural improvement per cost. A ridge value model scored proposal features including epistemic entropy, remaining budget, proposal cost, intervention coverage, local edge uncertainty, experiment magnitude/size, and designer identity.

Pilot: 8 training worlds / 12 held-out worlds, exact 29,281-DAG posterior, matched total cost.

### Results

| Policy | Mean expected edge error ↓ | Mean entropy ↓ | Mean experiments |
|---|---:|---:|---:|
| COVERAGE | **1.2776** | **3.2625** | 6.92 |
| CHEAPEST | 1.3011 | 3.4845 | 10.00 |
| Proposal-value model | 1.4752 | 3.5203 | 8.83 |
| INFO proxy | 1.5282 | 3.6089 | 5.00 |
| RIVAL | 1.5851 | 3.6790 | 5.00 |
| FALSIFY | 2.0048 | 4.3245 | 10.00 |

Proposal-value selections: INFO 8, FALSIFY 37, CHEAPEST 32, RIVAL 0, COVERAGE 29.

## Interpretation

Proposal-level selection is directionally the correct architectural unit, but one-step labels remain too myopic. Neither retrospective leave-one-out credit nor one-step privileged proposal value captures interaction and downstream option value well enough to beat simple coverage in this small-world regime.

## Next queued experiment — 002E

Two-step proposal lookahead under exact Bayesian scoring and matched cost:

1. Each epistemic specialist proposes one concrete intervention.
2. For each first-step proposal, sample plausible outcomes from the posterior predictive distribution.
3. Update the exact DAG posterior for each sampled outcome.
4. Generate second-step proposals from the resulting posterior states.
5. Score the first proposal by expected terminal posterior quality after the best second step, including resource cost.
6. Compare against myopic INFOGAIN, coverage, cheapest, one-step proposal judge, and random controls on identical held-out worlds.

Primary criterion: expected edge error at matched total cost. Secondary: posterior entropy, exact true-DAG posterior mass, MAP recovery, and information gain per cost.

No superiority claim is supported by 002C or 002D; both are pilot-scale falsification/diagnostic runs.
