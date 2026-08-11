# Experiment Protocol 001

## Objective
Determine whether looped meta-learning over experiment-design strategies improves causal discovery efficiency.

## Independent variable
Experiment-selection policy: random, information gain, falsification, cheapest-test, novelty/exploration, learned/frozen meta-policy.

## Dependent variables
1. Final graph-recovery accuracy.
2. Information gain per unit intervention cost.
3. Number of interventions used.
4. Experiment-role reward estimates learned during meta-training.

## Scientific loop
Hidden world → uncertain state → parallel candidate design strategies → selected intervention → noisy observation → belief update → information-gain score → meta-policy update → next intervention / next world.

## Controls
All policies use the same simulator family, world size, intervention budget, noise model, and stop condition. Version 0.2 uses deterministic world seeds and a disjoint held-out test set.

## Pilot 0.1 result
The original direct adaptive-weight update underperformed the strongest static heuristic and drove the controller toward an unstable falsification preference. This result triggered redesign.

## Pilot 0.2 redesign
Use an upper-confidence-bound meta-controller during training to balance exploitation of high-reward experiment-design roles with continued exploration. Freeze the best learned role before held-out testing.

## Success criterion
The learned/frozen policy must outperform random selection and at least one strong static heuristic on held-out information gain per cost without reducing graph recovery. Secondary success is fewer interventions for equal or better accuracy.

## Falsification criterion
If the learned policy fails to exceed static heuristics under matched held-out worlds and compute, the hypothesis is weakened or rejected for this simulator family.

## Pilot 0.2 observation
On the initial 150-world training / 100-world held-out run, the meta-controller selected novelty/exploration. Held-out graph recovery was 97.18% with 1.670 information/cost and 15.41 interventions, versus 95.00%, 1.665, and 16.60 for static information-gain. This is provisional evidence only.

## Required next loop
1. Add bootstrap confidence intervals and paired tests.
2. Add a validation split so the final test set remains untouched during architecture iteration.
3. Add calibration and structural-distance metrics.
4. Ablate each design role.
5. Introduce Think Harder operators as a larger cognitive action space.
6. Add blind parallel replicator, falsifier, and evidence-auditor agents.
7. Persist state → operator → experiment → observation → reward trajectories as the experience ledger.
8. Test transfer to a second simulator family before claiming general experiment-design improvement.
