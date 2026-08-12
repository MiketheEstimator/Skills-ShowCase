# EXP-002R12 — Budget-Aware Terminal Value-of-Information Screen

## Motivation
EXP-002R11 found measurable posterior-predictive discrepancies but essentially no relationship between calibration error and terminal recovery failure. Earlier work also falsified low-simulation estimator repair, simple edge-entropy utility replacement, and proposal diversification. The remaining live mechanism is horizon mismatch: the planner optimizes immediate entropy reduction per cost rather than expected scientific state after the remaining intervention budget is spent.

## Hypothesis
A budget-aware rollout value that scores an intervention by expected terminal edge uncertainty after spending the remaining budget will align better with realized terminal causal recovery than high-precision one-step EIG.

## Design
Use 6 fresh fixed worlds, seeds 59001 through 59006, under the frozen benchmark-v2 engine. Build the normal posterior from 30 passive samples. Evaluate the same 10 fixed hard interventions formed by 5 targets crossed with setpoints {-2,+2}. For each candidate, estimate two scores without ground-truth access: (1) the existing 30-simulation DAG-entropy EIG/cost score; and (2) a budget-aware terminal score from 8 posterior-predictive rollouts. Each rollout forces the candidate first, then spends the remaining intervention budget with the frozen width-1 controller, and scores the terminal posterior by negative summed edge-marginal uncertainty. RNG namespaces are isolated by world, action, rollout, and continuation step.

## Matched realized evaluation
For each candidate separately, force that candidate as the first real intervention and spend the remaining real intervention budget with the same frozen width-1 controller. Ground truth is revealed only after each rollout to score terminal edge error, Brier score, true-DAG mass, and MAP recovery.

## Primary diagnostic
Within each world compare Spearman rank correlation with negative realized terminal edge error for budget-aware terminal VOI versus 30-simulation one-step EIG. Primary screen statistic is the paired world-level change in rank correlation.

## Secondary diagnostics
- Terminal edge-error rank and regret of each score's argmax.
- Brier and true-DAG-mass rank alignment.
- Planner simulation count and wall-clock compute.

## Success criterion
Promote budget-aware terminal VOI only if mean rank-alignment improves by at least +0.15 and terminal-regret improves in at least 4 of 6 worlds without pathological compute blow-up above 25x the one-step audit. Otherwise falsify this mechanism at screen and redirect away from deeper planning.

## Checkpoint discipline
Persist each world atomically. Seeds, action set, rollout count, continuation controller, terminal utility, and success criterion are frozen before execution.