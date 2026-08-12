# Model-Based Planner V6

## Hypothesis
A short-horizon model-based controller can improve experiment selection by having each scientific role propose an intervention and then evaluating those candidates across sampled plausible causal worlds before acting.

## Method
At each step, information-gain, falsification, cheapest-test, and novelty roles proposed candidate interventions. The planner sampled hidden graphs from current edge beliefs, simulated intervention outcomes using an internal nominal causal/noise model, and chose the candidate with highest expected profile utility. The internal simulator was deliberately not matched exactly to either evaluation environment.

## Result
The hypothesis was not supported. The planner did not beat the strongest fixed heuristic.

### Original family
Discovery planner: 95.94% recovery, 1.623 info/cost, 17.09 experiments.
Novelty baseline: 97.09%, 1.649, 15.86.

### Transfer family
Discovery planner: 89.77% recovery, 1.681 info/cost.
Information-gain baseline: 90.16%, 1.678.
Novelty baseline: 93.41%, 1.617.

Efficiency and balanced planner variants were also inferior to at least one fixed baseline.

## Interpretation
A planner is only as useful as its world model and planning horizon. One-step counterfactual search under a misspecified nominal simulator can confidently optimize the wrong surrogate. More planning is not inherently better than a robust heuristic.

## Established finding
Model-based experiment planning should carry explicit world-model uncertainty, calibrate itself from observed prediction errors, and search over longer trajectories before it is expected to outperform simple policies.

## Next design
V7 should treat the internal world model itself as a hypothesis ensemble. Maintain multiple candidate environment models with posterior weights, plan interventions across the ensemble, use prediction error to reweight models, and choose experiments that jointly improve domain understanding and discriminate among world models. This turns model uncertainty into part of the scientific state rather than hiding it inside one simulator.
