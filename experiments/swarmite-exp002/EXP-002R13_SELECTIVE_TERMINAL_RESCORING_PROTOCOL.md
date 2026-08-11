# EXP-002R13 — Selective Terminal Rescoring of One-Step Shortlist

## Motivation
EXP-002R12 falsified exhaustive full-horizon terminal VOI as a general ranking mechanism: mean rank alignment worsened and compute averaged 37.7x the one-step audit. However, its selected argmax reduced terminal edge-error regret in 4/6 worlds and reduced mean regret from 0.312 to 0.122. This suggests terminal information may be useful only for resolving a small decision boundary, not for globally ranking all ten actions.

## Hypothesis
Applying terminal rollout only to a small high-precision one-step-EIG shortlist will preserve the R12 terminal-regret signal while avoiding pathological compute and without requiring terminal VOI to globally rank all actions.

## Frozen design
Use 12 fresh benchmark-v2 worlds, seeds 60001 through 60012. Start from 30 passive observations. Score the same ten fixed hard interventions (5 targets x {-2,+2}) with the existing 30-simulation one-step DAG-entropy EIG/cost audit. Form a top-3 shortlist by that score. Only those three candidates receive budget-aware terminal rescoring, using 4 posterior-predictive remaining-budget rollouts per candidate with the frozen width-1 continuation controller and negative summed edge-marginal uncertainty as terminal utility. Select the candidate with best terminal score among the top three.

## Matched control
Control selects the ordinary 30-simulation one-step-EIG argmax. Treatment selects the terminal-rescored action from the frozen top-3 shortlist. For each arm, force its chosen first real intervention, then spend the remaining intervention budget using the same frozen width-1 controller. Use isolated RNG namespaces by world, arm, rollout, action and continuation step.

## Primary endpoint
Paired terminal edge error, treatment minus control. Lower is better.

## Secondary endpoints
MAP recovery, Brier score, true-DAG posterior mass, terminal edge-error regret versus the best of the ten realized first-action counterfactuals, planner simulations, and wall-clock compute.

## Success criterion
Promote selective terminal rescoring only if all hold: (1) mean paired terminal edge-error delta <= -0.10; (2) treatment wins edge error in at least 8/12 worlds; (3) Brier does not worsen by more than +0.005 on average; and (4) total planner simulation count is <=10x the 30-simulation one-step audit. Otherwise falsify and redirect away from terminal rollout search.

## Checkpoint discipline
Persist every world atomically before starting the next. The action set, top-3 shortlist size, 4 rollout count, seeds, continuation controller, endpoints and promotion criteria are frozen before prospective execution. No R12 world may be pooled into R13.